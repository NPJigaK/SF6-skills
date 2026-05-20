from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .aliases import ResolvedContext, resolve_query
from .current_facts import lookup_current_fact
from .paths import repo_root

NUMERIC_TERMS = (
    "frame",
    "startup",
    "block",
    "damage",
    "scaling",
    "punish",
    "フレーム",
    "発生",
    "ガード",
    "硬直差",
    "確反",
    "ダメージ",
    "補正",
    "何f",
    "何F",
)


def is_numeric_or_current_fact_query(query: str) -> bool:
    lowered = query.casefold()
    return any(term.casefold() in lowered for term in NUMERIC_TERMS)


def prepare_answer(query: str) -> dict[str, Any]:
    context = resolve_query(query)
    packet: dict[str, Any] = {
        "schema_version": "answer_packet/v1",
        "query": query,
        "resolved_context": context.to_dict(),
        "mode": "daily_local",
        "status": "hold",
        "answer": None,
        "evidence": [],
        "uncertainty": [],
    }

    if not is_numeric_or_current_fact_query(query):
        packet["status"] = "prepared"
        packet["answer"] = (
            "This scaffold can prepare deterministic current-fact answers. "
            "General coaching prose is intentionally deferred to a later ExecPlan."
        )
        packet["uncertainty"].append("General prose retrieval is not implemented in this scaffold.")
        return packet

    missing = _missing_lookup_parts(context)
    if missing:
        packet["status"] = "hold"
        packet["uncertainty"].append(
            "Numeric/current-fact answer requires deterministic lookup fields: "
            + ", ".join(missing)
        )
        return packet

    assert context.character_slug is not None
    assert context.move_input is not None
    assert context.field is not None
    try:
        fact = lookup_current_fact(context.character_slug, context.move_input, context.field)
    except (LookupError, ValueError) as exc:
        packet["status"] = "hold"
        packet["uncertainty"].append(str(exc))
        return packet

    packet["status"] = "answered"
    packet["answer"] = (
        f"{fact.character_slug} {fact.input} {fact.field}: {fact.value} "
        f"({fact.authority})"
    )
    packet["evidence"].append(
        {
            "kind": "deterministic_current_fact_lookup",
            "authority": fact.authority,
            "source_path": fact.source_path,
            "fact": fact.to_dict(),
        }
    )
    return packet


def verify_answer_packet(packet: dict[str, Any]) -> dict[str, Any]:
    numeric = is_numeric_or_current_fact_query(str(packet.get("query", "")))
    evidence = packet.get("evidence", [])
    deterministic_evidence = [
        item for item in evidence if item.get("kind") == "deterministic_current_fact_lookup"
    ]
    issues: list[str] = []
    if numeric and packet.get("status") == "answered" and not deterministic_evidence:
        issues.append("Numeric/current-fact answer lacks deterministic current-fact evidence.")
    if packet.get("status") == "answered" and packet.get("answer") is None:
        issues.append("Answered packet has no answer text.")
    return {
        "ok": not issues,
        "issues": issues,
        "checked_at": datetime.now(UTC).isoformat(),
    }


def append_answer_log(packet: dict[str, Any], base_dir: Path | None = None) -> Path:
    target_dir = (base_dir or _default_log_dir()).expanduser()
    path = target_dir / "answer-log.jsonl"
    _reject_repo_internal_log_path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    record = {"logged_at": datetime.now(UTC).isoformat(), "packet": packet}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def _default_log_dir() -> Path:
    env_value = os.environ.get("SF6_COACH_LOG_DIR")
    if env_value:
        return Path(env_value).expanduser()
    state_home = os.environ.get("XDG_STATE_HOME")
    if state_home:
        return Path(state_home).expanduser() / "sf6-knowledge-coach"
    return Path.home() / ".local" / "state" / "sf6-knowledge-coach"


def _missing_lookup_parts(context: ResolvedContext) -> list[str]:
    missing: list[str] = []
    if not context.character_slug:
        missing.append("character_slug")
    if not context.move_input:
        missing.append("move_input")
    if not context.field:
        missing.append("field")
    return missing


def _reject_repo_internal_log_path(path: Path) -> None:
    resolved_repo = repo_root().resolve()
    resolved_path = path.resolve()
    if resolved_path == resolved_repo or resolved_repo in resolved_path.parents:
        raise ValueError("Answer logs must be outside the Git repository.")
