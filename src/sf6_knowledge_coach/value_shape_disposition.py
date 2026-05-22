from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Any

from .paths import repo_root
from .supercombo_field_mapping import validate_mapping_artifacts
from .value_shape_inventory import MAX_PUBLIC_RAW_VALUE_CHARS, validate_inventory_artifacts


RUN_ID = "20260521T025403Z"
INPUT_INVENTORY_JSON = Path("data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json")
INPUT_MAPPING_JSON = Path("data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json")
OUTPUT_JSON = Path("data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json")
OUTPUT_MD = Path("docs/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition.md")
ARTIFACT_SCHEMA_VERSION = "value_shape_review_item_disposition_summary/v1"
EXPECTED_REVIEW_ITEM_COUNT = 247

DISPOSITIONS = [
    "parse_rule_required_before_schema",
    "schema_supports_raw_only",
    "source_specific_enum_required",
    "out_of_scope_first_normalized_export",
    "blocked_pending_source_review",
]

OFFICIAL_FIELD_MAPPINGS: dict[tuple[str, ...], tuple[str, str, str]] = {
    ("技名",): ("move_name", "identity", "技名"),
    ("動作フレーム", "発生"): ("startup", "timing", "発生"),
    ("動作フレーム", "持続"): ("active", "timing", "持続"),
    ("動作フレーム", "硬直"): ("recovery", "timing", "硬直"),
    ("硬直差", "ヒット"): ("hit_advantage", "advantage", "ヒット硬直差"),
    ("硬直差", "ガード"): ("block_advantage", "advantage", "ガード硬直差"),
    ("キャンセル",): ("cancel", "cancel", "キャンセル"),
    ("ダメージ",): ("damage", "damage", "ダメージ"),
    ("コンボ補正値",): ("combo_scaling", "scaling", "コンボ補正値"),
    ("Dゲージ増加", "ヒット"): ("drive_gain_on_hit", "gauge", "Dゲージ増加 ヒット"),
    ("Dゲージ減少", "ガード"): ("drive_loss_on_block", "gauge", "Dゲージ減少 ガード"),
    ("Dゲージ減少", "パニッシュカウンター"): ("drive_loss_on_punish_counter", "gauge", "Dゲージ減少 パニッシュカウンター"),
    ("SAゲージ増加",): ("sa_gain", "gauge", "SAゲージ増加"),
    ("属性",): ("attribute", "attribute", "属性"),
    ("備考",): ("remarks", "note", "備考"),
}

PARSE_RULE_FAMILIES = {
    "advantage",
    "damage",
    "gauge",
    "metadata",
    "mobility",
    "projectile",
    "scaling",
    "timing",
    "vital",
}
ENUM_FAMILIES = {"attribute", "cancel", "defense", "guard"}

FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\\\\Users\\\\"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)\b(?:answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault|browser profile)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump)\b"),
]


def default_inventory_path() -> Path:
    return repo_root() / INPUT_INVENTORY_JSON


def default_mapping_path() -> Path:
    return repo_root() / INPUT_MAPPING_JSON


def default_output_json_path() -> Path:
    return repo_root() / OUTPUT_JSON


def default_output_md_path() -> Path:
    return repo_root() / OUTPUT_MD


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    validate_inventory_artifacts()
    inventory_path = path or default_inventory_path()
    return json.loads(inventory_path.read_text(encoding="utf-8"))


def load_supercombo_mapping(path: Path | None = None) -> dict[str, Any]:
    validate_mapping_artifacts()
    mapping_path = path or default_mapping_path()
    return json.loads(mapping_path.read_text(encoding="utf-8"))


