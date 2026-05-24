# Annotated Official Parser-Schema Slice

Status: Drafted for review.

## Purpose

Plan the first annotated official parser/schema slice for the `4`
`later_annotated_parser_eligible` source-review groups from PR #341.

This is a docs-only planning unit. It does not implement parser, schema,
classifier, calculator, retrieval, answer, export, runtime, live acquisition,
or SymPy changes.

The central contract is that parse possible and calculation-safe are separate
states. This slice may plan extraction of an annotated numeric token only as
condition-bound candidate data. It must not make the value calculation-safe or
authoritative.

## Inputs

- `docs/execplans/2026-05-24-official-note-linkage-v4-source-review-update.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/validation/validate_official_note_linkage_source_review.py`

## Scope

Included:

- Target only these `4` official groups with
  `later_parser_eligibility == "later_annotated_parser_eligible"`:
  - startup annotated values
  - recovery annotated values
  - block_advantage annotated values
  - hit_advantage annotated values
- Define parser/schema requirements for official annotated values with
  deterministic single-candidate v4 row-note evidence.
- Preserve `raw_value` exactly, including marker placement.
- Represent note metadata separately from the numeric candidate:
  `note_marker`, `note_id`, row note candidate evidence, `note_text_status`,
  `note_scope`, source column, and calculation safety.
- Permit extraction of an annotated numeric token only as condition-bound
  candidate data.
- Keep official records as `authority_candidate` only.
- Define fixture and validator requirements for a later implementation PR.

Excluded:

- No ambiguous groups:
  - `sa_gain`
  - `combo_scaling`
  - `damage`
  - `active`
- No non-note active grammar blockers.
- No parser implementation in this docs-only PR.
- No schema implementation in this docs-only PR.
- No classifier behavior changes.
- No calculator or SymPy logic.
- No retrieval, answer, export, or runtime changes.
- No calculation-safe promotion.
- No numeric authority promotion.
- No current-fact authority promotion.
- No live acquisition.
- No SuperCombo authority promotion or parser implementation.

## Exact Target Groups

| # | Review item | Field | Source header | Affected | Representative raw values | PR #341 result | Planned parser family |
| ---: | --- | --- | --- | ---: | --- | --- | --- |
| 1 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `startup` | `動作フレーム > 発生` | 6 | `122※`; `128※` | `structured_row_note_evidence_found` / `later_annotated_parser_eligible` | annotated unsigned frame candidate |
| 2 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `recovery` | `動作フレーム > 硬直` | 28 | `全体 ※43`; `※16` | `structured_row_note_evidence_found` / `later_annotated_parser_eligible` | annotated frame or total-duration candidate |
| 3 | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `block_advantage` | `硬直差 > ガード` | 6 | `※-4`; `※-2` | `structured_row_note_evidence_found` / `later_annotated_parser_eligible` | annotated signed-frame candidate |
| 4 | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `hit_advantage` | `硬直差 > ヒット` | 4 | `※-3`; `※1` | `structured_row_note_evidence_found` / `later_annotated_parser_eligible` | annotated signed-frame candidate |

These are source-review readiness targets only. They are not parser-approved,
calculation-safe, numeric authority, or current-fact authority.

## Explicitly Excluded Groups

The following PR #341 groups remain out of scope because their v4 source-review
result is `structured_row_note_evidence_ambiguous`:

