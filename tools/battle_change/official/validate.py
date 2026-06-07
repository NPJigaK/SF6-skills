#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tools.battle_change.official.capture import (
    adjust_from_payload,
    extract_next_data,
    sha256_file,
    validate_adjust_payload,
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def validate_artifact(path: Path, artifact: dict[str, Any], label: str) -> None:
    if not path.exists():
        raise AssertionError(f"{label} missing: {path}")
    assert_equal(path.stat().st_size, artifact["byte_count"], f"{label} byte_count")
    assert_equal(sha256_file(path), artifact["sha256"], f"{label} sha256")


def validate_capture_files(
    *,
    page_html_path: Path,
    data_json_path: Path,
    metadata_path: Path,
    expected_version: str | None,
    expected_build_id: str,
    label: str,
) -> dict[str, Any]:
    metadata = read_json(metadata_path)
    artifacts = metadata["artifacts"]
    validate_artifact(page_html_path, artifacts["page_html"], f"{label} page_html")
    validate_artifact(data_json_path, artifacts["data_json"], f"{label} data_json")
    assert_equal(metadata.get("build_id"), expected_build_id, f"{label} build_id")

    page_html = page_html_path.read_text(encoding="utf-8")
    data_payload = read_json(data_json_path)
    html_adjust = adjust_from_payload(extract_next_data(page_html))
    data_adjust = adjust_from_payload(data_payload)
    assert_equal(html_adjust, data_adjust, f"{label} HTML adjust vs data JSON adjust")
    summary = validate_adjust_payload(data_adjust, expected_version=expected_version)
    assert_equal(metadata["validation_summary"], summary, f"{label} validation_summary")
    return summary


def repo_path(repo_root: Path, relative_path: str) -> Path:
    return repo_root / relative_path.replace("/", "\\")


def validate_raw_capture(repo_root: Path) -> dict[str, Any]:
    raw_root = repo_root / "raw" / "battle-change" / "official"
    manifest_path = raw_root / "manifest.json"
    manifest = read_json(manifest_path)
    build_id = manifest["build_id"]
    current_version = manifest["current_version"]
    versions = manifest["versions"]
    captures = manifest["captures"]
    assert_equal(manifest["version_count"], len(captures), "manifest version_count")
    assert_equal([item["id"] for item in versions], [item["version_id"] for item in captures], "manifest version order")

    discovery = manifest["discovery"]
    discovery_summary = validate_capture_files(
        page_html_path=repo_path(repo_root, discovery["page_html"]),
        data_json_path=repo_path(repo_root, discovery["data_json"]),
        metadata_path=repo_path(repo_root, discovery["metadata_json"]),
        expected_version=current_version,
        expected_build_id=build_id,
        label="discovery",
    )
    assert_equal(discovery_summary["version_count"], len(versions), "discovery version_count")

    total_policy_count = 0
    total_common_section_count = 0
    total_common_change_count = 0
    total_fighter_count = 0
    total_fighter_detail_count = 0
    total_fighter_change_count = 0
    validated_versions: list[dict[str, Any]] = []

    for capture in captures:
        version_id = capture["version_id"]
        summary = validate_capture_files(
            page_html_path=repo_path(repo_root, capture["page_html"]),
            data_json_path=repo_path(repo_root, capture["data_json"]),
            metadata_path=repo_path(repo_root, capture["metadata_json"]),
            expected_version=version_id,
            expected_build_id=build_id,
            label=f"version {version_id}",
        )
        total_policy_count += summary["policy_count"]
        total_common_section_count += summary["common_section_count"]
        total_common_change_count += summary["common_change_count"]
        total_fighter_count += summary["fighter_count"]
        total_fighter_detail_count += summary["fighter_detail_count"]
        total_fighter_change_count += summary["fighter_change_count"]
        validated_versions.append(summary)

    return {
        "manifest": manifest_path.relative_to(repo_root).as_posix(),
        "build_id": build_id,
        "current_version": current_version,
        "version_count": len(validated_versions),
        "total_policy_count": total_policy_count,
        "total_common_section_count": total_common_section_count,
        "total_common_change_count": total_common_change_count,
        "total_fighter_count": total_fighter_count,
        "total_fighter_detail_count": total_fighter_detail_count,
        "total_fighter_change_count": total_fighter_change_count,
        "versions": validated_versions,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = validate_raw_capture(args.repo_root.resolve())
    print(json.dumps({"validated": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
