from __future__ import annotations

import json
from pathlib import Path

from sf6_ingest.core.io import load_run_manifest
from sf6_ingest.core.pipeline import parse_from_raw, publish_run

from .conftest import fixture_html, save_fixture_snapshot, save_html_snapshot
from .supercombo_fixture import build_supercombo_contract_html


MINIMUM_SUPERCOMBO_REVIEW_FIELDS = {
    "dataset",
    "source",
    "snapshot_id",
    "source_row_id",
    "raw_source_token",
    "reason_codes",
    "raw_excerpt",
}
ROW_OPEN = '        <tr>\n          <td>\n            <span class="frame_arts__name">'
ROW_CLOSE = "        </tr>\n"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _supercombo_export_bytes(export_root: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in export_root.glob("supercombo_enrichment*")}


def _remove_move_row(html: str, *, which: str) -> str:
    if which == "first":
        row_start = html.find(ROW_OPEN)
    elif which == "last":
        row_start = html.rfind(ROW_OPEN)
    else:
        raise ValueError(f"unsupported row selector: {which}")
    if row_start == -1:
        raise AssertionError("fixture row marker not found")
    row_end = html.index(ROW_CLOSE, row_start) + len(ROW_CLOSE)
    return html[:row_start] + html[row_end:]


def _publish_baseline(temp_repo_root: Path) -> tuple[str, Path]:
    save_fixture_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T000000Z-11111111",
        fixture_name="official_success.html",
        fetched_at="2026-03-08T00:00:00Z",
    )
    save_html_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000100Z-22222222",
        html=build_supercombo_contract_html(),
        fetched_at="2026-03-08T00:01:00Z",
        page_title="Street Fighter 6/JP/Data - SuperCombo Wiki",
    )

    run_id = parse_from_raw(
        "jp",
        {"official": "20260308T000000Z-11111111", "supercombo": "20260308T000100Z-22222222"},
        temp_repo_root,
    )
    summary = publish_run("jp", run_id, temp_repo_root)
    assert summary.dataset_states == {
        "official_raw": "published",
        "supercombo_enrichment": "published",
        "derived_metrics": "published",
    }
    return run_id, temp_repo_root / "data" / "exports" / "jp"


def test_checked_in_supercombo_main_is_subset_of_checked_in_official_main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    export_root_parent = repo_root / "data" / "exports"
    for export_root in sorted(path for path in export_root_parent.iterdir() if (path / "supercombo_enrichment.json").exists()):
        character_slug = export_root.name
        official_move_ids = {row["move_id"] for row in _load_json(export_root / "official_raw.json")}
        supercombo_move_ids = {row["move_id"] for row in _load_json(export_root / "supercombo_enrichment.json")}
        assert supercombo_move_ids.issubset(official_move_ids)


def test_publish_writes_anchored_main_exports_and_withheld_sidecars(temp_repo_root) -> None:
    run_id, export_root = _publish_baseline(temp_repo_root)

    official_rows = _load_json(export_root / "official_raw.json")
    supercombo_rows = _load_json(export_root / "supercombo_enrichment.json")
    official_review_rows = _load_json(export_root / "official_raw_manual_review.json")
    supercombo_review_rows = _load_json(export_root / "supercombo_enrichment_manual_review.json")

    assert len(official_rows) == 2
    official_move_ids = {row["move_id"] for row in official_rows}
    assert len(supercombo_rows) == 1
    assert {row["move_id"] for row in supercombo_rows} == {"jp_001_5lp"}
    assert {row["move_id"] for row in supercombo_rows}.issubset(official_move_ids)
    assert all("raw_source_token" not in row for row in supercombo_rows)

    assert len(official_review_rows) == 1
    assert len(supercombo_review_rows) == 7
    by_token = {row["raw_source_token"]: row for row in supercombo_review_rows}
    assert set(by_token) == {
        "jp_jlp",
        "jp_236236k(ca)",
        "jp_6hphk_recovery",
        "jp_mpmk_66_drc",
        "jp_22pp",
        "jp_214p_214hp",
        "jp_22k_bomb",
    }
    for token in {"jp_jlp", "jp_236236k(ca)", "jp_6hphk_recovery", "jp_mpmk_66_drc"}:
        assert MINIMUM_SUPERCOMBO_REVIEW_FIELDS.issubset(set(by_token[token]))
        assert by_token[token]["reason_codes"] == ["supercombo_missing_official_safe_row"]
    assert by_token["jp_22pp"]["candidate_move_ids"] == [
        "jp_030_22pp_triglav_od_weak",
        "jp_031_22pp_triglav_od_medium",
        "jp_032_22pp_triglav_od_heavy",
    ]
    assert by_token["jp_214p_214hp"]["collision_group"] == "jp_vihat_cheni_followup"
    assert by_token["jp_22k_bomb"]["binding_class"] == "G"
    assert by_token["jp_22k_bomb"]["move_id"] is None
    assert "supercombo_missing_official_safe_row" not in by_token["jp_22pp"]["reason_codes"]

    snapshot_manifest = _load_json(export_root / "snapshot_manifest.json")
    official_manifest = snapshot_manifest["datasets"]["official_raw"]
    supercombo_manifest = snapshot_manifest["datasets"]["supercombo_enrichment"]
    derived_manifest = snapshot_manifest["datasets"]["derived_metrics"]
    assert snapshot_manifest["schema_version"] == "3.0.0"
    assert snapshot_manifest["export_contract_version"] == "3.0.0"
    assert snapshot_manifest["derivation_rule_version"] == "1.0.0"
    assert snapshot_manifest["repo_generation_registry_version"] == "2.1.0"
    assert len(snapshot_manifest["repo_generation_registry_sha256"]) == 64
    assert snapshot_manifest["repo_generation_binding_policy_version"] == "1.0.0"
    assert len(snapshot_manifest["repo_generation_binding_policy_sha256"]) == 64
    assert supercombo_manifest["publication_state"] == "available"
    assert supercombo_manifest["published_run_id"] == run_id
    assert supercombo_manifest["published_snapshot_ids"] == ["20260308T000100Z-22222222"]
    assert supercombo_manifest["published_record_count"] == 1
    assert supercombo_manifest["withheld_review_count"] == 7
    assert supercombo_manifest["binding_policy_version"] == "1.0.0"
    assert len(supercombo_manifest["binding_policy_sha256"]) == 64
    assert official_manifest["binding_policy_version"] is None
    assert official_manifest["binding_policy_sha256"] is None
    assert derived_manifest["binding_policy_version"] is None
    assert derived_manifest["binding_policy_sha256"] is None


