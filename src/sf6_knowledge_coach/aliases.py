from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import aliases_file, exports_dir


FIELD_ALIASES = {
    "startup": ["startup", "発生", "何f", "何F"],
    "block_adv": ["block", "on block", "ガード", "硬直差", "有利不利"],
    "hit_adv": ["hit", "ヒット"],
    "damage": ["damage", "ダメージ"],
}


@dataclass(frozen=True)
class ResolvedContext:
    query: str
    character_slug: str | None = None
    move_input: str | None = None
    field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "character_slug": self.character_slug,
            "move_input": self.move_input,
            "field": self.field,
        }


def load_alias_entries(path: Path | None = None) -> list[dict[str, Any]]:
    source = path or aliases_file()
    if not source.exists():
        return []
    payload = json.loads(source.read_text(encoding="utf-8"))
    return list(payload.get("entries", []))


def available_character_slugs() -> set[str]:
    root = exports_dir()
    if not root.exists():
        return set()
    return {path.name for path in root.iterdir() if path.is_dir() and not path.name.startswith("_")}


def resolve_query(query: str) -> ResolvedContext:
    lowered = query.casefold()
    resolved: dict[str, str] = {}

    for entry in load_alias_entries():
        aliases = entry.get("aliases", [])
        if any(str(alias).casefold() in lowered for alias in aliases):
            normalized = entry.get("normalized", {})
            for key, value in normalized.items():
                if isinstance(value, str):
                    resolved[key] = value

    for slug in sorted(available_character_slugs(), key=len, reverse=True):
        if slug.casefold() in lowered:
            resolved.setdefault("character_slug", slug)

    move_match = re.search(
        r"(?<![A-Za-z0-9])(?:[1-9])?(?:LP|MP|HP|LK|MK|HK)(?![A-Za-z0-9])",
        query,
        re.IGNORECASE,
    )
    if move_match:
        resolved.setdefault("move_input", move_match.group(0).upper())

    for field, aliases in FIELD_ALIASES.items():
        if any(alias.casefold() in lowered for alias in aliases):
            resolved.setdefault("field", field)

    return ResolvedContext(
        query=query,
        character_slug=resolved.get("character_slug"),
        move_input=resolved.get("move_input"),
        field=resolved.get("field"),
    )
