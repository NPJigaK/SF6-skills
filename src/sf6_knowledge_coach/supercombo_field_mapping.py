from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import repo_root
from .value_shape_inventory import validate_inventory_artifacts


RUN_ID = "20260521T025403Z"
INPUT_INVENTORY_JSON = Path("data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json")
INPUT_INVENTORY_MD = Path("docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md")
OUTPUT_JSON = Path("data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json")
OUTPUT_MD = Path("docs/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-review.md")
ARTIFACT_SCHEMA_VERSION = "supercombo_field_mapping_summary/v1"
EXPECTED_SUPERCOMBO_FIELD_SUMMARIES = 403

MAPPING_STATUSES = [
    "maps_to_existing_official_field_key",
    "supercombo_source_specific_field_key",
    "enrichment_only_no_current_fact_mapping",
    "out_of_scope_first_normalized_export",
    "blocked_pending_human_review",
]

SEMANTIC_SOURCE_FAMILIES = {
    "timing",
    "advantage",
    "damage",
    "gauge",
    "cancel",
    "guard",
    "defense",
    "projectile",
    "throw",
    "mobility",
    "vital",
    "identity",
    "note",
    "metadata",
    "unknown",
}

MOVE_SECTIONS = {
    "Command Normals",
    "Drive Moves",
    "Hidden Arts",
    "Normals",
    "Prowler Stance",
    "Serenity Stream",
    "Special Moves",
    "Super Arts",
    "Target Combos",
    "Throws",
}

OUT_OF_SCOPE_SECTIONS = {"Taunts"}

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
class MappingPolicy:
    mapping_status: str
    source_family: str
    proposed_field_key: str | None
    official_field_key_target: str | None
    source_role: str
    rationale: str
    json_schema_redesign_blocked: bool = False
    display_label_ja: str | None = None


OFFICIAL_CROSS_REFERENCE_LABELS: dict[str, tuple[str, str, str]] = {
    "Startup": ("startup", "timing", "SuperCombo Startup is a cross-reference candidate for official startup after review."),
    "Active": ("active", "timing", "SuperCombo Active is a cross-reference candidate for official active frames after review."),
    "Recovery": ("recovery", "timing", "SuperCombo Recovery is a cross-reference candidate for official recovery after review."),
    "Hit Advantage": ("hit_advantage", "advantage", "SuperCombo Hit Advantage is a cross-reference candidate for official hit advantage after review."),
    "Block Advantage": ("block_advantage", "advantage", "SuperCombo Block Advantage is a cross-reference candidate for official block advantage after review."),
    "Cancel": ("cancel", "cancel", "SuperCombo Cancel is a cross-reference candidate for official cancel after category review."),
    "Damage": ("damage", "damage", "SuperCombo Damage is a cross-reference candidate for official damage after review."),
    "Dmg Scaling": ("combo_scaling", "damage", "SuperCombo Dmg Scaling is a cross-reference candidate for official combo scaling after review."),
}

