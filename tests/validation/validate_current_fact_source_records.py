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
from sf6_knowledge_coach.current_fact_source_record_generator import build_source_record_input_payload


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "contracts/current-facts"
FIXTURE_DIR = ROOT / "tests/fixtures/current-facts/source-records"
PRODUCTION_JSON = ROOT / "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"
PRODUCTION_MD = ROOT / "docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md"
CANDIDATE_JSON = ROOT / "data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json"
CANDIDATE_JSON_REF = "data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json"
CANDIDATE_MD_REF = "docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md"
SOURCE_RECORD_SCHEMA_PATH = SCHEMA_DIR / "current_fact_source_record_input.schema.json"
SOURCE_RECORD_SCHEMA_ID = (
    "https://sf6-knowledge-coach.local/schemas/current-facts/current_fact_source_record_input.schema.json"
)
SCHEMA_FILES = [
    "parsed_value.schema.json",
    "value_shape.schema.json",
    "source_reference.schema.json",
    "current_fact_record.schema.json",
    "current_fact_source_record_input.schema.json",
]
LOOKUP_READY_BLOCKED_STATUSES = {
    "review_required_not_calculation_safe",
    "out_of_scope_not_emitted",
}
EXPECTED_PRODUCTION_COUNT = 13
EXPECTED_PRODUCTION_RUN_ID = "20260525T000000Z"
EXPECTED_PRODUCTION_STATUS_COUNTS = {
    "annotated_candidate_not_calculation_safe": 9,
    "parsed_range_not_single_value_calculation_safe": 4,
}
EXPECTED_PRODUCTION_FIELD_COUNTS = {
    "block_advantage": 5,
    "hit_advantage": 4,
    "startup": 4,
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
        except Exception as exc:  # pragma: no cover - exact exception type is not important here
            errors.append(f"{path.relative_to(ROOT)} is not a valid Draft 2020-12 schema: {exc}")

    validator = Draft202012Validator(schemas[SOURCE_RECORD_SCHEMA_PATH], registry=registry)
    record_validator = Draft202012Validator(schemas[SCHEMA_DIR / "current_fact_record.schema.json"], registry=registry)
    _validate_schema_contract(schemas[SOURCE_RECORD_SCHEMA_PATH], errors)
    valid_payloads = _validate_valid_fixtures(validator, errors)
    _validate_invalid_fixtures(validator, errors)
    _validate_synthetic_boundary_rejections(validator, valid_payloads, errors)
    _scan_valid_public_fixtures(errors)
    _validate_approved_production_source_record_artifacts(validator, record_validator, errors)
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
    if version != "current_fact_source_record_input/v1":
        errors.append("source-record input schema must use current_fact_source_record_input/v1")
    generated_from = schema.get("properties", {}).get("generated_from", {})
    if generated_from.get("minItems") != 1 or not generated_from.get("uniqueItems"):
        errors.append("source-record input schema must require non-empty unique generated_from paths")
    records = schema.get("properties", {}).get("records", {})
    if records.get("minItems") != 1:
        errors.append("source-record input schema must require at least one lookup-ready record")


def _validate_valid_fixtures(
    validator: Draft202012Validator,
    errors: list[str],
) -> dict[Path, dict[str, Any]]:
    payloads: dict[Path, dict[str, Any]] = {}
    fixtures = sorted((FIXTURE_DIR / "valid").glob("*.json"))
    if not fixtures:
        errors.append(f"Missing valid source-record fixtures under {(FIXTURE_DIR / 'valid').relative_to(ROOT)}")
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
        errors.append(f"Missing invalid source-record fixtures under {(FIXTURE_DIR / 'invalid').relative_to(ROOT)}")
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
            {"generated_from": ["docs/.local/source-records.json"]}
        ),
        "image reviewer path": lambda payload: payload.update(
            {"generated_from": ["docs/current-facts/source-records/value-screenshot.png"]}
        ),
        "vlm observation path": lambda payload: payload.update(
            {"generated_from": ["docs/current-facts/source-records/chatgpt-vlm-observation.md"]}
        ),
        "legacy evidence path": lambda payload: _first_record(payload)["current_fact_record"]["evidence"].update(
            {"public_reference": "data/exports/jp/official_raw.json"}
        ),
        "local absolute evidence path": lambda payload: _first_record(payload)["current_fact_record"]["evidence"].update(
            {"public_reference": "/mnt/e/github/SF6-skills/.local/source.json"}
        ),
        "raw html value": lambda payload: _first_record(payload)["current_fact_record"].update(
            {"raw_value": "<table></table>"}
        ),
        "hash mismatch": lambda payload: _first_record(payload).update(
            {"raw_value_sha256": "0" * 64}
        ),
        "header mismatch": lambda payload: _first_record(payload).update(
            {"source_header_path": ["mismatched", "header"]}
        ),
    }
    for label, mutate in mutations.items():
        payload = copy.deepcopy(base)
        mutate(payload)
        if not _schema_errors(validator, payload) and not _semantic_errors(payload):
            errors.append(f"synthetic source-record boundary mutation should be rejected: {label}")


