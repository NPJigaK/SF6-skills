from __future__ import annotations

import unittest
from pathlib import Path

from sf6_knowledge_coach import parsed_value_classifier as classifier


class ParsedValueClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.disposition = classifier.load_disposition()
        cls.records = classifier.disposition_by_review_item_id(cls.disposition)

    def test_build_coverage_payload_covers_disposition_and_policy_counts(self) -> None:
        payload = classifier.build_coverage_payload(disposition=self.disposition)
        self.assertEqual(payload["total_review_items"], 247)
        self.assertEqual(
            payload["classifier_decision_counts"],
            {
                "enum_classified": 16,
                "out_of_scope_first_normalized_export": 17,
                "parsed_numeric_structured": 1,
                "raw_preserved_non_calculation": 6,
                "review_required": 207,
            },
        )
        self.assertEqual(payload["parse_rule_policy_counts"]["timing"], 63)
        self.assertEqual(payload["enum_policy_counts"], {"attribute": 1, "cancel": 6, "defense": 9})
        self.assertTrue(all(payload["system_mechanics_anchors_checked"].values()))
        sa_gain = next(
            record for record in payload["coverage_records"]
            if record["review_item_id"] == "value-shape:official--source_specific_expression--sa"
        )
        self.assertEqual(sa_gain["classifier_decision"], "review_required")
        self.assertEqual(sa_gain["calculation_input_status"], "review_required_not_calculation_safe")

    def test_strict_numeric_values_parse_without_collapsing_complex_shapes(self) -> None:
        block_advantage = self.records["value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"]
        result = classifier.classify_raw_value("-2", block_advantage)
        self.assertEqual(result.value_shape["classifier_status"], "parsed")
        self.assertEqual(result.parsed_value, {"kind": "signed_frame", "unit": "frame", "value": -2})

        active = self.records["value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1"]
        result = classifier.classify_raw_value("6-8", active)
        self.assertEqual(result.parsed_value, {"kind": "frame_range", "unit": "frame", "start": 6, "end": 8})

        damage = self.records["value-shape:official--source_specific_expression--u_202a059d9b1b"]
        result = classifier.classify_raw_value("500", damage)
        self.assertEqual(result.parsed_value, {"kind": "integer", "unit": "damage", "value": 500})

        throw_pair = self.records["value-shape:supercombo--unclassified_expression--character_vitals--throw_range_hurtbox"]
        result = classifier.classify_raw_value("0.8 / 0.33", throw_pair)
        self.assertEqual(result.parsed_value["kind"], "ordered_pair")
        self.assertEqual(result.parsed_value["labels"], ["throw_range", "hurtbox"])
        self.assertEqual(result.parsed_value["values"], [0.8, 0.33])
        self.assertEqual(result.calculation_input_status, "not_numeric_authority")

    def test_supercombo_parsed_coverage_is_not_numeric_authority(self) -> None:
        payload = classifier.build_coverage_payload(disposition=self.disposition)
        supercombo_parsed = [
            record for record in payload["coverage_records"]
            if record["source_name"] == "supercombo" and record["classifier_decision"] == "parsed_numeric_structured"
        ]
        self.assertTrue(supercombo_parsed)
        self.assertTrue(
            all(record["calculation_input_status"] == "not_numeric_authority" for record in supercombo_parsed)
        )

    def test_unsupported_calculation_relevant_values_remain_review_required(self) -> None:
        damage = self.records["value-shape:official--source_specific_expression--u_202a059d9b1b"]
        result = classifier.classify_raw_value("※500", damage)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIn("note marker", result.review_required_reason)

        active = self.records["value-shape:supercombo--unclassified_expression--command_normals--active"]
        result = classifier.classify_raw_value("3(5)3", active)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIn("active-window", result.review_required_reason)

        advantage = self.records["value-shape:supercombo--unclassified_expression--command_normals--hit_advantage"]
        result = classifier.classify_raw_value("KD +27(+30)", advantage)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIn("Parenthesized", result.review_required_reason)

        scaling = self.records["value-shape:official--source_specific_expression--u_55d872f6091a"]
        result = classifier.classify_raw_value("※即時補正10%", scaling)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIn("scaling", result.review_required_reason)

        juggle = self.records["value-shape:supercombo--unclassified_expression--command_normals--juggle_start"]
        result = classifier.classify_raw_value("0/1", juggle)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIn("Juggle", result.review_required_reason)

    def test_enum_classifier_preserves_only_reviewed_source_native_examples(self) -> None:
        official_cancel = self.records["value-shape:official--unclassified_expression--u_bca84ea5c65f"]
        result = classifier.classify_raw_value("SA3", official_cancel)
        self.assertEqual(result.classifier_decision, "enum_classified")
        self.assertEqual(result.parsed_value, {"kind": "enum_token", "tokens": ["SA3"]})

        unknown = classifier.classify_raw_value("SA4", official_cancel)
        self.assertEqual(unknown.value_shape["classifier_status"], "review_required")
        self.assertIn("not in reviewed representative examples", unknown.review_required_reason)

    def test_raw_preserved_and_out_of_scope_dispositions_do_not_parse(self) -> None:
        remarks = self.records["value-shape:official--source_specific_expression--u_80309c573b8b"]
        result = classifier.classify_raw_value("連打キャンセル対応", remarks)
        self.assertEqual(result.classifier_decision, "raw_preserved_non_calculation")
        self.assertIsNone(result.parsed_value)

        out_of_scope = self.records["value-shape:supercombo--unclassified_expression--taunts--damage"]
        result = classifier.classify_raw_value("100x8", out_of_scope)
        self.assertEqual(result.classifier_decision, "out_of_scope_first_normalized_export")
        self.assertEqual(result.value_shape["classifier_status"], "rejected")

    def test_validate_coverage_artifacts_reports_missing_files(self) -> None:
        errors = classifier.validate_coverage_artifacts(
            json_path=Path("missing-parsed-value-classifier-coverage.json"),
            markdown_path=Path("missing-parsed-value-classifier-coverage.md"),
        )
        self.assertTrue(any("Missing" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
