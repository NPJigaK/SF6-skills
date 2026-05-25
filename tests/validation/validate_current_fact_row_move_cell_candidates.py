from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from sf6_knowledge_coach.current_fact_guards import is_scalar_calculation_input


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "contracts/current-facts"
FIXTURE_DIR = ROOT / "tests/fixtures/current-facts/candidate-inputs"
PRODUCTION_JSON = ROOT / "data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json"
PRODUCTION_MD = ROOT / "docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md"
EVIDENCE_JSON = ROOT / "data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json"
CANDIDATE_SCHEMA_PATH = SCHEMA_DIR / "current_fact_row_move_cell_candidate_input.schema.json"
SCHEMA_FILES = [
    "parsed_value.schema.json",
    "value_shape.schema.json",
    "source_reference.schema.json",
    "current_fact_record.schema.json",
    "current_fact_row_move_cell_candidate_input.schema.json",
]
LOOKUP_READY_BLOCKED_STATUSES = {
    "review_required_not_calculation_safe",
    "out_of_scope_not_emitted",
}
FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\.local(?:/|\\)"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|chatgpt|vlm|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
]
FORBIDDEN_SOURCE_PATH_TERMS = (
    "data/exports/",
    ".local/",
    "screenshot",
    "chatgpt",
    "vlm",
    "raw-html",
    "raw_html",
    "full-row",
    "full_raw",
    "cookie",
    "profile",
    "trace",
    "debug",
    "private",
)
REFERENCE_ARRAY_FIELDS = (
    "acquisition_report_refs",
    "coverage_refs",
    "source_review_refs",
)
EXPECTED_PRODUCTION_COUNT = 13
EXPECTED_PRODUCTION_RUN_ID = "20260525T000000Z"
EVIDENCE_JSON_REF = "data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json"
EVIDENCE_MD_REF = "docs/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.md"
COVERAGE_REF = "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"
EXPECTED_PRODUCTION_STATUS_COUNTS = {
    "annotated_candidate_not_calculation_safe": 9,
    "parsed_range_not_single_value_calculation_safe": 4,
}
EXPECTED_PRODUCTION_FIELD_COUNTS = {
    "block_advantage": 5,
    "hit_advantage": 4,
    "startup": 4,
}


def main() -> int:
    errors: list[str] = []
    schemas = _load_schemas(errors)
    if errors:
        return _finish(errors)

    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )
    for path, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # pragma: no cover - exact type is not important here
            errors.append(f"{path.relative_to(ROOT)} is not a valid Draft 2020-12 schema: {exc}")

    validator = Draft202012Validator(schemas[CANDIDATE_SCHEMA_PATH], registry=registry)
    _validate_schema_contract(schemas[CANDIDATE_SCHEMA_PATH], errors)
    valid_payloads = _validate_valid_fixtures(validator, errors)
    _validate_invalid_fixtures(validator, errors)
    _validate_synthetic_boundary_rejections(validator, valid_payloads, errors)
    _scan_valid_public_fixtures(errors)
    _validate_approved_production_candidate_artifacts(validator, errors)
    return _finish(errors)


def _load_schemas(errors: list[str]) -> dict[Path, dict[str, Any]]:
    schemas: dict[Path, dict[str, Any]] = {}
    for name in SCHEMA_FILES:
        path = SCHEMA_DIR / name
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        schemas[path] = json.loads(path.read_text(encoding="utf-8"))
        if schemas[path].get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)} must use JSON Schema Draft 2020-12")
    return schemas


def _validate_schema_contract(schema: dict[str, Any], errors: list[str]) -> None:
    version = schema.get("properties", {}).get("artifact_schema_version", {}).get("const")
    if version != "current_fact_row_move_cell_candidate_input/v1":
        errors.append("candidate schema must use current_fact_row_move_cell_candidate_input/v1")
    generated_from = schema.get("properties", {}).get("generated_from", {})
    if generated_from.get("minItems") != 1 or not generated_from.get("uniqueItems"):
        errors.append("candidate schema must require non-empty unique generated_from paths")
    records = schema.get("properties", {}).get("records", {})
    if records.get("minItems") != 1:
        errors.append("candidate schema must require at least one lookup-ready record")


def _validate_valid_fixtures(
    validator: Draft202012Validator,
    errors: list[str],
) -> dict[Path, dict[str, Any]]:
    payloads: dict[Path, dict[str, Any]] = {}
    fixtures = sorted((FIXTURE_DIR / "valid").glob("*.json"))
    if not fixtures:
        errors.append(f"Missing valid candidate fixtures under {(FIXTURE_DIR / 'valid').relative_to(ROOT)}")
    for path in fixtures:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payloads[path] = payload
        failures = _schema_errors(validator, payload)
        semantic_failures = _semantic_errors(payload)
        if failures or semantic_failures:
            message = failures[0] if failures else semantic_failures[0]
            errors.append(f"{path.relative_to(ROOT)} should be valid: {message}")
    return payloads


