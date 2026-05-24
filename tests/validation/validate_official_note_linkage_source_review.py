from __future__ import annotations

import json
import re
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "data/source-reviews/20260524-official-note-linkage-source-review-summary.json"
MD_PATH = ROOT / "docs/source-reviews/20260524-official-note-linkage-source-review.md"
COVERAGE_PATH = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"

ALLOWED_RESULTS = {
    "structured_row_note_evidence_found",
    "structured_row_note_evidence_ambiguous",
    "structured_row_note_evidence_missing",
    "source_confirmed_non_note_grammar_blocked",
}
ALLOWED_ELIGIBILITY = {
    "later_annotated_parser_eligible",
    "blocked_pending_source_review",
    "blocked_pending_acquisition_fields",
    "not_note_linkage_target",
}
REQUIRED_V4_FIELDS = {
    "official_table_rows_raw/v4",
    "row_note_count",
    "row_notes",
    "row_note_extraction_status",
    "cell_note_markers",
    "cell_note_ids",
    "row_note_reference_candidates",
    "note_linkage_status",
}
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/(?:home|mnt|Users)/[^\s\"'`]+)"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
]
FORBIDDEN_LITERALS = {
    ".agents/",
    ".local/",
    ".venv/",
    "/tmp",
    "__NEXT_DATA__.json",
    "official_table_rows.raw.json",
    "page.html",
}


def main() -> int:
    errors: list[str] = []
    if not JSON_PATH.exists():
        errors.append(f"Missing {JSON_PATH.relative_to(ROOT)}")
    if not MD_PATH.exists():
        errors.append(f"Missing {MD_PATH.relative_to(ROOT)}")
    if not COVERAGE_PATH.exists():
        errors.append(f"Missing {COVERAGE_PATH.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    expected_ids = {
        record["review_item_id"]
        for record in coverage["coverage_records"]
        if record.get("source_name") == "official" and record.get("classifier_decision") == "review_required"
    }

    if payload.get("artifact_schema_version") != "official_note_linkage_source_review_summary/v1":
        errors.append("unexpected artifact_schema_version")
    if payload.get("run_id") != "20260524":
        errors.append("unexpected run_id")
    if payload.get("artifact_boundary") != "source_review_summary_only":
        errors.append("artifact_boundary must be source_review_summary_only")
    if payload.get("authority_status") != "review_decision_only_not_authority":
        errors.append("authority_status must be review_decision_only_not_authority")
    if payload.get("total_review_records") != 9 or payload.get("review_counts", {}).get("total_review_records") != 9:
        errors.append("official note-linkage source review must contain exactly 9 records")
    _validate_source_evidence_summary(payload.get("source_evidence_summary"), errors)

    records = payload.get("review_records", [])
    actual_ids = {record.get("review_item_id") for record in records}
    if actual_ids != expected_ids:
        errors.append("review_records do not match official review_required coverage records")

    expected_counts = Counter(record.get("source_review_result") for record in records)
    expected_counts.update(record.get("later_parser_eligibility") for record in records)
    expected_counts["total_review_records"] = len(records)
    if payload.get("review_counts") != dict(sorted(expected_counts.items())):
        errors.append("review_counts must match source_review_result and later_parser_eligibility values")

    for index, record in enumerate(records):
        _validate_record(index, record, errors)

    for record in records:
        if record.get("review_item_id", "").startswith("value-shape:official--malformed_looking_source_value"):
            if record.get("later_parser_eligibility") != "not_note_linkage_target":
                errors.append("malformed active group must remain not_note_linkage_target")
            if record.get("source_review_result") != "source_confirmed_non_note_grammar_blocked":
                errors.append("malformed active group must remain source_confirmed_non_note_grammar_blocked")
        elif record.get("source_review_result") == "structured_row_note_evidence_ambiguous":
            if record.get("later_parser_eligibility") != "blocked_pending_source_review":
                errors.append(f"{record.get('review_item_id')} ambiguous evidence must remain blocked_pending_source_review")
        elif record.get("source_review_result") == "structured_row_note_evidence_missing":
            if record.get("later_parser_eligibility") != "blocked_pending_acquisition_fields":
                errors.append(f"{record.get('review_item_id')} missing v4 evidence must remain blocked_pending_acquisition_fields")
        elif record.get("source_review_result") == "structured_row_note_evidence_found":
            if record.get("later_parser_eligibility") != "later_annotated_parser_eligible":
                errors.append(f"{record.get('review_item_id')} found evidence must only become later_annotated_parser_eligible")
        elif record.get("later_parser_eligibility") != "blocked_pending_acquisition_fields":
            errors.append(f"{record.get('review_item_id')} has invalid source-review/eligibility combination")

    for path in (JSON_PATH, MD_PATH):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
                break
        for literal in FORBIDDEN_LITERALS:
            if literal in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden literal: {literal}")

    return _finish(errors)


