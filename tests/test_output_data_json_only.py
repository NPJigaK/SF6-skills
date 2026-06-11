from __future__ import annotations

import json
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


def test_battle_change_move_index_version_ids_are_unique() -> None:
    paths = [
        Path("wiki") / "outputs" / "data" / "battle-change" / "official" / "move-change-index.json",
        Path("wiki") / "outputs" / "data" / "battle-change" / "supercombo-patch-notes" / "move-change-index.json",
    ]

    offenders: list[str] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        version_field = "version_ids" if "official" in path.parts else "versions"
        for row in payload["rows"]:
            versions = row[version_field]
            if len(versions) != len(set(versions)):
                offenders.append(f"{path.as_posix()}: {row['normalized_target_key']}")

    assert offenders == []


def test_battle_change_json_fields_cover_row_keys() -> None:
    output_root = Path("wiki") / "outputs" / "data" / "battle-change"

    offenders: list[str] = []
    for path in sorted(output_root.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("rows")
        if not isinstance(rows, list):
            continue
        fields = payload.get("fields")
        if not isinstance(fields, list):
            offenders.append(f"{path.as_posix()}: missing fields")
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            missing = sorted(set(row) - set(fields))
            if missing:
                offenders.append(f"{path.as_posix()} row {index}: missing fields {missing}")

    assert offenders == []


def test_battle_change_fighter_indexes_use_frame_data_character_slugs() -> None:
    paths = [
        Path("wiki") / "outputs" / "data" / "battle-change" / "official" / "move-change-index.json",
        Path("wiki") / "outputs" / "data" / "battle-change" / "supercombo-patch-notes" / "move-change-index.json",
    ]
    frame_data_root = Path("wiki") / "outputs" / "data" / "frame-data" / "official"

    offenders: list[str] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload["rows"]:
            if row["scope"] != "fighter":
                continue
            character_slug = row.get("character_slug", "")
            if not character_slug:
                offenders.append(f"{path.as_posix()}: {row['normalized_target_key']} has no character_slug")
                continue
            if not (frame_data_root / character_slug).exists():
                offenders.append(f"{path.as_posix()}: {character_slug} has no official frame-data output")

    assert offenders == []