def _validate_invalid_fixtures(validator: Draft202012Validator, errors: list[str]) -> None:
    fixtures = sorted((FIXTURE_DIR / "invalid").glob("*.json"))
    if not fixtures:
        errors.append(f"Missing invalid candidate fixtures under {(FIXTURE_DIR / 'invalid').relative_to(ROOT)}")
    for path in fixtures:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not _schema_errors(validator, payload) and not _semantic_errors(payload):
            errors.append(f"{path.relative_to(ROOT)} should be rejected")


def _validate_synthetic_boundary_rejections(
    validator: Draft202012Validator,
    valid_payloads: dict[Path, dict[str, Any]],
    errors: list[str],
) -> None:
    if not valid_payloads:
        return
    base = copy.deepcopy(next(iter(valid_payloads.values())))
    mutations = {
        "legacy generated_from": lambda payload: payload.update(
            {"generated_from": ["data/exports/jp/official_raw.json"]}
        ),
        "local generated_from": lambda payload: payload.update(
            {"generated_from": ["docs/.local/candidate-inputs.json"]}
        ),
        "image reviewer path": lambda payload: payload.update(
            {"generated_from": ["docs/current-facts/candidate-inputs/value-screenshot.png"]}
        ),
        "vlm observation path": lambda payload: payload.update(
            {"generated_from": ["docs/current-facts/candidate-inputs/chatgpt-vlm-observation.md"]}
        ),
        "legacy evidence path": lambda payload: _first_record(payload)["evidence"].update(
            {"public_reference": "data/exports/jp/official_raw.json"}
        ),
        "local source review ref": lambda payload: _first_record(payload).update(
            {"source_review_refs": ["docs/.local/source-review.json"]}
        ),
        "raw html value": lambda payload: _first_record(payload).update(
            {"raw_value": "<table></table>"}
        ),
        "hash mismatch": lambda payload: _first_record(payload).update(
            {"raw_value_sha256": "0" * 64}
        ),
        "header mismatch": lambda payload: _first_record(payload).update(
            {"source_header_path": ["mismatched", "header"]}
        ),
        "official authority promotion": lambda payload: _first_record(payload).update(
            {"authority_status": "not_authority"}
        ),
    }
    for label, mutate in mutations.items():
        payload = copy.deepcopy(base)
        mutate(payload)
        if not _schema_errors(validator, payload) and not _semantic_errors(payload):
            errors.append(f"synthetic candidate boundary mutation should be rejected: {label}")


def _schema_errors(validator: Draft202012Validator, payload: dict[str, Any]) -> list[str]:
    failures = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    return [failure.message for failure in failures]


