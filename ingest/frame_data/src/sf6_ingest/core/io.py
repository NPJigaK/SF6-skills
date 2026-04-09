from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ..schemas import ManualReviewRecord, RunManifest, SnapshotManifest, SnapshotMetadata, field_names
from ..versioning import DERIVATION_RULE_VERSION, EXPORT_CONTRACT_VERSION, SCHEMA_VERSION


@dataclass(frozen=True)
class LoadedSnapshot:
    raw_bytes: bytes
    html: str
    metadata: SnapshotMetadata


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def raw_snapshot_dir(repo_root: Path, source: str, character_slug: str, snapshot_id: str) -> Path:
    return repo_root / "data" / "raw" / source / character_slug / snapshot_id


def decode_snapshot_bytes(raw_bytes: bytes, response_encoding: str | None) -> str:
    encoding = response_encoding or "utf-8"
    try:
        decoded = raw_bytes.decode(encoding, errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"failed to decode snapshot bytes with encoding={encoding}") from exc
    return decoded.replace("\r\n", "\n").replace("\r", "\n")


def save_snapshot(repo_root: Path, raw_bytes: bytes, metadata: SnapshotMetadata) -> LoadedSnapshot:
    target_dir = raw_snapshot_dir(repo_root, metadata.source, metadata.character_slug, metadata.snapshot_id)
    ensure_dir(target_dir)
    raw_payload_filename = "page.html"
    metadata_filename = "metadata.json"
    (target_dir / raw_payload_filename).write_bytes(raw_bytes)
    enriched_metadata = metadata.model_copy(
        update={"raw_payload_filename": raw_payload_filename, "metadata_filename": metadata_filename}
    )
    (target_dir / metadata_filename).write_text(
        json.dumps(enriched_metadata.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    html = decode_snapshot_bytes(raw_bytes, enriched_metadata.response_encoding)
    return LoadedSnapshot(raw_bytes=raw_bytes, html=html, metadata=enriched_metadata)


def load_snapshot(repo_root: Path, source: str, character_slug: str, snapshot_id: str) -> LoadedSnapshot:
    target_dir = raw_snapshot_dir(repo_root, source, character_slug, snapshot_id)
    metadata = SnapshotMetadata.model_validate_json((target_dir / "metadata.json").read_text(encoding="utf-8"))
    raw_bytes = (target_dir / metadata.raw_payload_filename).read_bytes()
    html = decode_snapshot_bytes(raw_bytes, metadata.response_encoding)
    return LoadedSnapshot(raw_bytes=raw_bytes, html=html, metadata=metadata)


def normalized_run_dir(repo_root: Path, character_slug: str, run_id: str) -> Path:
    return repo_root / "data" / "normalized" / character_slug / run_id


def exports_dir(repo_root: Path, character_slug: str) -> Path:
    return repo_root / "data" / "exports" / character_slug


def write_model_rows(target_dir: Path, records: list[BaseModel], model_cls: type[BaseModel], manual_review_rows: list[BaseModel]) -> None:
    ensure_dir(target_dir)
    rows = [model_cls.model_validate(record).model_dump(mode="json") for record in records]
    _write_json(target_dir / "records.json", rows)
    _write_csv(target_dir / "records.csv", rows, field_names(model_cls))
    review_rows = [model_cls.model_validate(record).model_dump(mode="json") for record in manual_review_rows]
    _write_json(target_dir / "manual_review.json", review_rows)
    _write_csv(target_dir / "manual_review.csv", review_rows, field_names(model_cls))


def read_model_rows(path: Path, model_cls: type[BaseModel]) -> list[BaseModel]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [model_cls.model_validate(row) for row in rows]


def save_run_manifest(path: Path, manifest: RunManifest) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load_run_manifest(path: Path) -> RunManifest:
    return RunManifest.model_validate_json(path.read_text(encoding="utf-8"))


def default_snapshot_manifest(character_slug: str) -> SnapshotManifest:
    return SnapshotManifest.model_validate(
        {
            "character_slug": character_slug,
            "schema_version": SCHEMA_VERSION,
            "export_contract_version": EXPORT_CONTRACT_VERSION,
            "derivation_rule_version": DERIVATION_RULE_VERSION,
            "datasets": {
                "official_raw": {"publication_state": "unavailable"},
                "supercombo_enrichment": {"publication_state": "unavailable"},
                "derived_metrics": {"publication_state": "unavailable"},
            },
        }
    )


def load_snapshot_manifest(path: Path, character_slug: str) -> SnapshotManifest:
    if not path.exists():
        return default_snapshot_manifest(character_slug)
    manifest = SnapshotManifest.model_validate_json(path.read_text(encoding="utf-8"))
    return manifest.model_copy(
        update={
            "schema_version": SCHEMA_VERSION,
            "export_contract_version": EXPORT_CONTRACT_VERSION,
            "derivation_rule_version": DERIVATION_RULE_VERSION,
        }
    )


def save_snapshot_manifest(path: Path, manifest: SnapshotManifest) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_export_dataset(
    target_dir: Path,
    stem: str,
    records: list[BaseModel],
    model_cls: type[BaseModel],
    manual_review_rows: list[BaseModel],
    manual_review_model_cls: type[BaseModel] = ManualReviewRecord,
) -> str:
    ensure_dir(target_dir)
    rows = [model_cls.model_validate(record).model_dump(mode="json") for record in records]
    json_path = target_dir / f"{stem}.json"
    csv_path = target_dir / f"{stem}.csv"
    manual_json_path = target_dir / f"{stem}_manual_review.json"
    manual_csv_path = target_dir / f"{stem}_manual_review.csv"
    _write_json(json_path, rows)
    _write_csv(csv_path, rows, field_names(model_cls))
    review_rows = [manual_review_model_cls.model_validate(record).model_dump(mode="json") for record in manual_review_rows]
    _write_json(manual_json_path, review_rows)
    _write_csv(manual_csv_path, review_rows, field_names(manual_review_model_cls))
    digest = hashlib.sha256()
    for path in (json_path, csv_path, manual_json_path, manual_csv_path):
        digest.update(path.read_bytes())
    return digest.hexdigest()


def remove_export_dataset(target_dir: Path, stem: str) -> None:
    for path in (
        target_dir / f"{stem}.json",
        target_dir / f"{stem}.csv",
        target_dir / f"{stem}_manual_review.json",
        target_dir / f"{stem}_manual_review.csv",
    ):
        if path.exists():
            path.unlink()


def _write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _write_csv(path: Path, rows: list[dict[str, Any]], header: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(_csv_ready(row))


def _csv_ready(record: dict[str, Any]) -> dict[str, Any]:
    prepared: dict[str, Any] = {}
    for key, value in record.items():
        if isinstance(value, list):
            prepared[key] = " | ".join(str(item) for item in value)
        else:
            prepared[key] = value
    return prepared
