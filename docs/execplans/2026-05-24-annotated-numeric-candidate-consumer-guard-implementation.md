# Annotated Numeric Candidate Consumer Guard Implementation

Status: Drafted for review.

## Purpose

Plan implementation of deterministic guard helpers and validators so future
consumers cannot accidentally treat non-scalar parsed values as scalar
calculation inputs.

The immediate trigger is PR #346, which added
`parsed_value.kind == "annotated_numeric_candidate"` with
`calculation_input_status == "annotated_candidate_not_calculation_safe"`.
This implementation plan also covers the earlier `frame_range` guard contract
from PR #335 because both shapes are parsed but not scalar calculation-safe.

This ExecPlan is docs-only. It does not implement runtime, retrieval, answer,
export, calculator, parser, classifier, schema, generated artifact, live
acquisition, or SymPy changes.

## Inputs

- `docs/execplans/2026-05-23-frame-range-consumer-guard.md`
- `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard.md`
- `docs/execplans/2026-05-24-annotated-official-parser-schema-implementation.md`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `tests/fixtures/current-facts/records/valid/*.json`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/test_cli.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`

## Context

Current parsed values now include scalar and non-scalar shapes:

- scalar-like examples: `signed_frame`, `integer`, and other values that may
  be calculation inputs only when their status and authority contract allow
  it;
- non-scalar examples: `frame_range` with
  `parsed_range_not_single_value_calculation_safe`;
- condition-bound non-scalar examples: `annotated_numeric_candidate` with
  `annotated_candidate_not_calculation_safe`;
- blocked examples: review-required values with no `parsed_value`.

The current repo has only a minimal current-fact lookup and answer scaffold:

- `src/sf6_knowledge_coach/current_facts.py` reads legacy
  `data/exports/<character>/official_raw.json`;
- `src/sf6_knowledge_coach/answering.py` calls that lookup for deterministic
  numeric/current-fact answers;
- no normalized parsed-value export, retrieval table, scalar calculator, or
  condition-aware calculator exists yet.

Because future consumers will likely read `parsed_value` directly, this plan
places a small deterministic guard before those surfaces expand.

## Scope

Included for future implementation planning:

- Add a small helper that answers whether a parsed value is safe for scalar
  calculation contexts.
- Add focused tests proving the helper rejects non-scalar parsed values and
  blocked values.
- Add validator coverage that future current-fact/export/retrieval/answer/
  calculator consumers must use or match before consuming parsed values.
- Add fixtures for accepted scalar and rejected non-scalar cases.
- Keep `calculation_input_status` mandatory to carry forward in any future
  consumer artifact that reads parsed values.
- Keep Issue #343 double-check as a required gate before future annotated
  raw-value expansion.

Excluded:

- No runtime behavior changes in this docs-only PR.
- No retrieval implementation.
- No answer behavior changes.
- No normalized export implementation.
- No calculator implementation.
- No parser or classifier changes in this docs-only PR.
- No schema changes in this docs-only PR.
- No generated artifact changes.
- No SymPy logic.
- No live acquisition.
- No calculation-safe promotion.
- No numeric authority or current-fact authority promotion.

## Current Consumer Surface Decision

The immediate implementation slice should treat these as existing or near-term
consumer surfaces:

- `current_facts.py`: current lookup surface. It currently reads legacy raw
  export records and does not consume `parsed_value`; implementation should
  add tests that any future parsed-value lookup path must pass through the
  guard before returning scalar values.
- `answering.py`: exact numeric answer surface. It currently depends on
  deterministic current-fact lookup; implementation should add tests or
  validator fixtures proving exact-answer paths reject non-scalar parsed
  values when a parsed-value-backed lookup is introduced.
- `contracts/current-facts/*.schema.json` and fixtures: schema validation
  surface. The first implementation can use synthetic fixtures without schema
  changes unless a real schema blocker is found.
- Future normalized exports, retrieval tables, and calculators: no runtime
  implementation yet, but validators should define the contract they must
  obey before those surfaces consume `parsed_value`.

No immediate guard implementation should alter user-facing answer behavior
unless a later ExecPlan explicitly introduces a parsed-value-backed lookup.

## Helper Decision

The implementation should add a small helper rather than duplicating guard
logic across future consumers.

Proposed helper shape:

```python
def is_scalar_calculation_input(
    parsed_value: object | None,
    calculation_input_status: str | None,
) -> bool:
    ...
```

The exact module location should be chosen during implementation, but the
preferred location is a small current-fact consumer utility module under
`src/sf6_knowledge_coach/`, for example
`current_fact_guards.py`, to avoid coupling consumer guards back into the raw
parser/classifier.

Required behavior:

- return `False` when `parsed_value` is missing;
- return `False` for `calculation_input_status` values that are known
  non-scalar or blocked, including:
  - `annotated_candidate_not_calculation_safe`;
  - `parsed_range_not_single_value_calculation_safe`;
  - `review_required_not_calculation_safe`;
  - `enum_only_not_arithmetic`;
  - `raw_preserved_not_calculation`;
  - `not_numeric_authority`;
  - `out_of_scope_not_emitted`;
- return `False` for `parsed_value.kind` values that are known non-scalar in
  scalar calculation contexts, including:
  - `annotated_numeric_candidate`;
  - `frame_range`;
  - `enum_token`;
  - `ordered_pair`;
- return `True` only for explicitly approved scalar kinds with an approved
  calculation status.

This plan does not approve any new value as calculation-safe. If the current
coverage has no production `eligible_only_after_domain_source_and_unit_checks`
official scalar authority records, the accepted scalar fixture must be a
synthetic contract fixture, not a new authority claim.

## Scalar Status Decision

The helper must not infer scalar safety from `parsed_value.kind` alone.

Future implementation should define a closed set of calculation-safe statuses.
For the first guard implementation, the expected set may be empty or limited
to synthetic contract fixture statuses already approved by current policy. If
there is no approved calculation-safe status in production artifacts, tests
must prove that normal scalar parsed shapes are still rejected without an
approved status.

This keeps the guard conservative:

- `{"kind": "signed_frame", "value": -2}` is not enough by itself;
- `calculation_input_status` must explicitly allow scalar calculation;
- authority/source checks remain a separate requirement for real current-fact
  use.

## Validator Decision

Implementation should add a focused validator or extend an existing validation
surface only where evidence already exists.

Preferred implementation:

- add `tests/validation/validate_current_fact_consumer_guards.py`;
- use synthetic fixtures embedded in the validator or stored under
  `tests/fixtures/current-facts/consumer-guards/`;
- validate helper behavior for accepted and rejected cases;
- validate that current parsed-value coverage records with
  `annotated_candidate_not_calculation_safe` and
  `parsed_range_not_single_value_calculation_safe` are rejected by scalar
  guard logic;
- validate that blocked review-required records with no `parsed_value` are
  rejected.

Validators must be evidence-first and boundary-based. They must not weaken
schema or classifier validators to fit current output.

## Exact Test Fixture Strategy

The implementation must include at least these fixtures or equivalent
synthetic contract cases.

Accepted scalar fixture:

- a normal scalar `signed_frame` or `integer` parsed value;
- an explicitly approved scalar calculation status if one exists by policy;
- if no approved status exists, this fixture must stay synthetic and clearly
  marked as a contract-only example.

Rejected non-scalar fixtures:

- `parsed_value.kind == "annotated_numeric_candidate"` with
  `calculation_input_status == "annotated_candidate_not_calculation_safe"`;
- `parsed_value.kind == "frame_range"` with
  `calculation_input_status ==
  "parsed_range_not_single_value_calculation_safe"`;
- review-required blocked value with no `parsed_value` and
  `calculation_input_status == "review_required_not_calculation_safe"`;
- normal scalar-looking `signed_frame` or `integer` with missing or
  non-approved `calculation_input_status`;
- SuperCombo parsed numeric candidate with
  `calculation_input_status == "not_numeric_authority"`.

The tests must prove that nested numeric content inside
`annotated_numeric_candidate.numeric_candidate.value` cannot make the value
scalar-safe.

## Future Consumer Requirements

Any future export, retrieval, answer, calculator, or current-fact consumer PR
that reads parsed values must:

- carry `calculation_input_status` forward;
- call the guard helper or satisfy an equivalent validator;
- reject `annotated_numeric_candidate` and `frame_range` in scalar contexts;
- keep non-scalar parsed values available only as display/search/review
  metadata unless a later condition-aware or range-aware contract is approved;
- avoid flattening nested numeric candidates to `integer`, `signed_frame`, or
  exact answer values;
- preserve authority boundaries and avoid current-fact authority promotion.

## Issue #343 Gate

Issue #343 double-check remains required for any future annotated raw-value
expansion.

The guard implementation must not parse additional raw values. It only ensures
that already parsed non-scalar values cannot be used as scalar calculation
inputs.

Same-grammar annotated variants such as `124※`, block `※-15`, block `※-5`,
and block `※-10` remain blocked until a later plan provides:

- targeted Scrapling screenshot bundle;
- human ChatGPT/VLM observation recorded as `observation_candidate` only;
- deterministic artifact/reviewer evidence alignment;
- parser/classifier coverage updates approved by mandatory review.

## Acceptance Criteria

- The ExecPlan identifies current consumer surfaces and future consumer
  surfaces.
- The ExecPlan defines a small helper direction such as
  `is_scalar_calculation_input`.
- The ExecPlan requires tests proving annotated candidates, frame ranges, and
  blocked review-required values are rejected in scalar contexts.
- The ExecPlan requires future consumer artifacts to carry
  `calculation_input_status`.
- The ExecPlan keeps parser/classifier/schema/generated artifact changes out
  of this docs-only PR.
- The ExecPlan keeps calculator/retrieval/answer/export/runtime implementation
  out of this docs-only PR.
- The ExecPlan keeps SymPy and live acquisition out of scope.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard-implementation.md`

Future implementation may touch only after this plan is reviewed:

- a small guard helper module under `src/sf6_knowledge_coach/`;
- focused unit tests under `tests/`;
- a focused guard validator under `tests/validation/`;
- focused synthetic fixtures under `tests/fixtures/current-facts/` if needed;
- this ExecPlan progress/decision log.

Future implementation must not touch parser/classifier/schema/generated
artifacts unless mandatory review amends this plan first.

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) PR #347 was marked ready and merged with normal merge
  commit `15fd7453bb62505e5f1bde4f9bf331361bec7aa1`.
- [x] (2026-05-24 JST) Local `main` was fast-forwarded to `origin/main` at
  commit `15fd7453bb62505e5f1bde4f9bf331361bec7aa1`.
- [x] (2026-05-24 JST) Confirmed main CI passed for the PR #347 merge commit:
  run `26361621417`.
- [x] (2026-05-24 JST) Created branch
  `plan/annotated-numeric-candidate-consumer-guard-implementation`.
- [x] (2026-05-24 JST) Inspected current consumer surfaces:
  `current_facts.py`, `answering.py`, current-fact schemas/fixtures, and
  parsed-value coverage.
- [x] (2026-05-24 JST) Drafted this docs-only implementation ExecPlan.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete review before implementation approval.

## Decision Log

- Decision: Plan a small helper such as `is_scalar_calculation_input` for
  future consumer code.
  Rationale: Centralized guard logic is less error-prone than repeating
  parsed-value/status checks in each future export, retrieval, answer, or
  calculator surface.
  Date/Author: 2026-05-24 / Codex

- Decision: Require `calculation_input_status` before scalar acceptance.
  Rationale: Parsed shape alone is not enough; `signed_frame` and `integer`
  can still be unsafe without source, authority, and status checks.
  Date/Author: 2026-05-24 / Codex

- Decision: Treat current accepted scalar tests as synthetic contract fixtures
  unless an approved production scalar calculation status already exists.
  Rationale: This guard must not promote any current raw value to
  calculation-safe authority.
  Date/Author: 2026-05-24 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: This plan defines rejection and routing behavior, not arithmetic.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Remaining Risks

- Guard implementation remains future work until a reviewed implementation PR
  lands.
- The exact helper module name and accepted scalar status set must be fixed in
  implementation review.
- Existing `current_facts.py` still reads legacy raw export data and does not
  yet expose parsed-value-backed lookup.
- Future consumers could bypass the helper unless validators require it.
- Same-grammar annotated raw-value expansion remains blocked pending an
  Issue #343-style supplemental double-check gate.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer guard implementation plan | Drafted docs-only plan for future helper/tests/validators that reject non-scalar parsed values in scalar contexts | `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard-implementation.md` | `git diff --check`; `uv lock --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future implementation still required |
| Current surface inventory | Identified `current_facts.py`, `answering.py`, current-fact schemas/fixtures, and future export/retrieval/calculator surfaces | This ExecPlan only | Diff/status review | Passed | None | Implementation review must confirm exact touched files | Existing lookup remains legacy raw export |
| Scope exclusions | No runtime/retrieval/answer/export/calculator/parser/classifier/schema/generated artifact/SymPy/live acquisition changes added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Guard bypass remains possible until implemented |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard-implementation.md.

Check:
- PR diff contains exactly one docs-only ExecPlan file.
- It plans implementation of deterministic guard helpers/validators only.
- It does not implement runtime/retrieval/answer/export/calculator/parser/classifier/schema/generated artifact changes.
- It covers both annotated_numeric_candidate and frame_range as non-scalar parsed values.
- It requires calculation_input_status to carry forward.
- It plans rejection fixtures for annotated_candidate_not_calculation_safe, parsed_range_not_single_value_calculation_safe, review_required values with no parsed_value, and not_numeric_authority values.
- It does not promote any value to calculation-safe, numeric authority, or current-fact authority.
- It keeps SymPy and live acquisition out of scope.
- Issue #343 double-check remains required for future raw-value expansion.

Run:
- git diff --check
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
- git status --short --branch

Return blocking findings first, validation results, PLAN deviations,
remaining risks, and whether docs-only stage/commit is approved.
```