def test_supercombo_failure_retains_last_known_good_when_official_set_is_unchanged(temp_repo_root) -> None:
    first_run_id, export_root = _publish_baseline(temp_repo_root)
    supercombo_export_before = _supercombo_export_bytes(export_root)

    save_fixture_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T000200Z-33333333",
        fixture_name="official_success.html",
        fetched_at="2026-03-08T00:02:00Z",
    )
    save_fixture_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000300Z-44444444",
        fixture_name="supercombo_challenge.html",
        fetched_at="2026-03-08T00:03:00Z",
        success=False,
        challenge_detected=True,
        error_message="challenge detected",
    )

    second_run_id = parse_from_raw(
        "jp",
        {"official": "20260308T000200Z-33333333", "supercombo": "20260308T000300Z-44444444"},
        temp_repo_root,
    )
    second_summary = publish_run("jp", second_run_id, temp_repo_root)
    assert second_summary.dataset_states == {
        "official_raw": "published",
        "supercombo_enrichment": "retained_last_known_good",
        "derived_metrics": "published",
    }

    second_manifest = load_run_manifest(temp_repo_root / "data" / "normalized" / "jp" / second_run_id / "run_manifest.json")
    assert second_manifest.binding_policy_version == "1.0.0"
    assert len(second_manifest.binding_policy_sha256) == 64
    assert second_manifest.source_status["supercombo"].fetch_success is False
    assert second_manifest.source_status["supercombo"].parse_state == "skipped_fetch_failure"
    assert second_manifest.dataset_status["supercombo_enrichment"].publication_outcome == "retained_last_known_good"
    assert second_manifest.dataset_status["supercombo_enrichment"].published_run_id == first_run_id
    assert second_manifest.dataset_status["supercombo_enrichment"].published_record_count == 0
    assert second_manifest.dataset_status["supercombo_enrichment"].withheld_review_count == 0
    assert (temp_repo_root / "data" / "normalized" / "jp" / second_run_id / "supercombo_enrichment" / "records.json").exists()

    supercombo_export_after = _supercombo_export_bytes(export_root)
    assert supercombo_export_after == supercombo_export_before

    snapshot_manifest = _load_json(export_root / "snapshot_manifest.json")
    supercombo_manifest = snapshot_manifest["datasets"]["supercombo_enrichment"]
    assert supercombo_manifest["published_run_id"] == first_run_id
    assert supercombo_manifest["published_snapshot_ids"] == ["20260308T000100Z-22222222"]
    assert supercombo_manifest["published_record_count"] == 1
    assert supercombo_manifest["withheld_review_count"] == 7


