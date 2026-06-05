#!/usr/bin/env python3
from __future__ import annotations

from extract_supercombo_frame_data import compare_basic_field


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def test_landing_recovery_equivalence() -> None:
    comparison = compare_basic_field("recovery", "着地後3", "3 land")
    assert comparison is not None
    assert_equal(comparison.get("comparable"), True, "landing recovery should be comparable")
    assert_equal(comparison.get("match"), True, "landing recovery should match")
    assert_equal(comparison.get("reason"), "landing_recovery_equivalent", "landing recovery reason")

    compound = compare_basic_field("recovery", "37+着地後15", "37+15 land")
    assert compound is not None
    assert_equal(compound.get("comparable"), True, "compound landing recovery should be comparable")
    assert_equal(compound.get("match"), True, "compound landing recovery should match")
    assert_equal(compound.get("reason"), "landing_recovery_equivalent", "compound landing reason")


def test_condition_parenthetical_damage_is_not_safe_match() -> None:
    comparison = compare_basic_field("damage", "800", "800(700)")
    assert comparison is not None
    assert_equal(comparison.get("comparable"), False, "parenthetical damage should not be comparable")
    assert_equal(
        comparison.get("reason"),
        "condition_dependent_supercombo_field",
        "parenthetical damage reason",
    )


def test_condition_parenthetical_recovery_is_not_safe_match() -> None:
    comparison = compare_basic_field("recovery", "14", "14(16)")
    assert comparison is not None
    assert_equal(comparison.get("comparable"), False, "parenthetical recovery should not be comparable")
    assert_equal(
        comparison.get("reason"),
        "condition_dependent_supercombo_field",
        "parenthetical recovery reason",
    )


def main() -> int:
    test_landing_recovery_equivalence()
    test_condition_parenthetical_damage_is_not_safe_match()
    test_condition_parenthetical_recovery_is_not_safe_match()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
