from __future__ import annotations

import json
from pathlib import Path

import pytest

from sf6_ingest.core.pipeline import parse_from_raw, publish_run
from sf6_ingest.core.prune import prune_latest_published_state

from .conftest import save_fixture_snapshot


def test_prune_dry_run_lists_stale_state_without_mutation(temp_repo_root: Path) -> None:
    _build_published_repo(temp_repo_root)
    _add_stale_data(temp_repo_root)

    summary = prune_latest_published_state("jp", apply=False, verbose=True, base_repo_root=temp_repo_root)

    delete_paths = {item.path.as_posix() for item in summary.delete_items}
    assert summary.dry_run is True
    assert "official_raw" in summary.kept_datasets
    assert "derived_metrics" in summary.kept_datasets
    assert any("data/normalized/jp/old-run" in path for path in delete_paths)
    assert any("data/raw/official/jp/stale-official" in path for path in delete_paths)
    assert any("data/archive" in path for path in delete_paths)
    assert any("data/exports/jp/supercombo_enrichment.json" in path for path in delete_paths)
    assert (temp_repo_root / "data" / "normalized" / "jp" / "old-run").exists()
    assert (temp_repo_root / "data" / "archive").exists()


def test_prune_apply_is_idempotent(temp_repo_root: Path) -> None:
    _build_published_repo(temp_repo_root)
    _add_stale_data(temp_repo_root)

    first = prune_latest_published_state("jp", apply=True, base_repo_root=temp_repo_root)
    second = prune_latest_published_state("jp", apply=False, base_repo_root=temp_repo_root)

    assert first.dry_run is False
    assert second.delete_items == ()
    assert not (temp_repo_root / "data" / "normalized").exists()
    assert not (temp_repo_root / "data" / "archive").exists()
    assert not (temp_repo_root / "data" / "raw" / "official" / "jp" / "stale-official").exists()
    assert not (temp_repo_root / "data" / "exports" / "jp" / "supercombo_enrichment.json").exists()
    assert (temp_repo_root / "data" / "exports" / "jp" / "official_raw.json").exists()


def test_prune_fails_closed_on_manifest_version_mismatch(temp_repo_root: Path) -> None:
    _build_published_repo(temp_repo_root)
    manifest_path = temp_repo_root / "data" / "exports" / "jp" / "snapshot_manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["schema_version"] = "9.9.9"
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    with pytest.raises(ValueError, match="unsupported snapshot manifest schema_version"):
        prune_latest_published_state("jp", apply=False, base_repo_root=temp_repo_root)


def _build_published_repo(repo_root: Path) -> str:
    save_fixture_snapshot(
        repo_root,
        source="official",
        snapshot_id="20260308T000000Z-11111111",
        fixture_name="official_success.html",
        fetched_at="2026-03-08T00:00:00Z",
    )
    run_id = parse_from_raw("jp", {"official": "20260308T000000Z-11111111"}, repo_root)
    publish_run("jp", run_id, repo_root)
    return run_id


def _add_stale_data(repo_root: Path) -> None:
    stale_run = repo_root / "data" / "normalized" / "jp" / "old-run"
    stale_run.mkdir(parents=True, exist_ok=True)
    (stale_run / "run_manifest.json").write_text("{}", encoding="utf-8", newline="\n")

    stale_raw = repo_root / "data" / "raw" / "official" / "jp" / "stale-official"
    stale_raw.mkdir(parents=True, exist_ok=True)
    (stale_raw / "page.html").write_bytes(b"<html></html>\n")
    (stale_raw / "metadata.json").write_text("{}\n", encoding="utf-8", newline="\n")

    empty_supercombo = repo_root / "data" / "raw" / "supercombo" / "jp"
    empty_supercombo.mkdir(parents=True, exist_ok=True)

    archive_path = repo_root / "data" / "archive" / "raw_legacy" / "official" / "jp"
    archive_path.mkdir(parents=True, exist_ok=True)
    (archive_path / "legacy.html").write_text("<html>legacy</html>\n", encoding="utf-8", newline="\n")

    stale_export = repo_root / "data" / "exports" / "jp" / "supercombo_enrichment.json"
    stale_export.write_text("[]\n", encoding="utf-8", newline="\n")
