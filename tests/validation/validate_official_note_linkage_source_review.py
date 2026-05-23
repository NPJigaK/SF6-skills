from __future__ import annotations

import json
import re
import sys
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "data/source-reviews/20260524-official-note-linkage-source-review-summary.json"
MD_PATH = ROOT / "docs/source-reviews/20260524-official-note-linkage-source-review.md"
COVERAGE_PATH = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"

ALLOWED_RESULTS = {
    "source_evidence_found_acquisition_field_gap",
    "source_confirmed_non_note_grammar_blocked",
}
ALLOWED_ELIGIBILITY = {
    "blocked_pending_acquisition_fields",
    "not_note_linkage_target",
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

    records = payload.get("review_records", [])
    actual_ids = {record.get("review_item_id") for record in records}
    if actual_ids != expected_ids:
        errors.append("review_records do not match official review_required coverage records")

    for index, record in enumerate(records):
        _validate_record(index, record, errors)

    for record in records:
        if record.get("review_item_id", "").startswith("value-shape:official--malformed_looking_source_value"):
            if record.get("later_parser_eligibility") != "not_note_linkage_target":
                errors.append("malformed active group must remain not_note_linkage_target")
        elif record.get("later_parser_eligibility") != "blocked_pending_acquisition_fields":
            errors.append(f"{record.get('review_item_id')} must remain blocked_pending_acquisition_fields")

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


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Official note-linkage source review validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
