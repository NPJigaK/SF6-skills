#!/usr/bin/env python3
from __future__ import annotations

from tools.frame_data.supercombo.extract import candidate_score, compare_basic_field


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


def test_strict_multihit_damage_sum() -> None:
    repeated = compare_basic_field("damage", "400", "200x2")
    assert repeated is not None
    assert_equal(repeated.get("comparable"), True, "repeated multihit damage should be comparable")
    assert_equal(repeated.get("match"), True, "repeated multihit damage should match")
    assert_equal(repeated.get("reason"), "multihit_damage_sum", "repeated multihit reason")

    listed = compare_basic_field("damage", "700", "300,400")
    assert listed is not None
    assert_equal(listed.get("comparable"), True, "listed multihit damage should be comparable")
    assert_equal(listed.get("match"), True, "listed multihit damage should match")
    assert_equal(listed.get("reason"), "multihit_damage_sum", "listed multihit reason")


def test_simple_damage_is_not_multihit() -> None:
    comparison = compare_basic_field("damage", "300", "300")
    assert comparison is not None
    assert_equal(comparison.get("comparable"), True, "simple damage should be comparable")
    assert_equal(comparison.get("match"), True, "simple damage should match")
    assert_equal(comparison.get("reason"), None, "simple damage should not have multihit reason")


def test_conditional_multihit_damage_is_not_safe_match() -> None:
    parenthetical = compare_basic_field("damage", "800", "400x2 (800)")
    assert parenthetical is not None
    assert_equal(parenthetical.get("comparable"), False, "parenthetical multihit should not be comparable")

    bracketed = compare_basic_field("damage", "800", "400x2[800]")
    assert bracketed is not None
    assert_equal(bracketed.get("comparable"), False, "bracketed multihit should not be comparable")


def test_multihit_damage_does_not_drive_candidate_selection() -> None:
    official = {
        "official_input_signature": "OFFICIAL",
        "official_category": "unknown",
        "official_move_name": "Official Move",
        "startup": "",
        "active": "",
        "recovery": "",
        "damage": "400",
    }
    candidate = {
        "input": "OTHER",
        "move_type": "special",
        "move_id": "candidate_200x2",
        "startup": "",
        "active": "",
        "recovery": "",
        "damage": "200x2",
    }

    score, reasons = candidate_score(official, candidate, "FAMILY")

    assert_equal(score, 0, "multihit damage should not increase candidate score")
    assert_equal(reasons, [], "multihit damage should not add candidate score reason")


def test_simple_damage_can_drive_candidate_selection() -> None:
    official = {
        "official_input_signature": "OFFICIAL",
        "official_category": "unknown",
        "official_move_name": "Official Move",
        "startup": "",
        "active": "",
        "recovery": "",
        "damage": "400",
    }
    candidate = {
        "input": "OTHER",
        "move_type": "special",
        "move_id": "candidate_400",
        "startup": "",
        "active": "",
        "recovery": "",
        "damage": "400",
    }

    score, reasons = candidate_score(official, candidate, "FAMILY")

    assert_equal(score, 3, "simple damage should increase candidate score")
    assert_equal(reasons, ["damage_match"], "simple damage should add candidate score reason")


def main() -> int:
    test_landing_recovery_equivalence()
    test_condition_parenthetical_damage_is_not_safe_match()
    test_condition_parenthetical_recovery_is_not_safe_match()
    test_strict_multihit_damage_sum()
    test_simple_damage_is_not_multihit()
    test_conditional_multihit_damage_is_not_safe_match()
    test_multihit_damage_does_not_drive_candidate_selection()
    test_simple_damage_can_drive_candidate_selection()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
