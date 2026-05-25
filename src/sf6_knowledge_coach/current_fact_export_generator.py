from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from sf6_knowledge_coach.current_fact_guards import is_scalar_calculation_input
from sf6_knowledge_coach.paths import repo_root


SCHEMA_DIR = repo_root() / "contracts/current-facts"
SOURCE_RECORD_SCHEMA_PATH = SCHEMA_DIR / "current_fact_source_record_input.schema.json"
EXPORT_SCHEMA_PATH = SCHEMA_DIR / "current_fact_export.schema.json"
SCHEMA_FILES = (
    "parsed_value.schema.json",
    "value_shape.schema.json",
    "source_reference.schema.json",
    "current_fact_record.schema.json",
    "current_fact_export.schema.json",
    "current_fact_source_record_input.schema.json",
)
BLOCKED_LOOKUP_STATUSES = frozenset(
    {
        "review_required_not_calculation_safe",
        "out_of_scope_not_emitted",
    }
)
SOURCE_RECORD_ONLY_FIELDS = frozenset(
    {
        "raw_value_length",
        "raw_value_sha256",
        "source_cell_key",
        "source_cell_order",
        "source_record_id",
        "source_row_key",
        "source_row_order",
        "source_value_key",
    }
)
FORBIDDEN_PUBLIC_PATH_TERMS = (
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
FORBIDDEN_TEXT_PATTERNS = (
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)\b(?:screenshot|chatgpt|vlm|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
)
PRODUCTION_SOURCE_RECORD_JSON_PATH = "data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"
PRODUCTION_EXPORT_JSON_PATH = "data/current-facts/20260525T000000Z-current-fact-export.json"
PRODUCTION_EXPORT_MD_PATH = "docs/current-facts/20260525T000000Z-current-fact-export.md"


class CurrentFactExportGeneratorError(ValueError):
    """Raised when source-record input cannot build a valid current-fact export."""


def build_current_fact_export(
    source_record_payload: Mapping[str, Any],
    *,
    generated_from: list[str] | None = None,
) -> dict[str, Any]:
    errors = validate_source_record_payload(source_record_payload)
    if errors:
        raise CurrentFactExportGeneratorError(_format_errors("invalid source-record input", errors))

    records = [
        copy.deepcopy(source_record["current_fact_record"])
        for source_record in source_record_payload["records"]
    ]
    export_payload = {
        "artifact_schema_version": "current_fact_export/v2",
        "authority_boundary": copy.deepcopy(source_record_payload["authority_boundary"]),
        "generated_from": sorted(generated_from if generated_from is not None else source_record_payload["generated_from"]),
        "records": sorted(records, key=_record_sort_key),
        "run_id": source_record_payload["run_id"],
    }

    export_errors = validate_current_fact_export_payload(export_payload)
    if export_errors:
        raise CurrentFactExportGeneratorError(_format_errors("invalid generated current-fact export", export_errors))
    return export_payload


def build_production_current_fact_export(source_record_payload: Mapping[str, Any]) -> dict[str, Any]:
    return build_current_fact_export(
        source_record_payload,
        generated_from=[PRODUCTION_SOURCE_RECORD_JSON_PATH],
    )


def build_current_fact_export_summary_markdown(export_payload: Mapping[str, Any]) -> str:
    records = export_payload.get("records", [])
    if not isinstance(records, list):
        raise CurrentFactExportGeneratorError("export payload records must be a list")
    status_counts = Counter(
        record.get("calculation_input_status")
        for record in records
        if isinstance(record, Mapping)
    )
    field_counts = Counter(
        record.get("field_key")
        for record in records
        if isinstance(record, Mapping)
    )
    return "\n".join(
        [
            "# Current-Fact Export",
            "",
            f"- JSON artifact: `{PRODUCTION_EXPORT_JSON_PATH}`",
            f"- Run ID: `{export_payload.get('run_id')}`",
            f"- Source-record input: `{PRODUCTION_SOURCE_RECORD_JSON_PATH}`",
            f"- Total records: `{len(records)}`",
            "- Export boundary: source-record sidecar fields are excluded.",
            "- Calculation boundary: non-scalar values remain not calculation-safe.",
            "- Authority boundary: official values remain authority candidates only.",
            "- Runtime lookup and answer behavior are unchanged.",
            "",
            "## Counts",
            "",
            "| Dimension | Value | Count |",
            "| --- | --- | --- |",
            *[
                f"| calculation_input_status | `{status}` | {count} |"
                for status, count in sorted(status_counts.items())
            ],
            *[
                f"| field_key | `{field}` | {count} |"
                for field, count in sorted(field_counts.items())
            ],
            "",
            "## Boundaries",
            "",
            "- No runtime current-fact lookup switch is included.",
            "- `annotated_numeric_candidate` and `frame_range` must not be flattened into scalar values.",
            "- Legacy raw exports, ignored local artifacts, raw source payloads, reviewer observations, and private data are excluded as authority.",
            "",
        ]
    )


def validate_source_record_payload(source_record_payload: Mapping[str, Any]) -> list[str]:
    schema_errors = _schema_errors(_source_record_validator(), source_record_payload)
    semantic_errors = _source_record_semantic_errors(source_record_payload)
    return [*schema_errors, *semantic_errors]


def validate_current_fact_export_payload(export_payload: Mapping[str, Any]) -> list[str]:
    schema_errors = _schema_errors(_export_validator(), export_payload)
    semantic_errors = _export_semantic_errors(export_payload)
    return [*schema_errors, *semantic_errors]


def _record_sort_key(record: Mapping[str, Any]) -> tuple[str, str, str, str, str]:
    move_id = record.get("move_id")
    return (
        str(record.get("source_name", "")),
        str(record.get("character_slug", "")),
        "" if move_id is None else str(move_id),
        str(record.get("field_key", "")),
        str(record.get("record_id", "")),
    )


def _source_record_validator() -> Draft202012Validator:
    schemas = _load_schemas()
    registry = _schema_registry(schemas)
    return Draft202012Validator(schemas[SOURCE_RECORD_SCHEMA_PATH], registry=registry)


def _export_validator() -> Draft202012Validator:
    schemas = _load_schemas()
    registry = _schema_registry(schemas)
    return Draft202012Validator(schemas[EXPORT_SCHEMA_PATH], registry=registry)


def _load_schemas() -> dict[Path, dict[str, Any]]:
    return {
        SCHEMA_DIR / name: json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
        for name in SCHEMA_FILES
    }


def _schema_registry(schemas: Mapping[Path, Mapping[str, Any]]) -> Registry:
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )


