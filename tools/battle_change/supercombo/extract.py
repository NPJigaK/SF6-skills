#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from collections import OrderedDict
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from tools.battle_change.characters import canonical_character_slug
from tools.battle_change.paths import repo_relative_path

CHANGE_EVENT_FIELDS = [
    "event_id",
    "source_authority",
    "source_family",
    "version",
    "gameversion",
    "date",
    "summary",
    "official_battle_change_id_from_link",
    "supercombo_version_url",
    "section_order",
    "section_title",
    "section_level",
    "scope",
    "fighter_display_name",
    "fighter_key",
    "character_slug",
    "event_order",
    "line_number",
    "target_title",
    "normalized_target_key",
    "change_types",
    "confidence",
    "value_changes",
    "top_line",
    "detail_lines",
    "table_text_blocks",
    "raw_top_line",
    "raw_detail_lines",
    "raw_table_blocks",
    "text_plain",
    "raw_wikitext_path",
]

MOVE_CHANGE_INDEX_FIELDS = [
    "normalized_target_key",
    "scope",
    "fighter_display_name",
    "fighter_key",
    "character_slug",
    "target_title",
    "event_count",
    "numeric_explicit_event_count",
    "versions",
    "official_battle_change_ids_from_links",
    "event_ids",
    "source_authorities",
    "source_families",
    "raw_wikitext_paths",
    "change_types",
]

FIGHTER_KEY_BY_DISPLAY_NAME = {
    "A.K.I.": "aki",
    "Akuma": "gouki",
    "Alex": "alex",
    "Blanka": "blanka",
    "C. Viper": "cviper",
    "Cammy": "cammy",
    "Chun-Li": "chunli",
    "Dee Jay": "deejay",
    "Dhalsim": "dhalsim",
    "E. Honda": "honda",
    "Ed": "ed",
    "Elena": "elena",
    "Guile": "guile",
    "Jamie": "jamie",
    "JP": "jp",
    "Juri": "juri",
    "Ken": "ken",
    "Kimberly": "kimberly",
    "Lily": "lily",
    "Luke": "luke",
    "M. Bison": "vega",
    "Mai": "mai",
    "Manon": "manon",
    "Marisa": "marisa",
    "Rashid": "rashid",
    "Ryu": "ryu",
    "Sagat": "sagat",
    "Terry": "terry",
    "Zangief": "zangief",
}

CHANGE_TYPE_PATTERNS = [
    ("bugfix", [r"\bfixed issue\b", r"\bbug\b", r"\bunintended\b", r"\bcorrected\b"]),
    ("frame_advantage", [r"\badvantage\b", r"\bblockstun\b", r"\bhitstun\b"]),
    ("startup", [r"\bstartup\b", r"\bstart-up\b"]),
    ("active", [r"\bactive frames?\b"]),
    ("recovery", [r"\brecovery\b", r"\btotal (?:animation|frames?)\b"]),
    ("hitbox_hurtbox", [r"\bhitbox\b", r"\bhurtbox\b", r"\bcollision box\b", r"\bproximity guard\b"]),
    ("juggle", [r"\bjuggle\b", r"\bairborne\b", r"\bknockdown\b", r"\bKD\b", r"\bbounce\b", r"\blaunched?\b"]),
    ("combo", [r"\bcombo\b", r"\blink\b", r"\bchain\b", r"\bblockstring\b", r"\bhitconfirm\b", r"\bcancel"]),
    ("damage", [r"\bdamage\b", r"\bscaling\b", r"\bchip\b"]),
    ("drive_gauge", [r"\bdrive (?:gauge|meter|bar|gain|damage|regeneration)\b", r"\bburnout\b"]),
    ("super_gauge", [r"\bsuper (?:gauge|meter|gain)\b", r"\bSA[123]?\b", r"\bsuper art\b"]),
    ("throw", [r"\bthrow\b", r"\bthrow escape\b", r"\bthrow tech\b"]),
    ("input", [r"\binput\b", r"\bbuffer\b", r"\bmodern controls?\b", r"\bnegative edge\b", r"\bcommand\b", r"\bbutton\b"]),
    ("projectile", [r"\bprojectile\b"]),
    ("movement", [r"\bpushback\b", r"\bforward movement\b", r"\brange\b", r"\bwalk\b", r"\bbackdash\b", r"\bshimmy\b"]),
]

VALUE_CHANGE_RE = re.compile(
    r"(?P<context>[^.;\n]{0,64}?)"
    r"(?P<before>[+-]?\d+(?:\.\d+)?(?:x\d+)?(?:,\d+(?:x\d+)?)?)"
    r"\s*(?P<unit_before>f|F|%|％|frames?|Drive bars?|bar|bars?)?"
    r"\s*(?:→|⇒|->|-&gt;)\s*"
    r"(?:[A-Za-z]+\s+)?"
    r"(?P<after>[+-]?\d+(?:\.\d+)?(?:x\d+)?(?:,\d+(?:x\d+)?)?)"
    r"\s*(?P<unit_after>f|F|%|％|frames?|Drive bars?|bar|bars?)?"
)

