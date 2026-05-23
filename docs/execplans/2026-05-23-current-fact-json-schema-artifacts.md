# Current-Fact JSON Schema Artifacts

Status: Implemented and locally reviewed; PR pending.

## Purpose

Implement the first structural JSON Schema artifacts for normalized
current-fact records, following
`docs/execplans/2026-05-23-current-fact-json-schema-redesign.md`.

This step creates schema contracts, small fixtures, and a validator. It does
not implement parsing, normalized export generation, retrieval, answer
behavior, or authority promotion.

## Scope

Included:

- Add Draft 2020-12 JSON Schemas for:
  - `current_fact_record`
  - `parsed_value`
  - `value_shape`
  - `source_reference`
  - `current_fact_export`
- Add minimal valid and invalid fixtures.
- Add a deterministic schema validator.
- Add a schema review note.
- Update validator/test evidence audit for the new validator.

Excluded:

- No parser/classifier implementation.
- No generated normalized current-fact export.
- No source acquisition or live web access.
- No retrieval DB changes.
- No answer behavior changes.
- No SuperCombo numeric authority promotion.
- No new dependencies.

## Acceptance Criteria

- All schema files use `https://json-schema.org/draft/2020-12/schema`.
- Schemas validate against the Draft 2020-12 meta-schema using the locked
  `jsonschema` package already present in `uv.lock`.
- Valid fixtures pass.
- Invalid fixtures fail for the intended boundaries:
  - `source_family` cannot be source identity.
  - SuperCombo cannot be promoted to numeric authority.
- The validator scans public schema/fixture files for local paths, raw HTML,
  source dumps, screenshots, secrets, logs, and private data markers.
- The new validator is recorded in the validator/test evidence audit.
- Existing repo validators and unit tests pass.

## Files / Interfaces

Added:

- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/source_reference.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `tests/fixtures/current-facts/records/valid/*.json`
- `tests/fixtures/current-facts/records/invalid/*.json`
- `tests/fixtures/current-facts/exports/valid/*.json`
- `tests/validation/validate_current_fact_schemas.py`
- `docs/schema-reviews/20260521T025403Z-current-fact-json-schema-redesign.md`
- `docs/execplans/2026-05-23-current-fact-json-schema-artifacts.md`

Updated:

- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`
- `tests/validation/validate_clean_slate.py`

## Validation Commands

Run from repository root:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
for script in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$script"; done
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Created implementation branch
  `impl/current-fact-json-schema-artifacts`.
- [x] (2026-05-23 JST) Confirmed `jsonschema` is available through
  `uv run --locked` without adding dependencies.
- [x] (2026-05-23 JST) Added schema artifacts.
- [x] (2026-05-23 JST) Added focused fixtures for official and SuperCombo
  boundaries.
- [x] (2026-05-23 JST) Added schema validator and validator audit entry.
- [x] (2026-05-23 JST) Narrowly updated clean-slate validation to allow only
  `contracts/current-facts/` schema files, without restoring legacy
  `contracts/` content.
- [x] (2026-05-23 JST) Marked SuperCombo schema fixtures as synthetic
  contract fixtures so they are not mistaken for source truth.
- [x] (2026-05-23 JST) Completed validation:
  `git diff --check`,
  `uv lock --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py`,
  validator loop,
  `PYTHONPATH=src uv run --locked python -m unittest discover -s tests`,
  and JP 5LP daily-answer smoke.
- [x] (2026-05-23 JST) Completed local reviewer check: no parser,
  classifier implementation, normalized export, retrieval, answer behavior, or
  authority promotion was added.

## Decision Log

- Decision: Use the locked `jsonschema` package rather than adding a new
  dependency.
  Rationale: `jsonschema` is already available in `uv.lock`; adding
  dependencies would expand scope.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep fixtures small and contract-focused.
  Rationale: Full source rows and raw HTML belong in ignored source acquisition
  artifacts, not schema fixture commits.
  Date/Author: 2026-05-23 / Codex

- Decision: Record the schema validator as `synthetic_contract` evidence in
  the validator audit.
  Rationale: Passing schema fixtures proves contract shape, not source truth or
  parser correctness.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- The schemas are first structural contracts and may need refinement when
  parser implementation starts.
- Fixture values are small contract examples. Official examples are
  source-derived smoke fixtures; SuperCombo examples are synthetic and are not
  source facts.
- The schemas do not make official data current-fact authority and do not make
  SuperCombo numeric authority.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Add schema artifacts | Added five Draft 2020-12 schemas | `contracts/current-facts/*.schema.json` | `validate_current_fact_schemas.py` | Pass | None | PR review pending | Parser work may require later refinements |
| Add fixtures | Added small valid/invalid fixtures | `tests/fixtures/current-facts/` | `validate_current_fact_schemas.py` | Pass | None | PR review pending | Fixtures are contract examples only |
| Preserve clean-slate boundary | Allowed only `contracts/current-facts/` schemas | `validate_clean_slate.py` | `validate_clean_slate.py` | Pass | None | PR review pending | Future contracts surfaces need explicit plans |
| Preserve evidence rigor | Added validator audit entry | validator audit JSON/MD | `validate_validator_test_audit.py` | Pass | None | PR review pending | Validator must not be treated as source truth |
