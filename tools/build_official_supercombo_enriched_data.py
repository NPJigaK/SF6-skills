#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SUPPLEMENTAL_FRAME_FIELDS = [
    "section",
    "move_type",
    "move_id",
    "input",
    "name",
    "damage",
    "startup",
    "active",
    "recovery",
    "total",
    "hit_advantage",
    "block_advantage",
    "guard",
    "cancel",
    "hitconfirm",
    "chip",
    "damage_scaling",
    "punish_advantage",
    "perfect_parry_advantage",
    "drive_rush_cancel_on_hit",
    "drive_rush_cancel_on_block",
    "after_drive_rush_on_hit",
    "after_drive_rush_on_block",
    "hitstun",
    "blockstun",
    "hitstop",
    "drive_damage_block",
    "drive_damage_hit",
    "drive_gain",
    "super_gain_hit",
    "super_gain_block",
    "invuln",
    "armor",
    "airborne",
    "attack_range",
    "range_notes",
    "juggle_start",
    "juggle_increase",
    "juggle_limit",
    "projectile_speed",
    "pushback_hit",
    "pushback_block",
    "images",
    "hitboxes",
    "notes",
]

ENRICHMENT_META_FIELDS = [
    "enrichment_status",
    "enrichment_review_flags",
    "supercombo_match_status",
    "supercombo_match_method",
    "supercombo_candidate_count",
    "supercombo_field_conflicts",
    "supercombo_field_comparisons_json",
]

HUMAN_REVIEW_FIELDS = [
    "human_review_status",
    "human_review_decision",
    "human_review_value_policy",
    "human_review_note",
]

SUPERCOMBO_ONLY_LINK_FIELDS = [
    "link_type",
    "primary_official_row_order",
    "primary_official_move_name",
    "enabled_by_official_row_order",
    "enabled_by_official_move_name",
    "value_policy",
    "link_note",
]

