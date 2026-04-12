from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

import yaml

from .binding_policy import (
    LoadedSupercomboBindingPolicy,
    SupercomboBindingEntry,
    SupercomboBindingPolicyDocument,
)
from .config import package_root, repo_root
from .core.common import compact_text, sha256_hex
from .core.io import LoadedSnapshot
from .core.supercombo import parse_supercombo_snapshot
from .registry import LoadedRegistry, RegistryMove
from .schemas import OfficialExportRecord, SupercomboNormalizedRecord


BINDING_POLICY_VERSION = "1.0.0"
EMPTY_BINDING_POLICY_TEXT = "binding_policy_version: 1.0.0\nentries: []\n"
STRENGTH_NAME_PREFIXES = ("弱_", "中_", "強_")
TOKEN_MARKERS = {"ca", "charged", "hold", "perfect", "recovery", "denjin", "pdr", "drc", "lv2", "lv3", "bomb"}
NOTATION_SEGMENT_RE = re.compile(
    r"^(?:j)?(?:\d+)?(?:lp|mp|hp|lk|mk|hk|pp|kk|lplk|mpmk|hphk|p|k)+$",
    re.IGNORECASE,
)
GENERIC_STRENGTH_TOKEN_RE = re.compile(r"^\d+(?:p|k|pp|kk)$", re.IGNORECASE)
CA_SUFFIX_RE = re.compile(r"\(ca\)$", re.IGNORECASE)
NUMERIC_TOKEN_RE = re.compile(r"-?\d+")


@dataclass(frozen=True)
class OfficialMetrics:
    move_id: str
    input: str | None
    startup: str | None
    recovery: str | None
    total: str | None
    hit_adv: str | None
    block_adv: str | None
    damage: str | None
    cancel: str | None


@dataclass(frozen=True)
class RegistryCandidate:
    move: RegistryMove
    input_key: str | None
    input_compact_key: str | None
    family_key: str | None
    final_key: str | None
    notation_prefix: str | None
    notation_compact_prefix: str | None
    notation_final_key: str | None
    move_id_tail: str
    tags: frozenset[str]
    official: OfficialMetrics | None


@dataclass(frozen=True)
class RecordContext:
    record: SupercomboNormalizedRecord
    raw_body: str
    full_key: str | None
    final_key: str | None
    compact_key: str | None
    family_key: str | None
    followup_key: str | None
    followup_compact_key: str | None
    followup_family_key: str | None
    row_key: str | None
    row_compact_key: str | None
    row_final_key: str | None
    row_followup_key: str | None
    row_followup_compact_key: str | None
    desired_tags: frozenset[str]
    excluded_tags: frozenset[str]
    prefer_tags: frozenset[str]
    avoid_tags: frozenset[str]
    notation_segments: tuple[str, ...]
    generic_strength_base: bool
    is_followup: bool
    jump_alias: bool
    field_map: dict[str, str]


def build_supercombo_binding_policy_document(
    character_slug: str,
    snapshot: LoadedSnapshot,
    registry: LoadedRegistry,
) -> SupercomboBindingPolicyDocument:
    empty_policy = LoadedSupercomboBindingPolicy(
        BINDING_POLICY_VERSION,
        sha256_hex(EMPTY_BINDING_POLICY_TEXT),
        [],
        registry,
    )
    records, _status = parse_supercombo_snapshot(snapshot.metadata, snapshot.html, registry, empty_policy)
    official_metrics = _load_official_metrics(character_slug)
    registry_candidates = [_registry_candidate(move, official_metrics.get(move.move_id)) for move in registry.moves]
    entries = [_propose_entry(_record_context(record), registry_candidates, character_slug) for record in records]
    _apply_collision_entries(entries)
    return SupercomboBindingPolicyDocument(binding_policy_version=BINDING_POLICY_VERSION, entries=entries)


def supercombo_binding_policy_path(character_slug: str) -> Path:
    return Path(package_root() / "config" / "binding_policy" / f"{character_slug}.supercombo.yaml")


