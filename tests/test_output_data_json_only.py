from __future__ import annotations

import re
from pathlib import Path

QUERY_FACING_WIKI_ROOTS = [
    Path("wiki") / "concepts",
    Path("wiki") / "entities",
    Path("wiki") / "outputs",
    Path("wiki") / "questions",
    Path("wiki") / "sources",
    Path("wiki") / "syntheses",
]


def test_wiki_output_data_contains_no_csv_files() -> None:
    output_root = Path("wiki") / "outputs" / "data"
    csv_files = sorted(path.as_posix() for path in output_root.rglob("*.csv"))

    assert csv_files == []


def test_output_schemas_do_not_advertise_csv_contracts() -> None:
    output_root = Path("wiki") / "outputs" / "data"
    offenders: list[str] = []
    for schema_path in sorted(output_root.rglob("schema.json")):
        text = schema_path.read_text(encoding="utf-8")
        if ".csv" in text or "_csv" in text:
            offenders.append(schema_path.as_posix())

    assert offenders == []


def test_query_facing_wiki_pages_do_not_advertise_removed_output_contracts() -> None:
    forbidden_patterns = [
        re.compile(r"wiki/outputs/data/[^`\s)]+\.csv"),
        re.compile(r"field-meanings\.json"),
        re.compile(r"\binput_token_json\b"),
        re.compile(r"\bfield_comparisons_json\b"),
        re.compile(r"派生 CSV|公式 CSV|補助列付き CSV|公式CSV|CSV値|CSV と raw DOM"),
    ]

    offenders: list[str] = []
    for root in QUERY_FACING_WIKI_ROOTS:
        for markdown_path in sorted(root.rglob("*.md")):
            text = markdown_path.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                match = pattern.search(text)
                if match:
                    offenders.append(f"{markdown_path.as_posix()}: {match.group(0)}")

    assert offenders == []


def test_wiki_output_data_paths_in_query_facing_pages_exist() -> None:
    output_path_pattern = re.compile(r"`(wiki/outputs/data/[^`\s)]+)`")

    missing_paths: list[str] = []
    for root in QUERY_FACING_WIKI_ROOTS:
        for markdown_path in sorted(root.rglob("*.md")):
            text = markdown_path.read_text(encoding="utf-8")
            for output_path in output_path_pattern.findall(text):
                if "<" in output_path or ">" in output_path:
                    continue
                if not Path(output_path).exists():
                    missing_paths.append(f"{markdown_path.as_posix()}: {output_path}")

    assert missing_paths == []
