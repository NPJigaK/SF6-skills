from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import repo_root


RUN_ID = "20260521T025403Z"
DISPOSITION_JSON = Path("data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json")
POLICY_JSON = Path("data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json")
SYSTEM_MECHANICS_MD = Path("docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md")
COVERAGE_JSON = Path("data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json")
COVERAGE_MD = Path("docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md")
ARTIFACT_SCHEMA_VERSION = "parsed_value_classifier_coverage/v2"

DISPOSITION_TO_DECISION = {
    "schema_supports_raw_only": "raw_preserved_non_calculation",
    "source_specific_enum_required": "enum_classified",
    "out_of_scope_first_normalized_export": "out_of_scope_first_normalized_export",
}

SUPPORTED_PARSE_RULES_BY_FAMILY = {
    "advantage": ["signed_frame.strict.v1"],
    "damage": ["integer_damage.strict.v1"],
    "gauge": ["gauge_amount.strict.v1"],
    "metadata": ["decimal_metric.strict.v1"],
    "mobility": ["decimal_metric.strict.v1"],
    "projectile": ["decimal_metric.strict.v1"],
    "throw": ["throw_range_hurtbox_pair.strict.v1"],
    "timing": ["frame_scalar.strict.v1", "frame_range.strict.v1"],
}

REVIEW_REQUIRED_FIELDS = {
    "combo_scaling": "System mechanics distinguishes starter, combo, immediate, multiplier, minimum, and exception scaling; current schema has no safe structured scaling object.",
    "supercombo_juggle_increase": "Juggle fields need domain-specific objects and Capcom/community terminology mapping before calculation use.",
    "supercombo_juggle_limit": "Juggle fields need domain-specific objects and Capcom/community terminology mapping before calculation use.",
    "supercombo_juggle_start": "Juggle fields need domain-specific objects and Capcom/community terminology mapping before calculation use.",
}

SYSTEM_MECHANICS_ANCHORS = {
    "time_and_frames": "One frame is one sixtieth of a second.",
    "active_window_sequence": "X(n)Y",
    "context_parentheses": "X(Y)",
    "knockdown": "`KD` means knockdown",
    "scaling": "`combo_scaling` cannot be a single percent field",
    "gauge": "gauge parsers need explicit unit conversion and event context",
    "enum": "Unknown tokens must be review-required, not guessed.",
    "juggle": "juggle values are not ordinary signed integers",
    "spatial": "mobility/spatial values require domain-specific units and",
    "supercombo_boundary": "numeric authority table",
}

INTEGER_RE = re.compile(r"^[+-]?\d+$")
UNSIGNED_INTEGER_RE = re.compile(r"^\d+$")
DECIMAL_RE = re.compile(r"^[+-]?(?:\d+\.\d+|\d+)$")
FRAME_RANGE_RE = re.compile(r"^(\d+)\s*[-~]\s*(\d+)$")
OFFICIAL_SIGNED_WAVE_DASH_RANGE_RE = re.compile(r"^([+-]?\d+)～([+-]?\d+)$")
THROW_PAIR_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)$")
OFFICIAL_SIGNED_WAVE_DASH_RANGE_RULE_ID = "frame_range.official_signed_wave_dash.v1"
PARSED_RANGE_NOT_SINGLE_VALUE_CALCULATION_SAFE = "parsed_range_not_single_value_calculation_safe"
ANNOTATED_FRAME_SUFFIX_MARKER_RULE_ID = "annotated_frame.official_suffix_marker.v1"
ANNOTATED_SIGNED_FRAME_NEGATIVE_RULE_ID = "annotated_signed_frame.official_prefix_marker.negative.v1"
ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE = "annotated_candidate_not_calculation_safe"
PARTIAL_RAW_VALUE_COVERAGE_DECISION = "partial_raw_value_coverage"
ANNOTATED_STARTUP_REVIEW_ITEM_ID = "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100"
ANNOTATED_BLOCK_ADVANTAGE_REVIEW_ITEM_ID = "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
ANNOTATED_HIT_ADVANTAGE_REVIEW_ITEM_ID = "value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69"
OFFICIAL_SIGNED_WAVE_DASH_RANGE_REVIEW_ITEM_IDS = frozenset(
    {
        "value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb",
        "value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69",
    }
)
ANNOTATED_OFFICIAL_REVIEW_METADATA = {
    ANNOTATED_STARTUP_REVIEW_ITEM_ID: {
        "approved_raw_values": frozenset({"122※", "128※"}),
        "candidate_type": "unsigned_frame",
        "field_key": "startup",
        "marker_placement": "suffix",
        "note_scope": "row_startup_condition",
        "parser_rule_id": ANNOTATED_FRAME_SUFFIX_MARKER_RULE_ID,
        "source_column_header_path": ["動作フレーム", "発生"],
        "source_review_id": "source-review:official-note-linkage-startup",
    },
    ANNOTATED_BLOCK_ADVANTAGE_REVIEW_ITEM_ID: {
        "approved_raw_values": frozenset({"※-4", "※-2"}),
        "candidate_type": "signed_frame",
        "field_key": "block_advantage",
        "marker_placement": "prefix",
        "note_scope": "row_block_advantage_condition",
        "parser_rule_id": ANNOTATED_SIGNED_FRAME_NEGATIVE_RULE_ID,
        "source_column_header_path": ["硬直差", "ガード"],
        "source_review_id": "source-review:official-note-linkage-block-advantage",
    },
    ANNOTATED_HIT_ADVANTAGE_REVIEW_ITEM_ID: {
        "approved_raw_values": frozenset({"※-3", "※-1", "※-4"}),
        "candidate_type": "signed_frame",
        "field_key": "hit_advantage",
        "marker_placement": "prefix",
        "note_scope": "row_hit_advantage_condition",
        "parser_rule_id": ANNOTATED_SIGNED_FRAME_NEGATIVE_RULE_ID,
        "source_column_header_path": ["硬直差", "ヒット"],
        "source_review_id": "source-review:official-note-linkage-hit-advantage",
    },
}
ANNOTATED_OFFICIAL_RULE_IDS = frozenset(
    metadata["parser_rule_id"] for metadata in ANNOTATED_OFFICIAL_REVIEW_METADATA.values()
)
FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\\\\Users\\\\"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)\b(?:answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault|browser profile)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump)\b"),
]


