# Frame Range Consumer Guard

Status: Drafted for review.

## Purpose

Plan the contract that prevents parsed `frame_range` advantage values from
being consumed as single-frame values by future normalized exports, retrieval,
answer preparation, or calculators.

This ExecPlan is docs-only. It does not implement runtime, export, calculator,
retrieval, answer, parser, classifier, schema, generated coverage artifact, or
SymPy changes.

## Context

PR #334 introduced two official parsed range records:

- `value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb`
- `value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69`

They have:

- `parsed_value.kind == "frame_range"`
- parser rule `frame_range.official_signed_wave_dash.v1`
- `calculation_input_status == "parsed_range_not_single_value_calculation_safe"`
- `source_name == "official"`
- `source_role == "authority_candidate"`
- field domain `block_advantage` or `hit_advantage`

The parsed endpoints are useful structure, but the range reason is unknown.
The left and right endpoints must not be interpreted as best/worst, min/max
policy, matchup state, spacing state, or a single exact value unless a later
reviewed range-aware contract says so.

## Scope

Included:

- Define future guard behavior only.
- Ensure future exports preserve `frame_range` as an interval/range, never a
  scalar.
- Ensure future calculators reject `frame_range` unless a specific
  range-aware calculator contract is approved.
- Ensure future answer generation can display the range with caveat, but
  cannot answer as a single exact value.
- Ensure future retrieval and numeric tables can index the value as range
  metadata only, not exact scalar advantage.
- Define validator expectations for any future export or calculator that
  consumes `parsed_value`.

Excluded:

- No export implementation.
- No calculator implementation.
- No SymPy calculation logic.
- No parser or classifier changes.
- No schema changes.
- No generated coverage artifact changes.
- No answer, retrieval, or runtime changes.
- No authority promotion.

## Guard Contract

Future consumers must treat `frame_range` advantage values as structured range
metadata unless a later approved range-aware contract explicitly opts in.

Any future consumer that reads parsed current-fact values must check:

- `parsed_value.kind`
- `calculation_input_status`
- `value_shape.parser_rule_id`
- `source_name`
- `source_role`
- `field_key`
- source family or domain

For the PR #334 records, the effective guard is:

```text
parsed_value.kind == frame_range
and calculation_input_status == parsed_range_not_single_value_calculation_safe
and value_shape.parser_rule_id == frame_range.official_signed_wave_dash.v1
and source_name == official
and source_role == authority_candidate
and field_key in {block_advantage, hit_advantage}
```

If all of these hold, scalar consumers must reject the value. They may carry
the raw value, parser metadata, and interval endpoints as non-scalar metadata.

## Future Export Contract

Future normalized exports must not convert these values to `signed_frame`.
They must not emit `value`, `exact_frame`, `advantage`, `best`, `worst`,
`min`, `max`, or any equivalent single-frame scalar field derived from the
range endpoints.

Acceptable future export behavior:

- preserve `parsed_value.kind == "frame_range"` with left/right endpoints;
- preserve `raw_value`;
- preserve or reference `calculation_input_status`;
- mark the value as not scalar calculation-safe;
- optionally expose explicit interval metadata for display or filtering.

Blocked export behavior:

- collapse `-12～-1` to `-12`, `-1`, an average, or any preferred endpoint;
- sort endpoints into numeric low/high and present them as best/worst;
- treat official `authority_candidate` as current-fact authority;
- omit the not-single-value calculation status.

## Future Calculator Contract

Future calculators that expect scalar advantage must reject these records.
The rejection should be deterministic and explain that the parsed value is a
range with unknown range reason.

A range-aware calculator may consume these records only after a separate
approved ExecPlan defines:

- accepted `parser_rule_id` values;
- allowed field domains;
- whether left/right order, numeric low/high, or explicit labels are used;
- required range-reason evidence;
- output semantics and caveats;
- tests proving scalar calculators still reject the range.

SymPy is not needed for this guard plan because no arithmetic is implemented.
If a later range-aware calculator performs interval arithmetic, that belongs
in a separate calculator ExecPlan.

## Future Retrieval And Answer Contract

Future retrieval and numeric tables may index these records as range metadata
for filtering, display, or review triage. They must not index them as exact
scalar advantage values.

Future answer preparation may display the raw range with a caveat, for example
that the official value is a parsed range whose reason is not yet reviewed. It
must not answer questions that require a single exact frame value using these
records alone.

