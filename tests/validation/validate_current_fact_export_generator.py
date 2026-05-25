from __future__ import annotations

import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from sf6_knowledge_coach.current_fact_export_generator import (
    CurrentFactExportGeneratorError,
    build_current_fact_export_summary_markdown,
    build_current_fact_export,
    build_production_current_fact_export,
    validate_current_fact_export_payload,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_RECORD_FIXTURE_DIR = ROOT / "tests/fixtures/current-facts/source-records"
PRODUCTION_ARTIFACT_DIRS = (
    ROOT / "data/current-facts",
    ROOT / "docs/current-facts",
)
APPROVED_PRODUCTION_INPUT_ARTIFACTS = {
    "data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json",
    "data/current-facts/20260525T000000Z-current-fact-export.json",
    "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json",
    "docs/current-facts/20260525T000000Z-current-fact-export.md",
    "docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md",
    "docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md",
}
PRODUCTION_SOURCE_RECORD_JSON = ROOT / "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"
PRODUCTION_EXPORT_JSON = ROOT / "data/current-facts/20260525T000000Z-current-fact-export.json"
PRODUCTION_EXPORT_MD = ROOT / "docs/current-facts/20260525T000000Z-current-fact-export.md"
PRODUCTION_SOURCE_RECORD_JSON_REF = "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"
EXPECTED_PRODUCTION_RUN_ID = "20260525T000000Z"
EXPECTED_PRODUCTION_COUNT = 13
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
FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\.local(?:/|\\)"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|chatgpt|vlm|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
]


def main() -> int:
    errors: list[str] = []
    valid_payloads = _load_valid_source_record_fixtures(errors)
    _validate_valid_fixture_generation(valid_payloads, errors)
    _validate_invalid_fixture_rejections(errors)
    _validate_synthetic_export_boundary_mutations(valid_payloads, errors)
    _validate_no_production_artifacts(errors)
    _validate_approved_production_export_artifacts(errors)
    return _finish(errors)


def _load_valid_source_record_fixtures(errors: list[str]) -> dict[Path, dict[str, Any]]:
    valid_dir = SOURCE_RECORD_FIXTURE_DIR / "valid"
    payloads: dict[Path, dict[str, Any]] = {}
    for path in sorted(valid_dir.glob("*.json")):
        payloads[path] = json.loads(path.read_text(encoding="utf-8"))
    if not payloads:
        errors.append(f"Missing source-record generator fixtures under {valid_dir.relative_to(ROOT)}")
    return payloads


def _validate_valid_fixture_generation(
    payloads: dict[Path, dict[str, Any]],
    errors: list[str],
) -> None:
    for path, source_payload in payloads.items():
        try:
            export_payload = build_current_fact_export(source_payload)
        except CurrentFactExportGeneratorError as exc:
            errors.append(f"{path.relative_to(ROOT)} should build a valid export: {exc}")
            continue
        export_errors = validate_current_fact_export_payload(export_payload)
        if export_errors:
            errors.append(f"{path.relative_to(ROOT)} generated invalid export: {export_errors[0]}")
            continue
        if export_payload.get("artifact_schema_version") != "current_fact_export/v2":
            errors.append(f"{path.relative_to(ROOT)} generated wrong export schema version")
        if export_payload.get("generated_from") != sorted(source_payload.get("generated_from", [])):
            errors.append(f"{path.relative_to(ROOT)} generated_from must be sorted source paths")
        _validate_records(path, export_payload.get("records", []), errors)


