from __future__ import annotations

import copy
import unittest

from sf6_knowledge_coach import supercombo_field_mapping as mapping


class SuperComboFieldMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = mapping.load_inventory()
        cls.payload = mapping.build_mapping_summary()

    def test_build_mapping_summary_covers_expected_counts(self) -> None:
        self.assertEqual(self.payload["total_supercombo_field_summaries"], 403)
        self.assertEqual(
            self.payload["mapping_status_counts"],
            {
                "maps_to_existing_official_field_key": 80,
                "supercombo_source_specific_field_key": 274,
                "enrichment_only_no_current_fact_mapping": 10,
                "out_of_scope_first_normalized_export": 38,
                "blocked_pending_human_review": 1,
            },
        )
        self.assertEqual(self.payload["source_role_counts"], {"cross_reference_candidate": 80, "enrichment_candidate": 323})

    def test_validate_rejects_missing_mapping_record(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mappings"].pop()
        errors = mapping.validate_mapping_payload(payload, inventory=self.inventory)
        self.assertTrue(any("exactly 403" in error for error in errors), errors)
        self.assertTrue(any("missing SuperCombo source_header_path" in error for error in errors), errors)

    def test_validate_rejects_authority_promotion(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mappings"][0]["authority_status"] = "current_fact_authority"
        errors = mapping.validate_mapping_payload(payload, inventory=self.inventory)
        self.assertTrue(any("must not claim current_fact_authority" in error for error in errors), errors)

    def test_validate_rejects_status_rule_violation(self) -> None:
        payload = copy.deepcopy(self.payload)
        record = next(
            item
            for item in payload["mappings"]
            if item["mapping_status"] == "enrichment_only_no_current_fact_mapping"
        )
        record["proposed_field_key"] = "notes"
        errors = mapping.validate_mapping_payload(payload, inventory=self.inventory)
        self.assertTrue(any("proposed_field_key must be null" in error for error in errors), errors)

    def test_validate_rejects_multiple_status_field(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mappings"][0]["mapping_statuses"] = [payload["mappings"][0]["mapping_status"]]
        errors = mapping.validate_mapping_payload(payload, inventory=self.inventory)
        self.assertTrue(any("exactly one mapping_status" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
