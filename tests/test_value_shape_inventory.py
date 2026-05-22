from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from sf6_knowledge_coach.value_shape_inventory import (
    MAX_PUBLIC_RAW_VALUE_CHARS,
    RUN_ID,
    SHAPE_CLASSES,
    SUMMARY_SCHEMA_VERSION,
    build_inventory,
    classify_value,
    validate_inventory_artifacts,
    validate_inventory_payload,
)


def _public_example(raw_value: str) -> dict:
    return {
        "raw_value": raw_value,
        "raw_value_excerpt": raw_value,
        "raw_value_sha256": "sha256:" + sha256(raw_value.encode("utf-8")).hexdigest(),
        "raw_value_length": len(raw_value),
        "raw_value_truncated": False,
    }


def _valid_inventory() -> dict:
    return {
        "artifact_schema_version": SUMMARY_SCHEMA_VERSION,
        "run_id": RUN_ID,
        "acquisition_report": "docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md",
        "inventory_status": "reviewed_summary",
        "artifact_boundary": "summarized_inventory_only",
        "authority_status": "inventory_only_not_authority",
        "source_families": ["official", "supercombo"],
        "source_family_summaries": [],
        "shape_vocabulary": SHAPE_CLASSES,
        "examples_per_field_limit": 5,
        "public_raw_value_max_chars": MAX_PUBLIC_RAW_VALUE_CHARS,
        "field_shape_summaries": [
            {
                "source_family": "official",
                "source_role": "current_fact_authority_candidate",
                "source_label": "発生",
                "source_header_path": ["動作フレーム", "発生"],
                "character_count": 1,
                "row_or_cell_count": 1,
                "shape_counts": {shape: 0 for shape in SHAPE_CLASSES},
                "representative_examples": [
                    {
                        **_public_example("6+0"),
                        "character_slug": "jp",
                        "source_family": "official",
                        "source_label": "発生",
                        "source_header_path": ["動作フレーム", "発生"],
                        "shape_classes": ["plus_expression"],
                        "example_scope": "bounded_representative",
                    }
                ],
            },
            {
                "source_family": "supercombo",
                "source_role": "enrichment_candidate",
                "source_label": "Startup",
                "source_header_path": ["Normals", "Startup"],
                "character_count": 1,
                "row_or_cell_count": 1,
                "shape_counts": {shape: 0 for shape in SHAPE_CLASSES},
                "representative_examples": [],
            },
        ],
        "review_item_summary": {
            "grouped_count": 0,
            "emitted_count": 0,
            "omitted_count": 0,
            "truncated": False,
            "blocker_for_json_schema_redesign": False,
        },
        "review_items": [],
        "source_boundary": {
            "raw_html_public_commit": "forbidden",
            "full_raw_rows_public_commit": "forbidden",
            "full_source_table_public_commit": "forbidden",
            "local_artifacts_public_commit": "forbidden",
        },
        "authority_boundary": {
            "official": "authority_candidate_only_not_current_fact_authority",
            "supercombo": "enrichment_cross_reference_candidate_only",
            "parsed_values": "not_emitted",
        },
        "input_report_summary": {},
    }


class ValueShapeInventoryTests(unittest.TestCase):
    def test_classifies_official_special_shapes_without_numeric_meaning(self) -> None:
        self.assertIn("plus_expression", classify_value("6+0"))
        self.assertIn("hidden_detail", classify_value("10-23 10-14, 20-23", hidden_detail="10-14, 20-23"))
        self.assertIn("until_landing", classify_value("着地まで"))
        self.assertIn("note_separated_alternate", classify_value("2200※1850"))
        self.assertIn("percent_expression", classify_value("始動補正20％"))

    def test_validate_inventory_payload_rejects_authority_promotion(self) -> None:
        inventory = _valid_inventory()
        inventory["authority_status"] = "current_fact_authority"
        errors = validate_inventory_payload(inventory)
        self.assertIn("authority_status must be inventory_only_not_authority", errors)
        self.assertIn("inventory must not claim current_fact_authority", errors)

    def test_validate_inventory_payload_rejects_silent_review_item_truncation(self) -> None:
        inventory = _valid_inventory()
        inventory["review_items"] = [
            {
                "kind": "source_specific_expression",
                "source_family": "official",
                "source_label": "発生",
                "source_header_path": ["動作フレーム", "発生"],
                "affected_count": 1,
                "examples": [_public_example("122※")],
                "review_question": "Review deterministic classification before schema/parser work.",
            }
        ]
        inventory["review_item_summary"] = {
            "grouped_count": 1,
            "emitted_count": 0,
            "omitted_count": 1,
            "truncated": True,
            "blocker_for_json_schema_redesign": True,
        }
        errors = validate_inventory_payload(inventory)
        self.assertIn("review_item_summary.emitted_count must be 1", errors)
        self.assertIn("review_item_summary.omitted_count must be 0", errors)
        self.assertIn("review_item_summary.truncated must be False", errors)

    def test_validate_inventory_payload_rejects_uncapped_long_raw_example(self) -> None:
        inventory = _valid_inventory()
        long_value = "x" * (MAX_PUBLIC_RAW_VALUE_CHARS + 1)
        inventory["field_shape_summaries"][0]["representative_examples"][0] = {
            **_public_example(long_value),
            "character_slug": "jp",
            "source_family": "official",
            "source_label": "発生",
            "source_header_path": ["動作フレーム", "発生"],
            "shape_classes": ["prose"],
            "example_scope": "bounded_representative",
        }
        errors = validate_inventory_payload(inventory)
        self.assertIn(
            "field_shape_summaries[0].representative_examples[0].raw_value must not exceed the public limit",
            errors,
        )

    def test_validate_inventory_artifacts_rejects_raw_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_path = root / "inventory.json"
            markdown_path = root / "inventory.md"
            json_path.write_text(json.dumps(_valid_inventory(), ensure_ascii=False), encoding="utf-8")
            markdown_path.write_text("<html><table><tr><td>raw</td></tr></table></html>", encoding="utf-8")
            with self.assertRaises(ValueError) as context:
                validate_inventory_artifacts(json_path=json_path, markdown_path=markdown_path)
            self.assertIn("forbidden public inventory content", str(context.exception))

    def test_build_inventory_blocks_when_local_artifacts_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_workspace = Path(tmp) / "missing"
            with self.assertRaises(FileNotFoundError):
                build_inventory(workspace=missing_workspace)


if __name__ == "__main__":
    unittest.main()