def _validate_records(path: Path, records: Any, errors: list[str]) -> None:
    if not isinstance(records, list):
        errors.append(f"{path.relative_to(ROOT)} generated records must be a list")
        return
    sort_keys = [
        (
            record.get("source_name"),
            record.get("character_slug"),
            "" if record.get("move_id") is None else record.get("move_id"),
            record.get("field_key"),
            record.get("record_id"),
        )
        for record in records
        if isinstance(record, dict)
    ]
    if sort_keys != sorted(sort_keys):
        errors.append(f"{path.relative_to(ROOT)} generated records are not deterministically sorted")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"{path.relative_to(ROOT)} records[{index}] must be an object")
            continue
        leaked = sorted(SIDECAR_FIELDS & set(record))
        if leaked:
            errors.append(f"{path.relative_to(ROOT)} records[{index}] leaked source-record sidecar fields: {leaked}")
        if "parsed_value" not in record:
            errors.append(f"{path.relative_to(ROOT)} records[{index}] missing parsed_value")
        status = record.get("calculation_input_status")
        parsed_value = record.get("parsed_value")
        parsed_kind = parsed_value.get("kind") if isinstance(parsed_value, dict) else None
        if status == "annotated_candidate_not_calculation_safe" and parsed_kind != "annotated_numeric_candidate":
            errors.append(f"{path.relative_to(ROOT)} records[{index}] flattened annotated candidate")
        if status == "parsed_range_not_single_value_calculation_safe" and parsed_kind != "frame_range":
            errors.append(f"{path.relative_to(ROOT)} records[{index}] collapsed frame_range")
        if record.get("source_name") == "supercombo" and status == "eligible_only_after_domain_source_and_unit_checks":
            errors.append(f"{path.relative_to(ROOT)} records[{index}] promoted SuperCombo numeric authority")


def _validate_invalid_fixture_rejections(errors: list[str]) -> None:
    invalid_dir = SOURCE_RECORD_FIXTURE_DIR / "invalid"
    fixtures = sorted(invalid_dir.glob("*.json"))
    if not fixtures:
        errors.append(f"Missing invalid source-record fixtures under {invalid_dir.relative_to(ROOT)}")
    for path in fixtures:
        try:
            build_current_fact_export(json.loads(path.read_text(encoding="utf-8")))
        except CurrentFactExportGeneratorError:
            continue
        errors.append(f"{path.relative_to(ROOT)} should be rejected by generator")


def _validate_synthetic_export_boundary_mutations(
    payloads: dict[Path, dict[str, Any]],
    errors: list[str],
) -> None:
    if not payloads:
        return
    export_payload = build_current_fact_export(next(iter(payloads.values())))
    mutations = {
        "legacy generated_from": lambda payload: payload.update(
            {"generated_from": ["data/exports/jp/official_raw.json"]}
        ),
        "local generated_from": lambda payload: payload.update(
            {"generated_from": ["docs/.local/current-fact-export.json"]}
        ),
        "screenshot generated_from": lambda payload: payload.update(
            {"generated_from": ["docs/current-facts/value-screenshot.png"]}
        ),
        "sidecar leak": lambda payload: payload["records"][0].update(
            {"source_record_id": "source-record:leak"}
        ),
        "raw html value": lambda payload: payload["records"][0].update(
            {"raw_value": "<table></table>"}
        ),
        "supercombo scalar authority": lambda payload: payload["records"][0].update(
            {
                "authority_status": "cross_reference_candidate",
                "calculation_input_status": "eligible_only_after_domain_source_and_unit_checks",
                "source_name": "supercombo",
                "source_role": "cross_reference_candidate",
            }
        ),
    }
    for label, mutate in mutations.items():
        mutated = copy.deepcopy(export_payload)
        mutate(mutated)
        if not validate_current_fact_export_payload(mutated):
            errors.append(f"synthetic export boundary mutation should be rejected: {label}")


def _validate_no_production_artifacts(errors: list[str]) -> None:
    for directory in PRODUCTION_ARTIFACT_DIRS:
        if not directory.exists():
            continue
        files = sorted(path for path in directory.rglob("*") if path.is_file())
        unexpected = [
            path.relative_to(ROOT).as_posix()
            for path in files
            if path.relative_to(ROOT).as_posix() not in APPROVED_PRODUCTION_INPUT_ARTIFACTS
        ]
        if unexpected:
            errors.append(f"fixture-contract generator must not create current-fact export artifacts: {unexpected}")