@dataclass(frozen=True)
class ClassificationResult:
    raw_value: str
    classifier_decision: str
    value_shape: dict[str, Any]
    parsed_value: dict[str, Any] | None
    calculation_input_status: str
    policy_note: str
    review_required_reason: str | None = None

    def current_fact_fields(self) -> dict[str, Any]:
        fields: dict[str, Any] = {
            "raw_value": self.raw_value,
            "value_shape": self.value_shape,
        }
        if self.parsed_value is not None:
            fields["parsed_value"] = self.parsed_value
        return fields


def default_disposition_path() -> Path:
    return repo_root() / DISPOSITION_JSON


def default_policy_path() -> Path:
    return repo_root() / POLICY_JSON


def default_system_mechanics_path() -> Path:
    return repo_root() / SYSTEM_MECHANICS_MD


def default_coverage_json_path() -> Path:
    return repo_root() / COVERAGE_JSON


def default_coverage_md_path() -> Path:
    return repo_root() / COVERAGE_MD


def load_disposition(path: Path | None = None) -> dict[str, Any]:
    payload = json.loads((path or default_disposition_path()).read_text(encoding="utf-8"))
    if payload.get("run_id") != RUN_ID:
        raise ValueError(f"disposition run_id must be {RUN_ID}")
    return payload


def load_policy(path: Path | None = None) -> dict[str, Any]:
    payload = json.loads((path or default_policy_path()).read_text(encoding="utf-8"))
    if payload.get("run_id") != RUN_ID:
        raise ValueError(f"policy run_id must be {RUN_ID}")
    return payload


def load_system_mechanics_summary(path: Path | None = None) -> str:
    return (path or default_system_mechanics_path()).read_text(encoding="utf-8")


def disposition_by_review_item_id(disposition: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    payload = disposition or load_disposition()
    return {record["review_item_id"]: record for record in payload.get("dispositions", [])}


def classify_raw_value(raw_value: str | None, disposition_record: dict[str, Any]) -> ClassificationResult:
    raw = "" if raw_value is None else str(raw_value)
    stripped = raw.strip()
    disposition = str(disposition_record.get("disposition"))
    review_item_id = str(disposition_record.get("review_item_id"))
    family = str(disposition_record.get("semantic_source_family"))
    field_key = str(disposition_record.get("proposed_field_key") or "")
    source_name = str(disposition_record.get("source_name") or "")
    source_role = str(disposition_record.get("source_role") or "")

    if disposition == "out_of_scope_first_normalized_export":
        return _non_parsed_result(
            raw,
            "out_of_scope_first_normalized_export",
            "rejected",
            review_item_id,
            "out_of_scope_not_emitted",
            "Deferred from the first normalized export by reviewed disposition policy.",
        )
    if not stripped:
        return _non_parsed_result(
            raw,
            "raw_preserved_non_calculation",
            "raw_preserved",
            review_item_id,
            "raw_preserved_not_calculation",
            "Blank or missing source value is preserved but excluded from calculation.",
        )
    if disposition == "schema_supports_raw_only":
        return _non_parsed_result(
            raw,
            "raw_preserved_non_calculation",
            "raw_preserved",
            review_item_id,
            "raw_preserved_not_calculation",
            "Reviewed raw-only text is preserved and excluded from calculation.",
        )
    if disposition == "source_specific_enum_required":
        return _classify_enum(raw, disposition_record)
    if disposition != "parse_rule_required_before_schema":
        return _review_required(raw, review_item_id, f"Unsupported disposition for parser/classifier: {disposition}")

    unsupported_reason = _unsupported_field_reason(disposition_record)
    if unsupported_reason:
        return _review_required(raw, review_item_id, unsupported_reason)
    annotated = _parse_annotated_official_value(
        stripped,
        review_item_id=review_item_id,
        source_name=source_name,
        source_role=source_role,
        family=family,
        field_key=field_key,
    )
    if annotated is not None:
        parsed_value, parser_rule_id = annotated
        return ClassificationResult(
            raw_value=raw,
            classifier_decision="parsed_numeric_structured",
            value_shape={
                "classes": _infer_shape_classes(stripped),
                "classifier_status": "parsed",
                "parser_rule_id": parser_rule_id,
                "review_item_id": review_item_id,
            },
            parsed_value=parsed_value,
            calculation_input_status=ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE,
            policy_note="Parsed as an official annotated numeric candidate; the nested numeric token is condition-bound and not scalar calculation-safe.",
        )
    if family == "throw":
        parsed = _parse_supported_value(
            stripped,
            family=family,
            field_key=field_key,
            review_item_id=review_item_id,
            source_name=source_name,
        )
        if parsed is not None:
            parsed_value, parser_rule_id = parsed
            return ClassificationResult(
                raw_value=raw,
                classifier_decision="parsed_numeric_structured",
                value_shape={
                    "classes": ["scalar"],
                    "classifier_status": "parsed",
                    "parser_rule_id": parser_rule_id,
                    "review_item_id": review_item_id,
                },
                parsed_value=parsed_value,
                calculation_input_status=_parsed_calculation_status(disposition_record, parser_rule_id=parser_rule_id),
                policy_note="Parsed by a strict deterministic rule; calculators must still check source role, authority status, kind, unit, and domain.",
            )
    complex_reason = _complex_expression_reason(stripped)
    if complex_reason:
        return _review_required(raw, review_item_id, complex_reason)

    parsed = _parse_supported_value(
        stripped,
        family=family,
        field_key=field_key,
        review_item_id=review_item_id,
        source_name=source_name,
    )
    if parsed is None:
        return _review_required(raw, review_item_id, "No deterministic parser rule accepts this raw value shape.")
    parsed_value, parser_rule_id = parsed
    return ClassificationResult(
        raw_value=raw,
        classifier_decision="parsed_numeric_structured",
        value_shape={
            "classes": _infer_shape_classes(stripped),
            "classifier_status": "parsed",
            "parser_rule_id": parser_rule_id,
            "review_item_id": review_item_id,
        },
        parsed_value=parsed_value,
        calculation_input_status=_parsed_calculation_status(disposition_record, parser_rule_id=parser_rule_id),
        policy_note="Parsed by a strict deterministic rule; calculators must still check source role, authority status, kind, unit, and domain.",
    )


def build_coverage_payload(
    *,
    disposition: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    system_mechanics_summary: str | None = None,
) -> dict[str, Any]:
    disposition_payload = disposition or load_disposition()
    policy_payload = policy or load_policy()
    mechanics_text = system_mechanics_summary if system_mechanics_summary is not None else load_system_mechanics_summary()
    records = [_coverage_record(record) for record in disposition_payload.get("dispositions", [])]
    decision_counts = Counter(record["classifier_decision"] for record in records)
    calculation_counts = Counter(record["calculation_input_status"] for record in records)
    variant_records = [
        variant
        for record in records
        for variant in record.get("raw_value_variant_coverage", [])
        if isinstance(variant, dict)
    ]
    variant_decision_counts = Counter(variant["classifier_decision"] for variant in variant_records)
    variant_calculation_counts = Counter(variant["calculation_input_status"] for variant in variant_records)
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_id": RUN_ID,
        "artifact_boundary": "classifier_coverage_policy_only",
        "authority_status": "coverage_not_authority",
        "input_disposition": DISPOSITION_JSON.as_posix(),
        "input_policy": POLICY_JSON.as_posix(),
        "input_system_mechanics_summary": SYSTEM_MECHANICS_MD.as_posix(),
        "current_fact_export_status": "not_emitted",
        "normalized_export_generation": "not_implemented",
        "supercombo_numeric_authority": "forbidden",
        "system_mechanics_anchors_checked": _mechanics_anchor_presence(mechanics_text),
        "total_review_items": len(records),
        "classifier_decision_counts": dict(sorted(decision_counts.items())),
        "calculation_input_status_counts": dict(sorted(calculation_counts.items())),
        "raw_value_variant_decision_counts": dict(sorted(variant_decision_counts.items())),
        "raw_value_variant_calculation_input_status_counts": dict(sorted(variant_calculation_counts.items())),
        "parse_rule_policy_counts": policy_payload.get("parse_rule_policy_counts", {}),
        "enum_policy_counts": policy_payload.get("enum_policy_counts", {}),
        "coverage_records": records,
    }
    errors = validate_coverage_payload(
        payload,
        disposition=disposition_payload,
        policy=policy_payload,
        system_mechanics_summary=mechanics_text,
    )
    if errors:
        raise ValueError("\n".join(errors))
    return payload


