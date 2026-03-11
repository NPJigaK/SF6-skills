from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


SourceName = Literal["official", "supercombo"]


class CharacterConfig(BaseModel):
    character_slug: str
    display_name: str
    sources: dict[str, str]


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


def load_characters() -> dict[str, CharacterConfig]:
    payload = yaml.safe_load((package_root() / "config" / "characters.yaml").read_text(encoding="utf-8")) or {}
    return {slug: CharacterConfig.model_validate(config) for slug, config in payload.items()}


def available_character_slugs() -> tuple[str, ...]:
    return tuple(load_characters().keys())


def load_character(character_slug: str) -> CharacterConfig:
    return load_characters()[character_slug]


def load_fetch_profile(source: SourceName) -> FetchProfile:
    payload = yaml.safe_load((package_root() / "config" / "fetch_profiles.yaml").read_text(encoding="utf-8")) or {}
    return FetchProfile.model_validate(payload[source])
