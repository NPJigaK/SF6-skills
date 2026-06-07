#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tools.frame_data.official.capture import frame_data_payload_from_dom, write_json


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", help="Deprecated; frame-data raw uses fixed latest paths.")
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--mode", choices=["classic", "modern"], action="append")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    modes = args.mode or ["classic", "modern"]
    output_dir = args.repo_root / "wiki" / "outputs" / "data" / "frame-data" / "official" / args.character_slug
    for mode in modes:
        raw_dir = (
            args.repo_root
            / "raw"
            / "frame-data"
            / "official"
            / args.character_slug
            / mode
        )
        table_dom_path = raw_dir / "table.dom.json"
        if not table_dom_path.exists():
            raise FileNotFoundError(table_dom_path)
        table_dom = json.loads(table_dom_path.read_text(encoding="utf-8"))
        payload = frame_data_payload_from_dom(table_dom)
        write_json(output_dir / f"{mode}.json", payload)
        print(f"{mode}: wrote {payload['row_count']} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
