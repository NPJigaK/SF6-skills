# Annotated Numeric Candidate Consumer Guard

Status: Drafted for review.

## Purpose

Plan the contract that prevents parsed
`parsed_value.kind == "annotated_numeric_candidate"` records from being
consumed as scalar integer, `signed_frame`, or calculation input values by
future normalized exports, retrieval tables, answer preparation, calculators,
or current-fact consumers.

This ExecPlan is docs-only. It does not implement calculator, retrieval,
answer, export, runtime, parser, classifier, schema, generated coverage
artifact, live acquisition, or SymPy changes.

## Context

PR #346 introduced official annotated numeric candidates for the narrowed
Issue #343 double-check-passed raw values only.

The affected official coverage records are:

- `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100`
  for `startup`;
- `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb`
  for `block_advantage`;
- `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69`
  for `hit_advantage`.

They have:

- `parsed_value.kind == "annotated_numeric_candidate"` for approved raw
  variants;
- parser rule `annotated_frame.official_suffix_marker.v1` or
  `annotated_signed_frame.official_prefix_marker.negative.v1`;
- `calculation_input_status == "annotated_candidate_not_calculation_safe"`;
- `source_name == "official"`;
- `source_role == "authority_candidate"`;
- top-level `classifier_decision == "partial_raw_value_coverage"`.

Coverage currently records seven parsed annotated raw variants and five
blocked raw variants:

- parsed: `122※`, `128※`, block `※-4`, block `※-2`, hit `※-3`,
  hit `※-1`, hit `※-4`;
- blocked: `124※`, block `※-15`, block `※-5`, block `※-10`, `※1`.

The nested numeric token is useful for display and search metadata, but it is
condition-bound by official note text. It is not a scalar current fact and is
not calculation-safe.

## Scope

Included:

- Define future guard behavior only.
- Ensure future normalized exports do not flatten
  `annotated_numeric_candidate` into `integer`, `signed_frame`, `value`,
  `exact_frame`, or equivalent scalar fields.
- Ensure future retrieval and numeric tables can index annotated candidates
  only as display/search metadata, not exact scalar values.
- Ensure future answer preparation can display the raw annotated value with
  caveat, but cannot answer exact frame, punish, damage, or calculator
  questions from the nested numeric candidate.
- Ensure future scalar calculators reject annotated candidates unless a later
  condition-aware calculator contract is approved.
- Define validator expectations for future consumers that read
  `parsed_value`.
- Preserve the requirement that Issue #343-style double-check gates are needed
  before expanding to additional raw-value variants.

Excluded:

- No calculator implementation.
- No SymPy logic.
- No retrieval implementation.
- No answer behavior changes.
- No export implementation.
- No runtime changes.
- No parser or classifier changes.
- No schema changes.
- No generated coverage artifact changes.
- No live acquisition.
- No calculation-safe promotion.
- No numeric authority or current-fact authority promotion.

## Guard Contract

Future consumers must treat `annotated_numeric_candidate` as non-scalar
metadata unless a later approved condition-aware contract explicitly opts in.

Any future consumer that reads parsed current-fact values must check:

- `parsed_value.kind`;
- `calculation_input_status`;
- `value_shape.parser_rule_id`;
- `source_name`;
- `source_role`;
- field domain;
- note linkage and annotation metadata when available.

The effective guard for PR #346 records is:

```text
parsed_value.kind == annotated_numeric_candidate
and calculation_input_status == annotated_candidate_not_calculation_safe
and value_shape.parser_rule_id in {
  annotated_frame.official_suffix_marker.v1,
  annotated_signed_frame.official_prefix_marker.negative.v1
}
and source_name == official
and source_role == authority_candidate
and field_key in {startup, block_advantage, hit_advantage}
```

If these hold, scalar consumers must reject the value. They may carry the raw
value, note metadata, parser metadata, field domain, and nested numeric
candidate as display/search metadata only.

The guard must follow the status, not just the parsed kind. A future consumer
that copies parsed values forward must also carry
`annotated_candidate_not_calculation_safe` or an equivalent reviewed
non-scalar status.

## Future Export Contract

Future normalized exports must not flatten annotated candidates into scalar
facts. They must not emit `integer`, `signed_frame`, `value`, `exact_frame`,
`advantage`, `startup`, or any equivalent scalar field derived from the nested
numeric candidate unless a later condition-aware export contract is approved.