def test_supercombo_lkg_remains_valid_when_official_move_set_changes_but_subset_holds(temp_repo_root) -> None:
    first_run_id, export_root = _publish_baseline(temp_repo_root)
    supercombo_export_before = _supercombo_export_bytes(export_root)

    save_html_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T000200Z-33333333",
        html=_remove_move_row(fixture_html("official_success.html"), which="last"),
        fetched_at="2026-03-08T00:02:00Z",
        page_title="fixture",
    )
    save_fixture_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000300Z-44444444",
        fixture_name="supercombo_challenge.html",
        fetched_at="2026-03-08T00:03:00Z",
        success=False,
        challenge_detected=True,
        error_message="challenge detected",
    )

    second_run_id = parse_from_raw(
        "jp",
        {"official": "20260308T000200Z-33333333", "supercombo": "20260308T000300Z-44444444"},
        temp_repo_root,
    )
    second_summary = publish_run("jp", second_run_id, temp_repo_root)
    assert second_summary.dataset_states["supercombo_enrichment"] == "retained_last_known_good"

    second_manifest = load_run_manifest(temp_repo_root / "data" / "normalized" / "jp" / second_run_id / "run_manifest.json")
    assert second_manifest.dataset_status["supercombo_enrichment"].publication_outcome == "retained_last_known_good"
    assert second_manifest.dataset_status["supercombo_enrichment"].published_run_id == first_run_id

    supercombo_export_after = _supercombo_export_bytes(export_root)
    assert supercombo_export_after == supercombo_export_before

    snapshot_manifest = _load_json(export_root / "snapshot_manifest.json")
    official_manifest = snapshot_manifest["datasets"]["official_raw"]
    supercombo_manifest = snapshot_manifest["datasets"]["supercombo_enrichment"]
    assert official_manifest["published_run_id"] == second_run_id
    assert supercombo_manifest["published_run_id"] == first_run_id
    assert supercombo_manifest["published_record_count"] == 1
    assert supercombo_manifest["withheld_review_count"] == 7


def test_supercombo_lkg_is_invalidated_when_official_move_set_changes_and_subset_fails(temp_repo_root) -> None:
    _publish_baseline(temp_repo_root)
    export_root = temp_repo_root / "data" / "exports" / "jp"

    save_html_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T000200Z-33333333",
        html=_remove_move_row(fixture_html("official_success.html"), which="first"),
        fetched_at="2026-03-08T00:02:00Z",
        page_title="fixture",
    )
    save_fixture_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000300Z-44444444",
        fixture_name="supercombo_challenge.html",
        fetched_at="2026-03-08T00:03:00Z",
        success=False,
        challenge_detected=True,
        error_message="challenge detected",
    )

    second_run_id = parse_from_raw(
        "jp",
        {"official": "20260308T000200Z-33333333", "supercombo": "20260308T000300Z-44444444"},
        temp_repo_root,
    )
    second_summary = publish_run("jp", second_run_id, temp_repo_root)
    assert second_summary.dataset_states == {
        "official_raw": "published",
        "supercombo_enrichment": "unavailable",
        "derived_metrics": "published",
    }

    second_manifest = load_run_manifest(temp_repo_root / "data" / "normalized" / "jp" / second_run_id / "run_manifest.json")
    assert second_manifest.dataset_status["supercombo_enrichment"].publication_outcome == "unavailable"
    assert second_manifest.dataset_status["supercombo_enrichment"].published_run_id is None
    assert not any(export_root.glob("supercombo_enrichment*"))

    snapshot_manifest = _load_json(export_root / "snapshot_manifest.json")
    assert snapshot_manifest["datasets"]["supercombo_enrichment"] == {
        "publication_state": "unavailable",
        "published_run_id": None,
        "published_snapshot_ids": [],
        "published_record_count": 0,
        "withheld_review_count": 0,
        "registry_version": "2.1.0",
        "registry_sha256": snapshot_manifest["datasets"]["supercombo_enrichment"]["registry_sha256"],
        "binding_policy_version": "1.0.0",
        "binding_policy_sha256": snapshot_manifest["datasets"]["supercombo_enrichment"]["binding_policy_sha256"],
        "content_hash": None,
    }


def test_supercombo_zero_publishable_rows_retains_last_known_good(temp_repo_root) -> None:
    first_run_id, export_root = _publish_baseline(temp_repo_root)
    supercombo_export_before = _supercombo_export_bytes(export_root)

    save_html_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000400Z-55555555",
        html=build_supercombo_contract_html(include_tokens={"jp_22pp", "jp_214p_214hp", "jp_22k_bomb"}),
        fetched_at="2026-03-08T00:04:00Z",
        page_title="Street Fighter 6/JP/Data - SuperCombo Wiki",
    )

    second_run_id = parse_from_raw(
        "jp",
        {"official": "20260308T000000Z-11111111", "supercombo": "20260308T000400Z-55555555"},
        temp_repo_root,
    )
    second_summary = publish_run("jp", second_run_id, temp_repo_root)
    assert second_summary.dataset_states["supercombo_enrichment"] == "retained_last_known_good"

    second_manifest = load_run_manifest(temp_repo_root / "data" / "normalized" / "jp" / second_run_id / "run_manifest.json")
    assert second_manifest.dataset_status["supercombo_enrichment"].publication_outcome == "retained_last_known_good"
    assert second_manifest.dataset_status["supercombo_enrichment"].published_run_id == first_run_id
    assert second_manifest.dataset_status["supercombo_enrichment"].published_record_count == 0
    assert second_manifest.dataset_status["supercombo_enrichment"].withheld_review_count == 3

    supercombo_export_after = _supercombo_export_bytes(export_root)
    assert supercombo_export_after == supercombo_export_before


