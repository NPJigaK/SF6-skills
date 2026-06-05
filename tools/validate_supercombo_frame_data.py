#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from capture_supercombo_frame_data import cargo_records, sha256_file, write_json


DISPLAY_TABLES = {
    "Normals and Target Combos": {
        "move_types": {"ground_normal", "normal", "air_normal", "serenity_stream"},
        "tabs": {
            "General": [
                ("input", "input"),
                ("Damage", "damage"),
                ("Startup", "startup"),
                ("Active", "active"),
                ("Recovery", "recovery"),
                ("Total", "total"),
                ("Hit Adv", "hitAdv"),
                ("Block Adv", "blockAdv"),
                ("Guard", "guard"),
                ("Cancel", "cancel"),
                ("Hitconfirm", "hitconfirm"),
            ],
            "Details": [
                ("input", "input"),
                ("Dmg Scaling", "dmgScaling"),
                ("Punish Adv", "punishAdv"),
                ("PerfParry Adv", "perfParryAdv"),
                ("DR Cancel onHit", "DRcancelHit"),
                ("DR Cancel onBlock", "DRcancelBlk"),
                ("After DR onHit", "afterDRHit"),
                ("After DR onBlock", "afterDRBlk"),
                ("Hitstun", "hitstun"),
                ("Blockstun", "blockstun"),
                ("Hitstop", "hitstop"),
            ],
            "Meter": [
                ("input", "input"),
                ("DriveDmg Block", "driveDmgBlk"),
                ("DriveDmg Hit[PC]", "driveDmgHit"),
                ("Drive Gain", "driveGain"),
                ("SuperGain Hit", "superGainHit"),
                ("SuperGain Block", "superGainBlk"),
            ],
            "Properties": [
                ("input", "input"),
                ("Invuln", "invuln"),
                ("Armor", "armor"),
                ("Airborne", "airborne"),
                ("Range", "atkRange"),
                ("Juggle Start", "jugStart"),
                ("Juggle Increase", "jugIncrease"),
                ("Juggle Limit", "jugLimit"),
            ],
            "Notes": [("input", "input"), ("Notes", "notes")],
        },
    },
    "Drive and Throw": {
        "move_types": {"drive", "throw"},
        "tabs": {
            "General": [
                ("input", "input"),
                ("Damage", "damage"),
                ("Startup", "startup"),
                ("Active", "active"),
                ("Recovery", "recovery"),
                ("Total", "total"),
                ("Hit Adv", "hitAdv"),
                ("Block Adv", "blockAdv"),
                ("Guard", "guard"),
            ],
            "Details": [
                ("input", "input"),
                ("Chip", "chip"),
                ("Dmg Scaling", "dmgScaling"),
                ("Punish Adv", "punishAdv"),
                ("PerfParry Adv", "perfParryAdv"),
                ("Blockstun", "blockstun"),
                ("Hitstop", "hitstop"),
            ],
            "Meter": [
                ("input", "input"),
                ("DriveDmg Block", "driveDmgBlk"),
                ("DriveDmg Hit[PC]", "driveDmgHit"),
                ("Drive Gain", "driveGain"),
                ("SuperGain Hit", "superGainHit"),
            ],
            "Properties": [
                ("input", "input"),
                ("Invuln", "invuln"),
                ("Armor", "armor"),
                ("Range", "atkRange"),
                ("Juggle Start", "jugStart"),
                ("Juggle Increase", "jugIncrease"),
                ("Juggle Limit", "jugLimit"),
            ],
            "Notes": [("input", "input"), ("Notes", "notes")],
        },
    },
    "Specials": {
        "move_types": {"special"},
        "tabs": {
            "General": [
                ("input", "input"),
                ("Damage", "damage"),
                ("Startup", "startup"),
                ("Active", "active"),
                ("Recovery", "recovery"),
                ("Total", "total"),
                ("Hit Adv", "hitAdv"),
                ("Block Adv", "blockAdv"),
                ("Guard", "guard"),
                ("Cancel", "cancel"),
                ("Hitconfirm", "hitconfirm"),
            ],
            "Details": [
                ("input", "input"),
                ("Chip", "chip"),
                ("Dmg Scaling", "dmgScaling"),
                ("Punish Adv", "punishAdv"),
                ("PerfParry Adv", "perfParryAdv"),
                ("Blockstun", "blockstun"),
                ("Hitstop", "hitstop"),
            ],
            "Meter": [
                ("input", "input"),
                ("DriveDmg Block", "driveDmgBlk"),
                ("DriveDmg Hit[PC]", "driveDmgHit"),
                ("Drive Gain", "driveGain"),
                ("SuperGain Hit", "superGainHit"),
                ("SuperGain Block", "superGainBlk"),
            ],
            "Properties": [
                ("input", "input"),
                ("Invuln", "invuln"),
                ("Armor", "armor"),
                ("Airborne", "airborne"),
                ("Range", "atkRange"),
                ("Juggle Start", "jugStart"),
                ("Juggle Increase", "jugIncrease"),
                ("Juggle Limit", "jugLimit"),
            ],
            "Notes": [("input", "input"), ("Notes", "notes")],
        },
    },
    "Supers": {
        "move_types": {"super"},
        "tabs": {
            "General": [
                ("input", "input"),
                ("Damage", "damage"),
                ("Startup", "startup"),
                ("Active", "active"),
                ("Recovery", "recovery"),
                ("Total", "total"),
                ("Hit Adv", "hitAdv"),
                ("Block Adv", "blockAdv"),
                ("Guard", "guard"),
            ],
            "Details": [
                ("input", "input"),
                ("Chip", "chip"),
                ("Dmg Scaling", "dmgScaling"),
                ("Punish Adv", "punishAdv"),
                ("PerfParry Adv", "perfParryAdv"),
                ("Blockstun", "blockstun"),
                ("Hitstop", "hitstop"),
            ],
            "Meter": [
                ("input", "input"),
                ("DriveDmg Block", "driveDmgBlk"),
                ("DriveDmg Hit[PC]", "driveDmgHit"),
                ("SuperGain Hit", "superGainHit"),
                ("SuperGain Block", "superGainBlk"),
            ],
            "Properties": [
                ("input", "input"),
                ("Invuln", "invuln"),
                ("Armor", "armor"),
                ("Airborne", "airborne"),
                ("Range", "atkRange"),
                ("Juggle Start", "jugStart"),
                ("Juggle Increase", "jugIncrease"),
                ("Juggle Limit", "jugLimit"),
            ],
            "Notes": [("input", "input"), ("Notes", "notes")],
        },
    },
}
DISPLAY_ROWS_PER_PAGE = 50


