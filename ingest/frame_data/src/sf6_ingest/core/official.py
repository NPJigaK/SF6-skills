from __future__ import annotations

from selectolax.parser import HTMLParser

from ..registry import LoadedRegistry
from ..schemas import OfficialNormalizedRecord, SnapshotMetadata, SourceRunStatus
from .common import (
    build_official_source_row_id,
    canonical_group,
    compact_text,
    extract_explicit_total,
    join_nonempty,
    mark_manual_review,
    normalize_name_key,
    normalize_official_input,
    parse_official_active,
    stable_json_dumps,
    tokenize_input_string,
)


EXPECTED_OFFICIAL_CELL_COUNT = 15
OFFICIAL_HEADER_MARKERS = [
    "技名",
    "動作フレーム",
    "持続",
    "硬直",
    "ヒット",
    "ガード",
    "キャンセル",
    "ダメージ",
    "コンボ補正値",
    "Dゲージ増加",
    "Dゲージ減少",
    "パニッシュカウンター",
    "SAゲージ増加",
    "属性",
    "備考",
]


def parse_official_snapshot(snapshot_metadata: SnapshotMetadata, html: str, registry: LoadedRegistry) -> tuple[list[OfficialNormalizedRecord], SourceRunStatus]:
    status = SourceRunStatus(
        source="official",
        selected=True,
        snapshot_id=snapshot_metadata.snapshot_id,
        fetch_success=snapshot_metadata.success,
    )
    tree = HTMLParser(html)
    table = tree.css_first("table")
    if table is None:
        status.parse_state = "blocked"
        status.blockers.append("missing official table")
        status.blocker_count = len(status.blockers)
        return [], status

    header_text = " ".join(
        filter(
            None,
            (compact_text(node.text(separator=" ", strip=True)) for node in tree.css("table thead th")),
        )
    )
    missing_headers = [marker for marker in OFFICIAL_HEADER_MARKERS if marker not in header_text]
    if missing_headers:
        status.blockers.append(f"official header drift missing={','.join(missing_headers)}")

    records: list[OfficialNormalizedRecord] = []
    current_group = ""
    matched_rows = 0
    for row_index, row in enumerate(table.css("tbody tr"), start=1):
        cells = row.css("td")
        if len(cells) == 1 and cells[0].attributes.get("colspan"):
            current_group = compact_text(cells[0].text(separator=" ", strip=True)) or ""
            continue
        if len(cells) != EXPECTED_OFFICIAL_CELL_COUNT:
            status.blockers.append(f"official row length drift row={row_index} cells={len(cells)}")
            continue

        move_name_node = cells[0].css_first('[class*="frame_arts__"]')
        move_name = compact_text(move_name_node.text(separator=" ", strip=True) if move_name_node else cells[0].text(separator=" ", strip=True))
        input_node = cells[0].css_first("p")
        icon_sources = [image.attributes.get("src", "") for image in input_node.css("img")] if input_node else []
        normalized_input = normalize_official_input(icon_sources, move_name)
        icon_tokens = tokenize_input_string(normalized_input)
        section = canonical_group(current_group)
        name_key = normalize_name_key(move_name)
        combo_scaling_items = [compact_text(node.text(separator=" ", strip=True)) for node in cells[8].css("li")]
        notes_items = [compact_text(node.text(separator=" ", strip=True)) for node in cells[14].css("li")]
        starter_scaling = join_nonempty(combo_scaling_items)
        notes_official = join_nonempty(notes_items)
        recovery = compact_text(cells[3].text(separator=" ", strip=True))
        active = compact_text(cells[2].text(separator=" ", strip=True))
        total = extract_explicit_total(recovery)

        payload = {
            "source": "official",
            "snapshot_id": snapshot_metadata.snapshot_id,
            "source_row_id": build_official_source_row_id(snapshot_metadata.snapshot_id, current_group, row_index, move_name),
            "character_slug": snapshot_metadata.character_slug,
            "source_url": snapshot_metadata.source_url,
            "page_locale": snapshot_metadata.page_locale,
            "fetched_at": snapshot_metadata.fetched_at,
            "move_id": "",
            "move_name": move_name,
            "input": normalized_input,
            "move_group": section,
            "startup": compact_text(cells[1].text(separator=" ", strip=True)),
            "active": active,
            "recovery": recovery,
            "total": total,
            "hit_adv": compact_text(cells[4].text(separator=" ", strip=True)),
            "block_adv": compact_text(cells[5].text(separator=" ", strip=True)),
            "cancel": compact_text(cells[6].text(separator=" ", strip=True)),
            "damage": compact_text(cells[7].text(separator=" ", strip=True)),
            "starter_scaling": starter_scaling,
            "drive_gain_hit": compact_text(cells[9].text(separator=" ", strip=True)),
            "drive_loss_guard": compact_text(cells[10].text(separator=" ", strip=True)),
            "drive_loss_punish": compact_text(cells[11].text(separator=" ", strip=True)),
            "sa_gain": compact_text(cells[12].text(separator=" ", strip=True)),
            "attribute": compact_text(cells[13].text(separator=" ", strip=True)),
            "notes_official": notes_official,
            "raw_row_json": stable_json_dumps(
                {
                    "group_heading": current_group,
                    "section": section,
                    "cells": [compact_text(cell.text(separator=" ", strip=True)) for cell in cells],
                    "input_icons": icon_sources,
                    "icon_tokens": icon_tokens,
                    "name_key": name_key,
                    "combo_scaling": combo_scaling_items,
                    "notes": notes_items,
                }
            ),
            "extraction_confidence": "high",
            "manual_review_needed": False,
            "review_reasons": [],
        }

        matches = registry.match_official(section, icon_tokens, name_key)
        if len(matches) != 1:
            payload["move_id"] = f"unmatched:{payload['source_row_id']}"
            mark_manual_review(payload, "official registry mismatch", "low")
            status.blockers.append(f"official registry mismatch row={payload['source_row_id']}")
        else:
            payload["move_id"] = matches[0].move_id
            payload["move_group"] = matches[0].group
            matched_rows += 1

        if recovery and recovery.startswith("全体") and total is None:
            mark_manual_review(payload, "official total parse failed", "medium")
        active_parse = parse_official_active(active)
        if active and active_parse.ambiguous:
            mark_manual_review(payload, f"official active parse ambiguous: {active}", "medium")

        records.append(OfficialNormalizedRecord.model_validate(payload))

    status.parse_state = "blocked" if status.blockers else "parsed"
    status.row_count = len(records)
    status.matched_row_count = matched_rows
    status.manual_review_count = sum(1 for record in records if record.manual_review_needed)
    status.blocker_count = len(status.blockers)
    return records, status
