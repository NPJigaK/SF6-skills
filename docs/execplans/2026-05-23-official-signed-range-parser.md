# Official Signed Range Parser

Status: Drafted for review.

## Purpose

Plan the smallest parser implementation slice for official signed `～`
advantage ranges only.

This ExecPlan is docs-only. It does not implement parser, schema, classifier,
calculator, retrieval, answer, export, live acquisition, or SymPy changes.

## Inputs

- `docs/execplans/2026-05-23-official-parser-schema-slice.md`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- `contracts/current-facts/parsed_value.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/test_parsed_value_classifier.py`
- `tests/validation/validate_parsed_value_classifier.py`

## Scope

Included:

- Cover exactly these official `review_required` groups:
  - `value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb`
  - `value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69`
- Add a parser rule for official signed Japanese wave-dash advantage ranges:
  - `-12～-1`
  - `-4～-1`
  - `-39～-33`
  - `-28～-23`
- Reuse existing `parsed_value.kind == "frame_range"`.
- Preserve `raw_value` exactly.
- Store parsed endpoints as signed integers.
- Preserve that the range reason is unknown.
- Keep parsed range values out of single-value calculation-safe status.
- Keep official records as `authority_candidate`; parser coverage may improve,
  but calculator authority is not granted.

Excluded:

- No note marker parser.
- No active-window parser.
- No damage parser.
- No scaling parser.
- No `total_duration` parser.
- No calculator or SymPy logic.
- No retrieval, answer, or export changes.
- No SuperCombo parser implementation.
- No numeric authority promotion.
- No live acquisition.

## Exact Target Groups

| # | Review item | Family | Field | Source header | Affected | Representative official raw values | Current status | Planned parser rule |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | `value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb` | `advantage` | `block_advantage` | `硬直差 > ガード` | 3 | `-12～-1`; `-4～-1`; `-39～-33` | `review_required_not_calculation_safe` | `frame_range.official_signed_wave_dash.v1` |
| 2 | `value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69` | `advantage` | `hit_advantage` | `硬直差 > ヒット` | 1 | `-28～-23` | `review_required_not_calculation_safe` | `frame_range.official_signed_wave_dash.v1` |

No other official, SuperCombo, note-bearing, active, damage, scaling, or
`total_duration` groups are in this implementation slice.

## Schema Decision

Existing `parsed_value.kind == "frame_range"` is sufficient for this slice:

```json
{
  "kind": "frame_range",
  "unit": "frame",
  "start": -12,
  "end": -1
}
```

Do not add `range_reason`, `delimiter`, or calculation-safety metadata to
`parsed_value`. The current schema has `additionalProperties: false`, and the
value object should stay focused on machine-readable endpoints and unit.

Do not add metadata to `value_shape` in this slice. The current
`value_shape.schema.json` has `additionalProperties: false`; it can already
carry `classes`, `classifier_status`, `parser_rule_id`, and `review_item_id`.

Use existing surfaces instead:

- `raw_value` preserves the exact `～` delimiter and original source text.
- `value_shape.parser_rule_id` records
  `frame_range.official_signed_wave_dash.v1`.
- coverage policy records that the range reason is unknown and that the parsed
  range is not single-value calculation-safe.

If review decides that `range_reason` must be represented in a public schema
before parsing, implementation must stop and amend this ExecPlan. Do not
silently widen `frame_range`.

## Parser Design

Future implementation should add a narrowly scoped parser helper for official
signed Japanese wave-dash advantage ranges.

Required behavior:

- Match only the literal full-width delimiter `～` for this rule.
- Match signed integer endpoints on both sides.
- Preserve `raw_value` exactly; only use stripped text for matching.
- Store `start` and `end` exactly as signed integers from left to right.
- Do not reorder endpoints.
- Do not collapse the range to one signed frame.
- Reject reversed endpoints rather than reordering them.
- Reject ASCII tilde `~` unless a later review explicitly approves it.
- Reject hyphen-delimited signed ranges for this advantage rule.
- Apply only to the two target official review item IDs in this ExecPlan.

Suggested regex:

```python
OFFICIAL_SIGNED_WAVE_DASH_RANGE_RE = re.compile(r"^([+-]?\\d+)～([+-]?\\d+)$")
```

Suggested parser rule ID:

```text
frame_range.official_signed_wave_dash.v1
```

The rule should be separate from the existing unsigned timing
`frame_range.strict.v1` rule. It must not make SuperCombo ranges parseable and
must not change active-frame parsing.

## Calculation Status

The selected design is: parsed, but not single-value calculation-safe.

Future implementation should not return
`eligible_only_after_domain_source_and_unit_checks` for this rule. These values
are official `authority_candidate` parsed ranges, but the range reason is
unknown. They cannot be consumed by a calculator that expects a single
advantage value.

Preferred coverage status:

```text
parsed_range_not_single_value_calculation_safe
```