def normalized_move_type(value: Any) -> str:
    return str(value or "").strip().lower()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collapse_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def template_to_text(match: re.Match[str]) -> str:
    inner = match.group(1)
    parts = inner.split("|")
    name = parts[0].strip()
    args = [part.strip() for part in parts[1:]]
    if not args:
        return ""
    if name in {"sf6-adv", "clr"}:
        return args[-1]
    if name in {"tt", "tooltip"}:
        return args[0]
    return args[-1]


def strip_mediawiki_list_markers(text: str, *, field_name: str) -> str:
    if field_name == "notes" and re.fullmatch(r"\*[^*\n].*\*", text.strip()):
        return text
    return re.sub(r"(?m)^\*+\s*", "", text)


def wiki_to_text(value: str, *, field_name: str = "") -> str:
    if not value:
        return ""
    value = value.strip()
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    value = strip_mediawiki_list_markers(value, field_name=field_name)
    value = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    for _ in range(12):
        new_value = re.sub(r"\{\{([^{}]+)\}\}", template_to_text, value)
        if new_value == value:
            break
        value = new_value
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("'''", "").replace("''", "")
    return collapse_ws(html.unescape(value))


def display_value(record: dict[str, Any], field: str) -> str:
    value = str(record.get(field, "")).strip()
    if not value or value == f"{{{{{{{field}}}}}}}":
        return ""
    return wiki_to_text(value, field_name=field)


def frame_records_for_section(frames: list[dict[str, Any]], section: str) -> list[dict[str, Any]]:
    move_types = DISPLAY_TABLES[section]["move_types"]
    return [record for record in frames if normalized_move_type(record.get("moveType", "")) in move_types]


def expected_table(frames: list[dict[str, Any]], section: str, tab: str) -> dict[str, Any]:
    columns = DISPLAY_TABLES[section]["tabs"][tab]
    records = frame_records_for_section(frames, section)
    return {
        "headers": [label for label, _field in columns],
        "rows": [
            [display_value(record, field) for _label, field in columns]
            for record in records
        ],
        "moveIds": [str(record.get("moveId", "")) for record in records],
    }


