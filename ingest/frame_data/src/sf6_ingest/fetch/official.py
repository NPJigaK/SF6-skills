from __future__ import annotations

from ..config import CharacterConfig, FetchProfile
from ..schemas import SnapshotMetadata
from ..versioning import SCHEMA_VERSION
from .scrapling_client import build_snapshot_id, fetch_with_profile


def fetch_official_snapshot(character: CharacterConfig, profile: FetchProfile) -> tuple[bytes, SnapshotMetadata]:
    result = fetch_with_profile(character.sources["official"], profile)
    metadata = SnapshotMetadata.model_validate(
        {
            "schema_version": SCHEMA_VERSION,
            "source": "official",
            "character_slug": character.character_slug,
            "snapshot_id": build_snapshot_id(result.fetched_at, result.raw_sha256),
            "source_url": character.sources["official"],
            "final_url": result.final_url,
            "fetched_at": result.fetched_at,
            "page_locale": profile.page_locale,
            "success": bool(result.raw_bytes)
            and not result.challenge_detected
            and (result.status_code is None or result.status_code < 400),
            "fetcher_name": profile.fetcher_name,
            "status_code": result.status_code,
            "timeout_ms": profile.timeout_ms,
            "retry_count": profile.retry_count,
            "retry_delay_ms": profile.retry_delay_ms,
            "wait_ms": profile.wait_ms,
            "network_idle": profile.network_idle,
            "solve_cloudflare": profile.solve_cloudflare,
            "response_encoding": result.response_encoding,
            "page_title": result.page_title,
            "challenge_detected": result.challenge_detected,
            "raw_sha256": result.raw_sha256,
            "raw_bytes": result.raw_bytes_count,
            "raw_payload_filename": "",
            "metadata_filename": "",
            "error_message": result.error_message,
        }
    )
    return result.raw_bytes, metadata