def build_disposition_summary(
    *,
    inventory_path: Path | None = None,
    mapping_path: Path | None = None,
) -> dict[str, Any]:
    inventory = load_inventory(inventory_path)
    mapping = load_supercombo_mapping(mapping_path)
    if inventory.get("run_id") != RUN_ID:
        raise ValueError(f"input inventory run_id must be {RUN_ID}")
    if mapping.get("run_id") != RUN_ID:
        raise ValueError(f"SuperCombo mapping run_id must be {RUN_ID}")

    shape_classes_by_key = _shape_classes_by_key(inventory)
    mapping_by_path = {
        tuple(record.get("source_header_path", [])): record
        for record in mapping.get("mappings", [])
    }
    review_items = inventory.get("review_items", [])
    dispositions = [
        _disposition_record(item, shape_classes_by_key=shape_classes_by_key, mapping_by_path=mapping_by_path)
        for item in review_items
    ]
    dispositions.sort(key=lambda item: (item["inventory_source_family"], item["source_header_path"], item["review_kind"]))
    summary = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_id": RUN_ID,
        "input_inventory": INPUT_INVENTORY_JSON.as_posix(),
        "input_supercombo_mapping": INPUT_MAPPING_JSON.as_posix(),
        "artifact_boundary": "review_item_disposition_summary_only",
        "authority_status": "disposition_only_not_authority",
        "total_review_items": len(dispositions),
        "disposition_counts": _count_by(dispositions, "disposition", DISPOSITIONS),
        "inventory_source_family_counts": _count_by(dispositions, "inventory_source_family", ["official", "supercombo"]),
        "review_kind_counts": _count_by(
            dispositions,
            "review_kind",
            ["malformed_looking_source_value", "source_specific_expression", "unclassified_expression"],
        ),
        "source_role_counts": _count_by(
            dispositions,
            "source_role",
            ["authority_candidate", "cross_reference_candidate", "enrichment_candidate"],
        ),
        "supercombo_mapping_dependency_count": sum(1 for item in dispositions if item["supercombo_mapping_dependency"]),
        "json_schema_redesign_blocked_count": sum(1 for item in dispositions if item["json_schema_redesign_blocked"]),
        "dispositions": dispositions,
        "source_boundary": {
            "raw_html_public_commit": "forbidden",
            "full_raw_rows_public_commit": "forbidden",
            "full_source_table_public_commit": "forbidden",
            "parsed_values": "not_emitted",
        },
        "json_schema_redesign_gate": {
            "status": "blocked",
            "blocked_until": [
                "all parse_rule_required_before_schema records get parser/classifier policy",
                "all source_specific_enum_required records get enum design",
                "all blocked_pending_source_review records are resolved or scoped out",
                "reviewer approves combined mapping and disposition surfaces",
            ],
        },
    }
    errors = validate_disposition_payload(summary, inventory=inventory, mapping=mapping)
    if errors:
        raise ValueError("\n".join(errors))
    return summary