def validate_coverage_payload(
    payload: dict[str, Any],
    *,
    disposition: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    system_mechanics_summary: str | None = None,
) -> list[str]:
    errors: list[str] = []
    disposition_payload = disposition or load_disposition()
    policy_payload = policy or load_policy()
    mechanics_text = system_mechanics_summary if system_mechanics_summary is not None else load_system_mechanics_summary()
    if payload.get("artifact_schema_version") != ARTIFACT_SCHEMA_VERSION:
        errors.append(f"artifact_schema_version must be {ARTIFACT_SCHEMA_VERSION}")
    if payload.get("run_id") != RUN_ID:
        errors.append(f"run_id must be {RUN_ID}")
    if payload.get("artifact_boundary") != "classifier_coverage_policy_only":
        errors.append("artifact_boundary must be classifier_coverage_policy_only")
    if payload.get("authority_status") != "coverage_not_authority":
        errors.append("authority_status must be coverage_not_authority")
    if payload.get("current_fact_export_status") != "not_emitted":
        errors.append("coverage artifact must not emit current-fact exports")
    if payload.get("supercombo_numeric_authority") != "forbidden":
        errors.append("coverage artifact must forbid SuperCombo numeric authority promotion")

    anchor_presence = payload.get("system_mechanics_anchors_checked", {})
    expected_anchor_presence = _mechanics_anchor_presence(mechanics_text)
    if anchor_presence != expected_anchor_presence:
        errors.append("system mechanics anchor checks do not match source summary")
    missing_anchors = sorted(anchor for anchor, present in expected_anchor_presence.items() if not present)
    if missing_anchors:
        errors.append(f"system mechanics summary missing parser anchors: {missing_anchors}")

    records = payload.get("coverage_records", [])
    if not isinstance(records, list):
        errors.append("coverage_records must be a list")
        records = []
    disposition_records = disposition_payload.get("dispositions", [])
    if payload.get("total_review_items") != len(disposition_records):
        errors.append("total_review_items must match disposition count")
    if len(records) != len(disposition_records):
        errors.append("coverage_records must cover every disposition record")
    disposition_ids = {record.get("review_item_id") for record in disposition_records}
    coverage_ids = [record.get("review_item_id") for record in records if isinstance(record, dict)]
    if set(coverage_ids) != disposition_ids:
        errors.append("coverage review_item_id set must match disposition artifact")
    duplicates = sorted(item_id for item_id, count in Counter(coverage_ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate coverage records: {duplicates[:3]}")

    parse_counts = Counter(
        record["semantic_source_family"]
        for record in records
        if isinstance(record, dict) and record.get("source_disposition") == "parse_rule_required_before_schema"
    )
    enum_counts = Counter(
        record["semantic_source_family"]
        for record in records
        if isinstance(record, dict) and record.get("source_disposition") == "source_specific_enum_required"
    )
    if dict(sorted(parse_counts.items())) != policy_payload.get("parse_rule_policy_counts"):
        errors.append("parse-rule coverage counts must match classifier policy artifact")
    if dict(sorted(enum_counts.items())) != policy_payload.get("enum_policy_counts"):
        errors.append("enum coverage counts must match classifier policy artifact")

    decision_counts = Counter(record.get("classifier_decision") for record in records if isinstance(record, dict))
    if payload.get("classifier_decision_counts") != dict(sorted(decision_counts.items())):
        errors.append("classifier_decision_counts mismatch")
    calculation_counts = Counter(record.get("calculation_input_status") for record in records if isinstance(record, dict))
    if payload.get("calculation_input_status_counts") != dict(sorted(calculation_counts.items())):
        errors.append("calculation_input_status_counts mismatch")
    variant_records = [
        variant
        for record in records
        if isinstance(record, dict)
        for variant in record.get("raw_value_variant_coverage", [])
        if isinstance(variant, dict)
    ]
    variant_decision_counts = Counter(variant.get("classifier_decision") for variant in variant_records)
    if payload.get("raw_value_variant_decision_counts") != dict(sorted(variant_decision_counts.items())):
        errors.append("raw_value_variant_decision_counts mismatch")
    variant_calculation_counts = Counter(variant.get("calculation_input_status") for variant in variant_records)
    if payload.get("raw_value_variant_calculation_input_status_counts") != dict(
        sorted(variant_calculation_counts.items())
    ):
        errors.append("raw_value_variant_calculation_input_status_counts mismatch")

    by_id = {record["review_item_id"]: record for record in disposition_records}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"coverage_records[{index}] must be an object")
            continue
        errors.extend(_coverage_record_errors(index, record, disposition_record=by_id.get(record.get("review_item_id"))))
    if _contains_forbidden_authority_claim(payload):
        errors.append("coverage artifact must not claim current_fact_authority")
    return errors


def write_coverage_artifacts(
    payload: dict[str, Any],
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> None:
    output_json = json_path or default_coverage_json_path()
    output_md = markdown_path or default_coverage_md_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_coverage_markdown(payload), encoding="utf-8")


def validate_coverage_artifacts(
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    output_json = json_path or default_coverage_json_path()
    output_md = markdown_path or default_coverage_md_path()
    if not output_json.exists():
        errors.append(f"Missing {_display_path(output_json)}")
    if not output_md.exists():
        errors.append(f"Missing {_display_path(output_md)}")
    if errors:
        return errors
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    errors.extend(validate_coverage_payload(payload))
    for path in (output_json, output_md):
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            if pattern.search(text):
                errors.append(f"{_display_path(path)} contains forbidden public content")
                break
    if errors:
        raise ValueError("\n".join(errors))
    return []


def render_coverage_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Parsed-Value Classifier Coverage",
        "",
        "This artifact records deterministic parser/classifier coverage decisions.",
        "It does not emit normalized current-fact exports, add calculators, or",
        "promote SuperCombo values to numeric authority.",
        "",
        f"- Run ID: `{payload['run_id']}`",
        f"- Input disposition: `{payload['input_disposition']}`",
        f"- Input policy: `{payload['input_policy']}`",
        f"- Input system mechanics summary: `{payload['input_system_mechanics_summary']}`",
        f"- Total review items: `{payload['total_review_items']}`",
        "",
        "## Classifier Decisions",
        "",
    ]
    for decision, count in payload["classifier_decision_counts"].items():
        lines.append(f"- `{decision}`: {count}")
    lines.extend(["", "## Calculation Input Status", ""])
    for status, count in payload["calculation_input_status_counts"].items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Raw Value Variant Coverage", ""])
    if payload.get("raw_value_variant_decision_counts"):
        lines.append("Classifier decisions:")
        lines.append("")
        for decision, count in payload["raw_value_variant_decision_counts"].items():
            lines.append(f"- `{decision}`: {count}")
        lines.extend(["", "Calculation input statuses:", ""])
        for status, count in payload["raw_value_variant_calculation_input_status_counts"].items():
            lines.append(f"- `{status}`: {count}")
    else:
        lines.append("- No raw-value-level variant coverage recorded.")
    lines.extend(
        [
            "",
            "## Mechanics Anchors",
            "",
        ]
    )
    for anchor, present in sorted(payload["system_mechanics_anchors_checked"].items()):
        lines.append(f"- `{anchor}`: `{str(present).lower()}`")
    lines.extend(
        [
            "",
            "## Coverage Records",
            "",
            "| Review item | Source | Family | Field | Disposition | Decision | Calculation status | Parser rules | Variant coverage | Note |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in payload["coverage_records"]:
        variants = record.get("raw_value_variant_coverage", [])
        variant_summary = ""
        if variants:
            variant_counts = Counter(variant["classifier_decision"] for variant in variants)
            variant_summary = ", ".join(f"{decision}: {count}" for decision, count in sorted(variant_counts.items()))
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_code(record["review_item_id"]),
                    _markdown_code(record["source_name"]),
                    _markdown_code(record["semantic_source_family"]),
                    _markdown_code(record["proposed_field_key"] or ""),
                    _markdown_code(record["source_disposition"]),
                    _markdown_code(record["classifier_decision"]),
                    _markdown_code(record["calculation_input_status"]),
                    _markdown_code(", ".join(record["parser_rule_ids"])),
                    _markdown_code(variant_summary),
                    record["policy_note"].replace("|", "\\|"),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _coverage_record(record: dict[str, Any]) -> dict[str, Any]:
    disposition = str(record.get("disposition"))
    family = str(record.get("semantic_source_family"))
    field_key = str(record.get("proposed_field_key") or "")
    decision = DISPOSITION_TO_DECISION.get(disposition)
    parser_rule_ids: list[str] = []
    value_shape_status = "review_required"
    calculation_status = "review_required_not_calculation_safe"
    note = "Unsupported or calculation-relevant values remain review-required."
    raw_value_variant_coverage: list[dict[str, Any]] = []

    if disposition == "parse_rule_required_before_schema":
        unsupported_reason = _unsupported_field_reason(record)
        if unsupported_reason:
            decision = "review_required"
            note = unsupported_reason
        else:
            parser_rule_ids = _supported_parse_rule_ids(record)
            parsed_examples = _parsed_representative_examples(record)
            raw_value_variant_coverage = _raw_value_variant_coverage(record)
            blocked_variant_count = sum(
                1
                for variant in raw_value_variant_coverage
                if variant.get("classifier_decision") == "review_required"
            )
            if parser_rule_ids and parsed_examples:
                if blocked_variant_count:
                    decision = PARTIAL_RAW_VALUE_COVERAGE_DECISION
                    value_shape_status = "partial"
                else:
                    decision = "parsed_numeric_structured"
                    value_shape_status = "parsed"
                calculation_status = _parsed_calculation_status(record, parser_rule_id=parser_rule_ids[0])
                if calculation_status == PARSED_RANGE_NOT_SINGLE_VALUE_CALCULATION_SAFE:
                    note = "Official signed range parses to frame_range endpoints, but range reason is unknown and it is not single-value calculation-safe."
                elif calculation_status == ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE:
                    if blocked_variant_count:
                        note = "Official annotated numeric candidates parse only for approved raw variants; blocked variants remain review-required and no candidate is scalar calculation-safe."
                    else:
                        note = "Official annotated numeric candidates parse into a non-scalar wrapper; note-bound candidates are not calculation-safe."
                else:
                    note = "Reviewed representative examples parse under strict rules; complex variants still remain review-required at raw-value classification time."
            else:
                decision = "review_required"
                parser_rule_ids = []
                note = "Reviewed representative examples do not parse under strict rules; this disposition group remains review-required."
    elif disposition == "source_specific_enum_required":
        parser_rule_ids = ["enum_token.source_native_examples.v1"]
        value_shape_status = "parsed"
        calculation_status = "enum_only_not_arithmetic"
        note = "Representative source-native enum tokens are preserved; unknown tokens are review-required."
    elif disposition == "schema_supports_raw_only":
        value_shape_status = "raw_preserved"
        calculation_status = "raw_preserved_not_calculation"
        note = "Reviewed raw-only field is preserved for display/context and excluded from calculation."
    elif disposition == "out_of_scope_first_normalized_export":
        value_shape_status = "rejected"
        calculation_status = "out_of_scope_not_emitted"
        note = "Reviewed policy defers this field from the first normalized export."
    if record.get("source_name") == "supercombo" and calculation_status == "eligible_only_after_domain_source_and_unit_checks":
        calculation_status = "not_numeric_authority"

    coverage_record = {
        "review_item_id": record.get("review_item_id"),
        "source_name": record.get("source_name"),
        "source_role": record.get("source_role"),
        "semantic_source_family": family,
        "proposed_field_key": field_key or None,
        "source_header_path": record.get("source_header_path", []),
        "source_disposition": disposition,
        "shape_classes": record.get("shape_classes", []),
        "classifier_decision": decision,
        "value_shape_classifier_status": value_shape_status,
        "parser_rule_ids": parser_rule_ids,
        "calculation_input_status": calculation_status,
        "raw_value_policy": "preserve_raw_value_always",
        "supercombo_authority_policy": _supercombo_authority_policy(record),
        "policy_note": note,
    }
    if raw_value_variant_coverage:
        coverage_record["raw_value_variant_coverage"] = raw_value_variant_coverage
    return coverage_record


def _coverage_record_errors(
    index: int,
    record: dict[str, Any],
    *,
    disposition_record: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    context = f"coverage_records[{index}]"
    required = {
        "review_item_id",
        "source_name",
        "source_role",
        "semantic_source_family",
        "proposed_field_key",
        "source_header_path",
        "source_disposition",
        "shape_classes",
        "classifier_decision",
        "value_shape_classifier_status",
        "parser_rule_ids",
        "calculation_input_status",
        "raw_value_policy",
        "supercombo_authority_policy",
        "policy_note",
    }
    for key in sorted(required):
        if key not in record:
            errors.append(f"{context}.{key} is required")
    if disposition_record is None:
        errors.append(f"{context}.review_item_id is not in disposition artifact")
        return errors
    for key in ("source_name", "source_role", "semantic_source_family", "source_disposition"):
        source_key = "disposition" if key == "source_disposition" else key
        if record.get(key) != disposition_record.get(source_key):
            errors.append(f"{context}.{key} must match disposition artifact")
    disposition = str(record.get("source_disposition"))
    decision = record.get("classifier_decision")
    if disposition == "parse_rule_required_before_schema" and decision not in {
        "parsed_numeric_structured",
        PARTIAL_RAW_VALUE_COVERAGE_DECISION,
        "review_required",
    }:
        errors.append(f"{context}.classifier_decision invalid for parse-rule disposition")
    if disposition == "source_specific_enum_required" and decision != "enum_classified":
        errors.append(f"{context}.classifier_decision must be enum_classified")
    if disposition == "schema_supports_raw_only" and decision != "raw_preserved_non_calculation":
        errors.append(f"{context}.classifier_decision must be raw_preserved_non_calculation")
    if disposition == "out_of_scope_first_normalized_export" and decision != "out_of_scope_first_normalized_export":
        errors.append(f"{context}.classifier_decision must be out_of_scope_first_normalized_export")
    if record.get("source_name") == "supercombo":
        if record.get("source_role") not in {"cross_reference_candidate", "enrichment_candidate"}:
            errors.append(f"{context}.source_role must keep SuperCombo enrichment/cross-reference only")
        if record.get("supercombo_authority_policy") != "not_numeric_authority":
            errors.append(f"{context}.supercombo_authority_policy must forbid numeric authority")
    if record.get("raw_value_policy") != "preserve_raw_value_always":
        errors.append(f"{context}.raw_value_policy must preserve raw values")
    if not record.get("policy_note"):
        errors.append(f"{context}.policy_note is required")
    errors.extend(_raw_value_variant_coverage_errors(context, record))
    return errors


def _raw_value_variant_coverage_errors(context: str, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    variants = record.get("raw_value_variant_coverage", [])
    if variants == []:
        if record.get("classifier_decision") == PARTIAL_RAW_VALUE_COVERAGE_DECISION:
            errors.append(f"{context}.raw_value_variant_coverage is required for partial coverage")
        return errors
    if not isinstance(variants, list):
        return [f"{context}.raw_value_variant_coverage must be a list"]
    parsed_count = 0
    blocked_count = 0
    for variant_index, variant in enumerate(variants):
        variant_context = f"{context}.raw_value_variant_coverage[{variant_index}]"
        if not isinstance(variant, dict):
            errors.append(f"{variant_context} must be an object")
            continue
        required = {
            "raw_value",
            "raw_value_length",
            "raw_value_sha256",
            "classifier_decision",
            "value_shape_classifier_status",
            "parser_rule_ids",
            "calculation_input_status",
        }
        for key in sorted(required):
            if key not in variant:
                errors.append(f"{variant_context}.{key} is required")
        decision = variant.get("classifier_decision")
        if decision == "parsed_numeric_structured":
            parsed_count += 1
            if variant.get("parsed_value_kind") != "annotated_numeric_candidate":
                errors.append(f"{variant_context}.parsed_value_kind must be annotated_numeric_candidate")
            if variant.get("calculation_input_status") != ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE:
                errors.append(f"{variant_context}.calculation_input_status must not be scalar calculation-safe")
            if not variant.get("parser_rule_ids"):
                errors.append(f"{variant_context}.parser_rule_ids must identify the annotated parser")
        elif decision == "review_required":
            blocked_count += 1
            if variant.get("parser_rule_ids") != []:
                errors.append(f"{variant_context}.parser_rule_ids must be empty for blocked variants")
            if not variant.get("review_required_reason"):
                errors.append(f"{variant_context}.review_required_reason is required for blocked variants")
        else:
            errors.append(f"{variant_context}.classifier_decision is invalid")
        raw_value = variant.get("raw_value")
        if isinstance(raw_value, str):
            expected_length = len(raw_value)
            expected_hash = "sha256:" + hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
            if variant.get("raw_value_length") != expected_length:
                errors.append(f"{variant_context}.raw_value_length does not match raw_value")
            if variant.get("raw_value_sha256") != expected_hash:
                errors.append(f"{variant_context}.raw_value_sha256 does not match raw_value")
    if record.get("classifier_decision") == PARTIAL_RAW_VALUE_COVERAGE_DECISION:
        if parsed_count == 0 or blocked_count == 0:
            errors.append(f"{context}.raw_value_variant_coverage must include parsed and blocked variants")
    elif blocked_count:
        errors.append(f"{context}.classifier_decision must be partial when variants remain blocked")
    return errors


def _classify_enum(raw: str, disposition_record: dict[str, Any]) -> ClassificationResult:
    review_item_id = str(disposition_record.get("review_item_id"))
    approved_examples = {
        str(example["raw_value"])
        for example in disposition_record.get("representative_examples", [])
        if isinstance(example, dict) and isinstance(example.get("raw_value"), str)
    }
    if raw in approved_examples:
        return ClassificationResult(
            raw_value=raw,
            classifier_decision="enum_classified",
            value_shape={
                "classes": _infer_shape_classes(raw),
                "classifier_status": "parsed",
                "parser_rule_id": "enum_token.source_native_examples.v1",
                "review_item_id": review_item_id,
            },
            parsed_value={"kind": "enum_token", "tokens": [raw]},
            calculation_input_status="enum_only_not_arithmetic",
            policy_note="Source-native enum token is preserved exactly from reviewed representative examples.",
        )
    return _review_required(raw, review_item_id, "Enum token is not in reviewed representative examples; do not guess source-native enum semantics.")


def _parsed_representative_examples(record: dict[str, Any]) -> list[str]:
    parsed: list[str] = []
    for example in record.get("representative_examples", []):
        if not isinstance(example, dict) or not isinstance(example.get("raw_value"), str):
            continue
        result = classify_raw_value(example["raw_value"], record)
        if result.classifier_decision == "parsed_numeric_structured":
            parsed.append(example["raw_value"])
    return parsed


def _raw_value_variant_coverage(record: dict[str, Any]) -> list[dict[str, Any]]:
    if not _is_annotated_official_target_record(record):
        return []
    variants: list[dict[str, Any]] = []
    for example in record.get("representative_examples", []):
        if not isinstance(example, dict) or not isinstance(example.get("raw_value"), str):
            continue
        raw = example["raw_value"]
        result = classify_raw_value(raw, record)
        variant = {
            "raw_value": raw,
            "raw_value_length": example.get("raw_value_length", len(raw)),
            "raw_value_sha256": example.get(
                "raw_value_sha256",
                "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            ),
            "classifier_decision": result.classifier_decision,
            "value_shape_classifier_status": result.value_shape["classifier_status"],
            "parser_rule_ids": [result.value_shape["parser_rule_id"]]
            if result.value_shape.get("parser_rule_id")
            else [],
            "calculation_input_status": result.calculation_input_status,
        }
        if result.parsed_value is not None:
            variant["parsed_value_kind"] = result.parsed_value["kind"]
        if result.review_required_reason:
            variant["review_required_reason"] = result.review_required_reason
        variants.append(variant)
    return variants


def _supported_parse_rule_ids(record: dict[str, Any]) -> list[str]:
    if _is_official_signed_wave_dash_range_record(record):
        return [OFFICIAL_SIGNED_WAVE_DASH_RANGE_RULE_ID]
    metadata = _annotated_official_metadata_for_record(record)
    if metadata:
        return [metadata["parser_rule_id"]]
    family = str(record.get("semantic_source_family"))
    return SUPPORTED_PARSE_RULES_BY_FAMILY.get(family, [])


def _parsed_calculation_status(disposition_record: dict[str, Any], *, parser_rule_id: str) -> str:
    if parser_rule_id == OFFICIAL_SIGNED_WAVE_DASH_RANGE_RULE_ID:
        return PARSED_RANGE_NOT_SINGLE_VALUE_CALCULATION_SAFE
    if parser_rule_id in ANNOTATED_OFFICIAL_RULE_IDS:
        return ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE
    if disposition_record.get("source_name") == "supercombo":
        return "not_numeric_authority"
    return "eligible_only_after_domain_source_and_unit_checks"


def _parse_annotated_official_value(
    raw: str,
    *,
    review_item_id: str,
    source_name: str,
    source_role: str,
    family: str,
    field_key: str,
) -> tuple[dict[str, Any], str] | None:
    metadata = ANNOTATED_OFFICIAL_REVIEW_METADATA.get(review_item_id)
    if not metadata:
        return None
    if source_name != "official" or source_role != "authority_candidate" or field_key != metadata["field_key"]:
        return None
    if raw not in metadata["approved_raw_values"]:
        return None
    if metadata["candidate_type"] == "unsigned_frame":
        if family != "timing":
            return None
        match = re.fullmatch(r"(\d+)※", raw)
        if not match:
            return None
        value = int(match.group(1))
    else:
        if family != "advantage":
            return None
        match = re.fullmatch(r"※(-\d+)", raw)
        if not match:
            return None
        value = int(match.group(1))

    return (
        {
            "kind": "annotated_numeric_candidate",
            "numeric_candidate": {
                "candidate_type": metadata["candidate_type"],
                "unit": "frame",
                "value": value,
            },
            "annotation": {
                "note_marker": "※",
                "marker_placement": metadata["marker_placement"],
                "note_id": None,
                "note_text_status": "structured_row_note_text_found",
                "note_scope": metadata["note_scope"],
                "row_note_candidate_count": 1,
                "note_linkage_status": "same_row_note_candidates_available",
            },
            "source_context": {
                "source_review_id": metadata["source_review_id"],
                "review_item_id": review_item_id,
                "source_column_header_path": metadata["source_column_header_path"],
            },
            "calculation": {
                "calculation_input_status": ANNOTATED_CANDIDATE_NOT_CALCULATION_SAFE,
                "reason": "condition_bound_by_official_note",
            },
        },
        metadata["parser_rule_id"],
    )


def _parse_supported_value(
    raw: str,
    *,
    family: str,
    field_key: str,
    review_item_id: str,
    source_name: str,
) -> tuple[dict[str, Any], str] | None:
    if family == "advantage" and INTEGER_RE.fullmatch(raw):
        return {"kind": "signed_frame", "unit": "frame", "value": int(raw)}, "signed_frame.strict.v1"
    if _is_official_signed_wave_dash_range_target(
        review_item_id=review_item_id,
        source_name=source_name,
        family=family,
        field_key=field_key,
    ):
        match = OFFICIAL_SIGNED_WAVE_DASH_RANGE_RE.fullmatch(raw)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            if start <= end:
                return (
                    {"kind": "frame_range", "unit": "frame", "start": start, "end": end},
                    OFFICIAL_SIGNED_WAVE_DASH_RANGE_RULE_ID,
                )
    if family == "timing":
        match = FRAME_RANGE_RE.fullmatch(raw)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            if start <= end:
                return {"kind": "frame_range", "unit": "frame", "start": start, "end": end}, "frame_range.strict.v1"
        if UNSIGNED_INTEGER_RE.fullmatch(raw):
            return {"kind": "integer", "unit": "frame", "value": int(raw)}, "frame_scalar.strict.v1"
    if family == "damage" and UNSIGNED_INTEGER_RE.fullmatch(raw):
        return {"kind": "integer", "unit": "damage", "value": int(raw)}, "integer_damage.strict.v1"
    if family == "gauge" and DECIMAL_RE.fullmatch(raw):
        unit = _gauge_amount_unit(field_key)
        value = float(raw) if "." in raw else int(raw)
        return {"kind": "gauge_amount", "unit": unit, "value": value}, "gauge_amount.strict.v1"
    if family == "throw":
        match = THROW_PAIR_RE.fullmatch(raw)
        if match:
            return (
                {
                    "kind": "ordered_pair",
                    "unit": "source_native_distance",
                    "labels": ["throw_range", "hurtbox"],
                    "values": [float(match.group(1)), float(match.group(2))],
                },
                "throw_range_hurtbox_pair.strict.v1",
            )
    if family in {"metadata", "mobility", "projectile"} and DECIMAL_RE.fullmatch(raw):
        unit = _decimal_metric_unit(field_key)
        value = float(raw) if "." in raw else int(raw)
        return {"kind": "decimal", "unit": unit, "value": value}, "decimal_metric.strict.v1"
    return None


def _is_official_signed_wave_dash_range_record(record: dict[str, Any]) -> bool:
    return (
        record.get("review_item_id") in OFFICIAL_SIGNED_WAVE_DASH_RANGE_REVIEW_ITEM_IDS
        and record.get("source_name") == "official"
        and record.get("semantic_source_family") == "advantage"
        and record.get("proposed_field_key") in {"block_advantage", "hit_advantage"}
    )


def _is_official_signed_wave_dash_range_target(
    *,
    review_item_id: str,
    source_name: str,
    family: str,
    field_key: str,
) -> bool:
    return (
        review_item_id in OFFICIAL_SIGNED_WAVE_DASH_RANGE_REVIEW_ITEM_IDS
        and source_name == "official"
        and family == "advantage"
        and field_key in {"block_advantage", "hit_advantage"}
    )


def _annotated_official_metadata_for_record(record: dict[str, Any]) -> dict[str, Any] | None:
    metadata = ANNOTATED_OFFICIAL_REVIEW_METADATA.get(str(record.get("review_item_id")))
    if not metadata:
        return None
    if (
        record.get("source_name") == "official"
        and record.get("source_role") == "authority_candidate"
        and record.get("proposed_field_key") == metadata["field_key"]
    ):
        return metadata
    return None


def _is_annotated_official_target_record(record: dict[str, Any]) -> bool:
    return _annotated_official_metadata_for_record(record) is not None


def _unsupported_field_reason(record: dict[str, Any]) -> str | None:
    family = str(record.get("semantic_source_family"))
    field_key = str(record.get("proposed_field_key") or "")
    source_name = str(record.get("source_name"))
    if family == "scaling":
        return REVIEW_REQUIRED_FIELDS["combo_scaling"]
    if field_key in REVIEW_REQUIRED_FIELDS:
        return REVIEW_REQUIRED_FIELDS[field_key]
    if source_name == "supercombo" and field_key == "active":
        return "SuperCombo active values include X(n)Y active-window sequences; current schema lacks a structured active-window object."
    return None


def _complex_expression_reason(raw: str) -> str | None:
    if "※" in raw:
        return "Source note marker may change semantics; a reviewed note parser is required."
    if "%" in raw or "％" in raw:
        return "Scaling and percent expressions need reviewed scaling_type, trigger, target, and stacking semantics."
    if "[" in raw or "]" in raw:
        return "Bracketed alternates or tags need reviewed condition labels before calculation."
    if "(" in raw or ")" in raw:
        return "Parenthesized values are context-dependent per system mechanics summary."
    if re.search(r"\b(?:KD|HKD|Wall Splat|Crumple|PC|CH)\b", raw):
        return "Stateful advantage tokens need explicit state/modifier context before calculation."
    if re.search(r"\b(?:total|land|each|recoverable|Projectile|Air|Throw|Strike|release)\b", raw, re.IGNORECASE):
        return "Source-native condition text needs a reviewed structured modifier before calculation."
    if "x" in raw or "*" in raw:
        return "Multihit expressions need structured per-hit values before calculation."
    if "/" in raw:
        return "Slash-separated values need reviewed component labels before calculation."
    if "+" in raw and not raw.startswith("+"):
        return "Plus sequences need component labels and must not be collapsed as arithmetic."
    if re.search(r"[A-Za-zぁ-んァ-ン一-龯]", raw):
        return "Text-bearing calculation value needs reviewed enum/modifier semantics."
    if re.search(r"\d+\s*[-~]\s*$", raw):
        return "Open-ended ranges need reviewed semantics before calculation."
    return None


def _non_parsed_result(
    raw: str,
    decision: str,
    classifier_status: str,
    review_item_id: str,
    calculation_status: str,
    note: str,
) -> ClassificationResult:
    return ClassificationResult(
        raw_value=raw,
        classifier_decision=decision,
        value_shape={
            "classes": _infer_shape_classes(raw),
            "classifier_status": classifier_status,
            "review_item_id": review_item_id,
        },
        parsed_value=None,
        calculation_input_status=calculation_status,
        policy_note=note,
    )


def _review_required(raw: str, review_item_id: str, reason: str) -> ClassificationResult:
    return ClassificationResult(
        raw_value=raw,
        classifier_decision="review_required",
        value_shape={
            "classes": _infer_shape_classes(raw),
            "classifier_status": "review_required",
            "review_item_id": review_item_id,
        },
        parsed_value=None,
        calculation_input_status="review_required_not_calculation_safe",
        policy_note="Raw value is preserved and blocked from calculation until a later reviewed parser policy covers it.",
        review_required_reason=reason,
    )


def _infer_shape_classes(raw: str) -> list[str]:
    stripped = raw.strip()
    classes: set[str] = set()
    if not stripped:
        return ["blank"]
    if stripped.startswith("※"):
        classes.add("note_prefixed")
    elif "※" in stripped:
        classes.add("note_suffixed")
    if "%" in stripped or "％" in stripped:
        classes.add("percent_expression")
    if "+" in stripped and not stripped.startswith("+"):
        classes.add("plus_expression")
    if "/" in stripped:
        classes.add("multihit")
    if "x" in stripped or "*" in stripped:
        classes.add("multihit")
    if "(" in stripped or ")" in stripped or "[" in stripped or "]" in stripped:
        classes.add("hidden_detail")
    if FRAME_RANGE_RE.fullmatch(stripped) or "～" in stripped or "~" in stripped:
        classes.add("range")
    if re.search(r"[A-Za-zぁ-んァ-ン一-龯]", stripped):
        classes.add("categorical")
    if INTEGER_RE.fullmatch(stripped):
        classes.add("signed_frame" if stripped.startswith(("+", "-")) else "scalar")
    elif DECIMAL_RE.fullmatch(stripped):
        classes.add("scalar")
    if not classes:
        classes.add("unclassified")
    return sorted(classes)


def _decimal_metric_unit(field_key: str) -> str:
    if "speed" in field_key or field_key.endswith("_walk_speed"):
        return "source_native_speed"
    if "range" in field_key or "distance" in field_key or "apex" in field_key:
        return "source_native_distance"
    return "source_native_metric"


def _gauge_amount_unit(field_key: str) -> str:
    if field_key == "sa_gain" or field_key.startswith("super_gain") or "_super_gain" in field_key:
        return "super_art"
    return "drive"


def _mechanics_anchor_presence(text: str) -> dict[str, bool]:
    return {name: phrase in text for name, phrase in SYSTEM_MECHANICS_ANCHORS.items()}


def _supercombo_authority_policy(record: dict[str, Any]) -> str:
    if record.get("source_name") == "supercombo":
        return "not_numeric_authority"
    return "not_applicable"


def _contains_forbidden_authority_claim(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_authority_claim(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_authority_claim(item) for item in value)
    if isinstance(value, str):
        return "current_fact_authority" in value
    return False


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def _markdown_code(value: str) -> str:
    return "`" + str(value).replace("`", "\\`") + "`"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or validate parsed-value classifier coverage artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build")
    subparsers.add_parser("validate")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            payload = build_coverage_payload()
            write_coverage_artifacts(payload)
            print(f"Parsed-value classifier coverage written: {payload['total_review_items']} records")
            return 0
        errors = validate_coverage_artifacts()
        if errors:
            raise ValueError("\n".join(errors))
        print("Parsed-value classifier coverage validation OK")
        return 0
    except Exception as exc:  # pragma: no cover - CLI error message matters
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
