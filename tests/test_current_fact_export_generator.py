from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from sf6_knowledge_coach.current_fact_export_generator import (
    CurrentFactExportGeneratorError,
    build_current_fact_export,
    validate_current_fact_export_payload,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_RECORD_FIXTURE_DIR = ROOT / "tests/fixtures/current-facts/source-records"
SOURCE_RECORD_ONLY_FIELDS = {
    "raw_value_length",
    "raw_value_sha256",
    "source_cell_key",
    "source_cell_order",
    "source_record_id",
    "source_row_key",
    "source_row_order",
    "source_value_key",
}


def _fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CurrentFactExportGeneratorTests(unittest.TestCase):
    def test_builds_current_fact_export_from_minimal_source_record_fixture(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_minimal.json")

        export_payload = build_current_fact_export(source_payload)

        self.assertEqual(export_payload["artifact_schema_version"], "current_fact_export/v2")
        self.assertEqual(export_payload["run_id"], source_payload["run_id"])
        self.assertEqual(export_payload["authority_boundary"], source_payload["authority_boundary"])
        self.assertEqual(export_payload["generated_from"], sorted(source_payload["generated_from"]))
        self.assertEqual(len(export_payload["records"]), 1)
        self.assertEqual(validate_current_fact_export_payload(export_payload), [])

    def test_source_record_sidecar_fields_do_not_leak_into_export_records(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_minimal.json")

        export_payload = build_current_fact_export(source_payload)

        for record in export_payload["records"]:
            self.assertFalse(SOURCE_RECORD_ONLY_FIELDS & set(record))

    def test_non_scalar_parsed_values_remain_wrapped(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_non_scalar_values.json")

        export_payload = build_current_fact_export(source_payload)
        parsed_by_status = {
            record["calculation_input_status"]: record["parsed_value"]
            for record in export_payload["records"]
        }

        self.assertEqual(
            parsed_by_status["annotated_candidate_not_calculation_safe"]["kind"],
            "annotated_numeric_candidate",
        )
        self.assertIn(
            "numeric_candidate",
            parsed_by_status["annotated_candidate_not_calculation_safe"],
        )
        self.assertEqual(
            parsed_by_status["parsed_range_not_single_value_calculation_safe"]["kind"],
            "frame_range",
        )
        self.assertEqual(
            parsed_by_status["parsed_range_not_single_value_calculation_safe"],
            {"kind": "frame_range", "unit": "frame", "start": 6, "end": 8},
        )

    def test_output_ordering_is_deterministic(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_non_scalar_values.json")
        source_payload["records"] = list(reversed(source_payload["records"]))

        export_payload = build_current_fact_export(source_payload)

        self.assertEqual(
            [record["field_key"] for record in export_payload["records"]],
            ["block_advantage", "active"],
        )

    def test_invalid_source_record_fixtures_are_rejected(self) -> None:
        for path in sorted((SOURCE_RECORD_FIXTURE_DIR / "invalid").glob("*.json")):
            with self.subTest(path=path.name):
                with self.assertRaises(CurrentFactExportGeneratorError):
                    build_current_fact_export(_fixture(path))

    def test_source_record_identity_mismatches_are_rejected(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_minimal.json")
        source_payload["records"][0]["raw_value_sha256"] = "0" * 64

        with self.assertRaises(CurrentFactExportGeneratorError):
            build_current_fact_export(source_payload)

    def test_export_validation_rejects_flattened_annotated_candidate(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_non_scalar_values.json")
        export_payload = build_current_fact_export(source_payload)
        flattened = copy.deepcopy(export_payload)
        annotated = next(
            record for record in flattened["records"]
            if record["calculation_input_status"] == "annotated_candidate_not_calculation_safe"
        )
        annotated["parsed_value"] = {"kind": "signed_frame", "unit": "frame", "value": -4}

        errors = validate_current_fact_export_payload(flattened)

        self.assertTrue(any("annotated status must keep annotated_numeric_candidate" in error for error in errors))

    def test_export_validation_rejects_collapsed_frame_range(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_non_scalar_values.json")
        export_payload = build_current_fact_export(source_payload)
        collapsed = copy.deepcopy(export_payload)
        frame_range = next(
            record for record in collapsed["records"]
            if record["calculation_input_status"] == "parsed_range_not_single_value_calculation_safe"
        )
        frame_range["parsed_value"] = {"kind": "signed_frame", "unit": "frame", "value": 6}

        errors = validate_current_fact_export_payload(collapsed)

        self.assertTrue(any("range status must keep frame_range wrapper" in error for error in errors))

    def test_export_validation_rejects_legacy_generated_from(self) -> None:
        source_payload = _fixture(SOURCE_RECORD_FIXTURE_DIR / "valid/current_fact_source_record_input_minimal.json")
        export_payload = build_current_fact_export(source_payload)
        export_payload["generated_from"] = ["data/exports/jp/official_raw.json"]

        errors = validate_current_fact_export_payload(export_payload)

        self.assertTrue(any("data/exports" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
