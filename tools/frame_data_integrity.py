from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from typing import Any


SUPERCOMBO_RAW_FINGERPRINT_SCHEMA_VERSION = "supercombo_frame_raw_fingerprint/v1"
FINGERPRINT_EXCLUDED_ARTIFACTS = {"validation.json"}


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint_path_key(path: str) -> str:
    return path.replace("\\", "/")


def normalized_metadata_artifacts(metadata: dict[str, Any]) -> dict[str, Any]:
    artifacts = metadata.get("artifacts", {})
    return {
        fingerprint_path_key(path): artifacts[path]
        for path in sorted(artifacts)
        if fingerprint_path_key(path) not in FINGERPRINT_EXCLUDED_ARTIFACTS
    }


def raw_file_fingerprints(raw_root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    for path in sorted(raw_root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(raw_root).as_posix()
        if relative_path in FINGERPRINT_EXCLUDED_ARTIFACTS:
            continue
        files[relative_path] = {
            "byte_count": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    return files


def supercombo_raw_fingerprint(raw_root: Path) -> dict[str, Any]:
    metadata_path = raw_root / "metadata.json"
    metadata = read_json(metadata_path)
    return {
        "fingerprint_schema_version": SUPERCOMBO_RAW_FINGERPRINT_SCHEMA_VERSION,
        "metadata_sha256": sha256_file(metadata_path),
        "capture_label": metadata.get("capture_label"),
        "source_revision": metadata.get("source_revision"),
        "metadata_artifacts": normalized_metadata_artifacts(metadata),
        "raw_files": raw_file_fingerprints(raw_root),
    }


def ensure_supercombo_validation_matches_current_raw(raw_root: Path, validation: dict[str, Any]) -> None:
    expected = validation.get("raw_fingerprint")
    if not expected:
        raise RuntimeError("SuperCombo validation is missing raw_fingerprint; rerun validation")
    current = supercombo_raw_fingerprint(raw_root)
    if expected != current:
        raise RuntimeError("SuperCombo validation raw_fingerprint does not match current SuperCombo raw")


def invalidate_supercombo_validation(raw_root: Path) -> None:
    (raw_root / "validation.json").unlink(missing_ok=True)
