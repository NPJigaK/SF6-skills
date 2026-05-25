from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from sf6_knowledge_coach.current_fact_export_generator import (
    CurrentFactExportGeneratorError,
    build_current_fact_export,
    validate_current_fact_export_payload,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_RECORD_FIXTURE_DIR = ROOT / "tests/fixtures/current-facts/source-records"
PRODUCTION_ARTIFACT_DIRS = (
    ROOT / "data/current-facts",
    ROOT / "docs/current-facts",
)
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


def main() -> int:
    errors: list[str] = []
    valid_payloads = _load_valid_source_record_fixtures(errors)
    _validate_valid_fixture_generation(valid_payloads, errors)
    _validate_invalid_fixture_rejections(errors)
    _validate_synthetic_export_boundary_mutations(valid_payloads, errors)
    _validate_no_production_artifacts(errors)
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
        if files:
            relative = [path.relative_to(ROOT).as_posix() for path in files]
            errors.append(f"fixture-contract generator must not create production artifacts: {relative}")


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact export generator validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
