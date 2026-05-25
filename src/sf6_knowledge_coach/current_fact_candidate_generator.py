from __future__ import annotations

import copy
import hashlib
from collections import Counter
from collections.abc import Mapping
from typing import Any

from .parsed_value_classifier import (
    classify_raw_value,
    disposition_by_review_item_id,
    load_disposition,
)


CANDIDATE_RUN_ID = "20260525T000000Z"
CANDIDATE_JSON_PATH = f"data/current-facts/candidate-inputs/{CANDIDATE_RUN_ID}-row-move-cell-candidates.json"
CANDIDATE_MD_PATH = f"docs/current-facts/candidate-inputs/{CANDIDATE_RUN_ID}-row-move-cell-candidates.md"
EVIDENCE_JSON_PATH = "data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json"
EVIDENCE_MD_PATH = "docs/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.md"
COVERAGE_JSON_PATH = "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"
ALLOWED_STATUSES = frozenset(
    {
        "annotated_candidate_not_calculation_safe",
        "parsed_range_not_single_value_calculation_safe",
    }
)


class CurrentFactCandidateGeneratorError(ValueError):
    """Raised when reviewed evidence cannot build candidate records."""


def build_candidate_input_payload(evidence_payload: Mapping[str, Any]) -> dict[str, Any]:
    _validate_evidence_top_level(evidence_payload)
    disposition_by_id = disposition_by_review_item_id(load_disposition())
    records = [
        _candidate_record(record, disposition_by_id)
        for record in evidence_payload["evidence_records"]
    ]
    return {
        "artifact_schema_version": "current_fact_row_move_cell_candidate_input/v1",
        "authority_boundary": {
            "official": "authority_candidate_only",
            "supercombo": "enrichment_or_cross_reference_only",
        },
        "candidate_boundary": {
            "blocked_records": "excluded_to_classifier_or_source_review",
            "legacy_raw_exports": "excluded_as_source_input",
            "local_source_payloads": "excluded_from_public_artifact",
            "lookup_ready_candidates": "parsed_value_only",
            "reviewer_observations": "observation_candidate_only_not_authority",
            "supercombo": "enrichment_or_cross_reference_only",
            "synthetic_fixtures": "not_source_truth",
        },
        "generated_from": _generated_from(evidence_payload),
        "records": sorted(records, key=_record_sort_key),
        "run_id": CANDIDATE_RUN_ID,
    }


def build_candidate_summary_markdown(
    candidate_payload: Mapping[str, Any],
    evidence_payload: Mapping[str, Any],
) -> str:
    records = candidate_payload.get("records", [])
    if not isinstance(records, list):
        raise CurrentFactCandidateGeneratorError("candidate payload records must be a list")
    status_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, Mapping))
    field_counts = Counter(record.get("field_key") for record in records if isinstance(record, Mapping))
    source_run_id = str(evidence_payload.get("source_run_id"))
    return "\n".join(
        [
            "# Current-Fact Row/Move/Cell Candidate Input",
            "",
            f"- JSON artifact: `{CANDIDATE_JSON_PATH}`",
            f"- Run ID: `{candidate_payload.get('run_id')}`",
            f"- Source evidence: `{EVIDENCE_JSON_PATH}`",
            f"- Source run ID: `{source_run_id}`",
            f"- Total records: `{len(records)}`",
            "- Candidate boundary: parsed-value-only, non-scalar values remain not calculation-safe.",
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
            "- No production source-record artifact is generated.",
            "- No production current-fact export artifact is generated.",
            "- Runtime lookup and answer behavior are unchanged.",
            "- `annotated_numeric_candidate` and `frame_range` must not be flattened into scalar values.",
            "",
        ]
    )


def _validate_evidence_top_level(evidence_payload: Mapping[str, Any]) -> None:
    expected = {
        "artifact_schema_version": "current_fact_candidate_evidence/v1",
        "artifact_boundary": "source_review_summary_only",
        "authority_status": "review_decision_only_not_authority",
        "candidate_artifact_generation": "blocked_until_mandatory_review",
        "run_id": "20260525",
        "source_run_id": "20260521T025403Z",
    }
    for key, value in expected.items():
        if evidence_payload.get(key) != value:
            raise CurrentFactCandidateGeneratorError(f"unexpected evidence {key}: {evidence_payload.get(key)!r}")
    records = evidence_payload.get("evidence_records")
    if not isinstance(records, list) or len(records) != 13:
        raise CurrentFactCandidateGeneratorError("evidence_records must contain exactly 13 records")


