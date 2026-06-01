#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


FIELD_MAP = [
    ("damage", "damage"),
    ("startup", "startup"),
    ("active", "active"),
    ("recovery", "recovery"),
    ("total", "total"),
    ("hit_advantage", "hitAdv"),
    ("block_advantage", "blockAdv"),
    ("guard", "guard"),
    ("cancel", "cancel"),
    ("hitconfirm", "hitconfirm"),
    ("chip", "chip"),
    ("damage_scaling", "dmgScaling"),
    ("punish_advantage", "punishAdv"),
    ("perfect_parry_advantage", "perfParryAdv"),
    ("drive_rush_cancel_on_hit", "DRcancelHit"),
    ("drive_rush_cancel_on_block", "DRcancelBlk"),
    ("after_drive_rush_on_hit", "afterDRHit"),
    ("after_drive_rush_on_block", "afterDRBlk"),
    ("hitstun", "hitstun"),
    ("blockstun", "blockstun"),
    ("hitstop", "hitstop"),
    ("drive_damage_block", "driveDmgBlk"),
    ("drive_damage_hit", "driveDmgHit"),
    ("drive_gain", "driveGain"),
    ("super_gain_hit", "superGainHit"),
    ("super_gain_block", "superGainBlk"),
    ("invuln", "invuln"),
    ("armor", "armor"),
    ("airborne", "airborne"),
    ("attack_range", "atkRange"),
    ("range_notes", "rangeNotes"),
    ("juggle_start", "jugStart"),
    ("juggle_increase", "jugIncrease"),
    ("juggle_limit", "jugLimit"),
    ("projectile_speed", "projSpeed"),
    ("pushback_hit", "pushbackHit"),
    ("pushback_block", "pushbackBlk"),
    ("images", "images"),
    ("hitboxes", "hitboxes"),
    ("notes", "notes"),
]

FRAME_CSV_FIELDS = [
    "row_order",
    "section",
    "move_type",
    "move_id",
    "input",
    "name",
    *[display_name for display_name, _raw_name in FIELD_MAP],
]

CHARACTER_CSV_FIELDS = [
    "row_order",
    "chara",
    "name",
    "hp",
    "throw_range",
    "throw_hurtbox",
    "forward_walk_speed",
    "back_walk_speed",
    "forward_dash_speed",
    "back_dash_speed",
    "forward_dash_distance",
    "back_dash_distance",
    "jump_speed",
    "jump_apex",
    "forward_jump_distance",
    "back_jump_distance",
    "drive_rush_min",
    "drive_rush_block",
    "drive_rush_max",
    "portrait",
    "icon",
]

CHARACTER_FIELD_MAP = [
    ("chara", "chara"),
    ("name", "name"),
    ("hp", "hp"),
    ("throw_range", "throwRange"),
    ("throw_hurtbox", "throwHurtbox"),
    ("forward_walk_speed", "fwdWalkSpd"),
    ("back_walk_speed", "bwdWalkSpd"),
    ("forward_dash_speed", "fwdDashSpd"),
    ("back_dash_speed", "bwdDashSpd"),
    ("forward_dash_distance", "fwdDashDist"),
    ("back_dash_distance", "bwdDashDist"),
    ("jump_speed", "jumpSpd"),
    ("jump_apex", "jumpApex"),
    ("forward_jump_distance", "fwdJumpDist"),
    ("back_jump_distance", "bwdJumpDist"),
    ("drive_rush_min", "dRushMin"),
    ("drive_rush_block", "dRushBlock"),
    ("drive_rush_max", "dRushMax"),
    ("portrait", "portrait"),
    ("icon", "icon"),
]

IMAGE_TOKEN_TO_COMMAND = {
    "key-d": "2",
    "key-dr": "3",
    "key-r": "6",
    "key-dl": "1",
    "key-l": "4",
    "key-nutral": "5",
    "key-plus": "",
    "key-or": "/",
    "arrow_3": "~",
    "icon_punch_l": "LP",
    "icon_punch_m": "MP",
    "icon_punch_h": "HP",
    "icon_punch": "P",
    "icon_kick_l": "LK",
    "icon_kick_m": "MK",
    "icon_kick_h": "HK",
    "icon_kick": "K",
}

