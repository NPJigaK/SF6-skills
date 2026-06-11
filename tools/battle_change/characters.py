from __future__ import annotations


SOURCE_FIGHTER_KEY_TO_CHARACTER_SLUG = {
    "gouki": "gouki_akuma",
    "honda": "ehonda",
    "vega": "vega_mbison",
}


def canonical_character_slug(source_fighter_key: str) -> str:
    key = source_fighter_key.strip()
    return SOURCE_FIGHTER_KEY_TO_CHARACTER_SLUG.get(key, key)
