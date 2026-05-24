from __future__ import annotations

import argparse
import json
import re
import sys
import time
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from .paths import repo_root


REPORT_JSON_HEADER = "## Machine Report"
REPORT_JSON_FENCE = "```json"
LOCAL_PATH_PATTERN = re.compile(
    r"(?i)(?:/"
    r"home/"
    r"|/"
    r"mnt/[a-z]/"
    r"|/"
    r"Users/"
    r"|(?:^|[\s\"'`(])[A-Z]:[\\/]"
    r"|\\\\Users\\\\)"
)
REPO_LOCAL_RAW_ARTIFACT_BOUNDARY = "repo_local_ignored_raw_capture"
REPO_LOCAL_REVIEWER_EVIDENCE_BOUNDARY = "repo_local_ignored_reviewer_evidence"


def repo_local_raw_workspace_root() -> Path:
    return repo_root() / ".local" / "source-acquisition"


def repo_local_reviewer_evidence_root() -> Path:
    return repo_root() / ".local" / "reviewer-evidence"


@dataclass(frozen=True)
class RosterCharacter:
    character_slug: str
    display_name: str
    official_url: str | None
    supercombo_url: str | None


@dataclass(frozen=True)
class FetchResult:
    content: bytes
    final_url: str
    http_status: int
    content_type: str
    content_length: int | None
    etag: str | None
    last_modified: str | None
    failure_reason: str | None = None
    capture_method: str = "scrapling_fetcher"


def load_roster(path: Path | None = None) -> list[RosterCharacter]:
    roster_path = path or repo_root() / "data" / "roster" / "current-character-roster.json"
    payload = json.loads(roster_path.read_text(encoding="utf-8"))
    characters = []
    for item in payload.get("characters", []):
        sources = item.get("sources", {})
        characters.append(
            RosterCharacter(
                character_slug=item["character_slug"],
                display_name=item["display_name"],
                official_url=sources.get("official"),
                supercombo_url=sources.get("supercombo_data"),
            )
        )
    return characters


def default_workspace(run_id: str) -> Path:
    return repo_local_raw_workspace_root() / "current-source-acquisition" / run_id