SOURCE_SECTIONS = {
    "ground_normal": "Normals and Target Combos",
    "normal": "Normals and Target Combos",
    "air_normal": "Normals and Target Combos",
    "drive": "Drive and Throw",
    "throw": "Drive and Throw",
    "special": "Specials",
    "super": "Supers",
    "taunt": "Taunts",
}

OFFICIAL_CATEGORY_TO_MOVE_TYPES = {
    "通常技": {"ground_normal", "air_normal", "normal"},
    "特殊技": {"ground_normal", "normal"},
    "必殺技": {"special"},
    "スーパーアーツ": {"super"},
    "通常投げ": {"throw"},
    "共通システム": {"drive"},
}

JP_NAME_OVERRIDES = {
    "ヴィーハト・アクノ": "jp_214p_214lp_mp",
    "ヴィーハト・チェーニ": "jp_214p_214hp",
    "パリィドライブラッシュ": "jp_mpmk_66_pdr",
    "キャンセルドライブラッシュ": "jp_mpmk_66_drc",
}

RYU_NAME_OVERRIDES = {
    "[電刃錬気]波動拳": "ryu_236p(charged)",
    "[電刃錬気]OD 波動拳": "ryu_236pp(charged)",
    "[電刃錬気]波掌撃": "ryu_214p(charged)",
    "[電刃錬気]SA1 真空波動拳": "ryu_236236p_denjin",
    "SA2 真波掌撃（Lv2）": "ryu_214214p_lv2",
    "SA2 真波掌撃（Lv3）": "ryu_214214p_lv3",
    "[電刃錬気]SA2 真波掌撃（Lv2）": "ryu_214214p_denjin_lv2",
    "[電刃錬気]SA2 真波掌撃（Lv3）": "ryu_214214p_denjin_lv3",
}

