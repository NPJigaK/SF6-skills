from __future__ import annotations

from pathlib import Path
import yaml
from pydantic import BaseModel, Field

from .config import package_root
from .core.common import sha256_hex
from .registry import LoadedRegistry
from .schemas import BindingClass, ConfirmationStatus


class SupercomboBindingEntry(BaseModel):
    raw_source_token: str
    binding_class: BindingClass
    target_move_id: str | None = None
    candidate_move_ids: list[str] = Field(default_factory=list)
    collision_group: str | None = None
    conflicting_move_ids: list[str] = Field(default_factory=list)
    publish_eligible: bool = False
    confirmation_status: ConfirmationStatus = "not_required"
    notes: str | None = None


class SupercomboBindingPolicyDocument(BaseModel):
    binding_policy_version: str
    entries: list[SupercomboBindingEntry]


class LoadedSupercomboBindingPolicy:
    def __init__(self, version: str, sha256: str, entries: list[SupercomboBindingEntry], registry: LoadedRegistry) -> None:
        self.version = version
        self.sha256 = sha256
        self.entries = entries
        self.by_raw_source_token = {entry.raw_source_token: entry for entry in entries}
        if len(self.by_raw_source_token) != len(entries):
            raise ValueError("duplicate raw_source_token entries in binding policy")
        for entry in entries:
            self._validate_entry(entry, registry)

    def lookup(self, raw_source_token: str | None) -> SupercomboBindingEntry | None:
        if not raw_source_token:
            return None
        return self.by_raw_source_token.get(raw_source_token)

    @staticmethod
    def _validate_entry(entry: SupercomboBindingEntry, registry: LoadedRegistry) -> None:
        def ensure_move_ids_exist(move_ids: list[str]) -> None:
            unknown = [move_id for move_id in move_ids if move_id not in registry.by_move_id]
            if unknown:
                raise ValueError(f"binding policy unknown move_id(s) for {entry.raw_source_token}: {unknown}")

        if entry.target_move_id is not None and entry.target_move_id not in registry.by_move_id:
            raise ValueError(f"binding policy unknown target_move_id for {entry.raw_source_token}: {entry.target_move_id}")
        ensure_move_ids_exist(entry.candidate_move_ids)
        ensure_move_ids_exist(entry.conflicting_move_ids)

        if entry.binding_class in {"A", "B", "C"}:
            if not entry.target_move_id or not entry.publish_eligible or entry.confirmation_status != "not_required":
                raise ValueError(f"binding policy invalid publishable entry for {entry.raw_source_token}")
        elif entry.binding_class == "F":
            if not entry.target_move_id or entry.confirmation_status not in {"confirmed", "unconfirmed"}:
                raise ValueError(f"binding policy invalid class F entry for {entry.raw_source_token}")
            if not isinstance(entry.publish_eligible, bool):
                raise ValueError(f"binding policy invalid class F entry for {entry.raw_source_token}")
        elif entry.binding_class == "D":
            if not entry.candidate_move_ids or entry.publish_eligible:
                raise ValueError(f"binding policy invalid class D entry for {entry.raw_source_token}")
        elif entry.binding_class == "E":
            if not entry.collision_group and not entry.conflicting_move_ids:
                raise ValueError(f"binding policy invalid class E entry for {entry.raw_source_token}")
            if entry.publish_eligible:
                raise ValueError(f"binding policy invalid class E entry for {entry.raw_source_token}")
        elif entry.binding_class == "G":
            if entry.publish_eligible:
                raise ValueError(f"binding policy invalid class G entry for {entry.raw_source_token}")


def load_supercombo_binding_policy(character_slug: str, registry: LoadedRegistry) -> LoadedSupercomboBindingPolicy:
    path = Path(package_root() / "config" / "binding_policy" / f"{character_slug}.supercombo.yaml")
    text = path.read_text(encoding="utf-8")
    payload = yaml.safe_load(text) or {}
    document = SupercomboBindingPolicyDocument.model_validate(payload)
    return LoadedSupercomboBindingPolicy(document.binding_policy_version, sha256_hex(text), document.entries, registry)
