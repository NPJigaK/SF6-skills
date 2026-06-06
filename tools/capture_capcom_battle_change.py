#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from scrapling.fetchers import Fetcher


PUBLISHER = "Capcom"
GAME = "Street Fighter 6"
LOCALE = "ja-jp"
SOURCE_TYPE = "official_battle_change"
BASE_ORIGIN = "https://www.streetfighter.com"
ASSET_PREFIX = "/6/buckler"
PUBLIC_BASE_URL = f"{BASE_ORIGIN}{ASSET_PREFIX}/{LOCALE}/battle_change"
RAW_SCHEMA_VERSION = "capcom_battle_change_raw_capture/v1"
METADATA_SCHEMA_VERSION = "capcom_battle_change_raw_capture_metadata/v1"
MANIFEST_SCHEMA_VERSION = "capcom_battle_change_raw_capture_manifest/v1"


@dataclass(frozen=True)
class VersionCapture:
    version_id: str
    title: str
    raw_dir: Path
    page_html: Path
    data_json: Path
    metadata_json: Path
    summary: dict[str, Any]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def read_text_response(url: str, *, timeout: int) -> tuple[str, dict[str, Any]]:
    page = Fetcher.get(url, stealthy_headers=True, impersonate="chrome", timeout=timeout)
    body = page.body.decode("utf-8", "replace") if isinstance(page.body, (bytes, bytearray)) else str(page.body)
    return body, {
        "url": url,
        "final_url": str(getattr(page, "url", url)),
        "status": getattr(page, "status", None),
        "byte_count": len(body.encode("utf-8")),
        "sha256": sha256_text(body),
    }


def extract_next_data(page_html: str) -> dict[str, Any]:
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        page_html,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("page HTML does not contain __NEXT_DATA__")
    return json.loads(html.unescape(match.group(1)))


def adjust_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if "pageProps" in payload:
        page_props = payload["pageProps"]
    else:
        page_props = payload.get("props", {}).get("pageProps", {})
    adjust = page_props.get("adjust")
    if not isinstance(adjust, dict):
        raise ValueError("payload does not contain pageProps.adjust")
    return adjust


def build_data_url(build_id: str, version_id: str, *, locale: str = LOCALE, asset_prefix: str = ASSET_PREFIX) -> str:
    return f"{BASE_ORIGIN}{asset_prefix}/_next/data/{build_id}/{locale}/battle_change/{version_id}.json"


def build_discovery_data_url(build_id: str, *, locale: str = LOCALE, asset_prefix: str = ASSET_PREFIX) -> str:
    return f"{BASE_ORIGIN}{asset_prefix}/_next/data/{build_id}/{locale}/battle_change.json"


def build_public_url(version_id: str | None = None) -> str:
    if version_id:
        return f"{PUBLIC_BASE_URL}/{version_id}"
    return PUBLIC_BASE_URL


def require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"adjust.{field_name} must be a list")
    return value


def require_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    return value


def validate_body_items(items: list[Any], path: str) -> int:
    count = 0
    for item_index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"{path}[{item_index}] must be an object")
        require_string(item.get("text"), f"{path}[{item_index}].text")
        category = item.get("category", "")
        if category is not None and not isinstance(category, str):
            raise ValueError(f"{path}[{item_index}].category must be a string")
        count += 1
    return count