def serialize_supercombo_binding_policy_document(document: SupercomboBindingPolicyDocument) -> str:
    payload = document.model_dump(mode="json")
    payload["entries"] = [_prune_empty_values(entry) for entry in payload["entries"]]
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False).replace("\r\n", "\n")


def write_supercombo_binding_policy_document(character_slug: str, document: SupercomboBindingPolicyDocument) -> Path:
    path = supercombo_binding_policy_path(character_slug)
    path.write_text(serialize_supercombo_binding_policy_document(document), encoding="utf-8", newline="\n")
    return path


def _load_official_metrics(character_slug: str) -> dict[str, OfficialMetrics]:
    path = repo_root() / "data" / "exports" / character_slug / "official_raw.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = [OfficialExportRecord.model_validate(row) for row in payload]
    return {
        record.move_id: OfficialMetrics(
            move_id=record.move_id,
            input=record.input,
            startup=record.startup,
            recovery=record.recovery,
            total=record.total,
            hit_adv=record.hit_adv,
            block_adv=record.block_adv,
            damage=record.damage,
            cancel=record.cancel,
        )
        for record in records
    }


def _propose_entry(
    context: RecordContext,
    registry_candidates: list[RegistryCandidate],
    character_slug: str,
) -> SupercomboBindingEntry:
    if _is_excluded_token(context):
        return _excluded_entry(context.record.raw_source_token)

    candidates = _candidate_pool(context, registry_candidates)
    if context.compact_key == "MPMK" and not ({"pdr", "drc"} & set(context.desired_tags)):
        parry_candidates = [candidate for candidate in candidates if "parry" in candidate.move.move_id]
        if parry_candidates:
            candidates = parry_candidates
    candidates = _apply_tag_filters(context, candidates)

    if context.compact_key == "MPMK" and not ({"pdr", "drc"} & set(context.desired_tags)) and len(candidates) > 1:
        return SupercomboBindingEntry(
            raw_source_token=context.record.raw_source_token,
            binding_class="D",
            candidate_move_ids=[candidate.move.move_id for candidate in candidates],
            publish_eligible=False,
            confirmation_status="not_required",
        )

    if "hold" in context.desired_tags and candidates and not any("hold" in candidate.tags for candidate in candidates):
        return _hold_excluded_entry(context.record.raw_source_token)
    if "charged" in context.desired_tags and candidates and not any("charged" in candidate.tags for candidate in candidates):
        return _hold_excluded_entry(context.record.raw_source_token)

    scored = _score_candidates(context, candidates)
    if not scored and ("hold" in context.desired_tags or "charged" in context.desired_tags):
        return _hold_excluded_entry(context.record.raw_source_token)
    if not scored:
        return SupercomboBindingEntry(
            raw_source_token=context.record.raw_source_token,
            binding_class="G",
            publish_eligible=False,
            confirmation_status="not_required",
            notes="excluded source row without canonical official move_id",
        )

    best_score, best_candidate = scored[0]
    tied_candidates = [candidate for score, candidate in scored if score == best_score]
    if len(tied_candidates) > 1:
        return SupercomboBindingEntry(
            raw_source_token=context.record.raw_source_token,
            binding_class="D",
            candidate_move_ids=[candidate.move.move_id for candidate in tied_candidates],
            publish_eligible=False,
            confirmation_status="not_required",
        )

    move_id = best_candidate.move.move_id
    binding_class = "A"
    confirmation_status = "not_required"
    notes = None

    if context.jump_alias:
        binding_class = "B"
        notes = "jump-token alias drift"
    elif "pdr" in context.desired_tags:
        binding_class = "B"
        notes = "live token renamed from Luke-prefixed pattern" if character_slug == "luke" else "live token renamed from legacy registry token"
    elif "ca" in context.desired_tags:
        binding_class = "C"
    elif "recovery" in context.desired_tags or "drc" in context.desired_tags:
        binding_class = "F"
        confirmation_status = "confirmed"
        if character_slug == "luke":
            notes = "live token explicitly marks wakeup recovery variant" if "recovery" in context.desired_tags else "live token renamed from Luke-prefixed pattern"
        else:
            notes = "fixture-confirmed wakeup drive reversal" if "recovery" in context.desired_tags else "fixture-confirmed cancel drive rush"
    elif context.compact_key == "6HPHK" and character_slug == "jp":
        notes = "live source explicitly marks block variant"

    if binding_class == "C" and character_slug == "jp":
        notes = "publishable only when raw token suffix is preserved"

    return SupercomboBindingEntry(
        raw_source_token=context.record.raw_source_token,
        binding_class=binding_class,
        target_move_id=move_id,
        publish_eligible=True,
        confirmation_status=confirmation_status,
        notes=notes,
    )


