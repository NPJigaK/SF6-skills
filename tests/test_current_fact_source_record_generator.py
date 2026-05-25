from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from sf6_knowledge_coach.current_fact_candidate_generator import CANDIDATE_JSON_PATH, CANDIDATE_RUN_ID
from sf6_knowledge_coach.current_fact_source_record_generator import (
    CurrentFactSourceRecordGeneratorError,
    build_source_record_input_payload,
    build_source_record_summary_markdown,
)


ROOT = Path(__file__).resolve().parents[1]


def _candidate_payload() -> dict:
    return json.loads((ROOT / CANDIDATE_JSON_PATH).read_text(encoding="utf-8"))


class CurrentFactSourceRecordGeneratorTests(unittest.TestCase):
    def test_builds_source_record_payload_from_candidate_input(self) -> None:
        payload = build_source_record_input_payload(_candidate_payload())

        self.assertEqual(payload["artifact_schema_version"], "current_fact_source_record_input/v1")
        self.assertEqual(payload["run_id"], CANDIDATE_RUN_ID)
        self.assertIn(CANDIDATE_JSON_PATH, payload["generated_from"])
        self.assertEqual(len(payload["records"]), 13)
        self.assertEqual(
            Counter(record["current_fact_record"]["calculation_input_status"] for record in payload["records"]),
            {
                "annotated_candidate_not_calculation_safe": 9,
                "parsed_range_not_single_value_calculation_safe": 4,
            },
        )

    def test_current_fact_record_contains_no_source_record_sidecar_fields(self) -> None:
        payload = build_source_record_input_payload(_candidate_payload())

        for record in payload["records"]:
            current_fact = record["current_fact_record"]
            self.assertTrue(record["source_record_id"].startswith("source-record:"))
            self.assertTrue(current_fact["record_id"].startswith("current-fact:"))
            self.assertNotIn("source_record_id", current_fact)
            self.assertNotIn("source_row_key", current_fact)
            self.assertNotIn("source_cell_key", current_fact)
            self.assertNotIn("source_value_key", current_fact)

    def test_non_scalar_wrappers_are_preserved(self) -> None:
        payload = build_source_record_input_payload(_candidate_payload())
        parsed_by_status = {
            record["current_fact_record"]["calculation_input_status"]: record["current_fact_record"]["parsed_value"]
            for record in payload["records"]
        }

        self.assertEqual(
            parsed_by_status["annotated_candidate_not_calculation_safe"]["kind"],
            "annotated_numeric_candidate",
        )
        self.assertIn("numeric_candidate", parsed_by_status["annotated_candidate_not_calculation_safe"])
        self.assertEqual(
            parsed_by_status["parsed_range_not_single_value_calculation_safe"]["kind"],
            "frame_range",
        )
        self.assertIn("start", parsed_by_status["parsed_range_not_single_value_calculation_safe"])
        self.assertIn("end", parsed_by_status["parsed_range_not_single_value_calculation_safe"])

    def test_candidate_run_id_is_carried_to_source_record_artifact(self) -> None:
        payload = build_source_record_input_payload(_candidate_payload())

        self.assertEqual(payload["run_id"], "20260525T000000Z")
        self.assertNotEqual(payload["run_id"], "20260525")

    def test_rejects_raw_value_expansion_not_in_candidate_input(self) -> None:
        candidate = _candidate_payload()
        mutated = copy.deepcopy(candidate)
        mutated["records"][0]["calculation_input_status"] = "review_required_not_calculation_safe"

        with self.assertRaises(CurrentFactSourceRecordGeneratorError):
            build_source_record_input_payload(mutated)

    def test_summary_is_boundary_only(self) -> None:
        payload = build_source_record_input_payload(_candidate_payload())
        markdown = build_source_record_summary_markdown(payload)

        self.assertIn("Total records: `13`", markdown)
        self.assertIn("not calculation-safe", markdown)
        self.assertNotIn(".local", markdown)
        self.assertNotIn("data/exports/", markdown)


if __name__ == "__main__":
    unittest.main()
