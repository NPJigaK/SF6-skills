from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any

from .paths import repo_root
from .source_acquisition import (
    default_workspace,
    load_acquisition_report,
    validate_acquisition_artifacts,
    validate_acquisition_report,
)


RUN_ID = "20260521T025403Z"
REPORT_PATH = Path("docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md")
SUMMARY_JSON_PATH = Path("data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json")
SUMMARY_MD_PATH = Path("docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md")
SUMMARY_SCHEMA_VERSION = "value_shape_inventory_summary/v1"
MAX_EXAMPLES_PER_FIELD = 5
MAX_REVIEW_ITEM_EXAMPLES = 5
MAX_PUBLIC_RAW_VALUE_CHARS = 120
SHAPE_CLASSES = [
    "scalar",
    "signed_frame",
    "range",
    "plus_expression",
    "note_prefixed",
    "note_suffixed",
    "note_separated_alternate",
    "hidden_detail",
    "multihit",
    "conditional",
    "landing_expression",
    "until_landing",
    "categorical",
    "prose",
    "blank",
    "dash_variant",
    "percent_expression",
    "raw_only",
    "unclassified",
]
FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\\\\Users\\\\"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)\b(?:answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault|browser profile)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump)\b"),
]


@dataclass
class Example:
    raw_value: str
    raw_value_sha256: str
    character_slug: str
    source_family: str
    source_label: str
    source_header_path: list[str]
    shape_classes: list[str]
    example_scope: str


