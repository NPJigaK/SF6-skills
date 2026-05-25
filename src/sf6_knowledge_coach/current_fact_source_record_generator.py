from __future__ import annotations

import copy
from collections import Counter
from collections.abc import Mapping
from typing import Any

from .current_fact_candidate_generator import CANDIDATE_JSON_PATH, CANDIDATE_MD_PATH, CANDIDATE_RUN_ID


SOURCE_RECORD_JSON_PATH = f"data/current-facts/source-records/{CANDIDATE_RUN_ID}-current-fact-source-records.json"
SOURCE_RECORD_MD_PATH = f"docs/current-facts/source-records/{CANDIDATE_RUN_ID}-current-fact-source-records.md"
ALLOWED_STATUSES = frozenset(
    {
        "annotated_candidate_not_calculation_safe",
        "parsed_range_not_single_value_calculation_safe",
    }
)


class CurrentFactSourceRecordGeneratorError(ValueError):
    """Raised when candidate input cannot build source-record input."""


def build_source_record_input_payload(candidate_payload: Mapping[str, Any]) -> dict[str, Any]:
    _validate_candidate_payload(candidate_payload)
    records = [_source_record(record) for record in candidate_payload["records"]]
    return {
        "artifact_schema_version": "current_fact_source_record_input/v1",
        "authority_boundary": copy.deepcopy(candidate_payload["authority_boundary"]),
        "generated_from": [CANDIDATE_JSON_PATH, CANDIDATE_MD_PATH],
        "records": sorted(records, key=_source_record_sort_key),
        "run_id": CANDIDATE_RUN_ID,
        "source_record_boundary": {
            "blocked_records": "excluded_to_classifier_or_source_review",
            "legacy_raw_exports": "excluded_as_source_input",
            "local_source_payloads": "excluded_from_public_artifact",
            "lookup_ready_records": "parsed_value_only",
            "reviewer_observations": "observation_candidate_only_not_authority",
            "supercombo": "enrichment_or_cross_reference_only",
        },
    }


def build_source_record_summary_markdown(source_record_payload: Mapping[str, Any]) -> str:
    records = source_record_payload.get("records", [])
    if not isinstance(records, list):
        raise CurrentFactSourceRecordGeneratorError("source-record payload records must be a list")
    status_counts = Counter(
        record.get("current_fact_record", {}).get("calculation_input_status")
        for record in records
        if isinstance(record, Mapping)
    )
    field_counts = Counter(
        record.get("current_fact_record", {}).get("field_key")
        for record in records
        if isinstance(record, Mapping)
    )
    return "\n".join(
        [
            "# Current-Fact Source-Record Input",
            "",
            f"- JSON artifact: `{SOURCE_RECORD_JSON_PATH}`",
            f"- Run ID: `{source_record_payload.get('run_id')}`",
            f"- Source candidate input: `{CANDIDATE_JSON_PATH}`",
            f"- Total records: `{len(records)}`",
            "- Source-record boundary: parsed-value-only, non-scalar values remain not calculation-safe.",
            "- Authority boundary: official values remain authority candidates only.",
            "- Legacy raw exports, ignored local artifacts, raw source payloads, reviewer observations, and private data are excluded as authority.",
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
            "- No production current-fact export artifact is generated.",
            "- Runtime lookup and answer behavior are unchanged.",
            "- `annotated_numeric_candidate` and `frame_range` must not be flattened into scalar values.",
            "",
        ]
    )


def _validate_candidate_payload(candidate_payload: Mapping[str, Any]) -> None:
    expected = {
        "artifact_schema_version": "current_fact_row_move_cell_candidate_input/v1",
        "run_id": CANDIDATE_RUN_ID,
    }
    for key, value in expected.items():
        if candidate_payload.get(key) != value:
            raise CurrentFactSourceRecordGeneratorError(f"unexpected candidate {key}: {candidate_payload.get(key)!r}")
    records = candidate_payload.get("records")
    if not isinstance(records, list) or len(records) != 13:
        raise CurrentFactSourceRecordGeneratorError("candidate records must contain exactly 13 records")