def _record_context(record: SupercomboNormalizedRecord) -> RecordContext:
    raw_body = record.raw_source_token.split("_", 1)[1] if "_" in record.raw_source_token else record.raw_source_token
    full_key, notation_segments, markers = _token_notation_signature(raw_body)
    compact_key = _compact_notation_key(full_key)
    family_key = _family_key(compact_key)
    row_key = _normalize_row_input(record.input)
    row_compact_key = _compact_notation_key(row_key)
    desired_tags = set(markers)
    lowered_name = (compact_text(record.move_name) or "").lower()
    if CA_SUFFIX_RE.search(record.move_name or ""):
        desired_tags.add("ca")
    if "perfect" in lowered_name:
        desired_tags.add("perfect")
    if "hold" in lowered_name:
        desired_tags.add("hold")
    if "denjin" in lowered_name:
        desired_tags.add("denjin")
    if "lv2" in lowered_name:
        desired_tags.add("lv2")
    if "lv3" in lowered_name:
        desired_tags.add("lv3")
    if _is_aerial_special_token(notation_segments):
        desired_tags.add("aerial")
    jump_alias = _is_jump_alias(notation_segments)
    field_map = _raw_row_field_map(record)
    generic_strength_base = (
        len(notation_segments) == 1
        and bool(notation_segments)
        and GENERIC_STRENGTH_TOKEN_RE.fullmatch(notation_segments[0])
        and record.move_group != "super_arts"
    )
    is_followup = len(notation_segments) > 1
    prefer_tags: set[str] = set()
    avoid_tags: set[str] = set()
    if generic_strength_base:
        prefer_tags.add("strength_named")
    if is_followup:
        avoid_tags.add("strength_named")
    excluded_tags = {"ca", "hold", "perfect", "aerial", "recovery", "drc", "pdr"} - desired_tags
    if compact_key == "MPMK":
        excluded_tags.discard("perfect")
    followup_key = _followup_key(full_key)
    followup_compact_key = _compact_notation_key(followup_key)
    row_followup_key = _followup_key(row_key)
    row_followup_compact_key = _compact_notation_key(row_followup_key)
    return RecordContext(
        record=record,
        raw_body=raw_body.lower(),
        full_key=full_key,
        final_key=_final_step(full_key),
        compact_key=compact_key,
        family_key=family_key,
        followup_key=followup_key,
        followup_compact_key=followup_compact_key,
        followup_family_key=_family_key(followup_compact_key),
        row_key=row_key,
        row_compact_key=row_compact_key,
        row_final_key=_final_step(row_key),
        row_followup_key=row_followup_key,
        row_followup_compact_key=row_followup_compact_key,
        desired_tags=frozenset(desired_tags),
        excluded_tags=frozenset(excluded_tags),
        prefer_tags=frozenset(prefer_tags),
        avoid_tags=frozenset(avoid_tags),
        notation_segments=notation_segments,
        generic_strength_base=generic_strength_base,
        is_followup=is_followup,
        jump_alias=jump_alias,
        field_map=field_map,
    )