def _schema_errors(validator: Draft202012Validator, payload: dict[str, Any]) -> list[str]:
    failures = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    return [failure.message for failure in failures]


def _semantic_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path in payload.get("generated_from", []):
        _validate_public_source_path(path, "generated_from", errors)
    for index, source_record in enumerate(payload.get("records", [])):
        if not isinstance(source_record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        current_fact = source_record.get("current_fact_record", {})
        if not isinstance(current_fact, dict):
            errors.append(f"records[{index}].current_fact_record must be an object")
            continue
        _validate_record_identity(index, source_record, current_fact, errors)
        _validate_record_source_boundary(index, current_fact, errors)
        _validate_record_guard_boundary(index, current_fact, errors)
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


def _validate_record_identity(
    index: int,
    source_record: dict[str, Any],
    current_fact: dict[str, Any],
    errors: list[str],
) -> None:
    raw_value = current_fact.get("raw_value")
    if isinstance(raw_value, str):
        expected_hash = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
        if source_record.get("raw_value_sha256") != expected_hash:
            errors.append(f"records[{index}] raw_value_sha256 does not match raw_value")
        if source_record.get("raw_value_length") != len(raw_value):
            errors.append(f"records[{index}] raw_value_length does not match raw_value")
    if source_record.get("source_header_path") != current_fact.get("source_header_path"):
        errors.append(f"records[{index}] source_header_path must match current_fact_record.source_header_path")
    evidence = current_fact.get("evidence", {})
    if isinstance(evidence, dict):
        if evidence.get("source_header_path") != current_fact.get("source_header_path"):
            errors.append(f"records[{index}] evidence.source_header_path must match current_fact_record.source_header_path")
        for field in ("source_name", "source_role", "source_label"):
            if evidence.get(field) != current_fact.get(field):
                errors.append(f"records[{index}] evidence.{field} must match current_fact_record.{field}")


def _validate_record_source_boundary(index: int, current_fact: dict[str, Any], errors: list[str]) -> None:
    evidence = current_fact.get("evidence", {})
    if isinstance(evidence, dict):
        _validate_public_source_path(evidence.get("public_reference"), f"records[{index}].evidence.public_reference", errors)
        if evidence.get("evidence_basis") == "official_raw_snapshot":
            errors.append(f"records[{index}] must not use official_raw_snapshot as source-record evidence")
    status = current_fact.get("calculation_input_status")
    if status in LOOKUP_READY_BLOCKED_STATUSES:
        errors.append(f"records[{index}] blocked status is not lookup-ready: {status}")
    if "parsed_value" not in current_fact:
        errors.append(f"records[{index}] lookup-ready source record must include parsed_value")
    if current_fact.get("value_shape", {}).get("classifier_status") == "review_required":
        errors.append(f"records[{index}] review_required value_shape is not lookup-ready")
    if current_fact.get("source_name") == "supercombo" and status == "eligible_only_after_domain_source_and_unit_checks":
        errors.append(f"records[{index}] SuperCombo value must not be scalar calculation authority")


def _validate_record_guard_boundary(index: int, current_fact: dict[str, Any], errors: list[str]) -> None:
    parsed_value = current_fact.get("parsed_value")
    status = current_fact.get("calculation_input_status")
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


def _validate_approved_production_source_record_artifacts(
    validator: Draft202012Validator,
    record_validator: Draft202012Validator,
    errors: list[str],
) -> None:
    approved = {
        PRODUCTION_JSON.relative_to(ROOT).as_posix(),
        PRODUCTION_MD.relative_to(ROOT).as_posix(),
    }
    for relative in ("data/current-facts/source-records", "docs/current-facts/source-records"):
        directory = ROOT / relative
        if not directory.exists():
            errors.append(f"Missing production source-record directory: {relative}")
            continue
        files = {
            path.relative_to(ROOT).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
        }
        unexpected = sorted(files - approved)
        if unexpected:
            errors.append(f"unexpected source-record production artifacts: {unexpected}")
    if not PRODUCTION_JSON.exists():
        errors.append(f"Missing approved production source-record JSON: {PRODUCTION_JSON.relative_to(ROOT)}")
        return
    if not PRODUCTION_MD.exists():
        errors.append(f"Missing approved production source-record summary: {PRODUCTION_MD.relative_to(ROOT)}")
    if not CANDIDATE_JSON.exists():
        errors.append(f"Missing candidate input artifact: {CANDIDATE_JSON.relative_to(ROOT)}")
        return

    payload = json.loads(PRODUCTION_JSON.read_text(encoding="utf-8"))
    failures = _schema_errors(validator, payload)
    semantic_failures = _semantic_errors(payload)
    if failures or semantic_failures:
        message = failures[0] if failures else semantic_failures[0]
        errors.append(f"{PRODUCTION_JSON.relative_to(ROOT)} should be valid: {message}")
        return
    candidate_payload = json.loads(CANDIDATE_JSON.read_text(encoding="utf-8"))
    generated_payload = build_source_record_input_payload(candidate_payload)
    if payload != generated_payload:
        errors.append("production source-record JSON must match deterministic generator output")
    _validate_production_payload_against_candidates(payload, candidate_payload, record_validator, errors)
    for path in (PRODUCTION_JSON, PRODUCTION_MD):
        _scan_public_text(path, errors)


def _validate_production_payload_against_candidates(
    payload: dict[str, Any],
    candidate_payload: dict[str, Any],
    record_validator: Draft202012Validator,
    errors: list[str],
) -> None:
    if payload.get("run_id") != EXPECTED_PRODUCTION_RUN_ID:
        errors.append(f"production source-record run_id must be {EXPECTED_PRODUCTION_RUN_ID}")
    if payload.get("run_id") != candidate_payload.get("run_id"):
        errors.append("production source-record run_id must match production candidate run_id")
    if payload.get("generated_from") != [CANDIDATE_JSON_REF, CANDIDATE_MD_REF]:
        errors.append("production source-record generated_from must point only to PR #366 candidate artifacts")
    candidate_records = candidate_payload.get("records", [])
    records = payload.get("records", [])
    if not isinstance(candidate_records, list) or not isinstance(records, list):
        errors.append("production source-record and candidate records must be lists")
        return
    if len(records) != EXPECTED_PRODUCTION_COUNT:
        errors.append(f"production source-record artifact must contain {EXPECTED_PRODUCTION_COUNT} records")
    status_counts = Counter(
        record.get("current_fact_record", {}).get("calculation_input_status")
        for record in records
        if isinstance(record, dict)
    )
    field_counts = Counter(
        record.get("current_fact_record", {}).get("field_key")
        for record in records
        if isinstance(record, dict)
    )
    if dict(sorted(status_counts.items())) != EXPECTED_PRODUCTION_STATUS_COUNTS:
        errors.append("production source-record calculation status counts do not match approved candidates")
    if dict(sorted(field_counts.items())) != EXPECTED_PRODUCTION_FIELD_COUNTS:
        errors.append("production source-record field counts do not match approved candidates")

    candidates_by_source_record_id = {
        _source_record_id(candidate.get("candidate_record_id")): candidate
        for candidate in candidate_records
        if isinstance(candidate, dict)
    }
    source_record_ids = [record.get("source_record_id") for record in records if isinstance(record, dict)]
    if len(set(source_record_ids)) != len(source_record_ids):
        errors.append("production source_record_id values must be unique")
    if set(source_record_ids) != set(candidates_by_source_record_id):
        errors.append("production source records must exactly match PR #366 candidate ids")
        return
    current_fact_record_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"records[{index}] must be an object")
            continue
        candidate = candidates_by_source_record_id[record["source_record_id"]]
        current_fact = record.get("current_fact_record", {})
        record_failures = _schema_errors(record_validator, current_fact) if isinstance(current_fact, dict) else ["current_fact_record must be an object"]
        if record_failures:
            errors.append(f"records[{index}].current_fact_record should be valid: {record_failures[0]}")
            continue
        current_fact_record_id = current_fact.get("record_id")
        if current_fact_record_id in current_fact_record_ids:
            errors.append(f"current_fact_record.record_id must be unique: {current_fact_record_id}")
        if isinstance(current_fact_record_id, str):
            current_fact_record_ids.add(current_fact_record_id)
        _validate_production_record(index, record, current_fact, candidate, errors)