SUPERCOMBO_SPECIFIC_MOVE_LABELS: dict[str, tuple[str, str, str]] = {
    "After DR Blk": ("supercombo_after_drive_rush_block_advantage", "advantage", "Drive-rush block advantage is SuperCombo-specific enrichment."),
    "After DR Hit": ("supercombo_after_drive_rush_hit_advantage", "advantage", "Drive-rush hit advantage is SuperCombo-specific enrichment."),
    "Airborne": ("supercombo_airborne", "defense", "Airborne state is SuperCombo-specific categorical enrichment."),
    "Armor": ("supercombo_armor", "defense", "Armor state is SuperCombo-specific categorical enrichment."),
    "Attack Range": ("supercombo_attack_range", "metadata", "Attack range is SuperCombo-specific context, not official numeric authority."),
    "Blockstun": ("supercombo_blockstun", "timing", "Blockstun is SuperCombo-specific timing enrichment."),
    "Chip Dmg": ("supercombo_chip_damage", "damage", "Chip damage is SuperCombo-specific damage enrichment."),
    "DR Cancel Blk": ("supercombo_drive_rush_cancel_block_advantage", "advantage", "Drive-rush cancel block advantage is SuperCombo-specific enrichment."),
    "DR Cancel Hit": ("supercombo_drive_rush_cancel_hit_advantage", "advantage", "Drive-rush cancel hit advantage is SuperCombo-specific enrichment."),
    "Drive Gain": ("supercombo_drive_gain", "gauge", "Drive gain is SuperCombo-specific gauge enrichment."),
    "DriveDmg Blk": ("supercombo_drive_damage_on_block", "gauge", "Drive damage on block is SuperCombo-specific gauge enrichment."),
    "DriveDmg Hit [PC]": ("supercombo_drive_damage_on_punish_counter_hit", "gauge", "Drive damage on punish counter hit is SuperCombo-specific gauge enrichment."),
    "Guard": ("supercombo_guard", "guard", "Guard category is SuperCombo-specific categorical enrichment."),
    "Hitconfirm Window": ("supercombo_hitconfirm_window", "timing", "Hitconfirm window is SuperCombo-specific timing enrichment."),
    "Hitstop": ("supercombo_hitstop", "timing", "Hitstop is SuperCombo-specific timing enrichment."),
    "Hitstun": ("supercombo_hitstun", "timing", "Hitstun is SuperCombo-specific timing enrichment."),
    "Invuln": ("supercombo_invulnerability", "defense", "Invulnerability is SuperCombo-specific defensive metadata."),
    "Juggle Increase": ("supercombo_juggle_increase", "metadata", "Juggle increase is SuperCombo-specific combo metadata."),
    "Juggle Limit": ("supercombo_juggle_limit", "metadata", "Juggle limit is SuperCombo-specific combo metadata."),
    "Juggle Start": ("supercombo_juggle_start", "metadata", "Juggle start is SuperCombo-specific combo metadata."),
    "Perfect Parry Advantage": ("supercombo_perfect_parry_advantage", "advantage", "Perfect parry advantage is SuperCombo-specific advantage enrichment."),
    "Projectile Speed": ("supercombo_projectile_speed", "projectile", "Projectile speed is SuperCombo-specific projectile metadata."),
    "Punish Advantage": ("supercombo_punish_advantage", "advantage", "Punish advantage is SuperCombo-specific advantage enrichment."),
    "Super Gain Blk": ("supercombo_super_gain_on_block", "gauge", "Super gain on block is SuperCombo-specific gauge enrichment."),
    "Super Gain Hit": ("supercombo_super_gain_on_hit", "gauge", "Super gain on hit is SuperCombo-specific gauge enrichment."),
    "Total": ("supercombo_total_duration", "timing", "Total duration is SuperCombo-specific timing enrichment."),
}

