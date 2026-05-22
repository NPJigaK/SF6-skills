from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "data/source-reviews/20260521T025403Z-value-shape-blocked-source-review-summary.json"
MD_PATH = ROOT / "docs/source-reviews/20260521T025403Z-value-shape-blocked-source-review.md"
EXPECTED_IDS = {
    "value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1",
    "value-shape:official--source_specific_expression--u_1aa6a6f86513",
    "value-shape:supercombo--unclassified_expression--character_vitals--throw_range_hurtbox",
}
DISPOSITIONS = {
    "parse_rule_required_before_schema",
    "schema_supports_raw_only",
}
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
]


def main() -> int:
    errors: list[str] = []
    if not JSON_PATH.exists():
        errors.append(f"Missing {JSON_PATH.relative_to(ROOT)}")
    if not MD_PATH.exists():
        errors.append(f"Missing {MD_PATH.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if payload.get("artifact_schema_version") != "value_shape_source_review_summary/v1":
        errors.append("unexpected artifact_schema_version")
    if payload.get("run_id") != "20260521T025403Z":
        errors.append("unexpected run_id")
    if payload.get("artifact_boundary") != "source_review_summary_only":
        errors.append("artifact_boundary must be source_review_summary_only")
    if payload.get("authority_status") != "review_decision_only_not_authority":
        errors.append("authority_status must be review_decision_only_not_authority")

    records = payload.get("review_records", [])
    ids = {record.get("review_item_id") for record in records}
    if len(records) != 3 or payload.get("total_review_records") != 3:
        errors.append("source review must contain exactly 3 records")
    if ids != EXPECTED_IDS:
        errors.append("source review records do not match blocked disposition IDs")

    for index, record in enumerate(records):
        if record.get("source_review_result") != "resolved_for_disposition":
            errors.append(f"review_records[{index}] must be resolved_for_disposition")
        if record.get("disposition_recommendation") not in DISPOSITIONS:
            errors.append(f"review_records[{index}] has invalid disposition recommendation")
        if record.get("source_name") == "official" and record.get("source_role") != "authority_candidate":
            errors.append(f"review_records[{index}] official role must remain authority_candidate")
        if record.get("source_name") == "supercombo" and record.get("source_role") != "enrichment_candidate":
            errors.append(f"review_records[{index}] SuperCombo role must remain enrichment_candidate")
        if "parsed_value" in record or "current_fact_authority" in json.dumps(record, ensure_ascii=False):
            errors.append(f"review_records[{index}] must not include parsed values or authority promotion")

    for path in (JSON_PATH, MD_PATH):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
                break
        for literal in [".local/", ".venv/", ".agents/", "/tmp", "page.html", "official_table_rows.raw.json", "supercombo_tables.raw.json"]:
            if literal in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden literal: {literal}")
    return _finish(errors)


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Value-shape source review validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
