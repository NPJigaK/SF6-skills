# Current-Fact Lookup Parity And Rollback

Status: Drafted for review; validation passed.

## Purpose

Plan the parity and rollback criteria required before any runtime lookup switch
from legacy `data/exports/<character>/official_raw.json` to the reviewed
production `current_fact_export/v2` artifact.

This plan must not switch `current_facts.py`, `answering.py`, retrieval,
answers, parsers, classifiers, calculators, or source acquisition. It defines
what must be true before a future runtime switch can be safely considered, and
what must cause an immediate rollback if a future switch is attempted.

## Draft PR Flow

Use the same draft PR flow as PR #365 through PR #368:

1. Commit this docs-only plan and open a draft PR.
2. Complete mandatory plan review.
3. Add implementation commits to the same draft PR only if this plan is
   amended to authorize a validator-only implementation and mandatory plan
   review passes.
4. Complete mandatory implementation review.
5. Ready and merge only after the relevant review passes.

The plan-only draft PR must not be merged if the reviewer requires an
implementation slice in the same PR.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `docs/execplans/2026-05-25-current-fact-export-artifact-from-source-records.md`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `data/current-facts/20260525T000000Z-current-fact-export.json`
- `docs/current-facts/20260525T000000Z-current-fact-export.md`
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- `data/exports/jp/official_raw.json` as legacy comparison input only
- current validator audit artifacts

## Context

Current runtime lookup behavior is still legacy raw export backed:

- `current_facts.py` loads `data/exports/<character>/official_raw.json`;
- `lookup_current_fact(character_slug, move_input, field)` normalizes
  `move_input` to uppercase, scans records by `input`, and returns the field
  value directly from the raw record;
- returned evidence reports `authority == "data/exports official_raw"` and a
  legacy raw export `source_path`;
- `answering.py` calls `lookup_current_fact` for numeric/current-fact queries
  and formats the returned raw value as an answered packet.

The reviewed production current-fact export now exists:

- `data/current-facts/20260525T000000Z-current-fact-export.json`;
- artifact schema `current_fact_export/v2`;
- 13 records total;
- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`;
- 0 scalar eligible records;
- all records remain official `authority_candidate`.

Because all 13 export records are non-scalar and not calculation-safe, they
cannot be used as exact scalar answers. Parity must therefore distinguish:

- lookup identity and evidence parity that can be validated now;
- answer-value parity that is expected to fail or be held for non-scalar
  current-fact records;
- runtime switch criteria that remain blocked until exact-answer behavior,
  fallback behavior, and rollback behavior are reviewed.

## Scope

Included in this docs-only plan:

- inventory current legacy lookup and answer behavior;
- define comparison surfaces between legacy raw-backed lookup and the reviewed
  production current-fact export;
- define expected parity, non-parity, and hold cases;
- define rollback criteria for any future runtime lookup switch;
- define guard requirements for `annotated_numeric_candidate` and
  `frame_range`;
- define future validator-only implementation slices if review approves them;
- keep runtime lookup unchanged.

Excluded:

- No runtime lookup switch.
- No `current_facts.py` behavior change.
- No `answering.py` behavior change.
- No retrieval implementation.
- No answer implementation.
- No parser/classifier behavior change.
- No parser/classifier expansion.
- No calculator implementation.
- No SymPy logic.
- No source acquisition implementation.
- No live acquisition.
- No legacy raw export retirement.
- No authority promotion.
- No calculation-safe promotion.
- No Issue #343 raw-value expansion.

## Comparison Inputs And Boundaries

Allowed comparison inputs:

- `data/current-facts/20260525T000000Z-current-fact-export.json`;
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`;
- current-fact JSON Schemas and guard helpers;
- `data/exports/jp/official_raw.json` only as the current legacy runtime
  comparison surface, not as replacement source input and not as proof that the
  reviewed export should add or promote facts.

Forbidden as authority or replacement input:

- legacy `data/exports/*/official_raw.json` for new reviewed export records;
- ignored `.local` artifacts;
- raw HTML;
- full rows;
- screenshots as authority;
- ChatGPT/VLM output as authority;
- cookies;
- browser profiles;
- request/response headers;
- tokens;
- traces;
- debug dumps;
- logs;
- answer logs;
- training logs;
- private data;
- SuperCombo numeric authority.