def ensure_acquisition_workspace(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    repo_local_root = repo_local_raw_workspace_root().resolve()
    if resolved != repo_local_root and repo_local_root not in resolved.parents:
        raise ValueError(
            "Acquisition workspace must stay under repo-local ignored "
            f"{repo_local_raw_workspace_root().as_posix()}: {resolved}"
        )
    return resolved


def ensure_reviewer_evidence_workspace(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    repo_local_root = repo_local_reviewer_evidence_root().resolve()
    if resolved != repo_local_root and repo_local_root not in resolved.parents:
        raise ValueError(
            "Reviewer evidence workspace must stay under repo-local ignored "
            f"{repo_local_reviewer_evidence_root().as_posix()}: {resolved}"
        )
    return resolved


def current_run_id(now: datetime | None = None) -> str:
    value = now or datetime.now(UTC)
    return value.strftime("%Y%m%dT%H%M%SZ")


def utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_url(url: str, timeout: float = 30.0) -> FetchResult:
    try:
        from scrapling.fetchers import Fetcher
    except ImportError as exc:
        raise RuntimeError(
            "Scrapling is required for source acquisition. "
            'Install it with: uv pip install "scrapling[all]>=0.4.8,<0.5"'
        ) from exc

    try:
        page = Fetcher.get(
            url,
            stealthy_headers=True,
            impersonate="chrome",
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - exercised by live acquisition
        return FetchResult(
            content=b"",
            final_url=url,
            http_status=0,
            content_type="unknown",
            content_length=None,
            etag=None,
            last_modified=None,
            failure_reason=f"Scrapling Fetcher.get failed: {exc}",
        )

    content = _page_body(page)
    headers = getattr(page, "headers", {}) or {}
    return FetchResult(
        content=content,
        final_url=str(getattr(page, "url", url) or url),
        http_status=int(getattr(page, "status", None) or getattr(page, "status_code", 0) or 0),
        content_type=_header_value(headers, "Content-Type") or "unknown",
        content_length=_header_int(_header_value(headers, "Content-Length")),
        etag=_header_value(headers, "ETag"),
        last_modified=_header_value(headers, "Last-Modified"),
    )


def fetch_supercombo_url(url: str, timeout: float = 90_000.0) -> FetchResult:
    try:
        from scrapling.fetchers import StealthyFetcher
    except ImportError as exc:
        raise RuntimeError(
            "Scrapling is required for SuperCombo source acquisition. "
            'Install it with: uv pip install "scrapling[all]>=0.4.8,<0.5"'
        ) from exc

    try:
        page = StealthyFetcher.fetch(
            url,
            headless=True,
            network_idle=True,
            wait_selector="main table",
            wait=1000,
            timeout=timeout,
            solve_cloudflare=True,
        )
    except Exception as exc:  # pragma: no cover - exercised by live acquisition
        return FetchResult(
            content=b"",
            final_url=url,
            http_status=0,
            content_type="unknown",
            content_length=None,
            etag=None,
            last_modified=None,
            failure_reason=f"Scrapling StealthyFetcher.fetch failed: {exc}",
            capture_method="scrapling_stealthy_fetcher",
        )

    content = _page_body(page)
    headers = getattr(page, "headers", {}) or {}
    return FetchResult(
        content=content,
        final_url=str(getattr(page, "url", url) or url),
        http_status=int(getattr(page, "status", None) or getattr(page, "status_code", 0) or 0),
        content_type=_header_value(headers, "Content-Type") or "unknown",
        content_length=_header_int(_header_value(headers, "Content-Length")),
        etag=_header_value(headers, "ETag"),
        last_modified=_header_value(headers, "Last-Modified"),
        capture_method="scrapling_stealthy_fetcher",
    )


def acquire_official_sources(
    *,
    report_path: Path,
    workspace: Path | None = None,
    run_id: str | None = None,
    roster_path: Path | None = None,
    fetcher: Callable[[str], FetchResult] = fetch_url,
    supercombo_fetcher: Callable[[str], FetchResult] = fetch_supercombo_url,
    include_supercombo: bool = False,
    sleep_seconds: float = 0.0,
) -> dict[str, Any]:
    run = run_id or current_run_id()
    raw_workspace = ensure_acquisition_workspace(workspace or default_workspace(run))
    official_workspace = raw_workspace / "official"
    supercombo_workspace = raw_workspace / "supercombo"
    official_workspace.mkdir(parents=True, exist_ok=True)
    if include_supercombo:
        supercombo_workspace.mkdir(parents=True, exist_ok=True)

    characters = load_roster(roster_path)
    report_captured_at = utc_timestamp()
    entries: list[dict[str, Any]] = []
    review_items: list[str] = []

    for index, character in enumerate(characters):
        captured_at = utc_timestamp()
        if not character.official_url:
            entries.append(_missing_official_entry(character, captured_at))
            review_items.append(f"{character.character_slug}: missing sources.official")
            continue

        result = fetcher(character.official_url)
        content_hash = None
        if result.content:
            content_hash = "sha256:" + sha256(result.content).hexdigest()
            character_dir = official_workspace / character.character_slug
            character_dir.mkdir(parents=True, exist_ok=True)
            (character_dir / "page.html").write_bytes(result.content)
            official_artifacts = _write_official_artifacts(
                character=character,
                source_url=character.official_url,
                result=result,
                character_dir=character_dir,
                captured_at=captured_at,
                content_hash=content_hash,
            )
        else:
            official_artifacts = _empty_official_artifacts()

        success, failure_reason = _capture_status(character.official_url, result)
        artifact_review_items = _official_artifact_review_items(character.character_slug, official_artifacts)
        if success and artifact_review_items:
            success = False
            failure_reason = "; ".join(artifact_review_items)
        if not success:
            review_items.append(f"{character.character_slug}: {failure_reason}")

        entries.append(
            {
                "character_slug": character.character_slug,
                "display_name": character.display_name,
                "source_family": "official",
                "source_role": "current_fact_authority_candidate",
                "source_url": character.official_url,
                "final_url": result.final_url,
                "captured_at_utc": captured_at,
                "http_status": result.http_status,
                "content_type": result.content_type,
                "content_length": len(result.content) if result.content else result.content_length,
                "source_version_label": "unknown",
                "source_revision_label": result.etag or result.last_modified or "unknown",
                "capture_method": result.capture_method,
                "capture_success": success,
                "failure_reason": None if success else failure_reason,
                "content_hash": content_hash,
                "artifact_boundary": REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
                "metadata_hash": official_artifacts["metadata_hash"],
                "official_next_data_present": official_artifacts["next_data_present"],
                "official_next_data_hash": official_artifacts["next_data_hash"],
                "official_table_count": official_artifacts["table_count"],
                "official_raw_row_count": official_artifacts["raw_row_count"],
                "official_table_rows_schema_version": official_artifacts["table_rows_schema_version"],
                "official_row_note_rows": official_artifacts["row_note_rows"],
                "official_row_note_count": official_artifacts["row_note_count"],
                "official_header_missing": official_artifacts["header_missing"],
                "official_header_path_violations": official_artifacts["header_path_violations"],
                "official_row_cell_count_violations": official_artifacts["row_cell_count_violations"],
                "official_table_rows_hash": official_artifacts["table_rows_hash"],
            }
        )

        if sleep_seconds and index < len(characters) - 1:
            time.sleep(sleep_seconds)

    if include_supercombo:
        for index, character in enumerate(characters):
            captured_at = utc_timestamp()
            if not character.supercombo_url:
                entries.append(_missing_supercombo_entry(character, captured_at))
                review_items.append(f"supercombo:{character.character_slug}: missing sources.supercombo_data")
                continue

            result = supercombo_fetcher(character.supercombo_url)
            content_hash = None
            if result.content:
                content_hash = "sha256:" + sha256(result.content).hexdigest()
                character_dir = supercombo_workspace / character.character_slug
                character_dir.mkdir(parents=True, exist_ok=True)
                (character_dir / "page.html").write_bytes(result.content)
                supercombo_artifacts = _write_supercombo_artifacts(
                    character=character,
                    source_url=character.supercombo_url,
                    result=result,
                    character_dir=character_dir,
                    captured_at=captured_at,
                    content_hash=content_hash,
                )
            else:
                supercombo_artifacts = _empty_supercombo_artifacts()

            success, failure_reason = _supercombo_capture_status(character.supercombo_url, result)
            artifact_review_items = _supercombo_artifact_review_items(character.character_slug, supercombo_artifacts)
            if success and artifact_review_items:
                success = False
                failure_reason = "; ".join(artifact_review_items)
            if not success:
                review_items.append(f"supercombo:{character.character_slug}: {failure_reason}")

            entries.append(
                {
                    "character_slug": character.character_slug,
                    "display_name": character.display_name,
                    "source_family": "supercombo",
                    "source_role": "enrichment_candidate",
                    "source_url": character.supercombo_url,
                    "final_url": result.final_url,
                    "captured_at_utc": captured_at,
                    "http_status": result.http_status,
                    "content_type": result.content_type,
                    "content_length": len(result.content) if result.content else result.content_length,
                    "source_version_label": "unknown",
                    "source_revision_label": result.etag or result.last_modified or "unknown",
                    "capture_method": result.capture_method,
                    "capture_success": success,
                    "failure_reason": None if success else failure_reason,
                    "content_hash": content_hash,
                    "artifact_boundary": REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
                    "metadata_hash": supercombo_artifacts["metadata_hash"],
                    "supercombo_table_count": supercombo_artifacts["table_count"],
                    "supercombo_raw_row_count": supercombo_artifacts["raw_row_count"],
                    "supercombo_tables_hash": supercombo_artifacts["tables_hash"],
                }
            )

            if sleep_seconds and index < len(characters) - 1:
                time.sleep(sleep_seconds)

    official_entries = [entry for entry in entries if entry["source_family"] == "official"]
    official_captured_count = sum(1 for entry in official_entries if entry["capture_success"])
    official_failed_count = len(official_entries) - official_captured_count
    supercombo_entries = [entry for entry in entries if entry["source_family"] == "supercombo"]
    supercombo_captured_count = sum(1 for entry in supercombo_entries if entry["capture_success"])
    supercombo_failed_count = len(supercombo_entries) - supercombo_captured_count
    report = {
        "run_id": run,
        "captured_at_utc": report_captured_at,
        "source_families": ["official"] + (["supercombo"] if include_supercombo else []),
        "roster": {
            "roster_path": "data/roster/current-character-roster.json",
            "expected_character_count": len(characters),
        },
        "official_coverage": {
            "expected_count": len(characters),
            "captured_count": official_captured_count,
            "failed_count": official_failed_count,
            "review_item_count": sum(1 for item in review_items if not item.startswith("supercombo:")),
            "official_raw_row_count": sum(int(entry.get("official_raw_row_count") or 0) for entry in official_entries),
            "official_table_count": sum(int(entry.get("official_table_count") or 0) for entry in official_entries),
            "official_row_note_rows": sum(int(entry.get("official_row_note_rows") or 0) for entry in official_entries),
            "official_row_note_count": sum(int(entry.get("official_row_note_count") or 0) for entry in official_entries),
        },
        "supercombo_decision": {
            "status": "same_run_approved" if include_supercombo else "queued",
            "reason": "SuperCombo captured in the same run as enrichment/cross-reference/candidate evidence only."
            if include_supercombo
            else "Default scope is latest official acquisition only; SuperCombo remains queued for a later approved implementation.",
        },
        "supercombo_coverage": {
            "expected_count": len(characters) if include_supercombo else 0,
            "captured_count": supercombo_captured_count,
            "failed_count": supercombo_failed_count,
            "review_item_count": sum(1 for item in review_items if item.startswith("supercombo:")),
            "supercombo_table_count": sum(int(entry.get("supercombo_table_count") or 0) for entry in supercombo_entries),
            "supercombo_raw_row_count": sum(int(entry.get("supercombo_raw_row_count") or 0) for entry in supercombo_entries),
        },
        "source_boundary": {
            "full_raw_html_public_commit": "prohibited_without_explicit_review",
            "reviewed_terms_license_robots_attribution": "pending",
        },
        "entries": entries,
        "review_items": review_items,
    }

    report_text = render_acquisition_report(report)
    validate_acquisition_report_text(report_text, roster_characters=characters)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    return report


def render_acquisition_report(report: dict[str, Any]) -> str:
    coverage = report["official_coverage"]
    supercombo_coverage = report.get("supercombo_coverage", {})
    lines = [
        "# Current Source Acquisition Report",
        "",
        "This report records latest source acquisition metadata and extracted artifact counts only.",
        "Raw source documents are preserved in the repo-local ignored acquisition workspace and are not included here.",
        "",
        f"- Run ID: `{report['run_id']}`",
        f"- Captured at UTC: `{report['captured_at_utc']}`",
        f"- Source families: `{', '.join(report['source_families'])}`",
        f"- Expected official characters: `{coverage['expected_count']}`",
        f"- Captured official characters: `{coverage['captured_count']}`",
        f"- Failed official characters: `{coverage['failed_count']}`",
        f"- Official raw rows: `{coverage.get('official_raw_row_count', 0)}`",
        f"- Official tables: `{coverage.get('official_table_count', 0)}`",
        f"- Official row-note rows: `{coverage.get('official_row_note_rows', 0)}`",
        f"- Official row notes: `{coverage.get('official_row_note_count', 0)}`",
        f"- Captured SuperCombo characters: `{supercombo_coverage.get('captured_count', 0)}`",
        f"- Failed SuperCombo characters: `{supercombo_coverage.get('failed_count', 0)}`",
        f"- SuperCombo tables: `{supercombo_coverage.get('supercombo_table_count', 0)}`",
        f"- Review items: `{len(report['review_items'])}`",
        f"- SuperCombo status: `{report['supercombo_decision']['status']}`",
        f"- Full raw HTML public commit: `{report['source_boundary']['full_raw_html_public_commit']}`",
        f"- Source-boundary review: `{report['source_boundary']['reviewed_terms_license_robots_attribution']}`",
        "",
        REPORT_JSON_HEADER,
        "",
        REPORT_JSON_FENCE,
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Review Items",
        "",
    ]
    if report["review_items"]:
        lines.extend(f"- {item}" for item in report["review_items"])
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Boundary Notes",
            "",
            "- This report is not daily-answer authority.",
            "- Official captures remain authority candidates until later parser, schema, validator, and review gates pass.",
            "- SuperCombo remains enrichment/cross-reference/candidate evidence only and is not numeric authority in this run.",
        ]
    )
    return "\n".join(lines) + "\n"


def load_acquisition_report(report_path: Path) -> dict[str, Any]:
    return extract_report_json(report_path.read_text(encoding="utf-8"))


def extract_report_json(report_text: str) -> dict[str, Any]:
    marker_index = report_text.find(REPORT_JSON_HEADER)
    if marker_index < 0:
        raise ValueError("Report lacks Machine Report section")
    fence_start = report_text.find(REPORT_JSON_FENCE, marker_index)
    if fence_start < 0:
        raise ValueError("Report lacks JSON fence")
    json_start = report_text.find("\n", fence_start)
    if json_start < 0:
        raise ValueError("Report JSON fence is malformed")
    fence_end = report_text.find("\n```", json_start)
    if fence_end < 0:
        raise ValueError("Report JSON fence is not closed")
    return json.loads(report_text[json_start:fence_end])


def validate_acquisition_report(report_path: Path, roster_path: Path | None = None) -> list[str]:
    report_text = report_path.read_text(encoding="utf-8")
    return validate_acquisition_report_text(report_text, roster_characters=load_roster(roster_path))


def validate_acquisition_artifacts(
    report_path: Path,
    *,
    workspace: Path | None = None,
    roster_path: Path | None = None,
) -> list[str]:
    validate_acquisition_report(report_path, roster_path)
    report = load_acquisition_report(report_path)
    raw_workspace = ensure_acquisition_workspace(workspace or default_workspace(str(report["run_id"])))
    errors = _validate_artifact_integrity(report, raw_workspace, load_roster(roster_path))
    if errors:
        raise ValueError("\n".join(errors))
    return []


def validate_acquisition_report_text(
    report_text: str,
    *,
    roster_characters: list[RosterCharacter],
) -> list[str]:
    errors: list[str] = []
    errors.extend(_forbidden_report_content_errors(report_text))
    try:
        report = extract_report_json(report_text)
    except (json.JSONDecodeError, ValueError) as exc:
        return [f"Invalid acquisition report JSON: {exc}"] + errors

    errors.extend(_validate_report_structure(report, roster_characters))
    errors.extend(_forbidden_json_value_errors(report))
    if errors:
        raise ValueError("\n".join(errors))
    return []


def prepare_official_note_linkage_review_bundle(
    *,
    report_path: Path,
    output_dir: Path | None = None,
    run_id: str | None = None,
    slugs: list[str] | None = None,
    screenshotter: Callable[[str, Path], str] | None = None,
) -> dict[str, Any]:
    report = load_acquisition_report(report_path)
    bundle_id = run_id or f"{report['run_id']}-official-note-linkage"
    root = ensure_reviewer_evidence_workspace(
        output_dir or repo_local_reviewer_evidence_root() / "official-note-linkage" / bundle_id
    )
    root.mkdir(parents=True, exist_ok=True)
    screenshots_dir = root / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    selected_slugs = set(slugs or [])
    capture = screenshotter or _scrapling_official_full_page_screenshot
    targets = []
    for entry in report.get("entries", []):
        if entry.get("source_family") != "official" or entry.get("capture_success") is not True:
            continue
        slug = str(entry["character_slug"])
        if selected_slugs and slug not in selected_slugs:
            continue
        screenshot_path = screenshots_dir / f"{slug}-full-page.png"
        final_url = capture(str(entry["source_url"]), screenshot_path)
        targets.append(
            {
                "character_slug": slug,
                "source_url": entry["source_url"],
                "final_url": final_url,
                "screenshot": f"screenshots/{screenshot_path.name}",
                "official_row_note_rows": entry.get("official_row_note_rows", 0),
                "official_row_note_count": entry.get("official_row_note_count", 0),
            }
        )

    manifest = {
        "bundle_schema_version": "official_note_linkage_reviewer_bundle/v1",
        "evidence_boundary": REPO_LOCAL_REVIEWER_EVIDENCE_BOUNDARY,
        "source_run_id": report["run_id"],
        "bundle_id": bundle_id,
        "screenshot_method": "scrapling_dynamic_fetcher_page_action",
        "chatgpt_result_status": "observation_candidate_only",
        "forbidden_uses": [
            "validator_evidence",
            "source_truth",
            "parser_schema_approval",
            "calculation_safe_promotion",
            "numeric_authority",
        ],
        "targets": targets,
    }
    manifest_path = root / "manifest.json"
    prompt_path = root / "chatgpt-check-prompt.md"
    _write_json(manifest_path, manifest)
    prompt_path.write_text(_official_note_linkage_chatgpt_prompt(manifest), encoding="utf-8")

    zip_path = root.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(root))
    return {
        "ok": True,
        "bundle_id": bundle_id,
        "target_count": len(targets),
        "bundle_dir": str(root),
        "zip_path": str(zip_path),
    }


