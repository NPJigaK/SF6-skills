from __future__ import annotations

import json

from capture_capcom_battle_change import (
    adjust_from_payload,
    build_data_url,
    extract_next_data,
    validate_adjust_payload,
)


def test_extract_next_data_decodes_embedded_payload() -> None:
    payload = {
        "buildId": "build-123",
        "props": {
            "pageProps": {
                "adjust": {
                    "title": "2026.04.15 update",
                    "current_version": "20260415",
                    "versions": [{"id": "20260415", "title": "2026.04.15 update"}],
                    "policy": [],
                    "common": [],
                    "fighter": [],
                    "fighter_list": [],
                    "current_fighter": "",
                    "title_bg": "",
                }
            }
        },
    }
    html = (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(payload, ensure_ascii=False).replace('"', "&quot;")
        + "</script></body></html>"
    )

    data = extract_next_data(html)

    assert data["buildId"] == "build-123"
    assert adjust_from_payload(data)["current_version"] == "20260415"


def test_build_data_url_uses_buckler_asset_prefix_and_locale() -> None:
    assert build_data_url("build-123", "20260415") == (
        "https://www.streetfighter.com/6/buckler/_next/data/"
        "build-123/ja-jp/battle_change/20260415.json"
    )


def test_validate_adjust_payload_rejects_version_mismatch() -> None:
    adjust = {
        "title": "2026.04.15 update",
        "current_version": "20260415",
        "versions": [{"id": "20260415", "title": "2026.04.15 update"}],
        "policy": [],
        "common": [],
        "fighter": [],
        "fighter_list": [],
        "current_fighter": "",
        "title_bg": "",
    }

    try:
        validate_adjust_payload(adjust, expected_version="20260528")
    except ValueError as exc:
        assert "current_version mismatch" in str(exc)
    else:
        raise AssertionError("version mismatch should fail closed")


def test_validate_adjust_payload_accepts_common_and_fighter_sections() -> None:
    adjust = {
        "title": "2026.05.28 update",
        "current_version": "20260528",
        "versions": [{"id": "20260528", "title": "2026.05.28 update"}],
        "policy": [{"title": "全体コンセプト", "text": "本文"}],
        "common": [
            {
                "title": "通常投げ",
                "body": [{"category": "調整", "text": "共通変更本文"}],
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
        "fighter_list": [{"fighter_id": "リュウ", "fighter_tool_name": "ryu"}],
        "current_fighter": "",
        "title_bg": "",
    }

    summary = validate_adjust_payload(adjust, expected_version="20260528")

    assert summary == {
        "version_id": "20260528",
        "title": "2026.05.28 update",
        "policy_count": 1,
        "common_section_count": 1,
        "common_change_count": 1,
        "fighter_count": 1,
        "fighter_detail_count": 1,
        "fighter_change_count": 1,
        "version_count": 1,
        "fighter_list_count": 1,
    }


def main() -> int:
    test_extract_next_data_decodes_embedded_payload()
    test_build_data_url_uses_buckler_asset_prefix_and_locale()
    test_validate_adjust_payload_rejects_version_mismatch()
    test_validate_adjust_payload_accepts_common_and_fighter_sections()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
