from __future__ import annotations

import json
import tempfile
import unittest
import shutil
from pathlib import Path

from sf6_knowledge_coach.paths import repo_root
from sf6_knowledge_coach.source_acquisition import (
    FetchResult,
    REPO_LOCAL_RAW_ARTIFACT_BOUNDARY,
    REPO_LOCAL_REVIEWER_EVIDENCE_BOUNDARY,
    RosterCharacter,
    acquire_official_sources,
    default_workspace,
    prepare_official_note_linkage_review_bundle,
    render_acquisition_report,
    validate_acquisition_artifacts,
    validate_acquisition_report,
    validate_acquisition_report_text,
)


def _fake_fetch(url: str) -> FetchResult:
    slug = url.rstrip("/").split("/")[-2]
    return FetchResult(
        content=f"""
<html>
  <head>
    <script id="__NEXT_DATA__" type="application/json">{{"character":"{slug}"}}</script>
  </head>
  <body>
    <table>
      <thead>
        <tr>
          <th rowspan="2">技名</th>
          <th colspan="3">動作フレーム<ul><li>発生</li><li>持続</li><li>硬直</li></ul></th>
          <th colspan="2">硬直差<ul><li>ヒット</li><li>ガード</li></ul></th>
          <th rowspan="2"><label>キャンセル</label></th>
          <th rowspan="2"><p>ダメージ</p></th>
          <th rowspan="2"><label>コンボ補正値</label></th>
          <th>Dゲージ増加<ul><li><label>ヒット</label></li></ul></th>
          <th colspan="2">Dゲージ減少<ul><li><label>ガード</label></li><li><label>パニッシュカウンター</label></li></ul></th>
          <th rowspan="2">SAゲージ増加</th>
          <th rowspan="2"><label>属性</label></th>
          <th rowspan="2">備考</th>
        </tr>
      </thead>
      <tbody>
        <tr><td colspan="15">通常技</td></tr>
        <tr>
          <td><span>{slug} 5LP</span><p><img src="/i/lp.png" alt="LP"></p></td>
          <td>4</td><td><label>3</label><div class="frame_ex___test"><div>1-2, 4</div></div></td>
          <td>7</td><td>+4</td><td>-2</td><td>※</td>
          <td>300</td><td>始動補正(20%)</td><td>250</td><td>-500</td><td>+6</td>
          <td>100</td><td>上</td><td><ul><li>※ヒット時のみキャンセル可能</li></ul></td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
""".encode("utf-8"),
        final_url=url,
        http_status=200,
        content_type="text/html; charset=utf-8",
        content_length=None,
        etag=f"etag-{slug}",
        last_modified=None,
    )


def _fake_supercombo_fetch(url: str) -> FetchResult:
    slug = url.rstrip("/").split("/")[-2]
    return FetchResult(
        content=f"""
<html>
  <main>
    <h2>Normal Moves</h2>
    <h3>{slug}</h3>
    <table>
      <tr><th>{slug} 5LP</th></tr>
      <tr><td>Move</td><td>Value</td></tr>
      <tr><td>Startup</td><td>4</td></tr>
    </table>
  </main>
</html>
""".encode("utf-8"),
        final_url=url,
        http_status=200,
        content_type="text/html; charset=utf-8",
        content_length=None,
        etag=f"etag-sc-{slug}",
        last_modified=None,
        capture_method="scrapling_stealthy_fetcher",
    )


def _repo_local_test_workspace(prefix: str) -> Path:
    root = repo_root() / ".local" / "source-acquisition" / "unit-tests"
    root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=f"{prefix}-", dir=root))


def _repo_local_reviewer_workspace(prefix: str) -> Path:
    root = repo_root() / ".local" / "reviewer-evidence" / "unit-tests"
    root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=f"{prefix}-", dir=root))