def _candidate_record(
    evidence_record: Mapping[str, Any],
    disposition_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    _validate_evidence_record(evidence_record)
    review_item_id = _single_review_item_id(evidence_record)
    disposition_record = disposition_by_id.get(review_item_id)
    if disposition_record is None:
        raise CurrentFactCandidateGeneratorError(f"missing disposition record for {review_item_id}")
    classification = classify_raw_value(str(evidence_record["raw_value"]), dict(disposition_record))
    if classification.parsed_value is None:
        raise CurrentFactCandidateGeneratorError(f"evidence record did not reproduce parsed_value: {review_item_id}")
    parser_rule_id = classification.value_shape.get("parser_rule_id")
    if evidence_record.get("parser_rule_ids") != [parser_rule_id]:
        raise CurrentFactCandidateGeneratorError(f"parser rule mismatch for {evidence_record.get('candidate_record_id')}")
    if classification.calculation_input_status != evidence_record.get("calculation_input_status"):
        raise CurrentFactCandidateGeneratorError(f"calculation status mismatch for {evidence_record.get('candidate_record_id')}")
    if classification.parsed_value.get("kind") != evidence_record.get("parsed_value_kind"):
        raise CurrentFactCandidateGeneratorError(f"parsed kind mismatch for {evidence_record.get('candidate_record_id')}")

    raw_value = str(evidence_record["raw_value"])
    expected_hash = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
    if evidence_record.get("raw_value_sha256") != expected_hash:
        raise CurrentFactCandidateGeneratorError(f"raw hash mismatch for {evidence_record.get('candidate_record_id')}")
    if evidence_record.get("raw_value_length") != len(raw_value):
        raise CurrentFactCandidateGeneratorError(f"raw length mismatch for {evidence_record.get('candidate_record_id')}")

    source_review_refs = sorted({EVIDENCE_JSON_PATH, *[str(ref) for ref in evidence_record["source_review_refs"]]})
    return {
        "acquisition_report_refs": copy.deepcopy(evidence_record["acquisition_report_refs"]),
        "authority_status": "authority_candidate",
        "calculation_input_status": classification.calculation_input_status,
        "candidate_record_id": str(evidence_record["candidate_record_id"]),
        "character_slug": str(evidence_record["character_slug"]),
        "coverage_refs": [COVERAGE_JSON_PATH],
        "display_label_ja": str(evidence_record["display_label_ja"]),
        "evidence": {
            "evidence_basis": "source_review_summary",
            "public_reference": EVIDENCE_JSON_PATH,
            "run_id": "20260521T025403Z",
            "source_header_path": copy.deepcopy(evidence_record["source_header_path"]),
            "source_label": str(evidence_record["source_label"]),
            "source_name": str(evidence_record["source_name"]),
            "source_role": str(evidence_record["source_role"]),
        },
        "field_key": str(evidence_record["field_key"]),
        "move_id": str(evidence_record["move_id"]),
        "parsed_value": copy.deepcopy(classification.parsed_value),
        "parser_rule_ids": copy.deepcopy(evidence_record["parser_rule_ids"]),
        "raw_value": raw_value,
        "raw_value_length": len(raw_value),
        "raw_value_sha256": expected_hash,
        "source_cell_key": str(evidence_record["source_cell_key"]),
        "source_cell_order": int(evidence_record["source_cell_order"]),
        "source_family": str(evidence_record["source_family"]),
        "source_header_path": copy.deepcopy(evidence_record["source_header_path"]),
        "source_label": str(evidence_record["source_label"]),
        "source_name": str(evidence_record["source_name"]),
        "source_review_refs": source_review_refs,
        "source_role": str(evidence_record["source_role"]),
        "source_row_key": str(evidence_record["source_row_key"]),
        "source_row_order": int(evidence_record["source_row_order"]),
        "source_value_key": str(evidence_record["source_value_key"]),
        "value_shape": copy.deepcopy(classification.value_shape),
    }


def _validate_evidence_record(evidence_record: Mapping[str, Any]) -> None:
    expected = {
        "authority_status": "authority_candidate_not_promoted",
        "candidate_generation_status": "blocked_until_candidate_artifact_execplan_review",
        "source_name": "official",
        "source_role": "authority_candidate",
        "source_review_result": "candidate_identity_evidence_found",
    }
    for key, value in expected.items():
        if evidence_record.get(key) != value:
            raise CurrentFactCandidateGeneratorError(
                f"{evidence_record.get('candidate_record_id')} has unexpected {key}: {evidence_record.get(key)!r}"
            )
    if evidence_record.get("calculation_input_status") not in ALLOWED_STATUSES:
        raise CurrentFactCandidateGeneratorError(f"unsupported calculation status: {evidence_record.get('calculation_input_status')}")
    if "parsed_value" in evidence_record:
        raise CurrentFactCandidateGeneratorError("source-review evidence must not provide parsed_value payloads")


def _single_review_item_id(evidence_record: Mapping[str, Any]) -> str:
    coverage_refs = evidence_record.get("coverage_refs")
    if not isinstance(coverage_refs, list) or len(coverage_refs) != 1 or not isinstance(coverage_refs[0], str):
        raise CurrentFactCandidateGeneratorError(f"{evidence_record.get('candidate_record_id')} must have one review item ref")
    return coverage_refs[0]


def _generated_from(evidence_payload: Mapping[str, Any]) -> list[str]:
    generated_from = {
        EVIDENCE_JSON_PATH,
        EVIDENCE_MD_PATH,
        *[str(ref) for ref in evidence_payload.get("generated_from", [])],
    }
    return sorted(generated_from)


def _record_sort_key(record: Mapping[str, Any]) -> tuple[str, str, int, int, str]:
    return (
        str(record.get("source_name", "")),
        str(record.get("character_slug", "")),
        int(record.get("source_row_order", 0)),
        int(record.get("source_cell_order", 0)),
        str(record.get("source_value_key", "")),
    )
