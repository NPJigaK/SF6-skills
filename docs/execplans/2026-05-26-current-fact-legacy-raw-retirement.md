# Current-Fact Legacy Raw Retirement

Status: One-shot retirement implementation complete; validation passed.

## Purpose

Plan the one-shot retirement of the legacy raw-backed current-fact path.

The repository now has reviewed current-fact artifacts, but the 13 production
current-fact export records are all non-scalar and not calculation-safe. This
means they cannot preserve legacy exact numeric answers. The safe direction is
therefore not fallback, dual lookup, or alias bridging. The safe direction is
to retire the legacy raw-backed answer path in one pass and make
numeric/current-fact exact answers hold until a later reviewed scalar-safe or
non-scalar disposition contract exists.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- Issue #343 roadmap
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parity-rollback.md`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/cli.py`
- `tests/test_cli.py`
- `tests/validation/validate_clean_slate.py`
- `tests/validation/validate_current_fact_lookup_parity.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/current-facts/20260525T000000Z-current-fact-export.json`
- `docs/current-facts/20260525T000000Z-current-fact-export.md`
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- `data/exports/README.md`
- `data/exports/*/official_raw.json`
- current validator audit artifacts

## Context

Current legacy raw-backed behavior:

- `current_facts.py` reads `data/exports/<character>/official_raw.json`;
- `lookup_current_fact(character_slug, move_input, field)` matches legacy
  `input` strings and returns raw field values;
- `search_moves()` scans the same legacy raw export tree;
- `cli.py` exposes `search` and `current lookup` paths backed by
  `current_facts.py`;
- `answering.py` calls `lookup_current_fact` for numeric/current-fact queries
  and can return answered packets using raw values;
- `tests/test_cli.py` currently asserts JP 5LP legacy raw lookup behavior;
- `tests/validation/validate_current_fact_lookup_parity.py` currently protects
  the transition boundary by fixing the legacy JP raw comparison surface and
  source-text markers.

Reviewed current-fact artifact state:

- production export:
  `data/current-facts/20260525T000000Z-current-fact-export.json`;
