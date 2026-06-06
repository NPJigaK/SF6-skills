from __future__ import annotations

import json
import tempfile
from pathlib import Path

from frame_data_integrity import (
    ensure_supercombo_validation_matches_current_raw,
    invalidate_supercombo_validation,
    supercombo_raw_fingerprint,
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_minimal_raw(root: Path, *, label: str, template_payload: object) -> None:
    write_json(root / "data.templates.json", template_payload)
    write_json(root / "cargo" / "frame-data.json", [{"moveId": "test"}])
    write_json(
        root / "metadata.json",
        {
            "capture_label": label,
            "source_revision": {
                "latest_revision_timestamp": f"{label}T00:00:00Z",
                "pages": [{"title": "Street Fighter 6/Test/Data", "lastrevid": label}],
            },
            "artifacts": {
                "data.templates.json": {"sha256": "sha256:metadata-recorded-template", "byte_count": 10},
                "cargo/frame-data.json": {"sha256": "sha256:cargo", "byte_count": 20},
                "validation.json": {"sha256": "sha256:stale-validation", "byte_count": 30},
            },
        },
    )


def test_validation_fingerprint_must_match_current_raw_metadata() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        write_minimal_raw(root, label="2026-01-01", template_payload={"templates": ["a"]})
        validation = {
            "status": "passed",
            "raw_fingerprint": supercombo_raw_fingerprint(root),
        }

        write_minimal_raw(root, label="2026-01-02", template_payload={"templates": ["b"]})

        try:
            ensure_supercombo_validation_matches_current_raw(root, validation)
        except RuntimeError as exc:
            assert "does not match current SuperCombo raw" in str(exc)
        else:
            raise AssertionError("stale validation should not match changed raw metadata")


def test_validation_without_fingerprint_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        write_minimal_raw(root, label="2026-01-01", template_payload={"templates": ["a"]})

        try:
            ensure_supercombo_validation_matches_current_raw(root, {"status": "passed"})
        except RuntimeError as exc:
            assert "missing raw_fingerprint" in str(exc)
        else:
            raise AssertionError("passed validation without fingerprint should be rejected")


def test_validation_fingerprint_must_match_actual_raw_files() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        write_minimal_raw(root, label="2026-01-01", template_payload={"templates": ["a"]})
        validation = {
            "status": "passed",
            "raw_fingerprint": supercombo_raw_fingerprint(root),
        }

        write_json(root / "data.templates.json", {"templates": ["mutated-without-metadata-update"]})

        try:
            ensure_supercombo_validation_matches_current_raw(root, validation)
        except RuntimeError as exc:
            assert "does not match current SuperCombo raw" in str(exc)
        else:
            raise AssertionError("stale validation should not match changed raw artifact files")


def test_capture_invalidation_removes_stale_validation() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        write_json(root / "validation.json", {"status": "passed"})

        invalidate_supercombo_validation(root)

        assert not (root / "validation.json").exists()


def main() -> int:
    test_validation_fingerprint_must_match_current_raw_metadata()
    test_validation_without_fingerprint_is_rejected()
    test_validation_fingerprint_must_match_actual_raw_files()
    test_capture_invalidation_removes_stale_validation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
