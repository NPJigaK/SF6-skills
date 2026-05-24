# Annotated Official Parser-Schema Slice Amendment

Status: Drafted for review.

## Purpose

Resolve the two implementation blockers left by
`docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md` before
any parser/schema work starts:

- recovery values containing `全体` / total-duration semantics;
- positive advantage values such as `※1` that lack an explicit `+` sign.

This amendment is docs-only. It does not implement parser, schema, classifier,
calculator, retrieval, answer, export, runtime, SymPy, or live acquisition
behavior.

## Inputs

- `docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`

## Scope

Included:

- Resolve or explicitly defer the two PR #342 blockers:
  - `recovery` values containing `全体` / total-duration semantics;
  - positive `hit_advantage` or `block_advantage` values without an explicit
    plus sign, such as `※1`.
- Narrow the first annotated parser implementation slice where needed.
- Keep all annotated values parse-possible only as condition-bound candidate
  data.
- Keep all annotated values not calculation-safe.
- Preserve `raw_value` exactly.
- Keep note marker, note id, row-note candidate evidence, note text status,
  note scope, source column, and calculation safety separate from any numeric
  token.

Excluded:

- No ambiguous PR #341 groups:
  - `sa_gain`
  - `combo_scaling`
  - `damage`
  - `active`
- No non-note active grammar blockers.
- No parser implementation.
- No schema implementation.
- No classifier behavior changes.
- No calculator or SymPy logic.
- No retrieval, answer, export, or runtime changes.
- No calculation-safe promotion.
- No numeric authority promotion.
- No current-fact authority promotion.
- No live acquisition.

## Amendment Decisions

### Decision 1: Defer Recovery From The First Implementation Slice

The `recovery` source-review group remains `later_annotated_parser_eligible`,
but it is deferred from the first annotated parser implementation slice.

Rationale:

- The group mixes ordinary recovery-like values such as `※16` with
  total-duration-labelled values such as `全体 ※43`.
- `全体` means total duration, not ordinary recovery.
- The current schema does not have an approved annotated `total_duration`
  candidate representation.
- Parsing only the non-`全体` subset while the review item remains mixed would
  make coverage and validator semantics easy to misread.

Required future work:

- Create a separate `total_duration` / recovery split ExecPlan, or add an
  approved annotated total-duration candidate schema before parsing this group.
- Keep `全体 ※NN` values out of ordinary recovery parsers.
- Keep `※16`-style recovery values blocked until the mixed group is split or
  the parser/coverage surfaces can represent safe subset parsing without
  implying the whole group is parsed.

### Decision 2: Defer Positive Advantage Without Explicit Plus Sign

Positive advantage text without an explicit plus sign, such as `※1`, is
deferred from the first annotated parser implementation slice.

Rationale:

- The source column implies advantage polarity, but the raw value does not
  carry an explicit `+`.
- Converting `※1` to `+1` would be a normalization policy decision, not a
  syntactic parse.
- Column-context polarity needs an approved schema field or normalization
  policy before it can be represented safely.

Required future work:

- Add a plus-sign / column-context normalization ExecPlan before parsing
  positive unsigned advantage values.
- Keep `※1` review-required or blocked in the first implementation.
- Add negative fixtures proving `※1` is not silently parsed as `+1`.

### Decision 3: Narrow The First Annotated Parser Implementation Slice

The first annotated parser implementation slice is narrowed to:

| Included target | Review item | Raw-value surface | Planned status |
| --- | --- | --- | --- |
| startup suffix-marker frames | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `122※`, `128※`, and same-shape reviewed startup suffix-marker values | annotated frame candidate, not calculation-safe |
| block advantage explicit negative prefix-marker frames | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `※-4`, `※-2`, and same-shape reviewed explicit negative block-advantage values | annotated signed-frame candidate, not calculation-safe |
| hit advantage explicit negative prefix-marker frames | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `※-3`, `※-1`, `※-4`, and same-shape reviewed explicit negative hit-advantage values | annotated signed-frame candidate, not calculation-safe |

The implementation must not mark an entire mixed review item as safely parsed
if unresolved raw-value variants remain in that same item. If the implementation
cannot represent raw-value-level partial acceptance while keeping blocked
variants blocked, it must defer the whole mixed review item and amend the plan
again.

## Deferred Items