def _semantic_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path in payload.get("generated_from", []):
        _validate_public_source_path(path, "generated_from", errors)
    for index, record in enumerate(payload.get("records", [])):
        if not isinstance(record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        _validate_record_identity(index, record, errors)
        _validate_record_source_boundary(index, record, errors)
        _validate_record_guard_boundary(index, record, errors)
    return errors


def _validate_public_source_path(path: Any, context: str, errors: list[str]) -> None:
    if not isinstance(path, str):
        errors.append(f"{context} path must be a string")
        return
    lowered = path.lower()
    if re.search(r"(^|[\s\"'`])(?:/[a-z0-9_.-]+)+", path, flags=re.IGNORECASE):
        errors.append(f"{context} must not contain a local absolute path")
    for term in FORBIDDEN_SOURCE_PATH_TERMS:
        if term in lowered:
            errors.append(f"{context} must not reference forbidden source input: {path}")
            return


def _validate_record_identity(index: int, record: dict[str, Any], errors: list[str]) -> None:
    raw_value = record.get("raw_value")
    if isinstance(raw_value, str):
        expected_hash = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
        if record.get("raw_value_sha256") != expected_hash:
            errors.append(f"records[{index}] raw_value_sha256 does not match raw_value")
        if record.get("raw_value_length") != len(raw_value):
            errors.append(f"records[{index}] raw_value_length does not match raw_value")
    evidence = record.get("evidence", {})
    if isinstance(evidence, dict):
        if evidence.get("source_header_path") != record.get("source_header_path"):
            errors.append(f"records[{index}] evidence.source_header_path must match source_header_path")
        for field in ("source_name", "source_role", "source_label"):
            if evidence.get(field) != record.get(field):
                errors.append(f"records[{index}] evidence.{field} must match record.{field}")


def _validate_record_source_boundary(index: int, record: dict[str, Any], errors: list[str]) -> None:
    evidence = record.get("evidence", {})
    if isinstance(evidence, dict):
        _validate_public_source_path(evidence.get("public_reference"), f"records[{index}].evidence.public_reference", errors)
        if evidence.get("evidence_basis") == "official_raw_snapshot":
            errors.append(f"records[{index}] must not use official_raw_snapshot as candidate evidence")
    for field in REFERENCE_ARRAY_FIELDS:
        for path in record.get(field, []):
            _validate_public_source_path(path, f"records[{index}].{field}", errors)
    status = record.get("calculation_input_status")
    if status in LOOKUP_READY_BLOCKED_STATUSES:
        errors.append(f"records[{index}] blocked status is not lookup-ready: {status}")
    if "parsed_value" not in record:
        errors.append(f"records[{index}] lookup-ready candidate must include parsed_value")
    if record.get("value_shape", {}).get("classifier_status") == "review_required":
        errors.append(f"records[{index}] review_required value_shape is not lookup-ready")
    if record.get("source_name") == "official" and record.get("authority_status") != "authority_candidate":
        errors.append(f"records[{index}] official candidate must remain authority_candidate")
    if record.get("source_name") == "supercombo" and status == "eligible_only_after_domain_source_and_unit_checks":
        errors.append(f"records[{index}] SuperCombo candidate must not be scalar calculation authority")


def _validate_record_guard_boundary(index: int, record: dict[str, Any], errors: list[str]) -> None:
    parsed_value = record.get("parsed_value")
    status = record.get("calculation_input_status")
    parsed_kind = parsed_value.get("kind") if isinstance(parsed_value, dict) else None
    if status == "annotated_candidate_not_calculation_safe" and parsed_kind != "annotated_numeric_candidate":
        errors.append(f"records[{index}] annotated status must keep annotated_numeric_candidate wrapper")
    if parsed_kind == "annotated_numeric_candidate" and status != "annotated_candidate_not_calculation_safe":
        errors.append(f"records[{index}] annotated_numeric_candidate must carry annotated non-calculation status")
    if status == "parsed_range_not_single_value_calculation_safe" and parsed_kind != "frame_range":
        errors.append(f"records[{index}] range status must keep frame_range wrapper")
    if parsed_kind == "frame_range" and status != "parsed_range_not_single_value_calculation_safe":
        errors.append(f"records[{index}] frame_range must carry non-scalar range status")
    if parsed_kind in {"annotated_numeric_candidate", "frame_range"}:
        if is_scalar_calculation_input(parsed_value, status):
            errors.append(f"records[{index}] non-scalar parsed value must be rejected by scalar guard")


def _scan_valid_public_fixtures(errors: list[str]) -> None:
    for path in sorted((FIXTURE_DIR / "valid").glob("*.json")):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
                break


def _validate_approved_production_candidate_artifacts(
    validator: Draft202012Validator,
    errors: list[str],
) -> None:
    approved = {
        PRODUCTION_JSON.relative_to(ROOT).as_posix(),
        PRODUCTION_MD.relative_to(ROOT).as_posix(),
    }
    for relative in ("data/current-facts/candidate-inputs", "docs/current-facts/candidate-inputs"):
        directory = ROOT / relative
        if not directory.exists():
            errors.append(f"Missing production candidate directory: {relative}")
            continue
        files = {
            path.relative_to(ROOT).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
        }
        unexpected = sorted(files - approved)
        if unexpected:
            errors.append(f"unexpected current-fact production artifacts: {unexpected}")
    if not PRODUCTION_JSON.exists():
        errors.append(f"Missing approved production candidate JSON: {PRODUCTION_JSON.relative_to(ROOT)}")
        return
    if not PRODUCTION_MD.exists():
        errors.append(f"Missing approved production candidate summary: {PRODUCTION_MD.relative_to(ROOT)}")
    if not EVIDENCE_JSON.exists():
        errors.append(f"Missing source evidence artifact: {EVIDENCE_JSON.relative_to(ROOT)}")
        return

    payload = json.loads(PRODUCTION_JSON.read_text(encoding="utf-8"))
    failures = _schema_errors(validator, payload)
    semantic_failures = _semantic_errors(payload)
    if failures or semantic_failures:
        message = failures[0] if failures else semantic_failures[0]
        errors.append(f"{PRODUCTION_JSON.relative_to(ROOT)} should be valid: {message}")
        return

    evidence_payload = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    _validate_production_payload_against_evidence(payload, evidence_payload, errors)
    for path in (PRODUCTION_JSON, PRODUCTION_MD):
        _scan_public_text(path, errors)


def _validate_production_payload_against_evidence(
    payload: dict[str, Any],
    evidence_payload: dict[str, Any],
    errors: list[str],
) -> None:
    if payload.get("run_id") != EXPECTED_PRODUCTION_RUN_ID:
        errors.append(f"production candidate run_id must be {EXPECTED_PRODUCTION_RUN_ID}")
    if payload.get("run_id") == evidence_payload.get("run_id"):
        errors.append("production candidate run_id must not reuse date-only source-review evidence run_id")
    generated_from = set(payload.get("generated_from", []))
    for required in (EVIDENCE_JSON_REF, EVIDENCE_MD_REF, COVERAGE_REF):
        if required not in generated_from:
            errors.append(f"production generated_from missing {required}")

    evidence_records = evidence_payload.get("evidence_records", [])
    if not isinstance(evidence_records, list):
        errors.append("source evidence records must be a list")
        return
    records = payload.get("records", [])
    if not isinstance(records, list):
        errors.append("production candidate records must be a list")
        return
    if len(records) != EXPECTED_PRODUCTION_COUNT:
        errors.append(f"production candidate artifact must contain {EXPECTED_PRODUCTION_COUNT} records")
    status_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, dict))
    field_counts = Counter(record.get("field_key") for record in records if isinstance(record, dict))
    if dict(sorted(status_counts.items())) != EXPECTED_PRODUCTION_STATUS_COUNTS:
        errors.append("production calculation status counts do not match approved evidence")
    if dict(sorted(field_counts.items())) != EXPECTED_PRODUCTION_FIELD_COUNTS:
        errors.append("production field counts do not match approved evidence")

    evidence_by_id = {
        record.get("candidate_record_id"): record
        for record in evidence_records
        if isinstance(record, dict)
    }
    record_ids = [record.get("candidate_record_id") for record in records if isinstance(record, dict)]
    if len(set(record_ids)) != len(record_ids):
        errors.append("production candidate_record_id values must be unique")
    if set(record_ids) != set(evidence_by_id):
        errors.append("production candidate records must exactly match PR #365 evidence ids")
        return
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        evidence_record = evidence_by_id[record["candidate_record_id"]]
        _validate_production_record(index, record, evidence_record, errors)


