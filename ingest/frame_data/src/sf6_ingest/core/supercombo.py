from __future__ import annotations

import re
from dataclasses import dataclass

from selectolax.parser import HTMLParser, Node

from ..config import load_character
from ..binding_policy import LoadedSupercomboBindingPolicy, SupercomboBindingEntry
from ..registry import LoadedRegistry
from ..schemas import SnapshotMetadata, SourceRunStatus, SupercomboNormalizedRecord
from .common import (
    build_supercombo_source_row_id,
    canonical_group,
    compact_text,
    mark_manual_review,
    normalize_supercombo_input,
    stable_json_dumps,
)


EXPECTED_LABEL_BLOCKS: tuple[tuple[int, tuple[str, ...]], ...] = (
    (3, ("Damage", "Chip Dmg", "Dmg Scaling", "Guard", "Cancel", "Hitconfirm Window")),
    (5, ("Startup", "Active", "Recovery", "Hitstun", "Blockstun", "Hitstop")),
    (7, ("Total", "DriveDmg Blk", "DriveDmg Hit [PC]", "Drive Gain", "Super Gain Hit", "Super Gain Blk")),
    (9, ("Invuln", "Armor", "Airborne", "Juggle Start", "Juggle Increase", "Juggle Limit")),
    (11, ("After DR Hit", "After DR Blk", "Projectile Speed", "Attack Range", "DR Cancel Hit", "DR Cancel Blk")),
    (13, ("Punish Advantage", "Perfect Parry Advantage")),
    (15, ("Hit Advantage", "Block Advantage")),
    (17, ("Notes",)),
)

REDUCED_LABEL_MAP = {
    "Hitconfirm Window": "hitconfirm_window",
    "Hitstun": "hitstun",
    "Blockstun": "blockstun",
    "Hitstop": "hitstop",
    "Punish Advantage": "punish_adv",
    "Perfect Parry Advantage": "perf_parry_adv",
    "DR Cancel Hit": "dr_cancel_hit",
    "DR Cancel Blk": "dr_cancel_blk",
    "After DR Hit": "after_dr_hit",
    "After DR Blk": "after_dr_blk",
    "Invuln": "invuln",
    "Armor": "armor",
    "Airborne": "airborne",
    "Juggle Start": "jug_start",
    "Juggle Increase": "jug_increase",
    "Juggle Limit": "jug_limit",
    "Projectile Speed": "proj_speed",
    "Attack Range": "atk_range",
    "Super Gain Blk": "super_gain_blk",
    "Notes": "notes_sc",
}


@dataclass(frozen=True)
class ParsedSupercomboRow:
    table_index: int
    raw_source_token: str
    move_name: str | None
    input: str | None
    move_group: str
    field_map: dict[str, str | None]
    raw_row_json: str
    row_review_reasons: list[str]


def parse_supercombo_snapshot(
    snapshot_metadata: SnapshotMetadata,
    html: str,
    registry: LoadedRegistry,
    binding_policy: LoadedSupercomboBindingPolicy,
) -> tuple[list[SupercomboNormalizedRecord], SourceRunStatus]:
    status = SourceRunStatus(
        source="supercombo",
        selected=True,
        snapshot_id=snapshot_metadata.snapshot_id,
        fetch_success=snapshot_metadata.success,
    )
    tree = HTMLParser(html)
    main = tree.css_first("main")
    if main is None:
        status.parse_state = "blocked"
        status.blockers.append("missing supercombo main element")
        status.blocker_count = len(status.blockers)
        return [], status

    headings = {"h2": "", "h3": "", "h4": "", "h5": ""}
    parsed_rows: list[ParsedSupercomboRow] = []
    character_label = load_character(snapshot_metadata.character_slug).display_name

    table_index = -1
    for node in main.traverse():
        tag = node.tag.lower()
        if tag in headings:
            headings[tag] = compact_text(node.text(separator=" ", strip=True)) or ""
            if tag == "h2":
                headings["h3"] = headings["h4"] = headings["h5"] = ""
            elif tag == "h3":
                headings["h4"] = headings["h5"] = ""
            elif tag == "h4":
                headings["h5"] = ""
            continue
        if tag != "table":
            continue

        table_index += 1
        parsed_row, blocker = _parse_move_table(snapshot_metadata, node, table_index, headings, character_label)
        if blocker:
            status.blockers.append(blocker)
            continue
        if parsed_row is not None:
            parsed_rows.append(parsed_row)

    if not parsed_rows and not status.blockers:
        status.blockers.append("no supercombo move tables parsed")

    records = [_bind_row(snapshot_metadata, row, registry, binding_policy) for row in parsed_rows]
    status.parse_state = "blocked" if status.blockers else "parsed"
    status.row_count = len(parsed_rows)
    status.matched_row_count = sum(1 for record in records if record.move_id is not None)
    status.manual_review_count = sum(1 for record in records if record.manual_review_needed)
    status.blocker_count = len(status.blockers)
    return records, status