def _scrapling_official_full_page_screenshot(url: str, output_path: Path) -> str:
    try:
        from scrapling.fetchers import DynamicFetcher
    except ImportError as exc:
        raise RuntimeError(
            "Scrapling is required for reviewer screenshot bundles. "
            'Install it with: uv pip install "scrapling[all]>=0.4.8,<0.5"'
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)

    def capture(page: Any) -> None:
        page.screenshot(path=str(output_path), full_page=True)

    page = DynamicFetcher.fetch(
        url,
        headless=True,
        network_idle=True,
        wait_selector="table",
        wait=1000,
        timeout=90_000,
        page_action=capture,
    )
    return str(getattr(page, "url", url) or url)


def _official_note_linkage_chatgpt_prompt(manifest: dict[str, Any]) -> str:
    target_lines = "\n".join(
        f"- {target['character_slug']}: {target['source_url']} -> {target['screenshot']}"
        for target in manifest["targets"]
    )
    return (
        "# Official Note Linkage Screenshot Review\n\n"
        "You are reviewing SF6 official frame-data screenshots as an external observation aid only.\n"
        "Do not treat your response as source truth, validator evidence, parser/schema approval, "
        "calculation-safe promotion, or numeric authority.\n\n"
        "For each screenshot, inspect the official frame-data table and row-local notes. Report only "
        "whether visible row notes appear consistent with the row-note fields described by the accompanying "
        "manifest. Mark uncertain cases as observation_candidate review items.\n\n"
        "Targets:\n"
        f"{target_lines}\n\n"
        "Return a concise table with character_slug, screenshot, observation_candidate_status, and notes.\n"
    )


def _validate_report_structure(report: dict[str, Any], roster_characters: list[RosterCharacter]) -> list[str]:
    errors: list[str] = []
    roster_slugs = {character.character_slug for character in roster_characters}
    entries = report.get("entries")
    if not isinstance(entries, list):
        return ["Report entries must be a list"]

    official_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("source_family") == "official"]
    supercombo_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("source_family") == "supercombo"]
    errors.extend(_coverage_errors("official", official_entries, roster_slugs, required=True))
    errors.extend(
        _coverage_errors(
            "supercombo",
            supercombo_entries,
            roster_slugs,
            required="supercombo" in set(report.get("source_families", [])),
        )
    )

    expected_count = report.get("roster", {}).get("expected_character_count")
    if expected_count != len(roster_characters):
        errors.append(f"Expected character count must be {len(roster_characters)}, got {expected_count}")

    coverage = report.get("official_coverage", {})
    if coverage.get("expected_count") != len(roster_characters):
        errors.append("official_coverage.expected_count must match roster count")
    if coverage.get("captured_count", 0) + coverage.get("failed_count", 0) != len(roster_characters):
        errors.append("captured_count + failed_count must equal roster count")
    errors.extend(
        _coverage_aggregate_errors(
            "official_coverage",
            coverage,
            official_entries,
            review_items=report.get("review_items", []),
            review_item_prefix=None,
            aggregate_fields={
                "official_table_count": "official_table_count",
                "official_raw_row_count": "official_raw_row_count",
                "official_row_note_rows": "official_row_note_rows",
                "official_row_note_count": "official_row_note_count",
            },
        )
    )
    if "supercombo" in set(report.get("source_families", [])):
        supercombo_coverage = report.get("supercombo_coverage", {})
        if supercombo_coverage.get("expected_count") != len(roster_characters):
            errors.append("supercombo_coverage.expected_count must match roster count")
        if supercombo_coverage.get("captured_count", 0) + supercombo_coverage.get("failed_count", 0) != len(roster_characters):
            errors.append("supercombo captured_count + failed_count must equal roster count")
        errors.extend(
            _coverage_aggregate_errors(
                "supercombo_coverage",
                supercombo_coverage,
                supercombo_entries,
                review_items=report.get("review_items", []),
                review_item_prefix="supercombo:",
                aggregate_fields={
                    "supercombo_table_count": "supercombo_table_count",
                    "supercombo_raw_row_count": "supercombo_raw_row_count",
                },
            )
        )

    review_items = report.get("review_items", [])
    if not isinstance(review_items, list):
        errors.append("review_items must be a list")
        review_items = []
    review_text = "\n".join(str(item) for item in review_items)
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Every report entry must be an object")
            continue
        source_family = entry.get("source_family")
        if source_family not in {"official", "supercombo"}:
            errors.append(f"{entry.get('character_slug')}: source_family must be official or supercombo")
        expected_role = "current_fact_authority_candidate" if source_family == "official" else "enrichment_candidate"
        if entry.get("source_role") != expected_role:
            errors.append(f"{entry.get('character_slug')}: source_role must be {expected_role}")
        if entry.get("artifact_boundary") != REPO_LOCAL_RAW_ARTIFACT_BOUNDARY:
            errors.append(
                f"{entry.get('character_slug')}: artifact_boundary must be {REPO_LOCAL_RAW_ARTIFACT_BOUNDARY}"
            )
        expected_method = "scrapling_fetcher" if source_family == "official" else "scrapling_stealthy_fetcher"
        if entry.get("capture_method") != expected_method:
            errors.append(f"{entry.get('character_slug')}: capture_method must be {expected_method}")
        if source_family == "official" and entry.get("capture_success") is True:
            if int(entry.get("official_raw_row_count") or 0) <= 0:
                errors.append(f"{entry.get('character_slug')}: successful official capture requires raw rows")
            if int(entry.get("official_table_count") or 0) <= 0:
                errors.append(f"{entry.get('character_slug')}: successful official capture requires table count")
            if entry.get("official_table_rows_schema_version") != OFFICIAL_TABLE_ROWS_SCHEMA_VERSION:
                errors.append(
                    f"{entry.get('character_slug')}: official_table_rows_schema_version "
                    f"must be {OFFICIAL_TABLE_ROWS_SCHEMA_VERSION}"
                )
            if int(entry.get("official_row_note_rows") or 0) < 0:
                errors.append(f"{entry.get('character_slug')}: official_row_note_rows must be non-negative")
            if int(entry.get("official_row_note_count") or 0) < 0:
                errors.append(f"{entry.get('character_slug')}: official_row_note_count must be non-negative")
        if source_family == "supercombo" and entry.get("capture_success") is True:
            if int(entry.get("supercombo_table_count") or 0) <= 0:
                errors.append(f"{entry.get('character_slug')}: successful SuperCombo capture requires table count")
            if int(entry.get("supercombo_raw_row_count") or 0) <= 0:
                errors.append(f"{entry.get('character_slug')}: successful SuperCombo capture requires raw rows")
        if entry.get("capture_success") is not True:
            failure_reason = entry.get("failure_reason")
            slug = str(entry.get("character_slug"))
            if not failure_reason:
                errors.append(f"{slug}: failed capture requires failure_reason")
            review_key = f"supercombo:{slug}" if source_family == "supercombo" else slug
            if review_key not in review_text:
                errors.append(f"{review_key}: failed capture requires matching review item")

    source_boundary = report.get("source_boundary", {})
    if source_boundary.get("full_raw_html_public_commit") != "prohibited_without_explicit_review":
        errors.append("full_raw_html_public_commit must be prohibited_without_explicit_review")
    if source_boundary.get("reviewed_terms_license_robots_attribution") not in {"pending", "reviewed"}:
        errors.append("source-boundary review status must be pending or reviewed")

    supercombo_status = report.get("supercombo_decision", {}).get("status")
    if supercombo_status not in {"queued", "same_run_approved", "blocked"}:
        errors.append("SuperCombo status must be queued, same_run_approved, or blocked")

    return errors


def _coverage_errors(source_family: str, entries: list[dict[str, Any]], roster_slugs: set[str], *, required: bool) -> list[str]:
    if not required:
        return []
    entry_slugs = {entry.get("character_slug") for entry in entries}
    errors: list[str] = []
    if entry_slugs != roster_slugs:
        missing = sorted(roster_slugs - entry_slugs)
        extra = sorted(slug for slug in entry_slugs - roster_slugs if slug)
        if missing:
            errors.append(f"Report lacks {source_family} roster entries: {', '.join(missing)}")
        if extra:
            errors.append(f"Report includes non-roster {source_family} entries: {', '.join(extra)}")
    return errors


