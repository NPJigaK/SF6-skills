#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from tools.battle_change.official.capture import adjust_from_payload, validate_adjust_payload


CSV_FIELDS = [
    "version_order",
    "version_id",
    "version_title",
    "version_selector_title",
    "version_title_mismatch",
    "section_type",
    "section_order",
    "body_order",
    "policy_title",
    "common_title",
    "fighter_order",
    "fighter_id",
    "fighter_alpha",
    "fighter_tool_name",
    "fighter_url_name",
    "detail_order",
    "detail_title",
    "category",
    "text_html",
    "data_json_path",
]


def title_mismatch(page_title: str, selector_title: str) -> str:
    return str(page_title != selector_title).lower()


def blank_row(
    version_order: int,
    adjust: dict[str, Any],
    section_type: str,
    data_json_path: str,
    version_selector_title: str,
) -> dict[str, str]:
    version_title = str(adjust["title"])
    return {
        "version_order": str(version_order),
        "version_id": str(adjust["current_version"]),
        "version_title": version_title,
        "version_selector_title": version_selector_title,
        "version_title_mismatch": title_mismatch(version_title, version_selector_title),
        "section_type": section_type,
        "section_order": "",
        "body_order": "",
        "policy_title": "",
        "common_title": "",
        "fighter_order": "",
        "fighter_id": "",
        "fighter_alpha": "",
        "fighter_tool_name": "",
        "fighter_url_name": "",
        "detail_order": "",
        "detail_title": "",
        "category": "",
        "text_html": "",
        "data_json_path": data_json_path,
    }


def flatten_adjust(
    version_order: int,
    adjust: dict[str, Any],
    data_json_path: str,
    version_selector_title: str | None = None,
) -> list[dict[str, str]]:
    validate_adjust_payload(adjust, expected_version=adjust.get("current_version"))
    selector_title = version_selector_title if version_selector_title is not None else str(adjust["title"])
    rows: list[dict[str, str]] = []

    for policy_index, item in enumerate(adjust.get("policy", []), start=1):
        row = blank_row(version_order, adjust, "policy", data_json_path, selector_title)
        row.update(
            {
                "section_order": str(policy_index),
                "policy_title": str(item.get("title", "")),
                "text_html": str(item.get("text", "")),
            }
        )
        rows.append(row)

    for common_index, section in enumerate(adjust.get("common", []), start=1):
        for body_index, body in enumerate(section.get("body", []), start=1):
            row = blank_row(version_order, adjust, "common", data_json_path, selector_title)
            row.update(
                {
                    "section_order": str(common_index),
                    "body_order": str(body_index),
                    "common_title": str(section.get("title", "")),
                    "category": str(body.get("category", "")),
                    "text_html": str(body.get("text", "")),
                }
            )
            rows.append(row)

    for fighter_index, fighter in enumerate(adjust.get("fighter", []), start=1):
        for detail_index, detail in enumerate(fighter.get("detail", []), start=1):
            for body_index, body in enumerate(detail.get("body", []), start=1):
                row = blank_row(version_order, adjust, "fighter", data_json_path, selector_title)
                row.update(
                    {
                        "section_order": str(fighter_index),
                        "body_order": str(body_index),
                        "fighter_order": str(fighter_index),
                        "fighter_id": str(fighter.get("fighter_id", "")),
                        "fighter_alpha": str(fighter.get("fighter_alpha", "")),
                        "fighter_tool_name": str(fighter.get("fighter_tool_name", "")),
                        "fighter_url_name": str(fighter.get("fighter_url_name", "")),
                        "detail_order": str(detail_index),
                        "detail_title": str(detail.get("title", "")),
                        "category": str(body.get("category", "")),
                        "text_html": str(body.get("text", "")),
                    }
                )
                rows.append(row)

    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_all(repo_root: Path) -> dict[str, Any]:
    raw_root = repo_root / "raw" / "battle-change" / "official"
    manifest_path = raw_root / "manifest.json"
    manifest = read_json(manifest_path)
    output_dir = repo_root / "wiki" / "outputs" / "data" / "battle-change" / "official"

    version_rows: list[dict[str, str]] = []
    change_rows: list[dict[str, str]] = []
    selector_titles = {
        str(version["id"]): str(version["title"])
        for version in manifest["versions"]
    }
    for version_order, capture in enumerate(manifest["captures"], start=1):
        data_json_path = repo_root / capture["data_json"].replace("/", "\\")
        payload = read_json(data_json_path)
        adjust = adjust_from_payload(payload)
        summary = validate_adjust_payload(adjust, expected_version=capture["version_id"])
        selector_title = selector_titles.get(capture["version_id"], summary["title"])
        version_rows.append(
            {
                "version_order": str(version_order),
                "version_id": summary["version_id"],
                "version_title": summary["title"],
                "version_selector_title": selector_title,
                "version_title_mismatch": title_mismatch(summary["title"], selector_title),
                "policy_count": str(summary["policy_count"]),
                "common_section_count": str(summary["common_section_count"]),
                "common_change_count": str(summary["common_change_count"]),
                "fighter_count": str(summary["fighter_count"]),
                "fighter_detail_count": str(summary["fighter_detail_count"]),
                "fighter_change_count": str(summary["fighter_change_count"]),
                "data_json_path": capture["data_json"],
            }
        )
        change_rows.extend(
            flatten_adjust(
                version_order,
                adjust,
                capture["data_json"],
                version_selector_title=selector_title,
            )
        )

    schema = {
        "schema_version": "capcom_battle_change_derived_outputs/v1",
        "source_manifest": "raw/battle-change/official/manifest.json",
        "changes_fields": CSV_FIELDS,
        "version_fields": list(version_rows[0].keys()) if version_rows else [],
        "notes": [
            "`version_title` is the per-version page title from that version's data JSON.",
            "`version_selector_title` is the title from the discovery page version selector.",
            "`version_title_mismatch` is true when those two official title strings differ.",
            "`text_html` preserves official HTML fragments such as <br>, span, and class attributes.",
            "Rows are derived from raw `_next/data` JSON, not translated or normalized source replacements.",
        ],
    }

    write_csv(output_dir / "versions.csv", version_rows, list(version_rows[0].keys()) if version_rows else [])
    write_csv(output_dir / "changes.csv", change_rows, CSV_FIELDS)
    write_json(output_dir / "changes.json", change_rows)
    write_json(output_dir / "schema.json", schema)
    return {
        "output_dir": output_dir.relative_to(repo_root).as_posix(),
        "version_count": len(version_rows),
        "change_count": len(change_rows),
        "policy_count": sum(1 for row in change_rows if row["section_type"] == "policy"),
        "common_change_count": sum(1 for row in change_rows if row["section_type"] == "common"),
        "fighter_change_count": sum(1 for row in change_rows if row["section_type"] == "fighter"),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = extract_all(args.repo_root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