HEADING_RE = re.compile(r"^(?P<marks>={2,6})\s*(?P<title>.*?)\s*(?P=marks)\s*$")
BULLET_RE = re.compile(r"^(?P<stars>\*+)\s+(?P<body>.*)$")
BATTLE_CHANGE_ID_RE = re.compile(r"/battle_change/([^/?#]+)")

SUPERCOMBO_RAW_ROOT = Path("raw") / "web-pages" / "wiki.supercombo.gg" / "patch-notes"
SUPERCOMBO_OUTPUT_DIR = Path("wiki") / "outputs" / "data" / "battle-change" / "supercombo-patch-notes"
OFFICIAL_VERSIONS_PATH = Path("wiki") / "outputs" / "data" / "battle-change" / "official" / "versions.json"

VERSION_FIELDS = [
    "source",
    "source_authority",
    "version",
    "gameversion",
    "date",
    "summary",
    "summary_html_source_fragment",
    "supercombo_version_page_title",
    "supercombo_version_url",
    "supercombo_version_href",
    "raw_manifest_path",
    "raw_wikitext_path",
    "raw_rendered_dom_path",
    "raw_validation_path",
    "capture_validation_status",
    "mediawiki_revision_id",
    "source_updated_at",
    "captured_at_utc",
    "wikitext_bytes",
    "detail_heading_count",
    "detail_table_count",
    "wikitext_h2_count",
    "wikitext_h3_count",
    "wikitext_bullet_line_count",
    "h2_headings",
    "h3_headings_preview",
    "official_patch_link",
    "official_battle_change_id_from_link",
    "official_battle_change_raw_manifest_path",
    "patch_notes_table_order",
]

CROSSWALK_FIELDS = [
    "supercombo_version",
    "supercombo_gameversion",
    "supercombo_date",
    "supercombo_summary",
    "supercombo_raw_manifest_path",
    "supercombo_source_updated_at",
    "official_battle_change_id",
    "official_battle_change_title",
    "official_battle_change_raw_data_path",
    "official_policy_count",
    "official_common_change_count",
    "official_fighter_change_count",
    "match_status",
    "mapping_basis",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def clean_wikitext_inline(value: str) -> str:
    text = html.unescape(value)
    text = re.sub(r"<!--.*?-->", " ", text)
    text = re.sub(r"<\s*br\s*/?\s*>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[(https?://[^\s\]]+)\s+([^\]]+)\]", r"\2", text)
    text = re.sub(r"\[(https?://[^\s\]]+)\]", r"\1", text)
    text = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]/]+/)*([^\]]+)\]\]", r"\2", text)

    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\{\{([^{}|]+)\|([^{}]+)\}\}", _template_display_text, text)

    text = re.sub(r"\{\{([^{}]+)\}\}", r"\1", text)
    text = text.replace("'''", "").replace("''", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _template_display_text(match: re.Match[str]) -> str:
    parts = [part.strip() for part in match.group(0)[2:-2].split("|")]
    if len(parts) <= 1:
        return parts[0]
    return parts[-1]


def clean_table_block(raw_table: str) -> str:
    cells: list[str] = []
    for raw_line in raw_table.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("{|") or line == "|}" or line.startswith("|-"):
            continue
        line = re.sub(r'^\|\s*style="[^"]*"\s*\|\s*', "| ", line)
        line = re.sub(r"^!", "", line)
        line = re.sub(r"^\|", "", line)
        for cell in re.split(r"\s*(?:!!|\|\|)\s*", line):
            cell = re.sub(r'^(?:style|colspan|rowspan)="[^"]*"\s*\|\s*', "", cell.strip())
            cleaned = clean_wikitext_inline(cell)
            if cleaned:
                cells.append(cleaned)
    return re.sub(r"\s+", " ", " ".join(cells)).strip()


def fighter_key(display_name: str) -> str:
    if not display_name:
        return ""
    if display_name in FIGHTER_KEY_BY_DISPLAY_NAME:
        return FIGHTER_KEY_BY_DISPLAY_NAME[display_name]
    key = display_name.lower().replace(".", "")
    key = re.sub(r"[^a-z0-9]+", "", key)
    return key


def normalize_target(target: str) -> str:
    normalized = target.lower()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip(" :;.,")
    return normalized


def normalized_target_key(scope: str, fighter: str, target_title: str) -> str:
    owner = canonical_character_slug(fighter) if scope == "fighter" and fighter else scope
    return f"{owner}::{normalize_target(target_title)}"


def extract_target_title(top_line: str) -> str:
    text = top_line.strip()
    if ":" in text:
        candidate = text.split(":", 1)[0].strip()
        if 0 < len(candidate) <= 96:
            return candidate
    if "(" in text:
        candidate = text.split("(", 1)[0].strip()
        if 0 < len(candidate) <= 96:
            return candidate.rstrip(" -")

    split_patterns = [
        r"\s+(?:now|is now|are now|can now|no longer|cannot|can no longer)\b",
        r"\s+(?:reduced|increased|decreased|extended|expanded|added|removed|changed|fixed)\b",
        r"\s+(?:builds|causes|leaves|allows|improves|gives|launches|combos|juggles)\b",
        r"\s+(?:startup|active frames?|recovery|hitstun|blockstun|damage|drive damage|super gain)\b",
    ]
    for pattern in split_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match and match.start() > 0:
            candidate = text[: match.start()].strip()
            if candidate:
                return candidate.rstrip(" -")
    return text[:160].strip()


def scope_for(section_title: str, fighter_display_name: str) -> str:
    title = section_title.lower()
    if fighter_display_name:
        return "fighter"
    if "patch" in title and "universal" not in title:
        return "release"
    return "system"


def classify_change_types(text: str) -> list[str]:
    lowered = text.lower()
    change_types: list[str] = []
    for change_type, patterns in CHANGE_TYPE_PATTERNS:
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns):
            change_types.append(change_type)
    if not change_types:
        change_types.append("textual_change")
    return change_types