| Review item | Field | Reason |
| --- | --- | --- |
| `value-shape:official--source_specific_expression--sa` | `sa_gain` | Multiple same-row `※` candidates remain possible. |
| `value-shape:official--source_specific_expression--u_55d872f6091a` | `combo_scaling` | Mixed single and multiple same-row `※` candidate status remains. |
| `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | At least one representative row still has multiple same-row `※` candidates. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `active` | Standalone markers, bracketed ids, and visible/hidden detail concatenation remain mixed. |

The non-note active grammar blocker
`value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1`
also remains out of scope.

## Schema Requirements

The current `parsed_value` schema supports scalar numeric kinds such as
`integer` and `signed_frame`, but it has no annotation wrapper. The current
`value_shape` schema also has no place for note metadata. A later
implementation must not strip `※` and emit a plain scalar `parsed_value`.

Required representation:

- `raw_value`: exact source string, unchanged.
- numeric candidate: the numeric token extracted from the annotated value,
  stored as condition-bound candidate data only.
- annotation metadata:
  - `note_marker`
  - `note_id`
  - row note candidate count and linkage status
  - `note_text_status`
  - `note_scope`
  - source column header path
  - marker placement, such as prefix, suffix, or label-separated
- calculation gate:
  - explicit status meaning not calculation-safe
  - explicit reason that the value is condition-bound and needs later
    reviewed domain semantics

Preferred schema direction for implementation review:

- Do not reuse plain `parsed_value.kind == "integer"` or
  `parsed_value.kind == "signed_frame"` for annotated values.
- Add an explicit annotated candidate representation, with a planning label
  such as `annotated_numeric_candidate`.
- Keep the nested numeric token separate from annotation metadata and
  calculation safety.
- Keep calculators and exports from treating the nested candidate as a normal
  scalar by requiring them to check the outer annotated candidate kind and
  calculation status.

Planning labels are not approved public interfaces until the implementation
ExecPlan is reviewed.

## Parser Requirements

Future parser rules must be target-ID-limited and field-aware.

Suggested planning parser rule IDs:

- `annotated_frame.official_suffix_marker.v1` for `122※` and `128※`
- `annotated_frame.official_prefix_marker.v1` for `※16`
- `annotated_total_duration.official_label_marker.v1` for `全体 ※43`
- `annotated_signed_frame.official_prefix_marker.v1` for `※-4`, `※-2`,
  and `※-3`
- `annotated_signed_frame.official_prefix_marker.column_context.v1` for
  `※1` in `hit_advantage`, because positive advantage lacks an explicit plus
  sign and depends on the `硬直差 > ヒット` column context

Required behavior:

- Match only the literal official marker `※` for this slice.
- Preserve `raw_value` exactly.
- Preserve marker placement.
- Require PR #341 v4 source-review status:
  `structured_row_note_evidence_found`.
- Require one row note candidate for representative values.
- Require `source_name == "official"` and `source_role == "authority_candidate"`.
- Require source column header and field key to match the target group.
- Reject records from ambiguous groups even if their surface syntax resembles a
  target.
- Reject SuperCombo values.
- Reject note id or bracketed active values in this slice.
- Reject dot and double-dash active grammar in this slice.

## Calculation Safety

All planned annotated values remain not calculation-safe.

The implementation must add or reuse a calculation-input status that means:

```text
annotated_candidate_not_calculation_safe
```

The exact status name is a review decision, but it must be a closed, validated
status. It must not be a free-form string and must not be equivalent to
`eligible_only_after_domain_source_and_unit_checks`.

The status blocks scalar calculators, normalized scalar export, exact numeric
answers, and current-fact authority promotion. A later calculator ExecPlan must
explicitly decide which annotated candidate kinds, if any, can be consumed
under which reviewed conditions.

## Field-Specific Decisions

### Startup

`122※` and `128※` are suffix-marker frame candidates. The inner numeric token
can be parsed as an unsigned frame candidate, but the note says the value is
condition-bound. It is not a normal startup frame for calculation.

### Recovery

`※16` can be an annotated frame candidate. Values like `全体 ※43` must not be
modeled as ordinary recovery. They require a total-duration candidate path or a
separate `total_duration` field decision before implementation.

If the implementation cannot represent `全体` separately from recovery, it must
leave those records review-required and parse only the reviewed non-`全体`
recovery marker forms, or stop and amend this ExecPlan.

### Block Advantage

`※-4` and `※-2` can be annotated signed-frame candidates only. They cannot be
used as exact block advantage because the note condition is part of the value.
Embedded alternate forms remain out of scope unless represented by explicit
fixtures and parser rules.

### Hit Advantage

`※-3` can be an annotated signed-frame candidate. `※1` must preserve that the
positive sign is column-context-dependent; the parser may not silently convert
it into an unconditional `+1` scalar.

## Fixture And Validator Requirements

A later implementation PR must include focused fixtures proving:

- the four target review item IDs are the only annotated groups accepted;
- `122※`, `128※`, `※16`, `全体 ※43`, `※-4`, `※-2`, `※-3`, and `※1`
  preserve `raw_value` exactly;
- marker placement is represented;
- row note candidate count and linkage status come from PR #341 source-review
  evidence, not parser inference;
- ambiguous groups remain blocked:
  `sa_gain`, `combo_scaling`, `damage`, and `active`;
- non-note active grammar blockers remain blocked:
  `30-34.35`, `20-24.25`, and `23--33`;
- no SuperCombo value becomes parseable or authoritative through this slice;
- no annotated candidate has calculation-safe status;
- no annotated candidate is exported as plain `integer` or `signed_frame`.

Validators must be evidence-first and grounded in source-review artifacts,
schema fixtures, and approved coverage policy. They must not be weakened to
fit generated output.

## Future Implementation Files

A later implementation ExecPlan may touch:

- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`, only if the
  chosen annotation placement requires a new record-level field
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- focused parser/classifier tests
- focused schema/validator tests
- generated parsed-value classifier coverage artifacts, if classifier output
  changes
