from __future__ import annotations

from tools.battle_change.official.extract import (
    build_change_events,
    build_move_change_index,
    flatten_adjust,
)


def test_flatten_adjust_preserves_policy_common_and_fighter_order() -> None:
    adjust = {
        "title": "2026.05.28 update",
        "current_version": "20260528",
        "versions": [{"id": "20260528", "title": "2026.05.28 update"}],
        "policy": [{"title": "全体コンセプト", "text": "方針<br>本文"}],
        "common": [
            {
                "title": "通常投げ",
                "body": [{"category": "調整", "text": "共通本文"}],
            }
        ],
        "fighter": [
            {
                "fighter_id": "リュウ",
                "fighter_alpha": "RYU",
                "fighter_tool_name": "ryu",
                "fighter_url_name": "ryu",
                "detail": [
                    {
                        "title": "波動拳",
                        "body": [{"category": "不具合修正", "text": "キャラ別本文"}],
                    }
                ],
            }
        ],
        "fighter_list": [],
        "current_fighter": "",
        "title_bg": "",
    }

    rows = flatten_adjust(
        version_order=1,
        adjust=adjust,
        data_json_path="raw/example/data.json",
        version_selector_title="2026.05.28 update",
    )

    assert [row["section_type"] for row in rows] == ["policy", "common", "fighter"]
    assert rows[0]["text_html"] == "方針<br>本文"
    assert rows[1]["common_title"] == "通常投げ"
    assert rows[1]["category"] == "調整"
    assert rows[2]["fighter_tool_name"] == "ryu"
    assert rows[2]["detail_title"] == "波動拳"
    assert rows[2]["category"] == "不具合修正"
    assert all(row["version_id"] == "20260528" for row in rows)
    assert all(row["version_title"] == "2026.05.28 update" for row in rows)
    assert all(row["version_selector_title"] == "2026.05.28 update" for row in rows)
    assert all(row["version_title_mismatch"] == "false" for row in rows)
    assert all(row["data_json_path"] == "raw/example/data.json" for row in rows)


def test_flatten_adjust_marks_selector_and_page_title_mismatch() -> None:
    adjust = {
        "title": "2023.12.1 update",
        "current_version": "20231201",
        "versions": [{"id": "20231201", "title": "2023.12.01 update"}],
        "policy": [],
        "common": [
            {
                "title": "SA共通",
                "body": [{"category": "不具合修正", "text": "本文"}],
            }
        ],
        "fighter": [],
        "fighter_list": [],
        "current_fighter": "",
        "title_bg": "",
    }

    rows = flatten_adjust(
        version_order=17,
        adjust=adjust,
        data_json_path="raw/example/20231201/data.json",
        version_selector_title="2023.12.01 update",
    )

    assert len(rows) == 1
    assert rows[0]["version_id"] == "20231201"
    assert rows[0]["version_title"] == "2023.12.1 update"
    assert rows[0]["version_selector_title"] == "2023.12.01 update"
    assert rows[0]["version_title_mismatch"] == "true"
    assert rows[0]["section_type"] == "common"
    assert rows[0]["common_title"] == "SA共通"


def test_build_change_events_extracts_fighter_numeric_change_event() -> None:
    rows = [
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "9",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "9",
            "fighter_id": "サガット",
            "fighter_alpha": "SAGAT",
            "fighter_tool_name": "sagat",
            "fighter_url_name": "sagat",
            "detail_order": "2",
            "detail_title": "しゃがみ中K",
            "category": "調整",
            "text_html": "ヒット時の硬直差を+4F⇒+5Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        }
    ]

    events = build_change_events(rows)

    assert len(events) == 1
    event = events[0]
    assert event["event_id"] == "official-battle-change:20251216:fighter:9:2:1"
    assert event["source_authority"] == "official"
    assert event["scope"] == "fighter"
    assert event["fighter_tool_name"] == "sagat"
    assert event["character_slug"] == "sagat"
    assert event["target_title"] == "しゃがみ中K"
    assert event["normalized_target_key"] == "sagat::しゃがみ中k"
    assert event["change_types"] == ["frame_advantage"]
    assert event["confidence"] == "numeric_explicit"
    assert event["value_changes"] == [
        {
            "before": "+4F",
            "after": "+5F",
            "unit": "F",
            "context": "ヒット時の硬直差",
        }
    ]
    assert event["text_plain"] == "ヒット時の硬直差を+4F⇒+5Fに変更しました。"