def _schema_errors(validator: Draft202012Validator, payload: Mapping[str, Any]) -> list[str]:
    failures = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    return [failure.message for failure in failures]


def _source_record_semantic_errors(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for path in payload.get("generated_from", []):
        _validate_public_path(path, "generated_from", errors)
    for index, source_record in enumerate(payload.get("records", [])):
        if not isinstance(source_record, Mapping):
            errors.append(f"records[{index}] must be an object")
            continue
        current_fact = source_record.get("current_fact_record")
        if not isinstance(current_fact, Mapping):
            errors.append(f"records[{index}].current_fact_record must be an object")
            continue
        _validate_source_record_identity(index, source_record, current_fact, errors)
        _validate_current_fact_record(index, current_fact, errors)
    return errors


def _export_semantic_errors(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for path in payload.get("generated_from", []):
        _validate_public_path(path, "generated_from", errors)
    for index, record in enumerate(payload.get("records", [])):
        if not isinstance(record, Mapping):
            errors.append(f"records[{index}] must be an object")
            continue
        leaked_fields = sorted(SOURCE_RECORD_ONLY_FIELDS & set(record))
        if leaked_fields:
            errors.append(f"records[{index}] leaked source-record sidecar fields: {leaked_fields}")
        _validate_current_fact_record(index, record, errors)
    return errors


def _validate_current_fact_record(index: int, record: Mapping[str, Any], errors: list[str]) -> None:
    status = record.get("calculation_input_status")
    parsed_value = record.get("parsed_value")
    parsed_kind = parsed_value.get("kind") if isinstance(parsed_value, Mapping) else None
    if "parsed_value" not in record:
        errors.append(f"records[{index}] lookup-ready record must include parsed_value")
    if status in BLOCKED_LOOKUP_STATUSES:
        errors.append(f"records[{index}] blocked status is not lookup-ready: {status}")
    if record.get("source_name") == "official" and record.get("authority_status") != "authority_candidate":
        errors.append(f"records[{index}] official record must remain authority_candidate")
    if record.get("source_name") == "supercombo" and status == "eligible_only_after_domain_source_and_unit_checks":
        errors.append(f"records[{index}] SuperCombo value must not be scalar calculation authority")
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
    evidence = record.get("evidence")
    if isinstance(evidence, Mapping):
        _validate_public_path(evidence.get("public_reference"), f"records[{index}].evidence.public_reference", errors)
    _scan_public_value(record.get("raw_value"), f"records[{index}].raw_value", errors)


def _validate_source_record_identity(
    index: int,
    source_record: Mapping[str, Any],
    current_fact: Mapping[str, Any],
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
    evidence = current_fact.get("evidence")
    if isinstance(evidence, Mapping):
        if evidence.get("source_header_path") != current_fact.get("source_header_path"):
            errors.append(f"records[{index}] evidence.source_header_path must match current_fact_record.source_header_path")
        for field in ("source_name", "source_role", "source_label"):
            if evidence.get(field) != current_fact.get(field):
                errors.append(f"records[{index}] evidence.{field} must match current_fact_record.{field}")


def _validate_public_path(path: object, context: str, errors: list[str]) -> None:
    if not isinstance(path, str):
        errors.append(f"{context} path must be a string")
        return
    lowered = path.lower()
    for term in FORBIDDEN_PUBLIC_PATH_TERMS:
        if term in lowered:
            errors.append(f"{context} must not reference forbidden source input: {path}")
            return
    _scan_public_value(path, context, errors)


def _scan_public_value(value: object, context: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        return
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(value):
            errors.append(f"{context} contains forbidden public content")
            return


def _format_errors(prefix: str, errors: list[str]) -> str:
    return f"{prefix}: " + "; ".join(errors)
