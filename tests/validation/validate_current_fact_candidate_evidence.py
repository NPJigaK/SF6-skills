from __future__ import annotations

import json
import re
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json"
MD_PATH = ROOT / "docs/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.md"
COVERAGE_PATH = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"
NOTE_REVIEW_PATH = ROOT / "data/source-reviews/20260524-official-note-linkage-source-review-summary.json"

EXPECTED_FIELD_COUNTS = {
    "block_advantage": 5,
    "hit_advantage": 4,
    "startup": 4,
}
EXPECTED_STATUS_COUNTS = {
    "annotated_candidate_not_calculation_safe": 9,
    "parsed_range_not_single_value_calculation_safe": 4,
}
EXPECTED_RAW_COUNTS = {
    ("block_advantage", "-12～-1"): 1,
    ("block_advantage", "-39～-33"): 1,
    ("block_advantage", "-4～-1"): 1,
    ("block_advantage", "※-2"): 1,
    ("block_advantage", "※-4"): 1,
    ("hit_advantage", "-28～-23"): 1,
    ("hit_advantage", "※-1"): 1,
    ("hit_advantage", "※-3"): 1,
    ("hit_advantage", "※-4"): 1,
    ("startup", "122※"): 3,
    ("startup", "128※"): 1,
}
EXPECTED_HEADERS = {
    "block_advantage": ["硬直差", "ガード"],
    "hit_advantage": ["硬直差", "ヒット"],
    "startup": ["動作フレーム", "発生"],
}
EXPECTED_CALCULATION_KIND = {
    "annotated_candidate_not_calculation_safe": "annotated_numeric_candidate",
    "parsed_range_not_single_value_calculation_safe": "frame_range",
}
REQUIRED_RECORD_KEYS = {
    "acquisition_report_refs",
    "authority_status",
    "calculation_input_status",
    "candidate_generation_status",
    "candidate_record_id",
    "cell_note_marker_count",
    "character_slug",
    "coverage_refs",
    "display_label_ja",
    "evidence_id",
    "field_key",
    "move_id",
    "move_id_derivation_status",
    "note_linkage_status",
    "parsed_value_kind",
    "parsed_value_payload_status",
    "parser_rule_ids",
    "raw_value",
    "raw_value_length",
    "raw_value_sha256",
    "row_note_candidate_count",
    "source_cell_key",
    "source_cell_order",
    "source_family",
    "source_header_path",
    "source_label",
    "source_name",
    "source_review_refs",
    "source_role",
    "source_row_key",
    "source_row_order",
    "source_review_ids",
    "source_review_result",
    "source_value_key",
    "value_shape",
}
PUBLIC_PATH_RE = re.compile(r"^(data|docs|contracts)/[A-Za-z0-9_.:/-]+$")
IDENTITY_RE = re.compile(r"^[a-z0-9][a-z0-9_.:-]*$")
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/(?:home|mnt|Users)/[^\s\"'`]+)"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|chatgpt|vlm|trace|debug dump|answer[-_ ]?log|training[-_ ]?log)\b"),
]
FORBIDDEN_LITERALS = {
    ".agents/",
    ".local/",
    ".venv/",
    "__NEXT_DATA__.json",
    "data/exports/",
    "full raw row",
    "official_table_rows.raw.json",
    "page.html",
    "private vault",
}


def main() -> int:
    errors: list[str] = []
    for path in (JSON_PATH, MD_PATH, COVERAGE_PATH, NOTE_REVIEW_PATH):
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    note_review = json.loads(NOTE_REVIEW_PATH.read_text(encoding="utf-8"))

    _validate_top_level(payload, errors)
    _validate_source_evidence_summary(payload.get("source_evidence_summary"), errors)
    _validate_generated_from(payload.get("generated_from"), errors)

    records = payload.get("evidence_records", [])
    if not isinstance(records, list) or len(records) != 13:
        errors.append("evidence_records must contain exactly 13 records")
        records = []
    _validate_counts(payload.get("record_counts"), records, errors)

    coverage_by_id = {
        record.get("review_item_id"): record
        for record in coverage.get("coverage_records", [])
        if record.get("source_name") == "official"
    }
    note_review_ids = {
        record.get("source_review_id")
        for record in note_review.get("review_records", [])
        if isinstance(record, dict)
    }

    ids: dict[str, set[str]] = {
        "candidate_record_id": set(),
        "evidence_id": set(),
        "source_cell_key": set(),
        "source_value_key": set(),
    }
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"evidence_records[{index}] must be an object")
            continue
        _validate_record(index, record, coverage_by_id, note_review_ids, errors)
        for key, seen in ids.items():
            value = record.get(key)
            if value in seen:
                errors.append(f"{key} must be unique: {value}")
            if isinstance(value, str):
                seen.add(value)

    for path in (JSON_PATH, MD_PATH):
        _validate_public_text_boundary(path, errors)

    return _finish(errors)