## Parity Criteria

Parity checks must be explicit about what is being compared.

Required export invariants:

- production export is schema-valid `current_fact_export/v2`;
- production export has `run_id == "20260525T000000Z"`;
- production export has exactly 13 records;
- `generated_from` points only to
  `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`;
- every record has `parsed_value`;
- every record has top-level `calculation_input_status`;
- all records remain official `authority_candidate`;
- `annotated_numeric_candidate` remains wrapped;
- `frame_range` remains a range;
- `current_fact_guards.is_scalar_calculation_input` rejects all 13 records;
- source-record sidecar fields do not appear in export records.

Required legacy comparison inventory:

- enumerate which export records can be mapped to a legacy raw record by
  character, move identity, raw value, source header/field context, or another
  deterministic reviewed key;
- record which export records have no deterministic legacy lookup key because
  current legacy lookup is input/field-oriented while export records are
  row/move/cell-record-oriented;
- record whether any future lookup compatibility requires an alias/input
  bridge and whether that bridge is reviewed or missing.

Required answer behavior parity:

- current legacy lookup may answer raw scalar-looking values directly;
- reviewed export records must not produce exact scalar answers because all 13
  records are non-scalar and not calculation-safe;
- for the 13 reviewed records, a future export-backed runtime should hold or
  display non-scalar metadata with caveat only after a separate answer behavior
  ExecPlan approves that behavior;
- no parity test may treat an `annotated_numeric_candidate` nested numeric
  candidate or `frame_range` endpoint as a scalar answer.

## Expected Non-Parity

The following gaps are expected and must not be papered over:

- legacy lookup is keyed by `character_slug`, `move_input`, and field name;
- production export records are keyed by `record_id`, `move_id`, field key, and
  source/evidence metadata;
- legacy raw records include broad current raw fields; production export
  contains only 13 reviewed parsed records;
- legacy raw values can be returned as answer text; production export values
  are all non-scalar/not calculation-safe and cannot be exact scalar answers;
- `authority` and evidence strings differ by design;
- no current production export record is `eligible_only_after_domain_source_and_unit_checks`.

These expected gaps mean a runtime switch is not approved by this plan.

## Rollback Criteria

Any future runtime lookup switch must include rollback conditions before it is
approved. At minimum, rollback is required if:

- answered packet count changes for existing legacy-covered smoke queries
  without an approved expected-gap entry;
- numeric/current-fact queries that should hold begin answering without
  deterministic scalar-safe evidence;
- `annotated_numeric_candidate` is flattened into `signed_frame`, `integer`, or
  exact scalar answer text;
- `frame_range` is collapsed into a single frame value, endpoint, best/worst,
  or scalar advantage without a reviewed range-aware contract;
- `calculation_input_status` is missing or ignored;
- official `authority_candidate` is promoted to current-fact authority without
  review;
- legacy raw exports are silently used as replacement source input;
- private/local evidence paths or reviewer observations appear in runtime
  evidence;
- answer packet evidence changes from deterministic reviewed data to raw
  unreviewed paths;
- CI or local validators fail.

## Guard Requirements

Any future lookup implementation must prove:

- it carries `calculation_input_status` through the lookup path;
- it calls `current_fact_guards.is_scalar_calculation_input` or an equivalent
  validator before exact scalar answer use;
- it rejects all 13 current export records for scalar calculation/exact-answer
  use;
- it preserves `parsed_value.kind`;
- it does not flatten `annotated_numeric_candidate`;
- it does not collapse `frame_range`;
- it preserves source/evidence/authority fields;
- it can fall back to legacy behavior only under an explicitly reviewed
  fallback contract;
- it can be disabled or reverted without deleting reviewed export artifacts.

## Future Implementation Slices

This docs-only plan does not authorize implementation by itself unless the
mandatory plan review explicitly approves a validator-only implementation
commit in the same draft PR.

Possible future validator-only implementation in this same draft PR:

