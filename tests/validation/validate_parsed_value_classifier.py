from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from sf6_knowledge_coach import parsed_value_classifier as classifier


ROOT = Path(__file__).resolve().parents[2]
COVERAGE_JSON = ROOT / "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json"
COVERAGE_MD = ROOT / "docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md"
SCHEMA_DIR = ROOT / "contracts/current-facts"
RECORD_SCHEMA_ID = "https://sf6-knowledge-coach.local/schemas/current-facts/current_fact_record.schema.json"
SIGNED_WAVE_DASH_RULE_ID = "frame_range.official_signed_wave_dash.v1"
SIGNED_WAVE_DASH_CALCULATION_STATUS = "parsed_range_not_single_value_calculation_safe"
ANNOTATED_SUFFIX_RULE_ID = "annotated_frame.official_suffix_marker.v1"
ANNOTATED_NEGATIVE_RULE_ID = "annotated_signed_frame.official_prefix_marker.negative.v1"
ANNOTATED_CALCULATION_STATUS = "annotated_candidate_not_calculation_safe"
SIGNED_WAVE_DASH_TARGET_IDS = {
    "value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb",
    "value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69",
}
ANNOTATED_STARTUP_ID = "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100"
ANNOTATED_BLOCK_ID = "value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"
ANNOTATED_HIT_ID = "value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69"
ANNOTATED_TARGET_IDS = {ANNOTATED_STARTUP_ID, ANNOTATED_BLOCK_ID, ANNOTATED_HIT_ID}
SCHEMA_FILES = [
    "parsed_value.schema.json",
    "value_shape.schema.json",
    "source_reference.schema.json",
    "current_fact_record.schema.json",
]
FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"(?i)(?:^|[\s\"'`])(?:/[a-z0-9_.-]+)+"),
    re.compile(r"(?i)(?:^|[\s\"'`(])[A-Z]:[\\/]"),
    re.compile(r"(?i)\b(?:cookie|authorization|bearer|token|password|secret)\b"),
    re.compile(r"(?i)<html|</html|<!doctype|<table|</table|<tr|</tr|<td|</td|<th|</th"),
    re.compile(r"(?i)\b(?:screenshot|trace|debug dump|answer[-_ ]?log|training[-_ ]?log|private[-_ ]?vault)\b"),
]


def main() -> int:
    errors: list[str] = []
    for path in (COVERAGE_JSON, COVERAGE_MD):
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
    if errors:
        return _finish(errors)

    coverage = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    disposition = classifier.load_disposition()
    policy = classifier.load_policy()
    mechanics = classifier.load_system_mechanics_summary()
    errors.extend(
        classifier.validate_coverage_payload(
            coverage,
            disposition=disposition,
            policy=policy,
            system_mechanics_summary=mechanics,
        )
    )
    rebuilt = classifier.build_coverage_payload(
        disposition=disposition,
        policy=policy,
        system_mechanics_summary=mechanics,
    )
    if coverage != rebuilt:
        errors.append("coverage artifact is not the deterministic classifier output")
    rendered = classifier.render_coverage_markdown(coverage)
    if COVERAGE_MD.read_text(encoding="utf-8") != rendered:
        errors.append("coverage markdown is not the deterministic classifier rendering")
    _validate_signed_wave_dash_slice(coverage, errors)
    _validate_annotated_official_slice(coverage, errors)
    errors.extend(_validate_current_fact_compatible_outputs(disposition))
    _scan_public_files([COVERAGE_JSON, COVERAGE_MD], errors)
    return _finish(errors)