def _validate_source_evidence_summary(summary: object, errors: list[str]) -> None:
    if not isinstance(summary, dict):
        errors.append("source_evidence_summary must be an object")
        return
    expected_flags = {
        "live_acquisition_run": False,
        "reviewer_only_chatgpt_vlm_observation_used": False,
        "official_table_rows_v4_seen": True,
        "row_note_text_in_structured_table_row_artifact": True,
        "table_cell_boundaries_seen_in_structured_table_row_artifact": True,
        "visible_hidden_detail_fields_seen_in_structured_table_row_artifact": True,
    }
    for key, expected in expected_flags.items():
        if summary.get(key) is not expected:
            errors.append(f"source_evidence_summary.{key} must be {expected!r}")


def _validate_record(index: int, record: dict[str, object], errors: list[str]) -> None:
    required = {
        "affected_count",
        "cell_boundary_status",
        "later_parser_eligibility",
        "marker_roles",
        "note_review_status",
        "note_scope",
        "note_text_status",
        "proposed_field_key",
        "representative_examples",
        "required_source_fields_checked",
        "review_item_id",
        "row_identity_status",
        "semantic_source_family",
        "source_header_path",
        "source_name",
        "source_review_id",
        "source_review_result",
        "source_role",
        "v4_representative_evidence",
        "visible_hidden_detail_status",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"review_records[{index}] missing keys: {', '.join(missing)}")
    if record.get("source_name") != "official":
        errors.append(f"review_records[{index}] source_name must be official")
    if record.get("source_role") != "authority_candidate":
        errors.append(f"review_records[{index}] source_role must remain authority_candidate")
    if record.get("source_review_result") not in ALLOWED_RESULTS:
        errors.append(f"review_records[{index}] has invalid source_review_result")
    if record.get("later_parser_eligibility") not in ALLOWED_ELIGIBILITY:
        errors.append(f"review_records[{index}] has invalid later_parser_eligibility")
    if "parsed_value" in record or "current_fact_authority" in json.dumps(record, ensure_ascii=False):
        errors.append(f"review_records[{index}] must not include parsed values or authority promotion")
    checked_fields = record.get("required_source_fields_checked")
    if not isinstance(checked_fields, list) or not REQUIRED_V4_FIELDS.issubset(set(checked_fields)):
        errors.append(f"review_records[{index}] must record required v4 source fields")
    _validate_v4_evidence(index, record.get("v4_representative_evidence"), errors)

    examples = record.get("representative_examples")
    if not isinstance(examples, list) or not examples or len(examples) > 3:
        errors.append(f"review_records[{index}] must include 1-3 representative examples")
        return
    for example_index, example in enumerate(examples):
        if not isinstance(example, dict):
            errors.append(f"review_records[{index}].representative_examples[{example_index}] must be an object")
            continue
        raw_value = example.get("raw_value")
        raw_length = example.get("raw_value_length")
        raw_hash = example.get("raw_value_sha256")
        if not isinstance(raw_value, str) or len(raw_value) > 80:
            errors.append(f"review_records[{index}].representative_examples[{example_index}] has invalid raw_value")
            continue
        if raw_length != len(raw_value):
            errors.append(f"review_records[{index}].representative_examples[{example_index}] has invalid length")
        expected_hash = "sha256:" + sha256(raw_value.encode("utf-8")).hexdigest()
        if raw_hash != expected_hash:
            errors.append(f"review_records[{index}].representative_examples[{example_index}] has invalid hash")


def _validate_v4_evidence(index: int, evidence: object, errors: list[str]) -> None:
    if not isinstance(evidence, dict):
        errors.append(f"review_records[{index}].v4_representative_evidence must be an object")
        return
    match_count = evidence.get("representative_match_count")
    status_counts = evidence.get("note_linkage_status_counts")
    candidate_range = evidence.get("row_note_reference_candidate_count_range")
    if not isinstance(match_count, int) or match_count <= 0:
        errors.append(f"review_records[{index}].v4_representative_evidence has invalid match count")
    if not isinstance(status_counts, dict) or not status_counts:
        errors.append(f"review_records[{index}].v4_representative_evidence must include status counts")
    elif any(not isinstance(value, int) or value <= 0 for value in status_counts.values()):
        errors.append(f"review_records[{index}].v4_representative_evidence has invalid status count values")
    elif sum(status_counts.values()) != match_count:
        errors.append(f"review_records[{index}].v4_representative_evidence status counts must sum to match count")
    if (
        not isinstance(candidate_range, list)
        or len(candidate_range) != 2
        or not all(isinstance(value, int) and value >= 0 for value in candidate_range)
        or candidate_range[0] > candidate_range[1]
    ):
        errors.append(f"review_records[{index}].v4_representative_evidence has invalid candidate count range")
    for key in ("cell_note_markers_present", "cell_note_ids_present", "row_note_text_structured"):
        if not isinstance(evidence.get(key), bool):
            errors.append(f"review_records[{index}].v4_representative_evidence.{key} must be boolean")
    if not evidence.get("visible_hidden_detail_evidence"):
        errors.append(f"review_records[{index}].v4_representative_evidence.visible_hidden_detail_evidence is required")


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Official note-linkage source review validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