def _validate_approved_production_export_artifacts(errors: list[str]) -> None:
    if not PRODUCTION_SOURCE_RECORD_JSON.exists():
        errors.append(f"Missing production source-record input: {PRODUCTION_SOURCE_RECORD_JSON.relative_to(ROOT)}")
        return
    if not PRODUCTION_EXPORT_JSON.exists():
        errors.append(f"Missing approved production current-fact export JSON: {PRODUCTION_EXPORT_JSON.relative_to(ROOT)}")
        return
    if not PRODUCTION_EXPORT_MD.exists():
        errors.append(f"Missing approved production current-fact export summary: {PRODUCTION_EXPORT_MD.relative_to(ROOT)}")
        return

    source_payload = json.loads(PRODUCTION_SOURCE_RECORD_JSON.read_text(encoding="utf-8"))
    export_payload = json.loads(PRODUCTION_EXPORT_JSON.read_text(encoding="utf-8"))
    expected_payload = build_production_current_fact_export(source_payload)
    if export_payload != expected_payload:
        errors.append("production current-fact export JSON must match deterministic generator output")

    export_errors = validate_current_fact_export_payload(export_payload)
    if export_errors:
        errors.append(f"{PRODUCTION_EXPORT_JSON.relative_to(ROOT)} should be valid: {export_errors[0]}")
        return
    expected_markdown = build_current_fact_export_summary_markdown(export_payload)
    if PRODUCTION_EXPORT_MD.read_text(encoding="utf-8") != expected_markdown:
        errors.append("production current-fact export summary must match deterministic generator output")

    _validate_production_export_payload(export_payload, source_payload, errors)
    for path in (PRODUCTION_EXPORT_JSON, PRODUCTION_EXPORT_MD):
        _scan_public_text(path, errors)


def _validate_production_export_payload(
    export_payload: dict[str, Any],
    source_payload: dict[str, Any],
    errors: list[str],
) -> None:
    if export_payload.get("artifact_schema_version") != "current_fact_export/v2":
        errors.append("production export must use current_fact_export/v2")
    if export_payload.get("run_id") != EXPECTED_PRODUCTION_RUN_ID:
        errors.append(f"production export run_id must be {EXPECTED_PRODUCTION_RUN_ID}")
    if export_payload.get("generated_from") != [PRODUCTION_SOURCE_RECORD_JSON_REF]:
        errors.append("production export generated_from must point only to PR #367 source-record JSON")
    records = export_payload.get("records", [])
    source_records = source_payload.get("records", [])
    if not isinstance(records, list) or not isinstance(source_records, list):
        errors.append("production export and source-record records must be lists")
        return
    if len(records) != EXPECTED_PRODUCTION_COUNT:
        errors.append(f"production export must contain {EXPECTED_PRODUCTION_COUNT} records")
    status_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, dict))
    field_counts = Counter(record.get("field_key") for record in records if isinstance(record, dict))
    if dict(sorted(status_counts.items())) != EXPECTED_STATUS_COUNTS:
        errors.append("production export calculation status counts do not match approved source records")
    if dict(sorted(field_counts.items())) != EXPECTED_FIELD_COUNTS:
        errors.append("production export field counts do not match approved source records")

    source_current_facts = [
        record.get("current_fact_record")
        for record in source_records
        if isinstance(record, dict)
    ]
    if sorted(records, key=lambda record: record.get("record_id", "")) != sorted(
        source_current_facts,
        key=lambda record: record.get("record_id", "") if isinstance(record, dict) else "",
    ):
        errors.append("production export records must exactly match source-record current_fact_record payloads")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        leaked = sorted(SIDECAR_FIELDS & set(record))
        if leaked:
            errors.append(f"records[{index}] leaked source-record sidecar fields: {leaked}")
        if record.get("source_name") != "official" or record.get("authority_status") != "authority_candidate":
            errors.append(f"records[{index}] must remain official authority_candidate")


def _scan_public_text(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
            break


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact export generator validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
