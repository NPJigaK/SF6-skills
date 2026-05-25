from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from sf6_knowledge_coach.current_fact_guards import is_scalar_calculation_input


ROOT = Path(__file__).resolve().parents[2]
EXECPLAN = ROOT / "docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md"
EXPORT_JSON = ROOT / "data/current-facts/20260525T000000Z-current-fact-export.json"
SOURCE_RECORD_JSON_REF = "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"
LEGACY_JP_RAW = ROOT / "data/exports/jp/official_raw.json"
CURRENT_FACTS = ROOT / "src/sf6_knowledge_coach/current_facts.py"
ANSWERING = ROOT / "src/sf6_knowledge_coach/answering.py"
EXPECTED_STATUS_COUNTS = {
    "annotated_candidate_not_calculation_safe": 9,
    "parsed_range_not_single_value_calculation_safe": 4,
}
EXPECTED_FIELD_COUNTS = {
    "block_advantage": 5,
    "hit_advantage": 4,
    "startup": 4,
}
SIDECAR_FIELDS = {
    "raw_value_length",
    "raw_value_sha256",
    "source_cell_key",
    "source_cell_order",
    "source_record_id",
    "source_row_key",
    "source_row_order",
    "source_value_key",
}
FORBIDDEN_RUNTIME_CHANGE_MARKERS = (
    "data/current-facts/20260525T000000Z-current-fact-export.json",
    "current_fact_export/v2",
    "build_production_current_fact_export",
)


def main() -> int:
    errors: list[str] = []
    export_payload = _load_json_object(EXPORT_JSON, errors)
    legacy_records = _load_json_list(LEGACY_JP_RAW, errors)
    if export_payload:
        _validate_export_invariants(export_payload, errors)
    if legacy_records:
        _validate_legacy_comparison_surface(legacy_records, errors)
    if export_payload and legacy_records:
        _validate_expected_non_parity(export_payload, legacy_records, errors)
    _validate_runtime_still_legacy_backed(errors)
    _validate_execplan_rollback_contract(errors)
    return _finish(errors)


def _load_json_object(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"Missing {path.relative_to(ROOT)}")
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        errors.append(f"{path.relative_to(ROOT)} must be a JSON object")
        return {}
    return payload


def _load_json_list(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    if not path.exists():
        errors.append(f"Missing {path.relative_to(ROOT)}")
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        errors.append(f"{path.relative_to(ROOT)} must be a JSON array")
        return []
    if not all(isinstance(record, dict) for record in payload):
        errors.append(f"{path.relative_to(ROOT)} must contain only JSON objects")
        return []
    return payload


def _validate_export_invariants(payload: dict[str, Any], errors: list[str]) -> None:
    if payload.get("artifact_schema_version") != "current_fact_export/v2":
        errors.append("production export must use current_fact_export/v2")
    if payload.get("run_id") != "20260525T000000Z":
        errors.append("production export must keep run_id 20260525T000000Z")
    if payload.get("generated_from") != [SOURCE_RECORD_JSON_REF]:
        errors.append("production export generated_from must reference only the source-record JSON")
    records = payload.get("records")
    if not isinstance(records, list):
        errors.append("production export records must be a list")
        return
    if len(records) != 13:
        errors.append("production export must contain exactly 13 records")
    status_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, dict))
    field_counts = Counter(record.get("field_key") for record in records if isinstance(record, dict))
    if status_counts != Counter(EXPECTED_STATUS_COUNTS):
        errors.append("production export status counts changed")
    if field_counts != Counter(EXPECTED_FIELD_COUNTS):
        errors.append("production export field counts changed")
    scalar_eligible = [
        record for record in records
        if isinstance(record, dict)
        and record.get("calculation_input_status") == "eligible_only_after_domain_source_and_unit_checks"
    ]
    if scalar_eligible:
        errors.append("production export must not contain scalar-eligible records")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        parsed_value = record.get("parsed_value")
        status = record.get("calculation_input_status")
        parsed_kind = parsed_value.get("kind") if isinstance(parsed_value, dict) else None
        leaked_sidecar = sorted(SIDECAR_FIELDS & set(record))
        if leaked_sidecar:
            errors.append(f"records[{index}] leaked source-record sidecar fields: {leaked_sidecar}")
        if not isinstance(parsed_value, dict):
            errors.append(f"records[{index}] must keep parsed_value object")
            continue
        if not isinstance(status, str):
            errors.append(f"records[{index}] must keep calculation_input_status")
            continue
        if record.get("source_name") != "official" or record.get("authority_status") != "authority_candidate":
            errors.append(f"records[{index}] must remain official authority_candidate")
        if parsed_kind == "annotated_numeric_candidate" and status != "annotated_candidate_not_calculation_safe":
            errors.append(f"records[{index}] annotated candidate status changed")
        if parsed_kind == "frame_range" and status != "parsed_range_not_single_value_calculation_safe":
            errors.append(f"records[{index}] frame_range status changed")
        if parsed_kind not in {"annotated_numeric_candidate", "frame_range"}:
            errors.append(f"records[{index}] unexpected parsed_value kind for current export: {parsed_kind}")
        if isinstance(parsed_value, dict) and is_scalar_calculation_input(parsed_value, status):
            errors.append(f"records[{index}] must be rejected by scalar calculation guard")


