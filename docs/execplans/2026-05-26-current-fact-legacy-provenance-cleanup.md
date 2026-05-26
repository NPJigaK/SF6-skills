# Current-Fact Legacy Provenance Cleanup

Status: Draft.

## Purpose

Plan the cleanup of remaining current-fact legacy provenance debt after
one-shot legacy raw current-fact retirement.

PR #370 retired the runtime path that loaded `data/exports/*/official_raw.json`
and deleted those raw JSON files. The remaining cleanup candidates are now:

- historical synthetic current-fact record fixture references to deleted
  `data/exports/jp/official_raw.json`;
- retained `data/exports/*/snapshot_manifest.json` files;
- retained `data/exports/_index/manual-review-debt.json`;
- `data/exports/README.md`, which exists only to document the retained legacy
  provenance directory.

This plan treats compatibility fallback, dual lookup, alias bridging, and
legacy raw preservation as intentionally rejected. It plans deletion or
replacement only for surfaces that no longer have an active runtime,
validator, generator, or reviewed-artifact dependency.

## Inputs

- `AGENTS.md`
- `docs/PLAN.md`
- Issue #343 roadmap
- `docs/execplans/2026-05-23-data-surface-cleanup.md`
- `docs/execplans/2026-05-26-current-fact-legacy-raw-retirement.md`
- `README.md`
- `data/exports/README.md`
- `data/exports/*/snapshot_manifest.json`
- `data/exports/_index/manual-review-debt.json`
- `tests/fixtures/current-facts/records/valid/*.json`
- `tests/fixtures/current-facts/records/invalid/source_family_uses_source_identity.json`
- current current-fact validators and validator audit artifacts

## Current Findings

Current tracked `data/exports` inventory:

```text
29 data/exports/*/snapshot_manifest.json files
 1 data/exports/_index/manual-review-debt.json
 1 data/exports/README.md
31 tracked files total
```

Current synthetic record fixture references to deleted official raw data:

```text
tests/fixtures/current-facts/records/valid/official_active_frame_range.json
tests/fixtures/current-facts/records/valid/official_block_advantage_signed_frame.json
tests/fixtures/current-facts/records/valid/official_move_name_raw_preserved.json
tests/fixtures/current-facts/records/invalid/source_family_uses_source_identity.json
```

Those four references are historical synthetic fixture metadata. They should
not continue pointing at a deleted raw export file.

Other `data/exports/jp/official_raw.json` strings in invalid export,
source-record, candidate, and generator fixtures are boundary rejection checks.
They are not active dependencies and should remain allowed only as explicit
negative fixtures unless implementation review finds a cleaner equivalent
that preserves the same rejection coverage.

## Scope

Included after mandatory plan review:

- replace historical synthetic current-fact record fixture `public_reference`
  values that point to deleted `data/exports/jp/official_raw.json`;
- convert those synthetic fixtures away from `official_raw_snapshot` evidence
  where appropriate, without claiming source truth;
- delete all remaining tracked `data/exports` legacy provenance files if
  dependency scan confirms no active current dependency:
  - `data/exports/*/snapshot_manifest.json`;
  - `data/exports/_index/manual-review-debt.json`;
  - `data/exports/README.md`;
- update `README.md` so it no longer describes `data/exports/` as retained
  public current-fact seed data;
- update clean-slate validation to guard that `data/exports/` remains retired,
  while still permitting explicit negative fixture strings that reject legacy
  paths;
- update focused validators or validator audit artifacts only if required by
  the fixture and clean-slate changes;
- update this ExecPlan progress, decision log, risks, and completion table.

Excluded:

- No compatibility fallback.
- No dual lookup.
- No alias/input bridge.
- No runtime lookup change.
- No `current_facts.py` restoration.
- No `answering.py` exact numeric/current-fact answer restoration.
- No `cli.py` raw-backed search/current lookup restoration.
- No parser/classifier behavior change.
- No retrieval implementation.
- No answer generation expansion.
- No calculator implementation.
- No SymPy logic.
- No source acquisition or live acquisition.
- No production candidate/source-record/current-fact export generation.
- No schema change.
- No authority promotion.
- No calculation-safe promotion.
- No flattening `annotated_numeric_candidate`.
- No collapsing `frame_range`.
- No deletion of boundary-rejection fixtures solely because they contain a
  forbidden legacy path string.

