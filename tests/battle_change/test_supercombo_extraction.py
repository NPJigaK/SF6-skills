from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.battle_change.supercombo.extract import (
    build_upstream_outputs,
    build_change_events,
    build_move_change_index,
    clean_wikitext_inline,
    extract_all,
)


def test_clean_wikitext_inline_preserves_display_text_and_inputs() -> None:
    text = "{{clr|DR|Wakeup Drive Reversal}} refunds {{clr|DR|1 Drive bar}} on hit"

    assert clean_wikitext_inline(text) == "Wakeup Drive Reversal refunds 1 Drive bar on hit"


def test_build_change_events_groups_nested_bullets_under_top_level_event() -> None:
    version = {
        "version": "2.0301",
        "gameversion": "2.0301",
        "date": "2026-05-28",
        "summary": "Ingrid Release. Minor system changes and bug fixes.",
        "official_battle_change_id_from_link": "20260528",
        "supercombo_version_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Version/2.0301",
        "raw_wikitext_path": "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0301/page.raw.wikitext",
    }
    wikitext = """
== '''Universal Changes''' ==
* '''{{clr|DR|Wakeup Drive Reversal}}'''
** When the invincible startup interacts with an opponent's Throw hitbox, a 12f screen freeze now occurs and refunds {{clr|DR|1 Drive bar}} on hit
** This does not prevent Burnout from occurring before the meter is gained

== '''Character Changes''' ==

=== '''Ed''' ===
* {{clr|H|Low Smash Combination}} ({{clr|H|2HK}}~{{clr|H|HP}})
** Startup of 2nd hit reduced 12 → 10
** Total animation decreased 35 → 33
** This causes the Target Combo to always be a true blockstring
""".strip()

    events = build_change_events(version, wikitext)

    assert len(events) == 2
    system_event = events[0]
    assert system_event["event_id"] == "supercombo-patch-notes:2.0301:1"
    assert system_event["source_authority"] == "community"
    assert system_event["source_family"] == "supercombo-patch-notes"
    assert system_event["official_battle_change_id_from_link"] == "20260528"
    assert system_event["scope"] == "system"
    assert system_event["section_title"] == "Universal Changes"
    assert system_event["fighter_display_name"] == ""
    assert system_event["target_title"] == "Wakeup Drive Reversal"
    assert system_event["detail_lines"] == [
        "When the invincible startup interacts with an opponent's Throw hitbox, a 12f screen freeze now occurs and refunds 1 Drive bar on hit",
        "This does not prevent Burnout from occurring before the meter is gained",
    ]
    assert set(system_event["change_types"]) == {"drive_gauge", "hitbox_hurtbox", "startup", "throw"}
    assert system_event["value_changes"] == []
    assert "12f screen freeze" in system_event["text_plain"]

    fighter_event = events[1]
    assert fighter_event["event_id"] == "supercombo-patch-notes:2.0301:2"
    assert fighter_event["scope"] == "fighter"
    assert fighter_event["fighter_display_name"] == "Ed"
    assert fighter_event["fighter_key"] == "ed"
    assert fighter_event["character_slug"] == "ed"
    assert fighter_event["target_title"] == "Low Smash Combination"
    assert fighter_event["normalized_target_key"] == "ed::low smash combination"
    assert fighter_event["value_changes"] == [
        {
            "before": "12",
            "after": "10",
            "unit": "",
            "context": "Startup of 2nd hit reduced",
        },
        {
            "before": "35",
            "after": "33",
            "unit": "",
            "context": "Total animation decreased",
        },
    ]
    assert "true blockstring" in fighter_event["text_plain"]


