#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from capture_capcom_frame_data import csv_rows_from_dom, field_meanings_from_dom


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", help="Deprecated; frame-data raw uses fixed latest paths.")
    parser.add_argument("--character-slug", required=True)
    parser.add_argument("--mode", choices=["classic", "modern"], action="append")
    return parser.parse_args(argv)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table_html_from_page(page_html: str) -> str:
    match = re.search(r"<table\b.*?</table>", page_html, flags=re.DOTALL)
    if not match:
        raise ValueError("page.html does not contain a table element")
    return match.group(0)


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def validate_mode(repo_root: Path, character_slug: str, mode: str) -> dict[str, Any]:
    raw_dir = repo_root / "raw" / "frame-data" / "official" / character_slug / mode
    output_dir = repo_root / "wiki" / "outputs" / "data" / "frame-data" / character_slug

    page_html_path = raw_dir / "page.html"
    table_dom_path = raw_dir / "table.dom.json"
    metadata_path = raw_dir / "metadata.json"
    csv_path = output_dir / f"{mode}.csv"
    field_meanings_path = output_dir / f"{mode}.field-meanings.json"

    page_html = page_html_path.read_text(encoding="utf-8")
    table_dom = json.loads(table_dom_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    csv_rows = read_csv(csv_path)
    field_meanings = json.loads(field_meanings_path.read_text(encoding="utf-8"))

    table_hash_from_html = sha256_text(table_html_from_page(page_html))
    assert_equal(table_hash_from_html, table_dom["table_sha256"], f"{mode} page.html table hash")

    expected_rows = csv_rows_from_dom(table_dom)
    if csv_rows != expected_rows:
        for row_index, (actual_row, expected_row) in enumerate(zip(csv_rows, expected_rows, strict=False), start=1):
            if actual_row != expected_row:
                differing_fields = [
                    field
                    for field in sorted(set(actual_row) | set(expected_row))
                    if actual_row.get(field) != expected_row.get(field)
                ]
                raise AssertionError(
                    f"{mode} CSV differs from raw DOM at data row {row_index}; "
                    f"fields: {', '.join(differing_fields)}"
                )
        raise AssertionError(
            f"{mode} CSV row count differs from raw DOM: "
            f"csv={len(csv_rows)}, dom={len(expected_rows)}"
        )

    expected_field_meanings = field_meanings_from_dom(table_dom)
    assert_equal(field_meanings, expected_field_meanings, f"{mode} field meanings")

    manifest_count = metadata["artifacts"]["table_dom_json"]["data_row_count"]
    assert_equal(manifest_count, len(csv_rows), f"{mode} metadata row count")
    assert_equal(table_dom["data_row_count"], len(csv_rows), f"{mode} table DOM row count")

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
        "row_count": len(csv_rows),
        "category_row_count": table_dom["category_row_count"],
        "field_meaning_records": len(field_meanings["records"]),
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