- add a focused parity/rollback validator such as
  `tests/validation/validate_current_fact_lookup_parity.py`;
- compare the production export artifact with selected legacy raw lookup
  behavior without changing runtime code;
- assert the export has 13 records and zero scalar-eligible records;
- assert non-scalar guard rejection for all export records;
- assert expected non-parity is recorded rather than treated as a failure;
- assert no runtime lookup, answer, parser/classifier, retrieval, calculator,
  SymPy, source acquisition, live acquisition, or legacy raw retirement files
  changed.

Any helper, fixture, or validator file not listed in an amended file list
requires ExecPlan amendment and mandatory review before editing.

## Acceptance Criteria

- PR begins as docs-only and remains draft after plan review.
- Runtime lookup remains unchanged.
- `current_facts.py` remains unchanged.
- `answering.py` remains unchanged.
- No parser/classifier behavior change.
- No retrieval, answer, calculator, SymPy, source acquisition, or live
  acquisition changes.
- Legacy raw exports are not retired.
- Parity criteria, expected non-parity, rollback criteria, and guard
  requirements are explicit.
- All 13 production export records remain non-scalar and not calculation-safe.
- Issue #343 gate remains required for future raw-value expansion.

## Files / Interfaces

Plan-only initial PR should change only:

- `docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md`

Possible future implementation commits in the same draft PR may change only
after mandatory plan review explicitly approves implementation:

- `docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md`
- a focused parity validator under `tests/validation/` if approved
- validator audit JSON/MD if a validator is added or changed

Any additional file requires ExecPlan amendment and mandatory review before
implementation continues.

## Validation Commands

Plan-only validation:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

Implementation validation, if a later implementation is approved:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-26: Drafted plan after PR #368 merged. No runtime lookup switch,
  validator implementation, or legacy raw export retirement yet.
- 2026-05-26: Ran plan-only validation. All checks passed.

## Decision Log

- 2026-05-26: Runtime lookup switch remains blocked until parity criteria,
  expected gaps, rollback behavior, and guard behavior are reviewed.
- 2026-05-26: The production current-fact export is a reviewed artifact, but
  not an exact-answer runtime source yet.
- 2026-05-26: The 13 current export records must be treated as non-scalar and
  not calculation-safe for parity purposes.
- 2026-05-26: Legacy raw exports may be compared as the current runtime surface
  but must not become replacement source input for reviewed export records.

## Deviations

- None.

## Risks

- Runtime remains legacy raw export backed.
- A future lookup switch may require an input/alias bridge because legacy
  lookup is input-oriented and current export records are row/move/cell-record
  oriented.
- Parity may be mostly expected non-parity until scalar-safe reviewed records
  exist.
- Legacy raw export retirement remains future work.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lookup parity/rollback plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md` | `git diff --check`; `uv lock --check` | Pass | None | Mandatory review pending | Runtime remains legacy raw export backed |
| Runtime boundary | Plan excludes runtime lookup and answer behavior changes | Same | current-fact validators | Pass | None | Mandatory review pending | Future switch still needs review |
| Guard boundary | Plan requires non-scalar guard rejection for all 13 export records | Same | `validate_current_fact_consumer_guards.py`; `validate_current_fact_export_generator.py` | Pass | None | Mandatory review pending | No scalar-safe export records yet |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md.

Check:
- PR diff initially contains exactly one ExecPlan file.
- Plan compares current legacy raw-backed lookup behavior with the reviewed
  production current-fact export artifact.
- Plan defines parity criteria, expected non-parity, rollback criteria, and
  guard requirements.
- Runtime lookup remains unchanged.
- No current_facts.py / answering.py behavior switch is planned.
- No parser/classifier, retrieval, answer, calculator, SymPy, source/live
  acquisition changes are planned.
- Legacy raw exports are not retired.
- Legacy data/exports/*/official_raw.json is comparison input only, not
  replacement source input.
- All 13 export records remain non-scalar / not calculation-safe.
- Issue #343 double-check gate remains required for future raw-value expansion.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether docs-only plan is approved for same-PR implementation or
docs-only merge.
```