@dataclass
class FieldSummary:
    source_family: str
    source_role: str
    source_label: str
    source_header_path: tuple[str, ...]
    shape_counts: Counter[str] = field(default_factory=Counter)
    character_slugs: set[str] = field(default_factory=set)
    row_or_cell_count: int = 0
    representative_examples: list[Example] = field(default_factory=list)

    def add_observation(self, character_slug: str, raw_value: str, shapes: list[str]) -> None:
        self.character_slugs.add(character_slug)
        self.row_or_cell_count += 1
        self.shape_counts.update(shapes)
        self._maybe_add_example(character_slug, raw_value, shapes)

    def _maybe_add_example(self, character_slug: str, raw_value: str, shapes: list[str]) -> None:
        if len(self.representative_examples) >= MAX_EXAMPLES_PER_FIELD:
            return
        if any(example.raw_value == raw_value for example in self.representative_examples):
            return
        self.representative_examples.append(
            Example(
                raw_value=raw_value,
                raw_value_sha256="sha256:" + sha256(raw_value.encode("utf-8")).hexdigest(),
                character_slug=character_slug,
                source_family=self.source_family,
                source_label=self.source_label,
                source_header_path=list(self.source_header_path),
                shape_classes=shapes,
                example_scope="bounded_representative",
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_family": self.source_family,
            "source_role": self.source_role,
            "source_label": self.source_label,
            "source_header_path": list(self.source_header_path),
            "character_count": len(self.character_slugs),
            "row_or_cell_count": self.row_or_cell_count,
            "shape_counts": {shape: int(self.shape_counts.get(shape, 0)) for shape in SHAPE_CLASSES},
            "representative_examples": [
                {
                    **_public_raw_value_payload(example.raw_value),
                    "character_slug": example.character_slug,
                    "source_family": example.source_family,
                    "source_label": example.source_label,
                    "source_header_path": example.source_header_path,
                    "shape_classes": example.shape_classes,
                    "example_scope": example.example_scope,
                }
                for example in self.representative_examples
            ],
        }


def default_report_path() -> Path:
    return repo_root() / REPORT_PATH


def default_summary_json_path() -> Path:
    return repo_root() / SUMMARY_JSON_PATH


def default_summary_md_path() -> Path:
    return repo_root() / SUMMARY_MD_PATH


def build_inventory(
    *,
    run_id: str = RUN_ID,
    report_path: Path | None = None,
    workspace: Path | None = None,
) -> dict[str, Any]:
    report = report_path or default_report_path()
    validate_acquisition_report(report)
    raw_workspace = workspace or default_workspace(run_id)
    if not raw_workspace.exists():
        raise FileNotFoundError(
            "Ignored local source-acquisition artifacts are required for value-shape inventory. "
            "Do not fetch live sources in this unit."
        )
    validate_acquisition_artifacts(report, workspace=raw_workspace)
    acquisition_report = load_acquisition_report(report)

    summaries: dict[tuple[str, tuple[str, ...]], FieldSummary] = {}
    review_items: list[dict[str, Any]] = []

    official_dir = raw_workspace / "official"
    supercombo_dir = raw_workspace / "supercombo"
    for artifact_path in sorted(official_dir.glob("*/official_table_rows.raw.json")):
        _inventory_official_artifact(artifact_path, summaries, review_items)
    for artifact_path in sorted(supercombo_dir.glob("*/supercombo_tables.raw.json")):
        _inventory_supercombo_artifact(artifact_path, summaries, review_items)

    field_summaries = [summary.to_dict() for summary in summaries.values()]
    field_summaries.sort(key=lambda item: (item["source_family"], item["source_header_path"], item["source_label"]))
    review_items = _group_review_items(review_items)
    review_item_summary = _review_item_summary(review_items)
    source_family_summaries = _source_family_summaries(field_summaries, review_items)
    return {
        "artifact_schema_version": SUMMARY_SCHEMA_VERSION,
        "run_id": run_id,
        "acquisition_report": REPORT_PATH.as_posix(),
        "inventory_status": "reviewed_summary",
        "artifact_boundary": "summarized_inventory_only",
        "authority_status": "inventory_only_not_authority",
        "source_families": ["official", "supercombo"],
        "source_family_summaries": source_family_summaries,
        "shape_vocabulary": SHAPE_CLASSES,
        "examples_per_field_limit": MAX_EXAMPLES_PER_FIELD,
        "public_raw_value_max_chars": MAX_PUBLIC_RAW_VALUE_CHARS,
        "field_shape_summaries": field_summaries,
        "review_item_summary": review_item_summary,
        "review_items": review_items,
        "source_boundary": {
            "raw_html_public_commit": "forbidden",
            "full_raw_rows_public_commit": "forbidden",
            "full_source_table_public_commit": "forbidden",
            "local_artifacts_public_commit": "forbidden",
        },
        "authority_boundary": {
            "official": "authority_candidate_only_not_current_fact_authority",
            "supercombo": "enrichment_cross_reference_candidate_only",
            "parsed_values": "not_emitted",
        },
        "input_report_summary": {
            "official_captured_count": acquisition_report.get("official_coverage", {}).get("captured_count"),
            "official_raw_row_count": acquisition_report.get("official_coverage", {}).get("official_raw_row_count"),
            "supercombo_captured_count": acquisition_report.get("supercombo_coverage", {}).get("captured_count"),
            "supercombo_table_count": acquisition_report.get("supercombo_coverage", {}).get("supercombo_table_count"),
        },
    }


def write_inventory_artifacts(
    inventory: dict[str, Any],
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> None:
    output_json = json_path or default_summary_json_path()
    output_md = markdown_path or default_summary_md_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_inventory_markdown(inventory), encoding="utf-8")


def render_inventory_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        "# Latest Source Value-Shape Inventory",
        "",
        "This reviewed summary is inventory-only. It is not numeric authority,",
        "does not emit parsed values, and does not promote official or",
        "SuperCombo data to daily-answer authority.",
        "",
        f"- Run ID: `{inventory['run_id']}`",
        f"- Acquisition report: `{inventory['acquisition_report']}`",
        f"- Artifact boundary: `{inventory['artifact_boundary']}`",
        f"- Authority status: `{inventory['authority_status']}`",
        f"- Examples per field limit: `{inventory['examples_per_field_limit']}`",
        f"- Public raw value character limit: `{inventory['public_raw_value_max_chars']}`",
        "",
        "## Source Family Summary",
        "",
        "| Source family | Field summaries | Observations | Review items | Authority role |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for family in inventory["source_family_summaries"]:
        lines.append(
            f"| `{family['source_family']}` | {family['field_summary_count']} | "
            f"{family['observation_count']} | {family['review_item_count']} | "
            f"`{family['authority_role']}` |"
        )
    lines.extend(["", "## Shape Vocabulary", ""])
    lines.extend(f"- `{shape}`" for shape in inventory["shape_vocabulary"])
    review_summary = inventory.get("review_item_summary", {})
    lines.extend(
        [
            "",
            "## Review Item Summary",
            "",
            f"- Grouped count: `{review_summary.get('grouped_count')}`",
            f"- Emitted count: `{review_summary.get('emitted_count')}`",
            f"- Omitted count: `{review_summary.get('omitted_count')}`",
            f"- Truncated: `{review_summary.get('truncated')}`",
            f"- Blocks JSON Schema redesign: `{review_summary.get('blocker_for_json_schema_redesign')}`",
        ]
    )
    lines.extend(["", "## Field Summaries", ""])
    for summary in inventory["field_shape_summaries"]:
        nonzero_shapes = {
            key: value
            for key, value in summary["shape_counts"].items()
            if value
        }
        examples = "; ".join(
            f"{_markdown_code(_example_display_value(example))} ({', '.join(example['shape_classes'])})"
            for example in summary["representative_examples"][:3]
        )
        if not examples:
            examples = "None"
        lines.extend(
            [
                f"### {summary['source_family']}: {' > '.join(summary['source_header_path'])}",
                "",
                f"- Source role: `{summary['source_role']}`",
                f"- Character count: `{summary['character_count']}`",
                f"- Observations: `{summary['row_or_cell_count']}`",
                f"- Shape counts: `{json.dumps(nonzero_shapes, ensure_ascii=False, sort_keys=True)}`",
                f"- Representative examples: {examples}",
                "",
            ]
        )
    lines.extend(["## Review Items", ""])
    if inventory["review_items"]:
        for item in inventory["review_items"]:
            examples = ", ".join(_markdown_code(_example_display_value(value)) for value in item.get("examples", []))
            lines.append(
                f"- `{item['kind']}` / `{item['source_family']}` / "
                f"`{' > '.join(item['source_header_path'])}`: {item['affected_count']} observations; "
                f"examples: {examples}"
            )
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Boundary Notes",
            "",
            "- Official values remain authority candidates only.",
            "- SuperCombo remains enrichment, cross-reference, or candidate evidence only.",
            "- English canonical keys are deferred to a later normalized schema ExecPlan.",
            "- This artifact intentionally excludes raw HTML, full raw rows, and full source table dumps.",
        ]
    )
    return "\n".join(lines) + "\n"