CHARACTER_VITALS_LABELS: dict[str, MappingPolicy] = {
    "Back Dash Distance": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_back_dash_distance", None, "enrichment_candidate", "Character back dash distance is SuperCombo-specific mobility enrichment."),
    "Back Dash Speed": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_back_dash_speed", None, "enrichment_candidate", "Character back dash speed is SuperCombo-specific mobility enrichment."),
    "Back Jump Distance": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_back_jump_distance", None, "enrichment_candidate", "Character back jump distance is SuperCombo-specific mobility enrichment."),
    "Back Walk Speed": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_back_walk_speed", None, "enrichment_candidate", "Character back walk speed is SuperCombo-specific mobility enrichment."),
    "Drive Rush Max Distance": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_drive_rush_max_distance", None, "enrichment_candidate", "Drive Rush max distance is SuperCombo-specific mobility enrichment."),
    "Drive Rush Min. Distance (Block)": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_drive_rush_min_distance_block", None, "enrichment_candidate", "Drive Rush minimum block distance is SuperCombo-specific mobility enrichment."),
    "Drive Rush Min. Distance (Throw)": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_drive_rush_min_distance_throw", None, "enrichment_candidate", "Drive Rush minimum throw distance is SuperCombo-specific mobility enrichment."),
    "Forward Dash Distance": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_forward_dash_distance", None, "enrichment_candidate", "Character forward dash distance is SuperCombo-specific mobility enrichment."),
    "Forward Dash Speed": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_forward_dash_speed", None, "enrichment_candidate", "Character forward dash speed is SuperCombo-specific mobility enrichment."),
    "Forward Jump Distance": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_forward_jump_distance", None, "enrichment_candidate", "Character forward jump distance is SuperCombo-specific mobility enrichment."),
    "Forward Walk Speed": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_forward_walk_speed", None, "enrichment_candidate", "Character forward walk speed is SuperCombo-specific mobility enrichment."),
    "HP": MappingPolicy("supercombo_source_specific_field_key", "vital", "supercombo_character_hp", None, "enrichment_candidate", "Character HP is SuperCombo-specific vital enrichment."),
    "Icon": MappingPolicy("out_of_scope_first_normalized_export", "metadata", None, None, "enrichment_candidate", "Icon media is excluded from first normalized and enrichment outputs."),
    "Jump Apex": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_jump_apex", None, "enrichment_candidate", "Jump apex is SuperCombo-specific mobility enrichment."),
    "Jump Speed": MappingPolicy("supercombo_source_specific_field_key", "mobility", "supercombo_jump_speed", None, "enrichment_candidate", "Jump speed is SuperCombo-specific mobility enrichment."),
    "Portrait": MappingPolicy("out_of_scope_first_normalized_export", "metadata", None, None, "enrichment_candidate", "Portrait media is excluded from first normalized and enrichment outputs."),
    "Throw Range / Hurtbox": MappingPolicy("blocked_pending_human_review", "throw", None, None, "enrichment_candidate", "Combined throw range and hurtbox semantics require human review before mapping.", True),
}


def default_input_json_path() -> Path:
    return repo_root() / INPUT_INVENTORY_JSON


def default_output_json_path() -> Path:
    return repo_root() / OUTPUT_JSON


def default_output_md_path() -> Path:
    return repo_root() / OUTPUT_MD


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    inventory_path = path or default_input_json_path()
    validate_inventory_artifacts()
    return json.loads(inventory_path.read_text(encoding="utf-8"))


def build_mapping_summary(*, inventory_path: Path | None = None) -> dict[str, Any]:
    inventory = load_inventory(inventory_path)
    if inventory.get("run_id") != RUN_ID:
        raise ValueError(f"input inventory run_id must be {RUN_ID}")

    supercombo_summaries = [
        summary for summary in inventory.get("field_shape_summaries", [])
        if summary.get("source_family") == "supercombo"
    ]
    if len(supercombo_summaries) != EXPECTED_SUPERCOMBO_FIELD_SUMMARIES:
        raise ValueError(f"expected {EXPECTED_SUPERCOMBO_FIELD_SUMMARIES} SuperCombo field summaries")

    review_item_counts = Counter(
        tuple(item.get("source_header_path", []))
        for item in inventory.get("review_items", [])
        if item.get("source_family") == "supercombo"
    )
    mappings = [_mapping_record(summary, review_item_counts) for summary in supercombo_summaries]
    mappings.sort(key=lambda item: item["source_header_path"])
    summary = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_id": RUN_ID,
        "input_inventory": INPUT_INVENTORY_JSON.as_posix(),
        "artifact_boundary": "mapping_summary_only",
        "authority_status": "supercombo_not_numeric_authority",
        "total_supercombo_field_summaries": len(mappings),
        "mapping_status_counts": _count_by(mappings, "mapping_status", MAPPING_STATUSES),
        "source_family_counts": _count_by(mappings, "source_family", sorted(SEMANTIC_SOURCE_FAMILIES)),
        "source_role_counts": _count_by(mappings, "source_role", ["cross_reference_candidate", "enrichment_candidate"]),
        "section_counts": _section_counts(mappings),
        "json_schema_redesign_blocked_count": sum(1 for item in mappings if item["json_schema_redesign_blocked"]),
        "value_shape_disposition_dependency_count": sum(1 for item in mappings if item["value_shape_disposition_dependency"]),
        "mappings": mappings,
        "source_boundary": {
            "raw_html_public_commit": "forbidden",
            "full_raw_rows_public_commit": "forbidden",
            "full_source_table_public_commit": "forbidden",
            "parsed_values": "not_emitted",
        },
    }
    errors = validate_mapping_payload(summary, inventory=inventory)
    if errors:
        raise ValueError("\n".join(errors))
    return summary


