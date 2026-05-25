from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from sf6_knowledge_coach.current_fact_candidate_generator import (
    CANDIDATE_RUN_ID,
    EVIDENCE_JSON_PATH,
    CurrentFactCandidateGeneratorError,
    build_candidate_input_payload,
    build_candidate_summary_markdown,
)


ROOT = Path(__file__).resolve().parents[1]


def _evidence_payload() -> dict:
    return json.loads((ROOT / EVIDENCE_JSON_PATH).read_text(encoding="utf-8"))


class CurrentFactCandidateGeneratorTests(unittest.TestCase):
    def test_builds_candidate_payload_from_reviewed_evidence(self) -> None:
        payload = build_candidate_input_payload(_evidence_payload())

        self.assertEqual(payload["artifact_schema_version"], "current_fact_row_move_cell_candidate_input/v1")
        self.assertEqual(payload["run_id"], CANDIDATE_RUN_ID)
        self.assertIn(EVIDENCE_JSON_PATH, payload["generated_from"])
        self.assertEqual(len(payload["records"]), 13)
        self.assertEqual(
            Counter(record["calculation_input_status"] for record in payload["records"]),
            {
                "annotated_candidate_not_calculation_safe": 9,
                "parsed_range_not_single_value_calculation_safe": 4,
            },
        )

    def test_candidate_records_preserve_non_scalar_wrappers(self) -> None:
        payload = build_candidate_input_payload(_evidence_payload())
        annotated = next(
            record for record in payload["records"]
            if record["calculation_input_status"] == "annotated_candidate_not_calculation_safe"
        )
        frame_range = next(
            record for record in payload["records"]
            if record["calculation_input_status"] == "parsed_range_not_single_value_calculation_safe"
        )

        self.assertEqual(annotated["parsed_value"]["kind"], "annotated_numeric_candidate")
        self.assertIn("numeric_candidate", annotated["parsed_value"])
        self.assertEqual(frame_range["parsed_value"]["kind"], "frame_range")
        self.assertIn("start", frame_range["parsed_value"])
        self.assertIn("end", frame_range["parsed_value"])

    def test_pr365_evidence_identifier_is_reference_only(self) -> None:
        payload = build_candidate_input_payload(_evidence_payload())

        self.assertNotEqual(payload["run_id"], "20260525")
        for record in payload["records"]:
            self.assertEqual(record["evidence"]["public_reference"], EVIDENCE_JSON_PATH)
            self.assertIn(EVIDENCE_JSON_PATH, record["source_review_refs"])
            self.assertEqual(record["evidence"]["evidence_basis"], "source_review_summary")

    def test_unreviewed_raw_value_expansion_is_rejected(self) -> None:
        evidence = _evidence_payload()
        mutated = copy.deepcopy(evidence)
        target = next(record for record in mutated["evidence_records"] if record["raw_value"] == "※-2")
        target["raw_value"] = "※1"

        with self.assertRaises(CurrentFactCandidateGeneratorError):
            build_candidate_input_payload(mutated)

    def test_summary_is_boundary_only(self) -> None:
        evidence = _evidence_payload()
        payload = build_candidate_input_payload(evidence)
        markdown = build_candidate_summary_markdown(payload, evidence)

        self.assertIn("Total records: `13`", markdown)
        self.assertIn("not calculation-safe", markdown)
        self.assertNotIn(".local", markdown)
        self.assertNotIn("data/exports/", markdown)


if __name__ == "__main__":
    unittest.main()