def test_build_change_events_attaches_wikitext_table_to_preceding_event() -> None:
    version = {
        "version": "2.0111",
        "gameversion": "2.0111",
        "date": "2025-12-16",
        "summary": "Bug fixes and minor adjustments.",
        "official_battle_change_id_from_link": "20251216",
        "supercombo_version_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Version/2.0111",
        "raw_wikitext_path": "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0111/page.raw.wikitext",
    }
    wikitext = """
== '''Character Changes''' ==
=== '''Mai''' ===
* Kachousen (236P) - Charged / {{clr|OD|Charged OD}} / {{clr|3|Flame}} versions build more Drive gauge for the defender when Parried and/or Perfect Parried
{| class="wikitable"
! Kachousen (Fan) !! Drive Gain
|-
| 236[P] || 2500x2 → 5000,2500
|-
| {{clr|OD|236[PP]}} || colspan="2" | 1400x2 → 2500x2
|}
""".strip()

    events = build_change_events(version, wikitext)

    assert len(events) == 1
    event = events[0]
    assert event["target_title"] == "Kachousen"
    assert event["raw_table_blocks"] == [
        "{| class=\"wikitable\"\n! Kachousen (Fan) !! Drive Gain\n|-\n| 236[P] || 2500x2 → 5000,2500\n|-\n| {{clr|OD|236[PP]}} || colspan=\"2\" | 1400x2 → 2500x2\n|}"
    ]
    assert event["table_text_blocks"] == [
        "Kachousen (Fan) Drive Gain 236[P] 2500x2 → 5000,2500 236[PP] 1400x2 → 2500x2"
    ]
    assert event["change_types"] == ["drive_gauge"]


def test_build_move_change_index_groups_community_events_by_target() -> None:
    version = {
        "version": "2.0301",
        "gameversion": "2.0301",
        "date": "2026-05-28",
        "summary": "Ingrid Release. Minor system changes and bug fixes.",
        "official_battle_change_id_from_link": "20260528",
        "supercombo_version_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Version/2.0301",
        "raw_wikitext_path": "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0301/page.raw.wikitext",
    }
    wikitext = """
== '''Character Changes''' ==
=== '''Ed''' ===
* {{clr|H|Low Smash Combination}} ({{clr|H|2HK}}~{{clr|H|HP}})
** Startup of 2nd hit reduced 12 → 10
* {{clr|H|Low Smash Combination}} ({{clr|H|2HK}}~{{clr|H|HP}})
** Total animation decreased 35 → 33
""".strip()

    index = build_move_change_index(build_change_events(version, wikitext))

    assert index["row_count"] == 1
    row = index["rows"][0]
    assert row["source_authorities"] == ["community"]
    assert row["source_families"] == ["supercombo-patch-notes"]
    assert row["fighter_key"] == "ed"
    assert row["character_slug"] == "ed"
    assert row["normalized_target_key"] == "ed::low smash combination"
    assert row["event_count"] == 2
    assert row["versions"] == ["2.0301"]
    assert row["official_battle_change_ids_from_links"] == ["20260528"]
    assert row["numeric_explicit_event_count"] == 2


