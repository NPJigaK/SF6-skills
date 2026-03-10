from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


NULLISH_VALUES = {"", "-", "D", "d", "N/A", "?", "※", "※1", "※2"}
GROUP_ALIASES = {
    "通常技": "normals",
    "特殊技": "command_normals",
    "ターゲットコンボ": "target_combos",
    "通常投げ": "throws",
    "投げ": "throws",
    "共通システム": "system",
    "必殺技": "specials",
    "スーパーアーツ": "super_arts",
    "Taunts": "taunts",
    "Normals": "normals",
    "Command Normals": "command_normals",
    "Target Combos": "target_combos",
    "Throws": "throws",
    "Drive Moves": "system",
    "Special Moves": "specials",
    "Super Arts": "super_arts",
}
ICON_TOKEN_MAP = {
    "icon_punch_l.png": "LP",
    "icon_punch_m.png": "MP",
    "icon_punch_h.png": "HP",
    "icon_punch.png": "P",
    "icon_kick_l.png": "LK",
    "icon_kick_m.png": "MK",
    "icon_kick_h.png": "HK",
    "icon_kick.png": "K",
    "key-nutral.png": "5",
    "key-neutral.png": "5",
    "key-u.png": "8",
    "key-ur.png": "9",
    "key-r.png": "6",
    "key-dr.png": "3",
    "key-d.png": "2",
    "key-dl.png": "1",
    "key-l.png": "4",
    "key-ul.png": "7",
    "key-plus.png": "+",
    "key-or.png": "|",
    "arrow_3.png": ">",
    "modern_m.png": "M",
}
DIRECTION_TOKENS = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
BUTTON_TOKENS = {"LP", "MP", "HP", "P", "LK", "MK", "HK", "K", "LPLK", "MPMK", "HPHK"}
CONFIDENCE_ORDER = {"high": 3, "medium": 2, "low": 1}
INPUT_TOKEN_ORDER = ("LPLK", "MPMK", "HPHK", "LP", "MP", "HP", "LK", "MK", "HK", "P", "K", ">", "|", "+")


@dataclass(frozen=True)
class ActiveParseResult:
    kind: str | None
    start: int | None
    end: int | None
    frames: int | None
    ambiguous: bool = False


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def timestamp_token(utc_iso: str | None = None) -> str:
    value = utc_iso or utc_now()
    return value.replace("-", "").replace(":", "").replace(".", "")


