#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

from tools.battle_change.characters import canonical_character_slug
from tools.battle_change.official.capture import adjust_from_payload, validate_adjust_payload
from tools.battle_change.paths import repo_relative_path


CHANGE_FIELDS = [
    "version_order",
    "version_id",
    "version_title",
    "version_selector_title",
    "version_title_mismatch",
    "section_type",
    "section_order",
    "body_order",
    "policy_title",
    "common_title",
    "fighter_order",
    "fighter_id",
    "fighter_alpha",
    "fighter_tool_name",
    "fighter_url_name",
    "detail_order",
    "detail_title",
    "category",
    "text_html",
    "data_json_path",
]

CHANGE_EVENT_FIELDS = [
    "event_id",
    "source_authority",
    "version_order",
    "version_id",
    "version_title",
    "version_selector_title",
    "section_type",
    "scope",
    "section_order",
    "body_order",
    "fighter_order",
    "fighter_id",
    "fighter_alpha",
    "fighter_tool_name",
    "fighter_url_name",
    "character_slug",
    "detail_order",
    "target_title",
    "normalized_target_key",
    "category",
    "change_types",
    "confidence",
    "value_changes",
    "text_plain",
    "text_html",
    "data_json_path",
]

MOVE_CHANGE_INDEX_FIELDS = [
    "normalized_target_key",
    "scope",
    "fighter_tool_name",
    "fighter_alpha",
    "character_slug",
    "target_title",
    "event_count",
    "numeric_explicit_event_count",
    "version_ids",
    "event_ids",
    "source_authorities",
    "data_json_paths",
    "change_types",
]

VALUE_CHANGE_RE = re.compile(
    r"(?P<context>[^。\n]{0,32}?)"
    r"(?P<before>[+-]?\d+(?:\.\d+)?)\s*(?P<unit_before>F|f|％|%|本|バー|bars?|bar)?"
    r"\s*(?:⇒|→|->|-&gt;)\s*"
    r"(?P<after>[+-]?\d+(?:\.\d+)?)\s*(?P<unit_after>F|f|％|%|本|バー|bars?|bar)?"
)


def title_mismatch(page_title: str, selector_title: str) -> str:
    return str(page_title != selector_title).lower()