def _validate_legacy_comparison_surface(records: list[dict[str, Any]], errors: list[str]) -> None:
    if len(records) != 61:
        errors.append("legacy JP raw comparison surface changed from 61 records")
    required_keys = {"character_slug", "move_id", "move_name", "input"}
    for index, record in enumerate(records):
        missing = sorted(required_keys - set(record))
        if missing:
            errors.append(f"legacy records[{index}] missing lookup keys: {missing}")
        if record.get("character_slug") != "jp":
            errors.append(f"legacy records[{index}] must remain JP-only comparison data")
    sample = next((record for record in records if record.get("input") == "5LP"), None)
    if not sample:
        errors.append("legacy JP raw comparison surface must retain 5LP smoke record")
    elif sample.get("move_id") != "jp_001_5lp":
        errors.append("legacy JP 5LP smoke record move_id changed")


def _validate_expected_non_parity(
    export_payload: dict[str, Any],
    legacy_records: list[dict[str, Any]],
    errors: list[str],
) -> None:
    export_records = [record for record in export_payload.get("records", []) if isinstance(record, dict)]
    export_characters = {record.get("character_slug") for record in export_records}
    legacy_characters = {record.get("character_slug") for record in legacy_records}
    if export_characters & legacy_characters:
        errors.append("current export unexpectedly overlaps the JP legacy lookup character surface")
    if any("input" in record or "move_name" in record for record in export_records):
        errors.append("production export records must not pretend to be legacy input-keyed rows")
    legacy_field_keys = set().union(*(record.keys() for record in legacy_records))
    export_field_keys = {record.get("field_key") for record in export_records}
    if export_field_keys <= legacy_field_keys:
        errors.append("current expected non-parity changed: export field keys now look legacy-compatible")


def _validate_runtime_still_legacy_backed(errors: list[str]) -> None:
    current_facts_text = CURRENT_FACTS.read_text(encoding="utf-8")
    answering_text = ANSWERING.read_text(encoding="utf-8")
    required_current_facts = (
        'AUTHORITY_DATASET = "official_raw"',
        "def official_raw_path(character_slug: str) -> Path:",
        "def load_official_raw(character_slug: str) -> list[dict[str, Any]]:",
        "def lookup_current_fact(character_slug: str, move_input: str, field: str) -> CurrentFact:",
        "records = load_official_raw(character_slug)",
        'authority="data/exports official_raw"',
    )
    for marker in required_current_facts:
        if marker not in current_facts_text:
            errors.append(f"current_facts.py no longer shows legacy raw-backed lookup marker: {marker}")
    for marker in FORBIDDEN_RUNTIME_CHANGE_MARKERS:
        if marker in current_facts_text:
            errors.append(f"current_facts.py must not reference production export in this validator-only slice: {marker}")
        if marker in answering_text:
            errors.append(f"answering.py must not reference production export in this validator-only slice: {marker}")
    if "from .current_facts import lookup_current_fact" not in answering_text:
        errors.append("answering.py must still import lookup_current_fact from current_facts")
    if "fact = lookup_current_fact(context.character_slug, context.move_input, context.field)" not in answering_text:
        errors.append("answering.py current-fact path must remain lookup_current_fact-backed")


def _validate_execplan_rollback_contract(errors: list[str]) -> None:
    text = EXECPLAN.read_text(encoding="utf-8")
    required_phrases = (
        "Rollback Criteria",
        "annotated_numeric_candidate",
        "frame_range",
        "calculation_input_status",
        "Runtime lookup remains unchanged.",
        "Legacy raw exports are not retired.",
        "validator-only implementation",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"ExecPlan missing parity/rollback contract phrase: {phrase}")


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact lookup parity validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