## Draft PR Flow

Use the same draft PR flow as the recent current-fact artifact PRs:

1. Commit this docs-only plan to a draft PR.
2. Complete mandatory plan review.
3. Add implementation commits to the same draft PR only after mandatory plan
   review passes.
4. Complete mandatory implementation review.
5. Ready and merge only after implementation review passes.

If implementation needs files outside the approved list below, amend this
ExecPlan in the same draft PR and complete mandatory plan review again before
continuing.

## Implementation Decisions

- Decision: delete remaining tracked `data/exports` provenance files if the
  implementation dependency scan finds no active dependency.
  Rationale: PR #370 deleted the runtime raw lookup path and all
  `official_raw.json` files. The remaining snapshot and manual-review debt
  files are legacy provenance/observability surfaces without a regeneration
  workflow or active authority role.

- Decision: keep invalid fixtures that explicitly reject `data/exports/*`
  references unless equivalent rejection coverage replaces them.
  Rationale: rejection fixtures are not historical authority references. They
  prove that legacy raw paths cannot re-enter generated current-fact artifacts.

- Decision: replace valid synthetic record fixture evidence references rather
  than deleting those fixtures.
  Rationale: schema validators still need synthetic valid record fixtures.
  The fixtures should describe themselves as synthetic contract fixtures, not
  as records grounded in deleted official raw exports.

- Decision: keep the production current-fact export and source-record
  artifacts unchanged.
  Rationale: those reviewed artifacts do not depend on `data/exports` as
  source input and remain useful for future non-scalar disposition work.

## Acceptance Criteria

- Historical synthetic current-fact record fixtures no longer point at deleted
  `data/exports/jp/official_raw.json`.
- Remaining valid synthetic record fixtures make no source-truth claim based
  on deleted raw exports.
- `data/exports/` has no tracked files after implementation, unless mandatory
  implementation review finds and documents an explicit current dependency.
- `README.md` no longer presents `data/exports/` as retained public
  current-fact seed data.
- Clean-slate validation guards the retired `data/exports/` directory.
- Boundary rejection tests may still contain `data/exports` strings when their
  purpose is explicitly to reject legacy paths.
- Production current-fact artifacts remain retained and unchanged.
- The 13 production current-fact export records remain non-scalar and not
  calculation-safe.
- No runtime lookup, answer, parser/classifier, retrieval, calculator, SymPy,
  source/live acquisition, schema, generated artifact, authority promotion, or
  calculation-safe promotion is included.

## Files / Interfaces

Plan-only draft PR changes only:

- `docs/execplans/2026-05-26-current-fact-legacy-provenance-cleanup.md`

Allowed implementation files after mandatory plan review:

- `docs/execplans/2026-05-26-current-fact-legacy-provenance-cleanup.md`
- `README.md`
- `tests/fixtures/current-facts/records/valid/official_active_frame_range.json`
- `tests/fixtures/current-facts/records/valid/official_block_advantage_signed_frame.json`
- `tests/fixtures/current-facts/records/valid/official_move_name_raw_preserved.json`
- `tests/fixtures/current-facts/records/invalid/source_family_uses_source_identity.json`
- `tests/validation/validate_clean_slate.py`
- `tests/validation/validate_current_fact_schemas.py`, only if needed to
  preserve fixture/schema boundary validation;
- validator audit JSON/MD, only if validator or test evidence boundaries
  change;
- tracked deletions under `data/exports/`:
  - `data/exports/README.md`;
  - `data/exports/_index/manual-review-debt.json`;
  - `data/exports/*/snapshot_manifest.json`.

Not allowed without ExecPlan amendment:

- current-fact runtime modules;
- answer or CLI runtime behavior beyond existing retired behavior;
- parser/classifier code;
- schemas;
- production generated current-fact artifacts;
- retrieval/answer/calculator/SymPy/source acquisition/live acquisition files.

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

Implementation validation after mandatory plan review:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git ls-files data/exports
rg "data/exports/jp/official_raw\\.json" tests/fixtures/current-facts/records README.md data/exports || true
git status --short --branch
```

Expected implementation checks:

- `git ls-files data/exports` prints no tracked files.
- The `rg` fixture check prints no valid/current-fact record fixture or README
  references to deleted `official_raw.json`.
- Any remaining `data/exports` strings are limited to boundary rejection
  checks and historical ExecPlan prose.

## Progress

- [x] 2026-05-26: Created docs-only cleanup plan from updated `main`.
- [ ] Complete mandatory plan review.
- [ ] Implement scoped cleanup in the same draft PR.
- [ ] Run implementation validation.
- [ ] Complete implementation review table.

## Decision Log

- 2026-05-26: Treat remaining tracked `data/exports` files as deletion
  candidates after PR #370, subject to dependency scan.
- 2026-05-26: Treat valid synthetic record references to deleted
  `official_raw.json` as cleanup targets.
- 2026-05-26: Keep explicit negative fixtures that reject `data/exports/*`
  references unless replacement rejection coverage is reviewed.
- 2026-05-26: Do not use this cleanup to change non-scalar current-fact
  disposition or answer behavior.

## Deviations

- None.

## Risks

- Historical ExecPlans will still mention `data/exports`; they are not active
  dependencies and should not be rewritten unless a validator fails.
- Removing `data/exports/README.md` means the legacy provenance directory no
  longer has in-place documentation; `README.md` and this ExecPlan should carry
  the retirement rationale instead.
- Boundary rejection fixtures may still contain `data/exports` strings by
  design, which requires reviewer care when scanning for active dependencies.
- Production current-fact export records remain non-scalar and not
  calculation-safe; exact numeric/current-fact answers continue to hold.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan cleanup | Draft docs-only cleanup plan | `docs/execplans/2026-05-26-current-fact-legacy-provenance-cleanup.md` | plan-only validation | Pending | None | Mandatory review pending | Implementation not started |
| Fixture cleanup | Replace historical valid synthetic fixture references | planned fixture files | `validate_current_fact_schemas.py` | Pending | None | Implementation pending | Synthetic fixtures still do not prove source truth |
| Provenance deletion | Delete remaining tracked `data/exports` provenance files | planned `data/exports` deletions | `git ls-files data/exports` | Pending | None | Implementation pending | Historical ExecPlans still mention legacy paths |
| Boundary preservation | Keep rejection coverage for legacy path inputs | current-fact validators/fixtures | all validators | Pending | None | Implementation pending | Must not re-authorize legacy paths |

## Next Reviewer Prompt

```text
Review PR for current-fact legacy provenance cleanup plan.

Check:
- PR diff is exactly:
  docs/execplans/2026-05-26-current-fact-legacy-provenance-cleanup.md
- The plan targets historical synthetic fixture references and remaining
  data/exports snapshot/manual-review provenance debt only.
- The plan uses same draft PR flow: plan review before implementation commits.
- Remaining tracked data/exports files are deletion candidates only after
  dependency scan.
- Valid synthetic current-fact record fixtures must stop pointing at deleted
  data/exports/jp/official_raw.json.
- Invalid fixtures may retain data/exports strings only as boundary rejection
  checks.
- No runtime lookup, current_facts.py restoration, answering.py exact answer
  restoration, CLI raw-backed restoration, parser/classifier, retrieval,
  answer generation, calculator, SymPy, source/live acquisition, schema,
  generated artifact, authority promotion, or calculation-safe promotion is
  planned.
- Production current-fact artifacts remain retained.
- The 13 production export records remain non-scalar / not calculation-safe.

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

Return blocking findings first, validation results, PLAN deviations,
remaining risks, and whether implementation commits may proceed in the same
draft PR.
```