def validate_adjust_payload(adjust: dict[str, Any], *, expected_version: str | None = None) -> dict[str, Any]:
    title = require_string(adjust.get("title"), "adjust.title")
    current_version = require_string(adjust.get("current_version"), "adjust.current_version")
    if expected_version and current_version != expected_version:
        raise ValueError(f"current_version mismatch: expected {expected_version}, got {current_version}")

    versions = require_list(adjust.get("versions"), "versions")
    if not versions:
        raise ValueError("adjust.versions must not be empty")
    for version_index, version in enumerate(versions):
        if not isinstance(version, dict):
            raise ValueError(f"adjust.versions[{version_index}] must be an object")
        require_string(version.get("id"), f"adjust.versions[{version_index}].id")
        require_string(version.get("title"), f"adjust.versions[{version_index}].title")

    policy = require_list(adjust.get("policy"), "policy")
    for item_index, item in enumerate(policy):
        if not isinstance(item, dict):
            raise ValueError(f"adjust.policy[{item_index}] must be an object")
        require_string(item.get("title"), f"adjust.policy[{item_index}].title")
        require_string(item.get("text"), f"adjust.policy[{item_index}].text")

    common_change_count = 0
    common = require_list(adjust.get("common"), "common")
    for section_index, section in enumerate(common):
        if not isinstance(section, dict):
            raise ValueError(f"adjust.common[{section_index}] must be an object")
        require_string(section.get("title"), f"adjust.common[{section_index}].title")
        body = require_list(section.get("body"), f"common[{section_index}].body")
        common_change_count += validate_body_items(body, f"adjust.common[{section_index}].body")

    fighter_detail_count = 0
    fighter_change_count = 0
    fighters = require_list(adjust.get("fighter"), "fighter")
    for fighter_index, fighter in enumerate(fighters):
        if not isinstance(fighter, dict):
            raise ValueError(f"adjust.fighter[{fighter_index}] must be an object")
        require_string(fighter.get("fighter_id"), f"adjust.fighter[{fighter_index}].fighter_id")
        require_string(fighter.get("fighter_tool_name"), f"adjust.fighter[{fighter_index}].fighter_tool_name")
        details = require_list(fighter.get("detail"), f"fighter[{fighter_index}].detail")
        fighter_detail_count += len(details)
        for detail_index, detail in enumerate(details):
            if not isinstance(detail, dict):
                raise ValueError(f"adjust.fighter[{fighter_index}].detail[{detail_index}] must be an object")
            require_string(detail.get("title"), f"adjust.fighter[{fighter_index}].detail[{detail_index}].title")
            body = require_list(
                detail.get("body"),
                f"fighter[{fighter_index}].detail[{detail_index}].body",
            )
            fighter_change_count += validate_body_items(
                body,
                f"adjust.fighter[{fighter_index}].detail[{detail_index}].body",
            )

    fighter_list = require_list(adjust.get("fighter_list"), "fighter_list")

    return {
        "version_id": current_version,
        "title": title,
        "policy_count": len(policy),
        "common_section_count": len(common),
        "common_change_count": common_change_count,
        "fighter_count": len(fighters),
        "fighter_detail_count": fighter_detail_count,
        "fighter_change_count": fighter_change_count,
        "version_count": len(versions),
        "fighter_list_count": len(fighter_list),
    }


def version_items(adjust: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"id": str(item["id"]), "title": str(item["title"])}
        for item in require_list(adjust.get("versions"), "versions")
    ]


def capture_one_version(raw_root: Path, version_id: str, build_id: str, *, timeout: int) -> VersionCapture:
    public_url = build_public_url(version_id)
    data_url = build_data_url(build_id, version_id)
    page_html, page_response = read_text_response(public_url, timeout=timeout)
    data_text, data_response = read_text_response(data_url, timeout=timeout)
    html_payload = extract_next_data(page_html)
    data_payload = json.loads(data_text)
    html_adjust = adjust_from_payload(html_payload)
    data_adjust = adjust_from_payload(data_payload)
    if html_adjust != data_adjust:
        raise ValueError(f"HTML __NEXT_DATA__ adjust does not match data JSON for {version_id}")
    summary = validate_adjust_payload(data_adjust, expected_version=version_id)

    raw_dir = raw_root / "versions" / version_id
    page_html_path = raw_dir / "page.html"
    data_json_path = raw_dir / "data.json"
    metadata_path = raw_dir / "metadata.json"

    write_text(page_html_path, page_html)
    write_text(data_json_path, data_text)
    metadata = {
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "captured_at_utc": utc_now(),
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_type": SOURCE_TYPE,
        "version_id": version_id,
        "title": summary["title"],
        "source_url": public_url,
        "data_url": data_url,
        "build_id": build_id,
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "capture_method": "scrapling_fetcher_chrome_impersonation",
        "validation_summary": summary,
        "responses": {
            "page_html": page_response,
            "data_json": data_response,
        },
        "artifacts": {
            "page_html": {
                "path": "page.html",
                "sha256": sha256_file(page_html_path),
                "byte_count": page_html_path.stat().st_size,
            },
            "data_json": {
                "path": "data.json",
                "sha256": sha256_file(data_json_path),
                "byte_count": data_json_path.stat().st_size,
            },
        },
    }
    write_json(metadata_path, metadata)

    return VersionCapture(
        version_id=version_id,
        title=summary["title"],
        raw_dir=raw_dir,
        page_html=page_html_path,
        data_json=data_json_path,
        metadata_json=metadata_path,
        summary=summary,
    )


