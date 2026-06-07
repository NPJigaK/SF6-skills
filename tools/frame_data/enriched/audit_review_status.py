#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


RISK_FLAG_PREFIXES = (
    "manual_match",
    "ambiguous_match",
    "basic_field_conflict",
    "condition_dependent_supercombo_field",
    "multiple_candidates",
    "supercombo_row_reused",
    "uncomparable_basic_field",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def has_risky_flag(flags: str) -> bool:
    return any(
        flag.startswith(RISK_FLAG_PREFIXES)
        for flag in flags.split(";")
        if flag
    )


def condition_parenthetical_fields(comparisons: dict[str, Any]) -> list[str]:
    fields: list[str] = []
    for field, comparison in comparisons.items():
        if field not in {"damage", "startup", "recovery"}:
            continue
        if comparison.get("comparable") is not True or comparison.get("match") is not True:
            continue
        supercombo_raw = str(comparison.get("supercombo_raw", "")).strip()
        if re.fullmatch(r"[+-]?\d+\s*\([^)]*\)", supercombo_raw):
            fields.append(field)
    return fields


def audit(repo_root: Path) -> dict[str, object]:
    root = repo_root / "wiki" / "outputs" / "data" / "frame-data" / "official-supercombo-enriched"
    if not root.exists():
        raise FileNotFoundError(f"missing enriched data root: {root}")

    failures: list[dict[str, str]] = []
    rows_checked = 0

    for data_path in sorted(root.glob("*/classic-supercombo.json")):
        slug = data_path.parent.name
        for row in read_json(data_path)["rows"]:
            rows_checked += 1
            status = row.get("enrichment_status", "")
            flags = row.get("enrichment_review_flags", "")
            if status == "enriched" and has_risky_flag(flags):
                failures.append(
                    {
                        "slug": slug,
                        "row_order": row.get("row_order", ""),
                        "move_name": row.get("move_name", ""),
                        "status": status,
                        "flags": flags,
                        "supercombo_move_id": row.get("supercombo_move_id", ""),
                    }
                )

            if status == "enriched":
                comparisons = row.get("supercombo_field_comparisons", {})
                if not isinstance(comparisons, dict):
                    raise TypeError("supercombo_field_comparisons must be an object")
                parenthetical_fields = condition_parenthetical_fields(comparisons)
                if parenthetical_fields:
                    failures.append(
                        {
                            "slug": slug,
                            "row_order": row.get("row_order", ""),
                            "move_name": row.get("move_name", ""),
                            "status": status,
                            "flags": flags,
                            "supercombo_move_id": row.get("supercombo_move_id", ""),
                            "reason": "condition_parenthetical_enriched",
                            "fields": ",".join(parenthetical_fields),
                        }
                    )

            if (
                slug == "alex"
                and row.get("row_order") == "54"
                and row.get("move_name") == "パワードロップ"
                and status == "enriched"
            ):
                failures.append(
                    {
                        "slug": slug,
                        "row_order": row.get("row_order", ""),
                        "move_name": row.get("move_name", ""),
                        "status": status,
                        "flags": flags,
                        "supercombo_move_id": row.get("supercombo_move_id", ""),
                        "reason": "alex_power_drop_regression",
                    }
                )

    if rows_checked == 0:
        raise RuntimeError(f"no enriched rows found under {root}")

    return {
        "rows_checked": rows_checked,
        "failure_count": len(failures),
        "failures": failures[:50],
        "truncated": len(failures) > 50,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = audit(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["failure_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
