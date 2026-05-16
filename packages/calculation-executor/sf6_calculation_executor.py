#!/usr/bin/env python3
"""Deterministic arithmetic trace executor for SF6 maintainer workflows."""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, DivisionByZero, InvalidOperation, getcontext
from pathlib import Path
from typing import Any


EXECUTOR_ID = "sf6_calculation_executor.py@v1"
TRACE_SCHEMA_VERSION = "sf6-calculation-trace/v1"
AUTHORITY_STATUS = [
    "not_sf6_authority",
    "not_formula_authority",
    "not_current_fact_authority",
]


class CalculationError(Exception):
    """Raised when arithmetic cannot produce a valid trace step."""


def decimal_to_string(value: Decimal) -> str:
    if value.is_zero():
        return "0"
    normalized = value.normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def parse_decimal(name: str, raw: Any) -> Decimal:
    if isinstance(raw, bool):
        raise CalculationError(f"{name} must be a decimal string or number")
    try:
        return Decimal(str(raw))
    except (InvalidOperation, ValueError) as exc:
        raise CalculationError(f"{name} is not a valid decimal: {raw}") from exc


def resolve_input(name: str, values: dict[str, Decimal]) -> Decimal:
    if name not in values:
        raise CalculationError(f"missing input or previous output: {name}")
    return values[name]


def require_input_count(step_id: str, inputs: list[str], expected: int) -> None:
    if len(inputs) != expected:
        raise CalculationError(f"{step_id} requires {expected} input(s)")


def compute_operation(
    operation_kind: str,
    inputs: list[str],
    values: dict[str, Decimal],
    step_id: str,
) -> tuple[Decimal, str]:
    resolved = [resolve_input(input_name, values) for input_name in inputs]

    if operation_kind in {"add", "sum"}:
        if not resolved:
            raise CalculationError(f"{step_id} requires at least one input")
        return sum(resolved, Decimal("0")), "sum supplied inputs"

    if operation_kind == "subtract":
        require_input_count(step_id, inputs, 2)
        return resolved[0] - resolved[1], "subtract second input from first"

    if operation_kind == "multiply":
        if not resolved:
            raise CalculationError(f"{step_id} requires at least one input")
        result = Decimal("1")
        for value in resolved:
            result *= value
        return result, "multiply supplied inputs"

    if operation_kind == "divide":
        require_input_count(step_id, inputs, 2)
        if resolved[1].is_zero():
            raise CalculationError(f"{step_id} cannot divide by zero")
        try:
            return resolved[0] / resolved[1], "divide first input by second"
        except DivisionByZero as exc:
            raise CalculationError(f"{step_id} cannot divide by zero") from exc

    if operation_kind == "min":
        if not resolved:
            raise CalculationError(f"{step_id} requires at least one input")
        return min(resolved), "minimum of supplied inputs"

    if operation_kind == "max":
        if not resolved:
            raise CalculationError(f"{step_id} requires at least one input")
        return max(resolved), "maximum of supplied inputs"

    if operation_kind == "difference":
        require_input_count(step_id, inputs, 2)
        return abs(resolved[0] - resolved[1]), "absolute difference"

    if operation_kind == "compare":
        require_input_count(step_id, inputs, 2)
        if resolved[0] < resolved[1]:
            return Decimal("-1"), "first input is less than second"
        if resolved[0] > resolved[1]:
            return Decimal("1"), "first input is greater than second"
        return Decimal("0"), "inputs are equal"

    if operation_kind == "percent_of":
        require_input_count(step_id, inputs, 2)
        return (resolved[0] * resolved[1]) / Decimal("100"), (
            "first input as percent of second input"
        )

    raise CalculationError(f"unsupported operation: {operation_kind}")


def determine_block_status(request: dict[str, Any]) -> tuple[str | None, list[str]]:
    hold_reasons: list[str] = []
    intent = request.get("calculation_intent")
    formula_status = request.get("formula_status")
    rounding_status = request.get("rounding_status")
    input_status = request.get("input_status")

    if input_status == "hold":
        hold_reasons.append("input authority is missing or held")
        return "blocked_missing_input_authority", hold_reasons

    if request.get("route_status") == "ambiguous":
        hold_reasons.append("route, hit, action, timing, or move mapping is ambiguous")
        return "blocked_ambiguous_route", hold_reasons

    if intent == "accepted_formula_execution" and formula_status != "accepted":
        hold_reasons.append("accepted formula policy is required")
        return "blocked_missing_formula_policy", hold_reasons

    if request.get("rounding_required") and rounding_status != "accepted":
        hold_reasons.append("accepted rounding policy is required")
        return "blocked_missing_rounding_policy", hold_reasons

    return None, hold_reasons


def determine_success_status(request: dict[str, Any], operations_run: bool) -> str:
    if not operations_run:
        return "not_run"

    if request.get("input_status") == "hypothetical" or request.get("formula_status") == "hypothetical":
        return "hypothetical_arithmetic_only"

    if (
        request.get("calculation_intent") == "accepted_formula_execution"
        and request.get("input_status") == "accepted"
        and request.get("formula_status") == "accepted"
        and request.get("rounding_status") in {"accepted", "not_applicable"}
    ):
        return "accepted_formula_execution"

    return "trace_generated"