def write_mapping_artifacts(
    mapping: dict[str, Any],
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> None:
    output_json = json_path or default_output_json_path()
    output_md = markdown_path or default_output_md_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_mapping_markdown(mapping), encoding="utf-8")


def validate_mapping_artifacts(
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
    inventory_path: Path | None = None,
) -> list[str]:
    output_json = json_path or default_output_json_path()
    output_md = markdown_path or default_output_md_path()
    errors: list[str] = []
    if not output_json.exists():
        errors.append(f"Missing SuperCombo mapping JSON summary: {output_json.relative_to(repo_root())}")
    if not output_md.exists():
        errors.append(f"Missing SuperCombo mapping Markdown summary: {output_md.relative_to(repo_root())}")
    if errors:
        return errors
    try:
        payload = json.loads(output_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid SuperCombo mapping JSON summary: {exc}"]
    inventory = load_inventory(inventory_path)
    errors.extend(validate_mapping_payload(payload, inventory=inventory))
    for path in (output_json, output_md):
        errors.extend(_forbidden_public_text_errors(path.read_text(encoding="utf-8"), path))
    if errors:
        raise ValueError("\n".join(errors))
    return []


def validate_mapping_payload(payload: dict[str, Any], *, inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("artifact_schema_version") != ARTIFACT_SCHEMA_VERSION:
        errors.append(f"artifact_schema_version must be {ARTIFACT_SCHEMA_VERSION}")
    if payload.get("run_id") != RUN_ID:
        errors.append(f"run_id must be {RUN_ID}")
    if payload.get("artifact_boundary") != "mapping_summary_only":
        errors.append("artifact_boundary must be mapping_summary_only")
    if payload.get("authority_status") != "supercombo_not_numeric_authority":
        errors.append("authority_status must be supercombo_not_numeric_authority")
    if _contains_forbidden_authority_claim(payload):
        errors.append("mapping must not claim current_fact_authority")

    input_paths = {
        tuple(summary.get("source_header_path", []))
        for summary in inventory.get("field_shape_summaries", [])
        if summary.get("source_family") == "supercombo"
    }
    mappings = payload.get("mappings", [])
    if not isinstance(mappings, list):
        errors.append("mappings must be a list")
        mappings = []
    if len(mappings) != EXPECTED_SUPERCOMBO_FIELD_SUMMARIES:
        errors.append(f"mappings must contain exactly {EXPECTED_SUPERCOMBO_FIELD_SUMMARIES} records")
    mapping_paths = [tuple(record.get("source_header_path", [])) for record in mappings if isinstance(record, dict)]
    duplicate_paths = sorted(path for path, count in Counter(mapping_paths).items() if count > 1)
    if duplicate_paths:
        errors.append(f"duplicate source_header_path mappings: {duplicate_paths[:3]}")
    if set(mapping_paths) != input_paths:
        missing = sorted(input_paths - set(mapping_paths))
        extra = sorted(set(mapping_paths) - input_paths)
        if missing:
            errors.append(f"missing SuperCombo source_header_path mappings: {missing[:3]}")
        if extra:
            errors.append(f"unexpected SuperCombo source_header_path mappings: {extra[:3]}")

    for index, record in enumerate(mappings):
        if not isinstance(record, dict):
            errors.append(f"mappings[{index}] must be an object")
            continue
        errors.extend(_mapping_record_errors(index, record))
    errors.extend(_summary_count_errors(payload, mappings))
    return errors


def render_mapping_markdown(mapping: dict[str, Any]) -> str:
    lines = [
        "# SuperCombo Canonical Field Mapping Review",
        "",
        "This artifact is a mapping summary only. It does not emit parsed",
        "values, does not implement schema/parser behavior, and does not make",
        "SuperCombo numeric authority.",
        "",
        f"- Run ID: `{mapping['run_id']}`",
        f"- Input inventory: `{mapping['input_inventory']}`",
        f"- Total SuperCombo field summaries: `{mapping['total_supercombo_field_summaries']}`",
        f"- JSON Schema redesign blocked records: `{mapping['json_schema_redesign_blocked_count']}`",
        f"- Value-shape disposition dependencies: `{mapping['value_shape_disposition_dependency_count']}`",
        "",
        "## Mapping Status Counts",
        "",
    ]
    for status, count in mapping["mapping_status_counts"].items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Section Counts", ""])
    for section, count in mapping["section_counts"].items():
        lines.append(f"- `{section}`: {count}")
    lines.extend(
        [
            "",
            "## Mappings",
            "",
            "| Source header path | Status | Source family | Role | Proposed key | Official target | Observations | Review items | Rationale |",
            "| --- | --- | --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for record in mapping["mappings"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _markdown_code(" > ".join(record["source_header_path"])),
                    _markdown_code(record["mapping_status"]),
                    _markdown_code(record["source_family"]),
                    _markdown_code(record["source_role"]),
                    _markdown_code(record["proposed_field_key"] or ""),
                    _markdown_code(record["official_field_key_target"] or ""),
                    str(record["observation_count"]),
                    str(record["review_item_count"]),
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
            "- `source_label` and `source_header_path` remain source-native.",
            "- `source_family` is semantic and is never `supercombo`.",
            "- `source_name` is always `supercombo`.",
            "- SuperCombo remains enrichment/cross-reference/candidate only.",
            "- JSON Schema redesign remains blocked until this artifact and value-shape disposition are reviewed.",
        ]
    )
    return "\n".join(lines) + "\n"


def _mapping_record(summary: dict[str, Any], review_item_counts: Counter[tuple[str, ...]]) -> dict[str, Any]:
    source_header_path = [str(part) for part in summary.get("source_header_path", [])]
    source_section = source_header_path[0] if source_header_path else ""
    source_label = source_header_path[-1] if source_header_path else ""
    policy = _policy_for(source_section, source_label)
    review_item_count = int(review_item_counts.get(tuple(source_header_path), 0))
    return {
        "mapping_id": _mapping_id(source_header_path),
        "run_id": RUN_ID,
        "source_name": "supercombo",
        "source_role": policy.source_role,
        "source_header_path": source_header_path,
        "source_label": source_label,
        "source_section": source_section,
        "source_family": policy.source_family,
        "proposed_field_key": policy.proposed_field_key,
        "official_field_key_target": policy.official_field_key_target,
        "mapping_status": policy.mapping_status,
        "display_label_ja": policy.display_label_ja,
        "affected_field_summary_count": 1,
        "observation_count": int(summary.get("row_or_cell_count", 0)),
        "shape_classes": _shape_classes(summary),
        "review_item_count": review_item_count,
        "rationale": policy.rationale,
        "json_schema_redesign_blocked": policy.json_schema_redesign_blocked,
        "value_shape_disposition_dependency": "value_shape_review_item_disposition_required" if review_item_count else None,
    }


def _policy_for(section: str, label: str) -> MappingPolicy:
    if section == "Character Vitals":
        if label not in CHARACTER_VITALS_LABELS:
            return MappingPolicy("blocked_pending_human_review", "vital", None, None, "enrichment_candidate", "Unknown Character Vitals label requires human review.", True)
        return CHARACTER_VITALS_LABELS[label]
    if section == "SF6 Navigation":
        return MappingPolicy("out_of_scope_first_normalized_export", "metadata", None, None, "enrichment_candidate", "SF6 Navigation is excluded from first normalized and enrichment outputs.")
    if section in OUT_OF_SCOPE_SECTIONS:
        return MappingPolicy("out_of_scope_first_normalized_export", _source_family_for_label(label), None, None, "enrichment_candidate", f"{section} data is excluded from first normalized and enrichment outputs.")
    if section in MOVE_SECTIONS:
        if label in OFFICIAL_CROSS_REFERENCE_LABELS:
            official_key, source_family, rationale = OFFICIAL_CROSS_REFERENCE_LABELS[label]
            return MappingPolicy("maps_to_existing_official_field_key", source_family, official_key, official_key, "cross_reference_candidate", rationale)
        if label == "Notes":
            return MappingPolicy("enrichment_only_no_current_fact_mapping", "note", None, None, "enrichment_candidate", "Notes remain first-release enrichment/review context with no current-fact key.")
        if label in SUPERCOMBO_SPECIFIC_MOVE_LABELS:
            proposed_key, source_family, rationale = SUPERCOMBO_SPECIFIC_MOVE_LABELS[label]
            return MappingPolicy("supercombo_source_specific_field_key", source_family, proposed_key, None, "enrichment_candidate", rationale)
    return MappingPolicy("blocked_pending_human_review", "unknown", None, None, "enrichment_candidate", "No approved manual mapping policy exists for this source header path.", True)


def _source_family_for_label(label: str) -> str:
    if label in OFFICIAL_CROSS_REFERENCE_LABELS:
        return OFFICIAL_CROSS_REFERENCE_LABELS[label][1]
    if label in SUPERCOMBO_SPECIFIC_MOVE_LABELS:
        return SUPERCOMBO_SPECIFIC_MOVE_LABELS[label][1]
    if label == "Notes":
        return "note"
    return "metadata"


def _shape_classes(summary: dict[str, Any]) -> list[str]:
    counts = summary.get("shape_counts", {})
    return sorted(key for key, value in counts.items() if int(value or 0) > 0)


def _mapping_id(source_header_path: list[str]) -> str:
    return "supercombo:" + "--".join(_slug(part) for part in source_header_path)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "empty"


def _count_by(records: list[dict[str, Any]], key: str, expected_keys: list[str]) -> dict[str, int]:
    counts = Counter(str(record.get(key)) for record in records)
    return {expected: int(counts.get(expected, 0)) for expected in expected_keys}


def _section_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(record.get("source_section")) for record in records)
    return dict(sorted(counts.items()))


def _mapping_record_errors(index: int, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    context = f"mappings[{index}]"
    status = record.get("mapping_status")
    source_role = record.get("source_role")
    proposed_field_key = record.get("proposed_field_key")
    official_target = record.get("official_field_key_target")
    if record.get("run_id") != RUN_ID:
        errors.append(f"{context}.run_id must be {RUN_ID}")
    if record.get("source_name") != "supercombo":
        errors.append(f"{context}.source_name must be supercombo")
    if source_role not in {"enrichment_candidate", "cross_reference_candidate"}:
        errors.append(f"{context}.source_role must be enrichment_candidate or cross_reference_candidate")
    if record.get("source_family") not in SEMANTIC_SOURCE_FAMILIES:
        errors.append(f"{context}.source_family must be a semantic category")
    if record.get("source_family") in {"official", "supercombo"}:
        errors.append(f"{context}.source_family must not be a source identity")
    if not isinstance(record.get("source_header_path"), list) or not record["source_header_path"]:
        errors.append(f"{context}.source_header_path must be a non-empty list")
    if record.get("source_label") != (record.get("source_header_path") or [""])[-1]:
        errors.append(f"{context}.source_label must match source_header_path leaf")
    if status not in MAPPING_STATUSES:
        errors.append(f"{context}.mapping_status must be approved")
    if "mapping_statuses" in record:
        errors.append(f"{context} must use exactly one mapping_status, not mapping_statuses")
    if status == "maps_to_existing_official_field_key":
        if source_role != "cross_reference_candidate":
            errors.append(f"{context}.source_role must be cross_reference_candidate when mapped to official")
        if not proposed_field_key:
            errors.append(f"{context}.proposed_field_key is required when mapped to official")
        if not official_target:
            errors.append(f"{context}.official_field_key_target is required when mapped to official")
        if proposed_field_key and official_target and proposed_field_key != official_target:
            errors.append(f"{context}.proposed_field_key must match official_field_key_target when mapped to official")
    elif official_target:
        errors.append(f"{context}.official_field_key_target is only allowed when mapped to official")
    if status == "supercombo_source_specific_field_key" and not proposed_field_key:
        errors.append(f"{context}.proposed_field_key is required for SuperCombo-specific fields")
    if status in {"enrichment_only_no_current_fact_mapping", "out_of_scope_first_normalized_export", "blocked_pending_human_review"} and proposed_field_key is not None:
        errors.append(f"{context}.proposed_field_key must be null for {status}")
    if status == "blocked_pending_human_review" and not record.get("json_schema_redesign_blocked"):
        errors.append(f"{context}.json_schema_redesign_blocked must be true for blocked mappings")
    if int(record.get("affected_field_summary_count") or 0) != 1:
        errors.append(f"{context}.affected_field_summary_count must be 1")
    if int(record.get("observation_count") or 0) <= 0:
        errors.append(f"{context}.observation_count must be positive")
    if "parsed_value" in record:
        errors.append(f"{context} must not include parsed_value")
    return errors


def _summary_count_errors(payload: dict[str, Any], mappings: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if payload.get("total_supercombo_field_summaries") != len(mappings):
        errors.append("total_supercombo_field_summaries must match mappings length")
    for key, expected_keys in [
        ("mapping_status_counts", MAPPING_STATUSES),
        ("source_family_counts", sorted(SEMANTIC_SOURCE_FAMILIES)),
        ("source_role_counts", ["cross_reference_candidate", "enrichment_candidate"]),
    ]:
        expected = _count_by(mappings, key.removesuffix("_counts"), expected_keys)
        if payload.get(key) != expected:
            errors.append(f"{key} must match mapping records")
    section_counts = _section_counts(mappings)
    if payload.get("section_counts") != section_counts:
        errors.append("section_counts must match mapping records")
    blocked_count = sum(1 for item in mappings if item.get("json_schema_redesign_blocked"))
    if payload.get("json_schema_redesign_blocked_count") != blocked_count:
        errors.append("json_schema_redesign_blocked_count must match mapping records")
    dependency_count = sum(1 for item in mappings if item.get("value_shape_disposition_dependency"))
    if payload.get("value_shape_disposition_dependency_count") != dependency_count:
        errors.append("value_shape_disposition_dependency_count must match mapping records")
    return errors


def _forbidden_public_text_errors(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(repo_root()).as_posix() if path.is_absolute() and path.is_relative_to(repo_root()) else path.as_posix()
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"{relative}: forbidden public mapping content: {match.group(0).strip()}")
            break
    for literal in [".local/", ".venv/", ".agents/", "/tmp", "page.html", "official_table_rows.raw.json", "supercombo_tables.raw.json"]:
        if literal in text:
            errors.append(f"{relative}: forbidden public mapping literal: {literal}")
    return errors


def _contains_forbidden_authority_claim(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_authority_claim(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_authority_claim(item) for item in value)
    return value in {"current_fact_authority", "authority", "authority_candidate"}


def _markdown_code(value: str) -> str:
    return "`" + str(value).replace("`", "\\`") + "`"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="supercombo-field-mapping")
    subparsers = parser.add_subparsers(required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--inventory", type=Path, default=default_input_json_path())
    build.add_argument("--json-output", type=Path, default=default_output_json_path())
    build.add_argument("--markdown-output", type=Path, default=default_output_md_path())
    build.set_defaults(func=_build_command)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--inventory", type=Path, default=default_input_json_path())
    validate.add_argument("--json", type=Path, default=default_output_json_path())
    validate.add_argument("--markdown", type=Path, default=default_output_md_path())
    validate.set_defaults(func=_validate_command)
    return parser


def _build_command(args: argparse.Namespace) -> dict[str, Any]:
    mapping = build_mapping_summary(inventory_path=args.inventory)
    write_mapping_artifacts(mapping, json_path=args.json_output, markdown_path=args.markdown_output)
    validate_mapping_artifacts(json_path=args.json_output, markdown_path=args.markdown_output, inventory_path=args.inventory)
    return {
        "ok": True,
        "run_id": mapping["run_id"],
        "json": str(args.json_output),
        "markdown": str(args.markdown_output),
        "mapping_count": len(mapping["mappings"]),
        "mapping_status_counts": mapping["mapping_status_counts"],
    }


def _validate_command(args: argparse.Namespace) -> dict[str, Any]:
    validate_mapping_artifacts(json_path=args.json, markdown_path=args.markdown, inventory_path=args.inventory)
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