def _coverage_aggregate_errors(
    label: str,
    coverage: dict[str, Any],
    entries: list[dict[str, Any]],
    *,
    review_items: Any,
    review_item_prefix: str | None,
    aggregate_fields: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    captured_count = sum(1 for entry in entries if entry.get("capture_success") is True)
    failed_count = len(entries) - captured_count
    if coverage.get("captured_count") != captured_count:
        errors.append(f"{label}.captured_count must match successful entries: {captured_count}")
    if coverage.get("failed_count") != failed_count:
        errors.append(f"{label}.failed_count must match failed entries: {failed_count}")

    if isinstance(review_items, list):
        if review_item_prefix is None:
            review_item_count = sum(1 for item in review_items if not str(item).startswith("supercombo:"))
        else:
            review_item_count = sum(1 for item in review_items if str(item).startswith(review_item_prefix))
        if coverage.get("review_item_count") != review_item_count:
            errors.append(f"{label}.review_item_count must match review_items: {review_item_count}")

    for coverage_key, entry_key in aggregate_fields.items():
        expected_total = sum(int(entry.get(entry_key) or 0) for entry in entries)
        if coverage.get(coverage_key) != expected_total:
            errors.append(f"{label}.{coverage_key} must match entry aggregate: {expected_total}")
    return errors


def _validate_artifact_integrity(
    report: dict[str, Any],
    raw_workspace: Path,
    roster_characters: list[RosterCharacter],
) -> list[str]:
    errors: list[str] = []
    entries = [entry for entry in report.get("entries", []) if isinstance(entry, dict)]
    roster_slugs = {character.character_slug for character in roster_characters}
    official_entries = [entry for entry in entries if entry.get("source_family") == "official"]
    supercombo_entries = [entry for entry in entries if entry.get("source_family") == "supercombo"]
    errors.extend(_coverage_errors("official artifact", official_entries, roster_slugs, required=True))
    errors.extend(
        _coverage_errors(
            "SuperCombo artifact",
            supercombo_entries,
            roster_slugs,
            required="supercombo" in set(report.get("source_families", [])),
        )
    )

    for entry in entries:
        source_family = entry.get("source_family")
        if entry.get("capture_success") is not True:
            continue
        if source_family == "official":
            errors.extend(_validate_official_artifacts(raw_workspace, entry))
        elif source_family == "supercombo":
            errors.extend(_validate_supercombo_artifacts(raw_workspace, entry))
    return errors


def _validate_official_artifacts(raw_workspace: Path, entry: dict[str, Any]) -> list[str]:
    slug = str(entry.get("character_slug"))
    character_dir = raw_workspace / "official" / slug
    errors = _validate_common_artifacts(character_dir, entry)

    if entry.get("official_next_data_present"):
        errors.extend(
            _validate_artifact_hash(
                character_dir / "__NEXT_DATA__.json",
                entry.get("official_next_data_hash"),
                f"{slug}: __NEXT_DATA__.json",
            )
        )
    elif entry.get("official_next_data_hash"):
        errors.append(f"{slug}: official_next_data_hash present but official_next_data_present is false")

    table_rows_path = character_dir / "official_table_rows.raw.json"
    errors.extend(
        _validate_artifact_hash(
            table_rows_path,
            entry.get("official_table_rows_hash"),
            f"{slug}: official_table_rows.raw.json",
        )
    )
    table_payload = _read_json_if_available(table_rows_path, f"{slug}: official_table_rows.raw.json", errors)
    if isinstance(table_payload, dict):
        if table_payload.get("artifact_schema_version") != OFFICIAL_TABLE_ROWS_SCHEMA_VERSION:
            errors.append(f"{slug}: artifact_schema_version must be {OFFICIAL_TABLE_ROWS_SCHEMA_VERSION}")
        if table_payload.get("expected_column_header_paths") != EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS:
            errors.append(f"{slug}: expected_column_header_paths must match official contract")
        if table_payload.get("column_header_paths") != EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS:
            errors.append(f"{slug}: column_header_paths must match official contract")
        if table_payload.get("header_path_violations"):
            errors.append(f"{slug}: official header path violations must be empty")
        if table_payload.get("table_count") != entry.get("official_table_count"):
            errors.append(f"{slug}: official table_count does not match report")
        if table_payload.get("raw_row_count") != entry.get("official_raw_row_count"):
            errors.append(f"{slug}: official raw_row_count does not match report")
        if table_payload.get("row_note_rows") != entry.get("official_row_note_rows"):
            errors.append(f"{slug}: official row_note_rows does not match report")
        if table_payload.get("row_note_count") != entry.get("official_row_note_count"):
            errors.append(f"{slug}: official row_note_count does not match report")
        rows = table_payload.get("rows")
        if isinstance(rows, list) and len(rows) != entry.get("official_raw_row_count"):
            errors.append(f"{slug}: official rows length does not match report")
        if isinstance(rows, list):
            errors.extend(_official_cell_payload_errors(slug, rows))
    return errors


def _official_cell_payload_errors(slug: str, rows: list[Any]) -> list[str]:
    errors: list[str] = []
    required_row_keys = {
        "table_index",
        "row_index",
        "group_heading",
        "cell_count",
        "input_images",
        "row_note_count",
        "row_notes",
        "row_note_extraction_status",
    }
    required_cell_keys = {
        "cell_index",
        "column_index",
        "source_column_header_path",
        "source_column_leaf_header",
        "source_text",
        "source_text_stripped",
        "visible_text",
        "hidden_detail_text",
        "image_src",
        "image_alt",
        "cell_note_markers",
        "cell_note_ids",
        "row_note_reference_candidates",
        "note_linkage_status",
    }
    for row_index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"{slug}: official row {row_index} must be an object")
            continue
        missing_row_keys = sorted(required_row_keys - set(row))
        if missing_row_keys:
            errors.append(f"{slug}: official row {row_index} missing fields: {', '.join(missing_row_keys)}")
        input_images = row.get("input_images")
        if not isinstance(input_images, list):
            errors.append(f"{slug}: official row {row_index} input_images must be a list")
        else:
            for image_index, image in enumerate(input_images):
                if not isinstance(image, dict):
                    errors.append(f"{slug}: official row {row_index} input image {image_index} must be an object")
                    continue
                missing_image_keys = sorted({"src", "alt"} - set(image))
                if missing_image_keys:
                    errors.append(
                        f"{slug}: official row {row_index} input image {image_index} missing fields: "
                        f"{', '.join(missing_image_keys)}"
                    )
        row_notes = row.get("row_notes")
        if not isinstance(row_notes, list):
            errors.append(f"{slug}: official row {row_index} row_notes must be a list")
            row_notes = []
        if row.get("row_note_count") != len(row_notes):
            errors.append(f"{slug}: official row {row_index} row_note_count must match row_notes length")
        expected_status = "notes_extracted" if row_notes else "no_row_notes"
        if row.get("row_note_extraction_status") != expected_status:
            errors.append(f"{slug}: official row {row_index} row_note_extraction_status must be {expected_status}")
        errors.extend(_official_row_note_payload_errors(slug, row_index, row_notes))
        cells = row.get("cells")
        if not isinstance(cells, list):
            errors.append(f"{slug}: official row {row_index} cells must be a list")
            continue
        if row.get("cell_count") != len(cells):
            errors.append(f"{slug}: official row {row_index} cell_count must match cells length")
        for cell_index, cell in enumerate(cells):
            if not isinstance(cell, dict):
                errors.append(f"{slug}: official row {row_index} cell {cell_index} must be an object")
                continue
            missing = sorted(required_cell_keys - set(cell))
            if missing:
                errors.append(
                    f"{slug}: official row {row_index} cell {cell_index} missing fields: {', '.join(missing)}"
                )
            if not isinstance(cell.get("image_src"), list):
                errors.append(f"{slug}: official row {row_index} cell {cell_index} image_src must be a list")
            if not isinstance(cell.get("image_alt"), list):
                errors.append(f"{slug}: official row {row_index} cell {cell_index} image_alt must be a list")
            if not isinstance(cell.get("cell_note_markers"), list):
                errors.append(f"{slug}: official row {row_index} cell {cell_index} cell_note_markers must be a list")
            if not isinstance(cell.get("cell_note_ids"), list):
                errors.append(f"{slug}: official row {row_index} cell {cell_index} cell_note_ids must be a list")
            if not isinstance(cell.get("row_note_reference_candidates"), list):
                errors.append(
                    f"{slug}: official row {row_index} cell {cell_index} row_note_reference_candidates must be a list"
                )
            if cell.get("note_linkage_status") not in OFFICIAL_NOTE_LINKAGE_STATUSES:
                errors.append(
                    f"{slug}: official row {row_index} cell {cell_index} note_linkage_status "
                    "must be a known source-structural status"
                )
            expected_path = (
                EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS[cell_index]
                if cell_index < len(EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS)
                else []
            )
            if cell.get("column_index") != cell_index:
                errors.append(f"{slug}: official row {row_index} cell {cell_index} column_index must match cell index")
            if cell.get("source_column_header_path") != expected_path:
                errors.append(
                    f"{slug}: official row {row_index} cell {cell_index} source_column_header_path "
                    f"must be {expected_path}"
                )
            expected_leaf = expected_path[-1] if expected_path else ""
            if cell.get("source_column_leaf_header") != expected_leaf:
                errors.append(
                    f"{slug}: official row {row_index} cell {cell_index} source_column_leaf_header "
                    f"must be {expected_leaf}"
                )
            if "text_stripped" in cell:
                errors.append(f"{slug}: official row {row_index} cell {cell_index} must not use text_stripped")
    return errors


def _official_row_note_payload_errors(slug: str, row_index: int, row_notes: list[Any]) -> list[str]:
    errors: list[str] = []
    required_note_keys = {
        "note_index",
        "note_marker",
        "note_id",
        "note_text",
        "note_text_stripped",
        "note_source_scope",
        "source_order",
    }
    for note_index, note in enumerate(row_notes):
        if not isinstance(note, dict):
            errors.append(f"{slug}: official row {row_index} note {note_index} must be an object")
            continue
        missing = sorted(required_note_keys - set(note))
        if missing:
            errors.append(f"{slug}: official row {row_index} note {note_index} missing fields: {', '.join(missing)}")
        if note.get("note_index") != note_index:
            errors.append(f"{slug}: official row {row_index} note {note_index} note_index must match source order")
        if note.get("source_order") != note_index:
            errors.append(f"{slug}: official row {row_index} note {note_index} source_order must match source order")
        if note.get("note_source_scope") != OFFICIAL_ROW_NOTE_SOURCE_SCOPE:
            errors.append(
                f"{slug}: official row {row_index} note {note_index} note_source_scope "
                f"must be {OFFICIAL_ROW_NOTE_SOURCE_SCOPE}"
            )
        note_text = note.get("note_text")
        if not isinstance(note_text, str) or not note_text:
            errors.append(f"{slug}: official row {row_index} note {note_index} note_text must be non-empty text")
        if note.get("note_text_stripped") != _normalize_text(note_text or ""):
            errors.append(f"{slug}: official row {row_index} note {note_index} note_text_stripped must be normalized")
        if note.get("note_marker") is not None and not isinstance(note.get("note_marker"), str):
            errors.append(f"{slug}: official row {row_index} note {note_index} note_marker must be text or null")
        if note.get("note_id") is not None and not isinstance(note.get("note_id"), str):
            errors.append(f"{slug}: official row {row_index} note {note_index} note_id must be text or null")
    return errors