- this ExecPlan

It must not touch retrieval, answer behavior, normalized exports, calculators,
live acquisition, or SuperCombo parser/authority behavior.

## Acceptance Criteria

- This docs-only ExecPlan targets exactly the `4`
  `later_annotated_parser_eligible` official groups from PR #341.
- The ambiguous `sa_gain`, `combo_scaling`, `damage`, and `active` groups are
  excluded.
- Non-note active grammar blockers are excluded.
- Parser/schema requirements preserve raw values and annotation metadata.
- Numeric extraction is planned only as condition-bound candidate data.
- Calculation safety remains separate and blocked.
- No numeric authority or current-fact authority promotion is planned.
- No implementation changes are made.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md`

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

- [x] (2026-05-24 JST) PR #341 was marked ready and merged with normal merge
  commit `644ef66df307ab0cbbddd4ce5f1ef39432ef486e`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at the PR
  #341 merge commit.
- [x] (2026-05-24 JST) Confirmed main CI for the PR #341 merge commit passed:
  run `26352931513`.
- [x] (2026-05-24 JST) Created branch
  `plan/annotated-official-parser-schema-slice`.
- [x] (2026-05-24 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  `uv lock --check`, official note-linkage source-review validator,
  parsed-value classifier validator, clean-slate validator, and
  `git status --short --branch`.
- [ ] Complete mandatory review before parser/schema implementation.

## Decision Log

- Decision: Limit this plan to the four PR #341
  `later_annotated_parser_eligible` groups.
  Rationale: They have deterministic single-candidate v4 row-note evidence;
  ambiguous groups do not.
  Date/Author: 2026-05-24 / Codex

- Decision: Do not parse annotated values as plain scalar `parsed_value`
  records.
  Rationale: A plain scalar would invite calculator/export misuse and would
  hide the condition carried by the note marker.
  Date/Author: 2026-05-24 / Codex

- Decision: Keep calculation safety as a separate validated status.
  Rationale: Syntax extraction does not prove domain conditions, calculator
  eligibility, or numeric authority.
  Date/Author: 2026-05-24 / Codex

- Decision: Treat `全体` recovery-column forms as a schema blocker unless a
  total-duration candidate representation is approved.
  Rationale: `全体` means total duration, not ordinary recovery, even when it
  appears in the recovery-column surface.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Unresolved Schema Decisions

- Whether annotated candidate data belongs inside a new `parsed_value` kind,
  inside `value_shape`, or in a new record-level annotation field.
- Exact public name for the annotated candidate kind or wrapper.
- Exact closed calculation-input status name for condition-bound annotated
  candidates.
- Whether `全体 ※NN` should be included in the first implementation slice or
  held until a `total_duration` candidate schema is approved.
- Whether positive unsigned advantage text such as `※1` should be represented
  as a signed-frame candidate with column-context metadata or kept blocked
  until explicit plus-sign normalization policy is approved.

## Risks

- If annotation metadata is placed too close to scalar `parsed_value`, future
  exports or calculators may accidentally consume condition-bound values.
- The recovery group mixes ordinary recovery-like frames and `全体` total
  duration labels.
- `later_annotated_parser_eligible` is source-review readiness only; reviewers
  may still decide to reduce the first implementation slice.
- Ambiguous groups may look syntactically similar to target groups and require
  explicit negative fixtures.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Annotated official parser/schema slice plan | Drafted docs-only plan for the 4 PR #341 later-eligible groups | `docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md` | `git diff --check`; `uv lock --check`; source-review validator; parsed-value classifier validator; clean-slate validator; status check | Passed | None | Review pending | Schema placement still requires review |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md.

Check:
- it targets only the 4 PR #341 later_annotated_parser_eligible groups:
  startup, recovery, block_advantage, and hit_advantage;
- it excludes ambiguous sa_gain, combo_scaling, damage, and active groups;
- it excludes non-note active grammar blockers;
- it separates parse possible from calculation-safe;
- it preserves raw_value exactly;
- it represents note marker, note id, row-note candidate evidence, note text
  status, note scope, source column, and calculation safety separately;
- it does not approve parser/schema/classifier/calculator/retrieval/answer/
  export/runtime implementation;
- it does not use SymPy or live acquisition;
- unresolved schema decisions are explicit.

Return findings, unresolved schema decisions, PLAN deviations, and whether
the docs-only ExecPlan is stage/commit ready.
```