def _candidate_pool(context: RecordContext, registry_candidates: list[RegistryCandidate]) -> list[RegistryCandidate]:
    jump_alias_key = context.compact_key[1:] if context.jump_alias and context.compact_key and context.compact_key.startswith("J") else None
    exact_values = {
        value.lower()
        for value in (
            context.raw_body,
            context.compact_key,
            context.followup_compact_key,
            context.row_compact_key,
            context.row_followup_compact_key,
            jump_alias_key,
            "6656MPMK" if {"pdr", "drc"} & set(context.desired_tags) and context.compact_key == "MPMK" else None,
        )
        if value
    }
    key_values = {
        value.upper()
        for value in (
            context.full_key,
            context.final_key,
            context.row_key,
            context.row_final_key,
            context.followup_key,
            context.row_followup_key,
            jump_alias_key,
            "6656MPMK" if {"pdr", "drc"} & set(context.desired_tags) and context.compact_key == "MPMK" else None,
        )
        if value
    }
    family_values = {
        value
        for value in (
            context.family_key,
            context.followup_family_key,
        )
        if value
    }

    matches: list[RegistryCandidate] = []
    seen_move_ids: set[str] = set()
    for candidate in registry_candidates:
        match = False
        if candidate.move_id_tail.startswith(context.raw_body):
            match = True
        if context.followup_compact_key and candidate.move_id_tail.startswith(context.followup_compact_key.lower()):
            match = True
        if candidate.notation_compact_prefix and candidate.notation_compact_prefix.lower() in exact_values:
            match = True
        if candidate.input_compact_key and candidate.input_compact_key.lower() in exact_values:
            match = True
        if candidate.notation_prefix and candidate.notation_prefix in key_values:
            match = True
        if candidate.input_key and candidate.input_key in key_values:
            match = True
        if candidate.family_key and candidate.family_key in family_values:
            match = True
        if candidate.notation_final_key and candidate.notation_final_key in key_values:
            match = True
        if candidate.final_key and candidate.final_key in key_values:
            match = True
        if not match:
            continue
        if candidate.move.move_id in seen_move_ids:
            continue
        seen_move_ids.add(candidate.move.move_id)
        matches.append(candidate)
    return matches


def _apply_tag_filters(context: RecordContext, candidates: list[RegistryCandidate]) -> list[RegistryCandidate]:
    filtered = list(candidates)
    for tag in sorted(context.desired_tags):
        tagged = [candidate for candidate in filtered if tag in candidate.tags]
        if tagged:
            filtered = tagged
    for tag in sorted(context.excluded_tags):
        untagged = [candidate for candidate in filtered if tag not in candidate.tags]
        if untagged:
            filtered = untagged
    for tag in sorted(context.prefer_tags):
        preferred = [candidate for candidate in filtered if tag in candidate.tags]
        if preferred:
            filtered = preferred
    for tag in sorted(context.avoid_tags):
        preferred = [candidate for candidate in filtered if tag not in candidate.tags]
        if preferred:
            filtered = preferred
    return filtered


def _score_candidates(
    context: RecordContext,
    candidates: list[RegistryCandidate],
) -> list[tuple[int, RegistryCandidate]]:
    scored = [(_score_candidate(context, candidate), candidate) for candidate in candidates]
    scored = [(score, candidate) for score, candidate in scored if score > 0]
    return sorted(scored, key=lambda item: (-item[0], item[1].move.sort_key))