| Deferred item | Reason |
| --- | --- |
| `recovery` group `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | Mixed recovery and total-duration semantics. |
| `全体 ※NN` raw values | Require annotated total-duration schema or field decision. |
| `※16`-style recovery raw values | Deferred with the mixed recovery group until split/subset semantics are approved. |
| `※1` and other positive unsigned advantage values | Require explicit plus-sign / column-context normalization policy. |
| ambiguous `sa_gain`, `combo_scaling`, `damage`, `active` groups | PR #341 marks them `blocked_pending_source_review`. |
| non-note active grammar blockers | Dot/double-dash active grammar remains outside note-linkage parser scope. |

## Parser/Schema Requirements After Amendment

The later implementation ExecPlan must:

- preserve `raw_value` exactly;
- preserve marker placement;
- require literal `※` for this first annotated slice;
- require PR #341 source-review evidence for the target review item;
- extract numeric tokens only into an annotated candidate wrapper or equivalent
  non-scalar structure;
- keep annotation metadata separate from the numeric token;
- keep calculation safety as a closed validated status such as
  `annotated_candidate_not_calculation_safe`;
- ensure calculators, normalized exports, retrieval, and answers cannot consume
  the nested numeric candidate as a plain scalar;
- include negative fixtures for:
  - recovery `全体 ※NN`;
  - recovery `※NN` while the mixed recovery group is deferred;
  - positive advantage `※1`;
  - ambiguous PR #341 groups;
  - non-note active grammar blockers;
  - SuperCombo values.

## Acceptance Criteria

- This docs-only amendment resolves or defers the two PR #342 blockers.
- First implementation targets are narrowed to startup, explicit negative block
  advantage, and explicit negative hit advantage annotated candidates.
- Recovery and total-duration-labelled values are deferred.
- Positive unsigned advantage values are deferred.
- No value becomes calculation-safe.
- No numeric authority or current-fact authority promotion is planned.
- No parser/schema/classifier/calculator/retrieval/answer/export/runtime
  implementation is added.
- No SymPy logic and no live acquisition are planned.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-annotated-official-parser-schema-slice-amendment.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) PR #342 was marked ready and merged with normal merge
  commit `694ab5dbeb4b89fdcf87a75ce775f87512658976`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at the PR
  #342 merge commit.
- [x] (2026-05-24 JST) Confirmed main CI for the PR #342 merge commit passed:
  run `26353226502`.
- [x] (2026-05-24 JST) Created branch
  `plan/annotated-official-parser-schema-amendment`.
- [x] (2026-05-24 JST) Drafted this docs-only amendment ExecPlan.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  `uv lock --check`, official note-linkage source-review validator,
  parsed-value classifier validator, clean-slate validator, and
  `git status --short --branch`.
- [ ] Complete mandatory review before any annotated parser/schema
  implementation.

## Decision Log

- Decision: Defer the recovery group from the first annotated parser
  implementation slice.
  Rationale: The group mixes ordinary recovery-like values with `全体`
  total-duration labels, and no annotated total-duration schema is approved.
  Date/Author: 2026-05-24 / Codex

- Decision: Defer positive unsigned advantage values such as `※1`.
  Rationale: Treating them as positive signed frames requires a reviewed
  plus-sign / column-context normalization policy.
  Date/Author: 2026-05-24 / Codex

- Decision: Narrow the first annotated parser implementation slice to startup
  suffix-marker frames and explicit negative annotated advantage values.
  Rationale: These preserve raw marker semantics without total-duration or
  implicit-plus normalization.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Remaining Risks

- The implementation still needs an approved annotated candidate schema
  placement.
- The classifier coverage surface may need raw-value-level partial acceptance
  to include explicit negative hit advantage while keeping `※1` blocked.
- The deferred recovery group needs a separate total-duration/recovery split
  plan before parsing.
- Ambiguous PR #341 groups may still require additional source-review or
  acquisition support before parser/schema planning.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Annotated official parser/schema amendment | Drafted docs-only plan narrowing the first implementation slice and deferring recovery/positive unsigned advantage blockers | `docs/execplans/2026-05-24-annotated-official-parser-schema-slice-amendment.md` | `git diff --check`; `uv lock --check`; source-review validator; parsed-value classifier validator; clean-slate validator; status check | Passed | None | Review pending | Schema placement and partial coverage still need implementation planning |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-24-annotated-official-parser-schema-slice-amendment.md.

Check:
- recovery values containing 全体 / total-duration semantics are deferred;
- positive advantage values like ※1 without explicit plus sign are deferred;
- first implementation target is narrowed to startup annotated frames,
  explicit negative block_advantage annotated frames, and explicit negative
  hit_advantage annotated frames;
- ambiguous PR #341 groups remain excluded;
- non-note active grammar blockers remain excluded;
- parse possible remains separate from calculation-safe;
- no calculation-safe, numeric authority, or current-fact authority promotion
  is planned;
- no parser/schema/classifier/calculator/retrieval/answer/export/runtime
  implementation is included;
- SymPy and live acquisition remain excluded.

Return decisions, PLAN deviations, remaining risks, and whether docs-only
stage/commit is approved.
```