def _source_record(candidate_record: Mapping[str, Any]) -> dict[str, Any]:
    _validate_candidate_record(candidate_record)
    return {
        "current_fact_record": {
            "authority_status": copy.deepcopy(candidate_record["authority_status"]),
            "calculation_input_status": copy.deepcopy(candidate_record["calculation_input_status"]),
            "character_slug": copy.deepcopy(candidate_record["character_slug"]),
            "display_label_ja": copy.deepcopy(candidate_record["display_label_ja"]),
            "evidence": copy.deepcopy(candidate_record["evidence"]),
            "field_key": copy.deepcopy(candidate_record["field_key"]),
            "move_id": copy.deepcopy(candidate_record["move_id"]),
            "parsed_value": copy.deepcopy(candidate_record["parsed_value"]),
            "raw_value": copy.deepcopy(candidate_record["raw_value"]),
            "record_id": _replace_prefix(str(candidate_record["candidate_record_id"]), "candidate:", "current-fact:"),
            "source_family": copy.deepcopy(candidate_record["source_family"]),
            "source_header_path": copy.deepcopy(candidate_record["source_header_path"]),
            "source_label": copy.deepcopy(candidate_record["source_label"]),
            "source_name": copy.deepcopy(candidate_record["source_name"]),
            "source_role": copy.deepcopy(candidate_record["source_role"]),
            "value_shape": copy.deepcopy(candidate_record["value_shape"]),
        },
        "raw_value_length": copy.deepcopy(candidate_record["raw_value_length"]),
        "raw_value_sha256": copy.deepcopy(candidate_record["raw_value_sha256"]),
        "source_cell_key": copy.deepcopy(candidate_record["source_cell_key"]),
        "source_cell_order": copy.deepcopy(candidate_record["source_cell_order"]),
        "source_header_path": copy.deepcopy(candidate_record["source_header_path"]),
        "source_record_id": _replace_prefix(str(candidate_record["candidate_record_id"]), "candidate:", "source-record:"),
        "source_row_key": copy.deepcopy(candidate_record["source_row_key"]),
        "source_row_order": copy.deepcopy(candidate_record["source_row_order"]),
        "source_value_key": copy.deepcopy(candidate_record["source_value_key"]),
    }


def _validate_candidate_record(candidate_record: Mapping[str, Any]) -> None:
    if candidate_record.get("source_name") != "official":
        raise CurrentFactSourceRecordGeneratorError("first source-record slice accepts official candidate records only")
    if candidate_record.get("source_role") != "authority_candidate":
        raise CurrentFactSourceRecordGeneratorError("official source role must remain authority_candidate")
    if candidate_record.get("authority_status") != "authority_candidate":
        raise CurrentFactSourceRecordGeneratorError("official authority status must remain authority_candidate")
    if candidate_record.get("calculation_input_status") not in ALLOWED_STATUSES:
        raise CurrentFactSourceRecordGeneratorError(f"unsupported calculation status: {candidate_record.get('calculation_input_status')}")
    parsed_value = candidate_record.get("parsed_value")
    if not isinstance(parsed_value, Mapping):
        raise CurrentFactSourceRecordGeneratorError("candidate records must include parsed_value")
    parsed_kind = parsed_value.get("kind")
    status = candidate_record.get("calculation_input_status")
    if status == "annotated_candidate_not_calculation_safe" and parsed_kind != "annotated_numeric_candidate":
        raise CurrentFactSourceRecordGeneratorError("annotated status must keep annotated_numeric_candidate wrapper")
    if status == "parsed_range_not_single_value_calculation_safe" and parsed_kind != "frame_range":
        raise CurrentFactSourceRecordGeneratorError("range status must keep frame_range wrapper")


def _replace_prefix(value: str, old: str, new: str) -> str:
    if not value.startswith(old):
        raise CurrentFactSourceRecordGeneratorError(f"expected {old} prefix: {value}")
    return new + value[len(old):]


def _source_record_sort_key(record: Mapping[str, Any]) -> tuple[str, str, int, int, str]:
    current_fact = record.get("current_fact_record", {})
    return (
        str(current_fact.get("source_name", "")) if isinstance(current_fact, Mapping) else "",
        str(current_fact.get("character_slug", "")) if isinstance(current_fact, Mapping) else "",
        int(record.get("source_row_order", 0)),
        int(record.get("source_cell_order", 0)),
        str(record.get("source_value_key", "")),
    )