def _parse_move_table(
    snapshot_metadata: SnapshotMetadata,
    node: Node,
    table_index: int,
    headings: dict[str, str],
    character_label: str,
) -> tuple[ParsedSupercomboRow | None, str | None]:
    rows = [_extract_row_cells(table_row) for table_row in node.css("tr")]
    if not rows:
        return None, None

    source_row = rows[0]
    raw_source_token = _extract_raw_source_token(source_row, character_label)
    if raw_source_token is None:
        return None, None

    if len(rows) != 19:
        return None, f"supercombo table shape drift table_index={table_index} raw_source_token={raw_source_token} rows={len(rows)}"
    if len(rows[1]) != 1:
        return None, f"supercombo table shape drift table_index={table_index} raw_source_token={raw_source_token} move_header={len(rows[1])}"

    input_value, move_name = _parse_move_header(rows[1][0])
    row_review_reasons: list[str] = []
    field_map: dict[str, str | None] = {}

    for row_position, expected_labels in EXPECTED_LABEL_BLOCKS:
        labels = tuple(cell for cell in rows[row_position] if cell)
        if labels != expected_labels:
            row_review_reasons.append(
                f"supercombo label mismatch row={row_position} expected={'|'.join(expected_labels)} actual={'|'.join(labels)}"
            )
            continue
        values = rows[row_position + 1]
        if len(values) < len(expected_labels):
            row_review_reasons.append(f"supercombo value row short row={row_position + 1}")
            continue
        for label, value in zip(expected_labels, values):
            field_map[label] = compact_text(value)

    payload = {
        "heading_chain": headings,
        "table_index": table_index,
        "table_rows": rows,
        "field_map": field_map,
    }
    return (
        ParsedSupercomboRow(
            table_index=table_index,
            raw_source_token=raw_source_token,
            move_name=move_name,
            input=input_value,
            move_group=canonical_group(headings["h4"] or headings["h3"] or headings["h2"]),
            field_map=field_map,
            raw_row_json=stable_json_dumps(payload),
            row_review_reasons=row_review_reasons,
        ),
        None,
    )


def _bind_row(
    snapshot_metadata: SnapshotMetadata,
    row: ParsedSupercomboRow,
    registry: LoadedRegistry,
    binding_policy: LoadedSupercomboBindingPolicy,
) -> SupercomboNormalizedRecord:
    binding = binding_policy.lookup(row.raw_source_token)
    move_id = binding.target_move_id if binding else None
    move_group = registry.by_move_id[move_id].group if move_id and move_id in registry.by_move_id else row.move_group
    payload: dict[str, object] = {
        "source": "supercombo",
        "snapshot_id": snapshot_metadata.snapshot_id,
        "source_row_id": build_supercombo_source_row_id(snapshot_metadata.snapshot_id, row.table_index, row.raw_source_token),
        "raw_source_token": row.raw_source_token,
        "table_index": row.table_index,
        "character_slug": snapshot_metadata.character_slug,
        "source_url": snapshot_metadata.source_url,
        "page_locale": snapshot_metadata.page_locale,
        "fetched_at": snapshot_metadata.fetched_at,
        "move_id": move_id,
        "move_name": row.move_name,
        "input": row.input,
        "move_group": move_group,
        "binding_class": binding.binding_class if binding else None,
        "publish_eligible": bool(binding.publish_eligible) if binding else False,
        "confirmation_status": binding.confirmation_status if binding else None,
        "binding_confirmed": bool(binding and binding.confirmation_status == "confirmed"),
        "candidate_move_ids": list(binding.candidate_move_ids) if binding else [],
        "collision_group": binding.collision_group if binding else None,
        "conflicting_move_ids": list(binding.conflicting_move_ids) if binding else [],
        "raw_row_json": row.raw_row_json,
        "extraction_confidence": "high",
        "manual_review_needed": False,
        "review_reasons": [],
    }
    for label, field_name in REDUCED_LABEL_MAP.items():
        payload[field_name] = row.field_map.get(label)

    if binding is None:
        mark_manual_review(payload, "binding policy missing", "low")
    else:
        _apply_binding_review(payload, binding)
    for review_reason in row.row_review_reasons:
        mark_manual_review(payload, review_reason, "medium")
    return SupercomboNormalizedRecord.model_validate(payload)


def _apply_binding_review(payload: dict[str, object], binding: SupercomboBindingEntry) -> None:
    if binding.binding_class == "D":
        mark_manual_review(payload, "supercombo one-to-many binding withheld", "medium")
    elif binding.binding_class == "E":
        mark_manual_review(payload, "supercombo many-to-one binding collision", "medium")
    elif binding.binding_class == "G":
        mark_manual_review(payload, "supercombo excluded binding", "medium")
    elif binding.binding_class == "F" and (not binding.publish_eligible or binding.confirmation_status != "confirmed"):
        mark_manual_review(payload, "supercombo unconfirmed class F binding", "medium")


def _extract_row_cells(table_row: Node) -> list[str]:
    return [compact_text(cell.text(separator=" ", strip=True)) or "" for cell in table_row.css("th, td")]


def _extract_raw_source_token(source_row: list[str], character_label: str) -> str | None:
    if len(source_row) != 1:
        return None
    source_label_and_token = compact_text(source_row[0])
    if not source_label_and_token:
        return None
    parts = source_label_and_token.split()
    if len(parts) < 2:
        return None
    source_label = " ".join(parts[:-1])
    if _normalize_character_label(source_label) != _normalize_character_label(character_label):
        return None
    return compact_text(parts[-1])


def _normalize_character_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _parse_move_header(value: str) -> tuple[str | None, str | None]:
    text = compact_text(value)
    if not text:
        return None, None
    match = re.match(r"(\S+)\s+(.*)", text)
    if not match:
        normalized = normalize_supercombo_input(text)
        return normalized, None
    notation = normalize_supercombo_input(match.group(1))
    move_name = compact_text(match.group(2))
    return notation, move_name