def _validate_supercombo_artifacts(raw_workspace: Path, entry: dict[str, Any]) -> list[str]:
    slug = str(entry.get("character_slug"))
    character_dir = raw_workspace / "supercombo" / slug
    errors = _validate_common_artifacts(character_dir, entry)

    tables_path = character_dir / "supercombo_tables.raw.json"
    errors.extend(
        _validate_artifact_hash(
            tables_path,
            entry.get("supercombo_tables_hash"),
            f"{slug}: supercombo_tables.raw.json",
        )
    )
    tables_payload = _read_json_if_available(tables_path, f"{slug}: supercombo_tables.raw.json", errors)
    if isinstance(tables_payload, dict):
        if tables_payload.get("table_count") != entry.get("supercombo_table_count"):
            errors.append(f"{slug}: SuperCombo table_count does not match report")
        if tables_payload.get("raw_row_count") != entry.get("supercombo_raw_row_count"):
            errors.append(f"{slug}: SuperCombo raw_row_count does not match report")
        tables = tables_payload.get("tables")
        if isinstance(tables, list) and len(tables) != entry.get("supercombo_table_count"):
            errors.append(f"{slug}: SuperCombo tables length does not match report")
    return errors


def _validate_common_artifacts(character_dir: Path, entry: dict[str, Any]) -> list[str]:
    slug = str(entry.get("character_slug"))
    errors: list[str] = []
    errors.extend(_validate_artifact_hash(character_dir / "page.html", entry.get("content_hash"), f"{slug}: page.html"))
    metadata_path = character_dir / "metadata.json"
    errors.extend(_validate_artifact_hash(metadata_path, entry.get("metadata_hash"), f"{slug}: metadata.json"))
    metadata = _read_json_if_available(metadata_path, f"{slug}: metadata.json", errors)
    if isinstance(metadata, dict):
        for key in (
            "character_slug",
            "source_family",
            "source_url",
            "final_url",
            "http_status",
            "content_hash",
            "capture_method",
            "artifact_boundary",
        ):
            if metadata.get(key) != entry.get(key):
                errors.append(f"{slug}: metadata.{key} does not match report")
    return errors


def _validate_artifact_hash(path: Path, expected_hash: Any, label: str) -> list[str]:
    if not expected_hash:
        return [f"{label} hash missing from report"]
    if not path.exists():
        return [f"{label} missing"]
    if not path.is_file():
        return [f"{label} is not a file"]
    actual_hash = _file_hash(path)
    if actual_hash != expected_hash:
        return [f"{label} hash mismatch: expected {expected_hash}, got {actual_hash}"]
    return []


def _read_json_if_available(path: Path, label: str, errors: list[str]) -> Any | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label} invalid JSON: {exc}")
        return None


def _forbidden_report_content_errors(report_text: str) -> list[str]:
    checks = {
        "local absolute path": LOCAL_PATH_PATTERN,
        "browser profile path": re.compile(r"(?i)(?:AppData|Google/Chrome|google-chrome|browser profile|Default/Cookies)"),
        "cookie header": re.compile(r"(?im)^\s*(?:set-cookie|cookie)\s*:"),
        "authorization header": re.compile(r"(?im)^\s*authorization\s*:"),
        "bearer token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{12,}"),
        "token assignment": re.compile(r"(?i)\b(?:access_token|auth_token|api_key|secret)\s*[:=]\s*[A-Za-z0-9._~+/=-]{8,}"),
        "private vault reference": re.compile(r"(?i)\bprivate[-_ ]?vault\b"),
        "answer log reference": re.compile(r"(?i)\banswer[-_ ]?log"),
        "training log reference": re.compile(r"(?i)\btraining[-_ ]?log"),
        "real user profile reference": re.compile(r"(?i)\breal[-_ ]?user[-_ ]?profile\b"),
        "raw HTML": re.compile(r"(?i)<!doctype\s+html|<html\b|<head\b|<body\b|<script\b"),
        "raw source dump": re.compile(r"(?i)\b(?:source_rows|source-rows|raw_value|page\.html|\.har|\.mhtml)\b"),
    }
    return [f"Forbidden report content: {label}" for label, pattern in checks.items() if pattern.search(report_text)]