def _validate_signed_wave_dash_slice(coverage: dict[str, Any], errors: list[str]) -> None:
    if coverage.get("classifier_decision_counts", {}).get("parsed_numeric_structured") != 3:
        errors.append("parsed_numeric_structured count must include only signed ranges and pre-existing parsed coverage")
    if coverage.get("classifier_decision_counts", {}).get("partial_raw_value_coverage") != 3:
        errors.append("partial_raw_value_coverage count must be 3 for double-check-limited annotated variants")
    if coverage.get("classifier_decision_counts", {}).get("review_required") != 202:
        errors.append("review_required count must reflect only approved signed-range and annotated parser changes")

    calculation_counts = coverage.get("calculation_input_status_counts", {})
    if calculation_counts.get(SIGNED_WAVE_DASH_CALCULATION_STATUS) != 2:
        errors.append(f"{SIGNED_WAVE_DASH_CALCULATION_STATUS} count must be 2")
    if calculation_counts.get(ANNOTATED_CALCULATION_STATUS) != 3:
        errors.append(f"{ANNOTATED_CALCULATION_STATUS} count must be 3")
    if calculation_counts.get("review_required_not_calculation_safe") != 202:
        errors.append("review_required_not_calculation_safe count must be 202")
    if calculation_counts.get("not_numeric_authority") != 1:
        errors.append("not_numeric_authority count must remain 1")

    records = coverage.get("coverage_records", [])
    by_id = {record.get("review_item_id"): record for record in records if isinstance(record, dict)}
    for review_item_id in SIGNED_WAVE_DASH_TARGET_IDS:
        record = by_id.get(review_item_id)
        if record is None:
            errors.append(f"Missing signed wave-dash target coverage record: {review_item_id}")
            continue
        if record.get("source_name") != "official":
            errors.append(f"{review_item_id} must remain official")
        if record.get("source_role") != "authority_candidate":
            errors.append(f"{review_item_id} must remain authority_candidate")
        if record.get("classifier_decision") != "parsed_numeric_structured":
            errors.append(f"{review_item_id} must be parsed_numeric_structured")
        if record.get("calculation_input_status") != SIGNED_WAVE_DASH_CALCULATION_STATUS:
            errors.append(f"{review_item_id} must not be single-value calculation-safe")
        if record.get("parser_rule_ids") != [SIGNED_WAVE_DASH_RULE_ID]:
            errors.append(f"{review_item_id} must use only {SIGNED_WAVE_DASH_RULE_ID}")

    extra_rule_records = [
        record.get("review_item_id")
        for record in records
        if isinstance(record, dict)
        and SIGNED_WAVE_DASH_RULE_ID in record.get("parser_rule_ids", [])
        and record.get("review_item_id") not in SIGNED_WAVE_DASH_TARGET_IDS
    ]
    if extra_rule_records:
        errors.append(f"{SIGNED_WAVE_DASH_RULE_ID} leaked outside target groups: {extra_rule_records[:3]}")

    unsafe_official_ranges = [
        record.get("review_item_id")
        for record in records
        if isinstance(record, dict)
        and record.get("source_name") == "official"
        and SIGNED_WAVE_DASH_RULE_ID in record.get("parser_rule_ids", [])
        and record.get("calculation_input_status") == "eligible_only_after_domain_source_and_unit_checks"
    ]
    if unsafe_official_ranges:
        errors.append(f"official signed ranges must not be calculation-eligible: {unsafe_official_ranges[:3]}")