If a user asks for an exact punish, exact frame advantage, or calculator result,
the answer surface must route away from these records unless a later
range-aware tool is approved.

## Validator Expectations For Future Work

Any future export, retrieval table, answer-prep artifact, or calculator that
consumes `parsed_value` should add evidence-first validators that prove:

- `frame_range` records with
  `parsed_range_not_single_value_calculation_safe` are rejected by scalar
  calculators;
- official signed wave-dash range records remain `authority_candidate` unless
  a separate authority promotion plan is approved;
- raw delimiter and raw value remain available for display;
- interval endpoints are preserved left/right and are not silently reordered;
- numeric low/high are not labeled best/worst without reviewed range reason;
- `frame_range` is not exported as `signed_frame`;
- retrieval indexes these records as range metadata only;
- answer preparation includes caveat text or declines exact-value answers;
- SuperCombo or non-official ranges do not inherit authority through this
  guard.

Validators must not be weakened to match generated output. Each validator must
be grounded in a schema contract, coverage artifact, synthetic contract
fixture, or reviewed policy artifact.

## Required Decisions

- `frame_range` is parse-structured but not single-value calculation-safe.
- `parsed_range_not_single_value_calculation_safe` must block scalar
  calculators.
- Future guards must check `parsed_value.kind`, `calculation_input_status`,
  `parser_rule_id`, source role, and field domain.
- Range endpoints preserve left/right source order. Numeric low/high must not
  be conflated with best/worst without reviewed range reason.
- No SymPy use is needed for this guard plan because no arithmetic is
  implemented.

## Acceptance Criteria

- The ExecPlan defines guard behavior for future exports, calculators,
  retrieval, and answer preparation.
- The ExecPlan forbids scalar consumption of `frame_range` advantage values
  with `parsed_range_not_single_value_calculation_safe`.
- The ExecPlan requires future validators before any export or calculator
  consumes parsed `frame_range` values.
- The ExecPlan does not implement runtime/export/calculator/retrieval/answer
  changes.
- The ExecPlan does not modify parser/classifier behavior, schemas, or
  generated coverage artifacts.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-23-frame-range-consumer-guard.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Created branch
  `plan/frame-range-consumer-guard`.
- [x] (2026-05-23 JST) Confirmed PR #334 parsed range context from the
  coverage artifact.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`.
- [ ] Complete review before implementation approval.

## Decision Log

- Decision: Treat parsed `frame_range` advantage values as range metadata, not
  scalar frame values.
  Rationale: PR #334 made the values parse-structured but explicitly not
  single-value calculation-safe.
  Date/Author: 2026-05-23 / Codex

- Decision: Put future consumer guards in export/retrieval/answer/calculator
  contracts and validators, not in the parsed value schema.
  Rationale: Existing `frame_range` stores endpoint structure; consumer safety
  is determined by status, parser rule, source role, and field domain.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not use SymPy in this guard plan.
  Rationale: This plan defines rejection and routing behavior, not arithmetic.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- Future code could bypass the guard if it consumes `parsed_value.kind` without
  also checking `calculation_input_status`.
- A future export schema may need an explicit non-scalar status field if it
  does not carry classifier coverage metadata forward.
- Displaying a range without caveat could still imply an exact value to users.
- Range-aware calculator semantics remain undefined until a separate ExecPlan.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frame range consumer guard plan | Drafted docs-only guard contract for future export/retrieval/answer/calculator consumers | `docs/execplans/2026-05-23-frame-range-consumer-guard.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future consumers still need implementation |
| Scope exclusions | No runtime/export/calculator/retrieval/answer/parser/classifier/schema/artifact changes added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Guard bypass remains possible until implemented |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-23-frame-range-consumer-guard.md.

Confirm whether it is acceptable as the docs-only guard contract plan for
future consumers of parsed frame_range advantage values.

Check:
- it is docs-only and changes no runtime/export/calculator/retrieval/answer/parser/classifier/schema/generated artifacts;
- it prevents frame_range advantage values with parsed_range_not_single_value_calculation_safe from being consumed as scalar signed_frame values;
- it requires future consumers to check parsed_value.kind, calculation_input_status, parser_rule_id, source role, and field domain;
- it preserves left/right endpoints without conflating numeric low/high with best/worst;
- it allows display with caveat but forbids exact single-value answers;
- it keeps SymPy and arithmetic out of scope.

Return blocking findings first, then PLAN deviations and remaining risks.
```