def validate_inventory_artifacts(
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
) -> list[str]:
    output_json = json_path or default_summary_json_path()
    output_md = markdown_path or default_summary_md_path()
    errors: list[str] = []
    if not output_json.exists():
        errors.append(f"Missing value-shape JSON summary: {output_json.relative_to(repo_root())}")
    if not output_md.exists():
        errors.append(f"Missing value-shape Markdown summary: {output_md.relative_to(repo_root())}")
    if errors:
        return errors
    try:
        inventory = json.loads(output_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid value-shape JSON summary: {exc}"]
    errors.extend(validate_inventory_payload(inventory))
    for path in (output_json, output_md):
        text = path.read_text(encoding="utf-8")
        errors.extend(_forbidden_public_text_errors(text, path))
    if errors:
        raise ValueError("\n".join(errors))
    return []


def validate_inventory_payload(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if inventory.get("artifact_schema_version") != SUMMARY_SCHEMA_VERSION:
        errors.append(f"artifact_schema_version must be {SUMMARY_SCHEMA_VERSION}")
    if inventory.get("run_id") != RUN_ID:
        errors.append(f"run_id must be {RUN_ID}")
    if inventory.get("artifact_boundary") != "summarized_inventory_only":
        errors.append("artifact_boundary must be summarized_inventory_only")
    if inventory.get("authority_status") != "inventory_only_not_authority":
        errors.append("authority_status must be inventory_only_not_authority")
    if inventory.get("public_raw_value_max_chars") != MAX_PUBLIC_RAW_VALUE_CHARS:
        errors.append(f"public_raw_value_max_chars must be {MAX_PUBLIC_RAW_VALUE_CHARS}")
    if sorted(inventory.get("source_families", [])) != ["official", "supercombo"]:
        errors.append("source_families must include official and supercombo")
    if _contains_forbidden_authority_claim(inventory):
        errors.append("inventory must not claim current_fact_authority")
    field_summaries = inventory.get("field_shape_summaries")
    if not isinstance(field_summaries, list) or not field_summaries:
        errors.append("field_shape_summaries must be a non-empty list")
        field_summaries = []
    families_seen = {summary.get("source_family") for summary in field_summaries if isinstance(summary, dict)}
    if not {"official", "supercombo"}.issubset(families_seen):
        errors.append("field_shape_summaries must include official and supercombo")
    for index, summary in enumerate(field_summaries):
        if not isinstance(summary, dict):
            errors.append(f"field_shape_summaries[{index}] must be an object")
            continue
        errors.extend(_field_summary_errors(index, summary))
    review_items = inventory.get("review_items", [])
    if not isinstance(review_items, list):
        errors.append("review_items must be a list")
        review_items = []
    errors.extend(_review_item_summary_errors(inventory.get("review_item_summary"), review_items))
    for index, item in enumerate(review_items):
        if not isinstance(item, dict):
            errors.append(f"review_items[{index}] must be an object")
            continue
        errors.extend(_review_item_errors(index, item))
    return errors


def _inventory_official_artifact(
    artifact_path: Path,
    summaries: dict[tuple[str, tuple[str, ...]], FieldSummary],
    review_items: list[dict[str, Any]],
) -> None:
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    character_slug = str(payload["character_slug"])
    for row in payload.get("rows", []):
        for cell in row.get("cells", []):
            header_path = tuple(str(part) for part in cell.get("source_column_header_path", []))
            if not header_path:
                continue
            raw_value = str(cell.get("source_text_stripped", ""))
            hidden_detail = str(cell.get("hidden_detail_text", ""))
            shapes = classify_value(raw_value, hidden_detail=hidden_detail, source_family="official")
            summary = _summary_for(
                summaries,
                source_family="official",
                source_role="current_fact_authority_candidate",
                source_header_path=header_path,
            )
            summary.add_observation(character_slug, raw_value, shapes)
            _collect_review_items(
                review_items,
                source_family="official",
                source_header_path=list(header_path),
                raw_value=raw_value,
                shapes=shapes,
            )


def _inventory_supercombo_artifact(
    artifact_path: Path,
    summaries: dict[tuple[str, tuple[str, ...]], FieldSummary],
    review_items: list[dict[str, Any]],
) -> None:
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    character_slug = str(payload["character_slug"])
    for table in payload.get("tables", []):
        heading_chain = _heading_chain_values(table.get("heading_chain", {}))
        current_headers: list[str] = []
        for row in table.get("rows", []):
            cells = row.get("cells", [])
            if cells and all(cell.get("tag") == "th" for cell in cells):
                current_headers = [str(cell.get("text_stripped", "")) or f"column_{cell.get('cell_index')}" for cell in cells]
                continue
            for cell in cells:
                if cell.get("tag") != "td":
                    continue
                cell_index = int(cell.get("cell_index", 0))
                header = current_headers[cell_index] if cell_index < len(current_headers) else f"column_{cell_index}"
                source_header_path = tuple(heading_chain + [header])
                raw_value = str(cell.get("text_stripped", ""))
                shapes = classify_value(raw_value, hidden_detail="", source_family="supercombo")
                summary = _summary_for(
                    summaries,
                    source_family="supercombo",
                    source_role="enrichment_candidate",
                    source_header_path=source_header_path,
                )
                summary.add_observation(character_slug, raw_value, shapes)
                _collect_review_items(
                    review_items,
                    source_family="supercombo",
                    source_header_path=list(source_header_path),
                    raw_value=raw_value,
                    shapes=shapes,
                )


def classify_value(raw_value: str, *, hidden_detail: str = "", source_family: str = "official") -> list[str]:
    value = raw_value.strip()
    shapes: list[str] = []
    if hidden_detail.strip():
        shapes.append("hidden_detail")
    if value == "":
        shapes.append("blank")
    if value in {"-", "―", "ー", "—", "–"}:
        shapes.append("dash_variant")
    if re.fullmatch(r"\d+(?:\.\d+)?", value):
        shapes.append("scalar")
    if re.fullmatch(r"[+\-±]\d+(?:\.\d+)?", value):
        shapes.append("signed_frame")
    if re.search(r"\d\s*(?:-|ー|―|–|—|～|~)\s*\d", value):
        shapes.append("range")
    if re.search(r"\d\s*\+\s*\d", value) or re.fullmatch(r"\+\d+(?:\.\d+)?", value):
        shapes.append("plus_expression")
    if value.startswith("※"):
        shapes.append("note_prefixed")
    if value.endswith("※") or re.search(r"\d※$", value):
        shapes.append("note_suffixed")
    if "※" in value and not (value.startswith("※") or value.endswith("※")):
        shapes.append("note_separated_alternate")
    if "," in value and re.search(r"\d", value):
        shapes.append("multihit")
    if re.search(r"時|場合|条件|counter|punish|during|if|on ", value, re.IGNORECASE):
        shapes.append("conditional")
    if "着地" in value:
        shapes.append("landing_expression")
    if "着地まで" in value:
        shapes.append("until_landing")
    if "%" in value or "％" in value:
        shapes.append("percent_expression")
    if _is_categorical(value, source_family=source_family):
        shapes.append("categorical")
    if _is_prose(value):
        shapes.append("prose")
    if _is_raw_only(value):
        shapes.append("raw_only")
    if not shapes:
        shapes.append("unclassified")
    return list(dict.fromkeys(shapes))


def _summary_for(
    summaries: dict[tuple[str, tuple[str, ...]], FieldSummary],
    *,
    source_family: str,
    source_role: str,
    source_header_path: tuple[str, ...],
) -> FieldSummary:
    key = (source_family, source_header_path)
    if key not in summaries:
        summaries[key] = FieldSummary(
            source_family=source_family,
            source_role=source_role,
            source_label=source_header_path[-1] if source_header_path else "",
            source_header_path=source_header_path,
        )
    return summaries[key]


def _heading_chain_values(heading_chain: dict[str, Any]) -> list[str]:
    section_values = []
    fallback_values = []
    for key in sorted(heading_chain, key=_heading_key_sort):
        if key == "h1":
            continue
        if key.startswith("h") and key[1:].isdigit() and int(key[1:]) >= 5:
            continue
        value = str(heading_chain[key]).strip()
        if not value:
            continue
        if key == "h2":
            section_values.append(value)
        else:
            fallback_values.append(value)
    return section_values or fallback_values[:1]


def _heading_key_sort(value: str) -> tuple[str, int, str]:
    if value.startswith("h") and value[1:].isdigit():
        return ("h", int(value[1:]), value)
    return (value[:1], 999, value)


def _is_categorical(value: str, *, source_family: str) -> bool:
    if not value or any(char.isdigit() for char in value):
        return False
    if len(value) > 50:
        return False
    if source_family == "official":
        return bool(re.fullmatch(r"[A-Za-z0-9\s+/・,.\[\]（）()%-]+|[上中下弾投打無SAＣＤ弱中強・、／\s]+", value))
    return bool(re.fullmatch(r"[A-Za-z\s+/.,()\[\]*-]+", value))


def _is_prose(value: str) -> bool:
    if len(value) > 50:
        return True
    return bool(re.search(r"[。]|(?:\s{2,})", value))


def _is_raw_only(value: str) -> bool:
    if not value:
        return False
    return bool(
        "※" in value
        or re.search(r"\d--\d", value)
        or re.search(r"\d+-\d+\.\d+", value)
        or re.search(r"[一-龯ぁ-んァ-ン]", value)
    )


def _collect_review_items(
    review_items: list[dict[str, Any]],
    *,
    source_family: str,
    source_header_path: list[str],
    raw_value: str,
    shapes: list[str],
) -> None:
    kind = None
    if "unclassified" in shapes:
        kind = "unclassified_expression"
    elif re.search(r"\d--\d|\d+-\d+\.\d+", raw_value):
        kind = "malformed_looking_source_value"
    elif "raw_only" in shapes and any(shape in shapes for shape in ["note_prefixed", "note_suffixed", "note_separated_alternate"]):
        kind = "source_specific_expression"
    if kind is None:
        return
    review_items.append(
        {
            "kind": kind,
            "source_family": source_family,
            "source_label": source_header_path[-1] if source_header_path else "",
            "source_header_path": source_header_path,
            "raw_value": raw_value,
            "affected_count": 1,
            "review_question": "Review deterministic classification before schema/parser work.",
        }
    )


def _group_review_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, tuple[str, ...]], dict[str, Any]] = {}
    for item in items:
        key = (item["kind"], item["source_family"], tuple(item["source_header_path"]))
        if key not in grouped:
            grouped[key] = {
                "kind": item["kind"],
                "source_family": item["source_family"],
                "source_label": item["source_label"],
                "source_header_path": item["source_header_path"],
                "affected_count": 0,
                "examples": [],
                "_example_raw_values": set(),
                "review_question": item["review_question"],
            }
        grouped_item = grouped[key]
        grouped_item["affected_count"] += 1
        if (
            len(grouped_item["examples"]) < MAX_REVIEW_ITEM_EXAMPLES
            and item["raw_value"] not in grouped_item["_example_raw_values"]
        ):
            grouped_item["examples"].append(_public_raw_value_payload(item["raw_value"]))
            grouped_item["_example_raw_values"].add(item["raw_value"])
    for grouped_item in grouped.values():
        grouped_item.pop("_example_raw_values", None)
    result = sorted(grouped.values(), key=lambda item: (-item["affected_count"], item["source_family"], item["source_header_path"]))
    return result


