from __future__ import annotations

import unittest

from sf6_knowledge_coach.current_fact_guards import is_scalar_calculation_input


ELIGIBLE_STATUS = "eligible_only_after_domain_source_and_unit_checks"


class CurrentFactGuardTests(unittest.TestCase):
    def test_accepted_scalar_contract_fixtures_require_scalar_kind_and_status(self) -> None:
        self.assertTrue(
            is_scalar_calculation_input(
                {"kind": "signed_frame", "unit": "frame", "value": -2},
                ELIGIBLE_STATUS,
            )
        )
        self.assertTrue(
            is_scalar_calculation_input(
                {"kind": "integer", "unit": "damage", "value": 500},
                ELIGIBLE_STATUS,
            )
        )

    def test_scalar_shapes_without_eligible_status_are_rejected(self) -> None:
        parsed_value = {"kind": "signed_frame", "unit": "frame", "value": -2}
        for status in (None, "", "review_required_not_calculation_safe", "not_numeric_authority"):
            with self.subTest(status=status):
                self.assertFalse(is_scalar_calculation_input(parsed_value, status))

    def test_annotated_numeric_candidate_is_not_scalar_even_with_nested_value(self) -> None:
        parsed_value = {
            "kind": "annotated_numeric_candidate",
            "numeric_candidate": {
                "candidate_type": "signed_frame",
                "unit": "frame",
                "value": -4,
            },
        }
        self.assertFalse(
            is_scalar_calculation_input(
                parsed_value,
                "annotated_candidate_not_calculation_safe",
            )
        )
        self.assertFalse(is_scalar_calculation_input(parsed_value, ELIGIBLE_STATUS))

    def test_frame_range_and_ordered_pair_are_not_scalar_calculation_inputs(self) -> None:
        self.assertFalse(
            is_scalar_calculation_input(
                {"kind": "frame_range", "unit": "frame", "start": -12, "end": -1},
                "parsed_range_not_single_value_calculation_safe",
            )
        )
        self.assertFalse(
            is_scalar_calculation_input(
                {"kind": "ordered_pair", "labels": ["throw_range", "hurtbox"], "unit": "distance", "values": [0.8, 0.33]},
                "not_numeric_authority",
            )
        )

    def test_blocked_or_malformed_values_are_not_scalar_calculation_inputs(self) -> None:
        self.assertFalse(is_scalar_calculation_input(None, "review_required_not_calculation_safe"))
        self.assertFalse(is_scalar_calculation_input({}, ELIGIBLE_STATUS))
        self.assertFalse(is_scalar_calculation_input({"value": -2}, ELIGIBLE_STATUS))
        self.assertFalse(is_scalar_calculation_input({"kind": "unknown", "value": 1}, ELIGIBLE_STATUS))


if __name__ == "__main__":
    unittest.main()
