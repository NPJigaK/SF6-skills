from __future__ import annotations

from pathlib import Path

import pytest

from sf6_ingest.config import load_character
from sf6_ingest.core.common import sha256_bytes
from sf6_ingest.core.io import save_snapshot
from sf6_ingest.schemas import SnapshotMetadata
from sf6_ingest.versioning import SCHEMA_VERSION


FIXTURES_DIR = Path(__file__).parent / "fixtures"
SOURCE_URLS = {
    "official": {
        "jp": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
        "luke": "https://www.streetfighter.com/6/ja-jp/character/luke/frame",
    },
    "supercombo": {
        "jp": "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data",
        "luke": "https://wiki.supercombo.gg/w/Street_Fighter_6/Luke/Data",
    },
}


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def temp_repo_root(tmp_path: Path) -> Path:
    return tmp_path / "repo"


def fixture_html(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES_DIR / name).read_bytes()


def build_snapshot_metadata(
    *,
    source: str,
    character_slug: str = "jp",
    snapshot_id: str,
    raw_bytes: bytes,
    fetched_at: str,
    success: bool,
    page_locale: str,
    source_url: str | None = None,
    page_title: str | None = None,
    challenge_detected: bool = False,
    error_message: str | None = None,
    response_encoding: str | None = "utf-8",
) -> SnapshotMetadata:
    return SnapshotMetadata.model_validate(
        {
            "schema_version": SCHEMA_VERSION,
            "source": source,
            "character_slug": character_slug,
            "snapshot_id": snapshot_id,
            "source_url": source_url or _default_source_url(source, character_slug),
            "final_url": source_url or _default_source_url(source, character_slug),
            "fetched_at": fetched_at,
            "page_locale": page_locale,
            "success": success,
            "fetcher_name": "test_fixture",
            "status_code": 200 if success else 503,
            "timeout_ms": 1000,
            "retry_count": 0,
            "retry_delay_ms": 0,
            "wait_ms": 0,
            "network_idle": source == "supercombo",
            "solve_cloudflare": source == "supercombo",
            "response_encoding": response_encoding,
            "page_title": page_title,
            "challenge_detected": challenge_detected,
            "raw_sha256": sha256_bytes(raw_bytes),
            "raw_bytes": len(raw_bytes),
            "raw_payload_filename": "",
            "metadata_filename": "",
            "error_message": error_message,
        }
    )


def _default_source_url(source: str, character_slug: str) -> str:
    if character_slug in SOURCE_URLS.get(source, {}):
        return SOURCE_URLS[source][character_slug]
    character = load_character(character_slug)
    if source == "official":
        return character.sources["official"]
    return character.sources["supercombo_data"]


def save_html_snapshot(
    repo_root: Path,
    *,
    source: str,
    character_slug: str = "jp",
    snapshot_id: str,
    html: str,
    fetched_at: str,
    success: bool = True,
    page_locale: str | None = None,
    challenge_detected: bool = False,
    error_message: str | None = None,
    page_title: str = "fixture",
    response_encoding: str | None = "utf-8",
) -> SnapshotMetadata:
    raw_bytes = html.encode(response_encoding or "utf-8")
    metadata = build_snapshot_metadata(
        source=source,
        character_slug=character_slug,
        snapshot_id=snapshot_id,
        raw_bytes=raw_bytes,
        fetched_at=fetched_at,
        success=success,
        page_locale=page_locale or ("ja-jp" if source == "official" else "en"),
        challenge_detected=challenge_detected,
        error_message=error_message,
        response_encoding=response_encoding,
        page_title=page_title,
    )
    return save_snapshot(repo_root, raw_bytes, metadata).metadata


def save_fixture_snapshot(
    repo_root: Path,
    *,
    source: str,
    character_slug: str = "jp",
    snapshot_id: str,
    fixture_name: str,
    fetched_at: str,
    success: bool = True,
    page_locale: str | None = None,
    challenge_detected: bool = False,
    error_message: str | None = None,
    response_encoding: str | None = "utf-8",
) -> SnapshotMetadata:
    return save_html_snapshot(
        repo_root,
        source=source,
        character_slug=character_slug,
        snapshot_id=snapshot_id,
        html=fixture_html(fixture_name),
        fetched_at=fetched_at,
        success=success,
        page_locale=page_locale,
        challenge_detected=challenge_detected,
        error_message=error_message,
        page_title="fixture",
        response_encoding=response_encoding,
    )
