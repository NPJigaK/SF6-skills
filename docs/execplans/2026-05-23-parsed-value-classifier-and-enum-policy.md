# Parsed-Value Classifier And Enum Policy

Status: Implementation complete; review pending.

## Purpose

Convert the remaining value-shape disposition blockers into reviewed
schema-design policy inputs.

## Scope

Add Markdown/JSON policy artifacts and a validator. Do not implement parser,
classifier, JSON Schema, normalized export, retrieval, answer behavior, or
authority promotion.

## Result

- Covers all 208 `parse_rule_required_before_schema` records by semantic
  family.
- Covers all 16 `source_specific_enum_required` records by semantic family.
- Marks JSON Schema redesign as ready to start after this policy is reviewed.
- Keeps parser/classifier implementation as later work.

## Validation

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_policy.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_disposition.py
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
```

PLAN deviations: none.