def _validate_production_record(
    index: int,
    source_record: dict[str, Any],
    current_fact: dict[str, Any],
    candidate: dict[str, Any],
    errors: list[str],
) -> None:
    sidecar_fields = (
        "raw_value_length",
        "raw_value_sha256",
        "source_cell_key",
        "source_cell_order",
        "source_header_path",
        "source_row_key",
        "source_row_order",
        "source_value_key",
    )
    for field in sidecar_fields:
        if source_record.get(field) != candidate.get(field):
            errors.append(f"records[{index}].{field} does not match candidate artifact")
    if source_record.get("source_record_id") != _source_record_id(candidate.get("candidate_record_id")):
        errors.append(f"records[{index}].source_record_id must be derived from candidate_record_id")
    if current_fact.get("record_id") != _current_fact_record_id(candidate.get("candidate_record_id")):
        errors.append(f"records[{index}].current_fact_record.record_id must be derived from candidate_record_id")

    copied_current_fact_fields = (
        "authority_status",
        "calculation_input_status",
        "character_slug",
        "display_label_ja",
        "evidence",
        "field_key",
        "move_id",
        "parsed_value",
        "raw_value",
        "source_family",
        "source_header_path",
        "source_label",
        "source_name",
        "source_role",
        "value_shape",
    )
    for field in copied_current_fact_fields:
        if current_fact.get(field) != candidate.get(field):
            errors.append(f"records[{index}].current_fact_record.{field} does not match candidate artifact")
    forbidden_sidecars = {
        "candidate_record_id",
        "parser_rule_ids",
        "source_record_id",
        "source_row_key",
        "source_cell_key",
        "source_value_key",
        "source_row_order",
        "source_cell_order",
        "raw_value_length",
        "raw_value_sha256",
    }
    leaked = sorted(forbidden_sidecars & set(current_fact))
    if leaked:
        errors.append(f"records[{index}].current_fact_record leaked sidecar fields: {leaked}")


def _source_record_id(candidate_record_id: object) -> str:
    if not isinstance(candidate_record_id, str):
        return ""
    return candidate_record_id.replace("candidate:", "source-record:", 1)


def _current_fact_record_id(candidate_record_id: object) -> str:
    if not isinstance(candidate_record_id, str):
        return ""
    return candidate_record_id.replace("candidate:", "current-fact:", 1)


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
    print("Current-fact source-record validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