def _validate_annotated_official_slice(coverage: dict[str, Any], errors: list[str]) -> None:
    if coverage.get("artifact_schema_version") != "parsed_value_classifier_coverage/v2":
        errors.append("annotated raw-value partial coverage requires coverage schema v2")
    if coverage.get("raw_value_variant_decision_counts") != {
        "parsed_numeric_structured": 7,
        "review_required": 5,
    }:
        errors.append("raw value variant decision counts must distinguish 7 double-checked candidates and 5 blocked variants")
    if coverage.get("raw_value_variant_calculation_input_status_counts") != {
        ANNOTATED_CALCULATION_STATUS: 7,
        "review_required_not_calculation_safe": 5,
    }:
        errors.append("raw value variant calculation counts must keep annotated candidates non-calculation-safe")

    records = coverage.get("coverage_records", [])
    by_id = {record.get("review_item_id"): record for record in records if isinstance(record, dict)}
    expected = {
        ANNOTATED_STARTUP_ID: ("partial_raw_value_coverage", [ANNOTATED_SUFFIX_RULE_ID], ["122※", "128※"]),
        ANNOTATED_BLOCK_ID: (
            "partial_raw_value_coverage",
            [ANNOTATED_NEGATIVE_RULE_ID],
            ["※-4", "※-2"],
        ),
        ANNOTATED_HIT_ID: ("partial_raw_value_coverage", [ANNOTATED_NEGATIVE_RULE_ID], ["※-3", "※-1", "※-4"]),
    }
    for review_item_id, (decision, parser_rules, parsed_raw_values) in expected.items():
        record = by_id.get(review_item_id)
        if record is None:
            errors.append(f"Missing annotated target coverage record: {review_item_id}")
            continue
        if record.get("source_name") != "official" or record.get("source_role") != "authority_candidate":
            errors.append(f"{review_item_id} must remain official authority_candidate")
        if record.get("classifier_decision") != decision:
            errors.append(f"{review_item_id} classifier_decision must be {decision}")
        if record.get("parser_rule_ids") != parser_rules:
            errors.append(f"{review_item_id} parser rules must be {parser_rules}")
        if record.get("calculation_input_status") != ANNOTATED_CALCULATION_STATUS:
            errors.append(f"{review_item_id} must use {ANNOTATED_CALCULATION_STATUS}")
        variants = record.get("raw_value_variant_coverage", [])
        by_raw = {variant.get("raw_value"): variant for variant in variants if isinstance(variant, dict)}
        for raw_value in parsed_raw_values:
            variant = by_raw.get(raw_value)
            if variant is None:
                errors.append(f"{review_item_id} missing parsed variant {raw_value}")
                continue
            if variant.get("classifier_decision") != "parsed_numeric_structured":
                errors.append(f"{review_item_id} {raw_value} must be parsed")
            if variant.get("parsed_value_kind") != "annotated_numeric_candidate":
                errors.append(f"{review_item_id} {raw_value} must use annotated_numeric_candidate")
            if variant.get("calculation_input_status") != ANNOTATED_CALCULATION_STATUS:
                errors.append(f"{review_item_id} {raw_value} must not be calculation-safe")

    blocked_variants = {
        ANNOTATED_STARTUP_ID: ["124※"],
        ANNOTATED_BLOCK_ID: ["※-15", "※-5", "※-10"],
        ANNOTATED_HIT_ID: ["※1"],
    }
    for review_item_id, raw_values in blocked_variants.items():
        record = by_id.get(review_item_id, {})
        variants = {
            variant.get("raw_value"): variant
            for variant in record.get("raw_value_variant_coverage", [])
            if isinstance(variant, dict)
        }
        for raw_value in raw_values:
            blocked = variants.get(raw_value)
            if blocked is None:
                errors.append(f"{review_item_id} partial coverage must include blocked {raw_value}")
            elif blocked.get("classifier_decision") != "review_required" or blocked.get("parser_rule_ids") != []:
                errors.append(f"{raw_value} must remain blocked with no parser rule")

    blocked_ids = {
        "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef",
        "value-shape:official--source_specific_expression--sa",
        "value-shape:official--source_specific_expression--u_55d872f6091a",
        "value-shape:official--source_specific_expression--u_202a059d9b1b",
        "value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1",
    }
    for review_item_id in blocked_ids:
        record = by_id.get(review_item_id)
        if record is None:
            errors.append(f"Missing blocked annotated-slice exclusion record: {review_item_id}")
            continue
        if record.get("classifier_decision") != "review_required":
            errors.append(f"{review_item_id} must remain review_required")
        if record.get("parser_rule_ids"):
            errors.append(f"{review_item_id} must not gain annotated parser rules")


