#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pytest

from audit_supercombo_enriched_review_status import audit
from build_official_supercombo_enriched_data import review_queues_from_flags


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def test_review_queue_mapping() -> None:
    assert_equal(
        review_queues_from_flags(["multiple_candidates"]),
        ["structural_ambiguity"],
        "multiple candidates queue",
    )
    assert_equal(
        review_queues_from_flags(["supercombo_row_reused"]),
        ["structural_ambiguity"],
        "reused SuperCombo row queue",
    )
    assert_equal(
        review_queues_from_flags(["condition_dependent_supercombo_field:damage"]),
        ["condition_dependent_field"],
        "condition-dependent field queue",
    )
    assert_equal(
        review_queues_from_flags(["basic_field_conflict:damage"]),
        ["field_conflict"],
        "field conflict queue",
    )
    assert_equal(
        review_queues_from_flags(["manual_match", "ambiguous_match"]),
        ["manual_or_ambiguous_match"],
        "manual or ambiguous queue",
    )
    assert_equal(
        review_queues_from_flags(["uncomparable_basic_field:damage"]),
        ["uncomparable_notation"],
        "uncomparable notation queue",
    )


def test_audit_rejects_missing_enriched_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="official-supercombo-enriched"):
        audit(tmp_path)


def test_audit_rejects_empty_enriched_root(tmp_path: Path) -> None:
    root = (
        tmp_path
        / "wiki"
        / "outputs"
        / "data"
        / "frame-data"
        / "official-supercombo-enriched"
    )
    root.mkdir(parents=True)

    with pytest.raises(RuntimeError, match="no enriched rows"):
        audit(tmp_path)


def main() -> int:
    test_review_queue_mapping()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