def test_publish_is_byte_stable_for_same_normalized_input(temp_repo_root) -> None:
    save_fixture_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T010000Z-aaaaaaa1",
        fixture_name="official_success.html",
        fetched_at="2026-03-08T01:00:00Z",
    )

    first_run_id = parse_from_raw("jp", {"official": "20260308T010000Z-aaaaaaa1"}, temp_repo_root)
    publish_run("jp", first_run_id, temp_repo_root)

    export_root = temp_repo_root / "data" / "exports" / "jp"
    before = {path.name: path.read_bytes() for path in export_root.glob("*")}

    second_run_id = parse_from_raw("jp", {"official": "20260308T010000Z-aaaaaaa1"}, temp_repo_root)
    publish_run("jp", second_run_id, temp_repo_root)

    after = {path.name: path.read_bytes() for path in export_root.glob("*")}
    assert after == before


def test_supercombo_cannot_publish_without_official_main_dataset(temp_repo_root) -> None:
    save_html_snapshot(
        temp_repo_root,
        source="supercombo",
        snapshot_id="20260308T000100Z-22222222",
        html=build_supercombo_contract_html(),
        fetched_at="2026-03-08T00:01:00Z",
        page_title="Street Fighter 6/JP/Data - SuperCombo Wiki",
    )

    run_id = parse_from_raw("jp", {"supercombo": "20260308T000100Z-22222222"}, temp_repo_root)
    summary = publish_run("jp", run_id, temp_repo_root)
    assert summary.dataset_states == {
        "official_raw": "not_selected",
        "supercombo_enrichment": "unavailable",
        "derived_metrics": "not_selected",
    }

    export_root = temp_repo_root / "data" / "exports" / "jp"
    snapshot_manifest = _load_json(export_root / "snapshot_manifest.json")
    assert snapshot_manifest["datasets"]["supercombo_enrichment"] == {
        "publication_state": "unavailable",
        "published_run_id": None,
        "published_snapshot_ids": [],
        "published_record_count": 0,
        "withheld_review_count": 0,
        "registry_version": "2.1.0",
        "registry_sha256": snapshot_manifest["datasets"]["supercombo_enrichment"]["registry_sha256"],
        "binding_policy_version": "1.0.0",
        "binding_policy_sha256": snapshot_manifest["datasets"]["supercombo_enrichment"]["binding_policy_sha256"],
        "content_hash": None,
    }
    assert not any(export_root.glob("supercombo_enrichment*"))

    run_manifest = load_run_manifest(temp_repo_root / "data" / "normalized" / "jp" / run_id / "run_manifest.json")
    supercombo_status = run_manifest.dataset_status["supercombo_enrichment"]
    assert supercombo_status.publication_outcome == "unavailable"
    assert supercombo_status.published_record_count == 0
    assert supercombo_status.withheld_review_count == 8


def test_supercombo_unavailable_manifest_entry_has_fixed_v3_shape(temp_repo_root) -> None:
    save_fixture_snapshot(
        temp_repo_root,
        source="official",
        snapshot_id="20260308T020000Z-bbbbbbb2",
        fixture_name="official_success.html",
        fetched_at="2026-03-08T02:00:00Z",
    )

    run_id = parse_from_raw("jp", {"official": "20260308T020000Z-bbbbbbb2"}, temp_repo_root)
    summary = publish_run("jp", run_id, temp_repo_root)
    assert summary.dataset_states["supercombo_enrichment"] == "not_selected"

    snapshot_manifest = _load_json(temp_repo_root / "data" / "exports" / "jp" / "snapshot_manifest.json")
    supercombo_manifest = snapshot_manifest["datasets"]["supercombo_enrichment"]
    assert supercombo_manifest == {
        "publication_state": "unavailable",
        "published_run_id": None,
        "published_snapshot_ids": [],
        "published_record_count": 0,
        "withheld_review_count": 0,
        "registry_version": "2.1.0",
        "registry_sha256": supercombo_manifest["registry_sha256"],
        "binding_policy_version": "1.0.0",
        "binding_policy_sha256": supercombo_manifest["binding_policy_sha256"],
        "content_hash": None,
    }
    assert len(supercombo_manifest["registry_sha256"]) == 64
    assert len(supercombo_manifest["binding_policy_sha256"]) == 64
