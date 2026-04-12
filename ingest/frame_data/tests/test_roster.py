from __future__ import annotations

import pytest

from sf6_ingest.config import available_character_slugs, load_character, selected_sources


EXPECTED_CURRENT_CHARACTER_SLUGS = (
    "ryu",
    "luke",
    "jamie",
    "chunli",
    "guile",
    "kimberly",
    "juri",
    "ken",
    "blanka",
    "dhalsim",
    "ehonda",
    "deejay",
    "manon",
    "marisa",
    "jp",
    "zangief",
    "lily",
    "cammy",
    "rashid",
    "aki",
    "ed",
    "gouki_akuma",
    "vega_mbison",
    "terry",
    "mai",
    "elena",
    "sagat",
    "cviper",
    "alex",
)


def test_available_character_slugs_follow_the_canonical_roster_order() -> None:
    assert available_character_slugs() == EXPECTED_CURRENT_CHARACTER_SLUGS


def test_load_character_reads_non_legacy_roster_entries() -> None:
    ryu = load_character("ryu")
    assert ryu.character_slug == "ryu"
    assert ryu.display_name == "Ryu"
    assert ryu.sources == {
        "official": "https://www.streetfighter.com/6/ja-jp/character/ryu/frame",
        "supercombo_data": "https://wiki.supercombo.gg/w/Street_Fighter_6/Ryu/Data",
    }


def test_load_character_keeps_existing_supercombo_configuration() -> None:
    jp = load_character("jp")
    assert jp.sources["official"] == "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
    assert jp.sources["supercombo_data"] == "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data"


def test_selected_sources_for_all_only_uses_configured_sources() -> None:
    assert selected_sources("ryu", "all") == ("official", "supercombo")
    assert selected_sources("jp", "all") == ("official", "supercombo")


def test_every_current_roster_character_has_supercombo_data_configured() -> None:
    for character_slug in available_character_slugs():
        character = load_character(character_slug)
        assert character.sources["supercombo_data"].startswith("https://wiki.supercombo.gg/w/Street_Fighter_6/")
        assert "supercombo_frame_data" not in character.sources


def test_selected_sources_accepts_supercombo_for_every_current_roster_character() -> None:
    for character_slug in available_character_slugs():
        assert selected_sources(character_slug, "all") == ("official", "supercombo")
        assert selected_sources(character_slug, "supercombo") == ("official", "supercombo")[1:]