def capture_discovery(raw_root: Path, *, timeout: int) -> tuple[dict[str, Any], dict[str, Any]]:
    page_html, page_response = read_text_response(build_public_url(), timeout=timeout)
    next_payload = extract_next_data(page_html)
    build_id = require_string(next_payload.get("buildId"), "__NEXT_DATA__.buildId")
    data_url = build_discovery_data_url(build_id)
    data_text, data_response = read_text_response(data_url, timeout=timeout)
    data_payload = json.loads(data_text)
    html_adjust = adjust_from_payload(next_payload)
    data_adjust = adjust_from_payload(data_payload)
    if html_adjust != data_adjust:
        raise ValueError("discovery HTML __NEXT_DATA__ adjust does not match discovery data JSON")
    summary = validate_adjust_payload(data_adjust, expected_version=data_adjust.get("current_version"))

    raw_dir = raw_root / "discovery"
    page_html_path = raw_dir / "page.html"
    data_json_path = raw_dir / "data.json"
    metadata_path = raw_dir / "metadata.json"
    write_text(page_html_path, page_html)
    write_text(data_json_path, data_text)
    metadata = {
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "captured_at_utc": utc_now(),
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_type": SOURCE_TYPE,
        "source_url": build_public_url(),
        "data_url": data_url,
        "build_id": build_id,
        "current_version": summary["version_id"],
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "capture_method": "scrapling_fetcher_chrome_impersonation",
        "validation_summary": summary,
        "responses": {
            "page_html": page_response,
            "data_json": data_response,
        },
        "artifacts": {
            "page_html": {
                "path": "page.html",
                "sha256": sha256_file(page_html_path),
                "byte_count": page_html_path.stat().st_size,
            },
            "data_json": {
                "path": "data.json",
                "sha256": sha256_file(data_json_path),
                "byte_count": data_json_path.stat().st_size,
            },
        },
    }
    write_json(metadata_path, metadata)
    return next_payload, metadata


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def capture_all(repo_root: Path, *, timeout: int, delay_seconds: float, dry_run: bool) -> dict[str, Any]:
    raw_root = repo_root / "raw" / "battle-change" / "official"
    if dry_run:
        page_html, _ = read_text_response(build_public_url(), timeout=timeout)
        next_payload = extract_next_data(page_html)
        adjust = adjust_from_payload(next_payload)
        summary = validate_adjust_payload(adjust, expected_version=adjust.get("current_version"))
        return {
            "dry_run": True,
            "build_id": next_payload.get("buildId"),
            "current_version": summary["version_id"],
            "versions": version_items(adjust),
            "summary": summary,
        }

    next_payload, discovery_metadata = capture_discovery(raw_root, timeout=timeout)
    build_id = require_string(next_payload.get("buildId"), "__NEXT_DATA__.buildId")
    discovery_adjust = adjust_from_payload(next_payload)
    versions = version_items(discovery_adjust)
    captures: list[VersionCapture] = []
    for index, version in enumerate(versions):
        if index and delay_seconds > 0:
            time.sleep(delay_seconds)
        captures.append(capture_one_version(raw_root, version["id"], build_id, timeout=timeout))

    created_at_utc = utc_now()
    manifest = {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "created_at_utc": created_at_utc,
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_type": SOURCE_TYPE,
        "source_url": build_public_url(),
        "data_url": build_discovery_data_url(build_id),
        "build_id": build_id,
        "current_version": discovery_metadata["current_version"],
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "storage_policy": "latest_battle_change_mirror",
        "capture_label": created_at_utc[:10],
        "version_count": len(captures),
        "versions": versions,
        "discovery": {
            "raw_dir": relative(raw_root / "discovery", repo_root),
            "page_html": relative(raw_root / "discovery" / "page.html", repo_root),
            "data_json": relative(raw_root / "discovery" / "data.json", repo_root),
            "metadata_json": relative(raw_root / "discovery" / "metadata.json", repo_root),
            "summary": discovery_metadata["validation_summary"],
        },
        "captures": [
            {
                "version_id": capture.version_id,
                "title": capture.title,
                "raw_dir": relative(capture.raw_dir, repo_root),
                "page_html": relative(capture.page_html, repo_root),
                "data_json": relative(capture.data_json, repo_root),
                "metadata_json": relative(capture.metadata_json, repo_root),
                "summary": capture.summary,
            }
            for capture in captures
        ],
        "tool": "tools/capture_capcom_battle_change.py",
    }
    write_json(raw_root / "manifest.json", manifest)
    return {
        "dry_run": False,
        "manifest": relative(raw_root / "manifest.json", repo_root),
        "build_id": build_id,
        "current_version": discovery_metadata["current_version"],
        "version_count": len(captures),
        "versions": versions,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--delay-seconds", type=float, default=0.25)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = capture_all(
        args.repo_root.resolve(),
        timeout=args.timeout,
        delay_seconds=args.delay_seconds,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
