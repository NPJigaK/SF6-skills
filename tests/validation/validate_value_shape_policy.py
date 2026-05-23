from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY_JSON = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json"
POLICY_MD = ROOT / "docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.md"
DISPOSITION_JSON = ROOT / "data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json"
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
]


def main() -> int:
    errors: list[str] = []
    for path in (POLICY_JSON, POLICY_MD, DISPOSITION_JSON):
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    policy = json.loads(POLICY_JSON.read_text(encoding="utf-8"))
    disposition = json.loads(DISPOSITION_JSON.read_text(encoding="utf-8"))
    if policy.get("artifact_schema_version") != "parsed_value_classifier_enum_policy/v1":
        errors.append("unexpected policy schema version")
    if policy.get("authority_status") != "policy_only_not_authority":
        errors.append("policy must not claim authority")
    if policy.get("parsed_value_implementation") != "not_implemented":
        errors.append("policy must not implement parsed values")
    if policy.get("json_schema_redesign_status") != "ready_for_schema_design_after_policy_review":
        errors.append("unexpected JSON Schema redesign status")

    parse_counts = Counter(
        record["semantic_source_family"]
        for record in disposition["dispositions"]
        if record["disposition"] == "parse_rule_required_before_schema"
    )
    enum_counts = Counter(
        record["semantic_source_family"]
        for record in disposition["dispositions"]
        if record["disposition"] == "source_specific_enum_required"
    )
    if policy.get("parse_rule_policy_counts") != dict(sorted(parse_counts.items())):
        errors.append("parse_rule_policy_counts do not match disposition artifact")
    if policy.get("enum_policy_counts") != dict(sorted(enum_counts.items())):
        errors.append("enum_policy_counts do not match disposition artifact")
    if policy.get("total_parse_rule_policy_records") != sum(parse_counts.values()):
        errors.append("total_parse_rule_policy_records mismatch")
    if policy.get("total_enum_policy_records") != sum(enum_counts.values()):
        errors.append("total_enum_policy_records mismatch")

    parse_families = {record.get("semantic_source_family") for record in policy.get("parse_rule_policies", [])}
    enum_families = {record.get("semantic_source_family") for record in policy.get("enum_policies", [])}
    if parse_families != set(parse_counts):
        errors.append("parse_rule_policies do not cover every parse family")
    if enum_families != set(enum_counts):
        errors.append("enum_policies do not cover every enum family")
    if "current_fact_authority" in json.dumps(policy, ensure_ascii=False):
        errors.append("policy must not mention current_fact_authority")

    for path in (POLICY_JSON, POLICY_MD):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
                break
    return _finish(errors)


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Value-shape policy validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
