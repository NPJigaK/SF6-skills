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
                "parsed_numeric_structured": 3,
                "partial_raw_value_coverage": 3,
                "raw_preserved_non_calculation": 6,
                "review_required": 202,
            },
        )
        self.assertEqual(
            payload["calculation_input_status_counts"],
            {
                "annotated_candidate_not_calculation_safe": 3,
                "enum_only_not_arithmetic": 16,
                "not_numeric_authority": 1,
                "out_of_scope_not_emitted": 17,
                "parsed_range_not_single_value_calculation_safe": 2,
                "raw_preserved_not_calculation": 6,
                "review_required_not_calculation_safe": 202,
            },
        )
        self.assertEqual(
            payload["raw_value_variant_decision_counts"],
            {
                "parsed_numeric_structured": 7,
                "review_required": 5,
            },
        )
        self.assertEqual(
            payload["raw_value_variant_calculation_input_status_counts"],
            {
                "annotated_candidate_not_calculation_safe": 7,
                "review_required_not_calculation_safe": 5,
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

    def test_gauge_scalar_unit_does_not_confuse_supercombo_prefix(self) -> None:
        drive_gain = self.records["value-shape:supercombo--unclassified_expression--command_normals--drive_gain"]
        result = classifier.classify_raw_value("1000", drive_gain)
        self.assertEqual(result.parsed_value, {"kind": "gauge_amount", "unit": "drive", "value": 1000})
        self.assertEqual(result.calculation_input_status, "not_numeric_authority")

        drive_damage = self.records["value-shape:supercombo--unclassified_expression--command_normals--drivedmg_blk"]
        result = classifier.classify_raw_value("1000", drive_damage)
        self.assertEqual(result.parsed_value, {"kind": "gauge_amount", "unit": "drive", "value": 1000})

        super_gain = self.records["value-shape:supercombo--unclassified_expression--command_normals--super_gain_hit"]
        result = classifier.classify_raw_value("1000", super_gain)
        self.assertEqual(result.parsed_value, {"kind": "gauge_amount", "unit": "super_art", "value": 1000})

    def test_official_signed_wave_dash_advantage_ranges_parse_but_are_not_calculation_safe(self) -> None:
        block_advantage = self.records[
            "value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb"
        ]
        block_examples = {
            "-12～-1": {"kind": "frame_range", "unit": "frame", "start": -12, "end": -1},
            "-4～-1": {"kind": "frame_range", "unit": "frame", "start": -4, "end": -1},
            "-39～-33": {"kind": "frame_range", "unit": "frame", "start": -39, "end": -33},
        }
        for raw, expected in block_examples.items():
            result = classifier.classify_raw_value(raw, block_advantage)
            self.assertEqual(result.raw_value, raw)
            self.assertEqual(result.parsed_value, expected)
            self.assertEqual(result.value_shape["parser_rule_id"], "frame_range.official_signed_wave_dash.v1")
            self.assertEqual(result.calculation_input_status, "parsed_range_not_single_value_calculation_safe")

        hit_advantage = self.records["value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69"]
        result = classifier.classify_raw_value("-28～-23", hit_advantage)
        self.assertEqual(result.parsed_value, {"kind": "frame_range", "unit": "frame", "start": -28, "end": -23})
        self.assertEqual(result.value_shape["parser_rule_id"], "frame_range.official_signed_wave_dash.v1")
        self.assertEqual(result.calculation_input_status, "parsed_range_not_single_value_calculation_safe")

        for raw in ("-12~-1", "-12--1", "-1～-12"):
            result = classifier.classify_raw_value(raw, block_advantage)
            self.assertEqual(result.value_shape["classifier_status"], "review_required")
            self.assertIsNone(result.parsed_value)

    def test_official_annotated_numeric_candidates_parse_but_are_not_calculation_safe(self) -> None:
        startup = self.records[
            "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100"
        ]
        for raw, expected in {"122※": 122, "128※": 128}.items():
            result = classifier.classify_raw_value(raw, startup)
            self.assertEqual(result.raw_value, raw)
            self.assertEqual(result.value_shape["parser_rule_id"], "annotated_frame.official_suffix_marker.v1")
            self.assertEqual(result.calculation_input_status, "annotated_candidate_not_calculation_safe")
            self.assertEqual(result.parsed_value["kind"], "annotated_numeric_candidate")
            self.assertEqual(
                result.parsed_value["numeric_candidate"],
                {"candidate_type": "unsigned_frame", "unit": "frame", "value": expected},
            )
            self.assertEqual(result.parsed_value["annotation"]["marker_placement"], "suffix")
            self.assertEqual(result.parsed_value["annotation"]["note_marker"], "※")
            self.assertNotIn("value", {k for k in result.parsed_value if k != "numeric_candidate"})

        block_advantage = self.records[
            "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
        ]
        for raw, expected in {"※-4": -4, "※-2": -2}.items():
            result = classifier.classify_raw_value(raw, block_advantage)
            self.assertEqual(result.value_shape["parser_rule_id"], "annotated_signed_frame.official_prefix_marker.negative.v1")
            self.assertEqual(result.calculation_input_status, "annotated_candidate_not_calculation_safe")
            self.assertEqual(result.parsed_value["kind"], "annotated_numeric_candidate")
            self.assertEqual(
                result.parsed_value["numeric_candidate"],
                {"candidate_type": "signed_frame", "unit": "frame", "value": expected},
            )
            self.assertEqual(result.parsed_value["annotation"]["marker_placement"], "prefix")
            self.assertNotEqual(result.parsed_value["kind"], "signed_frame")

        hit_advantage = self.records[
            "value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69"
        ]
        for raw, expected in {"※-3": -3, "※-1": -1, "※-4": -4}.items():
            result = classifier.classify_raw_value(raw, hit_advantage)
            self.assertEqual(result.value_shape["parser_rule_id"], "annotated_signed_frame.official_prefix_marker.negative.v1")
            self.assertEqual(result.parsed_value["numeric_candidate"]["value"], expected)
            self.assertEqual(result.calculation_input_status, "annotated_candidate_not_calculation_safe")

    def test_annotated_slice_keeps_deferred_and_out_of_scope_values_blocked(self) -> None:
        hit_advantage = self.records[
            "value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69"
        ]
        result = classifier.classify_raw_value("※1", hit_advantage)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIsNone(result.parsed_value)

        recovery = self.records["value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef"]
        for raw in ("全体 ※43", "※16"):
            result = classifier.classify_raw_value(raw, recovery)
            self.assertEqual(result.value_shape["classifier_status"], "review_required")
            self.assertIsNone(result.parsed_value)

        startup = self.records[
            "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100"
        ]
        for raw in ("124※", "122*", "*122"):
            result = classifier.classify_raw_value(raw, startup)
            self.assertEqual(result.value_shape["classifier_status"], "review_required")
            self.assertIsNone(result.parsed_value)

        block_advantage = self.records[
            "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
        ]
        for raw in ("※-15", "※-5", "※-10"):
            result = classifier.classify_raw_value(raw, block_advantage)
            self.assertEqual(result.value_shape["classifier_status"], "review_required")
            self.assertIsNone(result.parsed_value)

        sa_gain = self.records["value-shape:official--source_specific_expression--sa"]
        result = classifier.classify_raw_value("※3000", sa_gain)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIsNone(result.parsed_value)

        supercombo_advantage = self.records[
            "value-shape:supercombo--unclassified_expression--command_normals--hit_advantage"
        ]
        result = classifier.classify_raw_value("※-3", supercombo_advantage)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIsNone(result.parsed_value)

    def test_annotated_coverage_records_partial_raw_value_acceptance(self) -> None:
        payload = classifier.build_coverage_payload(disposition=self.disposition)
        hit_record = next(
            record for record in payload["coverage_records"]
            if record["review_item_id"]
            == "value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69"
        )
        self.assertEqual(hit_record["classifier_decision"], "partial_raw_value_coverage")
        self.assertEqual(hit_record["value_shape_classifier_status"], "partial")
        by_raw = {variant["raw_value"]: variant for variant in hit_record["raw_value_variant_coverage"]}
        self.assertEqual(by_raw["※-3"]["classifier_decision"], "parsed_numeric_structured")
        self.assertEqual(by_raw["※-3"]["parsed_value_kind"], "annotated_numeric_candidate")
        self.assertEqual(by_raw["※1"]["classifier_decision"], "review_required")
        self.assertEqual(by_raw["※1"]["parser_rule_ids"], [])

        startup_record = next(
            record for record in payload["coverage_records"]
            if record["review_item_id"]
            == "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100"
        )
        self.assertEqual(startup_record["classifier_decision"], "partial_raw_value_coverage")
        startup_by_raw = {variant["raw_value"]: variant for variant in startup_record["raw_value_variant_coverage"]}
        self.assertEqual(startup_by_raw["122※"]["classifier_decision"], "parsed_numeric_structured")
        self.assertEqual(startup_by_raw["124※"]["classifier_decision"], "review_required")

        block_record = next(
            record for record in payload["coverage_records"]
            if record["review_item_id"]
            == "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
        )
        self.assertEqual(block_record["classifier_decision"], "partial_raw_value_coverage")
        block_by_raw = {variant["raw_value"]: variant for variant in block_record["raw_value_variant_coverage"]}
        self.assertEqual(block_by_raw["※-4"]["classifier_decision"], "parsed_numeric_structured")
        self.assertEqual(block_by_raw["※-15"]["classifier_decision"], "review_required")

    def test_official_signed_wave_dash_slice_does_not_expand_other_parsers(self) -> None:
        note_bearing_advantage = self.records[
            "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
        ]
        result = classifier.classify_raw_value("※-4", note_bearing_advantage)
        self.assertEqual(result.value_shape["parser_rule_id"], "annotated_signed_frame.official_prefix_marker.negative.v1")
        self.assertEqual(result.calculation_input_status, "annotated_candidate_not_calculation_safe")

        active = self.records["value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1"]
        for raw in ("30-34.35", "20-24.25", "23--33"):
            result = classifier.classify_raw_value(raw, active)
            self.assertEqual(result.value_shape["classifier_status"], "review_required")
            self.assertIsNone(result.parsed_value)

        supercombo_advantage = self.records[
            "value-shape:supercombo--unclassified_expression--command_normals--hit_advantage"
        ]
        result = classifier.classify_raw_value("-12～-1", supercombo_advantage)
        self.assertEqual(result.value_shape["classifier_status"], "review_required")
        self.assertIsNone(result.parsed_value)

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
