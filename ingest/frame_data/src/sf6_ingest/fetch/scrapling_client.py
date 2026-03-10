from __future__ import annotations

import inspect
import time
from dataclasses import dataclass

from scrapling import Fetcher, StealthyFetcher
from scrapling.engines.static import CurlSession
from selectolax.parser import HTMLParser

from ..config import FetchProfile
from ..core.common import compact_text, sha256_bytes, timestamp_token


@dataclass(frozen=True)
class ScraplingFetchResult:
    raw_bytes: bytes
    fetched_at: str
    final_url: str | None
    status_code: int | None
    response_encoding: str | None
    page_title: str | None
    challenge_detected: bool
    raw_sha256: str
    raw_bytes_count: int
    error_message: str | None


def build_snapshot_id(fetched_at: str, raw_sha256: str) -> str:
    return f"{timestamp_token(fetched_at)}-{raw_sha256[:8]}"


def fetch_with_profile(url: str, profile: FetchProfile) -> ScraplingFetchResult:
    last_error: Exception | None = None
    attempts = max(profile.retry_count, 0) + 1
    for attempt in range(1, attempts + 1):
        try:
            response = _perform_fetch(url, profile)
            encoding = getattr(response, "encoding", None)
            response_body = getattr(response, "body", None)
            if response_body is None:
                response_body = getattr(response, "content", b"")
            raw_bytes = _response_body_to_bytes(response_body, encoding)
            decoded = _decode_for_metadata(raw_bytes, encoding)
            title = _extract_title(decoded)
            challenge_detected = _has_challenge(decoded, title, profile.challenge_markers)
            status_code = getattr(response, "status", None)
            if status_code is None:
                status_code = getattr(response, "status_code", None)
            return ScraplingFetchResult(
                raw_bytes=raw_bytes,
                fetched_at=_fetched_at(),
                final_url=str(getattr(response, "url", url)),
                status_code=status_code,
                response_encoding=encoding,
                page_title=title,
                challenge_detected=challenge_detected,
                raw_sha256=sha256_bytes(raw_bytes),
                raw_bytes_count=len(raw_bytes),
                error_message=None,
            )
        except Exception as exc:  # pragma: no cover - exercised by integration behavior
            last_error = exc
            if attempt < attempts and profile.retry_delay_ms > 0:
                time.sleep(profile.retry_delay_ms / 1000.0)

    error_message = str(last_error) if last_error else "unknown fetch failure"
    raw_bytes = b""
    fetched_at = _fetched_at()
    return ScraplingFetchResult(
        raw_bytes=raw_bytes,
        fetched_at=fetched_at,
        final_url=url,
        status_code=None,
        response_encoding=None,
        page_title=None,
        challenge_detected=False,
        raw_sha256=sha256_bytes(raw_bytes),
        raw_bytes_count=0,
        error_message=error_message,
    )


def _perform_fetch(url: str, profile: FetchProfile):
    if profile.fetcher_name == "Fetcher":
        session = CurlSession()
        try:
            return session.get(
                url,
                timeout=profile.timeout_ms / 1000.0,
                impersonate="chrome",
            )
        finally:
            session.close()

    kwargs = {
        "url": url,
        "timeout": profile.timeout_ms,
        "wait": profile.wait_ms,
        "network_idle": profile.network_idle,
        "wait_selector": profile.wait_selector,
        "custom_config": {"huge_tree": True},
    }
    signature = inspect.signature(StealthyFetcher.fetch)
    if "solve_cloudflare" in signature.parameters:
        kwargs["solve_cloudflare"] = profile.solve_cloudflare
    return StealthyFetcher.fetch(**{key: value for key, value in kwargs.items() if value is not None})


def _decode_for_metadata(raw_bytes: bytes, encoding: str | None) -> str:
    if not raw_bytes:
        return ""
    try:
        return raw_bytes.decode(encoding or "utf-8", errors="replace")
    except LookupError:
        return raw_bytes.decode("utf-8", errors="replace")


def _response_body_to_bytes(body, encoding: str | None) -> bytes:
    if body is None:
        return b""
    if isinstance(body, bytes):
        return body
    if isinstance(body, bytearray):
        return bytes(body)
    if isinstance(body, str):
        return body.encode(encoding or "utf-8")
    return str(body).encode(encoding or "utf-8")


def _extract_title(decoded_html: str) -> str | None:
    if not decoded_html:
        return None
    tree = HTMLParser(decoded_html)
    title = tree.css_first("title")
    return compact_text(title.text(separator=" ", strip=True) if title else None)


def _has_challenge(decoded_html: str, title: str | None, markers: list[str]) -> bool:
    haystack = " ".join(filter(None, [title, decoded_html]))
    return any(marker and marker in haystack for marker in markers)


def _fetched_at() -> str:
    from ..core.common import utc_now

    return utc_now()