def _forbidden_json_value_errors(value: Any) -> list[str]:
    errors: list[str] = []

    def walk(item: Any, path: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                normalized_key = str(key).lower()
                if normalized_key in {"raw_html", "raw_content", "source_rows", "raw_value"}:
                    errors.append(f"Forbidden report field: {path}.{key}")
                walk(child, f"{path}.{key}")
        elif isinstance(item, list):
            for index, child in enumerate(item):
                walk(child, f"{path}[{index}]")
        elif isinstance(item, str):
            if LOCAL_PATH_PATTERN.search(item):
                errors.append(f"Forbidden local path in report field: {path}")

    walk(value, "report")
    return errors


EXPECTED_OFFICIAL_CELL_COUNT = 15
OFFICIAL_TABLE_ROWS_SCHEMA_VERSION = "official_table_rows_raw/v4"
OFFICIAL_ROW_NOTE_SOURCE_SCOPE = "row_local_note"
OFFICIAL_NOTE_LINKAGE_STATUSES = {
    "no_cell_note_markers",
    "no_row_notes",
    "same_row_note_candidates_available",
    "ambiguous_marker_without_id",
    "no_matching_row_note_candidate",
}
OFFICIAL_BRACKETED_NOTE_ID_RE = re.compile(r"[\[［]([※＊*]\d+)[\]］]")
OFFICIAL_LEADING_NOTE_ID_RE = re.compile(r"^([※＊*]\d+)(?:\s|　)")
EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS = [
    ["技名"],
    ["動作フレーム", "発生"],
    ["動作フレーム", "持続"],
    ["動作フレーム", "硬直"],
    ["硬直差", "ヒット"],
    ["硬直差", "ガード"],
    ["キャンセル"],
    ["ダメージ"],
    ["コンボ補正値"],
    ["Dゲージ増加", "ヒット"],
    ["Dゲージ減少", "ガード"],
    ["Dゲージ減少", "パニッシュカウンター"],
    ["SAゲージ増加"],
    ["属性"],
    ["備考"],
]
OFFICIAL_HEADER_MARKERS = [
    "技名",
    "動作フレーム",
    "発生",
    "持続",
    "硬直",
    "硬直差",
    "ヒット",
    "ガード",
    "キャンセル",
    "ダメージ",
    "コンボ補正値",
    "Dゲージ増加",
    "Dゲージ減少",
    "パニッシュカウンター",
    "SAゲージ増加",
    "属性",
    "備考",
]


def _write_official_artifacts(
    *,
    character: RosterCharacter,
    source_url: str,
    result: FetchResult,
    character_dir: Path,
    captured_at: str,
    content_hash: str,
) -> dict[str, Any]:
    soup = _soup(result.content)
    next_data_hash = None
    next_data_present = False
    next_data = _extract_next_data(soup)
    if next_data is not None:
        next_data_present = True
        next_data_hash = _write_json(character_dir / "__NEXT_DATA__.json", next_data)

    raw_rows = _extract_official_table_rows(soup)
    table_rows_payload = {
        "artifact_schema_version": OFFICIAL_TABLE_ROWS_SCHEMA_VERSION,
        "character_slug": character.character_slug,
        "source_family": "official",
        "source_role": "current_fact_authority_candidate",
        "source_url": source_url,
        "final_url": result.final_url,
        "captured_at_utc": captured_at,
        "expected_cell_count": EXPECTED_OFFICIAL_CELL_COUNT,
        "expected_header_markers": OFFICIAL_HEADER_MARKERS,
        "expected_column_header_paths": EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS,
        "header_text": raw_rows["header_text"],
        "header_missing": raw_rows["header_missing"],
        "header_structures": raw_rows["header_structures"],
        "column_header_paths": raw_rows["column_header_paths"],
        "header_path_violations": raw_rows["header_path_violations"],
        "table_count": raw_rows["table_count"],
        "raw_row_count": len(raw_rows["rows"]),
        "row_note_rows": raw_rows["row_note_rows"],
        "row_note_count": raw_rows["row_note_count"],
        "row_cell_count_violations": raw_rows["row_cell_count_violations"],
        "rows": raw_rows["rows"],
    }
    table_rows_hash = _write_json(character_dir / "official_table_rows.raw.json", table_rows_payload)

    metadata = _base_metadata(character, "official", source_url, result, captured_at, content_hash)
    metadata.update(
        {
            "next_data_present": next_data_present,
            "next_data_hash": next_data_hash,
            "official_table_count": raw_rows["table_count"],
            "official_raw_row_count": len(raw_rows["rows"]),
            "official_table_rows_schema_version": OFFICIAL_TABLE_ROWS_SCHEMA_VERSION,
            "official_row_note_rows": raw_rows["row_note_rows"],
            "official_row_note_count": raw_rows["row_note_count"],
            "official_header_missing": raw_rows["header_missing"],
            "official_header_path_violations": raw_rows["header_path_violations"],
            "official_row_cell_count_violations": raw_rows["row_cell_count_violations"],
            "official_table_rows_hash": table_rows_hash,
        }
    )
    metadata_hash = _write_json(character_dir / "metadata.json", metadata)
    return {
        "metadata_hash": metadata_hash,
        "next_data_present": next_data_present,
        "next_data_hash": next_data_hash,
        "table_count": raw_rows["table_count"],
        "raw_row_count": len(raw_rows["rows"]),
        "table_rows_schema_version": OFFICIAL_TABLE_ROWS_SCHEMA_VERSION,
        "row_note_rows": raw_rows["row_note_rows"],
        "row_note_count": raw_rows["row_note_count"],
        "header_missing": raw_rows["header_missing"],
        "header_path_violations": raw_rows["header_path_violations"],
        "row_cell_count_violations": raw_rows["row_cell_count_violations"],
        "table_rows_hash": table_rows_hash,
    }


def _write_supercombo_artifacts(
    *,
    character: RosterCharacter,
    source_url: str,
    result: FetchResult,
    character_dir: Path,
    captured_at: str,
    content_hash: str,
) -> dict[str, Any]:
    soup = _soup(result.content)
    raw_tables = _extract_supercombo_tables(soup)
    tables_payload = {
        "artifact_schema_version": "supercombo_tables_raw/v1",
        "character_slug": character.character_slug,
        "source_family": "supercombo",
        "source_role": "enrichment_candidate",
        "source_url": source_url,
        "final_url": result.final_url,
        "captured_at_utc": captured_at,
        "table_count": raw_tables["table_count"],
        "raw_row_count": raw_tables["raw_row_count"],
        "tables": raw_tables["tables"],
    }
    tables_hash = _write_json(character_dir / "supercombo_tables.raw.json", tables_payload)

    metadata = _base_metadata(character, "supercombo", source_url, result, captured_at, content_hash)
    metadata.update(
        {
            "supercombo_table_count": raw_tables["table_count"],
            "supercombo_raw_row_count": raw_tables["raw_row_count"],
            "supercombo_tables_hash": tables_hash,
        }
    )
    metadata_hash = _write_json(character_dir / "metadata.json", metadata)
    return {
        "metadata_hash": metadata_hash,
        "table_count": raw_tables["table_count"],
        "raw_row_count": raw_tables["raw_row_count"],
        "tables_hash": tables_hash,
    }


def _base_metadata(
    character: RosterCharacter,
    source_family: str,
    source_url: str,
    result: FetchResult,
    captured_at: str,
    content_hash: str,
) -> dict[str, Any]:
    return {
        "metadata_schema_version": "source_snapshot_metadata/v1",
        "character_slug": character.character_slug,
        "display_name": character.display_name,
        "source_family": source_family,
        "source_url": source_url,
        "final_url": result.final_url,
        "captured_at_utc": captured_at,
        "http_status": result.http_status,
        "content_type": result.content_type,
        "content_length": len(result.content) if result.content else result.content_length,
        "content_hash": content_hash,
        "capture_method": result.capture_method,
        "artifact_boundary": REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
        "source_version_label": "unknown",
        "source_revision_label": result.etag or result.last_modified or "unknown",
    }


def _empty_official_artifacts() -> dict[str, Any]:
    return {
        "metadata_hash": None,
        "next_data_present": False,
        "next_data_hash": None,
        "table_count": 0,
        "raw_row_count": 0,
        "table_rows_schema_version": OFFICIAL_TABLE_ROWS_SCHEMA_VERSION,
        "row_note_rows": 0,
        "row_note_count": 0,
        "header_missing": OFFICIAL_HEADER_MARKERS,
        "header_path_violations": ["missing official header paths"],
        "row_cell_count_violations": [],
        "table_rows_hash": None,
    }


def _empty_supercombo_artifacts() -> dict[str, Any]:
    return {
        "metadata_hash": None,
        "table_count": 0,
        "raw_row_count": 0,
        "tables_hash": None,
    }


def _official_artifact_review_items(character_slug: str, artifacts: dict[str, Any]) -> list[str]:
    items = []
    if int(artifacts["table_count"]) <= 0:
        items.append(f"{character_slug}: missing official table")
    if int(artifacts["raw_row_count"]) <= 0:
        items.append(f"{character_slug}: missing official raw rows")
    if artifacts["header_missing"]:
        items.append(f"{character_slug}: official header drift missing={','.join(artifacts['header_missing'])}")
    if artifacts["header_path_violations"]:
        items.append(f"{character_slug}: official header path drift")
    if artifacts["row_cell_count_violations"]:
        items.append(f"{character_slug}: official row cell count drift")
    return items


def _supercombo_artifact_review_items(character_slug: str, artifacts: dict[str, Any]) -> list[str]:
    items = []
    if int(artifacts["table_count"]) <= 0:
        items.append(f"{character_slug}: missing SuperCombo tables")
    if int(artifacts["raw_row_count"]) <= 0:
        items.append(f"{character_slug}: missing SuperCombo raw rows")
    return items


def _soup(content: bytes) -> Any:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return _simple_html_tree(content)

    return BeautifulSoup(content, "html.parser")


class _SimpleHtmlNode:
    def __init__(self, name: str | None, attrs: dict[str, str] | None = None) -> None:
        self.name = name
        self.attrs = attrs or {}
        self.children: list[_SimpleHtmlNode | str] = []

    def find(self, name: str, **attrs: str) -> _SimpleHtmlNode | None:
        for node in self.find_all(name):
            if all(node.get(key) == value for key, value in attrs.items()):
                return node
        return None

    def find_all(
        self,
        names: str | list[str],
        recursive: bool = True,
    ) -> list[_SimpleHtmlNode]:
        wanted = {names} if isinstance(names, str) else set(names)
        matches = []
        children = [child for child in self.children if isinstance(child, _SimpleHtmlNode)]
        for child in children:
            if child.name in wanted:
                matches.append(child)
            if recursive:
                matches.extend(child.find_all(names, recursive=True))
        return matches

    def select(self, selector: str) -> list[_SimpleHtmlNode]:
        current = [self]
        for part in selector.split():
            next_nodes: list[_SimpleHtmlNode] = []
            for node in current:
                next_nodes.extend(node.find_all(part, recursive=True))
            current = next_nodes
        return current

    @property
    def descendants(self) -> list[_SimpleHtmlNode]:
        nodes: list[_SimpleHtmlNode] = []
        for child in self.children:
            if isinstance(child, _SimpleHtmlNode):
                nodes.append(child)
                nodes.extend(child.descendants)
        return nodes

    @property
    def string(self) -> str | None:
        return self.children[0] if len(self.children) == 1 and isinstance(self.children[0], str) else None

    def has_attr(self, name: str) -> bool:
        return name in self.attrs

    def get(self, name: str) -> str | None:
        return self.attrs.get(name)

    def get_text(self, separator: str = "", strip: bool = False) -> str:
        parts: list[str] = []

        def collect(node: _SimpleHtmlNode) -> None:
            for child in node.children:
                if isinstance(child, str):
                    text = child.strip() if strip else child
                    if text or not strip:
                        parts.append(text)
                else:
                    collect(child)

        collect(self)
        return separator.join(parts)


def _simple_html_tree(content: bytes) -> _SimpleHtmlNode:
    from html.parser import HTMLParser

    class Parser(HTMLParser):
        void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.root = _SimpleHtmlNode("document")
            self.stack = [self.root]

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            node = _SimpleHtmlNode(tag.lower(), {key: value or "" for key, value in attrs})
            self.stack[-1].children.append(node)
            if tag.lower() not in self.void_tags:
                self.stack.append(node)

        def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            self.stack[-1].children.append(_SimpleHtmlNode(tag.lower(), {key: value or "" for key, value in attrs}))

        def handle_endtag(self, tag: str) -> None:
            target = tag.lower()
            while len(self.stack) > 1:
                node = self.stack.pop()
                if node.name == target:
                    break

        def handle_data(self, data: str) -> None:
            self.stack[-1].children.append(data)

    parser = Parser()
    parser.feed(content.decode("utf-8", errors="replace"))
    parser.close()
    return parser.root


def _extract_next_data(soup: Any) -> Any | None:
    script = soup.find("script", id="__NEXT_DATA__")
    if script is None:
        return None
    text = script.string if script.string is not None else script.get_text("", strip=False)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"unparsed_text": text}


def _extract_official_table_rows(soup: Any) -> dict[str, Any]:
    tables = soup.find_all("table")
    header_texts: list[str] = []
    header_structures: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    column_header_paths: list[list[str]] = []
    header_path_violations: list[dict[str, Any]] = []
    row_cell_count_violations: list[dict[str, int]] = []

    for table_index, table in enumerate(tables):
        header_structure = _extract_official_header_structure(table, table_index)
        header_structures.append(header_structure)
        header_texts.append(header_structure["header_text"])
        if table_index == 0:
            column_header_paths = header_structure["column_header_paths"]
        header_path_violations.extend(header_structure["header_path_violations"])
        group_heading = ""
        for row_index, row in enumerate(table.select("tbody tr"), start=1):
            cells = row.find_all("td", recursive=False)
            if len(cells) == 1 and cells[0].has_attr("colspan"):
                group_heading = _visible_text(cells[0])
                continue
            if not cells:
                continue
            if len(cells) != EXPECTED_OFFICIAL_CELL_COUNT:
                row_cell_count_violations.append(
                    {"table_index": table_index, "row_index": row_index, "cell_count": len(cells)}
                )
            row_notes = _official_row_notes(cells)
            rows.append(
                {
                    "table_index": table_index,
                    "row_index": row_index,
                    "group_heading": group_heading,
                    "cell_count": len(cells),
                    "input_images": _cell_images(cells[0]) if cells else [],
                    "row_note_count": len(row_notes),
                    "row_notes": row_notes,
                    "row_note_extraction_status": "notes_extracted" if row_notes else "no_row_notes",
                    "cells": [
                        _official_cell_payload(cell, cell_index, header_structure["column_header_paths"], row_notes)
                        for cell_index, cell in enumerate(cells)
                    ],
                }
            )

    header_text = " ".join(header_texts)
    return {
        "table_count": len(tables),
        "header_text": header_text,
        "header_missing": [marker for marker in OFFICIAL_HEADER_MARKERS if marker not in header_text],
        "header_structures": header_structures,
        "column_header_paths": column_header_paths,
        "header_path_violations": header_path_violations,
        "row_cell_count_violations": row_cell_count_violations,
        "row_note_rows": sum(1 for row in rows if row["row_note_count"] > 0),
        "row_note_count": sum(int(row["row_note_count"]) for row in rows),
        "rows": rows,
    }