def write_disposition_artifacts(
    disposition: dict[str, Any],
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> None:
    output_json = json_path or default_output_json_path()
    output_md = markdown_path or default_output_md_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(disposition, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_disposition_markdown(disposition), encoding="utf-8")


def validate_disposition_artifacts(
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
    inventory_path: Path | None = None,
    mapping_path: Path | None = None,
) -> list[str]:
    output_json = json_path or default_output_json_path()
    output_md = markdown_path or default_output_md_path()
    errors: list[str] = []
    if not output_json.exists():
        errors.append(f"Missing value-shape disposition JSON summary: {output_json.relative_to(repo_root())}")
    if not output_md.exists():
        errors.append(f"Missing value-shape disposition Markdown summary: {output_md.relative_to(repo_root())}")
    if errors:
        return errors
    try:
        payload = json.loads(output_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid value-shape disposition JSON summary: {exc}"]
    inventory = load_inventory(inventory_path)
    mapping = load_supercombo_mapping(mapping_path)
    errors.extend(validate_disposition_payload(payload, inventory=inventory, mapping=mapping))
    for path in (output_json, output_md):
        errors.extend(_forbidden_public_text_errors(path.read_text(encoding="utf-8"), path))
    if errors:
        raise ValueError("\n".join(errors))
    return []


def validate_disposition_payload(
    payload: dict[str, Any],
    *,
    inventory: dict[str, Any],
    mapping: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if payload.get("artifact_schema_version") != ARTIFACT_SCHEMA_VERSION:
        errors.append(f"artifact_schema_version must be {ARTIFACT_SCHEMA_VERSION}")
    if payload.get("run_id") != RUN_ID:
        errors.append(f"run_id must be {RUN_ID}")
    if payload.get("artifact_boundary") != "review_item_disposition_summary_only":
        errors.append("artifact_boundary must be review_item_disposition_summary_only")
    if payload.get("authority_status") != "disposition_only_not_authority":
        errors.append("authority_status must be disposition_only_not_authority")
    if _contains_forbidden_authority_claim(payload):
        errors.append("disposition artifact must not claim current_fact_authority")

    dispositions = payload.get("dispositions", [])
    if not isinstance(dispositions, list):
        errors.append("dispositions must be a list")
        dispositions = []
    if len(dispositions) != EXPECTED_REVIEW_ITEM_COUNT:
        errors.append(f"dispositions must contain exactly {EXPECTED_REVIEW_ITEM_COUNT} records")

    input_review_ids = {_review_item_id(item) for item in inventory.get("review_items", [])}
    output_review_ids = [record.get("review_item_id") for record in dispositions if isinstance(record, dict)]
    duplicate_ids = sorted(item_id for item_id, count in Counter(output_review_ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"duplicate review_item_id records: {duplicate_ids[:3]}")
    if set(output_review_ids) != input_review_ids:
        missing = sorted(input_review_ids - set(output_review_ids))
        extra = sorted(set(output_review_ids) - input_review_ids)
        if missing:
            errors.append(f"missing review item dispositions: {missing[:3]}")
        if extra:
            errors.append(f"unexpected review item dispositions: {extra[:3]}")

    mapping_by_id = {
        record.get("mapping_id"): record
        for record in mapping.get("mappings", [])
    }
    for index, record in enumerate(dispositions):
        if not isinstance(record, dict):
            errors.append(f"dispositions[{index}] must be an object")
            continue
        errors.extend(_disposition_record_errors(index, record, mapping_by_id=mapping_by_id))
    errors.extend(_summary_count_errors(payload, dispositions))
    return errors


def render_disposition_markdown(disposition: dict[str, Any]) -> str:
    lines = [
        "# Value-Shape Review Item Disposition",
        "",
        "This artifact is a review-item disposition summary only. It does not",
        "emit parsed values, does not implement JSON Schema/parser behavior,",
        "and does not promote official or SuperCombo data to daily-answer",
        "numeric authority.",
        "",
        f"- Run ID: `{disposition['run_id']}`",
        f"- Input inventory: `{disposition['input_inventory']}`",
        f"- Input SuperCombo mapping: `{disposition['input_supercombo_mapping']}`",
        f"- Total review items: `{disposition['total_review_items']}`",
        f"- JSON Schema redesign blocked records: `{disposition['json_schema_redesign_blocked_count']}`",
        f"- SuperCombo mapping dependencies: `{disposition['supercombo_mapping_dependency_count']}`",
        "",
        "## Disposition Counts",
        "",
    ]
    for status, count in disposition["disposition_counts"].items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Source Counts", ""])
    for family, count in disposition["inventory_source_family_counts"].items():
        lines.append(f"- `{family}`: {count}")
    lines.extend(
        [
            "",
            "## Dispositions",
            "",
            "| Review item | Source | Header path | Kind | Disposition | Proposed key | Role | Affected | Rationale |",
            "| --- | --- | --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for record in disposition["dispositions"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_code(record["review_item_id"]),
                    _markdown_code(record["inventory_source_family"]),
                    _markdown_code(" > ".join(record["source_header_path"])),
                    _markdown_code(record["review_kind"]),
                    _markdown_code(record["disposition"]),
                    _markdown_code(record["proposed_field_key"] or ""),
                    _markdown_code(record["source_role"]),
                    str(record["affected_count"]),
                    record["rationale"].replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary Notes",
            "",
            "- `inventory_source_family` is the inventory source identity.",
            "- No disposition record uses normalized-layer `source_family` for source identity.",
            "- Official remains authority candidate only.",
            "- SuperCombo remains enrichment/cross-reference/candidate only.",
            "- JSON Schema redesign remains blocked until parser, enum, blocked-review, and combined-surface gates are resolved.",
        ]
    )
    return "\n".join(lines) + "\n"


def _disposition_record(
    item: dict[str, Any],
    *,
    shape_classes_by_key: dict[tuple[str, tuple[str, ...]], list[str]],
    mapping_by_path: dict[tuple[str, ...], dict[str, Any]],
) -> dict[str, Any]:
    inventory_source_family = str(item.get("source_family"))
    source_header_path = [str(part) for part in item.get("source_header_path", [])]
    source_key = (inventory_source_family, tuple(source_header_path))
    shape_classes = shape_classes_by_key.get(source_key, [])
    if inventory_source_family == "official":
        policy = _official_disposition_policy(item, shape_classes)
        source_name = "official"
        source_role = "authority_candidate"
        supercombo_mapping_dependency = None
        semantic_family = policy["semantic_family"]
    elif inventory_source_family == "supercombo":
        mapping = mapping_by_path.get(tuple(source_header_path))
        if not mapping:
            raise ValueError(f"missing SuperCombo mapping for {source_header_path}")
        policy = _supercombo_disposition_policy(item, mapping)
        source_name = "supercombo"
        source_role = str(mapping["source_role"])
        supercombo_mapping_dependency = str(mapping["mapping_id"])
        semantic_family = str(mapping["source_family"])
    else:
        raise ValueError(f"unsupported inventory source family: {inventory_source_family}")

    return {
        "review_item_id": _review_item_id(item),
        "run_id": RUN_ID,
        "inventory_source_family": inventory_source_family,
        "source_name": source_name,
        "source_role": source_role,
        "source_header_path": source_header_path,
        "source_label": str(item.get("source_label", "")),
        "proposed_field_key": policy["proposed_field_key"],
        "semantic_source_family": semantic_family,
        "display_label_ja": policy["display_label_ja"],
        "review_kind": str(item.get("kind")),
        "shape_classes": shape_classes,
        "affected_count": int(item.get("affected_count") or 0),
        "representative_examples": [_public_example_payload(example) for example in item.get("examples", [])],
        "disposition": policy["disposition"],
        "rationale": policy["rationale"],
        "json_schema_redesign_blocked": policy["json_schema_redesign_blocked"],
        "supercombo_mapping_dependency": supercombo_mapping_dependency,
        "next_execplan_needed": policy["next_execplan_needed"],
        "reviewer_notes": policy["reviewer_notes"],
    }


def _official_disposition_policy(item: dict[str, Any], shape_classes: list[str]) -> dict[str, Any]:
    source_header_path = tuple(str(part) for part in item.get("source_header_path", []))
    field_key, semantic_family, display_label_ja = OFFICIAL_FIELD_MAPPINGS.get(
        source_header_path,
        (None, "unknown", None),
    )
    kind = str(item.get("kind"))
    if kind == "malformed_looking_source_value":
        return _policy(
            "blocked_pending_source_review",
            field_key,
            semantic_family,
            display_label_ja,
            "Malformed-looking official value must be checked against the source before schema work.",
            True,
            "source review for malformed official values",
            "Source-review blocker; do not infer numeric meaning.",
        )
    if source_header_path == ("備考",):
        return _policy(
            "schema_supports_raw_only",
            field_key,
            semantic_family,
            display_label_ja,
            "Official remarks are source prose and should remain raw-only in the first schema.",
            False,
            "normalized schema raw-only support",
            "Raw-only support is sufficient; no parsed value is approved.",
        )
    if source_header_path == ("技名",):
        return _policy(
            "blocked_pending_source_review",
            field_key,
            semantic_family,
            display_label_ja,
            "Note-bearing official move-name variants require source/domain review before identity schema design.",
            True,
            "source review for note-bearing move names",
            "Move identity must not be normalized from a note-bearing source string by guesswork.",
        )
    if semantic_family in {"cancel", "attribute"}:
        return _policy(
            "source_specific_enum_required",
            field_key,
            semantic_family,
            display_label_ja,
            "Official categorical values need a reviewed source-specific enum before schema/parser work.",
            True,
            "source-specific enum design",
            "Enum design must preserve official notation such as note markers.",
        )
    return _policy(
        "parse_rule_required_before_schema",
        field_key,
        semantic_family,
        display_label_ja,
        "Official current-fact values with special shapes need deterministic parse rules before schema redesign.",
        True,
        "deterministic parsed-value classifier policy",
        f"Observed shapes: {', '.join(shape_classes) or 'unknown'}.",
    )


def _supercombo_disposition_policy(item: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    status = str(mapping.get("mapping_status"))
    semantic_family = str(mapping.get("source_family"))
    proposed_field_key = mapping.get("proposed_field_key")
    display_label_ja = mapping.get("display_label_ja")
    if status == "out_of_scope_first_normalized_export":
        return _policy(
            "out_of_scope_first_normalized_export",
            None,
            semantic_family,
            display_label_ja,
            "The mapped SuperCombo field is explicitly deferred from the first normalized export.",
            False,
            None,
            "Deferral record only; do not hide source drift.",
        )
    if status == "blocked_pending_human_review":
        return _policy(
            "blocked_pending_source_review",
            None,
            semantic_family,
            display_label_ja,
            "The SuperCombo field mapping itself is blocked pending human review.",
            True,
            "SuperCombo field mapping human review",
            "Schema work must not consume this field until mapping is resolved or scoped out.",
        )
    if status == "enrichment_only_no_current_fact_mapping":
        return _policy(
            "schema_supports_raw_only",
            None,
            semantic_family,
            display_label_ja,
            "The SuperCombo field is enrichment context with no current-fact key and should remain raw-only.",
            False,
            "normalized schema raw-only enrichment support",
            "No parsed value or current-fact mapping is approved.",
        )
    if semantic_family in ENUM_FAMILIES:
        return _policy(
            "source_specific_enum_required",
            proposed_field_key,
            semantic_family,
            display_label_ja,
            "The SuperCombo field contains finite source-specific categories requiring enum design.",
            True,
            "source-specific enum design",
            "SuperCombo remains enrichment/cross-reference only.",
        )
    if semantic_family in PARSE_RULE_FAMILIES:
        return _policy(
            "parse_rule_required_before_schema",
            proposed_field_key,
            semantic_family,
            display_label_ja,
            "The SuperCombo field has special value shapes that need deterministic parse/classifier policy before schema use.",
            True,
            "deterministic parsed-value classifier policy",
            "Do not use these values as numeric authority.",
        )
    return _policy(
        "blocked_pending_source_review",
        proposed_field_key,
        semantic_family,
        display_label_ja,
        "No approved disposition policy exists for this SuperCombo semantic family.",
        True,
        "source review for SuperCombo disposition policy",
        "Defaulted to blocked rather than guessing.",
    )


def _policy(
    disposition: str,
    proposed_field_key: str | None,
    semantic_family: str,
    display_label_ja: str | None,
    rationale: str,
    json_schema_redesign_blocked: bool,
    next_execplan_needed: str | None,
    reviewer_notes: str,
) -> dict[str, Any]:
    return {
        "disposition": disposition,
        "proposed_field_key": proposed_field_key,
        "semantic_family": semantic_family,
        "display_label_ja": display_label_ja,
        "rationale": rationale,
        "json_schema_redesign_blocked": json_schema_redesign_blocked,
        "next_execplan_needed": next_execplan_needed,
        "reviewer_notes": reviewer_notes,
    }


def _shape_classes_by_key(inventory: dict[str, Any]) -> dict[tuple[str, tuple[str, ...]], list[str]]:
    classes: dict[tuple[str, tuple[str, ...]], list[str]] = {}
    for summary in inventory.get("field_shape_summaries", []):
        key = (str(summary.get("source_family")), tuple(summary.get("source_header_path", [])))
        shape_counts = summary.get("shape_counts", {})
        classes[key] = sorted(shape for shape, count in shape_counts.items() if int(count or 0) > 0)
    return classes


def _review_item_id(item: dict[str, Any]) -> str:
    parts = [
        str(item.get("source_family", "")),
        str(item.get("kind", "")),
        *[str(part) for part in item.get("source_header_path", [])],
    ]
    return "value-shape:" + "--".join(_slug(part) for part in parts)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if slug:
        return slug
    digest = sha256(value.encode("utf-8")).hexdigest()[:12]
    return f"u_{digest}"


def _public_example_payload(example: dict[str, Any]) -> dict[str, Any]:
    raw_value = example.get("raw_value")
    raw_value_excerpt = str(example.get("raw_value_excerpt", raw_value or ""))
    raw_value_length = int(example.get("raw_value_length") or len(str(raw_value or raw_value_excerpt)))
    payload: dict[str, Any] = {
        "raw_value_excerpt": raw_value_excerpt,
        "raw_value_sha256": str(example.get("raw_value_sha256") or "sha256:" + sha256(str(raw_value or raw_value_excerpt).encode("utf-8")).hexdigest()),
        "raw_value_length": raw_value_length,
        "raw_value_truncated": bool(example.get("raw_value_truncated", raw_value_length > MAX_PUBLIC_RAW_VALUE_CHARS)),
    }
    if isinstance(raw_value, str) and raw_value_length <= MAX_PUBLIC_RAW_VALUE_CHARS and not payload["raw_value_truncated"]:
        payload["raw_value"] = raw_value
    return payload


def _count_by(records: list[dict[str, Any]], key: str, expected_keys: list[str]) -> dict[str, int]:
    counts = Counter(str(record.get(key)) for record in records)
    return {expected: int(counts.get(expected, 0)) for expected in expected_keys}


def _disposition_record_errors(
    index: int,
    record: dict[str, Any],
    *,
    mapping_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    context = f"dispositions[{index}]"
    required = {
        "review_item_id",
        "run_id",
        "inventory_source_family",
        "source_name",
        "source_role",
        "source_header_path",
        "source_label",
        "proposed_field_key",
        "review_kind",
        "shape_classes",
        "affected_count",
        "representative_examples",
        "disposition",
        "rationale",
        "json_schema_redesign_blocked",
        "supercombo_mapping_dependency",
        "next_execplan_needed",
        "reviewer_notes",
    }
    for key in sorted(required):
        if key not in record:
            errors.append(f"{context}.{key} is required")
    if record.get("run_id") != RUN_ID:
        errors.append(f"{context}.run_id must be {RUN_ID}")
    if "source_family" in record:
        errors.append(f"{context} must use inventory_source_family, not source_family")
    if record.get("inventory_source_family") not in {"official", "supercombo"}:
        errors.append(f"{context}.inventory_source_family must be official or supercombo")
    if record.get("source_name") != record.get("inventory_source_family"):
        errors.append(f"{context}.source_name must match inventory_source_family")
    if record.get("source_name") == "official" and record.get("source_role") != "authority_candidate":
        errors.append(f"{context}.source_role must be authority_candidate for official")
    if record.get("source_name") == "supercombo" and record.get("source_role") not in {"enrichment_candidate", "cross_reference_candidate"}:
        errors.append(f"{context}.source_role must keep SuperCombo as enrichment/cross-reference/candidate")
    if not isinstance(record.get("source_header_path"), list) or not record.get("source_header_path"):
        errors.append(f"{context}.source_header_path must be a non-empty list")
    if record.get("source_label") != (record.get("source_header_path") or [""])[-1]:
        errors.append(f"{context}.source_label must match source_header_path leaf")
    if record.get("review_kind") not in {"unclassified_expression", "source_specific_expression", "malformed_looking_source_value"}:
        errors.append(f"{context}.review_kind is not approved")
    if record.get("disposition") not in DISPOSITIONS:
        errors.append(f"{context}.disposition is not approved")
    if int(record.get("affected_count") or 0) <= 0:
        errors.append(f"{context}.affected_count must be positive")
    if "parsed_value" in record:
        errors.append(f"{context} must not include parsed_value")
    if record.get("source_name") == "supercombo":
        dependency = record.get("supercombo_mapping_dependency")
        mapping = mapping_by_id.get(dependency)
        if not dependency or not mapping:
            errors.append(f"{context}.supercombo_mapping_dependency must reference a mapping record")
        else:
            if record.get("source_header_path") != mapping.get("source_header_path"):
                errors.append(f"{context}.supercombo_mapping_dependency source_header_path mismatch")
            if record.get("source_role") != mapping.get("source_role"):
                errors.append(f"{context}.source_role must match mapping source_role")
            if record.get("proposed_field_key") != mapping.get("proposed_field_key"):
                errors.append(f"{context}.proposed_field_key must match mapping proposed_field_key")
    elif record.get("supercombo_mapping_dependency") is not None:
        errors.append(f"{context}.supercombo_mapping_dependency must be null for official")
    if record.get("disposition") in {
        "parse_rule_required_before_schema",
        "source_specific_enum_required",
        "blocked_pending_source_review",
    } and record.get("json_schema_redesign_blocked") is not True:
        errors.append(f"{context}.json_schema_redesign_blocked must be true for blocking dispositions")
    if record.get("disposition") in {"schema_supports_raw_only", "out_of_scope_first_normalized_export"} and record.get("json_schema_redesign_blocked") is not False:
        errors.append(f"{context}.json_schema_redesign_blocked must be false for accepted raw-only/out-of-scope dispositions")
    errors.extend(_example_errors(context, record.get("representative_examples", [])))
    return errors


def _example_errors(context: str, examples: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(examples, list):
        return [f"{context}.representative_examples must be a list"]
    for example_index, example in enumerate(examples):
        if not isinstance(example, dict):
            errors.append(f"{context}.representative_examples[{example_index}] must be an object")
            continue
        for key in ("raw_value_excerpt", "raw_value_sha256", "raw_value_length", "raw_value_truncated"):
            if key not in example:
                errors.append(f"{context}.representative_examples[{example_index}].{key} is required")
        if "raw_value" in example and len(str(example["raw_value"])) > MAX_PUBLIC_RAW_VALUE_CHARS:
            errors.append(f"{context}.representative_examples[{example_index}].raw_value must not exceed public limit")
        if not str(example.get("raw_value_sha256", "")).startswith("sha256:"):
            errors.append(f"{context}.representative_examples[{example_index}].raw_value_sha256 must use sha256: prefix")
    return errors


def _summary_count_errors(payload: dict[str, Any], dispositions: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if payload.get("total_review_items") != len(dispositions):
        errors.append("total_review_items must match dispositions length")
    for key, expected_keys in [
        ("disposition_counts", DISPOSITIONS),
        ("inventory_source_family_counts", ["official", "supercombo"]),
        ("review_kind_counts", ["malformed_looking_source_value", "source_specific_expression", "unclassified_expression"]),
        ("source_role_counts", ["authority_candidate", "cross_reference_candidate", "enrichment_candidate"]),
    ]:
        record_key = key.removesuffix("_counts")
        if key == "inventory_source_family_counts":
            record_key = "inventory_source_family"
        elif key == "review_kind_counts":
            record_key = "review_kind"
        elif key == "source_role_counts":
            record_key = "source_role"
        expected = _count_by(dispositions, record_key, expected_keys)
        if payload.get(key) != expected:
            errors.append(f"{key} must match disposition records")
    dependency_count = sum(1 for item in dispositions if item.get("supercombo_mapping_dependency"))
    if payload.get("supercombo_mapping_dependency_count") != dependency_count:
        errors.append("supercombo_mapping_dependency_count must match disposition records")
    blocked_count = sum(1 for item in dispositions if item.get("json_schema_redesign_blocked"))
    if payload.get("json_schema_redesign_blocked_count") != blocked_count:
        errors.append("json_schema_redesign_blocked_count must match disposition records")
    return errors


def _forbidden_public_text_errors(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(repo_root()).as_posix() if path.is_absolute() and path.is_relative_to(repo_root()) else path.as_posix()
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"{relative}: forbidden public disposition content: {match.group(0).strip()}")
            break
    for literal in [".local/", ".venv/", ".agents/", "/tmp", "page.html", "official_table_rows.raw.json", "supercombo_tables.raw.json"]:
        if literal in text:
            errors.append(f"{relative}: forbidden public disposition literal: {literal}")
    return errors


def _contains_forbidden_authority_claim(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_authority_claim(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_authority_claim(item) for item in value)
    return value in {"current_fact_authority", "authority"}


def _markdown_code(value: str) -> str:
    return "`" + str(value).replace("`", "\\`") + "`"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="value-shape-disposition")
    subparsers = parser.add_subparsers(required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--inventory", type=Path, default=default_inventory_path())
    build.add_argument("--mapping", type=Path, default=default_mapping_path())
    build.add_argument("--json-output", type=Path, default=default_output_json_path())
    build.add_argument("--markdown-output", type=Path, default=default_output_md_path())
    build.set_defaults(func=_build_command)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--inventory", type=Path, default=default_inventory_path())
    validate.add_argument("--mapping", type=Path, default=default_mapping_path())
    validate.add_argument("--json", type=Path, default=default_output_json_path())
    validate.add_argument("--markdown", type=Path, default=default_output_md_path())
    validate.set_defaults(func=_validate_command)
    return parser


def _build_command(args: argparse.Namespace) -> dict[str, Any]:
    disposition = build_disposition_summary(inventory_path=args.inventory, mapping_path=args.mapping)
    write_disposition_artifacts(disposition, json_path=args.json_output, markdown_path=args.markdown_output)
    validate_disposition_artifacts(
        json_path=args.json_output,
        markdown_path=args.markdown_output,
        inventory_path=args.inventory,
        mapping_path=args.mapping,
    )
    return {
        "ok": True,
        "run_id": disposition["run_id"],
        "json": str(args.json_output),
        "markdown": str(args.markdown_output),
        "total_review_items": disposition["total_review_items"],
        "disposition_counts": disposition["disposition_counts"],
    }


def _validate_command(args: argparse.Namespace) -> dict[str, Any]:
    validate_disposition_artifacts(
        json_path=args.json,
        markdown_path=args.markdown,
        inventory_path=args.inventory,
        mapping_path=args.mapping,
    )
    return {"ok": True, "json": str(args.json), "markdown": str(args.markdown)}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