Acceptable future export behavior:

- preserve `parsed_value.kind == "annotated_numeric_candidate"`;
- preserve `raw_value`;
- preserve or reference `calculation_input_status`;
- preserve note marker, note linkage status, note scope, source column, and
  parser rule metadata;
- mark the exported value as not scalar calculation-safe;
- optionally expose the nested numeric candidate for display/search metadata.

Blocked export behavior:

- convert `※-4` to plain `-4`;
- convert `122※` to plain `122`;
- export nested values as `signed_frame`, `integer`, or exact current facts;
- omit the annotated non-calculation-safe status;
- promote official `authority_candidate` values to current-fact authority.

## Future Retrieval And Answer Contract

Future retrieval tables may index annotated candidates for display, filtering,
or review triage. They must not index them as exact scalar frame values.

Future answer preparation may display the raw annotated value with a caveat
that it is note-bound and not calculation-safe. It must not answer exact frame,
punish, damage, route, or calculator questions from the nested candidate
alone.

If a user asks for an exact scalar value, exact punish, or calculator result,
the answer surface must reject or route away from these records unless a later
condition-aware tool is approved.

## Future Calculator Contract

Scalar calculators must reject `annotated_numeric_candidate` records.

The rejection should be deterministic and explain that the parsed value is a
note-bound annotated candidate whose condition has not been modeled as a
calculation-safe input.

A condition-aware calculator may consume these records only after a separate
approved ExecPlan defines:

- accepted parser rule IDs;
- accepted field domains;
- required note text, note scope, and condition evidence;
- how condition truth is established at calculation time;
- output semantics and caveats;
- validators proving scalar calculators still reject annotated candidates;
- tests proving unresolved or blocked raw variants remain excluded.

SymPy is not needed for this guard plan because no arithmetic is implemented.
If a later condition-aware calculator performs exact arithmetic, that belongs
in a separate calculator ExecPlan after the value and condition contracts are
approved.

## Future Current-Fact Consumer Contract

Future current-fact consumers must not treat the nested numeric candidate as
the fact value. The outer wrapper is the fact shape.

Consumers must distinguish:

- raw official value;
- parsed annotation metadata;
- nested numeric candidate;
- calculation input status;
- source role and authority status.

`authority_candidate` remains insufficient for current-fact authority
promotion. A later authority promotion plan would need separate evidence,
schema, and validator changes.

## Raw-Value Expansion Gate

Issue #343-style double-check remains required for any future expansion to
additional annotated raw values.

Same-grammar raw values that were not in the PR #346 double-check gate remain
blocked until a later plan provides:

- a targeted Scrapling screenshot bundle;
- human ChatGPT/VLM observation recorded as `observation_candidate` only;
- deterministic artifact and reviewer evidence alignment;
- validator updates that keep blocked variants blocked unless explicitly
  approved.

ChatGPT/VLM output remains reviewer-only observation. It is not source truth,
validator evidence, parser approval, calculation-safe promotion, or authority
promotion.

## Validator Expectations For Future Work

Any future export, retrieval table, answer-prep artifact, current-fact
consumer, or calculator that consumes `parsed_value` should add evidence-first
validators proving:

- `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe` are rejected by scalar
  calculators;
- normalized exports do not flatten annotated candidates to `integer` or
  `signed_frame`;
- retrieval indexes annotated candidates only as metadata;
- answer preparation displays caveats or declines exact-value answers;
- current-fact consumers preserve the outer wrapper and status;
- official `authority_candidate` is not promoted to current-fact authority;
- blocked raw variants remain blocked unless a later double-check gate and
  ExecPlan approve expansion;
- no SuperCombo values inherit authority through this guard.

Validators must not be weakened to match generated output. Each validator must
be grounded in a schema contract, coverage artifact, synthetic contract
fixture, reviewed policy artifact, or privacy/security boundary.

## Required Decisions

- `annotated_numeric_candidate` is parse-structured but not scalar
  calculation-safe.
- `annotated_candidate_not_calculation_safe` must block scalar calculators and
  exact-answer paths.
- Future guards must check parsed kind, calculation status, parser rule,
  source role, and field domain.
- Annotated candidates are display/search metadata only until a later
  condition-aware contract is approved.