def _score_candidate(context: RecordContext, candidate: RegistryCandidate) -> int:
    score = 0
    if candidate.move_id_tail.startswith(context.raw_body):
        score += 50
    if context.followup_compact_key and candidate.move_id_tail.startswith(context.followup_compact_key.lower()):
        score += 45
    if candidate.notation_compact_prefix and candidate.notation_compact_prefix == context.compact_key:
        score += 40
    if context.followup_compact_key and candidate.notation_compact_prefix == context.followup_compact_key:
        score += 38
    if candidate.input_compact_key and candidate.input_compact_key == context.row_compact_key:
        score += 35
    if context.row_followup_compact_key and candidate.input_compact_key == context.row_followup_compact_key:
        score += 34
    if candidate.notation_prefix and candidate.notation_prefix == context.full_key:
        score += 30
    if context.followup_key and candidate.notation_prefix == context.followup_key:
        score += 28
    if candidate.input_key and candidate.input_key == context.row_key:
        score += 27
    if context.row_followup_key and candidate.input_key == context.row_followup_key:
        score += 25
    if candidate.family_key and candidate.family_key == context.family_key:
        score += 16
    if context.followup_family_key and candidate.family_key == context.followup_family_key:
        score += 14
    if candidate.notation_final_key and candidate.notation_final_key == context.final_key:
        score += 12
    if candidate.final_key and candidate.final_key == context.row_final_key:
        score += 10
    if context.is_followup and "strength_named" not in candidate.tags:
        score += 4
    if context.generic_strength_base and "strength_named" in candidate.tags:
        score += 4
    for tag in ("ca", "hold", "perfect", "aerial", "recovery", "pdr", "drc"):
        if tag in context.desired_tags and tag in candidate.tags:
            score += 18
    score += _metric_score(context, candidate.official)
    return score


def _metric_score(context: RecordContext, official: OfficialMetrics | None) -> int:
    if official is None:
        return 0
    score = 0
    score += _shared_numeric_score(context.field_map.get("Total"), official.total, points=10)
    score += _shared_numeric_score(context.field_map.get("Recovery"), official.recovery, points=8)
    score += _shared_numeric_score(context.field_map.get("Recovery"), official.total, points=4)
    score += _shared_numeric_score(context.field_map.get("Startup"), official.startup, points=6)
    score += _shared_numeric_score(context.field_map.get("Damage"), official.damage, points=6)
    score += _shared_numeric_score(context.field_map.get("Block Advantage"), official.block_adv, points=6)
    score += _shared_numeric_score(context.field_map.get("Hit Advantage"), official.hit_adv, points=4)
    if _same_cancel(context.field_map.get("Cancel"), official.cancel):
        score += 3
    return score


def _shared_numeric_score(left: str | None, right: str | None, *, points: int) -> int:
    left_numbers = _numeric_tokens(left)
    right_numbers = _numeric_tokens(right)
    if not left_numbers or not right_numbers:
        return 0
    if left_numbers[0] == right_numbers[0]:
        return points
    return 0


def _same_cancel(left: str | None, right: str | None) -> bool:
    left_value = compact_text(left)
    right_value = compact_text(right)
    if not left_value or not right_value:
        return False
    return left_value.upper() == right_value.upper()