GENERIC_NAME_OVERRIDE_PATTERNS = {
    "パリィドライブラッシュ": "{character_slug}_mpmk_66_pdr",
    "キャンセルドライブラッシュ": "{character_slug}_mpmk_66_drc",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


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


def wiki_to_text(value: Any, *, field_name: str = "") -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if field_name and text == f"{{{{{{{field_name}}}}}}}":
        return ""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    for _ in range(12):
        new_text = re.sub(r"\{\{([^{}]+)\}\}", template_to_text, text)
        if new_text == text:
            break
        text = new_text
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("'''", "").replace("''", "")
    return collapse_ws(html.unescape(text))


def normalized_move_type(value: Any) -> str:
    return str(value or "").strip().lower()


def section_for(record: dict[str, Any]) -> str:
    return SOURCE_SECTIONS.get(normalized_move_type(record.get("moveType", "")), "")


def frame_display_rows(frames: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, record in enumerate(frames, start=1):
        row = {
            "row_order": str(index),
            "section": section_for(record),
            "move_type": normalized_move_type(record.get("moveType", "")),
            "move_id": str(record.get("moveId", "")),
            "input": str(record.get("input", "")),
            "name": str(record.get("name", "")),
        }
        for display_name, raw_name in FIELD_MAP:
            row[display_name] = wiki_to_text(record.get(raw_name, ""), field_name=raw_name)
        rows.append(row)
    return rows


def frame_json_rows(frames: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, record in enumerate(frames, start=1):
        display = {display_name: wiki_to_text(record.get(raw_name, ""), field_name=raw_name) for display_name, raw_name in FIELD_MAP}
        raw = {raw_name: str(record.get(raw_name, "")) for _display_name, raw_name in FIELD_MAP}
        rows.append(
            {
                "row_order": index,
                "section": section_for(record),
                "move_type": normalized_move_type(record.get("moveType", "")),
                "move_id": str(record.get("moveId", "")),
                "input": str(record.get("input", "")),
                "name": str(record.get("name", "")),
                "display": display,
                "raw": raw,
                "template_sha256": record.get("_block_sha256", ""),
            }
        )
    return rows


def character_rows(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        row = {"row_order": str(index)}
        for display_name, raw_name in CHARACTER_FIELD_MAP:
            row[display_name] = wiki_to_text(record.get(raw_name, ""), field_name=raw_name)
        rows.append(row)
    return rows


def token_command_from_official(row: dict[str, str]) -> str:
    tokens = json.loads(row["input_token_json"])
    raw_parts: list[str] = []
    jump = any(token.get("type") == "text" and "ジャンプ中" in token.get("value", "") for token in tokens)
    for token in tokens:
        token_type = token.get("type")
        value = str(token.get("value", ""))
        if token_type == "image":
            command = IMAGE_TOKEN_TO_COMMAND.get(value, "")
            if command:
                raw_parts.append(command)
        elif token_type == "text":
            if value == row["move_name"] or value in {"弱", "中", "強"}:
                continue
            if value.startswith("（") or value.endswith("）") or "ガード方向" in value:
                continue
            if value.strip() in {"or", "OR"}:
                raw_parts.append("/")
    command = "".join(raw_parts)
    command = command.replace("+", "")
    command = re.sub(r"/+", "/", command)
    command = command.replace("5/6LPLK", "LPLK")
    if jump and command and not command.startswith("j."):
        command = "j." + command
    if row["category"] in {"通常技", "特殊技"} and re.match(r"^(?:LP|MP|HP|LK|MK|HK)", command):
        command = "5" + command
    return command


def input_family(command: str, category: str) -> str:
    if category in {"必殺技", "スーパーアーツ"}:
        command = re.sub(r"(?:LPMP|LPHP|MPHP|PP)$", "PP", command)
        command = re.sub(r"(?:LKMK|LKHK|MKHK|KK)$", "KK", command)
        command = re.sub(r"(?:LP|MP|HP)$", "P", command)
        command = re.sub(r"(?:LK|MK|HK)$", "K", command)
    return command


def simple_number(value: str) -> str:
    text = value.strip()
    if re.fullmatch(r"[+-]?\d+", text):
        return text
    return ""


def active_duration(value: str) -> str:
    text = value.strip()
    if re.fullmatch(r"\d+", text):
        return text
    match = re.fullmatch(r"(\d+)-(\d+)", text)
    if match:
        start, end = map(int, match.groups())
        if end >= start:
            return str(end - start + 1)
    return ""


def compare_fields(official: dict[str, str], supercombo: dict[str, str]) -> dict[str, Any]:
    comparisons = {
        "startup": (simple_number(official["startup"]), simple_number(supercombo["startup"])),
        "active_duration": (active_duration(official["active"]), active_duration(supercombo["active"])),
        "recovery": (simple_number(official["recovery"]), simple_number(supercombo["recovery"])),
        "damage": (simple_number(official["damage"]), simple_number(supercombo["damage"])),
    }
    result: dict[str, Any] = {}
    for field, (official_value, supercombo_value) in comparisons.items():
        if official_value and supercombo_value:
            result[field] = {
                "official": official_value,
                "supercombo": supercombo_value,
                "match": official_value == supercombo_value,
            }
    return result


def candidate_score(official: dict[str, str], candidate: dict[str, str], official_family: str) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    if candidate["input"] == official["official_input_signature"]:
        score += 50
        reasons.append("exact_input")
    if candidate["input"] == official_family:
        score += 35
        reasons.append("family_input")
    candidate_family = input_family(candidate["input"], official["official_category"])
    if candidate_family and candidate_family == official_family:
        score += 30
        reasons.append("same_family")
    if candidate["move_type"] in OFFICIAL_CATEGORY_TO_MOVE_TYPES.get(official["official_category"], set()):
        score += 10
        reasons.append("category_move_type")
    if "CA" in official["official_move_name"] and "ca" in candidate["move_id"].lower():
        score += 15
        reasons.append("ca_variant")
    if "SA3" in official["official_move_name"] and "ca" not in candidate["move_id"].lower():
        score += 5
        reasons.append("non_ca_variant")
    comparisons = compare_fields(official, candidate)
    for field, item in comparisons.items():
        if item["match"]:
            score += 3
            reasons.append(f"{field}_match")
    return score, reasons


def build_crosswalk(
    *,
    character_slug: str,
    official_rows: list[dict[str, str]],
    supercombo_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    crosswalk: list[dict[str, Any]] = []
    matched_supercombo: Counter[str] = Counter()
    supercombo_by_id = {row["move_id"]: row for row in supercombo_rows}

    for official_index, official_raw in enumerate(official_rows, start=1):
        official = {
            "official_row_order": str(official_index),
            "official_category": official_raw["category"],
            "official_move_name": official_raw["move_name"],
            "official_input_display": official_raw["input_raw_display"],
            "official_input_signature": token_command_from_official(official_raw),
            "startup": official_raw["startup"],
            "active": official_raw["active"],
            "recovery": official_raw["recovery"],
            "damage": official_raw["damage"],
            "on_hit": official_raw["on_hit"],
            "on_block": official_raw["on_block"],
            "cancel": official_raw["cancel"],
        }
        family = input_family(official["official_input_signature"], official["official_category"])
        override_move_id = ""
        override_source = ""
        if character_slug == "jp":
            for name_part, move_id in JP_NAME_OVERRIDES.items():
                if name_part in official["official_move_name"]:
                    override_move_id = move_id
                    override_source = "jp_name_override"
                    break
        elif character_slug == "ryu":
            override_move_id = RYU_NAME_OVERRIDES.get(official["official_move_name"], "")
            if override_move_id:
                override_source = "ryu_name_override"
        if not override_move_id:
            for name_part, move_id_pattern in GENERIC_NAME_OVERRIDE_PATTERNS.items():
                if name_part in official["official_move_name"]:
                    override_move_id = move_id_pattern.format(character_slug=character_slug)
                    override_source = "generic_name_override"
                    break
        if override_move_id and override_move_id in supercombo_by_id:
            eligible = [supercombo_by_id[override_move_id]]
            override = True
        else:
            eligible = [
            row
            for row in supercombo_rows
            if row["move_type"] in OFFICIAL_CATEGORY_TO_MOVE_TYPES.get(official["official_category"], set())
            and (
                row["input"] == official["official_input_signature"]
                or row["input"] == family
                or input_family(row["input"], official["official_category"]) == family
            )
            ]
            override = False
        scored = []
        for candidate in eligible:
            score, reasons = candidate_score(official, candidate, family)
            scored.append((score, reasons, candidate))
        scored.sort(key=lambda item: (-item[0], item[2]["row_order"], item[2]["move_id"]))

        if scored:
            best_score, reasons, best = scored[0]
            top_ties = [item for item in scored if item[0] == best_score]
            status = "matched_manual" if override else ("ambiguous" if len(top_ties) > 1 else "matched")
            match_method = override_source + "+" + "+".join(reasons) if override else "+".join(reasons)
            comparisons = compare_fields(official, best)
            matched_supercombo[best["move_id"]] += 1
            crosswalk.append(
                {
                    **official,
                    "official_input_family": family,
                    "match_status": status,
                    "match_method": match_method,
                    "candidate_count": str(len(scored)),
                    "supercombo_move_id": best["move_id"],
                    "supercombo_move_type": best["move_type"],
                    "supercombo_input": best["input"],
                    "supercombo_name": best["name"],
                    "supercombo_startup": best["startup"],
                    "supercombo_active": best["active"],
                    "supercombo_recovery": best["recovery"],
                    "supercombo_hit_advantage": best["hit_advantage"],
                    "supercombo_block_advantage": best["block_advantage"],
                    "supercombo_cancel": best["cancel"],
                    "supercombo_damage": best["damage"],
                    "field_comparisons_json": json.dumps(comparisons, ensure_ascii=False, sort_keys=True),
                }
            )
        else:
            crosswalk.append(
                {
                    **official,
                    "official_input_family": family,
                    "match_status": "unmatched",
                    "match_method": "",
                    "candidate_count": "0",
                    "supercombo_move_id": "",
                    "supercombo_move_type": "",
                    "supercombo_input": "",
                    "supercombo_name": "",
                    "supercombo_startup": "",
                    "supercombo_active": "",
                    "supercombo_recovery": "",
                    "supercombo_hit_advantage": "",
                    "supercombo_block_advantage": "",
                    "supercombo_cancel": "",
                    "supercombo_damage": "",
                    "field_comparisons_json": "{}",
                }
            )

    unmatched_supercombo = [
        row
        for row in supercombo_rows
        if row["move_id"] not in matched_supercombo
    ]
    summary = {
        "official_rows": len(official_rows),
        "supercombo_rows": len(supercombo_rows),
        "crosswalk_status_counts": dict(Counter(row["match_status"] for row in crosswalk)),
        "matched_distinct_supercombo_rows": len(matched_supercombo),
        "supercombo_unmatched_rows": len(unmatched_supercombo),
        "supercombo_rows_matched_multiple_times": {
            move_id: count
            for move_id, count in sorted(matched_supercombo.items())
            if count > 1
        },
    }
    return crosswalk, unmatched_supercombo, summary


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", help="Deprecated; frame-data raw uses fixed latest paths.")
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--official-date-label", help="Deprecated; official frame-data raw uses fixed latest paths.")
    parser.add_argument("--official-mode", default="classic")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    raw_root = args.repo_root / "raw" / "frame-data" / "supercombo" / args.character_slug
    output_dir = args.repo_root / "wiki" / "outputs" / "data" / "supercombo" / "frame-data" / args.character_slug
    templates = read_json(raw_root / "data.templates.json")
    validation = read_json(raw_root / "validation.json")
    if validation.get("status") != "passed":
        raise RuntimeError(f"SuperCombo validation is not passed: {validation.get('status')}")

    frame_rows = frame_display_rows(templates["frames"])
    character_display_rows = character_rows(templates["character"])
    write_csv(output_dir / "frames.csv", frame_rows, FRAME_CSV_FIELDS)
    write_json(
        output_dir / "frames.json",
        {
            "source_raw_root": str(raw_root),
            "row_count": len(frame_rows),
            "rows": frame_json_rows(templates["frames"]),
        },
    )
    write_csv(output_dir / "character.csv", character_display_rows, CHARACTER_CSV_FIELDS)
    write_json(
        output_dir / "schema.json",
        {
            "schema_version": "supercombo_frame_data_outputs/v1",
            "source": "SuperCombo Wiki",
            "raw_root": str(raw_root),
            "files": {
                "frames_csv": "frames.csv",
                "frames_json": "frames.json",
                "character_csv": "character.csv",
                "crosswalk_csv": "crosswalk-official-classic.csv",
                "crosswalk_summary": "crosswalk-summary.json",
                "supercombo_unmatched_csv": "supercombo-unmatched.csv",
            },
            "frame_csv_fields": FRAME_CSV_FIELDS,
            "character_csv_fields": CHARACTER_CSV_FIELDS,
        },
    )

    official_csv = (
        args.repo_root
        / "wiki"
        / "outputs"
        / "data"
        / "frame-data"
        / args.character_slug
        / f"{args.official_mode}.csv"
    )
    with official_csv.open(encoding="utf-8", newline="") as handle:
        official_rows = list(csv.DictReader(handle))

    crosswalk_rows, unmatched_supercombo, summary = build_crosswalk(
        character_slug=args.character_slug,
        official_rows=official_rows,
        supercombo_rows=frame_rows,
    )
    crosswalk_fields = [
        "official_row_order",
        "official_category",
        "official_move_name",
        "official_input_display",
        "official_input_signature",
        "official_input_family",
        "startup",
        "active",
        "recovery",
        "damage",
        "on_hit",
        "on_block",
        "cancel",
        "match_status",
        "match_method",
        "candidate_count",
        "supercombo_move_id",
        "supercombo_move_type",
        "supercombo_input",
        "supercombo_name",
        "supercombo_startup",
        "supercombo_active",
        "supercombo_recovery",
        "supercombo_hit_advantage",
        "supercombo_block_advantage",
        "supercombo_cancel",
        "supercombo_damage",
        "field_comparisons_json",
    ]
    write_csv(output_dir / "crosswalk-official-classic.csv", crosswalk_rows, crosswalk_fields)
    write_csv(output_dir / "supercombo-unmatched.csv", unmatched_supercombo, FRAME_CSV_FIELDS)
    write_json(
        output_dir / "crosswalk-summary.json",
        {
            **summary,
            "source_raw_root": str(raw_root),
            "official_csv": str(official_csv),
            "crosswalk_policy": {
                "authority": "Capcom official fields remain authoritative for overlapping official frame-data fields.",
                "supercombo_primary_key": "move_id",
                "candidate_matching": [
                    "official Classic input tokens are converted to command signatures",
                    "special and super motions may also match a strength-collapsed input family",
                    "category/moveType compatibility and simple field equality increase candidate score",
                    "character-specific name overrides are used for reviewed variants such as JP Vihhat follow-ups and Ryu Denjin / hold-level rows",
                    "generic name overrides are used for Drive Rush system rows",
                    "duplicate SuperCombo inputs are not merged; the selected candidate keeps move_id",
                ],
            },
        },
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
