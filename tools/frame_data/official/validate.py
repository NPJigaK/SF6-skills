#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from tools.frame_data.official.capture import (
    frame_data_payload_from_dom,
    unexpected_body_rows,
    validate_mode_tab_state,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", help="Deprecated; frame-data raw uses fixed latest paths.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--mode", choices=["classic", "modern"], action="append")
    return parser.parse_args(argv)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def table_html_from_page(page_html: str) -> str:
    match = re.search(r"<table\b.*?</table>", page_html, flags=re.DOTALL)
    if not match:
        raise ValueError("page.html does not contain a table element")
    return match.group(0)


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def expected_frame_data_for_comparison(actual: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    actual_source = actual.get("source")
    expected_source = expected.get("source")
    if (
        isinstance(actual_source, dict)
        and isinstance(expected_source, dict)
        and "source_revision" not in actual_source
        and "source_revision" in expected_source
    ):
        return {
            **expected,
            "source": {
                key: value
                for key, value in expected_source.items()
                if key != "source_revision"
            },
        }
    return expected


def validate_mode(repo_root: Path, character_slug: str, mode: str) -> dict[str, Any]:
    raw_dir = repo_root / "raw" / "frame-data" / "official" / character_slug / mode
    output_dir = repo_root / "wiki" / "outputs" / "data" / "frame-data" / "official" / character_slug

    page_html_path = raw_dir / "page.html"
    table_dom_path = raw_dir / "table.dom.json"
    metadata_path = raw_dir / "metadata.json"
    frame_data_path = output_dir / f"{mode}.json"

    page_html = page_html_path.read_text(encoding="utf-8")
    table_dom = json.loads(table_dom_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    frame_data = json.loads(frame_data_path.read_text(encoding="utf-8"))

    table_hash_from_html = sha256_text(table_html_from_page(page_html))
    assert_equal(table_hash_from_html, table_dom["table_sha256"], f"{mode} page.html table hash")
    tab_state = metadata.get("capture_adjustments", {}).get("tab_state")
    if tab_state:
        validate_mode_tab_state(mode, tab_state)

    unexpected_rows = table_dom.get("unexpected_rows", unexpected_body_rows(table_dom["rows"]))
    if unexpected_rows:
        details = ", ".join(
            f"row_index={row.get('row_index')} cell_count={row.get('cell_count')}"
            for row in unexpected_rows[:5]
        )
        raise AssertionError(f"{mode} raw DOM has unexpected row shapes: {details}")

    expected_frame_data = frame_data_payload_from_dom(table_dom)
    expected_rows = expected_frame_data["rows"]
    actual_rows = frame_data.get("rows", [])
    if actual_rows != expected_rows:
        for row_index, (actual_row, expected_row) in enumerate(zip(actual_rows, expected_rows, strict=False), start=1):
            if actual_row != expected_row:
                differing_fields = [
                    field
                    for field in sorted(set(actual_row) | set(expected_row))
                    if actual_row.get(field) != expected_row.get(field)
                ]
                raise AssertionError(
                    f"{mode} JSON rows differ from raw DOM at data row {row_index}; "
                    f"fields: {', '.join(differing_fields)}"
                )
        raise AssertionError(
            f"{mode} JSON row count differs from raw DOM: "
            f"json={len(actual_rows)}, dom={len(expected_rows)}"
        )

    comparable_expected_frame_data = expected_frame_data_for_comparison(frame_data, expected_frame_data)
    assert_equal(frame_data, comparable_expected_frame_data, f"{mode} frame data JSON")

    manifest_count = metadata["artifacts"]["table_dom_json"]["data_row_count"]
    assert_equal(manifest_count, len(actual_rows), f"{mode} metadata row count")
    assert_equal(table_dom["data_row_count"], len(actual_rows), f"{mode} table DOM row count")
    assert_equal(table_dom.get("unexpected_row_count", 0), 0, f"{mode} unexpected row count")

    screenshot = metadata["artifacts"]["screenshot_png"]
    horizontal_metrics = metadata["horizontal_metrics"]
    table_rect = table_dom["table_rect"]
    if screenshot["width"] < int(horizontal_metrics["table_rect_right"]):
        raise AssertionError(
            f"{mode} screenshot width {screenshot['width']} does not cover table right edge "
            f"{horizontal_metrics['table_rect_right']}"
        )
    if screenshot["height"] < float(table_rect["height"]):
        raise AssertionError(
            f"{mode} screenshot height {screenshot['height']} is smaller than table height "
            f"{table_rect['height']}"
        )
    overlay_counts = metadata["overlay_visible_counts_after_cleanup"]
    assert_equal(overlay_counts.get("cookiebot"), 0, f"{mode} visible Cookiebot overlays")
    assert_equal(overlay_counts.get("navigation"), 0, f"{mode} visible navigation overlays")

    return {
        "mode": mode,
        "row_count": len(actual_rows),
        "category_row_count": table_dom["category_row_count"],
        "field_meaning_records": len(frame_data["field_meanings"]["records"]),
        "table_sha256": table_dom["table_sha256"],
        "screenshot_width": screenshot["width"],
        "screenshot_height": screenshot["height"],
    }


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    modes = args.mode or ["classic", "modern"]
    results = [
        validate_mode(args.repo_root, args.character_slug, mode)
        for mode in modes
    ]
    print(json.dumps({"validated": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