class SourceAcquisitionTests(unittest.TestCase):
    def test_default_workspace_is_repo_local_ignored_path(self) -> None:
        workspace = default_workspace("20260521T000000Z")
        self.assertEqual(
            workspace,
            repo_root() / ".local" / "source-acquisition" / "current-source-acquisition" / "20260521T000000Z",
        )

    def test_acquires_official_sources_to_workspace_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("official")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    },
    {
      "character_slug": "ryu",
      "display_name": "Ryu",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/ryu/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )

            report = acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )

            self.assertEqual(report["official_coverage"]["expected_count"], 2)
            self.assertEqual(report["official_coverage"]["captured_count"], 2)
            self.assertEqual(report["supercombo_decision"]["status"], "queued")
            self.assertEqual(report["entries"][0]["capture_method"], "scrapling_fetcher")
            self.assertEqual(report["entries"][0]["artifact_boundary"], REPO_LOCAL_RAW_ARTIFACT_BOUNDARY)
            self.assertTrue((workspace / "official" / "jp" / "page.html").exists())
            self.assertTrue((workspace / "official" / "jp" / "__NEXT_DATA__.json").exists())
            self.assertTrue((workspace / "official" / "jp" / "metadata.json").exists())
            self.assertTrue((workspace / "official" / "jp" / "official_table_rows.raw.json").exists())
            raw_rows = json.loads((workspace / "official" / "jp" / "official_table_rows.raw.json").read_text())
            self.assertEqual(raw_rows["column_header_paths"][0], ["技名"])
            self.assertEqual(raw_rows["column_header_paths"][1], ["動作フレーム", "発生"])
            self.assertEqual(raw_rows["column_header_paths"][2], ["動作フレーム", "持続"])
            self.assertEqual(raw_rows["column_header_paths"][5], ["硬直差", "ガード"])
            self.assertEqual(raw_rows["column_header_paths"][11], ["Dゲージ減少", "パニッシュカウンター"])
            self.assertEqual(raw_rows["header_path_violations"], [])
            self.assertEqual(raw_rows["artifact_schema_version"], "official_table_rows_raw/v4")
            self.assertEqual(raw_rows["row_note_rows"], 1)
            self.assertEqual(raw_rows["row_note_count"], 1)
            self.assertEqual(report["entries"][0]["official_table_rows_schema_version"], "official_table_rows_raw/v4")
            self.assertEqual(report["entries"][0]["official_row_note_rows"], 1)
            self.assertEqual(report["entries"][0]["official_row_note_count"], 1)
            first_row_cells = raw_rows["rows"][0]["cells"]
            self.assertEqual(raw_rows["rows"][0]["row_note_count"], 1)
            self.assertEqual(raw_rows["rows"][0]["row_note_extraction_status"], "notes_extracted")
            self.assertEqual(
                raw_rows["rows"][0]["row_notes"][0],
                {
                    "note_index": 0,
                    "note_marker": "※",
                    "note_id": None,
                    "note_text": "※ヒット時のみキャンセル可能",
                    "note_text_stripped": "※ヒット時のみキャンセル可能",
                    "note_source_scope": "row_local_note",
                    "source_order": 0,
                },
            )
            self.assertEqual(first_row_cells[0]["source_column_header_path"], ["技名"])
            self.assertEqual(first_row_cells[1]["source_column_header_path"], ["動作フレーム", "発生"])
            self.assertEqual(first_row_cells[5]["source_column_header_path"], ["硬直差", "ガード"])
            self.assertEqual(first_row_cells[5]["source_column_leaf_header"], "ガード")
            self.assertEqual(first_row_cells[6]["cell_note_markers"], ["※"])
            self.assertEqual(first_row_cells[6]["cell_note_ids"], [])
            self.assertEqual(
                first_row_cells[6]["row_note_reference_candidates"],
                [{"note_index": 0, "note_marker": "※", "note_id": None}],
            )
            self.assertEqual(first_row_cells[6]["note_linkage_status"], "same_row_note_candidates_available")
            active_frame_cell = raw_rows["rows"][0]["cells"][2]
            self.assertEqual(active_frame_cell["column_index"], 2)
            self.assertEqual(active_frame_cell["source_column_header_path"], ["動作フレーム", "持続"])
            self.assertEqual(active_frame_cell["source_column_leaf_header"], "持続")
            self.assertEqual(active_frame_cell["visible_text"], "3")
            self.assertEqual(active_frame_cell["source_text_stripped"], "31-2, 4")
            self.assertEqual(active_frame_cell["hidden_detail_text"], "1-2, 4")
            self.assertNotIn("text_stripped", active_frame_cell)
            self.assertTrue(report_path.exists())
            self.assertNotIn(str(workspace.resolve()), report_path.read_text(encoding="utf-8"))
            validate_acquisition_report(report_path, roster_path)
            validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)

    def test_prepares_local_reviewer_bundle_with_fake_scrapling_screenshotter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("reviewer-bundle-source")
            bundle_dir = _repo_local_reviewer_workspace("official-note-bundle")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            self.addCleanup(lambda: shutil.rmtree(bundle_dir, ignore_errors=True))
            self.addCleanup(lambda: bundle_dir.with_suffix(".zip").unlink(missing_ok=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )

            def fake_screenshotter(url: str, output_path: Path) -> str:
                output_path.write_bytes(b"fake png")
                return url

            result = prepare_official_note_linkage_review_bundle(
                report_path=report_path,
                output_dir=bundle_dir,
                run_id="unit-review",
                slugs=["jp"],
                screenshotter=fake_screenshotter,
            )

            self.assertEqual(result["target_count"], 1)
            self.assertTrue((bundle_dir / "screenshots" / "jp-full-page.png").exists())
            self.assertTrue((bundle_dir / "manifest.json").exists())
            self.assertTrue((bundle_dir / "chatgpt-check-prompt.md").exists())
            self.assertTrue(bundle_dir.with_suffix(".zip").exists())
            manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["evidence_boundary"], REPO_LOCAL_REVIEWER_EVIDENCE_BOUNDARY)
            self.assertEqual(manifest["screenshot_method"], "scrapling_dynamic_fetcher_page_action")
            self.assertEqual(manifest["chatgpt_result_status"], "observation_candidate_only")
            self.assertEqual(manifest["targets"][0]["screenshot"], "screenshots/jp-full-page.png")
            self.assertNotIn(str(bundle_dir.resolve()), json.dumps(manifest))

    def test_acquires_supercombo_tables_when_included(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("supercombo")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
        "supercombo_data": "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )

            report = acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
                supercombo_fetcher=_fake_supercombo_fetch,
                include_supercombo=True,
            )

            self.assertEqual(report["official_coverage"]["captured_count"], 1)
            self.assertEqual(report["supercombo_coverage"]["captured_count"], 1)
            self.assertEqual(report["supercombo_decision"]["status"], "same_run_approved")
            self.assertTrue((workspace / "supercombo" / "jp" / "page.html").exists())
            self.assertTrue((workspace / "supercombo" / "jp" / "metadata.json").exists())
            self.assertTrue((workspace / "supercombo" / "jp" / "supercombo_tables.raw.json").exists())
            validate_acquisition_report(report_path, roster_path)
            validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)

    def test_artifact_validation_rejects_missing_official_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("missing-official-rows")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            (workspace / "official" / "jp" / "official_table_rows.raw.json").unlink()

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            self.assertIn("official_table_rows.raw.json missing", str(context.exception))

    def test_artifact_validation_rejects_page_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("hash-mismatch")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            (workspace / "official" / "jp" / "page.html").write_text("tampered", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            self.assertIn("page.html hash mismatch", str(context.exception))

    def test_artifact_validation_rejects_legacy_official_text_stripped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("legacy-text-stripped")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            rows_path = workspace / "official" / "jp" / "official_table_rows.raw.json"
            payload = json.loads(rows_path.read_text(encoding="utf-8"))
            payload["rows"][0]["cells"][2]["text_stripped"] = "3 1-2, 4"
            rows_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            self.assertIn("must not use text_stripped", str(context.exception))

    def test_artifact_validation_rejects_missing_official_row_and_image_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("missing-row-image-fields")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            rows_path = workspace / "official" / "jp" / "official_table_rows.raw.json"
            payload = json.loads(rows_path.read_text(encoding="utf-8"))
            del payload["rows"][0]["group_heading"]
            del payload["rows"][0]["row_note_count"]
            del payload["rows"][0]["row_notes"][0]["note_text"]
            del payload["rows"][0]["input_images"][0]["src"]
            del payload["rows"][0]["cells"][0]["image_src"]
            del payload["rows"][0]["cells"][6]["note_linkage_status"]
            rows_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            message = str(context.exception)
            self.assertIn("official row 1 missing fields: group_heading, row_note_count", message)
            self.assertIn("official row 1 note 0 missing fields: note_text", message)
            self.assertIn("official row 1 input image 0 missing fields: src", message)
            self.assertIn("official row 1 cell 0 missing fields: image_src", message)
            self.assertIn("official row 1 cell 6 missing fields: note_linkage_status", message)

    def test_artifact_validation_rejects_malformed_official_row_and_image_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("malformed-row-image-fields")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            rows_path = workspace / "official" / "jp" / "official_table_rows.raw.json"
            payload = json.loads(rows_path.read_text(encoding="utf-8"))
            payload["rows"][0]["cell_count"] = 99
            payload["rows"][0]["input_images"] = {"src": "/i/lp.png", "alt": "LP"}
            payload["rows"][0]["row_note_count"] = 99
            payload["rows"][0]["row_note_extraction_status"] = "no_row_notes"
            payload["rows"][0]["cells"][0]["image_src"] = "/i/lp.png"
            payload["rows"][0]["cells"][0]["image_alt"] = "LP"
            payload["rows"][0]["cells"][6]["cell_note_markers"] = "※"
            payload["rows"][0]["cells"][6]["cell_note_ids"] = "※1"
            payload["rows"][0]["cells"][6]["row_note_reference_candidates"] = {"note_index": 0}
            payload["rows"][0]["cells"][6]["note_linkage_status"] = "parsed_note"
            rows_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            message = str(context.exception)
            self.assertIn("official row 1 input_images must be a list", message)
            self.assertIn("official row 1 row_note_count must match row_notes length", message)
            self.assertIn("official row 1 row_note_extraction_status must be notes_extracted", message)
            self.assertIn("official row 1 cell_count must match cells length", message)
            self.assertIn("official row 1 cell 0 image_src must be a list", message)
            self.assertIn("official row 1 cell 0 image_alt must be a list", message)
            self.assertIn("official row 1 cell 6 cell_note_markers must be a list", message)
            self.assertIn("official row 1 cell 6 cell_note_ids must be a list", message)
            self.assertIn("official row 1 cell 6 row_note_reference_candidates must be a list", message)
            self.assertIn("official row 1 cell 6 note_linkage_status must be a known source-structural status", message)

    def test_artifact_validation_rejects_missing_or_shifted_official_header_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("missing-shifted-header-path")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )
            rows_path = workspace / "official" / "jp" / "official_table_rows.raw.json"
            payload = json.loads(rows_path.read_text(encoding="utf-8"))
            payload["column_header_paths"][5] = ["硬直差", "ヒット"]
            del payload["rows"][0]["cells"][1]["source_column_header_path"]
            payload["rows"][0]["cells"][5]["source_column_header_path"] = ["硬直差", "ヒット"]
            payload["rows"][0]["cells"][5]["source_column_leaf_header"] = "ヒット"
            rows_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(ValueError) as context:
                validate_acquisition_artifacts(report_path, workspace=workspace, roster_path=roster_path)
            message = str(context.exception)
            self.assertIn("column_header_paths must match official contract", message)
            self.assertIn("official row 1 cell 1 missing fields: source_column_header_path", message)
            self.assertIn("official row 1 cell 5 source_column_header_path must be ['硬直差', 'ガード']", message)
            self.assertIn("official row 1 cell 5 source_column_leaf_header must be ガード", message)

    def test_report_guard_requires_successful_supercombo_raw_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("supercombo-raw-count")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
        "supercombo_data": "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            report = acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
                supercombo_fetcher=_fake_supercombo_fetch,
                include_supercombo=True,
            )
            for entry in report["entries"]:
                if entry["source_family"] == "supercombo":
                    entry["supercombo_raw_row_count"] = 0

            with self.assertRaises(ValueError) as context:
                validate_acquisition_report_text(
                    render_acquisition_report(report),
                    roster_characters=[
                        RosterCharacter(
                            character_slug="jp",
                            display_name="JP",
                            official_url="https://www.streetfighter.com/6/ja-jp/character/jp/frame",
                            supercombo_url="https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data",
                        )
                    ],
                )
            self.assertIn("successful SuperCombo capture requires raw rows", str(context.exception))

    def test_report_guard_rejects_mismatched_coverage_aggregates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            workspace = _repo_local_test_workspace("coverage-aggregate")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
        "supercombo_data": "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            report = acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
                supercombo_fetcher=_fake_supercombo_fetch,
                include_supercombo=True,
            )
            report["official_coverage"]["captured_count"] = 0
            report["official_coverage"]["review_item_count"] = 1
            report["official_coverage"]["official_raw_row_count"] = 999
            report["supercombo_coverage"]["supercombo_raw_row_count"] = 999

            with self.assertRaises(ValueError) as context:
                validate_acquisition_report_text(
                    render_acquisition_report(report),
                    roster_characters=[
                        RosterCharacter(
                            character_slug="jp",
                            display_name="JP",
                            official_url="https://www.streetfighter.com/6/ja-jp/character/jp/frame",
                            supercombo_url="https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data",
                        )
                    ],
                )
            message = str(context.exception)
            self.assertIn("official_coverage.captured_count must match successful entries", message)
            self.assertIn("official_coverage.review_item_count must match review_items", message)
            self.assertIn("official_coverage.official_raw_row_count must match entry aggregate", message)
            self.assertIn("supercombo_coverage.supercombo_raw_row_count must match entry aggregate", message)

    def test_report_guard_requires_scrapling_capture_method(self) -> None:
        report_text = """
# Current Source Acquisition Report

## Machine Report

```json
{
  "run_id": "x",
  "captured_at_utc": "2026-05-21T00:00:00Z",
  "source_families": ["official"],
  "roster": {"roster_path": "data/roster/current-character-roster.json", "expected_character_count": 1},
  "official_coverage": {"expected_count": 1, "captured_count": 1, "failed_count": 0, "review_item_count": 0},
  "supercombo_decision": {"status": "queued", "reason": "later"},
  "source_boundary": {
    "full_raw_html_public_commit": "prohibited_without_explicit_review",
    "reviewed_terms_license_robots_attribution": "pending"
  },
  "entries": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "source_family": "official",
      "source_role": "current_fact_authority_candidate",
      "source_url": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
      "final_url": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
      "captured_at_utc": "2026-05-21T00:00:00Z",
      "http_status": 200,
      "content_type": "text/html",
      "source_version_label": "unknown",
      "source_revision_label": "unknown",
      "capture_method": "python_urllib_request",
      "capture_success": true,
      "failure_reason": null,
      "content_hash": "sha256:abc",
      "artifact_boundary": "repo_local_ignored_raw_capture"
    }
  ],
  "review_items": []
}
```
"""

        with self.assertRaises(ValueError) as context:
            validate_acquisition_report_text(
                report_text,
                roster_characters=[
                    RosterCharacter(
                        character_slug="jp",
                        display_name="JP",
                        official_url="https://www.streetfighter.com/6/ja-jp/character/jp/frame",
                        supercombo_url=None,
                    )
                ],
            )
        self.assertIn("capture_method must be scrapling_fetcher", str(context.exception))

    def test_rejects_unapproved_repo_internal_workspace_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roster_path = Path(tmp) / "roster.json"
            report_path = Path(tmp) / "report.md"
            roster_path.write_text('{"characters": []}', encoding="utf-8")
            workspace = repo_root() / "__forbidden_acquisition_workspace__"

            with self.assertRaises(ValueError):
                acquire_official_sources(
                    report_path=report_path,
                    workspace=workspace,
                    run_id="20260521T000000Z",
                    roster_path=roster_path,
                    fetcher=_fake_fetch,
                )

            self.assertFalse(workspace.exists())
            self.assertFalse(report_path.exists())

    def test_rejects_outside_repo_workspace_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            roster_path = root / "roster.json"
            report_path = root / "report.md"
            roster_path.write_text('{"characters": []}', encoding="utf-8")
            workspace = root / "outside-repo-workspace"

            with self.assertRaises(ValueError):
                acquire_official_sources(
                    report_path=report_path,
                    workspace=workspace,
                    run_id="20260521T000000Z",
                    roster_path=roster_path,
                    fetcher=_fake_fetch,
                )

            self.assertFalse(workspace.exists())
            self.assertFalse(report_path.exists())

    def test_allows_approved_repo_local_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roster_path = Path(tmp) / "roster.json"
            report_path = Path(tmp) / "report.md"
            roster_path.write_text(
                """
{
  "characters": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "sources": {
        "official": "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
      }
    }
  ]
}
""",
                encoding="utf-8",
            )
            workspace = _repo_local_test_workspace("approved")
            self.addCleanup(lambda: shutil.rmtree(workspace, ignore_errors=True))
            report = acquire_official_sources(
                report_path=report_path,
                workspace=workspace,
                run_id="20260521T000000Z",
                roster_path=roster_path,
                fetcher=_fake_fetch,
            )

            self.assertEqual(report["official_coverage"]["captured_count"], 1)
            self.assertTrue((workspace / "official" / "jp" / "page.html").exists())

    def test_report_guard_rejects_local_path_and_raw_html(self) -> None:
        local_path = "/" + "home/" + "example/secret"
        report_text = """
# Current Source Acquisition Report

## Machine Report

```json
{
  "run_id": "x",
  "captured_at_utc": "2026-05-21T00:00:00Z",
  "source_families": ["official"],
  "roster": {"roster_path": "data/roster/current-character-roster.json", "expected_character_count": 1},
  "official_coverage": {"expected_count": 1, "captured_count": 1, "failed_count": 0, "review_item_count": 0},
  "supercombo_decision": {"status": "queued", "reason": "later"},
  "source_boundary": {
    "full_raw_html_public_commit": "prohibited_without_explicit_review",
    "reviewed_terms_license_robots_attribution": "pending"
  },
  "entries": [
    {
      "character_slug": "jp",
      "display_name": "JP",
      "source_family": "official",
      "source_role": "current_fact_authority_candidate",
      "source_url": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
      "final_url": "https://www.streetfighter.com/6/ja-jp/character/jp/frame",
      "captured_at_utc": "2026-05-21T00:00:00Z",
      "http_status": 200,
      "content_type": "text/html",
      "source_version_label": "unknown",
      "source_revision_label": "unknown",
      "capture_success": true,
      "failure_reason": null,
      "content_hash": "sha256:abc",
      "artifact_boundary": "repo_local_ignored_raw_capture"
    }
  ],
  "review_items": []
}
```

<html>LOCAL_PATH</html>
""".replace("LOCAL_PATH", local_path)

        with self.assertRaises(ValueError) as context:
            validate_acquisition_report_text(
                report_text,
                roster_characters=[
                    RosterCharacter(
                        character_slug="jp",
                        display_name="JP",
                        official_url="https://www.streetfighter.com/6/ja-jp/character/jp/frame",
                        supercombo_url=None,
                    )
                ],
            )
        self.assertIn("Forbidden report content", str(context.exception))


if __name__ == "__main__":
    unittest.main()
