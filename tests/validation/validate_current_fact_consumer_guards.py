from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from sf6_knowledge_coach.current_fact_guards import (
    NON_SCALAR_OR_BLOCKED_CALCULATION_STATUSES,
    SCALAR_CALCULATION_INPUT_STATUSES,
    is_scalar_calculation_input,
)


ROOT = Path(__file__).resolve().parents[2]
COVERAGE_PATH = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"
ELIGIBLE_STATUS = "eligible_only_after_domain_source_and_unit_checks"
APPROVED_STATUSES = {
    ELIGIBLE_STATUS,
    "annotated_candidate_not_calculation_safe",
    "parsed_range_not_single_value_calculation_safe",
    "review_required_not_calculation_safe",
    "enum_only_not_arithmetic",
    "raw_preserved_not_calculation",
    "not_numeric_authority",
    "out_of_scope_not_emitted",
}


def main() -> int:
    errors: list[str] = []
    if not COVERAGE_PATH.exists():
        errors.append(f"Missing {COVERAGE_PATH.relative_to(ROOT)}")
        return _finish(errors)

    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    _validate_guard_status_sets(errors)
    _validate_synthetic_contract_fixtures(errors)
    _validate_coverage_status_guards(coverage, errors)
    return _finish(errors)


def _validate_guard_status_sets(errors: list[str]) -> None:
    if set(SCALAR_CALCULATION_INPUT_STATUSES) != {ELIGIBLE_STATUS}:
        errors.append("scalar calculation input status set must contain only the approved eligible status")
    if set(NON_SCALAR_OR_BLOCKED_CALCULATION_STATUSES) != APPROVED_STATUSES - {ELIGIBLE_STATUS}:
        errors.append("non-scalar or blocked calculation status set does not match approved schema statuses")


def _validate_synthetic_contract_fixtures(errors: list[str]) -> None:
    accepted = [
        ({"kind": "signed_frame", "unit": "frame", "value": -2}, ELIGIBLE_STATUS),
        ({"kind": "integer", "unit": "damage", "value": 500}, ELIGIBLE_STATUS),
    ]
    for parsed_value, status in accepted:
        if not is_scalar_calculation_input(parsed_value, status):
            errors.append(f"synthetic scalar fixture should be accepted: {parsed_value['kind']}")

    scalar_value = {"kind": "signed_frame", "unit": "frame", "value": -2}
    for status in sorted(APPROVED_STATUSES - {ELIGIBLE_STATUS}):
        if is_scalar_calculation_input(scalar_value, status):
            errors.append(f"blocked status should reject scalar fixture: {status}")

    rejected = [
        (
            {
                "kind": "annotated_numeric_candidate",
                "numeric_candidate": {
                    "candidate_type": "signed_frame",
                    "unit": "frame",
                    "value": -4,
                },
            },
            "annotated_candidate_not_calculation_safe",
        ),
        (
            {"kind": "frame_range", "unit": "frame", "start": -12, "end": -1},
            "parsed_range_not_single_value_calculation_safe",
        ),
        (None, "review_required_not_calculation_safe"),
        ({"kind": "signed_frame", "unit": "frame", "value": -2}, None),
        ({"kind": "integer", "unit": "damage", "value": 500}, "review_required_not_calculation_safe"),
        (
            {
                "kind": "ordered_pair",
                "labels": ["throw_range", "hurtbox"],
                "unit": "distance",
                "values": [0.8, 0.33],
            },
            "not_numeric_authority",
        ),
    ]
    for parsed_value, status in rejected:
        if is_scalar_calculation_input(parsed_value, status):
            errors.append(f"non-scalar or blocked fixture should be rejected: {parsed_value!r} / {status!r}")


def _validate_coverage_status_guards(coverage: dict[str, Any], errors: list[str]) -> None:
    records = coverage.get("coverage_records", [])
    if not isinstance(records, list):
        errors.append("coverage_records must be a list")
        return

    coverage_statuses = {
        record.get("calculation_input_status")
        for record in records
        if isinstance(record, dict)
    }
    unknown_statuses = coverage_statuses - APPROVED_STATUSES
    if unknown_statuses:
        errors.append(f"coverage contains unknown calculation_input_status values: {sorted(unknown_statuses)}")

    annotated_records = [
        record for record in records
        if isinstance(record, dict)
        and record.get("calculation_input_status") == "annotated_candidate_not_calculation_safe"
    ]
    if len(annotated_records) != 3:
        errors.append("expected exactly 3 annotated non-scalar coverage records")
    for record in annotated_records:
        _validate_annotated_record(record, errors)

    range_records = [
        record for record in records
        if isinstance(record, dict)
        and record.get("calculation_input_status") == "parsed_range_not_single_value_calculation_safe"
    ]
    if len(range_records) != 2:
        errors.append("expected exactly 2 frame_range non-scalar coverage records")
    for record in range_records:
        parsed_value = {"kind": "frame_range", "unit": "frame", "start": -12, "end": -1}
        if is_scalar_calculation_input(parsed_value, record.get("calculation_input_status")):
            errors.append(f"{record.get('review_item_id')} frame_range must be rejected by scalar guard")

    blocked_records = [
        record for record in records
        if isinstance(record, dict)
        and record.get("calculation_input_status") == "review_required_not_calculation_safe"
    ]
    if not blocked_records:
        errors.append("expected review_required_not_calculation_safe coverage records")
    for record in blocked_records:
        if is_scalar_calculation_input(None, record.get("calculation_input_status")):
            errors.append(f"{record.get('review_item_id')} review_required value must be rejected by scalar guard")

    non_authority_records = [
        record for record in records
        if isinstance(record, dict)
        and record.get("calculation_input_status") == "not_numeric_authority"
    ]
    if len(non_authority_records) != 1:
        errors.append("expected exactly 1 not_numeric_authority coverage record")
    for record in non_authority_records:
        parsed_value = {
            "kind": "ordered_pair",
            "labels": ["throw_range", "hurtbox"],
            "unit": "distance",
            "values": [0.8, 0.33],
        }
        if is_scalar_calculation_input(parsed_value, record.get("calculation_input_status")):
            errors.append(f"{record.get('review_item_id')} non-authority value must be rejected")


def _validate_annotated_record(record: dict[str, Any], errors: list[str]) -> None:
    variants = record.get("raw_value_variant_coverage", [])
    if not isinstance(variants, list) or not variants:
        errors.append(f"{record.get('review_item_id')} must include raw-value variant coverage")
        return
    parsed_variants = [
        variant for variant in variants
        if isinstance(variant, dict)
        and variant.get("classifier_decision") == "parsed_numeric_structured"
    ]
    if not parsed_variants:
        errors.append(f"{record.get('review_item_id')} must include parsed annotated variants")
    for variant in parsed_variants:
        if variant.get("parsed_value_kind") != "annotated_numeric_candidate":
            errors.append(f"{record.get('review_item_id')} parsed variant must remain annotated_numeric_candidate")
        parsed_value = {
            "kind": "annotated_numeric_candidate",
            "numeric_candidate": {
                "candidate_type": "signed_frame",
                "unit": "frame",
                "value": -4,
            },
        }
        if is_scalar_calculation_input(parsed_value, variant.get("calculation_input_status")):
            errors.append(f"{record.get('review_item_id')} annotated candidate must be rejected by scalar guard")


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact consumer guard validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