HUMAN_REVIEW_DECISIONS_BY_CHARACTER = {
    "jp": {
        "43": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; allow_supercombo_supplemental_fields",
            "note": "ヴィーハト・アクノ / 214P~214LP/MP は補助リンクとして採用する。公式の全体44Fと SuperCombo の total 44 が一致し、無敵・空中・31F以降行動可の説明も対応する。",
        },
        "44": {
            "status": "accepted",
            "decision": "non_additive_supplemental_damage",
            "value_policy": "keep_official_damage_zero; use_supercombo_damage_as_triggered_vihhat_spike_damage; do_not_sum_with_vihhat_damage",
            "note": "ヴィーハト・チェーニ / 214P~214HP はヴィーハトを任意タイミングで発火させる技として扱う。SuperCombo damage 800 は発火した spike の補助情報であり、元のヴィーハト damage と合算して1600などにしない。",
        },
        "54": {
            "status": "accepted",
            "decision": "conflict_supplemental_only",
            "value_policy": "keep_official_startup_29; retain_supercombo_projectile_sequence_as_supplemental_conflict",
            "note": "SA2 ラヴーシュカ / 214214P は startup conflict 付き補助情報として扱う。公式 startup 29 を正とし、SuperCombo startup 1 と projectile sequence startup notes は補助情報に留める。",
        },
        "68": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; allow_supercombo_supplemental_fields",
            "note": "パリィドライブラッシュ / MPMK~66 は補助リンクとして採用する。SuperCombo の cancel/recovery decomposition は公式値の置換ではなく補助情報として扱う。",
        },
        "69": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; allow_supercombo_supplemental_fields",
            "note": "キャンセルドライブラッシュ / MPMK or 66 は補助リンクとして採用する。SuperCombo total 24(46) の括弧内 total は公式全体46Fと対応する。",
        },
    },
    "ryu": {
        "30": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; link_to_denjin_charge_hadoken; do_not_overwrite_official_damage",
            "note": "[電刃錬気]波動拳は `ryu_236p(charged)` を補助リンクとして採用する。SuperCombo damage 500x2 は合計1000として公式 damage 1000 と対応するが、公式列は上書きしない。",
        },
        "31": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; retain_supercombo_multihit_damage_as_supplemental",
            "note": "OD 波動拳は `ryu_236pp` を補助リンクとして採用する。SuperCombo damage 500x2 は公式 damage 1000 の分解情報として扱う。",
        },
        "32": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; link_to_denjin_charge_od_hadoken; do_not_overwrite_official_damage",
            "note": "[電刃錬気]OD 波動拳は `ryu_236pp(charged)` を補助リンクとして採用する。SuperCombo damage 400x3 (1200)、total 38、block +2 が公式値と対応する。",
        },
        "50": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; link_to_denjin_charge_hashogeki; do_not_overwrite_official_damage_or_recovery",
            "note": "[電刃錬気]波掌撃は `ryu_214p(charged)` を補助リンクとして採用する。SuperCombo damage 400x2 は合計800として公式 damage 800 と対応し、recovery 19(31) は補助分解として扱う。",
        },
        "51": {
            "status": "accepted",
            "decision": "conflict_supplemental_only",
            "value_policy": "keep_official_active_18_22; retain_supercombo_active_6_as_supplemental_conflict",
            "note": "OD 波掌撃は `ryu_214pp` を補助リンクとして採用するが、active duration は公式 18-22 と SuperCombo active 6 が単純一致しないため、公式 active を正とする。",
        },
        "54": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; retain_supercombo_multihit_damage_as_supplemental",
            "note": "SA1 真空波動拳は `ryu_236236p` を補助リンクとして採用する。SuperCombo damage 400x5 (2000)、total 86、block -24 が公式値と対応する。",
        },
        "55": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; link_to_denjin_sa1; do_not_overwrite_official_damage",
            "note": "[電刃錬気]SA1 真空波動拳は `ryu_236236p_denjin` を補助リンクとして採用する。SuperCombo damage 200x7,1000 (2400) と total 89 が公式値と対応する。",
        },
        "57": {
            "status": "accepted",
            "decision": "hold_level_supplemental_link",
            "value_policy": "keep_official_startup_20_and_damage_2900; retain_supercombo_hold_level_fields_as_supplemental",
            "note": "SA2 真波掌撃（Lv2）は `ryu_214214p_lv2` を補助リンクとして採用する。SuperCombo damage 2900 は公式と一致するが、startup 18~ は hold-level 補助情報であり公式 startup 20 を上書きしない。",
        },
        "58": {
            "status": "accepted",
            "decision": "hold_level_supplemental_link",
            "value_policy": "keep_official_startup_70_and_damage_3000; retain_supercombo_hold_level_fields_as_supplemental",
            "note": "SA2 真波掌撃（Lv3）は `ryu_214214p_lv3` を補助リンクとして採用する。SuperCombo damage 3000 は公式と一致するが、startup 50~ は hold-level 補助情報であり公式 startup 70 を上書きしない。",
        },
        "60": {
            "status": "accepted",
            "decision": "hold_level_supplemental_link",
            "value_policy": "keep_official_startup_20_and_damage_3300; retain_supercombo_denjin_hold_level_fields_as_supplemental",
            "note": "[電刃錬気]SA2 真波掌撃（Lv2）は `ryu_214214p_denjin_lv2` を補助リンクとして採用する。SuperCombo damage 3300 は公式と一致するが、startup 18~ は hold-level 補助情報であり公式 startup 20 を上書きしない。",
        },
        "61": {
            "status": "accepted",
            "decision": "hold_level_supplemental_link",
            "value_policy": "keep_official_startup_70_and_damage_3400; retain_supercombo_denjin_hold_level_fields_as_supplemental",
            "note": "[電刃錬気]SA2 真波掌撃（Lv3）は `ryu_214214p_denjin_lv3` を補助リンクとして採用する。SuperCombo damage 3400 は公式と一致するが、startup 50~ は hold-level 補助情報であり公式 startup 70 を上書きしない。",
        },
        "74": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; allow_supercombo_drive_rush_decomposition",
            "note": "パリィドライブラッシュ / MPMK~66 は補助リンクとして採用する。SuperCombo の startup/recovery/total 分解は公式全体45Fの置換ではなく補助情報として扱う。",
        },
        "75": {
            "status": "accepted",
            "decision": "supplemental_link",
            "value_policy": "keep_official_values; allow_supercombo_drive_rush_decomposition",
            "note": "キャンセルドライブラッシュ / MPMK or 66 は補助リンクとして採用する。SuperCombo total 24(46) の括弧内 total は公式全体46Fと対応する。",
        },
    },
}