def test_build_move_change_index_uses_canonical_frame_data_slug_for_name_variants() -> None:
    version = {
        "version": "2.0301",
        "gameversion": "2.0301",
        "date": "2026-05-28",
        "summary": "Ingrid Release. Minor system changes and bug fixes.",
        "official_battle_change_id_from_link": "20260528",
        "supercombo_version_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Version/2.0301",
        "raw_wikitext_path": "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0301/page.raw.wikitext",
    }
    wikitext = """
== '''Character Changes''' ==
=== '''Akuma''' ===
* Gou Hadoken
** Startup 16 → 15
=== '''E. Honda''' ===
* Sumo Headbutt
** Recovery 22 → 24
=== '''M. Bison''' ===
* Psycho Crusher Attack
** Block advantage -4 → -5
""".strip()

    events = build_change_events(version, wikitext)
    index = build_move_change_index(events)

    assert {event["fighter_key"] for event in events} == {"gouki", "honda", "vega"}
    assert {event["character_slug"] for event in events} == {"gouki_akuma", "ehonda", "vega_mbison"}
    assert {row["normalized_target_key"] for row in index["rows"]} == {
        "gouki_akuma::gou hadoken",
        "ehonda::sumo headbutt",
        "vega_mbison::psycho crusher attack",
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_minimal_supercombo_patch_notes_fixture(tmp_path: Path) -> tuple[Path, Path]:
    raw_root = tmp_path / "raw" / "web-pages" / "wiki.supercombo.gg" / "patch-notes"
    output_root = tmp_path / "wiki" / "outputs" / "data" / "battle-change"

    write_json(
        raw_root / "manifest.json",
        {
            "captured_at_utc": "2026-06-11T00:00:00Z",
            "source_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes",
            "raw_root": "raw/web-pages/wiki.supercombo.gg/patch-notes",
            "storage_policy": "updateable_web_page_capture",
        },
    )
    write_json(
        raw_root / "rendered" / "main.dom.json",
        {
            "tables": [
                {
                    "headers": ["version", "gameversion", "date", "summary", "links"],
                    "rows": [
                        {
                            "row_index": 0,
                            "cells": [
                                {"text": "version", "html": "version"},
                                {"text": "gameversion", "html": "gameversion"},
                                {"text": "date", "html": "date"},
                                {"text": "summary", "html": "summary"},
                                {"text": "links", "html": "links"},
                            ],
                        },
                        {
                            "row_index": 1,
                            "cells": [
                                {
                                    "text": "2.0301",
                                    "html": '<a href="/w/Street_Fighter_6/Version/2.0301">2.0301</a>',
                                },
                                {"text": "2.0301", "html": "2.0301"},
                                {"text": "2026-05-28", "html": "2026-05-28"},
                                {
                                    "text": "Ingrid Release. Minor system changes and bug fixes.",
                                    "html": "<b>Ingrid Release</b>. Minor system changes and bug fixes.",
                                },
                                {
                                    "text": "Patch Notes",
                                    "html": '<a href="https://www.streetfighter.com/6/buckler/battle_change/20260528">Patch Notes</a>',
                                },
                            ],
                        },
                    ],
                }
            ]
        },
    )

    detail_root = raw_root / "versions" / "2-0301"
    write_json(
        detail_root / "manifest.json",
        {
            "page_title": "Street Fighter 6/Version/2.0301",
            "source_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Version/2.0301",
            "raw_root": "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0301",
            "captured_at_utc": "2026-06-11T00:10:00Z",
            "source_updated_at": "2026-06-10T00:00:00Z",
            "source_revision": {"revision_id": 12345, "revision_timestamp": "2026-06-10T00:00:00Z"},
        },
    )
    write_json(
        detail_root / "validation.json",
        {
            "status": "passed",
            "summary": {
                "wikitext_bytes": 120,
                "heading_count": 2,
                "table_count": 1,
                "mediawiki_revision_id": 12345,
            },
        },
    )
    (detail_root / "page.raw.wikitext").write_text("== Universal Changes ==\n* System note\n", encoding="utf-8")
    write_json(detail_root / "rendered" / "main.dom.json", {"tables": []})

    write_json(
        output_root / "official" / "versions.json",
        {
            "rows": [
                {
                    "version_id": "20260528",
                    "version_title": "2026.05.28 update",
                    "policy_count": "1",
                    "common_change_count": "5",
                    "fighter_change_count": "18",
                    "data_json_path": "raw/battle-change/official/versions/20260528/data.json",
                }
            ]
        },
    )
    return raw_root, output_root


def test_extract_all_does_not_leave_upstream_outputs_when_downstream_schema_is_missing(tmp_path: Path) -> None:
    raw_root, output_root = write_minimal_supercombo_patch_notes_fixture(tmp_path)

    with pytest.raises(FileNotFoundError):
        extract_all(tmp_path)

    supercombo_output_root = output_root / "supercombo-patch-notes"
    assert not (supercombo_output_root / "versions.json").exists()
    assert not (supercombo_output_root / "official-battle-change-crosswalk.json").exists()
    assert not (raw_root / "version-captures.json").exists()
    assert not (raw_root / "validation.batch.json").exists()


def test_build_upstream_outputs_regenerates_versions_crosswalk_and_validation(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw" / "web-pages" / "wiki.supercombo.gg" / "patch-notes"
    output_root = tmp_path / "wiki" / "outputs" / "data" / "battle-change"

    write_json(
        raw_root / "manifest.json",
        {
            "captured_at_utc": "2026-06-11T00:00:00Z",
            "source_url": "https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes",
            "raw_root": "raw/web-pages/wiki.supercombo.gg/patch-notes",
            "storage_policy": "updateable_web_page_capture",
        },
    )
    write_json(
        raw_root / "rendered" / "main.dom.json",
        {
            "tables": [
                {
                    "headers": ["version", "gameversion", "date", "summary", "links"],
                    "rows": [
                        {
                            "row_index": 0,
                            "cells": [
                                {"text": "version", "html": "version"},
                                {"text": "gameversion", "html": "gameversion"},
                                {"text": "date", "html": "date"},
                                {"text": "summary", "html": "summary"},
                                {"text": "links", "html": "links"},
                            ],
                        },
                        {
                            "row_index": 1,
                            "cells": [
                                {
                                    "text": "2.0301",
                                    "html": '<a href="/w/Street_Fighter_6/Version/2.0301">2.0301</a>',
                                },
                                {"text": "2.0301", "html": "2.0301"},
                                {"text": "2026-05-28", "html": "2026-05-28"},
                                {
                                    "text": "Ingrid Release. Minor system changes and bug fixes.",
                                    "html": "<b>Ingrid Release</b>. Minor system changes and bug fixes.",
                                },
                                {
                                    "text": "Patch Notes",
                                    "html": '<a href="https://www.streetfighter.com/6/buckler/battle_change/20260528">Patch Notes</a>',
                                },
                            ],
                        },
                        {
                            "row_index": 2,
                            "cells": [
                                {
                                    "text": "1.00",
                                    "html": '<a href="/w/Street_Fighter_6/Version/1.00">1.00</a>',
                                },
                                {"text": "1.00", "html": "1.00"},
                                {"text": "2023-06-02", "html": "2023-06-02"},
                                {"text": "Launch Version", "html": "Launch Version"},
                                {"text": "Official Site", "html": '<a href="https://streetfighter.com/6">Official Site</a>'},
                            ],
                        },
                    ],
                }
            ]
        },
    )

    for version, slug, title, official_id in [
        ("2.0301", "2-0301", "Street Fighter 6/Version/2.0301", "20260528"),
        ("1.00", "1-00", "Street Fighter 6/Version/1.00", None),
    ]:
        detail_root = raw_root / "versions" / slug
        write_json(
            detail_root / "manifest.json",
            {
                "page_title": title,
                "source_url": f"https://wiki.supercombo.gg/w/Street_Fighter_6/Version/{version}",
                "raw_root": f"raw/web-pages/wiki.supercombo.gg/patch-notes/versions/{slug}",
                "captured_at_utc": "2026-06-11T00:10:00Z",
                "source_updated_at": "2026-06-10T00:00:00Z",
                "source_revision": {"revision_id": 12345, "revision_timestamp": "2026-06-10T00:00:00Z"},
            },
        )
        write_json(
            detail_root / "validation.json",
            {
                "status": "passed",
                "summary": {
                    "wikitext_bytes": 120,
                    "heading_count": 2,
                    "table_count": 1,
                    "mediawiki_revision_id": 12345,
                },
            },
        )
        wikitext = "== Universal Changes ==\n* System note\n=== Ed ===\n* Low Smash Combination\n"
        if official_id is None:
            wikitext = "== Launch Version ==\n* Initial release\n"
        (detail_root / "page.raw.wikitext").write_text(wikitext, encoding="utf-8")
        write_json(detail_root / "rendered" / "main.dom.json", {"tables": []})

    write_json(
        output_root / "official" / "versions.json",
        {
            "rows": [
                {
                    "version_id": "20260528",
                    "version_title": "2026.05.28 update",
                    "policy_count": "1",
                    "common_change_count": "5",
                    "fighter_change_count": "18",
                    "data_json_path": "raw/battle-change/official/versions/20260528/data.json",
                }
            ]
        },
    )

    outputs = build_upstream_outputs(tmp_path, generated_at_utc="2026-06-11T00:20:00Z")

    versions = outputs["versions"]
    assert versions["row_count"] == 2
    assert versions["fields"] == list(versions["rows"][0].keys())
    assert versions["rows"][0]["source_authority"] == "community"
    assert versions["rows"][0]["raw_validation_path"] == (
        "raw/web-pages/wiki.supercombo.gg/patch-notes/versions/2-0301/validation.json"
    )

    crosswalk = outputs["official_battle_change_crosswalk"]
    assert crosswalk["summary"] == {
        "supercombo_row_count": 2,
        "matched_count": 1,
        "supercombo_no_official_link_count": 1,
        "official_unmatched_count": 0,
    }
    assert crosswalk["rows"][0]["mapping_basis"] == "SuperCombo Patch Notes external Patch Notes link"
    assert crosswalk["rows"][1]["match_status"] == "supercombo_no_official_battle_change_link"

    captures = outputs["version_captures"]
    assert captures["version_count"] == 2
    assert captures["detail_pages"][0]["official_battle_change_id_from_link"] == "20260528"

    validation = outputs["batch_validation"]
    assert validation["status"] == "passed"
    assert validation["summary"]["captured_version_detail_pages"] == 2
