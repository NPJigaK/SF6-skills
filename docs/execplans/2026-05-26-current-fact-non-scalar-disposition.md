# Current-Fact Non-Scalar Disposition

Status: Draft.

## Purpose

Plan the all-13 non-scalar disposition artifact and validator slice for the
production current-fact export.

The repository now has a production `current_fact_export/v2` artifact, but all
13 records are non-scalar and not calculation-safe:

- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`;
- 0 scalar-safe current-fact records.

This plan does not restore exact numeric/current-fact answers. It creates the
reviewed disposition layer needed to say, record by record, why exact answers
must hold and which future contract could make each record usable.

## Inputs

- `AGENTS.md`
- `docs/PLAN.md`
- Issue #343 roadmap
- `docs/execplans/2026-05-26-current-fact-legacy-raw-retirement.md`
- `docs/execplans/2026-05-26-current-fact-legacy-provenance-cleanup.md`
- `data/current-facts/20260525T000000Z-current-fact-export.json`
- `docs/current-facts/20260525T000000Z-current-fact-export.md`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `src/sf6_knowledge_coach/answering.py`
- current current-fact validators and validator audit artifacts

## Target Records

The target set is exactly the 13 records in
`data/current-facts/20260525T000000Z-current-fact-export.json`.

| # | record_id | character | field | raw_value | parsed kind | calculation status | planned non-scalar disposition |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `current-fact:official:alex:row-41:cell-5:value-520f8306db0f` | alex | block_advantage | `-12～-1` | frame_range | parsed_range_not_single_value_calculation_safe | future_range_aware_contract |
| 2 | `current-fact:official:cammy:row-52:cell-5:value-f3bd1df4c26d` | cammy | block_advantage | `-4～-1` | frame_range | parsed_range_not_single_value_calculation_safe | future_range_aware_contract |
| 3 | `current-fact:official:chunli:row-32:cell-5:value-b5112d05eab3` | chunli | block_advantage | `※-4` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 4 | `current-fact:official:chunli:row-32:cell-4:value-38098349c914` | chunli | hit_advantage | `※-3` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 5 | `current-fact:official:chunli:row-35:cell-4:value-dbdd09f8dbaa` | chunli | hit_advantage | `※-1` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 6 | `current-fact:official:chunli:row-36:cell-4:value-b5112d05eab3` | chunli | hit_advantage | `※-4` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 7 | `current-fact:official:ed:row-21:cell-5:value-522076e6afe2` | ed | block_advantage | `※-2` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 8 | `current-fact:official:kimberly:row-64:cell-1:value-1a036dd4c06c` | kimberly | startup | `122※` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 9 | `current-fact:official:kimberly:row-66:cell-1:value-3c911b4c4f5d` | kimberly | startup | `128※` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 10 | `current-fact:official:kimberly:row-67:cell-1:value-1a036dd4c06c` | kimberly | startup | `122※` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 11 | `current-fact:official:kimberly:row-68:cell-1:value-1a036dd4c06c` | kimberly | startup | `122※` | annotated_numeric_candidate | annotated_candidate_not_calculation_safe | condition_bound_pending_note_semantics |
| 12 | `current-fact:official:vega_mbison:row-53:cell-5:value-1c461fc0a5e3` | vega_mbison | block_advantage | `-39～-33` | frame_range | parsed_range_not_single_value_calculation_safe | future_range_aware_contract |
| 13 | `current-fact:official:vega_mbison:row-53:cell-4:value-1c81d53e6168` | vega_mbison | hit_advantage | `-28～-23` | frame_range | parsed_range_not_single_value_calculation_safe | future_range_aware_contract |

All 13 records keep:

- `source_name == "official"`;
- `source_role == "authority_candidate"`;
- `authority_status == "authority_candidate"`;
- exact-answer status `exact_answer_hold`.

## Scope

Included after mandatory plan review:

- create a committed all-13 non-scalar disposition JSON artifact;
- create a summary Markdown artifact for reviewer readability;
- add a focused validator for the all-13 disposition artifact;
- add answer-boundary validation that proves the disposition artifact does not
  permit exact numeric/current-fact answers;
- update validator audit artifacts if a validator is added;
- update this ExecPlan progress, decision log, risks, and completion table.

Excluded:

- No exact numeric/current-fact answer restoration.
- No `answering.py` behavior change.
- No `cli.py` behavior change.
- No runtime lookup implementation.
- No fallback, dual lookup, or alias bridge.
- No parser/classifier behavior change.
- No retrieval implementation.
- No answer generation expansion.
- No calculator implementation.
- No SymPy logic.
- No source acquisition or live acquisition.
- No production current-fact export regeneration.
- No production source-record or candidate artifact regeneration.
- No schema change unless this plan is amended and reviewed first.
- No authority promotion.
- No calculation-safe promotion.
- No flattening `annotated_numeric_candidate`.
- No collapsing `frame_range`.
- No scalar interpretation of range endpoints or nested numeric candidates.

## Draft PR Flow

Use the same draft PR flow as recent current-fact artifact PRs:

1. Commit this docs-only plan to a draft PR.
2. Complete mandatory plan review.
3. Add implementation commits to the same draft PR only after mandatory plan
   review passes.
4. Complete mandatory implementation review.
5. Ready and merge only after implementation review passes.

If implementation needs files outside the approved list below, amend this
ExecPlan in the same draft PR and complete mandatory plan review again before
continuing.

## Disposition Contract

Planned artifact path:

```text
data/current-facts/non-scalar-dispositions/20260526T000000Z-current-fact-non-scalar-disposition.json
```

Planned summary path:

```text
docs/current-facts/non-scalar-dispositions/20260526T000000Z-current-fact-non-scalar-disposition.md
```

Top-level contract:

- `artifact_schema_version`: `current_fact_non_scalar_disposition/v1`
- `run_id`: `20260526T000000Z`
- `generated_from`: exactly
  `data/current-facts/20260525T000000Z-current-fact-export.json`
- `record_count`: 13
- `records`: exactly one record for each production export record

Required per-record fields:

- `record_id`
- `character_slug`
- `field_key`
- `raw_value`
- `raw_value_sha256`
- `parsed_value_kind`
- `calculation_input_status`
- `source_name`
- `source_role`
- `authority_status`
- `non_scalar_disposition_status`
- `exact_answer_status`
- `answer_boundary`
- `future_contract_required`
- `rationale`

Closed `non_scalar_disposition_status` values:

- `condition_bound_pending_note_semantics`
- `future_range_aware_contract`
- `display_only_with_caveat`
- `exact_answer_hold`

Initial status assignment:

- `annotated_numeric_candidate` records:
  `condition_bound_pending_note_semantics`;
- `frame_range` records:
  `future_range_aware_contract`.

Every record must also carry:

- `exact_answer_status == "exact_answer_hold"`;
- `answer_boundary == "must_not_answer_as_exact_scalar"`.

`display_only_with_caveat` is included in the closed enum for future reviewed
display work, but this first artifact should not use it unless implementation
review explicitly amends the plan. There is no user-facing display behavior in
this slice.

## Answer Boundary Guard

The implementation should add a validator, not runtime behavior:

- validate all 13 records are rejected by
  `current_fact_guards.is_scalar_calculation_input`;
- validate all 13 disposition records carry `exact_answer_hold`;
- validate no record permits `exact_answer_allowed`;
- validate `annotated_numeric_candidate` records keep the wrapper and do not
  expose nested numeric candidates as scalar facts;
- validate `frame_range` records keep interval semantics and do not expose
  `start` or `end` as exact scalar facts;
- validate current `answering.prepare_answer()` still returns `hold` for
  representative numeric/current-fact queries;
- validate `answering.verify_answer_packet()` still rejects crafted answered
  numeric/current-fact packets.

This guard is intentionally deterministic and local. It must not call web,
VLM, source acquisition, live acquisition, or LLM tooling.

## Files / Interfaces

Plan-only draft PR changes only:

- `docs/execplans/2026-05-26-current-fact-non-scalar-disposition.md`

Allowed implementation files after mandatory plan review:

- `docs/execplans/2026-05-26-current-fact-non-scalar-disposition.md`
- `data/current-facts/non-scalar-dispositions/20260526T000000Z-current-fact-non-scalar-disposition.json`
- `docs/current-facts/non-scalar-dispositions/20260526T000000Z-current-fact-non-scalar-disposition.md`
- `tests/validation/validate_current_fact_non_scalar_disposition.py`
- validator audit JSON/MD, only because a new validator is added

Not allowed without ExecPlan amendment:

- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/cli.py`
- runtime lookup code
- parser/classifier code
- current-fact schemas
- existing production current-fact export/source-record/candidate artifacts
- retrieval/answer/calculator/SymPy/source acquisition/live acquisition files

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
git status --short --branch
```

Expected implementation checks:

- disposition JSON has exactly 13 records;
- disposition IDs exactly match the production export record IDs;
- status counts are 9 `condition_bound_pending_note_semantics` and 4
  `future_range_aware_contract`;
- exact-answer status count is 13 `exact_answer_hold`;
- scalar guard accepted count is 0;
- production current-fact export JSON is unchanged;
- runtime answer behavior remains hold.

## Progress

- [x] 2026-05-26: Created docs-only all-13 non-scalar disposition plan from
  updated `main`.
- [ ] Complete mandatory plan review.
- [ ] Implement scoped disposition artifacts and validator in the same draft
  PR.
- [ ] Run implementation validation.
- [ ] Complete implementation review table.

## Decision Log

- 2026-05-26: Treat all 13 production export records as non-scalar and not
  calculation-safe.
- 2026-05-26: Use `condition_bound_pending_note_semantics` for
  `annotated_numeric_candidate` records.
- 2026-05-26: Use `future_range_aware_contract` for `frame_range` records.
- 2026-05-26: Require `exact_answer_hold` and
  `must_not_answer_as_exact_scalar` for every record.
- 2026-05-26: Implement only validator-backed answer-boundary guards in this
  slice. Do not change runtime answer behavior.

## Deviations

- None.

## Risks

- The disposition artifact does not make any record calculation-safe.
- User-facing display behavior remains unimplemented.
- Future range-aware or condition-aware answer behavior still needs a separate
  reviewed contract.
- The artifact is a disposition layer over reviewed current-fact export
  records; it does not add source truth.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan non-scalar disposition | Draft docs-only plan | `docs/execplans/2026-05-26-current-fact-non-scalar-disposition.md` | plan-only validation | Pending | None | Mandatory review pending | Implementation not started |
| Disposition artifact | Create all-13 disposition JSON/MD | planned artifact files | new validator | Pending | None | Implementation pending | No source-truth expansion |
| Answer boundary guard | Validate exact answers remain held and scalar guard rejects all 13 | planned validator | all validators | Pending | None | Implementation pending | Runtime behavior unchanged |

## Next Reviewer Prompt

```text
Review PR for all-13 current-fact non-scalar disposition plan.

Check:
- PR diff is exactly:
  docs/execplans/2026-05-26-current-fact-non-scalar-disposition.md
- The target set is exactly the 13 records in:
  data/current-facts/20260525T000000Z-current-fact-export.json
- The plan keeps all 13 records non-scalar / not calculation-safe.
- annotated_numeric_candidate records are assigned
  condition_bound_pending_note_semantics.
- frame_range records are assigned future_range_aware_contract.
- every record requires exact_answer_hold and must_not_answer_as_exact_scalar.
- The plan adds only disposition artifact, summary, focused validator, and
  validator audit implementation after mandatory plan review.
- The answer-boundary guard is validator-only and does not change runtime.
- No exact answer restoration, fallback, dual lookup, alias bridge,
  parser/classifier, retrieval, answer generation, calculator, SymPy,
  source/live acquisition, schema, generated current-fact export regeneration,
  authority promotion, calculation-safe promotion, annotated flattening, or
  range collapse is planned.

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
