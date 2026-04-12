from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from .config import package_root
from .core.common import compact_text, sha256_hex


class OfficialMatchRule(BaseModel):
    section: str
    icon_tokens: list[str] = Field(default_factory=list)
    name_key: str | None = None


class RegistryMove(BaseModel):
    move_id: str
    group: str
    sort_key: int
    official_match: OfficialMatchRule


class RegistryDocument(BaseModel):
    registry_version: str
    moves: list[RegistryMove]


class LoadedRegistry:
    def __init__(self, version: str, sha256: str, moves: list[RegistryMove]) -> None:
        self.version = version
        self.sha256 = sha256
        self.moves = moves
        self.by_move_id = {move.move_id: move for move in moves}
        self.sort_key_by_move_id = {move.move_id: move.sort_key for move in moves}
        self.official_index: dict[tuple[str, tuple[str, ...]], list[RegistryMove]] = defaultdict(list)
        for move in moves:
            key = (move.official_match.section, tuple(move.official_match.icon_tokens))
            self.official_index[key].append(move)
        duplicates = [move_id for move_id, count in _counts(move.move_id for move in moves).items() if count > 1]
        if duplicates:
            raise ValueError(f"duplicate move_id(s) in registry: {duplicates}")
        duplicate_sort_keys = [sort_key for sort_key, count in _counts(move.sort_key for move in moves).items() if count > 1]
        if duplicate_sort_keys:
            raise ValueError(f"duplicate sort_key(s) in registry: {duplicate_sort_keys}")

    def match_official(self, section: str | None, icon_tokens: list[str], name_key: str | None) -> list[RegistryMove]:
        if not section:
            return []
        candidates = self.official_index.get((section, tuple(icon_tokens or [])), [])
        if len(candidates) <= 1:
            if not candidates and not icon_tokens and not name_key:
                return []
            return list(candidates)
        if not name_key:
            return []
        filtered = [candidate for candidate in candidates if compact_text(candidate.official_match.name_key) == compact_text(name_key)]
        return filtered


def _counts(values) -> dict[object, int]:
    counts: dict[object, int] = defaultdict(int)
    for value in values:
        counts[value] += 1
    return counts


def load_registry(character_slug: str) -> LoadedRegistry:
    path = Path(package_root() / "config" / "registry" / f"{character_slug}.moves.yaml")
    text = path.read_text(encoding="utf-8")
    payload = yaml.safe_load(text) or {}
    document = RegistryDocument.model_validate(payload)
    return LoadedRegistry(document.registry_version, sha256_hex(text), document.moves)
