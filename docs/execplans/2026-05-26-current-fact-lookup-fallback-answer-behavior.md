# Current-Fact Lookup Fallback And Answer Behavior

Status: Drafted for review; validation passed.

## Purpose

Plan the fallback and answer-behavior contract required before any runtime
lookup switch from legacy `data/exports/<character>/official_raw.json` to the
reviewed production `current_fact_export/v2` artifact.

The production current-fact export exists, and lookup parity/rollback validation
exists, but all 13 reviewed export records are non-scalar and not
calculation-safe. This plan therefore does not switch runtime lookup. It fixes
what a future export-backed lookup may return, when it must hold, and which
legacy raw retirement blockers remain.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- Issue #343 roadmap
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/current-facts/20260525T000000Z-current-fact-export.json`
- `docs/current-facts/20260525T000000Z-current-fact-export.md`
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- `data/exports/jp/official_raw.json` as current legacy comparison surface only
- current current-fact validators

## Context

The current runtime path is still legacy raw-backed:

- `current_facts.py` uses `AUTHORITY_DATASET == "official_raw"`;
- `lookup_current_fact(character_slug, move_input, field)` loads
  `data/exports/<character>/official_raw.json`;
- lookup matches the legacy `input` field and returns raw field values;
- returned evidence reports `authority == "data/exports official_raw"`;
- `answering.py` calls `lookup_current_fact` for deterministic numeric/current
  fact answers and formats the raw value into answer text.

The reviewed production current-fact export has:

- `artifact_schema_version == "current_fact_export/v2"`;
- `run_id == "20260525T000000Z"`;
- `generated_from` containing only
  `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`;
- 13 records total;
- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`;
- 0 records with `eligible_only_after_domain_source_and_unit_checks`;
- all records still official `authority_candidate`.

The lookup parity validator intentionally fixed expected non-parity: the legacy
JP raw lookup surface is input/field-oriented and has 61 JP records, while the
production export is row/move/cell-record-oriented and currently has no scalar
eligible records. A direct runtime switch would either lose answer coverage or
risk answering with non-scalar data.

## Scope

Included in this docs-only plan:

- define future export-backed lookup result states;
- define exact-answer hold behavior for non-scalar parsed values;
- define when legacy raw fallback may remain active;
- define how answer packets may represent hold, fallback, and non-scalar
  metadata in a future PR;
- list legacy raw retirement blockers;
- define future implementation slices and validators.

Excluded:

- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier behavior change.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No source acquisition.
- No live acquisition.
- No schema change.
- No fixture change.
- No generated artifact change.
- No legacy raw export retirement.
- No calculation-safe, numeric authority, or current-fact authority promotion.

## Decision

The next implementation must not be a runtime switch. The next safe direction is
to plan answer/fallback semantics first, then add validators or helper code in
later PRs.

This plan chooses the fallback/answer-behavior branch before legacy raw
retirement because retirement depends on a reviewed answer contract. Legacy raw
exports stay technical debt, but they remain the current runtime surface until a
replacement can answer, hold, or fall back predictably.

## Future Lookup Result States

A future export-backed lookup must distinguish at least these states:

- `exact_scalar_available`: a reviewed current-fact record has a parsed value
  and `current_fact_guards.is_scalar_calculation_input(parsed_value,
  calculation_input_status)` returns true, and source/domain/unit/authority
  checks pass.
- `non_scalar_metadata_only`: a reviewed record exists, but parsed value kind or
  `calculation_input_status` blocks exact scalar use. Current production export
  records all fall into this class.
- `reviewed_record_missing`: no reviewed export record matches the requested
  character/move/field identity.
- `legacy_fallback_used`: legacy raw-backed lookup answered because the future
  fallback contract explicitly allowed it for the query and no reviewed export
  answer was available.
- `hold_no_safe_answer`: no exact scalar answer is allowed, and fallback is not
  available or not approved for that query.

These states are planning labels. They must not be introduced as public runtime
API without a later implementation ExecPlan.

## Non-Scalar Answer Behavior

For `annotated_numeric_candidate` and `frame_range` records:

- exact scalar answer status must be `hold`;
- nested numeric candidates must not be flattened into `integer` or
  `signed_frame`;
- `frame_range` endpoints must not be collapsed to one frame value, best/worst,
  midpoint, or scalar advantage;
- answer text must not present the nested number or endpoint as the exact fact;
- evidence may point to reviewed current-fact export records only after a later
  answer behavior PR defines the packet shape;
- display/search metadata may be shown only with a caveat that the value is not
  calculation-safe and not exact scalar answerable.

The current 13 production export records are therefore not replacements for
legacy scalar answers.

## Fallback Contract Direction

A future transition should keep legacy raw fallback until the replacement path
can cover current deterministic answer behavior or explicitly document expected
gaps.

Allowed future fallback direction:

- export-backed exact scalar answer wins only when scalar guard, authority,
  source, domain, and unit checks pass;
- export-backed non-scalar records produce hold or metadata-only results, never
  exact scalar answers;
- legacy raw fallback may remain available for existing smoke queries only under
  a reviewed fallback contract;
- fallback evidence must clearly label legacy raw source as legacy technical
  debt, not reviewed current-fact export authority;
- no fallback path may use legacy raw exports to create new reviewed export
  records.

Forbidden future fallback behavior:

- silently preferring legacy raw when a reviewed non-scalar record exists and
  the user asked for an exact scalar fact without documenting the hold/fallback
  decision;