- artifact schema `current_fact_export/v2`;
- 13 records total;
- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`;
- 0 records with `eligible_only_after_domain_source_and_unit_checks`;
- all records remain official `authority_candidate`.

The 13 non-scalar records are not a blocker to retiring legacy raw. They are a
blocker only to preserving or replacing exact numeric/current-fact answers.
Flattening annotated candidates or collapsing frame ranges to avoid this hold
is forbidden.

## Scope

Included in this plan:

- retire the legacy raw-backed current-fact path in one implementation pass
  after mandatory plan review;
- remove or disable raw-backed current-fact exact answers;
- remove or disable raw-backed CLI lookup/search surfaces;
- update tests that currently assert legacy raw-backed answers;
- remove or replace validators that only protect legacy raw-backed behavior;
- treat `data/exports/*/official_raw.json` as deletion candidates unless the
  implementation review finds another explicit current dependency;
- keep reviewed current-fact artifacts;
- keep numeric/current-fact exact answers on hold unless a later all-13
  non-scalar disposition plan or scalar-safe artifact makes an answer safe.

Excluded:

- No compatibility fallback.
- No dual lookup.
- No alias/input bridge.
- No parsed-value-to-legacy joining.
- No parser/classifier behavior change.
- No retrieval implementation.
- No answer generation expansion.
- No calculator implementation.
- No SymPy logic.
- No source acquisition.
- No live acquisition.
- No new production current-fact artifact generation.
- No authority promotion.
- No calculation-safe promotion.
- No flattening `annotated_numeric_candidate`.
- No collapsing `frame_range`.

## Draft PR Flow

Use the same draft PR flow as recent current-fact artifact PRs:

1. Commit this replacement docs-only plan to PR #370.
2. Complete mandatory plan review.
3. Add one-shot retirement implementation commits to the same draft PR only
   after mandatory plan review passes.
4. Complete mandatory implementation review.
5. Ready and merge only after implementation review passes.

The previous fallback/dual-lookup direction is abandoned. PR #370 should not
contain a fallback/dual-lookup plan in its final diff.

## Retirement Decision

One-shot retirement means:

- `answering.py` must no longer answer numeric/current-fact queries by reading
  legacy raw export values;
- numeric/current-fact queries must hold with an explicit uncertainty until a
  reviewed scalar-safe or non-scalar answer behavior contract exists;
- `current_facts.py` must no longer expose legacy raw-backed current-fact
  authority as an answer source;
- CLI surfaces that depend on legacy raw current-fact data must be removed,
  disabled, or converted to explicit hold/unavailable behavior in the same
  implementation PR;
- validators/tests whose only purpose is protecting legacy raw behavior must be
  removed, replaced, or rewritten as retirement guards.

This is intentionally not behavior-preserving. It trades current legacy raw
answers for a cleaner authority boundary.

## Non-Scalar Disposition Boundary

The production export's 13 records may remain reviewed artifacts after legacy
raw retirement, but they must not become exact scalar answers:

- `annotated_numeric_candidate` stays condition-bound / note-bound candidate
  data;
- `frame_range` stays interval/range data;
- `current_fact_guards.is_scalar_calculation_input` must reject all 13 records;
- exact answer packets must not use nested numeric candidate values or range
  endpoints as scalar facts;
- if answer behavior for these 13 records is desired, create a separate
  all-13 non-scalar disposition PR first.

That disposition PR should classify each record as one of:

- `exact_answer_hold`;
- `display_only_with_caveat`;
- `future_range_aware_contract`;
- `condition_bound_pending_note_semantics`;
- another reviewed closed status.

It must still not flatten annotated candidates or collapse ranges.

## Implementation Targets To Review

A later implementation commit in this same draft PR may touch only the files
needed for one-shot retirement. Expected target groups are:

- `src/sf6_knowledge_coach/current_facts.py`;
- `src/sf6_knowledge_coach/answering.py`;
- `src/sf6_knowledge_coach/cli.py`;
- `tests/test_cli.py`;
- `tests/validation/validate_clean_slate.py`;
- `tests/validation/validate_current_fact_lookup_parity.py`, deleted or
  replaced because it currently protects legacy raw behavior;
- validator audit JSON/MD if validator/test files change;
- `data/exports/README.md`;
- `data/exports/*/official_raw.json`, if dependency scan confirms no remaining
  current dependency;
- this ExecPlan.

Any implementation that needs additional files must amend this ExecPlan and
complete mandatory review before continuing.

## Expected Implementation Shape

The implementation should be as small as possible:

- stop importing `lookup_current_fact` into `answering.py`;
- make numeric/current-fact answer preparation return `hold` with a clear
  deterministic-retirement message;
- remove or disable CLI handlers that call legacy raw lookup/search;
- update tests to assert hold/unavailable behavior instead of JP 5LP raw answer
  behavior;
- update clean-slate required paths so `data/exports/jp/official_raw.json` is
  no longer required;
- remove, replace, or narrow `validate_current_fact_lookup_parity.py` so it no
  longer requires legacy raw counts or source-text markers;
- delete `official_raw.json` files only if the same implementation proves no
  current dependency remains.

The implementation must not introduce a new lookup helper that reads the
production export for answers. That is a separate future plan.

## Legacy Export Deletion Boundary

`data/exports/*/official_raw.json` files are deletion candidates. Deletion is
allowed only if implementation review confirms no remaining current dependency
after retiring:

- `current_facts.py` raw lookup/load functions;
- `answering.py` raw lookup calls;
- `cli.py` raw-backed `search` / `current lookup` handlers;
- tests that assert raw-backed answers;
- validators that require legacy raw comparison data.

`snapshot_manifest.json`, `data/exports/_index/manual-review-debt.json`, and
`data/exports/README.md` are not automatically deleted by this plan. They may
need separate cleanup after official raw files are removed.

## Acceptance Criteria

- Runtime no longer answers numeric/current-fact queries from legacy raw export
  values.
- No fallback, dual lookup, or alias bridge is introduced.
- Legacy raw-backed current-fact CLI paths are removed or explicitly disabled.
- Tests no longer assert JP 5LP raw-backed answer behavior.
- Validators no longer require legacy raw-backed runtime markers as active
  current behavior.
- Reviewed current-fact artifacts remain in place.
- The 13 production export records remain non-scalar and not calculation-safe.
- Exact numeric/current-fact answers hold unless a later reviewed disposition or
  scalar-safe contract exists.
- No parser/classifier, retrieval, calculator, SymPy, source/live acquisition,
  generated artifact, authority promotion, or calculation-safe promotion is
  included.

## Files / Interfaces

Plan-only PR #370 should change only:

- `docs/execplans/2026-05-26-current-fact-legacy-raw-retirement.md`

The old fallback plan file must not remain in the final PR diff:

- `docs/execplans/2026-05-26-current-fact-lookup-fallback-answer-behavior.md`

Implementation commits require mandatory plan review first.

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

Implementation validation after mandatory plan review should include:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
rg "lookup_current_fact|search_moves|official_raw\\.json|data/exports" src tests
find data/exports -name official_raw.json
git status --short --branch
```

If implementation deletes `official_raw.json`, add a focused file inventory
check proving no `data/exports/*/official_raw.json` files remain and no current
runtime/test/validator code references them as active behavior.

## Progress

- 2026-05-26: Replaced fallback/dual-lookup PR #370 direction with one-shot
  legacy raw retirement plan. No implementation, schema, fixture, generated
  artifact, parser/classifier, retrieval, answer generation, calculator, SymPy,
  source/live acquisition, or legacy raw deletion yet.
- 2026-05-26: Ran plan-only validation. All checks passed.
- 2026-05-26: Implemented one-shot legacy raw retirement. Removed
  `current_facts.py`, stopped raw-backed numeric/current-fact answers, made
  raw-backed CLI `search` and `current lookup` explicitly unavailable, removed
  the legacy parity validator, updated clean-slate and validator audit
  boundaries, updated `data/exports/README.md`, and deleted all
  `data/exports/*/official_raw.json` files.
- 2026-05-26: Ran implementation validation. All checks passed.
- 2026-05-26: Tightened `verify_answer_packet()` so crafted
  numeric/current-fact `answered` packets are rejected even if they carry the
  retired `deterministic_current_fact_lookup` evidence kind. Added regression
  coverage.

## Decision Log

- 2026-05-26: Do not continue fallback, dual lookup, or alias bridge direction.
- 2026-05-26: Non-scalar 13 production export records do not block raw
  retirement, but they do block exact answer preservation.
- 2026-05-26: Numeric/current-fact exact answers should hold after raw
  retirement unless a later reviewed scalar-safe or all-13 non-scalar
  disposition contract exists.
- 2026-05-26: `data/exports/*/official_raw.json` are deletion candidates unless
  implementation review finds another explicit current dependency.
- 2026-05-26: Dependency scan found no remaining active source/runtime/test
  dependency that requires checked-in `official_raw.json`. Remaining
  `data/exports` references in `src` and `tests` are boundary rejection checks,
  invalid fixtures, or legacy provenance terms, not active raw-backed lookup.
- 2026-05-26: The legacy parity validator was deleted because its purpose was
  to protect a transition boundary that required legacy raw-backed runtime
  markers. Clean-slate now guards that raw exports and `current_facts.py` remain
  deleted.
- 2026-05-26: Answer packet verification now enforces the retirement boundary:
  numeric/current-fact exact answers must hold until a later reviewed contract
  exists.

## Deviations

- None.

## Risks

- Retiring raw-backed answers is intentionally not behavior-preserving.
- CLI users of `search` or `current lookup` may lose legacy raw-backed output
  until a reviewed replacement exists.
- Deleting `official_raw.json` may require README and clean-slate updates in
  the same implementation PR.
- `snapshot_manifest.json` and manual-review debt surfaces may remain as
  separate cleanup debt.
- The all-13 non-scalar disposition remains future work.
- Remaining `data/exports` snapshot manifests and manual-review debt index are
  legacy provenance/observability surfaces and may need a later cleanup PR.
- Some synthetic current-fact schema fixtures still use historical
  `data/exports/jp/official_raw.json` references. They are not active runtime
  dependencies, but they should be reviewed in a later fixture cleanup PR.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| One-shot raw retirement plan | Draft plan and implementation | `docs/execplans/2026-05-26-current-fact-legacy-raw-retirement.md` | `git diff --check`; `uv lock --check` | Pass | None | Implementation review pending | Raw retirement is not behavior-preserving |
| Fallback direction removal | Replaced fallback/dual-lookup plan direction | Same | PR diff inspection | Pass | None | Implementation review pending | PR branch name remains historical |
| Runtime answer retirement | Numeric/current-fact answers hold instead of reading legacy raw values | `src/sf6_knowledge_coach/answering.py`; `tests/test_cli.py` | `PYTHONPATH=src uv run --locked python -m unittest discover -s tests` | Pass | None | Implementation review pending | Exact answers now hold |
| Answer verifier retirement | Crafted numeric/current-fact answered packets are rejected even with retired deterministic lookup evidence | `src/sf6_knowledge_coach/answering.py`; `tests/test_cli.py` | `PYTHONPATH=src uv run --locked python -m unittest discover -s tests` | Pass | None | Implementation review pending | Exact answers now hold |
| CLI retirement | Raw-backed `search` and `current lookup` return explicit unavailable payloads | `src/sf6_knowledge_coach/cli.py`; `tests/test_cli.py` | `PYTHONPATH=src uv run --locked python -m unittest discover -s tests` | Pass | None | Implementation review pending | CLI output intentionally changed |
| Raw lookup deletion | Removed legacy raw lookup module and all checked-in official raw JSON files | `src/sf6_knowledge_coach/current_facts.py`; `data/exports/*/official_raw.json`; `data/exports/README.md`; `tests/validation/validate_clean_slate.py` | `find data/exports -name official_raw.json`; `validate_clean_slate.py` | Pass | None | Implementation review pending | Snapshot manifests remain legacy provenance |
| Validator/audit retirement | Deleted legacy parity validator and updated audit metadata | `tests/validation/validate_current_fact_lookup_parity.py`; validator audit JSON/MD | `validate_validator_test_audit.py`; all `tests/validation/validate_*.py` | Pass | None | Implementation review pending | Future runtime switch needs new validators |
| Non-scalar boundary | Plan keeps all 13 records non-scalar / not calculation-safe | Same | current-fact validators | Pass | None | Implementation review pending | Exact answers will hold |

## Next Reviewer Prompt

```text
Review PR #370 implementation for one-shot legacy raw current-fact retirement.

Check:
- PR implements the amended ExecPlan only.
- The previous fallback/dual-lookup ExecPlan file is not present in final diff.
- No compatibility fallback, dual lookup, or alias bridge is introduced.
- The implementation retires/removes/disables the legacy raw-backed answer path
  in one pass.
- `answering.py` no longer imports or calls legacy raw lookup.
- Numeric/current-fact answer packets hold until a reviewed scalar-safe or
  non-scalar disposition contract exists.
- `cli.py` raw-backed `search` / `current lookup` surfaces are explicitly
  unavailable and do not read raw exports.
- `current_facts.py` is deleted.
- `data/exports/*/official_raw.json` files are deleted.
- `validate_clean_slate.py` no longer requires legacy raw and guards deletion.
- The legacy parity validator is deleted and validator audit is updated.
- Reviewed current-fact artifacts remain retained.
- The 13 production export records remain non-scalar / not calculation-safe.
- The implementation does not flatten annotated_numeric_candidate or collapse
  frame_range.
- No parser/classifier, retrieval, answer generation expansion, calculator,
  SymPy, source/live acquisition, schema, fixture, generated artifact,
  authority promotion, or calculation-safe promotion is included.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- git diff --cached --check
- uv lock --check
- PYTHONPATH=src uv run --locked python -m unittest discover -s tests
- for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
- rg "lookup_current_fact|search_moves|official_raw\\.json|data/exports" src tests
- find data/exports -name official_raw.json

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether PR #370 is ready to mark ready and merge.
```
