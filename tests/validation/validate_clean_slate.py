from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "docs/PLAN.md",
    "docs/execplans/TEMPLATE.md",
    "docs/execplans/2026-05-20-new-app-scaffold.md",
    "pyproject.toml",
    "src/sf6_knowledge_coach/cli.py",
    "tests/test_cli.py",
    "tests/validation/validate_clean_slate.py",
    "data/aliases/ja-query-fixtures.json",
    "data/exports/jp/official_raw.json",
]

LEGACY_DIRS_EXPECTED_GONE = [
    ".github",
    "contracts",
    "docs/architecture",
    "docs/testing",
    "evals",
    "ingest",
    "knowledge",
    "packages",
    "packs",
    "runtime",
    "skills",
    "tools",
    "workflows",
]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required clean-slate path: {relative}")

    for relative in LEGACY_DIRS_EXPECTED_GONE:
        if (ROOT / relative).exists():
            errors.append(f"Legacy path should remain deleted: {relative}")

    for json_path in (ROOT / "data").rglob("*.json"):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON: {json_path.relative_to(ROOT)}: {exc}")

    plan_text = (ROOT / "docs" / "PLAN.md").read_text(encoding="utf-8")
    if "This PLAN is the architecture contract." not in plan_text:
        errors.append("docs/PLAN.md lacks the English architecture-contract note.")
    if "このPLANは全体アーキテクチャ契約である。" not in plan_text:
        errors.append("docs/PLAN.md lacks the Japanese architecture-contract note.")

    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for heading in ("## Project Goal", "## Plan Conformance", "## Hard Rules", "## Validation", "## Done"):
        if heading not in agents_text:
            errors.append(f"AGENTS.md lacks required heading: {heading}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Clean-slate validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
