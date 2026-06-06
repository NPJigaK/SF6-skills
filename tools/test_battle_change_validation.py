from __future__ import annotations

import json
import tempfile
from hashlib import sha256
from pathlib import Path

from validate_capcom_battle_change import validate_raw_capture


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2))


def next_html(payload: object) -> str:
    data = json.dumps(payload, ensure_ascii=False).replace('"', "&quot;")
    return f'<html><script id="__NEXT_DATA__" type="application/json">{data}</script></html>'


def artifact(path: Path) -> dict[str, object]:
    return {
        "path": path.name,
        "sha256": "sha256:" + sha256(path.read_bytes()).hexdigest(),
        "byte_count": path.stat().st_size,
    }


def write_minimal_capture(repo_root: Path) -> None:
    adjust = {
        "title": "2026.04.15 update",
        "current_version": "20260415",
        "versions": [{"id": "20260415", "title": "2026.04.15 update"}],
        "policy": [],
        "common": [
            {
                "title": "ドライブパリィ",
                "body": [{"category": "調整", "text": "本文"}],
            }
        ],
        "fighter": [],
        "fighter_list": [],
        "current_fighter": "",
        "title_bg": "",
    }
    html_payload = {"buildId": "build-123", "props": {"pageProps": {"adjust": adjust}}}
    data_payload = {"pageProps": {"adjust": adjust}}
    raw_root = repo_root / "raw" / "battle-change" / "official"

    discovery_dir = raw_root / "discovery"
    write_text(discovery_dir / "page.html", next_html(html_payload))
    write_json(discovery_dir / "data.json", data_payload)
    write_json(
        discovery_dir / "metadata.json",
        {
            "build_id": "build-123",
            "current_version": "20260415",
            "validation_summary": {
                "version_id": "20260415",
                "title": "2026.04.15 update",
                "policy_count": 0,
                "common_section_count": 1,
                "common_change_count": 1,
                "fighter_count": 0,
                "fighter_detail_count": 0,
                "fighter_change_count": 0,
                "version_count": 1,
                "fighter_list_count": 0,
            },
            "artifacts": {
                "page_html": artifact(discovery_dir / "page.html"),
                "data_json": artifact(discovery_dir / "data.json"),
            },
        },
    )

    version_dir = raw_root / "versions" / "20260415"
    write_text(version_dir / "page.html", next_html(html_payload))
    write_json(version_dir / "data.json", data_payload)
    write_json(
        version_dir / "metadata.json",
        {
            "build_id": "build-123",
            "version_id": "20260415",
            "title": "2026.04.15 update",
            "validation_summary": {
                "version_id": "20260415",
                "title": "2026.04.15 update",
                "policy_count": 0,
                "common_section_count": 1,
                "common_change_count": 1,
                "fighter_count": 0,
                "fighter_detail_count": 0,
                "fighter_change_count": 0,
                "version_count": 1,
                "fighter_list_count": 0,
            },
            "artifacts": {
                "page_html": artifact(version_dir / "page.html"),
                "data_json": artifact(version_dir / "data.json"),
            },
        },
    )

    write_json(
        raw_root / "manifest.json",
        {
            "build_id": "build-123",
            "current_version": "20260415",
            "version_count": 1,
            "versions": [{"id": "20260415", "title": "2026.04.15 update"}],
            "discovery": {
                "page_html": "raw/battle-change/official/discovery/page.html",
                "data_json": "raw/battle-change/official/discovery/data.json",
                "metadata_json": "raw/battle-change/official/discovery/metadata.json",
            },
            "captures": [
                {
                    "version_id": "20260415",
                    "title": "2026.04.15 update",
                    "page_html": "raw/battle-change/official/versions/20260415/page.html",
                    "data_json": "raw/battle-change/official/versions/20260415/data.json",
                    "metadata_json": "raw/battle-change/official/versions/20260415/metadata.json",
                }
            ],
        },
    )


def test_validate_raw_capture_accepts_minimal_valid_tree() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_root = Path(tmp_dir)
        write_minimal_capture(repo_root)

        result = validate_raw_capture(repo_root)

        assert result["current_version"] == "20260415"
        assert result["version_count"] == 1
        assert result["total_common_change_count"] == 1
        assert result["total_fighter_change_count"] == 0


def test_validate_raw_capture_rejects_tampered_artifact() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_root = Path(tmp_dir)
        write_minimal_capture(repo_root)
        (repo_root / "raw" / "battle-change" / "official" / "versions" / "20260415" / "data.json").write_text(
            '{"pageProps":{"adjust":{"current_version":"tampered"}}}',
            encoding="utf-8",
        )

        try:
            validate_raw_capture(repo_root)
        except AssertionError as exc:
            assert "data_json" in str(exc)
        else:
            raise AssertionError("tampered raw artifact should be rejected")


def main() -> int:
    test_validate_raw_capture_accepts_minimal_valid_tree()
    test_validate_raw_capture_rejects_tampered_artifact()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