def _validate_current_fact_compatible_outputs(disposition: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    schemas = _load_schemas(errors)
    if errors:
        return errors
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )
    validator = Draft202012Validator(schemas[SCHEMA_DIR / "current_fact_record.schema.json"], registry=registry)
    by_id = classifier.disposition_by_review_item_id(disposition)
    examples = [
        _record(
            "classifier:official:jp_001_5lp:block_advantage",
            "official",
            "authority_candidate",
            "authority_candidate",
            "jp",
            "jp_001_5lp",
            "block_advantage",
            "advantage",
            ["硬直差", "ガード"],
            "ガード",
            "ガード硬直差",
            classifier.classify_raw_value(
                "-2",
                by_id["value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb"],
            ),
        ),
        _record(
            "classifier:official:jp_001_5lp:cancel",
            "official",
            "authority_candidate",
            "authority_candidate",
            "jp",
            "jp_001_5lp",
            "cancel",
            "cancel",
            ["キャンセル"],
            "キャンセル",
            "キャンセル",
            classifier.classify_raw_value(
                "SA3",
                by_id["value-shape:official--unclassified_expression--u_bca84ea5c65f"],
            ),
        ),
        _record(
            "classifier:supercombo:jp:vitals:throw_range_hurtbox",
            "supercombo",
            "enrichment_candidate",
            "enrichment_candidate",
            "jp",
            None,
            "supercombo_throw_range_hurtbox_pair",
            "throw",
            ["Character Vitals", "Throw Range / Hurtbox"],
            "Throw Range / Hurtbox",
            "SuperCombo Throw Range / Hurtbox",
            classifier.classify_raw_value(
                "0.8 / 0.33",
                by_id["value-shape:supercombo--unclassified_expression--character_vitals--throw_range_hurtbox"],
            ),
        ),
        _record(
            "classifier:official:jp_001_5lp:combo_scaling",
            "official",
            "authority_candidate",
            "authority_candidate",
            "jp",
            "jp_001_5lp",
            "combo_scaling",
            "scaling",
            ["コンボ補正値"],
            "コンボ補正値",
            "コンボ補正値",
            classifier.classify_raw_value(
                "※即時補正10%",
                by_id["value-shape:official--source_specific_expression--u_55d872f6091a"],
            ),
        ),
        _record(
            "classifier:official:kimberly_special:startup_annotated",
            "official",
            "authority_candidate",
            "authority_candidate",
            "kimberly",
            "kimberly_special",
            "startup",
            "timing",
            ["動作フレーム", "発生"],
            "発生",
            "発生",
            classifier.classify_raw_value(
                "122※",
                by_id[ANNOTATED_STARTUP_ID],
            ),
        ),
        _record(
            "classifier:official:chunli_serenity:block_advantage_annotated",
            "official",
            "authority_candidate",
            "authority_candidate",
            "chunli",
            "chunli_serenity",
            "block_advantage",
            "advantage",
            ["硬直差", "ガード"],
            "ガード",
            "ガード硬直差",
            classifier.classify_raw_value(
                "※-4",
                by_id[ANNOTATED_BLOCK_ID],
            ),
        ),
    ]
    for record in examples:
        failures = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        if failures:
            errors.append(f"classifier output should fit current-fact record schema: {failures[0].message}")
    return errors


def _record(
    record_id: str,
    source_name: str,
    source_role: str,
    authority_status: str,
    character_slug: str,
    move_id: str | None,
    field_key: str,
    source_family: str,
    source_header_path: list[str],
    source_label: str,
    display_label_ja: str,
    result: classifier.ClassificationResult,
) -> dict[str, Any]:
    payload = {
        "authority_status": authority_status,
        "character_slug": character_slug,
        "display_label_ja": display_label_ja,
        "evidence": {
            "evidence_basis": "value_shape_policy",
            "public_reference": "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json",
            "run_id": classifier.RUN_ID,
            "source_header_path": source_header_path,
            "source_label": source_label,
            "source_name": source_name,
            "source_role": source_role,
        },
        "field_key": field_key,
        "move_id": move_id,
        "record_id": record_id,
        "source_family": source_family,
        "source_header_path": source_header_path,
        "source_label": source_label,
        "source_name": source_name,
        "source_role": source_role,
    }
    payload.update(result.current_fact_fields())
    return payload


def _load_schemas(errors: list[str]) -> dict[Path, dict[str, Any]]:
    schemas: dict[Path, dict[str, Any]] = {}
    for name in SCHEMA_FILES:
        path = SCHEMA_DIR / name
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        schemas[path] = json.loads(path.read_text(encoding="utf-8"))
    return schemas


def _scan_public_files(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PUBLIC_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)} contains forbidden public content")
                break


def _finish(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Parsed-value classifier validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
