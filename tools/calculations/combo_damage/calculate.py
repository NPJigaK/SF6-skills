#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from sympy import Rational, floor
from sympy import __version__ as sympy_version


CALCULATOR_NAME = "tools.calculations.combo_damage"
CALCULATOR_VERSION = "combo_damage/v1"
FORMULA_ID = "sf6_combo_damage_floor_sum_v1"
ROUNDING_POLICY_FLOOR_EACH_HIT = (
    "floor_each_hit_after_condition_multiplier_and_effective_scaling"
)
OUTPUT_TYPE = "combo_damage_calculation"
SCHEMA_VERSION = 1
_RATIONAL_PATTERN = re.compile(r"^-?\d+(?:/-?\d+)?$")
_AGGREGATED_HIT_SPAN_PATTERN = re.compile(r"^\d+\s*-\s*\d+$")
HIT_DAMAGE_GRANULARITY_VALUES = {"per_hit", "damage_segment", "move_total"}
OPTIONAL_HIT_TRACE_FIELDS = (
    "attack_step",
    "scaling_note",
    "damage_granularity",
    "segment_type",
)
REQUIRED_TOP_LEVEL_FIELDS = [
    "input_type",
    "schema_version",
    "source_paths",
    "authority",
    "rounding_policy",
    "hits",
]
REQUIRED_HIT_FIELDS = [
    "hit_index",
    "move",
    "base_damage",
    "condition_multiplier",
    "effective_scaling",
    "source_paths",
]
REQUIRED_AUTHORITY_FIELDS = [
    "authority_type",
    "confidence",
    "source_paths",
    "validation_status",
    "review_status",
]
DETERMINISTIC_AUTHORITY_TYPES = {
    "source_backed_ledger",
    "regression_fixture",
    "validated_fixture",
}


def load_ledger(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_sha256(ledger: dict[str, Any]) -> str:
    canonical = json.dumps(
        ledger,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def exact_rational(value: Any, field_name: str) -> Rational:
    if isinstance(value, int):
        return Rational(value, 1)
    if isinstance(value, str) and _RATIONAL_PATTERN.match(value):
        return Rational(value)
    raise ValueError(f"{field_name} must be an integer or exact rational string")


def require_fields(row: dict[str, Any], fields: list[str], context: str) -> None:
    missing = [field for field in fields if field not in row]
    if missing:
        raise ValueError(f"{context} is missing required fields: {', '.join(missing)}")


def require_non_empty_string_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field_name} must be a non-empty list")
    if not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field_name} must contain only non-empty strings")


def validate_authority(authority: Any) -> None:
    if not isinstance(authority, dict):
        raise ValueError("authority must be an object")
    require_fields(authority, REQUIRED_AUTHORITY_FIELDS, "authority")
    authority_type = authority["authority_type"]
    if authority_type not in DETERMINISTIC_AUTHORITY_TYPES:
        raise ValueError(
            "authority_type must be source_backed_ledger, "
            "regression_fixture, or validated_fixture"
        )
    if authority["confidence"] not in {"low", "medium", "high"}:
        raise ValueError("authority.confidence must be low, medium, or high")
    require_non_empty_string_list(authority["source_paths"], "authority.source_paths")
    for field in ("validation_status", "review_status"):
        if not isinstance(authority[field], str) or not authority[field]:
            raise ValueError(f"authority.{field} must be a non-empty string")


def validate_hit_trace_fields(hit: dict[str, Any], context: str) -> None:
    hit_span = hit.get("hit_span")
    if isinstance(hit_span, str) and _AGGREGATED_HIT_SPAN_PATTERN.match(hit_span):
        raise ValueError(
            f"{context}.hit_span must identify one damaging hit or segment, "
            "not an aggregated hit range"
        )
    damage_granularity = hit.get("damage_granularity")
    if damage_granularity is not None and damage_granularity not in (
        HIT_DAMAGE_GRANULARITY_VALUES
    ):
        raise ValueError(
            f"{context}.damage_granularity must be per_hit, "
            "damage_segment, or move_total"
        )
    segment_type = hit.get("segment_type")
    if segment_type is not None and (
        not isinstance(segment_type, str) or not segment_type
    ):
        raise ValueError(f"{context}.segment_type must be a non-empty string")
    if damage_granularity == "move_total" and segment_type is None:
        raise ValueError(f"{context}.segment_type is required for move_total")