def unique_run_token() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def stable_json_dumps(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def compact_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", value).strip()
    return text or None


def join_nonempty(values: list[str | None]) -> str | None:
    filtered = [value for value in (compact_text(item) for item in values) if value]
    if not filtered:
        return None
    return " | ".join(filtered)


def slugify(value: str | None) -> str:
    if not value:
        return "unknown"
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    normalized = normalized.replace(".", "_")
    normalized = re.sub(r"[^\w]+", "_", normalized, flags=re.UNICODE)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "unknown"


def normalize_name_key(value: str | None) -> str | None:
    text = compact_text(value)
    if not text:
        return None
    return slugify(text)


def build_official_source_row_id(snapshot_id: str, section: str | None, row_index: int, label: str | None) -> str:
    section_token = slugify(section)[:24]
    label_token = slugify(label)[:48]
    return f"{snapshot_id}:{section_token}:{row_index:03d}:{label_token}"


def build_supercombo_source_row_id(snapshot_id: str, table_index: int, raw_source_token: str | None) -> str:
    return f"{snapshot_id}:t{table_index:03d}:{(raw_source_token or 'unknown')}"


def lower_confidence(current: str, requested: str) -> str:
    if CONFIDENCE_ORDER[requested] < CONFIDENCE_ORDER[current]:
        return requested
    return current


def mark_manual_review(record: dict[str, Any], reason: str, confidence: str = "low") -> None:
    record["manual_review_needed"] = True
    reasons = record.setdefault("review_reasons", [])
    if reason not in reasons:
        reasons.append(reason)
    record["extraction_confidence"] = lower_confidence(record.get("extraction_confidence", "high"), confidence)


def canonical_group(value: str | None) -> str:
    text = compact_text(value) or "unknown"
    for key, mapped in GROUP_ALIASES.items():
        if key in text:
            return mapped
    return slugify(text)


def basename(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def tokenize_input_string(value: str | None) -> list[str]:
    text = compact_text(value)
    if not text:
        return []
    compact = text.replace(" ", "")
    tokens: list[str] = []
    index = 0
    while index < len(compact):
        if compact[index : index + 2].lower() == "j.":
            tokens.append("j.")
            index += 2
            continue
        matched = False
        for token in INPUT_TOKEN_ORDER:
            if compact.startswith(token, index):
                tokens.append(token)
                index += len(token)
                matched = True
                break
        if matched:
            continue
        if compact[index] in DIRECTION_TOKENS:
            tokens.append(compact[index])
            index += 1
            continue
        tokens.append(compact[index])
        index += 1
    return tokens


def normalize_supercombo_input(value: str | None) -> str | None:
    text = compact_text(value)
    if text is None:
        return None
    text = text.replace(" ", "")
    if text.lower().startswith("j."):
        return "j." + text[2:].upper()
    return re.sub(r"[a-z]+", lambda match: match.group(0).upper(), text, flags=re.IGNORECASE)


def infer_official_prefix(move_name: str | None) -> str | None:
    if not move_name:
        return None
    lowered = move_name.lower()
    if "立ち" in move_name or "stand" in lowered:
        return "5"
    if "しゃがみ" in move_name or "crouch" in lowered:
        return "2"
    if "ジャンプ" in move_name or "jump" in lowered:
        return "j."
    return None


def collapse_button_tokens(buttons: list[str]) -> str:
    joined = "".join(buttons)
    if joined in {"LPLK", "MPMK", "HPHK"}:
        return joined
    if len(buttons) >= 2 and all(button.endswith("P") for button in buttons):
        return "PP"
    if len(buttons) >= 2 and all(button.endswith("K") for button in buttons):
        return "KK"
    return joined


def collapse_input_tokens(tokens: list[str]) -> str | None:
    if not tokens:
        return None
    parts: list[str] = []
    segment: list[str] = []

    def flush() -> None:
        nonlocal segment
        if not segment:
            return
        directions = "".join(token for token in segment if token in DIRECTION_TOKENS)
        buttons = [token for token in segment if token in BUTTON_TOKENS]
        extras = [token for token in segment if token not in DIRECTION_TOKENS | BUTTON_TOKENS]
        if buttons:
            parts.append(f"{directions}{collapse_button_tokens(buttons)}")
        elif directions:
            parts.append(directions)
        elif extras:
            parts.append("".join(extras))
        segment = []

    for token in tokens:
        if token == "+":
            continue
        if token in {"|", ">"}:
            flush()
            parts.append(token)
            continue
        segment.append(token)
    flush()
    return compact_text("".join(parts))


def normalize_official_input(icon_sources: list[str], move_name: str | None) -> str | None:
    tokens = [ICON_TOKEN_MAP.get(basename(path)) for path in icon_sources]
    collapsed = collapse_input_tokens([token for token in tokens if token])
    prefix = infer_official_prefix(move_name)
    if collapsed and prefix and collapsed in BUTTON_TOKENS:
        return f"{prefix}{collapsed}"
    return collapsed


def parse_startup_int(value: str | None) -> int | None:
    text = compact_text(value)
    if not text:
        return None
    match = re.search(r"\d+", text)
    if not match:
        return None
    return int(match.group(0))


def parse_advantage_int(value: str | None) -> int | None:
    text = compact_text(value)
    if not text or text in NULLISH_VALUES:
        return None
    if re.fullmatch(r"[+-]?\d+", text):
        return int(text)
    signed = re.findall(r"[+-]?\d+", text)
    if signed:
        return int(signed[0])
    return None


def extract_explicit_total(value: str | None) -> str | None:
    text = compact_text(value)
    if not text:
        return None
    match = re.search(r"全体\s*(\d+)", text)
    if match:
        return match.group(1)
    return None


def parse_official_active(value: str | None) -> ActiveParseResult:
    text = compact_text(value)
    if not text or text in NULLISH_VALUES:
        return ActiveParseResult(kind=None, start=None, end=None, frames=None, ambiguous=False)
    note_prefix = False
    if text.startswith("[") and "]" in text:
        text = compact_text(text.split("]", 1)[1])
        note_prefix = True
    if text and re.fullmatch(r"\d+", text):
        number = int(text)
        return ActiveParseResult(kind="single", start=number, end=number, frames=1, ambiguous=note_prefix)
    if text:
        match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", text)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            return ActiveParseResult(kind="range", start=start, end=end, frames=end - start + 1, ambiguous=note_prefix)
    return ActiveParseResult(kind="unparsed", start=None, end=None, frames=None, ambiguous=True)