def build_trace(request: dict[str, Any]) -> dict[str, Any]:
    getcontext().prec = int(request.get("decimal_precision", 28))

    input_values_raw = request.get("input_values", {})
    if not isinstance(input_values_raw, dict):
        input_values_raw = {}

    values: dict[str, Decimal] = {}
    input_values: dict[str, str] = {}
    status, hold_reasons = determine_block_status(request)

    try:
        for name, raw in input_values_raw.items():
            parsed = parse_decimal(name, raw)
            values[name] = parsed
            input_values[name] = decimal_to_string(parsed)
    except CalculationError as exc:
        status = "invalid_input"
        hold_reasons.append(str(exc))

    operation_steps: list[dict[str, Any]] = []
    output_values: dict[str, str] = {}

    if status is None:
        try:
            operations = request.get("operations", [])
            if not isinstance(operations, list):
                raise CalculationError("operations must be an array")

            for index, operation in enumerate(operations, start=1):
                if not isinstance(operation, dict):
                    raise CalculationError(f"operation {index} must be an object")
                step_id = str(operation.get("step_id") or f"step-{index}")
                operation_kind = str(operation.get("operation_kind", ""))
                inputs = operation.get("inputs", [])
                if not isinstance(inputs, list) or not all(isinstance(item, str) for item in inputs):
                    raise CalculationError(f"{step_id} inputs must be an array of names")
                output_name = str(operation.get("output_name") or step_id)

                result, notes = compute_operation(operation_kind, inputs, values, step_id)
                result_text = decimal_to_string(result)
                values[output_name] = result
                output_values[output_name] = result_text
                operation_steps.append(
                    {
                        "step_id": step_id,
                        "operation_kind": operation_kind,
                        "inputs_used": [
                            {"name": input_name, "value": decimal_to_string(resolve_input(input_name, values))}
                            for input_name in inputs
                        ],
                        "output": {"name": output_name, "value": result_text},
                        "rounding_applied": "none",
                        "policy_ref": operation.get("policy_ref"),
                        "notes": operation.get("notes", notes),
                    }
                )

            status = determine_success_status(request, bool(operation_steps))
        except CalculationError as exc:
            status = "invalid_input"
            hold_reasons.append(str(exc))

    public_answer_allowed = bool(
        status == "accepted_formula_execution"
        and request.get("public_answer_allowed") is True
        and not hold_reasons
    )

    limitations = [
        "Executor output is an arithmetic trace, not SF6 authority.",
        "The executor does not look up SF6 facts, formulas, rounding rules, or current patch data.",
    ]
    if status != "accepted_formula_execution":
        limitations.append("Trace must not support public current-fact answers.")

    return {
        "trace_id": request.get("trace_id", "calculation-trace"),
        "trace_schema_version": TRACE_SCHEMA_VERSION,
        "executor_id": EXECUTOR_ID,
        "executor_role": "calculation_executor",
        "executor_authority_status": AUTHORITY_STATUS,
        "calculation_intent": request.get("calculation_intent", "hypothetical_arithmetic_check"),
        "question_scope": request.get("question_scope", ""),
        "input_values": input_values,
        "input_authority_refs": request.get("input_authority_refs", []),
        "input_status": request.get("input_status", "hypothetical"),
        "formula_policy_ref": request.get("formula_policy_ref"),
        "formula_status": request.get("formula_status", "hypothetical"),
        "rounding_policy_ref": request.get("rounding_policy_ref"),
        "rounding_status": request.get("rounding_status", "not_applicable"),
        "operation_steps": operation_steps,
        "output_values": output_values,
        "status": status,
        "public_answer_allowed": public_answer_allowed,
        "generated_reference_allowed": False,
        "accepted_current_fact_authority": False,
        "uncertainty_or_hold_reasons": hold_reasons,
        "created_by": request.get("created_by", "unknown"),
        "created_at": request.get("created_at"),
        "repo_revision": request.get("repo_revision"),
        "limitations": limitations,
    }


def load_request(path: str | None) -> dict[str, Any]:
    if path:
        text = Path(path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object")
    return data


def invalid_request_trace(message: str) -> dict[str, Any]:
    return {
        "trace_id": "invalid-request",
        "trace_schema_version": TRACE_SCHEMA_VERSION,
        "executor_id": EXECUTOR_ID,
        "executor_role": "calculation_executor",
        "executor_authority_status": AUTHORITY_STATUS,
        "calculation_intent": "hypothetical_arithmetic_check",
        "question_scope": "Invalid calculation request.",
        "input_values": {},
        "input_authority_refs": [],
        "input_status": "hold",
        "formula_policy_ref": None,
        "formula_status": "hold",
        "rounding_policy_ref": None,
        "rounding_status": "hold",
        "operation_steps": [],
        "output_values": {},
        "status": "invalid_input",
        "public_answer_allowed": False,
        "generated_reference_allowed": False,
        "accepted_current_fact_authority": False,
        "uncertainty_or_hold_reasons": [message],
        "created_by": "sf6_calculation_executor.py",
        "created_at": None,
        "repo_revision": None,
        "limitations": ["Input request could not be parsed."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic SF6 calculation trace arithmetic.")
    parser.add_argument("--input", help="Path to request JSON. Reads stdin when omitted.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    try:
        request = load_request(args.input)
        trace = build_trace(request)
    except Exception as exc:  # noqa: BLE001 - deterministic error trace for CLI callers.
        trace = invalid_request_trace(str(exc))

    indent = 2 if args.pretty else None
    print(json.dumps(trace, ensure_ascii=False, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