def extract_value_changes(text: str) -> list[dict[str, str]]:
    values: list[dict[str, str]] = []
    for match in VALUE_CHANGE_RE.finditer(text):
        context = re.sub(r"\s+", " ", match.group("context")).strip(" ,;:-")
        unit = match.group("unit_after") or match.group("unit_before") or ""
        values.append(
            {
                "before": match.group("before"),
                "after": match.group("after"),
                "unit": unit,
                "context": context,
            }
        )
    return values


def confidence_for_event(value_changes: list[dict[str, str]], change_types: list[str]) -> str:
    if value_changes:
        return "numeric_explicit"
    if change_types != ["textual_change"]:
        return "textual_direct"
    return "textual_unclassified"


def build_change_events(version: dict[str, Any], wikitext: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    current_h2 = ""
    current_h2_order = 0
    current_h2_level = 0
    current_fighter = ""
    current_event: dict[str, Any] | None = None
    table_lines: list[str] | None = None

    def finish_event() -> None:
        nonlocal current_event
        if current_event is None:
            return
        text_parts = [current_event["top_line"], *current_event["detail_lines"], *current_event["table_text_blocks"]]
        text_plain = " ".join(part for part in text_parts if part)
        value_changes: list[dict[str, str]] = []
        for part in text_parts:
            value_changes.extend(extract_value_changes(part))
        change_types = classify_change_types(text_plain)
        current_event["text_plain"] = text_plain
        current_event["value_changes"] = value_changes
        current_event["change_types"] = change_types
        current_event["confidence"] = confidence_for_event(value_changes, change_types)
        events.append(current_event)
        current_event = None

    def attach_table() -> None:
        nonlocal table_lines
        if table_lines is None:
            return
        raw_table = "\n".join(table_lines)
        if current_event is not None:
            current_event["raw_table_blocks"].append(raw_table)
            table_text = clean_table_block(raw_table)
            if table_text:
                current_event["table_text_blocks"].append(table_text)
        table_lines = None

    for line_number, raw_line in enumerate(wikitext.splitlines(), start=1):
        line = raw_line.rstrip()
        stripped = line.strip()

        if table_lines is not None:
            table_lines.append(line)
            if stripped == "|}":
                attach_table()
            continue
        if stripped.startswith("{|"):
            table_lines = [line]
            if stripped == "|}":
                attach_table()
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            attach_table()
            finish_event()
            level = len(heading_match.group("marks"))
            title = clean_wikitext_inline(heading_match.group("title"))
            if level == 2:
                current_h2_order += 1
                current_h2 = title
                current_h2_level = level
                current_fighter = ""
            elif level == 3:
                current_fighter = title
            continue

        bullet_match = BULLET_RE.match(stripped)
        if not bullet_match:
            continue

        depth = len(bullet_match.group("stars"))
        raw_body = bullet_match.group("body").strip()
        body = clean_wikitext_inline(raw_body)
        if depth == 1:
            attach_table()
            finish_event()
            event_order = len(events) + 1
            scope = scope_for(current_h2, current_fighter)
            key = fighter_key(current_fighter)
            character_slug = canonical_character_slug(key) if scope == "fighter" else ""
            target_title = extract_target_title(body)
            current_event = {
                "event_id": f"supercombo-patch-notes:{version['version']}:{event_order}",
                "source_authority": "community",
                "source_family": "supercombo-patch-notes",
                "version": str(version.get("version", "")),
                "gameversion": str(version.get("gameversion", "")),
                "date": str(version.get("date", "")),
                "summary": str(version.get("summary", "")),
                "official_battle_change_id_from_link": str(version.get("official_battle_change_id_from_link") or ""),
                "supercombo_version_url": str(version.get("supercombo_version_url", "")),
                "section_order": str(current_h2_order),
                "section_title": current_h2,
                "section_level": str(current_h2_level),
                "scope": scope,
                "fighter_display_name": current_fighter if scope == "fighter" else "",
                "fighter_key": key if scope == "fighter" else "",
                "character_slug": character_slug,
                "event_order": str(event_order),
                "line_number": str(line_number),
                "target_title": target_title,
                "normalized_target_key": normalized_target_key(scope, key, target_title),
                "change_types": [],
                "confidence": "",
                "value_changes": [],
                "top_line": body,
                "detail_lines": [],
                "table_text_blocks": [],
                "raw_top_line": raw_body,
                "raw_detail_lines": [],
                "raw_table_blocks": [],
                "text_plain": "",
                "raw_wikitext_path": str(version.get("raw_wikitext_path", "")),
            }
        elif current_event is not None:
            current_event["detail_lines"].append(body)
            current_event["raw_detail_lines"].append(raw_body)

    attach_table()
    finish_event()
    return events


def build_move_change_index(events: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for event in events:
        key = event["normalized_target_key"]
        if key not in grouped:
            grouped[key] = {
                "normalized_target_key": key,
                "scope": event["scope"],
                "fighter_display_name": event["fighter_display_name"],
                "fighter_key": event["fighter_key"],
                "character_slug": event["character_slug"],
                "target_title": event["target_title"],
                "event_count": 0,
                "numeric_explicit_event_count": 0,
                "versions": [],
                "official_battle_change_ids_from_links": [],
                "event_ids": [],
                "source_authorities": [],
                "source_families": [],
                "raw_wikitext_paths": [],
                "change_types": [],
            }
        item = grouped[key]
        item["event_count"] += 1
        if event["confidence"] == "numeric_explicit":
            item["numeric_explicit_event_count"] += 1
        for field, value in [
            ("versions", event["version"]),
            ("official_battle_change_ids_from_links", event["official_battle_change_id_from_link"]),
            ("event_ids", event["event_id"]),
            ("source_authorities", event["source_authority"]),
            ("source_families", event["source_family"]),
            ("raw_wikitext_paths", event["raw_wikitext_path"]),
        ]:
            if value and value not in item[field]:
                item[field].append(value)
        item["change_types"] = sorted(set(item["change_types"]) | set(event["change_types"]))

    rows = list(grouped.values())
    return {
        "schema_version": "supercombo_patch_notes_move_change_index/v1",
        "source_manifest": "raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json",
        "source_events": "wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json",
        "fields": MOVE_CHANGE_INDEX_FIELDS,
        "row_count": len(rows),
        "rows": rows,
    }


def extract_first_href(html_fragment: str) -> str:
    match = re.search(r"""href\s*=\s*(['"])(?P<href>.*?)\1""", html_fragment, flags=re.IGNORECASE)
    if not match:
        return ""
    return html.unescape(match.group("href"))


def official_battle_change_id_from_url(url: str) -> str | None:
    match = BATTLE_CHANGE_ID_RE.search(url)
    if not match:
        return None
    return match.group(1)


def version_slug(version: str) -> str:
    return version.replace(".", "-")


def rel_posix(path: Path) -> str:
    return path.as_posix()


def read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return {}
    return read_json(path)


def generated_at_for_run(repo_root: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    captures_path = repo_root / SUPERCOMBO_RAW_ROOT / "version-captures.json"
    existing = read_json_if_exists(captures_path)
    if existing.get("created_at_utc"):
        return str(existing["created_at_utc"])
    manifest = read_json_if_exists(repo_root / SUPERCOMBO_RAW_ROOT / "manifest.json")
    if manifest.get("captured_at_utc"):
        return str(manifest["captured_at_utc"])
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def heading_summary(wikitext: str) -> dict[str, Any]:
    h2_headings: list[str] = []
    h3_headings: list[str] = []
    bullet_count = 0
    for raw_line in wikitext.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("*"):
            bullet_count += 1
        match = HEADING_RE.match(stripped)
        if not match:
            continue
        level = len(match.group("marks"))
        title = clean_wikitext_inline(match.group("title"))
        if level == 2:
            h2_headings.append(title)
        elif level == 3:
            h3_headings.append(title)
    return {
        "wikitext_h2_count": len(h2_headings),
        "wikitext_h3_count": len(h3_headings),
        "wikitext_bullet_line_count": bullet_count,
        "h2_headings": h2_headings,
        "h3_headings_preview": h3_headings[:20],
    }


def patch_notes_table_rows(dom_payload: dict[str, Any]) -> list[dict[str, Any]]:
    tables = dom_payload.get("tables", [])
    if not tables:
        return []
    rows = tables[0].get("rows", [])
    data_rows: list[dict[str, Any]] = []
    for row in rows:
        cells = row.get("cells", [])
        if len(cells) < 5:
            continue
        first_text = str(cells[0].get("text", "")).strip().lower()
        if first_text == "version":
            continue
        data_rows.append(row)
    return data_rows


def cell_text(cells: list[dict[str, Any]], index: int) -> str:
    return str(cells[index].get("text", "")).strip()


def cell_html(cells: list[dict[str, Any]], index: int) -> str:
    return str(cells[index].get("html", "")).strip()


def official_versions_by_id(repo_root: Path) -> dict[str, dict[str, Any]]:
    payload = read_json_if_exists(repo_root / OFFICIAL_VERSIONS_PATH)
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        return {}
    return {str(row.get("version_id", "")): row for row in rows if row.get("version_id")}


def build_version_row(
    repo_root: Path,
    *,
    patch_notes_table_order: int,
    cells: list[dict[str, Any]],
    official_versions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    version = cell_text(cells, 0)
    slug = version_slug(version)
    detail_root_rel = SUPERCOMBO_RAW_ROOT / "versions" / slug
    detail_root = repo_root / detail_root_rel
    manifest_path_rel = detail_root_rel / "manifest.json"
    wikitext_path_rel = detail_root_rel / "page.raw.wikitext"
    dom_path_rel = detail_root_rel / "rendered" / "main.dom.json"
    validation_path_rel = detail_root_rel / "validation.json"

    manifest = read_json_if_exists(repo_root / manifest_path_rel)
    validation = read_json_if_exists(repo_root / validation_path_rel)
    validation_summary = validation.get("summary", {}) if isinstance(validation.get("summary"), dict) else {}
    wikitext_path = repo_root / wikitext_path_rel
    wikitext = wikitext_path.read_text(encoding="utf-8") if wikitext_path.exists() else ""
    headings = heading_summary(wikitext)

    version_href = extract_first_href(cell_html(cells, 0))
    version_url = urljoin("https://wiki.supercombo.gg", version_href) if version_href else ""
    official_patch_link = extract_first_href(cell_html(cells, 4)) or None
    official_id = official_battle_change_id_from_url(official_patch_link or "")
    official_metadata_path = (
        rel_posix(Path("raw") / "battle-change" / "official" / "versions" / official_id / "metadata.json")
        if official_id and official_id in official_versions
        else None
    )

    source_revision = manifest.get("source_revision", {}) if isinstance(manifest.get("source_revision"), dict) else {}
    mediawiki_revision_id = source_revision.get("revision_id") or validation_summary.get("mediawiki_revision_id")
    source_updated_at = manifest.get("source_updated_at") or source_revision.get("revision_timestamp") or ""
    captured_at_utc = manifest.get("captured_at_utc") or ""
    wikitext_bytes = wikitext_path.stat().st_size if wikitext_path.exists() else int(validation_summary.get("wikitext_bytes", 0) or 0)

    return {
        "source": "SuperCombo Wiki",
        "source_authority": "community",
        "version": version,
        "gameversion": cell_text(cells, 1),
        "date": cell_text(cells, 2),
        "summary": cell_text(cells, 3),
        "summary_html_source_fragment": cell_html(cells, 3),
        "supercombo_version_page_title": str(manifest.get("page_title") or f"Street Fighter 6/Version/{version}"),
        "supercombo_version_url": str(manifest.get("source_url") or version_url),
        "supercombo_version_href": version_href,
        "raw_manifest_path": rel_posix(manifest_path_rel),
        "raw_wikitext_path": rel_posix(wikitext_path_rel),
        "raw_rendered_dom_path": rel_posix(dom_path_rel),
        "raw_validation_path": rel_posix(validation_path_rel),
        "capture_validation_status": str(validation.get("status", "")),
        "mediawiki_revision_id": mediawiki_revision_id,
        "source_updated_at": str(source_updated_at),
        "captured_at_utc": str(captured_at_utc),
        "wikitext_bytes": wikitext_bytes,
        "detail_heading_count": int(validation_summary.get("heading_count", 0) or 0),
        "detail_table_count": int(validation_summary.get("table_count", 0) or 0),
        **headings,
        "official_patch_link": official_patch_link,
        "official_battle_change_id_from_link": official_id,
        "official_battle_change_raw_manifest_path": official_metadata_path,
        "patch_notes_table_order": patch_notes_table_order,
    }


def build_versions_output(repo_root: Path, generated_at_utc: str) -> dict[str, Any]:
    dom_payload = read_json(repo_root / SUPERCOMBO_RAW_ROOT / "rendered" / "main.dom.json")
    official_versions = official_versions_by_id(repo_root)
    rows = [
        build_version_row(
            repo_root,
            patch_notes_table_order=order,
            cells=row["cells"],
            official_versions=official_versions,
        )
        for order, row in enumerate(patch_notes_table_rows(dom_payload), start=1)
    ]
    return {
        "schema_version": "supercombo_patch_notes_versions/v1",
        "source_manifest": rel_posix(SUPERCOMBO_RAW_ROOT / "manifest.json"),
        "source_table_artifact": rel_posix(SUPERCOMBO_RAW_ROOT / "rendered" / "main.dom.json"),
        "generated_at_utc": generated_at_utc,
        "fields": VERSION_FIELDS,
        "row_count": len(rows),
        "rows": rows,
    }


def build_crosswalk_output(repo_root: Path, versions_output: dict[str, Any], generated_at_utc: str) -> dict[str, Any]:
    official_versions = official_versions_by_id(repo_root)
    linked_official_ids = {
        str(row.get("official_battle_change_id_from_link"))
        for row in versions_output["rows"]
        if row.get("official_battle_change_id_from_link")
    }
    rows: list[dict[str, Any]] = []
    for version in versions_output["rows"]:
        official_id = version.get("official_battle_change_id_from_link")
        official = official_versions.get(str(official_id), {}) if official_id else {}
        if official_id and official:
            match_status = "matched_official_battle_change"
            mapping_basis = "SuperCombo Patch Notes external Patch Notes link"
        elif official_id:
            match_status = "official_battle_change_link_without_local_official_capture"
            mapping_basis = "SuperCombo Patch Notes external Patch Notes link"
        else:
            match_status = "supercombo_no_official_battle_change_link"
            mapping_basis = "No external battle_change link in SuperCombo Patch Notes table"
        rows.append(
            {
                "supercombo_version": version["version"],
                "supercombo_gameversion": version["gameversion"],
                "supercombo_date": version["date"],
                "supercombo_summary": version["summary"],
                "supercombo_raw_manifest_path": version["raw_manifest_path"],
                "supercombo_source_updated_at": version["source_updated_at"],
                "official_battle_change_id": official_id,
                "official_battle_change_title": official.get("version_title"),
                "official_battle_change_raw_data_path": official.get("data_json_path"),
                "official_policy_count": official.get("policy_count"),
                "official_common_change_count": official.get("common_change_count"),
                "official_fighter_change_count": official.get("fighter_change_count"),
                "match_status": match_status,
                "mapping_basis": mapping_basis,
            }
        )

    official_unmatched_ids = sorted(set(official_versions) - linked_official_ids)
    summary = {
        "supercombo_row_count": len(versions_output["rows"]),
        "matched_count": sum(1 for row in rows if row["match_status"] == "matched_official_battle_change"),
        "supercombo_no_official_link_count": sum(
            1 for row in rows if row["match_status"] == "supercombo_no_official_battle_change_link"
        ),
        "official_unmatched_count": len(official_unmatched_ids),
    }
    return {
        "schema_version": "supercombo_patch_notes_official_battle_change_crosswalk/v1",
        "source_versions": rel_posix(SUPERCOMBO_OUTPUT_DIR / "versions.json"),
        "official_versions": rel_posix(OFFICIAL_VERSIONS_PATH),
        "generated_at_utc": generated_at_utc,
        "fields": CROSSWALK_FIELDS,
        "row_count": len(rows),
        "summary": summary,
        "official_unmatched_ids": official_unmatched_ids,
        "rows": rows,
    }


def build_version_captures_output(repo_root: Path, versions_output: dict[str, Any], generated_at_utc: str) -> dict[str, Any]:
    manifest = read_json_if_exists(repo_root / SUPERCOMBO_RAW_ROOT / "manifest.json")
    detail_pages: list[dict[str, Any]] = []
    for version in versions_output["rows"]:
        revision_id = version.get("mediawiki_revision_id")
        detail_pages.append(
            {
                "version": version["version"],
                "page_title": version["supercombo_version_page_title"],
                "source_url": version["supercombo_version_url"],
                "raw_root": str(Path(version["raw_manifest_path"]).parent).replace("\\", "/"),
                "manifest": version["raw_manifest_path"],
                "page_raw_wikitext": version["raw_wikitext_path"],
                "rendered_main_dom": version["raw_rendered_dom_path"],
                "validation": version["raw_validation_path"],
                "validation_status": version["capture_validation_status"],
                "source_revision_id": revision_id,
                "source_updated_at": version["source_updated_at"],
                "captured_at_utc": version["captured_at_utc"],
                "wikitext_bytes": version["wikitext_bytes"],
                "wikitext_bullet_line_count": version["wikitext_bullet_line_count"],
                "official_battle_change_id_from_link": version["official_battle_change_id_from_link"],
            }
        )
    return {
        "schema_version": "supercombo_patch_notes_version_captures/v1",
        "created_at_utc": generated_at_utc,
        "platform": "MediaWiki",
        "publisher": "SuperCombo Wiki",
        "source_url": str(manifest.get("source_url") or "https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes"),
        "storage_policy": str(manifest.get("storage_policy") or "updateable_web_page_capture"),
        "parent_manifest": rel_posix(SUPERCOMBO_RAW_ROOT / "manifest.json"),
        "version_capture_root": rel_posix(SUPERCOMBO_RAW_ROOT / "versions"),
        "version_count": len(detail_pages),
        "detail_pages": detail_pages,
    }


def build_batch_validation_output(
    repo_root: Path,
    versions_output: dict[str, Any],
    crosswalk_output: dict[str, Any],
    generated_at_utc: str,
) -> dict[str, Any]:
    parent_validation = read_json_if_exists(repo_root / SUPERCOMBO_RAW_ROOT / "validation.json")
    parent_validation_status = str(parent_validation.get("status", ""))
    rows = versions_output["rows"]
    validation_statuses = [row.get("capture_validation_status") for row in rows]
    largest = max(rows, key=lambda row: int(row.get("wikitext_bytes") or 0), default={})
    summary = {
        "patch_notes_table_version_rows": len(rows),
        "captured_version_detail_pages": sum(1 for row in rows if (repo_root / row["raw_manifest_path"]).exists()),
        "version_detail_validations_passed": sum(1 for status in validation_statuses if status == "passed"),
        "official_battle_change_matched_rows": crosswalk_output["summary"]["matched_count"],
        "supercombo_rows_without_official_battle_change_link": crosswalk_output["summary"][
            "supercombo_no_official_link_count"
        ],
        "official_battle_change_rows_without_supercombo_link": crosswalk_output["summary"]["official_unmatched_count"],
        "largest_wikitext_version": largest.get("version"),
        "largest_wikitext_bytes": largest.get("wikitext_bytes", 0),
    }
    checks = {
        "patch_notes_page_validation_passed": parent_validation_status in ("", "passed"),
        "patch_notes_table_has_version_rows": len(rows) > 0,
        "all_version_detail_pages_captured": summary["captured_version_detail_pages"] == len(rows),
        "all_version_detail_validations_passed": summary["version_detail_validations_passed"] == len(rows),
        "all_version_rows_have_raw_wikitext": all(
            repo_relative_path(repo_root, row["raw_wikitext_path"]).exists() for row in rows
        ),
        "official_crosswalk_counts_are_consistent": (
            crosswalk_output["summary"]["matched_count"]
            + crosswalk_output["summary"]["supercombo_no_official_link_count"]
            <= len(rows)
        ),
    }
    return {
        "validation_schema_version": "supercombo_patch_notes_batch_validation/v1",
        "created_at_utc": generated_at_utc,
        "status": "passed" if all(checks.values()) else "failed",
        "summary": summary,
        "checks": checks,
        "notes": [
            "Patch Notes page wikitext contains a Cargo query; the rendered table is preserved in rendered/main.dom.json and compiled into wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json.",
            "Each version detail page has an independent raw web-page capture under versions/<version-slug>/.",
            "Images were not downloaded for this patch-notes batch because no content media were requested or resolved; page text and rendered DOM are the canonical detail evidence.",
        ],
    }


def build_upstream_outputs(repo_root: Path, generated_at_utc: str | None = None) -> dict[str, Any]:
    generated_at = generated_at_for_run(repo_root, generated_at_utc)
    versions = build_versions_output(repo_root, generated_at)
    crosswalk = build_crosswalk_output(repo_root, versions, generated_at)
    version_captures = build_version_captures_output(repo_root, versions, generated_at)
    batch_validation = build_batch_validation_output(repo_root, versions, crosswalk, generated_at)
    return {
        "versions": versions,
        "official_battle_change_crosswalk": crosswalk,
        "version_captures": version_captures,
        "batch_validation": batch_validation,
    }


def sha256_file(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"sha256": f"sha256:{digest}", "bytes": path.stat().st_size}


def update_parent_manifest(repo_root: Path) -> None:
    manifest_path = repo_root / SUPERCOMBO_RAW_ROOT / "manifest.json"
    if not manifest_path.exists():
        return
    manifest = read_json(manifest_path)
    for field, value in [
        ("detail_page_capture_artifact", "version-captures.json"),
        ("detail_page_capture_root", rel_posix(SUPERCOMBO_RAW_ROOT / "versions")),
        ("batch_validation", "validation.batch.json"),
    ]:
        manifest[field] = value
    manifest["canonical_source_artifacts"] = [
        "page.raw.wikitext",
        "imageinfo.json",
        "images/manifest.json",
        "version-captures.json",
    ]
    manifest["derived_outputs"] = [
        rel_posix(SUPERCOMBO_OUTPUT_DIR / "versions.json"),
        rel_posix(SUPERCOMBO_OUTPUT_DIR / "official-battle-change-crosswalk.json"),
        rel_posix(SUPERCOMBO_OUTPUT_DIR / "change-events.json"),
        rel_posix(SUPERCOMBO_OUTPUT_DIR / "move-change-index.json"),
        rel_posix(SUPERCOMBO_OUTPUT_DIR / "schema.json"),
    ]
    captures = read_json_if_exists(repo_root / SUPERCOMBO_RAW_ROOT / "version-captures.json")
    detail_pages = captures.get("detail_pages", []) if isinstance(captures.get("detail_pages"), list) else []
    manifest["detail_page_count"] = len(detail_pages)
    manifest["detail_page_validation_status"] = (
        "passed" if detail_pages and all(page.get("validation_status") == "passed" for page in detail_pages) else "failed"
    )
    hashes = manifest.setdefault("artifact_hashes", {})
    for rel_path in ["version-captures.json", "validation.batch.json"]:
        artifact_path = repo_root / SUPERCOMBO_RAW_ROOT / rel_path
        if artifact_path.exists():
            hashes[rel_path] = sha256_file(artifact_path)
    write_json(manifest_path, manifest)


def write_upstream_outputs(repo_root: Path, generated_at_utc: str | None = None) -> dict[str, Any]:
    outputs = build_upstream_outputs(repo_root, generated_at_utc=generated_at_utc)
    output_dir = repo_root / SUPERCOMBO_OUTPUT_DIR
    raw_root = repo_root / SUPERCOMBO_RAW_ROOT
    write_json(output_dir / "versions.json", outputs["versions"])
    write_json(output_dir / "official-battle-change-crosswalk.json", outputs["official_battle_change_crosswalk"])
    write_json(raw_root / "version-captures.json", outputs["version_captures"])
    write_json(raw_root / "validation.batch.json", outputs["batch_validation"])
    update_parent_manifest(repo_root)
    return outputs


def extract_all(repo_root: Path) -> dict[str, Any]:
    output_dir = repo_root / SUPERCOMBO_OUTPUT_DIR
    raw_root = repo_root / SUPERCOMBO_RAW_ROOT
    upstream_outputs = build_upstream_outputs(repo_root)
    versions_payload = upstream_outputs["versions"]
    events: list[dict[str, Any]] = []

    for version in versions_payload["rows"]:
        raw_wikitext_path = repo_relative_path(repo_root, version["raw_wikitext_path"])
        wikitext = raw_wikitext_path.read_text(encoding="utf-8")
        events.extend(build_change_events(version, wikitext))

    move_change_index = build_move_change_index(events)
    schema_path = output_dir / "schema.json"
    schema = read_json(schema_path)
    schema.setdefault("outputs", {})
    schema["outputs"]["change_events_json"] = {
        "path": "wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json",
        "description": "Top-level SuperCombo Patch Notes bullets with nested detail bullets and table text preserved as community change events.",
        "row_key": "event_id",
        "source_authority": "community",
    }
    schema["outputs"]["move_change_index_json"] = {
        "path": "wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json",
        "description": "Community change events grouped by fighter/system scope and target title for cause-finding queries.",
        "row_key": "normalized_target_key",
        "source_authority": "community",
    }
    schema["change_event_fields"] = CHANGE_EVENT_FIELDS
    schema["move_change_index_fields"] = MOVE_CHANGE_INDEX_FIELDS
    schema["authority_policy"] = (
        "Capcom official battle_change remains official source for official update text. "
        "SuperCombo change-events and move-change-index are community source indexes that preserve "
        "SuperCombo wording, explanatory notes, and explicit links to official Battle Change IDs when present."
    )

    change_events_output = {
        "schema_version": "supercombo_patch_notes_change_events/v1",
        "source_manifest": "raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json",
        "source_versions": "wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json",
        "fields": CHANGE_EVENT_FIELDS,
        "row_count": len(events),
        "rows": events,
    }

    write_json(output_dir / "versions.json", upstream_outputs["versions"])
    write_json(output_dir / "official-battle-change-crosswalk.json", upstream_outputs["official_battle_change_crosswalk"])
    write_json(raw_root / "version-captures.json", upstream_outputs["version_captures"])
    write_json(raw_root / "validation.batch.json", upstream_outputs["batch_validation"])
    write_json(
        output_dir / "change-events.json",
        change_events_output,
    )
    write_json(output_dir / "move-change-index.json", move_change_index)
    write_json(schema_path, schema)
    update_parent_manifest(repo_root)

    return {
        "output_dir": output_dir.relative_to(repo_root).as_posix(),
        "version_count": len(versions_payload["rows"]),
        "change_event_count": len(events),
        "move_change_index_count": move_change_index["row_count"],
        "numeric_explicit_event_count": sum(1 for event in events if event["confidence"] == "numeric_explicit"),
        "table_attached_event_count": sum(1 for event in events if event["raw_table_blocks"]),
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