def _extract_official_header_structure(table: Any, table_index: int) -> dict[str, Any]:
    thead = table.find("thead")
    header_rows: list[dict[str, Any]] = []
    column_paths: list[list[str]] = []
    violations: list[dict[str, Any]] = []

    if thead is None:
        return {
            "table_index": table_index,
            "header_text": "",
            "header_rows": [],
            "column_header_paths": [],
            "header_path_violations": [{"table_index": table_index, "reason": "missing thead"}],
        }

    for header_row_index, header_row in enumerate(thead.find_all("tr", recursive=False), start=1):
        header_cells = []
        for header_cell_index, header_cell in enumerate(header_row.find_all("th", recursive=False)):
            primary_label = _official_header_primary_label(header_cell)
            child_labels = _official_header_child_labels(header_cell)
            colspan = _positive_int_attr(header_cell, "colspan", default=1)
            rowspan = _positive_int_attr(header_cell, "rowspan", default=1)
            if child_labels:
                cell_paths = [[primary_label, child_label] for child_label in child_labels]
                if len(cell_paths) != colspan:
                    violations.append(
                        {
                            "table_index": table_index,
                            "header_row_index": header_row_index,
                            "header_cell_index": header_cell_index,
                            "reason": "child label count does not match colspan",
                            "primary_label": primary_label,
                            "child_labels": child_labels,
                            "colspan": colspan,
                        }
                    )
            else:
                cell_paths = [[primary_label] for _ in range(colspan)]
                if colspan != 1:
                    violations.append(
                        {
                            "table_index": table_index,
                            "header_row_index": header_row_index,
                            "header_cell_index": header_cell_index,
                            "reason": "multi-column header lacks child labels",
                            "primary_label": primary_label,
                            "colspan": colspan,
                        }
                    )
            column_start = len(column_paths)
            column_paths.extend(cell_paths)
            header_cells.append(
                {
                    "header_cell_index": header_cell_index,
                    "primary_label": primary_label,
                    "child_labels": child_labels,
                    "source_text": header_cell.get_text("", strip=False),
                    "source_text_stripped": _normalize_text(header_cell.get_text("", strip=False)),
                    "visible_text": _official_visible_text(header_cell),
                    "rowspan": rowspan,
                    "colspan": colspan,
                    "column_start": column_start,
                    "column_span": len(cell_paths),
                    "source_column_header_paths": cell_paths,
                    "class": _class_tokens(header_cell),
                }
            )
        header_rows.append({"header_row_index": header_row_index, "cells": header_cells})

    if column_paths != EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS:
        violations.append(
            {
                "table_index": table_index,
                "reason": "column header paths do not match expected official order",
                "expected_column_header_paths": EXPECTED_OFFICIAL_COLUMN_HEADER_PATHS,
                "actual_column_header_paths": column_paths,
            }
        )

    return {
        "table_index": table_index,
        "header_text": " ".join(" > ".join(path) for path in column_paths),
        "header_rows": header_rows,
        "column_header_paths": column_paths,
        "header_path_violations": violations,
    }


def _official_header_primary_label(node: Any) -> str:
    parts: list[str] = []
    for child in getattr(node, "children", []):
        name = getattr(child, "name", None)
        if name is None:
            parts.append(str(child))
            continue
        tag_name = str(name).lower()
        if tag_name in {"ul", "div", "input", "script", "style", "noscript"}:
            continue
        parts.append(_official_visible_text(child))
    return _normalize_text(" ".join(part for part in parts if part.strip())) or _official_visible_text(node)


def _official_header_child_labels(node: Any) -> list[str]:
    labels: list[str] = []
    for child in getattr(node, "children", []):
        if str(getattr(child, "name", "")).lower() != "ul":
            continue
        for item in child.find_all("li", recursive=False):
            label = _official_header_primary_label(item)
            if label:
                labels.append(label)
    return labels


def _positive_int_attr(node: Any, name: str, *, default: int) -> int:
    try:
        value = int(node.get(name) or default)
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def _official_cell_payload(
    cell: Any,
    cell_index: int,
    column_header_paths: list[list[str]],
    row_notes: list[dict[str, Any]],
) -> dict[str, Any]:
    source_text = cell.get_text("", strip=False)
    header_path = column_header_paths[cell_index] if cell_index < len(column_header_paths) else []
    note_markers = _official_note_markers(source_text)
    note_ids = _official_note_ids(source_text)
    note_candidates = _row_note_reference_candidates(row_notes, note_markers, note_ids)
    return {
        "cell_index": cell_index,
        "column_index": cell_index,
        "source_column_header_path": header_path,
        "source_column_leaf_header": header_path[-1] if header_path else "",
        "source_text": source_text,
        "source_text_stripped": _normalize_text(source_text),
        "visible_text": _official_visible_text(cell),
        "hidden_detail_text": _official_hidden_detail_text(cell),
        "image_src": [image.get("src") for image in cell.find_all("img")],
        "image_alt": [image.get("alt") for image in cell.find_all("img")],
        "cell_note_markers": note_markers,
        "cell_note_ids": note_ids,
        "row_note_reference_candidates": note_candidates,
        "note_linkage_status": _note_linkage_status(note_markers, note_ids, row_notes, note_candidates),
    }


def _official_row_notes(cells: list[Any]) -> list[dict[str, Any]]:
    if len(cells) < EXPECTED_OFFICIAL_CELL_COUNT:
        return []
    note_cell = cells[EXPECTED_OFFICIAL_CELL_COUNT - 1]
    note_nodes = note_cell.find_all("li", recursive=True)
    if not note_nodes:
        note_text = _official_visible_text(note_cell)
        note_nodes = [note_cell] if note_text else []

    notes: list[dict[str, Any]] = []
    for note_index, node in enumerate(note_nodes):
        note_text = _official_visible_text(node)
        if not note_text:
            continue
        note_id = _official_note_id_from_note_text(note_text)
        notes.append(
            {
                "note_index": len(notes),
                "note_marker": _official_note_marker_from_text(note_text),
                "note_id": note_id,
                "note_text": note_text,
                "note_text_stripped": _normalize_text(note_text),
                "note_source_scope": OFFICIAL_ROW_NOTE_SOURCE_SCOPE,
                "source_order": len(notes),
            }
        )
    return notes


def _official_note_marker_from_text(text: str) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None
    if stripped.startswith("[") or stripped.startswith("［"):
        match = OFFICIAL_BRACKETED_NOTE_ID_RE.match(stripped)
        return _normalize_note_marker(match.group(1)[0]) if match else None
    first = stripped[0]
    return _normalize_note_marker(first) if first in {"※", "＊", "*"} else None


def _official_note_id_from_note_text(text: str) -> str | None:
    stripped = text.strip()
    bracketed_match = OFFICIAL_BRACKETED_NOTE_ID_RE.match(stripped)
    if bracketed_match:
        return _normalize_note_id(bracketed_match.group(1))
    leading_match = OFFICIAL_LEADING_NOTE_ID_RE.match(stripped)
    if leading_match:
        return _normalize_note_id(leading_match.group(1))
    return None


def _official_note_markers(text: str) -> list[str]:
    markers: list[str] = []
    for char in str(text):
        marker = _normalize_note_marker(char)
        if marker and marker not in markers:
            markers.append(marker)
    return markers


def _official_note_ids(text: str) -> list[str]:
    ids: list[str] = []
    for pattern in (OFFICIAL_BRACKETED_NOTE_ID_RE, OFFICIAL_LEADING_NOTE_ID_RE):
        for match in pattern.finditer(str(text)):
            note_id = _normalize_note_id(match.group(1))
            if note_id not in ids:
                ids.append(note_id)
    return ids


def _normalize_note_marker(value: str) -> str | None:
    if value == "＊":
        return "*"
    return value if value in {"※", "*"} else None


def _normalize_note_id(value: str) -> str:
    return value.replace("＊", "*")


def _row_note_reference_candidates(
    row_notes: list[dict[str, Any]],
    note_markers: list[str],
    note_ids: list[str],
) -> list[dict[str, Any]]:
    candidates = []
    for note in row_notes:
        note_id = note.get("note_id")
        note_marker = note.get("note_marker")
        if (note_id and note_id in note_ids) or (note_marker and note_marker in note_markers):
            candidates.append(
                {
                    "note_index": note["note_index"],
                    "note_marker": note_marker,
                    "note_id": note_id,
                }
            )
    if candidates or not note_markers:
        return candidates
    return [
        {
            "note_index": note["note_index"],
            "note_marker": note.get("note_marker"),
            "note_id": note.get("note_id"),
        }
        for note in row_notes
    ]


def _note_linkage_status(
    note_markers: list[str],
    note_ids: list[str],
    row_notes: list[dict[str, Any]],
    note_candidates: list[dict[str, Any]],
) -> str:
    if not note_markers and not note_ids:
        return "no_cell_note_markers"
    if not row_notes:
        return "no_row_notes"
    if note_ids and note_candidates:
        return "same_row_note_candidates_available"
    if note_candidates:
        return "same_row_note_candidates_available" if len(note_candidates) == 1 else "ambiguous_marker_without_id"
    return "no_matching_row_note_candidate"