def _numeric_tokens(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(NUMERIC_TOKEN_RE.findall(value))


def _registry_candidate(move: RegistryMove, official: OfficialMetrics | None) -> RegistryCandidate:
    input_key = _normalize_registry_input(move)
    notation_prefix = _registry_notation_prefix(move.move_id)
    move_id_tail = _move_id_tail(move.move_id)
    return RegistryCandidate(
        move=move,
        input_key=input_key,
        input_compact_key=_compact_notation_key(input_key),
        family_key=_family_key(_compact_notation_key(input_key)),
        final_key=_final_step(input_key),
        notation_prefix=notation_prefix,
        notation_compact_prefix=_compact_notation_key(notation_prefix),
        notation_final_key=_final_step(notation_prefix),
        move_id_tail=move_id_tail,
        tags=frozenset(_registry_tags(move)),
        official=official,
    )


def _registry_tags(move: RegistryMove) -> set[str]:
    lowered_move_id = move.move_id.lower()
    tail = _move_id_tail(move.move_id)
    notation_prefix = _registry_notation_prefix(move.move_id)
    lowered_name_key = compact_text(move.official_match.name_key)
    lowered_name_key = lowered_name_key.lower() if lowered_name_key else ""
    tags: set[str] = set()
    if "ca_" in lowered_name_key or "_ca_" in lowered_move_id:
        tags.add("ca")
    if "電刃" in lowered_name_key or "denjin" in lowered_move_id:
        tags.add("denjin")
    if "lv2" in lowered_name_key or "lv2" in lowered_move_id:
        tags.add("lv2")
    if "lv3" in lowered_name_key or "lv3" in lowered_move_id:
        tags.add("lv3")
    if "hold" in lowered_move_id or "ホールド" in lowered_name_key:
        tags.add("hold")
    if "charged" in lowered_move_id or "溜め" in lowered_name_key:
        tags.add("charged")
    if "perfect" in lowered_move_id or "ジャスト" in lowered_name_key:
        tags.add("perfect")
    if "起き上がり時" in lowered_name_key or "drive_reversal_wakeup" in lowered_move_id:
        tags.add("recovery")
    if "パリィドライブラッシュ" in lowered_name_key or "parry_drive_rush" in lowered_move_id:
        tags.add("pdr")
    if "キャンセルドライブラッシュ" in lowered_name_key or "cancel_drive_rush" in lowered_move_id:
        tags.add("drc")
    if notation_prefix and notation_prefix.startswith("J"):
        tags.add("aerial")
    if lowered_name_key.startswith(STRENGTH_NAME_PREFIXES):
        tags.add("strength_named")
    return tags


def _normalize_registry_input(move: RegistryMove) -> str | None:
    tokens = list(move.official_match.icon_tokens)
    if not tokens:
        return None
    if tokens[:3] == ["5", "|", "6"] and tokens[-1] == "LPLK":
        return "LPLK"
    normalized: list[str] = []
    for token in tokens:
        if token == "|":
            continue
        if token == "j.":
            normalized.append("J")
            continue
        normalized.append(token.upper())
    return "".join(normalized)


def _normalize_row_input(value: str | None) -> str | None:
    text = compact_text(value)
    if not text:
        return None
    normalized = text.replace("PF.", "").replace("pf.", "")
    normalized = normalized.replace("j.", "J").replace("J.", "J")
    normalized = normalized.replace("[", "").replace("]", "")
    normalized = normalized.replace("~", ">")
    return normalized.replace(".", "").upper()


def _token_notation_signature(raw_body: str) -> tuple[str | None, tuple[str, ...], frozenset[str]]:
    lowered_body = raw_body.lower()
    markers = {marker for marker in TOKEN_MARKERS if marker in lowered_body}
    if "(ca)" in lowered_body:
        markers.add("ca")
    if "(charged)" in lowered_body:
        markers.add("charged")
    notation_segments: list[str] = []
    for segment in raw_body.split("_"):
        cleaned_segment = segment.replace("(ca)", "").replace("(charged)", "")
        lowered_segment = cleaned_segment.lower()
        if lowered_segment in TOKEN_MARKERS or lowered_segment == "66":
            continue
        normalized = _normalize_notation_segment(cleaned_segment)
        if normalized:
            notation_segments.append(normalized)
    full_key = ">".join(notation_segments) if notation_segments else None
    return full_key, tuple(notation_segments), frozenset(markers)


def _normalize_notation_segment(value: str) -> str | None:
    text = compact_text(value)
    if not text:
        return None
    text = text.replace(".", "")
    lowered = text.lower()
    if not NOTATION_SEGMENT_RE.fullmatch(lowered):
        return None
    prefix = ""
    if lowered.startswith("j"):
        prefix = "J"
        text = text[1:]
    return prefix + text.upper()


def _compact_notation_key(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def _family_key(value: str | None) -> str | None:
    if not value:
        return None
    family = value.upper()
    for source, target in (("LP", "P"), ("MP", "P"), ("HP", "P"), ("LK", "K"), ("MK", "K"), ("HK", "K")):
        family = family.replace(source, target)
    return family


def _followup_key(value: str | None) -> str | None:
    if not value or ">" not in value:
        return None
    return value.split(">", 1)[1]


def _final_step(value: str | None) -> str | None:
    if not value:
        return None
    return value.rsplit(">", 1)[-1]


def _move_id_tail(move_id: str) -> str:
    parts = move_id.split("_", 2)
    return parts[2].lower() if len(parts) >= 3 else move_id.lower()


def _registry_notation_prefix(move_id: str) -> str | None:
    segments = _move_id_tail(move_id).split("_")
    notation_segments: list[str] = []
    started = False
    for segment in segments:
        if _normalize_notation_segment(segment):
            notation_segments.append(_normalize_notation_segment(segment) or "")
            started = True
            continue
        if started:
            break
    if not notation_segments:
        return None
    return ">".join(notation_segments)


def _is_aerial_special_token(notation_segments: tuple[str, ...]) -> bool:
    if not notation_segments:
        return False
    first = notation_segments[0]
    return first.startswith("J") and any(character.isdigit() for character in first[1:])


def _is_jump_alias(notation_segments: tuple[str, ...]) -> bool:
    if len(notation_segments) != 1:
        return False
    token = notation_segments[0]
    if not token.startswith("J"):
        return False
    return not any(character.isdigit() for character in token[1:])


def _raw_row_field_map(record: SupercomboNormalizedRecord) -> dict[str, str]:
    payload = json.loads(record.raw_row_json)
    field_map = payload.get("field_map", {})
    if not isinstance(field_map, dict):
        return {}
    return {str(key): str(value) for key, value in field_map.items()}


def _is_excluded_token(context: RecordContext) -> bool:
    lowered = context.record.raw_source_token.lower()
    return "bomb" in context.desired_tags or "pppkkk" in lowered


def _excluded_entry(raw_source_token: str) -> SupercomboBindingEntry:
    notes = "excluded bomb follow-up without canonical official move_id" if "bomb" in raw_source_token.lower() else "excluded taunt without canonical official move_id"
    return SupercomboBindingEntry(
        raw_source_token=raw_source_token,
        binding_class="G",
        publish_eligible=False,
        confirmation_status="not_required",
        notes=notes,
    )


def _hold_excluded_entry(raw_source_token: str) -> SupercomboBindingEntry:
    return SupercomboBindingEntry(
        raw_source_token=raw_source_token,
        binding_class="G",
        publish_eligible=False,
        confirmation_status="not_required",
        notes="excluded hold state without canonical official move_id",
    )


def _apply_collision_entries(entries: list[SupercomboBindingEntry]) -> None:
    by_move_id: dict[str, list[int]] = defaultdict(list)
    for index, entry in enumerate(entries):
        if entry.target_move_id and entry.binding_class in {"A", "B", "C", "F"}:
            by_move_id[entry.target_move_id].append(index)

    for move_id, indexes in by_move_id.items():
        if len(indexes) <= 1:
            continue
        collision_group = _collision_group(move_id)
        for index in indexes:
            entry = entries[index]
            if entry.binding_class in {"C", "F"}:
                continue
            entries[index] = SupercomboBindingEntry(
                raw_source_token=entry.raw_source_token,
                binding_class="E",
                collision_group=collision_group,
                conflicting_move_ids=[move_id],
                publish_eligible=False,
                confirmation_status="not_required",
            )


def _collision_group(move_id: str) -> str:
    parts = move_id.split("_")
    if len(parts) < 4:
        return f"{move_id}_followup"
    descriptor = "_".join(parts[3:])
    return f"{parts[0]}_{descriptor}_followup"


def _prune_empty_values(value: Any) -> Any:
    if isinstance(value, dict):
        pruned: dict[str, Any] = {}
        for key, nested_value in value.items():
            cleaned = _prune_empty_values(nested_value)
            if cleaned in (None, [], {}):
                continue
            pruned[key] = cleaned
        return pruned
    if isinstance(value, list):
        cleaned_list = [_prune_empty_values(item) for item in value]
        return [item for item in cleaned_list if item not in (None, [], {})]
    return value