def data_rows(table: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.get("rows", []):
        cells = row.get("cells", [])
        if len(cells) > 1:
            rows.append([collapse_ws(str(cell.get("text", ""))) for cell in cells])
    return rows


def validate_capture(root: Path, *, expected_frame_count: int | None) -> dict[str, Any]:
    manifest = read_json(root / "manifest.json")
    metadata = read_json(root / "metadata.json")
    templates = read_json(root / "data.templates.json")
    display_queries = read_json(root / "frame-data.cargo-queries.json")["queries"]
    frame_cargo = cargo_records(read_json(root / "cargo" / "frame-data.json"))
    character_cargo = cargo_records(read_json(root / "cargo" / "character-data.json"))
    rendered = read_json(root / "rendered" / "tables.dom.json")
    imageinfo = read_json(root / "imageinfo.json")
    image_manifest = read_json(root / "image-manifest.json")
    page_metadata = read_json(root / "api" / "page-metadata.json")

    character_templates = templates["character"]
    frame_templates = templates["frames"]
    failures: list[str] = []
    warnings: list[str] = []
    table_comparisons: list[dict[str, Any]] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(len(character_templates) == 1, f"expected 1 CharacterData-SF6 template, got {len(character_templates)}")
    if expected_frame_count is not None:
        require(
            len(frame_templates) == expected_frame_count,
            f"expected {expected_frame_count} FrameData-SF6 templates, got {len(frame_templates)}",
        )
    require(len(display_queries) == 21, f"expected 21 display Cargo queries, got {len(display_queries)}")
    require(len(frame_cargo) == len(frame_templates), "Cargo frame row count differs from raw FrameData-SF6 count")
    require(len(character_cargo) == len(character_templates), "Cargo character row count differs from raw CharacterData-SF6 count")
    require(not page_metadata.get("error"), f"page metadata API returned error: {page_metadata.get('error')}")
    require(
        len(page_metadata.get("query", {}).get("pages", [])) == 2,
        "page metadata API should contain Data and Frame_data pages",
    )

    raw_move_ids = [str(record.get("moveId", "")) for record in frame_templates]
    cargo_move_ids = [str(record.get("moveId", "")) for record in frame_cargo]
    require(raw_move_ids == cargo_move_ids, "raw FrameData-SF6 moveId order differs from Cargo _rowID order")

    move_type_counts = Counter(normalized_move_type(record.get("moveType", "")) for record in frame_templates)
    duplicate_inputs = {
        input_value: [record.get("moveId", "") for record in records]
        for input_value, records in group_by(frame_templates, "input").items()
        if input_value and len(records) > 1
    }

    tab_states = rendered.get("tab_states", [])
    require(len(tab_states) == 5, f"expected 5 rendered tab states, got {len(tab_states)}")
    for state in tab_states:
        tab = state.get("tab")
        screenshot = root / state.get("screenshot", {}).get("path", "")
        require(screenshot.exists(), f"missing screenshot for tab {tab}: {screenshot}")
        if screenshot.exists():
            require(sha256_file(screenshot) == state["screenshot"]["sha256"], f"screenshot sha mismatch for {tab}")
        require(state.get("iframe_count_after_cleanup") == 0, f"{tab} screenshot state has visible iframe count")
        require(state.get("ad_visible_count_after_cleanup") == 0, f"{tab} screenshot state has visible ad count")
        require(state.get("clicked_tab_controls") == 4, f"{tab} clicked {state.get('clicked_tab_controls')} tab controls, expected 4")
        active_sections = state.get("active_sections", [])
        require(len(active_sections) == 4, f"{tab} expected 4 active sections, got {len(active_sections)}")
        for active in active_sections:
            section = active.get("heading", "")
            table = active.get("table") or {}
            if section not in DISPLAY_TABLES or tab not in DISPLAY_TABLES[section]["tabs"]:
                failures.append(f"unexpected rendered section/tab: {section}/{tab}")
                continue
            expected = expected_table(frame_templates, section, tab)
            actual_headers = table.get("headers", [])
            actual_rows = data_rows(table)
            pagination_limited = len(expected["rows"]) > len(actual_rows) == DISPLAY_ROWS_PER_PAGE
            expected_rows_for_dom = expected["rows"][: len(actual_rows)] if pagination_limited else expected["rows"]
            comparison: dict[str, Any] = {
                "section": section,
                "tab": tab,
                "expected_rows": len(expected["rows"]),
                "actual_rows": len(actual_rows),
                "compared_rows": len(expected_rows_for_dom),
                "pagination_limited": pagination_limited,
                "header_match": actual_headers == expected["headers"],
                "row_count_match": len(actual_rows) == len(expected["rows"]) or pagination_limited,
                "input_order_match": [row[0] for row in actual_rows] == [row[0] for row in expected_rows_for_dom],
                "cell_mismatches": [],
                "note_mismatches": [],
            }
            if actual_headers != expected["headers"]:
                failures.append(f"{section}/{tab} headers differ: {actual_headers!r} != {expected['headers']!r}")
            if pagination_limited:
                warnings.append(
                    f"{section}/{tab} rendered table is paginated; compared first {len(actual_rows)} of {len(expected['rows'])} rows"
                )
            elif len(actual_rows) != len(expected["rows"]):
                failures.append(f"{section}/{tab} row count differs: {len(actual_rows)} != {len(expected['rows'])}")
            if [row[0] for row in actual_rows] != [row[0] for row in expected_rows_for_dom]:
                failures.append(f"{section}/{tab} input order differs")
            for row_index, (actual_row, expected_row) in enumerate(zip(actual_rows, expected_rows_for_dom, strict=False), start=1):
                for cell_index, (actual_cell, expected_cell) in enumerate(zip(actual_row, expected_row, strict=False), start=1):
                    if actual_cell == expected_cell:
                        continue
                    label = expected["headers"][cell_index - 1] if cell_index <= len(expected["headers"]) else str(cell_index)
                    mismatch = {
                        "row_index": row_index,
                        "cell_index": cell_index,
                        "header": label,
                        "actual": actual_cell,
                        "expected": expected_cell,
                    }
                    if label == "Notes":
                        comparison["note_mismatches"].append(mismatch)
                    else:
                        comparison["cell_mismatches"].append(mismatch)
            if comparison["cell_mismatches"]:
                failures.append(
                    f"{section}/{tab} has {len(comparison['cell_mismatches'])} non-note cell mismatches"
                )
            if comparison["note_mismatches"]:
                warnings.append(
                    f"{section}/{tab} has {len(comparison['note_mismatches'])} note text normalization mismatches"
                )
            comparison["cell_mismatches"] = comparison["cell_mismatches"][:20]
            comparison["note_mismatches"] = comparison["note_mismatches"][:20]
            table_comparisons.append(comparison)

    image_downloads = image_manifest.get("downloads", [])
    failed_downloads = [item for item in image_downloads if not item.get("ok")]
    if failed_downloads:
        warnings.append(f"{len(failed_downloads)} resolved image downloads failed")
    if imageinfo.get("missing_count"):
        warnings.append(f"{imageinfo.get('missing_count')} imageinfo titles are missing")

    result = {
        "validation_schema_version": "supercombo_frame_capture_validation/v1",
        "validated_at_utc": utc_now(),
        "raw_root": str(root),
        "capture_label": manifest.get("capture_label"),
        "source_revision": manifest.get("source_revision"),
        "storage_policy": manifest.get("storage_policy", "latest_frame_data_mirror"),
        "status": "passed" if not failures else "failed",
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "character_templates": len(character_templates),
            "frame_templates": len(frame_templates),
            "display_cargo_queries": len(display_queries),
            "cargo_frame_rows": len(frame_cargo),
            "cargo_character_rows": len(character_cargo),
            "move_type_counts": dict(sorted(move_type_counts.items())),
            "duplicate_inputs": duplicate_inputs,
            "rendered_tab_states": len(tab_states),
            "table_comparisons": len(table_comparisons),
            "image_refs": len(image_manifest.get("refs", [])),
            "imageinfo_resolved": imageinfo.get("resolved_count"),
            "imageinfo_missing": imageinfo.get("missing_count"),
            "downloaded_images": sum(1 for item in image_downloads if item.get("ok")),
            "failed_image_downloads": len(failed_downloads),
        },
        "table_comparisons": table_comparisons,
    }
    return result


def group_by(records: list[dict[str, Any]], field: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(str(record.get(field, "")), []).append(record)
    return grouped


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", help="Deprecated; frame-data raw uses fixed latest paths.")
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--expected-frame-count", type=int)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo_root / "raw" / "frame-data" / "supercombo" / args.character_slug
    result = validate_capture(root, expected_frame_count=args.expected_frame_count)
    write_json(root / "validation.json", result)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    if result["failures"]:
        for failure in result["failures"]:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