def strip_html(value: str) -> str:
    text = re.sub(r"<\s*br\s*/?\s*>", " ", value, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_target(value: str) -> str:
    text = strip_html(value).lower()
    text = re.sub(r"\s+", "", text)
    text = text.replace("（", "(").replace("）", ")")
    return text


def scope_for_section(section_type: str) -> str:
    if section_type == "policy":
        return "system"
    if section_type == "common":
        return "common"
    if section_type == "fighter":
        return "fighter"
    return "unknown"


def target_title_for_row(row: dict[str, str]) -> str:
    if row["section_type"] == "fighter":
        return strip_html(row["detail_title"])
    if row["section_type"] == "common":
        return strip_html(row["common_title"])
    return strip_html(row["policy_title"] or row["version_title"])


def normalized_target_key(row: dict[str, str]) -> str:
    target = normalize_target(target_title_for_row(row))
    if row["section_type"] == "fighter":
        fighter = row["fighter_tool_name"] or normalize_target(row["fighter_alpha"] or row["fighter_id"])
        return f"{canonical_character_slug(fighter)}::{target}"
    return f"{scope_for_section(row['section_type'])}::{target}"


def event_id_for_row(row: dict[str, str]) -> str:
    section_order = row["section_order"] or "0"
    detail_order = row["detail_order"] or "0"
    body_order = row["body_order"] or "0"
    return f"official-battle-change:{row['version_id']}:{row['section_type']}:{section_order}:{detail_order}:{body_order}"


def extract_value_changes(text_plain: str) -> list[dict[str, str]]:
    changes: list[dict[str, str]] = []
    for match in VALUE_CHANGE_RE.finditer(text_plain):
        unit = match.group("unit_after") or match.group("unit_before") or ""
        context = match.group("context").strip(" ：:、。を")
        changes.append(
            {
                "before": f"{match.group('before')}{match.group('unit_before') or unit}",
                "after": f"{match.group('after')}{match.group('unit_after') or unit}",
                "unit": unit,
                "context": context,
            }
        )
    return changes


def classify_change_types(row: dict[str, str], value_changes: list[dict[str, str]], text_plain: str) -> list[str]:
    haystack = " ".join(
        [
            text_plain,
            strip_html(row["category"]),
            target_title_for_row(row),
            strip_html(row["common_title"]),
            strip_html(row["policy_title"]),
        ]
    ).lower()
    types: set[str] = set()

    if any("硬直差" in item["context"] or "有利" in item["context"] or "不利" in item["context"] for item in value_changes):
        types.add("frame_advantage")
    if re.search(r"発生|startup|攻撃発生", haystack):
        types.add("startup")
    if re.search(r"攻撃持続|持続|active", haystack):
        types.add("active")
    if "frame_advantage" not in types and re.search(r"硬直|recovery", haystack) and value_changes:
        types.add("recovery")
    if re.search(r"キャンセル|cancel", haystack):
        types.add("cancel")
    if re.search(r"ジャグル|juggle|追撃|空中コンボ|リミット", haystack):
        types.add("juggle")
    if re.search(r"攻撃判定|判定|hitbox|やられ判定|hurtbox|押し合い判定|collision", haystack):
        types.add("hitbox_hurtbox")
    if re.search(r"ドライブゲージ|drive gauge|drive", haystack):
        types.add("drive_gauge")
    if re.search(r"saゲージ|super gauge|super art|スーパーゲージ", haystack):
        types.add("super_gauge")
    if re.search(r"ダメージ|damage", haystack):
        types.add("damage")
    if re.search(r"不具合|修正|bug|fix|fixed", haystack):
        types.add("bugfix")
    if value_changes and not types:
        types.add("numeric_change")
    if not types:
        types.add("textual_change")
    return sorted(types)


def confidence_for_event(value_changes: list[dict[str, str]], change_types: list[str]) -> str:
    if value_changes:
        return "numeric_explicit"
    if change_types == ["textual_change"]:
        return "related_only"
    return "textual_direct"


def build_change_events(change_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for row in change_rows:
        text_plain = strip_html(row["text_html"])
        value_changes = extract_value_changes(text_plain)
        change_types = classify_change_types(row, value_changes, text_plain)
        events.append(
            {
                "event_id": event_id_for_row(row),
                "source_authority": "official",
                "version_order": row["version_order"],
                "version_id": row["version_id"],
                "version_title": row["version_title"],
                "version_selector_title": row["version_selector_title"],
                "section_type": row["section_type"],
                "scope": scope_for_section(row["section_type"]),
                "section_order": row["section_order"],
                "body_order": row["body_order"],
                "fighter_order": row["fighter_order"],
                "fighter_id": row["fighter_id"],
                "fighter_alpha": row["fighter_alpha"],
                "fighter_tool_name": row["fighter_tool_name"],
                "fighter_url_name": row["fighter_url_name"],
                "character_slug": canonical_character_slug(row["fighter_tool_name"]) if row["section_type"] == "fighter" else "",
                "detail_order": row["detail_order"],
                "target_title": target_title_for_row(row),
                "normalized_target_key": normalized_target_key(row),
                "category": row["category"],
                "change_types": change_types,
                "confidence": confidence_for_event(value_changes, change_types),
                "value_changes": value_changes,
                "text_plain": text_plain,
                "text_html": row["text_html"],
                "data_json_path": row["data_json_path"],
            }
        )
    return events


def build_move_change_index(events: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for event in events:
        key = event["normalized_target_key"]
        if key not in grouped:
            grouped[key] = {
                "normalized_target_key": key,
                "scope": event["scope"],
                "fighter_tool_name": event["fighter_tool_name"],
                "fighter_alpha": event["fighter_alpha"],
                "character_slug": event["character_slug"],
                "target_title": event["target_title"],
                "event_count": 0,
                "numeric_explicit_event_count": 0,
                "version_ids": [],
                "event_ids": [],
                "source_authorities": [],
                "data_json_paths": [],
                "change_types": [],
            }
        item = grouped[key]
        item["event_count"] += 1
        if event["confidence"] == "numeric_explicit":
            item["numeric_explicit_event_count"] += 1
        if event["version_id"] not in item["version_ids"]:
            item["version_ids"].append(event["version_id"])
        item["event_ids"].append(event["event_id"])
        if event["source_authority"] not in item["source_authorities"]:
            item["source_authorities"].append(event["source_authority"])
        if event["data_json_path"] not in item["data_json_paths"]:
            item["data_json_paths"].append(event["data_json_path"])
        item["change_types"] = sorted(set(item["change_types"]) | set(event["change_types"]))

    rows = list(grouped.values())
    return {
        "schema_version": "capcom_battle_change_move_change_index/v1",
        "source_manifest": "raw/battle-change/official/manifest.json",
        "source_events": "wiki/outputs/data/battle-change/official/change-events.json",
        "fields": MOVE_CHANGE_INDEX_FIELDS,
        "row_count": len(rows),
        "rows": rows,
    }


def blank_row(
    version_order: int,
    adjust: dict[str, Any],
    section_type: str,
    data_json_path: str,
    version_selector_title: str,
) -> dict[str, str]:
    version_title = str(adjust["title"])
    return {
        "version_order": str(version_order),
        "version_id": str(adjust["current_version"]),
        "version_title": version_title,
        "version_selector_title": version_selector_title,
        "version_title_mismatch": title_mismatch(version_title, version_selector_title),
        "section_type": section_type,
        "section_order": "",
        "body_order": "",
        "policy_title": "",
        "common_title": "",
        "fighter_order": "",
        "fighter_id": "",
        "fighter_alpha": "",
        "fighter_tool_name": "",
        "fighter_url_name": "",
        "detail_order": "",
        "detail_title": "",
        "category": "",
        "text_html": "",
        "data_json_path": data_json_path,
    }


def flatten_adjust(
    version_order: int,
    adjust: dict[str, Any],
    data_json_path: str,
    version_selector_title: str | None = None,
) -> list[dict[str, str]]:
    validate_adjust_payload(adjust, expected_version=adjust.get("current_version"))
    selector_title = version_selector_title if version_selector_title is not None else str(adjust["title"])
    rows: list[dict[str, str]] = []

    for policy_index, item in enumerate(adjust.get("policy", []), start=1):
        row = blank_row(version_order, adjust, "policy", data_json_path, selector_title)
        row.update(
            {
                "section_order": str(policy_index),
                "policy_title": str(item.get("title", "")),
                "text_html": str(item.get("text", "")),
            }
        )
        rows.append(row)

    for common_index, section in enumerate(adjust.get("common", []), start=1):
        for body_index, body in enumerate(section.get("body", []), start=1):
            row = blank_row(version_order, adjust, "common", data_json_path, selector_title)
            row.update(
                {
                    "section_order": str(common_index),
                    "body_order": str(body_index),
                    "common_title": str(section.get("title", "")),
                    "category": str(body.get("category", "")),
                    "text_html": str(body.get("text", "")),
                }
            )
            rows.append(row)

    for fighter_index, fighter in enumerate(adjust.get("fighter", []), start=1):
        for detail_index, detail in enumerate(fighter.get("detail", []), start=1):
            for body_index, body in enumerate(detail.get("body", []), start=1):
                row = blank_row(version_order, adjust, "fighter", data_json_path, selector_title)
                row.update(
                    {
                        "section_order": str(fighter_index),
                        "body_order": str(body_index),
                        "fighter_order": str(fighter_index),
                        "fighter_id": str(fighter.get("fighter_id", "")),
                        "fighter_alpha": str(fighter.get("fighter_alpha", "")),
                        "fighter_tool_name": str(fighter.get("fighter_tool_name", "")),
                        "fighter_url_name": str(fighter.get("fighter_url_name", "")),
                        "detail_order": str(detail_index),
                        "detail_title": str(detail.get("title", "")),
                        "category": str(body.get("category", "")),
                        "text_html": str(body.get("text", "")),
                    }
                )
                rows.append(row)

    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_all(repo_root: Path) -> dict[str, Any]:
    raw_root = repo_root / "raw" / "battle-change" / "official"
    manifest_path = raw_root / "manifest.json"
    manifest = read_json(manifest_path)
    output_dir = repo_root / "wiki" / "outputs" / "data" / "battle-change" / "official"

    version_rows: list[dict[str, str]] = []
    change_rows: list[dict[str, str]] = []
    selector_titles = {
        str(version["id"]): str(version["title"])
        for version in manifest["versions"]
    }
    for version_order, capture in enumerate(manifest["captures"], start=1):
        data_json_path = repo_relative_path(repo_root, capture["data_json"])
        payload = read_json(data_json_path)
        adjust = adjust_from_payload(payload)
        summary = validate_adjust_payload(adjust, expected_version=capture["version_id"])
        selector_title = selector_titles.get(capture["version_id"], summary["title"])
        version_rows.append(
            {
                "version_order": str(version_order),
                "version_id": summary["version_id"],
                "version_title": summary["title"],
                "version_selector_title": selector_title,
                "version_title_mismatch": title_mismatch(summary["title"], selector_title),
                "policy_count": str(summary["policy_count"]),
                "common_section_count": str(summary["common_section_count"]),
                "common_change_count": str(summary["common_change_count"]),
                "fighter_count": str(summary["fighter_count"]),
                "fighter_detail_count": str(summary["fighter_detail_count"]),
                "fighter_change_count": str(summary["fighter_change_count"]),
                "data_json_path": capture["data_json"],
            }
        )
        change_rows.extend(
            flatten_adjust(
                version_order,
                adjust,
                capture["data_json"],
                version_selector_title=selector_title,
            )
        )

    change_events = build_change_events(change_rows)
    move_change_index = build_move_change_index(change_events)

    schema = {
        "schema_version": "capcom_battle_change_derived_outputs/v2",
        "source_manifest": "raw/battle-change/official/manifest.json",
        "files": {
            "versions": "versions.json",
            "changes": "changes.json",
            "change_events": "change-events.json",
            "move_change_index": "move-change-index.json",
        },
        "changes_fields": CHANGE_FIELDS,
        "change_event_fields": CHANGE_EVENT_FIELDS,
        "move_change_index_fields": MOVE_CHANGE_INDEX_FIELDS,
        "version_fields": list(version_rows[0].keys()) if version_rows else [],
        "notes": [
            "`version_title` is the per-version page title from that version's data JSON.",
            "`version_selector_title` is the title from the discovery page version selector.",
            "`version_title_mismatch` is true when those two official title strings differ.",
            "`text_html` preserves official HTML fragments such as <br>, span, and class attributes.",
            "Rows are derived from raw `_next/data` JSON, not translated or normalized source replacements.",
            "`change-events.json` is a shallow query index over official rows; it preserves official text and adds heuristic `change_types`, extracted explicit numeric before/after values, and confidence labels.",
            "`fighter_tool_name` preserves the official Battle Change source key. `character_slug` is the canonical frame-data join key, including source-name variants such as `gouki` -> `gouki_akuma`, `honda` -> `ehonda`, and `vega` -> `vega_mbison`.",
            "`move-change-index.json` groups change events by fighter and target title for cause-finding queries; it is an index, not a replacement for official source text.",
            "`move-change-index.json` keeps `version_ids` as an insertion-order unique update list; per-event rows are represented by `event_ids`.",
        ],
    }

    write_json(
        output_dir / "versions.json",
        {
            "schema_version": "capcom_battle_change_versions/v2",
            "source_manifest": "raw/battle-change/official/manifest.json",
            "fields": list(version_rows[0].keys()) if version_rows else [],
            "row_count": len(version_rows),
            "rows": version_rows,
        },
    )
    write_json(
        output_dir / "changes.json",
        {
            "schema_version": "capcom_battle_change_changes/v2",
            "source_manifest": "raw/battle-change/official/manifest.json",
            "fields": CHANGE_FIELDS,
            "row_count": len(change_rows),
            "rows": change_rows,
        },
    )
    write_json(
        output_dir / "change-events.json",
        {
            "schema_version": "capcom_battle_change_change_events/v1",
            "source_manifest": "raw/battle-change/official/manifest.json",
            "source_changes": "wiki/outputs/data/battle-change/official/changes.json",
            "fields": CHANGE_EVENT_FIELDS,
            "row_count": len(change_events),
            "rows": change_events,
        },
    )
    write_json(output_dir / "move-change-index.json", move_change_index)
    write_json(output_dir / "schema.json", schema)
    return {
        "output_dir": output_dir.relative_to(repo_root).as_posix(),
        "version_count": len(version_rows),
        "change_count": len(change_rows),
        "change_event_count": len(change_events),
        "move_change_index_count": move_change_index["row_count"],
        "policy_count": sum(1 for row in change_rows if row["section_type"] == "policy"),
        "common_change_count": sum(1 for row in change_rows if row["section_type"] == "common"),
        "fighter_change_count": sum(1 for row in change_rows if row["section_type"] == "fighter"),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = extract_all(args.repo_root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