- No SymPy use is needed for this guard plan because no arithmetic is
  implemented.
- Issue #343 double-check remains mandatory for future raw-value expansion.

## Acceptance Criteria

- The ExecPlan defines guard behavior for future export, retrieval, answer,
  calculator, runtime, and current-fact consumers.
- The ExecPlan forbids scalar consumption of
  `annotated_numeric_candidate` values with
  `annotated_candidate_not_calculation_safe`.
- The ExecPlan requires future validators before any consumer reads annotated
  candidates.
- The ExecPlan keeps annotated candidates display/search metadata only until a
  later condition-aware contract.
- The ExecPlan keeps SymPy and arithmetic out of scope.
- The ExecPlan does not implement parser, classifier, calculator, retrieval,
  answer, export, runtime, schema, or generated artifact changes.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard.md`

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

- [x] (2026-05-24 JST) PR #346 was marked ready and merged with normal merge
  commit `3d65d68dcb41ba0f10cdbc7436a2da37dff9d4ee`.
- [x] (2026-05-24 JST) Local `main` was fast-forwarded to `origin/main` at
  commit `3d65d68dcb41ba0f10cdbc7436a2da37dff9d4ee`.
- [x] (2026-05-24 JST) Confirmed main CI passed for the PR #346 merge commit:
  run `26360864490`.
- [x] (2026-05-24 JST) Created branch
  `plan/annotated-numeric-candidate-consumer-guard`.
- [x] (2026-05-24 JST) Confirmed annotated candidate coverage context from
  the parsed-value classifier coverage artifact.
- [x] (2026-05-24 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete review before implementation approval.

## Decision Log

- Decision: Treat annotated numeric candidates as display/search metadata, not
  scalar frame values.
  Rationale: PR #346 made the values parse-structured but explicitly not
  calculation-safe.
  Date/Author: 2026-05-24 / Codex

- Decision: Put consumer guards in future export/retrieval/answer/calculator
  and current-fact consumer contracts and validators.
  Rationale: The parsed-value schema can represent the non-scalar wrapper, but
  misuse prevention happens where values are consumed.
  Date/Author: 2026-05-24 / Codex

- Decision: Require `annotated_candidate_not_calculation_safe` to carry
  forward with any future consumer artifact.
  Rationale: Consumers must not infer safety from the nested numeric token.
  Date/Author: 2026-05-24 / Codex

- Decision: Do not use SymPy in this guard plan.
  Rationale: This plan defines rejection and routing behavior, not arithmetic.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Risks

- Future code could bypass the guard if it reads
  `parsed_value.numeric_candidate.value` without checking the outer kind and
  calculation status.
- A future export schema may need an explicit non-scalar status field if it
  does not carry classifier coverage metadata forward.
- Displaying an annotated value without caveat could imply an exact current
  fact.
- Condition-aware calculator semantics remain undefined until a separate
  ExecPlan.
- Future raw-value expansion could accidentally parse same-grammar variants
  without a supplemental Issue #343-style double-check gate.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Annotated numeric candidate consumer guard plan | Drafted docs-only guard contract for future export/retrieval/answer/calculator/runtime/current-fact consumers | `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard.md` | `git diff --check`; `uv lock --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future consumers still need implementation |
| Scope exclusions | No parser/classifier/calculator/retrieval/answer/export/runtime/schema/generated artifact changes added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Guard bypass remains possible until implemented |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard.md.

Confirm whether it is acceptable as the docs-only guard contract plan for
future consumers of parsed annotated numeric candidates.

Check:
- it is docs-only and changes no parser/classifier/calculator/retrieval/answer/export/runtime/schema/generated artifacts;
- annotated candidates are display/search metadata only until a later condition-aware contract;
- scalar calculators and exact-answer paths must reject annotated_numeric_candidate;
- calculation_input_status == annotated_candidate_not_calculation_safe is mandatory to carry forward;
- future consumers must check parsed_value.kind, calculation_input_status, parser_rule_id, source role, and field domain;
- normalized exports must not flatten nested numeric candidates to integer or signed_frame;
- Issue #343 double-check remains required for future raw-value expansion;
- SymPy and arithmetic remain out of scope.

Return blocking findings first, then PLAN deviations and remaining risks.
```
