# Apply Value-Shape Source Review Resolutions

Status: Implementation complete; review pending.

## Purpose

Consume the source-review decisions for the 3 previously blocked value-shape
items and update the mapping/disposition artifacts.

## Scope

Update only SuperCombo field mapping, value-shape disposition generation,
their generated public artifacts, tests, and relevant ExecPlan notes. Do not
change schema, parser, normalized export, retrieval, answer behavior, source
acquisition, or authority status.

## Result

- SuperCombo mapping `blocked_pending_human_review`: `1 -> 0`.
- SuperCombo mapping `supercombo_source_specific_field_key`: `274 -> 275`.
- Disposition `blocked_pending_source_review`: `3 -> 0`.
- Disposition `parse_rule_required_before_schema`: `206 -> 208`.
- Disposition `schema_supports_raw_only`: `5 -> 6`.
- JSON Schema redesign remains blocked by parser/classifier and enum policy,
  not source-review blockers.

## Validation

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_supercombo_field_mapping.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_disposition.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_source_review.py
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
```

PLAN deviations: none.