SUPERCOMBO_ONLY_LINKS_BY_CHARACTER = {
    "ryu": {
        "ryu_6hk_214k": {
            "link_type": "conditional_variant",
            "primary_official_row_order": "41",
            "enabled_by_official_row_order": "23",
            "value_policy": "keep_official_rows_separate; do_not_merge_damage_with_6hk; retain_supercombo_variant_fields_only",
            "link_note": "6HK 旋風脚からキャンセルした空中竜巻旋風脚の条件付き variant。row 23 旋風脚の数値には混ぜず、row 41 空中竜巻旋風脚の補助 variant として扱う。",
        },
        "ryu_6hk_214kk": {
            "link_type": "conditional_variant",
            "primary_official_row_order": "42",
            "enabled_by_official_row_order": "23",
            "value_policy": "keep_official_rows_separate; do_not_merge_damage_with_6hk; retain_supercombo_variant_fields_only",
            "link_note": "6HK 旋風脚からキャンセルした OD 空中竜巻旋風脚の条件付き variant。row 23 旋風脚の数値には混ぜず、row 42 OD 空中竜巻旋風脚の補助 variant として扱う。",
        },
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def conflict_fields(comparisons_json: str) -> list[str]:
    comparisons = json.loads(comparisons_json or "{}")
    return [
        field
        for field, item in comparisons.items()
        if item.get("match") is False
    ]


def review_flags(crosswalk_row: dict[str, str], reused_move_ids: set[str]) -> list[str]:
    flags: list[str] = []
    conflicts = conflict_fields(crosswalk_row.get("field_comparisons_json", "{}"))
    if crosswalk_row.get("match_status") == "matched_manual":
        flags.append("manual_match")
    if crosswalk_row.get("match_status") == "ambiguous":
        flags.append("ambiguous_match")
    if conflicts:
        flags.append("basic_field_conflict:" + ",".join(conflicts))
    if int(crosswalk_row.get("candidate_count") or "0") > 1:
        flags.append("multiple_candidates")
    if crosswalk_row.get("supercombo_move_id") in reused_move_ids:
        flags.append("supercombo_row_reused")
    return flags


def supplemental_only_handling(*, character_slug: str, row: dict[str, str]) -> str:
    move_type = row.get("move_type", "")
    move_id = row.get("move_id", "")
    if move_type == "taunt":
        return "supercombo_only_taunt"
    if move_id in SUPERCOMBO_ONLY_LINKS_BY_CHARACTER.get(character_slug, {}):
        return "supplemental_variant_row"
    if move_id.endswith("_bomb"):
        return "supplemental_followup_row"
    if move_id in {"jp_214pp_214hp", "jp_236k_hold"}:
        return "supplemental_variant_row"
    return "supercombo_only"


def supplemental_only_link_fields(
    *,
    character_slug: str,
    row: dict[str, str],
    official_by_order: dict[str, dict[str, str]],
) -> dict[str, str]:
    link = dict(SUPERCOMBO_ONLY_LINKS_BY_CHARACTER.get(character_slug, {}).get(row.get("move_id", ""), {}))
    if not link:
        return {field: "" for field in SUPERCOMBO_ONLY_LINK_FIELDS}

    primary = official_by_order.get(link.get("primary_official_row_order", ""), {})
    enabled_by = official_by_order.get(link.get("enabled_by_official_row_order", ""), {})
    link["primary_official_move_name"] = primary.get("move_name", "")
    link["enabled_by_official_move_name"] = enabled_by.get("move_name", "")
    return {field: link.get(field, "") for field in SUPERCOMBO_ONLY_LINK_FIELDS}


def build_enriched(
    *,
    character_slug: str,
    official_rows: list[dict[str, str]],
    supercombo_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
    supercombo_only_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, Any]]:
    human_review_decisions = HUMAN_REVIEW_DECISIONS_BY_CHARACTER.get(character_slug, {})
    supercombo_by_id = {row["move_id"]: row for row in supercombo_rows}
    official_by_order = {row.get("row_order", str(index)): row for index, row in enumerate(official_rows, start=1)}
    crosswalk_by_official_order = {
        row["official_row_order"]: row
        for row in crosswalk_rows
    }
    reused_move_ids = {
        move_id
        for move_id, count in Counter(
            row.get("supercombo_move_id", "")
            for row in crosswalk_rows
            if row.get("supercombo_move_id")
        ).items()
        if count > 1
    }

    enriched_rows: list[dict[str, str]] = []
    flag_counts: Counter[str] = Counter()
    conflict_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()

    for official_index, official in enumerate(official_rows, start=1):
        row = dict(official)
        crosswalk = crosswalk_by_official_order.get(str(official_index), {})
        flags = review_flags(crosswalk, reused_move_ids) if crosswalk else []
        for flag in flags:
            flag_counts[flag] += 1
        conflicts = conflict_fields(crosswalk.get("field_comparisons_json", "{}")) if crosswalk else []
        for conflict in conflicts:
            conflict_counts[conflict] += 1

        supercombo_move_id = crosswalk.get("supercombo_move_id", "")
        supercombo = supercombo_by_id.get(supercombo_move_id)
        if supercombo:
            status = "enriched_review_required" if any(
                flag.startswith(("manual_match", "ambiguous_match", "basic_field_conflict")) for flag in flags
            ) else "enriched"
            for field in SUPPLEMENTAL_FRAME_FIELDS:
                row[f"supercombo_{field}"] = supercombo.get(field, "")
        else:
            status = "official_only"
            for field in SUPPLEMENTAL_FRAME_FIELDS:
                row[f"supercombo_{field}"] = ""

        review_decision = human_review_decisions.get(str(official_index), {})
        if review_decision and status == "enriched_review_required":
            status = "enriched_reviewed"

        row["enrichment_status"] = status
        row["enrichment_review_flags"] = ";".join(flags)
        row["supercombo_match_status"] = crosswalk.get("match_status", "")
        row["supercombo_match_method"] = crosswalk.get("match_method", "")
        row["supercombo_candidate_count"] = crosswalk.get("candidate_count", "")
        row["supercombo_field_conflicts"] = ",".join(conflicts)
        row["supercombo_field_comparisons_json"] = crosswalk.get("field_comparisons_json", "{}")
        row["human_review_status"] = review_decision.get("status", "")
        row["human_review_decision"] = review_decision.get("decision", "")
        row["human_review_value_policy"] = review_decision.get("value_policy", "")
        row["human_review_note"] = review_decision.get("note", "")
        status_counts[status] += 1
        enriched_rows.append(row)

    supercombo_only_output: list[dict[str, str]] = []
    for row in supercombo_only_rows:
        output = dict(row)
        output["suggested_handling"] = supplemental_only_handling(character_slug=character_slug, row=row)
        output.update(
            supplemental_only_link_fields(
                character_slug=character_slug,
                row=row,
                official_by_order=official_by_order,
            )
        )
        supercombo_only_output.append(output)

    summary = {
        "official_rows": len(official_rows),
        "supercombo_rows": len(supercombo_rows),
        "enriched_rows": len(enriched_rows),
        "supercombo_only_rows": len(supercombo_only_output),
        "enrichment_status_counts": dict(status_counts),
        "review_flag_counts": dict(sorted(flag_counts.items())),
        "basic_field_conflict_counts": dict(sorted(conflict_counts.items())),
        "human_review_status_counts": dict(
            Counter(row["human_review_status"] for row in enriched_rows if row["human_review_status"])
        ),
        "human_review_decision_counts": dict(
            Counter(row["human_review_decision"] for row in enriched_rows if row["human_review_decision"])
        ),
        "supercombo_reused_move_ids": sorted(reused_move_ids),
        "supercombo_only_suggested_handling_counts": dict(
            Counter(row["suggested_handling"] for row in supercombo_only_output)
        ),
    }
    return enriched_rows, supercombo_only_output, summary


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--official-mode", default="classic")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    official_dir = args.repo_root / "wiki" / "outputs" / "data" / "frame-data" / args.character_slug
    supercombo_dir = args.repo_root / "wiki" / "outputs" / "data" / "supercombo" / "frame-data" / args.character_slug
    output_dir = args.repo_root / "wiki" / "outputs" / "data" / "enriched" / "frame-data" / args.character_slug

    official_csv = official_dir / f"{args.official_mode}.csv"
    supercombo_csv = supercombo_dir / "frames.csv"
    crosswalk_csv = supercombo_dir / f"crosswalk-official-{args.official_mode}.csv"
    supercombo_only_csv = supercombo_dir / "supercombo-unmatched.csv"

    official_rows = read_csv(official_csv)
    supercombo_rows = read_csv(supercombo_csv)
    crosswalk_rows = read_csv(crosswalk_csv)
    supercombo_only_rows = read_csv(supercombo_only_csv)

    enriched_rows, supercombo_only_output, summary = build_enriched(
        character_slug=args.character_slug,
        official_rows=official_rows,
        supercombo_rows=supercombo_rows,
        crosswalk_rows=crosswalk_rows,
        supercombo_only_rows=supercombo_only_rows,
    )

    official_fields = list(official_rows[0].keys()) if official_rows else []
    enriched_fields = [
        *official_fields,
        *ENRICHMENT_META_FIELDS,
        *HUMAN_REVIEW_FIELDS,
        *[f"supercombo_{field}" for field in SUPPLEMENTAL_FRAME_FIELDS],
    ]
    write_csv(output_dir / f"{args.official_mode}-supercombo.csv", enriched_rows, enriched_fields)
    write_json(
        output_dir / f"{args.official_mode}-supercombo.json",
        {
            "schema_version": "official_supercombo_enriched_frame_data/v1",
            "authority": "official_fields_authoritative",
            "official_csv": str(official_csv),
            "supercombo_frames_csv": str(supercombo_csv),
            "crosswalk_csv": str(crosswalk_csv),
            "summary": summary,
            "rows": enriched_rows,
        },
    )
    supercombo_only_base_fields = list(supercombo_only_rows[0].keys()) if supercombo_only_rows else []
    supercombo_only_fields = [*supercombo_only_base_fields, "suggested_handling", *SUPERCOMBO_ONLY_LINK_FIELDS]
    write_csv(output_dir / "supercombo-only.csv", supercombo_only_output, supercombo_only_fields)
    write_json(
        output_dir / "schema.json",
        {
            "schema_version": "official_supercombo_enriched_outputs/v1",
            "authority": "Capcom official columns are preserved and remain authoritative.",
            "files": {
                "enriched_csv": f"{args.official_mode}-supercombo.csv",
                "enriched_json": f"{args.official_mode}-supercombo.json",
                "supercombo_only_csv": "supercombo-only.csv",
                "summary": "summary.json",
            },
            "official_fields": official_fields,
            "enrichment_meta_fields": ENRICHMENT_META_FIELDS,
            "human_review_fields": HUMAN_REVIEW_FIELDS,
            "supercombo_prefixed_fields": [f"supercombo_{field}" for field in SUPPLEMENTAL_FRAME_FIELDS],
            "supercombo_only_extra_fields": ["suggested_handling", *SUPERCOMBO_ONLY_LINK_FIELDS],
        },
    )
    write_json(
        output_dir / "summary.json",
        {
            **summary,
            "official_csv": str(official_csv),
            "supercombo_frames_csv": str(supercombo_csv),
            "crosswalk_csv": str(crosswalk_csv),
            "output_csv": str(output_dir / f"{args.official_mode}-supercombo.csv"),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