def calculate_hit_damage(hit: dict[str, Any]) -> int:
    base_damage = exact_rational(hit["base_damage"], "base_damage")
    condition_multiplier = exact_rational(
        hit["condition_multiplier"],
        "condition_multiplier",
    )
    effective_scaling = exact_rational(hit["effective_scaling"], "effective_scaling")
    if base_damage < 0 or condition_multiplier < 0 or effective_scaling < 0:
        raise ValueError("damage factors must be nonnegative")
    return int(floor(base_damage * condition_multiplier * effective_scaling))


def calculate_combo_damage(ledger: dict[str, Any]) -> dict[str, Any]:
    require_fields(ledger, REQUIRED_TOP_LEVEL_FIELDS, "ledger")
    if ledger.get("rounding_policy") != ROUNDING_POLICY_FLOOR_EACH_HIT:
        raise ValueError(f"unsupported rounding_policy: {ledger.get('rounding_policy')!r}")
    if ledger.get("input_type") != "combo_damage_ledger":
        raise ValueError(f"unsupported input_type: {ledger.get('input_type')!r}")
    if ledger.get("schema_version") != 1:
        raise ValueError(
            f"unsupported ledger schema_version: {ledger.get('schema_version')!r}"
        )
    require_non_empty_string_list(ledger["source_paths"], "source_paths")
    validate_authority(ledger["authority"])

    hits = ledger.get("hits")
    if not isinstance(hits, list) or not hits:
        raise ValueError("ledger hits must be a non-empty list")

    rows: list[dict[str, Any]] = []
    cumulative_damage = 0
    for offset, hit in enumerate(hits, start=1):
        if not isinstance(hit, dict):
            raise ValueError(f"hit {offset} must be an object")
        require_fields(
            hit,
            REQUIRED_HIT_FIELDS,
            f"hit {offset}",
        )
        require_non_empty_string_list(hit["source_paths"], f"hit {offset}.source_paths")
        validate_hit_trace_fields(hit, f"hit {offset}")
        hit_damage = calculate_hit_damage(hit)
        cumulative_damage += hit_damage
        rows.append(
            {
                "hit_index": hit["hit_index"],
                **({"hit_span": hit["hit_span"]} if "hit_span" in hit else {}),
                **{
                    field: hit[field]
                    for field in OPTIONAL_HIT_TRACE_FIELDS
                    if field in hit
                },
                "move": hit["move"],
                "base_damage": hit["base_damage"],
                "condition_multiplier": hit["condition_multiplier"],
                "effective_scaling": hit["effective_scaling"],
                "hit_damage": hit_damage,
                "cumulative_damage": cumulative_damage,
                "source_paths": hit["source_paths"],
            }
        )

    expected_total = ledger.get("expected_total_damage")
    result: dict[str, Any] = {
        "output_type": OUTPUT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "title": ledger.get("title", ""),
        "calculator": {
            "name": CALCULATOR_NAME,
            "version": CALCULATOR_VERSION,
            "sympy_version": sympy_version,
        },
        "source": {
            "source_paths": ledger["source_paths"],
            "input_sha256": ledger_sha256(ledger),
            "authority": ledger["authority"],
        },
        "rounding_policy": ROUNDING_POLICY_FLOOR_EACH_HIT,
        "formula": {
            "id": FORMULA_ID,
            "description": (
                "For each source-backed hit or explicit damage segment, "
                "floor(base_damage * condition_multiplier * effective_scaling), "
                "then sum hit_damage."
            ),
        },
        "rows": rows,
        "total_damage": cumulative_damage,
    }
    if expected_total is not None:
        result["expected_total_damage"] = expected_total
        result["matches_expected"] = cumulative_damage == expected_total
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = calculate_combo_damage(load_ledger(args.ledger))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
