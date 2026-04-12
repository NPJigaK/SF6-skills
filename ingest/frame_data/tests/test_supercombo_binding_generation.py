from __future__ import annotations

from pathlib import Path

import yaml

from sf6_ingest.core.io import load_snapshot
from sf6_ingest.registry import load_registry
from sf6_ingest.supercombo_binding_generation import (
    build_supercombo_binding_policy_document,
    serialize_supercombo_binding_policy_document,
)
from sf6_ingest.binding_policy import SupercomboBindingPolicyDocument


CHECKED_IN_SUPERCOMBO_SNAPSHOTS = {
    "jp": "20260310T023617Z-3b8fa28a",
    "luke": "20260412T151204Z-d96c657b",
}


def _checked_in_binding_policy_payload(character_slug: str) -> dict:
    path = Path(__file__).resolve().parents[1] / "config" / "binding_policy" / f"{character_slug}.supercombo.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _normalized_binding_policy_payload(payload: dict) -> dict:
    normalized_entries = []
    for entry in payload["entries"]:
        normalized_entries.append({key: value for key, value in entry.items() if value not in (None, [], {})})
    normalized_entries.sort(key=lambda entry: entry["raw_source_token"])
    return {
        "binding_policy_version": payload["binding_policy_version"],
        "entries": normalized_entries,
    }


def test_binding_generation_reproduces_checked_in_jp_policy() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    registry = load_registry("jp")
    snapshot = load_snapshot(repo_root, "supercombo", "jp", CHECKED_IN_SUPERCOMBO_SNAPSHOTS["jp"])

    document = build_supercombo_binding_policy_document("jp", snapshot, registry)

    assert _normalized_binding_policy_payload(document.model_dump(mode="json")) == _normalized_binding_policy_payload(
        _checked_in_binding_policy_payload("jp")
    )


def test_binding_generation_reproduces_checked_in_luke_policy() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    registry = load_registry("luke")
    snapshot = load_snapshot(repo_root, "supercombo", "luke", CHECKED_IN_SUPERCOMBO_SNAPSHOTS["luke"])

    document = build_supercombo_binding_policy_document("luke", snapshot, registry)

    assert _normalized_binding_policy_payload(document.model_dump(mode="json")) == _normalized_binding_policy_payload(
        _checked_in_binding_policy_payload("luke")
    )


def test_empty_binding_policy_serialization_keeps_entries_array() -> None:
    document = SupercomboBindingPolicyDocument(binding_policy_version="1.0.0", entries=[])

    serialized = serialize_supercombo_binding_policy_document(document)

    assert yaml.safe_load(serialized) == {
        "binding_policy_version": "1.0.0",
        "entries": [],
    }