def _validate_top_level(payload: dict[str, object], errors: list[str]) -> None:
    expected = {
        "artifact_schema_version": "current_fact_candidate_evidence/v1",
        "artifact_boundary": "source_review_summary_only",
        "authority_status": "review_decision_only_not_authority",
        "candidate_artifact_generation": "blocked_until_mandatory_review",
        "run_id": "20260525",
        "source_run_id": "20260521T025403Z",
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            errors.append(f"{key} must be {value!r}")


def _validate_source_evidence_summary(summary: object, errors: list[str]) -> None:
    if not isinstance(summary, dict):
        errors.append("source_evidence_summary must be an object")
        return
    expected_flags = {
        "candidate_artifact_generated": False,
        "current_fact_export_generated": False,
        "ignored_structured_v4_rows_used_as_reviewer_input": True,
        "ignored_structured_payloads_committed": False,
        "issue_343_gate_required_for_future_value_expansion": True,
        "live_acquisition_run": False,
        "reviewer_observation_output_used_as_authority": False,
        "source_record_artifact_generated": False,
        "value_handling_change": False,
    }
    for key, expected in expected_flags.items():
        if summary.get(key) is not expected:
            errors.append(f"source_evidence_summary.{key} must be {expected!r}")


def _validate_generated_from(generated_from: object, errors: list[str]) -> None:
    if not isinstance(generated_from, list) or not generated_from:
        errors.append("generated_from must be a non-empty list")
        return
    for ref in generated_from:
        _validate_public_ref(ref, "generated_from", errors)


def _validate_counts(counts: object, records: list[object], errors: list[str]) -> None:
    if not isinstance(counts, dict):
        errors.append("record_counts must be an object")
        return
    if counts.get("total_evidence_records") != len(records):
        errors.append("record_counts.total_evidence_records must match evidence_records length")
    field_counts = Counter(record.get("field_key") for record in records if isinstance(record, dict))
    status_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, dict))
    result_counts = Counter(record.get("source_review_result") for record in records if isinstance(record, dict))
    if dict(sorted(field_counts.items())) != EXPECTED_FIELD_COUNTS:
        errors.append("field counts do not match expected evidence records")
    if dict(sorted(status_counts.items())) != EXPECTED_STATUS_COUNTS:
        errors.append("calculation_input_status counts do not match expected evidence records")
    if dict(sorted(result_counts.items())) != {"candidate_identity_evidence_found": len(records)}:
        errors.append("source_review_result counts must all be candidate_identity_evidence_found")
    if counts.get("by_field_key") != EXPECTED_FIELD_COUNTS:
        errors.append("record_counts.by_field_key is incorrect")
    if counts.get("by_calculation_input_status") != EXPECTED_STATUS_COUNTS:
        errors.append("record_counts.by_calculation_input_status is incorrect")

    raw_counts = Counter(
        (record.get("field_key"), record.get("raw_value")) for record in records if isinstance(record, dict)
    )
    if dict(sorted(raw_counts.items())) != dict(sorted(EXPECTED_RAW_COUNTS.items())):
        errors.append("raw value evidence counts do not match expected records")