def _review_item_summary(review_items: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(review_items)
    return {
        "grouped_count": count,
        "emitted_count": count,
        "omitted_count": 0,
        "truncated": False,
        "blocker_for_json_schema_redesign": False,
    }


def _source_family_summaries(field_summaries: list[dict[str, Any]], review_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for source_family, authority_role in [
        ("official", "authority_candidate_only_not_current_fact_authority"),
        ("supercombo", "enrichment_cross_reference_candidate_only"),
    ]:
        family_fields = [summary for summary in field_summaries if summary.get("source_family") == source_family]
        result.append(
            {
                "source_family": source_family,
                "field_summary_count": len(family_fields),
                "observation_count": sum(int(summary.get("row_or_cell_count", 0)) for summary in family_fields),
                "review_item_count": sum(1 for item in review_items if item.get("source_family") == source_family),
                "authority_role": authority_role,
            }
        )
    return result


def _field_summary_errors(index: int, summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_family = summary.get("source_family")
    if source_family not in {"official", "supercombo"}:
        errors.append(f"field_shape_summaries[{index}].source_family must be official or supercombo")
    expected_role = "current_fact_authority_candidate" if source_family == "official" else "enrichment_candidate"
    if summary.get("source_role") != expected_role:
        errors.append(f"field_shape_summaries[{index}].source_role must be {expected_role}")
    if not isinstance(summary.get("source_header_path"), list) or not summary["source_header_path"]:
        errors.append(f"field_shape_summaries[{index}].source_header_path must be a non-empty list")
    if int(summary.get("row_or_cell_count") or 0) <= 0:
        errors.append(f"field_shape_summaries[{index}].row_or_cell_count must be positive")
    shape_counts = summary.get("shape_counts")
    if not isinstance(shape_counts, dict):
        errors.append(f"field_shape_summaries[{index}].shape_counts must be an object")
    else:
        missing = sorted(set(SHAPE_CLASSES) - set(shape_counts))
        if missing:
            errors.append(f"field_shape_summaries[{index}].shape_counts lacks: {', '.join(missing)}")
    examples = summary.get("representative_examples")
    if not isinstance(examples, list):
        errors.append(f"field_shape_summaries[{index}].representative_examples must be a list")
    elif len(examples) > MAX_EXAMPLES_PER_FIELD:
        errors.append(f"field_shape_summaries[{index}] has too many examples")
    else:
        for example_index, example in enumerate(examples):
            errors.extend(_public_example_errors(f"field_shape_summaries[{index}].representative_examples[{example_index}]", example))
    return errors


def _review_item_summary_errors(summary: Any, review_items: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not isinstance(summary, dict):
        return ["review_item_summary must be an object"]
    expected_count = len(review_items)
    expected = {
        "grouped_count": expected_count,
        "emitted_count": expected_count,
        "omitted_count": 0,
        "truncated": False,
        "blocker_for_json_schema_redesign": False,
    }
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            errors.append(f"review_item_summary.{key} must be {expected_value}")
    return errors


def _review_item_errors(index: int, item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if item.get("source_family") not in {"official", "supercombo"}:
        errors.append(f"review_items[{index}].source_family must be official or supercombo")
    if not isinstance(item.get("source_header_path"), list) or not item["source_header_path"]:
        errors.append(f"review_items[{index}].source_header_path must be a non-empty list")
    if int(item.get("affected_count") or 0) <= 0:
        errors.append(f"review_items[{index}].affected_count must be positive")
    examples = item.get("examples")
    if not isinstance(examples, list):
        errors.append(f"review_items[{index}].examples must be a list")
    elif len(examples) > MAX_REVIEW_ITEM_EXAMPLES:
        errors.append(f"review_items[{index}] has too many examples")
    else:
        for example_index, example in enumerate(examples):
            errors.extend(_public_example_errors(f"review_items[{index}].examples[{example_index}]", example))
    return errors


def _public_raw_value_payload(raw_value: str) -> dict[str, Any]:
    value = str(raw_value)
    payload: dict[str, Any] = {
        "raw_value_sha256": "sha256:" + sha256(value.encode("utf-8")).hexdigest(),
        "raw_value_length": len(value),
        "raw_value_truncated": len(value) > MAX_PUBLIC_RAW_VALUE_CHARS,
    }
    if payload["raw_value_truncated"]:
        payload["raw_value_excerpt"] = value[:MAX_PUBLIC_RAW_VALUE_CHARS] + "..."
    else:
        payload["raw_value"] = value
        payload["raw_value_excerpt"] = value
    return payload


def _public_example_errors(context: str, example: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(example, dict):
        return [f"{context} must be an object"]
    raw_hash = example.get("raw_value_sha256")
    raw_length = example.get("raw_value_length")
    truncated = example.get("raw_value_truncated")
    excerpt = example.get("raw_value_excerpt")
    raw_value_present = "raw_value" in example
    raw_value = example.get("raw_value")
    if not isinstance(raw_hash, str) or not raw_hash.startswith("sha256:"):
        errors.append(f"{context}.raw_value_sha256 must be a sha256 digest")
    if not isinstance(raw_length, int) or raw_length < 0:
        errors.append(f"{context}.raw_value_length must be a non-negative integer")
    if not isinstance(truncated, bool):
        errors.append(f"{context}.raw_value_truncated must be a boolean")
    if not isinstance(excerpt, str):
        errors.append(f"{context}.raw_value_excerpt must be a string")
    elif len(excerpt) > MAX_PUBLIC_RAW_VALUE_CHARS + 3:
        errors.append(f"{context}.raw_value_excerpt is longer than the public limit")
    if truncated is True:
        if raw_value_present:
            errors.append(f"{context} must not expose raw_value when raw_value_truncated is true")
        if isinstance(raw_length, int) and raw_length <= MAX_PUBLIC_RAW_VALUE_CHARS:
            errors.append(f"{context}.raw_value_length must exceed the public limit when truncated")
    elif truncated is False:
        if not isinstance(raw_value, str):
            errors.append(f"{context}.raw_value must be present when raw_value_truncated is false")
        else:
            if len(raw_value) > MAX_PUBLIC_RAW_VALUE_CHARS:
                errors.append(f"{context}.raw_value must not exceed the public limit")
            if isinstance(raw_length, int) and raw_length != len(raw_value):
                errors.append(f"{context}.raw_value_length must match raw_value length")
            expected_hash = "sha256:" + sha256(raw_value.encode("utf-8")).hexdigest()
            if isinstance(raw_hash, str) and raw_hash != expected_hash:
                errors.append(f"{context}.raw_value_sha256 does not match raw_value")
    return errors


def _example_display_value(example: dict[str, Any]) -> str:
    if "raw_value" in example:
        return str(example["raw_value"])
    return str(example.get("raw_value_excerpt", ""))


def _markdown_code(value: str) -> str:
    return "`" + str(value).replace("`", "\\`") + "`"


def _contains_forbidden_authority_claim(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_authority_claim(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_authority_claim(item) for item in value)
    return value == "current_fact_authority"


def _forbidden_public_text_errors(text: str, path: Path) -> list[str]:
    errors: list[str] = []
    if path.is_absolute():
        try:
            relative = path.relative_to(repo_root()).as_posix()
        except ValueError:
            relative = path.name
    else:
        relative = path.as_posix()
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"{relative}: forbidden public inventory content: {match.group(0).strip()}")
            break
    forbidden_literals = [".local/", ".venv/", ".agents/", "/tmp", "page.html", "official_table_rows.raw.json", "supercombo_tables.raw.json"]
    for literal in forbidden_literals:
        if literal in text:
            errors.append(f"{relative}: forbidden public inventory literal: {literal}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="value-shape-inventory")
    subparsers = parser.add_subparsers(required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--run-id", default=RUN_ID)
    build.add_argument("--report", type=Path, default=default_report_path())
    build.add_argument("--workspace", type=Path, default=None)
    build.add_argument("--json-output", type=Path, default=default_summary_json_path())
    build.add_argument("--markdown-output", type=Path, default=default_summary_md_path())
    build.set_defaults(func=_build_command)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--json", type=Path, default=default_summary_json_path())
    validate.add_argument("--markdown", type=Path, default=default_summary_md_path())
    validate.set_defaults(func=_validate_command)
    return parser


def _build_command(args: argparse.Namespace) -> dict[str, Any]:
    inventory = build_inventory(run_id=args.run_id, report_path=args.report, workspace=args.workspace)
    write_inventory_artifacts(inventory, json_path=args.json_output, markdown_path=args.markdown_output)
    validate_inventory_artifacts(json_path=args.json_output, markdown_path=args.markdown_output)
    return {
        "ok": True,
        "run_id": inventory["run_id"],
        "json": str(args.json_output),
        "markdown": str(args.markdown_output),
        "field_summary_count": len(inventory["field_shape_summaries"]),
        "review_item_count": len(inventory["review_items"]),
    }


def _validate_command(args: argparse.Namespace) -> dict[str, Any]:
    validate_inventory_artifacts(json_path=args.json, markdown_path=args.markdown)
    return {"ok": True, "json": str(args.json), "markdown": str(args.markdown)}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
