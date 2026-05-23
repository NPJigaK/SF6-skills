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
    errors.extend(_validate_current_fact_compatible_outputs(disposition))
    _scan_public_files([COVERAGE_JSON, COVERAGE_MD], errors)
    return _finish(errors)


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