def _validate_record(
    index: int,
    record: dict[str, object],
    coverage_by_id: dict[object, dict[str, object]],
    note_review_ids: set[object],
    errors: list[str],
) -> None:
    missing = sorted(REQUIRED_RECORD_KEYS - set(record))
    if missing:
        errors.append(f"evidence_records[{index}] missing keys: {', '.join(missing)}")
    if "parsed_value" in record:
        errors.append(f"evidence_records[{index}] must not include parsed_value payloads")
    if "current_fact_authority" in json.dumps(record, ensure_ascii=False):
        errors.append(f"evidence_records[{index}] must not include current fact authority promotion")

    if record.get("source_name") != "official":
        errors.append(f"evidence_records[{index}] source_name must be official")
    if record.get("source_role") != "authority_candidate":
        errors.append(f"evidence_records[{index}] source_role must remain authority_candidate")
    if record.get("authority_status") != "authority_candidate_not_promoted":
        errors.append(f"evidence_records[{index}] must not promote official authority")
    if record.get("candidate_generation_status") != "blocked_until_candidate_artifact_execplan_review":
        errors.append(f"evidence_records[{index}] must keep candidate generation blocked")
    if record.get("source_review_result") != "candidate_identity_evidence_found":
        errors.append(f"evidence_records[{index}] has invalid source_review_result")
    if record.get("move_id_derivation_status") != "source_row_scoped_candidate_not_global_move_id":
        errors.append(f"evidence_records[{index}] must record row-scoped move-id derivation")

    field_key = record.get("field_key")
    if record.get("source_header_path") != EXPECTED_HEADERS.get(field_key):
        errors.append(f"evidence_records[{index}] has invalid source_header_path")
    raw_value = record.get("raw_value")
    if not isinstance(raw_value, str):
        errors.append(f"evidence_records[{index}] raw_value must be a string")
    else:
        if record.get("raw_value_length") != len(raw_value):
            errors.append(f"evidence_records[{index}] raw_value_length mismatch")
        if record.get("raw_value_sha256") != sha256(raw_value.encode("utf-8")).hexdigest():
            errors.append(f"evidence_records[{index}] raw_value_sha256 mismatch")

    calculation_status = record.get("calculation_input_status")
    expected_kind = EXPECTED_CALCULATION_KIND.get(calculation_status)
    if record.get("parsed_value_kind") != expected_kind:
        errors.append(f"evidence_records[{index}] parsed_value_kind does not match calculation status")
    value_shape = record.get("value_shape")
    if not isinstance(value_shape, dict):
        errors.append(f"evidence_records[{index}] value_shape must be an object")
    elif value_shape.get("parsed_value_kind") != record.get("parsed_value_kind"):
        errors.append(f"evidence_records[{index}] value_shape kind mismatch")

    for key in ("candidate_record_id", "evidence_id", "move_id", "source_cell_key", "source_row_key", "source_value_key"):
        value = record.get(key)
        if not isinstance(value, str) or not IDENTITY_RE.fullmatch(value):
            errors.append(f"evidence_records[{index}].{key} has invalid identity format")
    for key in ("source_cell_order", "source_row_order"):
        if not isinstance(record.get(key), int) or record[key] < 0:
            errors.append(f"evidence_records[{index}].{key} must be a non-negative integer")
    for refs_key in ("acquisition_report_refs", "source_review_refs"):
        refs = record.get(refs_key)
        if not isinstance(refs, list):
            errors.append(f"evidence_records[{index}].{refs_key} must be a list")
            continue
        for ref in refs:
            _validate_public_ref(ref, f"evidence_records[{index}].{refs_key}", errors)

    coverage_refs = record.get("coverage_refs")
    if not isinstance(coverage_refs, list) or len(coverage_refs) != 1:
        errors.append(f"evidence_records[{index}] must have exactly one coverage ref")
        return
    coverage_record = coverage_by_id.get(coverage_refs[0])
    if not coverage_record:
        errors.append(f"evidence_records[{index}] references missing coverage record")
        return
    _validate_coverage_ref(index, record, coverage_record, errors)

    for source_review_id in record.get("source_review_ids", []):
        if isinstance(source_review_id, str) and source_review_id.startswith("source-review:official-note-linkage"):
            if source_review_id not in note_review_ids:
                errors.append(f"evidence_records[{index}] references missing note-linkage source review")


def _validate_coverage_ref(index: int, record: dict[str, object], coverage_record: dict[str, object], errors: list[str]) -> None:
    parser_rule_ids = record.get("parser_rule_ids")
    if parser_rule_ids != coverage_record.get("parser_rule_ids"):
        errors.append(f"evidence_records[{index}] parser rules do not match coverage")
    if record.get("field_key") != coverage_record.get("proposed_field_key"):
        errors.append(f"evidence_records[{index}] field_key does not match coverage")
    if record.get("source_header_path") != coverage_record.get("source_header_path"):
        errors.append(f"evidence_records[{index}] source_header_path does not match coverage")
    if record.get("source_role") != coverage_record.get("source_role"):
        errors.append(f"evidence_records[{index}] source_role does not match coverage")

    if coverage_record.get("classifier_decision") == "partial_raw_value_coverage":
        variants = coverage_record.get("raw_value_variant_coverage", [])
        variant = next((item for item in variants if item.get("raw_value") == record.get("raw_value")), None)
        if not variant:
            errors.append(f"evidence_records[{index}] raw value is not covered by partial coverage")
            return
        if variant.get("classifier_decision") != "parsed_numeric_structured":
            errors.append(f"evidence_records[{index}] must not use blocked raw variants")
        if variant.get("calculation_input_status") != record.get("calculation_input_status"):
            errors.append(f"evidence_records[{index}] raw variant calculation status mismatch")
        if variant.get("raw_value_sha256") != "sha256:" + record.get("raw_value_sha256", ""):
            errors.append(f"evidence_records[{index}] raw variant hash mismatch")
        return

    if coverage_record.get("classifier_decision") != "parsed_numeric_structured":
        errors.append(f"evidence_records[{index}] coverage must be parsed or partial parsed")
    if coverage_record.get("calculation_input_status") != record.get("calculation_input_status"):
        errors.append(f"evidence_records[{index}] calculation status does not match coverage")


def _validate_public_ref(ref: object, context: str, errors: list[str]) -> None:
    if not isinstance(ref, str) or not PUBLIC_PATH_RE.fullmatch(ref):
        errors.append(f"{context} has invalid public ref: {ref!r}")
        return
    if ref.startswith("data/exports/") or ".local/" in ref:
        errors.append(f"{context} uses forbidden source ref: {ref}")
        return
    if not (ROOT / ref).exists():
        errors.append(f"{context} references missing path: {ref}")


def _validate_public_text_boundary(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
            break
    for literal in FORBIDDEN_LITERALS:
        if literal in text:
            errors.append(f"{path.relative_to(ROOT)} contains forbidden literal: {literal}")


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Current-fact candidate evidence validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
