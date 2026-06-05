#!/usr/bin/env python3
from __future__ import annotations

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


def main() -> int:
    test_review_queue_mapping()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