If adding that coverage-policy status is rejected in review, keep the two
groups `review_required_not_calculation_safe` and do not parse them until a
range-reason representation is approved. Do not parse them while marking them
as ordinary calculation-eligible numeric values.

## Future Implementation Plan

A later implementation PR may touch only the surfaces required for this slice:

- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/test_parsed_value_classifier.py`
- `tests/validation/validate_parsed_value_classifier.py`, only if validator
  expectations need the new calculation status or coverage counts
- generated parsed-value classifier coverage artifacts, if classifier output
  changes:
  - `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
  - `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`

It must not touch current-fact schemas unless review rejects the schema
decision above and this ExecPlan is amended first.

Expected coverage movement, if the preferred design is approved:

- the two target groups move from `review_required` to
  `parsed_numeric_structured`;
- `calculation_input_status` for those groups becomes
  `parsed_range_not_single_value_calculation_safe`;
- all non-target review-required groups remain unchanged.

## Required Tests

Future tests must prove:

- `-12～-1` parses for the official `block_advantage` target group as:
  `{"kind": "frame_range", "unit": "frame", "start": -12, "end": -1}`;
- `-4～-1`, `-39～-33`, and `-28～-23` parse with signed integer endpoints;
- endpoints are not reordered or collapsed;
- `raw_value` remains exactly the source string containing `～`;
- `value_shape.parser_rule_id` is
  `frame_range.official_signed_wave_dash.v1`;
- calculation status is not single-value calculation-safe;
- ASCII `-12~-1` remains `review_required` unless explicitly approved later;
- note-bearing official values such as `※-4` remain blocked;
- dot and double-dash active values such as `30-34.35`, `20-24.25`, and
  `23--33` remain blocked;
- SuperCombo remains non-authoritative and receives no signed wave-dash range
  parser implementation.

## Acceptance Criteria

- This ExecPlan covers exactly the two official signed `～` advantage range
  groups.
- Existing `frame_range` schema reuse is approved or a blocker is recorded.
- Range reason remains unknown and is not hidden by parser success.
- Parsed ranges are not treated as single-value calculation-safe.
- Raw values are preserved exactly.
- Parser rule ID and test expectations are explicit.
- No implementation changes are made in this docs-only planning unit.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-23-official-signed-range-parser.md`

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
  `plan/official-signed-range-parser`.
- [x] (2026-05-23 JST) Identified the exact two official signed `～`
  advantage range groups.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`.
- [ ] Complete review before implementation approval.

## Decision Log

- Decision: Limit this slice to the two official signed `～` advantage range
  groups.
  Rationale: They are the safest first parser target from the official parser
  schema slice because they require no note handling, active grammar,
  `total_duration`, damage, or scaling parser.
  Date/Author: 2026-05-23 / Codex

- Decision: Reuse existing `parsed_value.kind == "frame_range"`.
  Rationale: The current schema already supports signed integer endpoints and
  `unit == "frame"`. The missing information is range reason and calculation
  safety, not endpoint structure.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep delimiter and range-reason metadata out of `parsed_value`.
  Rationale: `raw_value` preserves the delimiter, `parser_rule_id` identifies
  the parser, and coverage policy can record unknown range reason without
  widening the current-fact parsed value schema.
  Date/Author: 2026-05-23 / Codex

- Decision: Parsed signed ranges are not single-value calculation-safe.
  Rationale: A frame range with unknown reason cannot be consumed by a
  calculator that expects one advantage value.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- The proposed `parsed_range_not_single_value_calculation_safe` status is a
  coverage-policy addition and requires reviewer approval.
- If reviewers require `range_reason` in current-fact schema before parsing,
  this slice must be amended before implementation.
- Future calculators must not consume `frame_range` advantage values as
  single signed frames.
- Accepting only literal `～` may leave visually similar source strings blocked
  until separately reviewed.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only signed range parser plan | Drafted implementation-prep plan for exactly two official signed `～` advantage range groups | `docs/execplans/2026-05-23-official-signed-range-parser.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Calculation status naming needs review |
| Scope exclusions | No parser/schema/classifier/calculator/retrieval/answer/export/live acquisition/SymPy implementation added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan approval required | Later work must not expand beyond target groups |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-23-official-signed-range-parser.md.

Confirm whether it is acceptable as the implementation ExecPlan for only the
two official signed `～` advantage range groups.

Check:
- it covers exactly the two target official review_required groups;
- existing `parsed_value.kind == "frame_range"` is reused appropriately;
- delimiter preservation relies on raw_value, not parsed_value widening;
- range reason remains unknown and is not hidden by parser success;
- parsed signed ranges are not treated as single-value calculation-safe;
- ASCII `~`, note-bearing values, active dot/double-dash values, damage,
  scaling, total_duration, SuperCombo, calculators, retrieval, answers,
  exports, live acquisition, and SymPy remain out of scope.

Return blocking findings first, then PLAN deviations and remaining risks.
```
