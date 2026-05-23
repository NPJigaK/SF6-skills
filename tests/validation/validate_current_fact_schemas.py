from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "contracts/current-facts"
FIXTURE_DIR = ROOT / "tests/fixtures/current-facts"
RECORD_SCHEMA_ID = "https://sf6-knowledge-coach.local/schemas/current-facts/current_fact_record.schema.json"
EXPORT_SCHEMA_ID = "https://sf6-knowledge-coach.local/schemas/current-facts/current_fact_export.schema.json"
SCHEMA_FILES = [
    "parsed_value.schema.json",
    "value_shape.schema.json",
    "source_reference.schema.json",
    "current_fact_record.schema.json",
    "current_fact_export.schema.json",
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
    schemas = _load_schemas(errors)
    if errors:
        return _finish(errors)

    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )
    for path, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # pragma: no cover - message matters more than exception type here
            errors.append(f"{path.relative_to(ROOT)} is not a valid Draft 2020-12 schema: {exc}")

    record_validator = Draft202012Validator(schemas[SCHEMA_DIR / "current_fact_record.schema.json"], registry=registry)
    export_validator = Draft202012Validator(schemas[SCHEMA_DIR / "current_fact_export.schema.json"], registry=registry)
    _validate_valid_fixtures(record_validator, FIXTURE_DIR / "records/valid", errors)
    _validate_invalid_fixtures(record_validator, FIXTURE_DIR / "records/invalid", errors)
    _validate_valid_fixtures(export_validator, FIXTURE_DIR / "exports/valid", errors)
    _scan_public_files([*schemas, *FIXTURE_DIR.rglob("*.json")], errors)
    return _finish(errors)


def _load_schemas(errors: list[str]) -> dict[Path, dict[str, Any]]:
    schemas: dict[Path, dict[str, Any]] = {}
    for name in SCHEMA_FILES:
        path = SCHEMA_DIR / name
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        schemas[path] = json.loads(path.read_text(encoding="utf-8"))
        if schemas[path].get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)} must use JSON Schema Draft 2020-12")
    return schemas


def _validate_valid_fixtures(validator: Draft202012Validator, directory: Path, errors: list[str]) -> None:
    fixtures = sorted(directory.glob("*.json"))
    if not fixtures:
        errors.append(f"Missing valid fixtures under {directory.relative_to(ROOT)}")
    for path in fixtures:
        payload = json.loads(path.read_text(encoding="utf-8"))
        failures = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
        if failures:
            errors.append(f"{path.relative_to(ROOT)} should be valid: {failures[0].message}")


def _validate_invalid_fixtures(validator: Draft202012Validator, directory: Path, errors: list[str]) -> None:
    fixtures = sorted(directory.glob("*.json"))
    if not fixtures:
        errors.append(f"Missing invalid fixtures under {directory.relative_to(ROOT)}")
    for path in fixtures:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not list(validator.iter_errors(payload)):
            errors.append(f"{path.relative_to(ROOT)} should be rejected")


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
    print("Current-fact schema validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