- treating legacy raw answer text as authority promotion;
- combining legacy raw values with parsed export metadata to infer new facts;
- using `.local`, screenshots, ChatGPT/VLM output, raw HTML, full rows, private
  paths, logs, cookies, profiles, traces, or debug dumps as runtime evidence.

## Legacy Raw Retirement Blockers

Legacy raw export retirement remains blocked until all of the following are
reviewed:

- an export-backed lookup identity model maps user query context to reviewed
  `record_id` / `character_slug` / `move_id` / `field_key` records;
- an input/alias bridge exists if legacy `move_input` behavior must be
  preserved;
- exact scalar answer behavior exists for at least one scalar-safe reviewed
  record class;
- non-scalar hold/metadata behavior is reviewed for `annotated_numeric_candidate`
  and `frame_range`;
- rollback criteria cover answered packet count, answer text, evidence strings,
  fallback behavior, and authority/status changes;
- daily-answer evidence remains deterministic and reviewed;
- `validate_current_fact_lookup_parity.py` is replaced or amended because it
  currently fixes the legacy JP raw count and source-text markers as transition
  boundary checks.

## Future Implementation Slices

Recommended sequence:

1. Docs-only answer/fallback behavior plan. This file.
2. Validator-only blocker inventory update.
   Check that the current production export has zero scalar-safe records, that
   legacy fallback remains the only current answer path, and that retirement is
   still blocked.
3. Export-backed lookup helper plan.
   Define an internal helper that reads production export and returns the result
   states above without changing `answering.py`.
4. Helper implementation behind tests.
   No answer behavior change; no legacy retirement.
5. Answer packet behavior plan.
   Decide hold/metadata/fallback packet shapes and evidence strings.
6. Runtime switch implementation only if scalar-safe records and fallback
   behavior are approved.
7. Legacy raw retirement plan only after replacement lookup is validated and
   rollback is proven.

## Acceptance Criteria

- This PR is docs-only.
- Runtime lookup remains unchanged.
- `current_facts.py` remains unchanged.
- `answering.py` remains unchanged.
- No schema, fixture, generated artifact, parser/classifier, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition change is included.
- Legacy raw exports are not retired.
- The plan states that all 13 current export records are non-scalar and not
  calculation-safe.
- The plan keeps Issue #343 double-check gate required for future value-handling
  decisions.

## Files / Interfaces

This docs-only PR changes only:

- `docs/execplans/2026-05-26-current-fact-lookup-fallback-answer-behavior.md`

Any implementation, validator, schema, fixture, generated artifact, runtime, or
legacy retirement change requires a later ExecPlan or an amendment plus
mandatory review.

## Validation Commands

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_lookup_parity.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-26: Drafted plan after PR #369 merged. No runtime lookup, answer
  behavior, validator, schema, fixture, generated artifact, or legacy raw
  retirement change.
- 2026-05-26: Ran docs-only validation. All checks passed.

## Decision Log

- 2026-05-26: Chose fallback/answer behavior planning before legacy raw
  retirement because current production export has zero scalar-safe records.
- 2026-05-26: Legacy raw exports remain technical debt, but they stay as the
  current runtime surface until replacement lookup and answer behavior are
  reviewed.
- 2026-05-26: Export-backed non-scalar records must hold or display metadata
  only; they must not replace exact scalar answers.

## Deviations

- None.

## Risks

- Runtime remains legacy raw export backed.
- Production export has no scalar-safe records yet.
- Legacy raw retirement remains blocked.
- A future input/alias bridge may be required before lookup parity can improve.
- The current parity validator intentionally fixes legacy JP raw count and
  source-text markers, so it will need amendment or replacement during runtime
  switch or retirement work.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fallback/answer behavior plan | Draft plan only | `docs/execplans/2026-05-26-current-fact-lookup-fallback-answer-behavior.md` | `git diff --check`; `uv lock --check` | Pass | None | Mandatory review pending | Runtime remains legacy raw export backed |
| Non-scalar answer boundary | Plan requires hold/metadata-only behavior for current 13 export records | Same | current-fact validators | Pass | None | Mandatory review pending | No scalar-safe export records yet |
| Legacy raw retirement blockers | Plan lists blockers and defers retirement | Same | `validate_current_fact_lookup_parity.py` | Pass | None | Mandatory review pending | Legacy retirement remains future work |

## Next Reviewer Prompt

```text
Review PR: Plan current-fact lookup fallback and answer behavior.

Check:
- PR diff contains exactly one ExecPlan file:
  docs/execplans/2026-05-26-current-fact-lookup-fallback-answer-behavior.md
- Plan does not authorize runtime lookup switch.
- current_facts.py / answering.py behavior remains unchanged.
- Plan recognizes production current-fact export has 13 records and 0 scalar-safe
  records.
- annotated_numeric_candidate and frame_range remain non-scalar / not
  calculation-safe.
- Future exact scalar answers must use current_fact_guards.is_scalar_calculation_input
  plus source/domain/unit/authority checks.
- Non-scalar export-backed lookup results hold or display metadata only; no
  nested candidate or range endpoint becomes exact answer text.
- Legacy raw fallback remains technical debt and comparison/runtime surface
  only, not replacement source input.
- Legacy raw retirement blockers are explicit.
- Issue #343 double-check gate remains required for future value-handling
  decisions.
- No parser/classifier, retrieval, answer, calculator, SymPy, source/live
  acquisition, schema, fixture, generated artifact, or legacy retirement change
  is included.

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
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_lookup_parity.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether docs-only PR is ready to mark ready and merge.
```
