# Current-Fact Row/Move/Cell Candidate Schema

Status: Drafted for review; validation passed.

## Purpose

Plan the schema, synthetic fixtures, focused validator, and validator audit
entries for `current_fact_row_move_cell_candidate_input/v1`.

This plan follows the reviewed row/move/cell candidate input boundary. It does
not implement candidate artifact generation and does not create production
source-record or current-fact export artifacts.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`
- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`
- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`
- `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/validation/validate_current_fact_source_records.py`
- `tests/validation/validate_current_fact_consumer_guards.py`
- `tests/validation/validate_current_fact_export_generator.py`
- `tests/validation/validate_validator_test_audit.py`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

The repository has:

- `current_fact_record.schema.json`;
- `current_fact_source_record_input/v1` schema and synthetic fixtures;
- `current_fact_export/v2` schema;
- guard tests for non-scalar parsed values;
- a fixture-contract current-fact export generator.

PR #361 planned the intermediate reviewed public candidate input that should
map public row/move/cell evidence to lookup-ready current-fact-like records.
That plan intentionally did not implement a schema or fixtures. The next safe
step is a contract-only implementation slice: schema, synthetic fixtures,
focused validator, and validator audit entries.

## Scope

Included in this docs-only plan:

- define exact files for the future schema/fixture/validator implementation;
- define the artifact schema version and high-level schema requirements;
- define synthetic valid and invalid fixture coverage;
- define focused validator behavior;
- define validator audit updates;
- preserve summary-safe, parsed-value-only, non-scalar guard, and source
  boundary rules.

Excluded:

- No schema implementation in this docs-only PR.
- No fixture implementation in this docs-only PR.
- No validator implementation in this docs-only PR.
- No candidate artifact generation.
- No production source-record artifact generation.
- No production current-fact export artifact generation.
- No generated artifact under `data/current-facts/`.
- No generated summary under `docs/current-facts/`.
- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier behavior change.
- No parser/classifier expansion.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No source acquisition implementation.
- No live acquisition.
- No authority promotion.

## Planned Files

Future implementation may touch only these files unless mandatory review
approves an amendment.

Schema:

- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`

Synthetic fixtures:

- `tests/fixtures/current-facts/candidate-inputs/valid/current_fact_row_move_cell_candidate_input_minimal.json`
- `tests/fixtures/current-facts/candidate-inputs/valid/current_fact_row_move_cell_candidate_input_non_scalar_values.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_legacy_generated_from.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_review_required_record.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_missing_parsed_value.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_flattened_annotated_candidate.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_collapsed_frame_range.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_supercombo_scalar_authority.json`
- `tests/fixtures/current-facts/candidate-inputs/invalid/current_fact_row_move_cell_candidate_input_private_or_local_reference.json`

Validator:

- `tests/validation/validate_current_fact_row_move_cell_candidates.py`

Existing validators, only if required for inventory or compatibility:

- `tests/validation/validate_clean_slate.py`
- `tests/validation/validate_current_fact_schemas.py`

Validator audit artifacts:

- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

ExecPlan progress update:

- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md`

## Schema Requirements

The future schema must define:

- `artifact_schema_version == "current_fact_row_move_cell_candidate_input/v1"`;
- `run_id` using the existing timestamp format;
- `generated_from` as committed public artifact paths only;
- `authority_boundary`;
- `candidate_boundary`;
- `records`.

The schema must reject:

- legacy `data/exports/` paths;
- `.local` paths;
- raw HTML markers;
- screenshot or VLM authority references;
- local absolute paths;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, answer logs,
  training logs, or private-data markers;
- SuperCombo scalar numeric authority;
- lookup-ready records without `parsed_value`;
- `review_required_not_calculation_safe`;
- `out_of_scope_not_emitted`;
- flattened `annotated_numeric_candidate`;
- collapsed `frame_range`.

Each candidate record must include:

- `candidate_record_id`;
- `character_slug`;
- `move_id`;
- `field_key`;
- `display_label_ja`;
- `source_row_key`;
- `source_cell_key`;
- `source_value_key`;
- `source_row_order`;
- `source_cell_order`;
- `source_header_path`;
- `raw_value`;
- `raw_value_length`;
- `raw_value_sha256`;
- `source_name`;
- `source_role`;
- `source_family`;
- `source_label`;
- `authority_status`;
- `evidence`;
- `source_review_refs`;
- `coverage_refs`;
- `acquisition_report_refs`;
- `parsed_value`;
- `value_shape`;
- `parser_rule_ids`;
- `calculation_input_status`.

The schema may reuse definitions from existing current-fact schemas through
`$ref` where practical. The future implementation should avoid duplicating the
full parsed-value schema if a direct `$ref` is sufficient.

## Fixture Strategy

All fixtures in the future implementation are synthetic contract fixtures.
They prove shape and boundary behavior; they do not prove source truth.

Valid fixtures:

- minimal official scalar candidate with
  `eligible_only_after_domain_source_and_unit_checks`;
- official `annotated_numeric_candidate` with
  `annotated_candidate_not_calculation_safe`;
- official `frame_range` with
  `parsed_range_not_single_value_calculation_safe`.

Invalid fixtures:

- legacy `data/exports/<character>/official_raw.json` in `generated_from`;
- `.local` or local/private path in `generated_from`, evidence, or refs;
- screenshot/VLM reference used as authority;
- raw HTML/full row marker in a public field;
- review-required candidate with no lookup-ready parsed value;
- missing `parsed_value`;
- `annotated_numeric_candidate` flattened to `signed_frame` or `integer`;
- `frame_range` collapsed to a scalar;
- SuperCombo candidate with scalar authority status;
- official candidate promoted beyond `authority_candidate`.

Fixtures must not contain raw HTML, full rows, screenshots, local paths,
cookies, profiles, traces, debug dumps, logs, ChatGPT output, or private data.

## Validator Requirements

The future focused validator should be evidence-first and concise.

It should:

- load the candidate schema with the existing current-fact schema registry
  pattern;
- validate every valid fixture;
- assert every invalid fixture fails;
- check `raw_value_length` and `raw_value_sha256` consistency;
- check `source_header_path` consistency between source identity fields and
  evidence, if modeled separately;
- check public reference boundaries for `generated_from`, evidence refs,
  source-review refs, coverage refs, and acquisition report refs;
- check no candidate fixture uses legacy raw export paths;
- check no candidate fixture uses `.local`, raw HTML, screenshots/VLM as
  authority, local paths, cookies, profiles, traces, debug dumps, logs, or
  private-data markers;
- check non-scalar guard behavior for `annotated_numeric_candidate` and
  `frame_range`;
- check blocked/review-required records are absent from valid lookup-ready
  fixtures;
- check no production candidate artifacts exist under
  `data/current-facts/candidate-inputs/` or
  `docs/current-facts/candidate-inputs/` as part of this implementation slice.

The validator must not weaken existing source-record, export, or guard
validators to fit candidate fixtures.

## Validator Audit Requirements

The future implementation must update validator audit artifacts when adding
new tests or validators.

Expected audit entries:

- `tests/validation/validate_current_fact_row_move_cell_candidates.py`
  - evidence class: synthetic contract plus privacy/source-boundary contract;
  - boundary: candidate input contract only, not source truth.
- Candidate fixture directory:
  - evidence class: synthetic contract;
  - boundary: shape and privacy checks only.

The audit must state that candidate fixtures are not source truth and do not
authorize production artifact generation, runtime lookup, answer behavior, or
authority promotion.

## Issue #343 Gate

Issue #343 remains required for future value-handling decisions.

The schema/fixture/validator implementation should use synthetic fixtures
only. It must not introduce new raw official value semantics. If a later
candidate artifact implementation includes new raw-value handling or
same-grammar expansion, the Issue #343 screenshot plus ChatGPT/VLM
double-check gate must complete before implementation approval.

ChatGPT/VLM output remains `observation_candidate` only. It is not source
truth, validator evidence, parser/schema approval, calculation-safe
promotion, or numeric authority.

## Acceptance Criteria

- The plan is docs-only.
- The plan defines exact schema, fixture, validator, audit, and ExecPlan files
  for the future implementation.
- Future fixtures are synthetic contract fixtures only.
- The plan does not authorize candidate artifact generation.
- The plan does not authorize production source-record or current-fact export
  artifact generation.
- The plan rejects legacy raw exports as replacement source input.
- The plan preserves summary-safe boundaries.
- The plan preserves parsed-value-only admission.
- The plan keeps review-required/no parsed-value records out of lookup-ready
  valid fixtures.
- The plan preserves `annotated_numeric_candidate` and `frame_range`
  non-scalar guard boundaries.
- The plan keeps Issue #343 double-check gate mandatory for future
  value-handling decisions.
- The plan does not change runtime lookup, `current_facts.py`, `answering.py`,
  parser/classifier behavior, retrieval, answer, calculator, SymPy, source
  acquisition, or live acquisition.

## Files / Interfaces

This docs-only PR should change only:

- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md`

Future implementation plans may touch the files listed in Planned Files only
after mandatory review approval.

## Validation Commands

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-25: Drafted docs-only schema/fixtures/validator/audit plan after
  PR #361 merged. No implementation or generated artifact changes included.
- 2026-05-25: Ran validation commands. They passed with only this new
  ExecPlan file untracked.

## Decision Log

- 2026-05-25: Candidate input gets a dedicated schema named
  `current_fact_row_move_cell_candidate_input/v1`.
- 2026-05-25: First implementation slice is contract-only with synthetic
  fixtures; production candidate artifacts remain blocked.
- 2026-05-25: Valid lookup-ready candidate fixtures must require
  `parsed_value`.
- 2026-05-25: Review-required/no parsed-value records belong in invalid
  fixtures and remain out of valid lookup-ready candidate fixtures.

## Deviations

- None.

## Risks

- Future schema implementation may uncover field naming conflicts with
  existing source-record schema conventions.
- Synthetic fixtures will not prove source truth.
- Production candidate artifact generation remains blocked until a separate
  reviewed public input implementation plan is approved.
- Runtime remains legacy raw export backed.
- First production coverage may be limited by parsed-value-only admission.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only schema/fixture/validator plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md` | `git diff --check` | Pass | None | Mandatory review pending | Schema implementation not started |
| Runtime and artifact boundary | No runtime, schema, validator, or generated artifact changes | Same | `git status --short --branch` | Pass; one untracked ExecPlan file only | None | Mandatory review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only.
- It defines exact schema file path, fixture paths, validator path, and audit files.
- It uses synthetic contract fixtures only.
- It does not authorize candidate artifact generation.
- It does not authorize production source-record artifact generation.
- It does not authorize production current-fact export artifact generation.
- It does not change runtime lookup, current_facts.py, answering.py, parser/classifier behavior, retrieval, answer, calculator, SymPy, source acquisition, or live acquisition.
- Summary-safe boundaries are preserved.
- Legacy data/exports/*/official_raw.json is rejected as replacement source input.
- Parsed-value-only admission is preserved.
- review_required/no parsed_value records stay out of valid lookup-ready candidate fixtures.
- annotated_numeric_candidate and frame_range non-scalar guard boundaries are preserved.
- Issue #343 double-check gate remains required for future value-handling decisions.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining risks, and whether docs-only stage/commit is approved.
```