def test_build_move_change_index_groups_events_by_character_and_target() -> None:
    rows = [
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "9",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "9",
            "fighter_id": "サガット",
            "fighter_alpha": "SAGAT",
            "fighter_tool_name": "sagat",
            "fighter_url_name": "sagat",
            "detail_order": "2",
            "detail_title": "しゃがみ中K",
            "category": "調整",
            "text_html": "ヒット時の硬直差を+4F⇒+5Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        },
        {
            "version_order": "8",
            "version_id": "20250901",
            "version_title": "2025.09.01 update",
            "version_selector_title": "2025.09.01 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "3",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "3",
            "fighter_id": "サガット",
            "fighter_alpha": "SAGAT",
            "fighter_tool_name": "sagat",
            "fighter_url_name": "sagat",
            "detail_order": "4",
            "detail_title": "しゃがみ中K",
            "category": "不具合修正",
            "text_html": "特定の状況で硬直が想定と異なる不具合を修正しました。",
            "data_json_path": "raw/battle-change/official/versions/20250901/data.json",
        },
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "9",
            "body_order": "2",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "9",
            "fighter_id": "サガット",
            "fighter_alpha": "SAGAT",
            "fighter_tool_name": "sagat",
            "fighter_url_name": "sagat",
            "detail_order": "2",
            "detail_title": "しゃがみ中K",
            "category": "調整",
            "text_html": "ガード時の硬直差を-2F⇒-1Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        },
    ]

    index = build_move_change_index(build_change_events(rows))

    assert index["row_count"] == 1
    row = index["rows"][0]
    assert row["fighter_tool_name"] == "sagat"
    assert row["character_slug"] == "sagat"
    assert row["normalized_target_key"] == "sagat::しゃがみ中k"
    assert row["event_count"] == 3
    assert row["version_ids"] == ["20251216", "20250901"]
    assert row["source_authorities"] == ["official"]
    assert row["data_json_paths"] == [
        "raw/battle-change/official/versions/20251216/data.json",
        "raw/battle-change/official/versions/20250901/data.json",
    ]
    assert row["change_types"] == ["bugfix", "frame_advantage"]
    assert row["numeric_explicit_event_count"] == 2


def test_build_move_change_index_uses_canonical_frame_data_slug_for_name_variants() -> None:
    rows = [
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "9",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "9",
            "fighter_id": "豪鬼",
            "fighter_alpha": "AKUMA",
            "fighter_tool_name": "gouki",
            "fighter_url_name": "gouki",
            "detail_order": "2",
            "detail_title": "豪波動拳",
            "category": "調整",
            "text_html": "硬直差を+1F⇒+2Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        },
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "10",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "10",
            "fighter_id": "エドモンド本田",
            "fighter_alpha": "E. HONDA",
            "fighter_tool_name": "honda",
            "fighter_url_name": "honda",
            "detail_order": "1",
            "detail_title": "スーパー頭突き",
            "category": "調整",
            "text_html": "硬直差を-4F⇒-5Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        },
        {
            "version_order": "4",
            "version_id": "20251216",
            "version_title": "2025.12.16 update",
            "version_selector_title": "2025.12.16 update",
            "version_title_mismatch": "false",
            "section_type": "fighter",
            "section_order": "11",
            "body_order": "1",
            "policy_title": "",
            "common_title": "",
            "fighter_order": "11",
            "fighter_id": "ベガ",
            "fighter_alpha": "M. BISON",
            "fighter_tool_name": "vega",
            "fighter_url_name": "vega",
            "detail_order": "1",
            "detail_title": "サイコクラッシャーアタック",
            "category": "調整",
            "text_html": "硬直差を-6F⇒-7Fに変更しました。",
            "data_json_path": "raw/battle-change/official/versions/20251216/data.json",
        },
    ]

    index = build_move_change_index(build_change_events(rows))

    keys = {row["normalized_target_key"] for row in index["rows"]}
    slugs = {row["character_slug"] for row in index["rows"]}
    assert keys == {
        "gouki_akuma::豪波動拳",
        "ehonda::スーパー頭突き",
        "vega_mbison::サイコクラッシャーアタック",
    }
    assert slugs == {"gouki_akuma", "ehonda", "vega_mbison"}


def main() -> int:
    test_flatten_adjust_preserves_policy_common_and_fighter_order()
    test_flatten_adjust_marks_selector_and_page_title_mismatch()
    test_build_change_events_extracts_fighter_numeric_change_event()
    test_build_move_change_index_groups_events_by_character_and_target()
    test_build_move_change_index_uses_canonical_frame_data_slug_for_name_variants()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
