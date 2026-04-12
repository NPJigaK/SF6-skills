from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
import yaml


SourceName = Literal["official", "supercombo"]


class CharacterConfig(BaseModel):
    character_slug: str
    display_name: str
    sources: dict[str, str]


class CharacterRosterDocument(BaseModel):
    schema_version: str
    characters: list[CharacterConfig]


class FetchProfile(BaseModel):
    page_locale: str
    fetcher_name: Literal["Fetcher", "StealthyFetcher"]
    timeout_ms: int = 30000
    retry_count: int = 0
    retry_delay_ms: int = 0
    wait_ms: int = 0
    network_idle: bool = False
    solve_cloudflare: bool = False
    wait_selector: str | None = None
    challenge_markers: list[str] = Field(default_factory=list)


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    override = os.environ.get("SF6_INGEST_REPO_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[4]


def canonical_roster_path() -> Path:
    return repo_root() / "shared" / "roster" / "current-character-roster.json"


def load_characters() -> dict[str, CharacterConfig]:
    payload = json.loads(canonical_roster_path().read_text(encoding="utf-8"))
    document = CharacterRosterDocument.model_validate(payload)
    return {character.character_slug: character for character in document.characters}


def available_character_slugs() -> tuple[str, ...]:
    return tuple(load_characters().keys())


def load_character(character_slug: str) -> CharacterConfig:
    return load_characters()[character_slug]


def _source_key(source: SourceName) -> str:
    if source == "official":
        return "official"
    return "supercombo_data"


def selected_sources(character_slug: str, requested_source: str) -> tuple[SourceName, ...]:
    character = load_character(character_slug)
    available_sources = tuple(source for source in ("official", "supercombo") if _source_key(source) in character.sources)
    if requested_source == "all":
        return available_sources
    if requested_source not in available_sources:
        raise ValueError(f"source '{requested_source}' is not configured for character '{character_slug}'")
    return (requested_source,)  # type: ignore[return-value]


def load_fetch_profile(source: SourceName) -> FetchProfile:
    payload = yaml.safe_load((package_root() / "config" / "fetch_profiles.yaml").read_text(encoding="utf-8")) or {}
    return FetchProfile.model_validate(payload[source])
