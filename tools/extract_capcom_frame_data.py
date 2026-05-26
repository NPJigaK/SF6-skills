#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from capture_capcom_frame_data import csv_rows_from_dom, field_meanings_from_dom, write_csv, write_json


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", default="2026-05-26")
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--mode", choices=["classic", "modern"], action="append")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    modes = args.mode or ["classic", "modern"]
    output_dir = args.repo_root / "wiki" / "outputs" / "data" / "frame-data" / args.character_slug
    for mode in modes:
        raw_dir = (
            args.repo_root
            / "raw"
            / "official"
            / "frame-data"
            / args.date_label
            / args.character_slug
            / mode
        )
        table_dom_path = raw_dir / "table.dom.json"
        if not table_dom_path.exists():
            raise FileNotFoundError(table_dom_path)
        table_dom = json.loads(table_dom_path.read_text(encoding="utf-8"))
        raw_rel = raw_dir.relative_to(args.repo_root).as_posix()
        rows = csv_rows_from_dom(
            table_dom,
            raw_capture_path=raw_rel,
            screenshot_path=f"{raw_rel}/screenshot.png",
        )
        write_csv(output_dir / f"{mode}.csv", rows)
        write_json(output_dir / f"{mode}.field-meanings.json", field_meanings_from_dom(table_dom))
        print(f"{mode}: wrote {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
