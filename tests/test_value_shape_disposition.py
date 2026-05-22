from __future__ import annotations

import copy
import unittest

from sf6_knowledge_coach import value_shape_disposition as disposition


class ValueShapeDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = disposition.load_inventory()
        cls.mapping = disposition.load_supercombo_mapping()
        cls.payload = disposition.build_disposition_summary()

    def test_build_disposition_summary_covers_all_review_items(self) -> None:
        self.assertEqual(self.payload["total_review_items"], 247)
        self.assertEqual(self.payload["inventory_source_family_counts"], {"official": 16, "supercombo": 231})
        self.assertEqual(sum(self.payload["disposition_counts"].values()), 247)
        self.assertEqual(self.payload["supercombo_mapping_dependency_count"], 231)

    def test_build_disposition_summary_preserves_boundaries(self) -> None:
        for record in self.payload["dispositions"]:
            self.assertNotIn("source_family", record)
            self.assertIn(record["inventory_source_family"], {"official", "supercombo"})
            self.assertNotIn("parsed_value", record)
            if record["inventory_source_family"] == "official":
                self.assertEqual(record["source_role"], "authority_candidate")
                self.assertIsNone(record["supercombo_mapping_dependency"])
            else:
                self.assertIn(record["source_role"], {"enrichment_candidate", "cross_reference_candidate"})
                self.assertIsNotNone(record["supercombo_mapping_dependency"])

    def test_validate_rejects_missing_disposition_record(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["dispositions"].pop()
        errors = disposition.validate_disposition_payload(payload, inventory=self.inventory, mapping=self.mapping)
        self.assertTrue(any("exactly 247" in error for error in errors), errors)
        self.assertTrue(any("missing review item dispositions" in error for error in errors), errors)

    def test_validate_rejects_source_family_identity_field(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["dispositions"][0]["source_family"] = payload["dispositions"][0]["inventory_source_family"]
        errors = disposition.validate_disposition_payload(payload, inventory=self.inventory, mapping=self.mapping)
        self.assertTrue(any("inventory_source_family, not source_family" in error for error in errors), errors)

    def test_validate_rejects_supercombo_authority_promotion(self) -> None:
        payload = copy.deepcopy(self.payload)
        supercombo_record = next(record for record in payload["dispositions"] if record["source_name"] == "supercombo")
        supercombo_record["source_role"] = "current_fact_authority"
        errors = disposition.validate_disposition_payload(payload, inventory=self.inventory, mapping=self.mapping)
        self.assertTrue(any("enrichment/cross-reference/candidate" in error for error in errors), errors)
        self.assertTrue(any("current_fact_authority" in error for error in errors), errors)

    def test_validate_rejects_long_public_raw_value(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["dispositions"][0]["representative_examples"][0]["raw_value"] = "x" * 121
        errors = disposition.validate_disposition_payload(payload, inventory=self.inventory, mapping=self.mapping)
        self.assertTrue(any("raw_value must not exceed public limit" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