def _validate_production_record(
    index: int,
    record: dict[str, Any],
    evidence_record: dict[str, Any],
    errors: list[str],
) -> None:
    copied_fields = (
        "candidate_record_id",
        "character_slug",
        "display_label_ja",
        "field_key",
        "move_id",
        "raw_value",
        "raw_value_length",
        "raw_value_sha256",
        "source_cell_key",
        "source_cell_order",
        "source_family",
        "source_header_path",
        "source_label",
        "source_name",
        "source_role",
        "source_row_key",
        "source_row_order",
        "source_value_key",
    )
    for field in copied_fields:
        if record.get(field) != evidence_record.get(field):
            errors.append(f"records[{index}].{field} does not match source evidence")
    if record.get("authority_status") != "authority_candidate":
        errors.append(f"records[{index}] official candidate authority must not be promoted")
    if record.get("calculation_input_status") != evidence_record.get("calculation_input_status"):
        errors.append(f"records[{index}] calculation_input_status does not match source evidence")
    if record.get("parser_rule_ids") != evidence_record.get("parser_rule_ids"):
        errors.append(f"records[{index}] parser_rule_ids does not match source evidence")
    if record.get("coverage_refs") != [COVERAGE_REF]:
        errors.append(f"records[{index}] coverage_refs must point to the public coverage artifact")
    if EVIDENCE_JSON_REF not in record.get("source_review_refs", []):
        errors.append(f"records[{index}] source_review_refs must include PR #365 evidence artifact")
    for source_ref in evidence_record.get("source_review_refs", []):
        if source_ref not in record.get("source_review_refs", []):
            errors.append(f"records[{index}] missing carried source_review_ref {source_ref}")

    value_shape = record.get("value_shape", {})
    if value_shape.get("review_item_id") != evidence_record.get("coverage_refs", [None])[0]:
        errors.append(f"records[{index}] value_shape.review_item_id must preserve source review item id")
    if value_shape.get("parser_rule_id") != evidence_record.get("parser_rule_ids", [None])[0]:
        errors.append(f"records[{index}] value_shape.parser_rule_id must match source evidence")
    parsed_value = record.get("parsed_value", {})
    if parsed_value.get("kind") != evidence_record.get("parsed_value_kind"):
        errors.append(f"records[{index}] parsed_value kind must match source evidence")

    evidence = record.get("evidence", {})
    if evidence.get("evidence_basis") != "source_review_summary":
        errors.append(f"records[{index}] evidence must use source_review_summary")
    if evidence.get("public_reference") != EVIDENCE_JSON_REF:
        errors.append(f"records[{index}] evidence.public_reference must point to PR #365 evidence JSON")
    if evidence.get("run_id") != "20260521T025403Z":
        errors.append(f"records[{index}] evidence.run_id must carry source acquisition/classifier run id")


def _scan_public_text(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
            break


def _first_record(payload: dict[str, Any]) -> dict[str, Any]:
    return payload["records"][0]


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact row/move/cell candidate validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