def _extract_supercombo_tables(soup: Any) -> dict[str, Any]:
    main = soup.find("main") or soup
    heading_chain = {f"h{level}": "" for level in range(1, 7)}
    tables = []
    for node in main.descendants:
        name = getattr(node, "name", None)
        if not name:
            continue
        name = name.lower()
        if name in heading_chain:
            heading_chain[name] = _visible_text(node)
            for level in range(int(name[1:]) + 1, 7):
                heading_chain[f"h{level}"] = ""
            continue
        if name != "table":
            continue
        table_index = len(tables)
        row_payloads = []
        for row_index, row in enumerate(node.find_all("tr"), start=1):
            cells = row.find_all(["th", "td"], recursive=False)
            row_payloads.append(
                {
                    "row_index": row_index,
                    "cell_count": len(cells),
                    "cells": [
                        {
                            "cell_index": cell_index,
                            "tag": cell.name,
                            "text": cell.get_text("", strip=False),
                            "text_stripped": _visible_text(cell),
                        }
                        for cell_index, cell in enumerate(cells)
                    ],
                }
            )
        tables.append(
            {
                "table_index": table_index,
                "heading_chain": {key: value for key, value in heading_chain.items() if value},
                "row_count": len(row_payloads),
                "rows": row_payloads,
            }
        )
    return {
        "table_count": len(tables),
        "raw_row_count": sum(table["row_count"] for table in tables),
        "tables": tables,
    }


def _visible_text(node: Any) -> str:
    return _normalize_text(node.get_text(" ", strip=True))


def _normalize_text(text: Any) -> str:
    return " ".join(str(text).split())


def _official_visible_text(node: Any) -> str:
    separator = "" if _has_class_prefix(node, "frame_attribute") else " "
    return _normalize_text(separator.join(part for part in _official_text_parts(node, hidden_only=False) if part.strip()))


def _official_hidden_detail_text(node: Any) -> str:
    return _normalize_text(" ".join(part for part in _official_text_parts(node, hidden_only=True) if part.strip()))


def _official_text_parts(node: Any, *, hidden_only: bool) -> list[str]:
    parts: list[str] = []

    def walk(current: Any, *, hidden_ancestor: bool) -> None:
        for child in getattr(current, "children", []):
            name = getattr(child, "name", None)
            if name is None:
                if hidden_only == hidden_ancestor:
                    parts.append(str(child))
                continue
            tag_name = str(name).lower()
            if tag_name in {"script", "style", "noscript", "input"}:
                continue
            is_hidden = hidden_ancestor or _is_official_hidden_detail_node(child)
            if hidden_only and is_hidden and not hidden_ancestor:
                parts.append(child.get_text("", strip=False))
                continue
            if not hidden_only and is_hidden:
                continue
            walk(child, hidden_ancestor=is_hidden)

    walk(node, hidden_ancestor=False)
    return parts


def _is_official_hidden_detail_node(node: Any) -> bool:
    if node.has_attr("hidden"):
        return True
    if str(node.get("aria-hidden") or "").lower() == "true":
        return True
    style = str(node.get("style") or "").replace(" ", "").lower()
    if any(marker in style for marker in ("display:none", "visibility:hidden", "opacity:0")):
        return True
    return any(token.startswith("frame_ex__") or token == "frame_ex" for token in _class_tokens(node))


def _has_class_prefix(node: Any, prefix: str) -> bool:
    return any(token == prefix or token.startswith(f"{prefix}__") for token in _class_tokens(node))


def _class_tokens(node: Any) -> list[str]:
    value = node.get("class")
    if value is None:
        return []
    if isinstance(value, str):
        return value.split()
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    return str(value).split()


def _cell_images(cell: Any) -> list[dict[str, str | None]]:
    return [
        {
            "src": image.get("src"),
            "alt": image.get("alt"),
        }
        for image in cell.find_all("img")
    ]


def _write_json(path: Path, payload: Any) -> str:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return _file_hash(path)


def _file_hash(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _missing_official_entry(character: RosterCharacter, captured_at: str) -> dict[str, Any]:
    return {
        "character_slug": character.character_slug,
        "display_name": character.display_name,
        "source_family": "official",
        "source_role": "current_fact_authority_candidate",
        "source_url": None,
        "final_url": None,
        "captured_at_utc": captured_at,
        "http_status": 0,
        "content_type": "unknown",
        "content_length": None,
        "source_version_label": "unknown",
        "source_revision_label": "unknown",
        "capture_method": "scrapling_fetcher",
        "capture_success": False,
        "failure_reason": "missing sources.official",
        "content_hash": None,
        "artifact_boundary": REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
        "metadata_hash": None,
        "official_next_data_present": False,
        "official_next_data_hash": None,
        "official_table_count": 0,
        "official_raw_row_count": 0,
        "official_table_rows_schema_version": OFFICIAL_TABLE_ROWS_SCHEMA_VERSION,
        "official_row_note_rows": 0,
        "official_row_note_count": 0,
        "official_header_missing": OFFICIAL_HEADER_MARKERS,
        "official_header_path_violations": ["missing official header paths"],
        "official_row_cell_count_violations": [],
        "official_table_rows_hash": None,
    }


def _missing_supercombo_entry(character: RosterCharacter, captured_at: str) -> dict[str, Any]:
    return {
        "character_slug": character.character_slug,
        "display_name": character.display_name,
        "source_family": "supercombo",
        "source_role": "enrichment_candidate",
        "source_url": None,
        "final_url": None,
        "captured_at_utc": captured_at,
        "http_status": 0,
        "content_type": "unknown",
        "content_length": None,
        "source_version_label": "unknown",
        "source_revision_label": "unknown",
        "capture_method": "scrapling_stealthy_fetcher",
        "capture_success": False,
        "failure_reason": "missing sources.supercombo_data",
        "content_hash": None,
        "artifact_boundary": REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
        "metadata_hash": None,
        "supercombo_table_count": 0,
        "supercombo_raw_row_count": 0,
        "supercombo_tables_hash": None,
    }


def _capture_status(source_url: str, result: FetchResult) -> tuple[bool, str]:
    if result.failure_reason:
        return False, result.failure_reason
    if result.http_status < 200 or result.http_status >= 300:
        return False, f"HTTP {result.http_status}"
    if not result.content:
        return False, "empty response body"
    if "streetfighter.com/6/" not in result.final_url:
        return False, f"unexpected final URL: {result.final_url}"
    source_slug = source_url.rstrip("/").split("/")[-2] if "/frame" in source_url else ""
    if source_slug and source_slug not in result.final_url:
        return False, f"final URL does not include character slug {source_slug}: {result.final_url}"
    return True, ""


def _supercombo_capture_status(source_url: str, result: FetchResult) -> tuple[bool, str]:
    if result.failure_reason:
        return False, result.failure_reason
    if result.http_status < 200 or result.http_status >= 300:
        return False, f"HTTP {result.http_status}"
    if not result.content:
        return False, "empty response body"
    text = result.content.decode("utf-8", errors="replace")
    if "Just a moment" in text or "security verification" in text:
        return False, "SuperCombo challenge page captured"
    if "wiki.supercombo.gg" not in result.final_url:
        return False, f"unexpected final URL: {result.final_url}"
    return True, ""


def _header_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _header_value(headers: Any, name: str) -> str | None:
    value = None
    try:
        value = headers.get(name)
    except AttributeError:
        value = None
    if value is None:
        try:
            value = headers.get(name.lower())
        except AttributeError:
            value = None
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value) if value is not None else None


def _page_body(page: Any) -> bytes:
    for attribute in ("body", "content", "html", "text"):
        body = getattr(page, attribute, None)
        if not body:
            continue
        if isinstance(body, bytes):
            return body
        if isinstance(body, str):
            return body.encode("utf-8")
        try:
            return bytes(body)
        except TypeError:
            continue
    rendered = str(page)
    return rendered.encode("utf-8") if rendered else b""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="source-acquisition")
    subparsers = parser.add_subparsers(required=True)

    official_parser = subparsers.add_parser("official")
    official_parser.add_argument("--report", required=True, type=Path)
    official_parser.add_argument("--workspace", type=Path)
    official_parser.add_argument("--run-id")
    official_parser.add_argument("--sleep-seconds", type=float, default=0.0)
    official_parser.add_argument("--include-supercombo", action="store_true")
    official_parser.set_defaults(func=_official_command)

    validate_parser = subparsers.add_parser("validate-report")
    validate_parser.add_argument("report", type=Path)
    validate_parser.set_defaults(func=_validate_report_command)

    validate_artifacts_parser = subparsers.add_parser("validate-artifacts")
    validate_artifacts_parser.add_argument("report", type=Path)
    validate_artifacts_parser.add_argument("--workspace", type=Path)
    validate_artifacts_parser.set_defaults(func=_validate_artifacts_command)

    bundle_parser = subparsers.add_parser("prepare-official-note-review-bundle")
    bundle_parser.add_argument("report", type=Path)
    bundle_parser.add_argument("--output-dir", type=Path)
    bundle_parser.add_argument("--run-id")
    bundle_parser.add_argument("--character", action="append", dest="characters", default=[])
    bundle_parser.set_defaults(func=_prepare_official_note_review_bundle_command)

    return parser


def _official_command(args: argparse.Namespace) -> dict[str, Any]:
    return acquire_official_sources(
        report_path=args.report,
        workspace=args.workspace,
        run_id=args.run_id,
        include_supercombo=args.include_supercombo,
        sleep_seconds=args.sleep_seconds,
    )


def _validate_report_command(args: argparse.Namespace) -> dict[str, Any]:
    validate_acquisition_report(args.report)
    report = load_acquisition_report(args.report)
    return {
        "ok": True,
        "run_id": report["run_id"],
        "expected_count": report["official_coverage"]["expected_count"],
        "captured_count": report["official_coverage"]["captured_count"],
        "failed_count": report["official_coverage"]["failed_count"],
    }


def _validate_artifacts_command(args: argparse.Namespace) -> dict[str, Any]:
    validate_acquisition_artifacts(args.report, workspace=args.workspace)
    report = load_acquisition_report(args.report)
    return {
        "ok": True,
        "run_id": report["run_id"],
        "official_captured_count": report["official_coverage"]["captured_count"],
        "supercombo_captured_count": report.get("supercombo_coverage", {}).get("captured_count", 0),
    }


def _prepare_official_note_review_bundle_command(args: argparse.Namespace) -> dict[str, Any]:
    return prepare_official_note_linkage_review_bundle(
        report_path=args.report,
        output_dir=args.output_dir,
        run_id=args.run_id,
        slugs=args.characters,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (LookupError, RuntimeError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
