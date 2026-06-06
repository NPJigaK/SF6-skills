from __future__ import annotations

from extract_capcom_battle_change import flatten_adjust


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


def main() -> int:
    test_flatten_adjust_preserves_policy_common_and_fighter_order()
    test_flatten_adjust_marks_selector_and_page_title_mismatch()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
