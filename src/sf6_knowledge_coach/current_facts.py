from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import exports_dir

AUTHORITY_DATASET = "official_raw"


@dataclass(frozen=True)
class CurrentFact:
    character_slug: str
    move_id: str
    move_name: str
    input: str
    field: str
    value: Any
    authority: str
    source_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_slug": self.character_slug,
            "move_id": self.move_id,
            "move_name": self.move_name,
            "input": self.input,
            "field": self.field,
            "value": self.value,
            "authority": self.authority,
            "source_path": self.source_path,
        }


def official_raw_path(character_slug: str) -> Path:
    return exports_dir() / character_slug / f"{AUTHORITY_DATASET}.json"


def load_official_raw(character_slug: str) -> list[dict[str, Any]]:
    path = official_raw_path(character_slug)
    if not path.exists():
        raise LookupError(f"No official current-fact data for character: {character_slug}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected a list in {path}")
    return payload


def lookup_current_fact(character_slug: str, move_input: str, field: str) -> CurrentFact:
    normalized_input = move_input.upper()
    records = load_official_raw(character_slug)
    for record in records:
        if str(record.get("input", "")).upper() != normalized_input:
            continue
        if field not in record:
            raise LookupError(f"Field {field!r} is not available for {character_slug} {move_input}")
        return CurrentFact(
            character_slug=character_slug,
            move_id=str(record.get("move_id", "")),
            move_name=str(record.get("move_name", "")),
            input=str(record.get("input", "")),
            field=field,
            value=record.get(field),
            authority="data/exports official_raw",
            source_path=str(official_raw_path(character_slug)),
        )
    raise LookupError(f"No move input {move_input!r} for character {character_slug!r}")


def search_moves(query: str, limit: int = 10) -> list[dict[str, Any]]:
    lowered = query.casefold()
    results: list[dict[str, Any]] = []
    root = exports_dir()
    if not root.exists():
        return results

    for character_dir in sorted(path for path in root.iterdir() if path.is_dir() and not path.name.startswith("_")):
        path = official_raw_path(character_dir.name)
        if not path.exists():
            continue
        for record in load_official_raw(character_dir.name):
            haystack = " ".join(
                str(record.get(key, ""))
                for key in ("character_slug", "move_id", "move_name", "input", "move_group")
            ).casefold()
            if lowered in haystack:
                results.append(
                    {
                        "character_slug": record.get("character_slug"),
                        "move_id": record.get("move_id"),
                        "move_name": record.get("move_name"),
                        "input": record.get("input"),
                        "source_path": str(path),
                    }
                )
                if len(results) >= limit:
                    return results
    return results
