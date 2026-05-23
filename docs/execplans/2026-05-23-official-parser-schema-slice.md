# Official Parser-Schema Slice

Status: Drafted for review; external evidence recorded.

## Purpose

Plan the first parser/schema implementation slice for the `11` official
authority-candidate groups that remain `review_required` in parsed-value
classifier coverage.

This ExecPlan is docs-only. It does not implement parser, schema, validator,
calculator, retrieval, answer, export, live acquisition, or SymPy changes.

## Inputs

- `docs/execplans/2026-05-23-review-required-parser-schema-expansion.md`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `contracts/current-facts/*.schema.json`
- `docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md`
  for mechanics context only, not as authority for official values.

## Scope

Included:

- Cover only records where `source_name == "official"` and
  `classifier_decision == "review_required"`.
- Explicitly plan the `11` official groups across `startup`, `active`,
  `recovery`, `hit_advantage`, `block_advantage`, `damage`, `sa_gain`, and
  `combo_scaling`.
- Decide which existing `parsed_value` kinds can be reused.
- Decide which new schema wrappers are needed before parsing note-bearing or
  source-specific official expressions.
- Preserve raw official values exactly.
- Keep official records as `authority_candidate` until parser/schema
  validation and review are complete.
- Keep SuperCombo out of implementation scope except as non-authoritative
  comparison context for expression shapes.

Excluded:

- No SuperCombo parser implementation.
- No calculator implementation.
- No SymPy calculation logic.
- No retrieval or answer behavior changes.
- No normalized export generation.
- No numeric authority promotion.
- No live acquisition.
- No LLM interpretation of raw values as facts.
- No validator or data artifact edits in this docs-only planning unit.

## Current Official Coverage

The official `review_required` groups are:

| # | Review item | Family | Field | Source header | Affected | Representative official raw values | Required direction |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | `value-shape:official--source_specific_expression--sa` | `gauge` | `sa_gain` | `SAゲージ増加` | 8 | `※3000`; `※2150` | Requires note-aware Super Art gauge wrapper; blocked if note text is not reviewed. |
| 2 | `value-shape:official--source_specific_expression--u_55d872f6091a` | `scaling` | `combo_scaling` | `コンボ補正値` | 55 | `※即時補正10%`; `※即時補正10％`; `※始動補正30%コンボ補正20%`; `※即時補正20%`; `※即時補正10％コンボ補正20%` | Requires scaling-rule schema; note-bearing values stay blocked without reviewed note linkage. |
| 3 | `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | `damage` | `ダメージ` | 36 | `※500`; `※600`; `※700`; `※900`; `※1000` | Requires note-aware damage wrapper; parse only after cell and `ダメージ` column boundary confirmation. |
| 4 | `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `timing` | `active` | `動作フレーム > 持続` | 3 | `30-34.35`; `20-24.25`; `23--33` | Source-confirmed raw official notation; dot and double-dash semantics remain blocked pending grammar policy. |
| 5 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `timing` | `active` | `動作フレーム > 持続` | 44 | `※`; `[※2] 1-12`; `6-366-11, 13-18※,20-25, 34-36`; `7-377-12,14-19※, 21-26, 35-37`; `8-388-13, 15-20※, 22-27, 36-38` | Requires visible-text and hidden-detail separation; concatenated strings are not valid active grammar. |
| 6 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `timing` | `startup` | `動作フレーム > 発生` | 6 | `122※`; `124※`; `128※` | Existing integer frame value can be inner value; note wrapper required before parsing. |
| 7 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `timing` | `recovery` | `動作フレーム > 硬直` | 28 | `全体 ※43`; `全体 ※42`; `※16`; `※17`; `※20` | `全体 N` should model `total_duration`, not recovery, after note and label review. |
| 8 | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `advantage` | `block_advantage` | `硬直差 > ガード` | 6 | `※-4`; `※-15`; `※-5`; `※-10`; `※-2` | Existing `signed_frame` can be inner value; note wrapper required before parsing. |
| 9 | `value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb` | `advantage` | `block_advantage` | `硬直差 > ガード` | 3 | `-12～-1`; `-4～-1`; `-39～-33` | Reuse existing `frame_range` syntax; range reason remains unknown and not single-value calculation-safe. |
| 10 | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `advantage` | `hit_advantage` | `硬直差 > ヒット` | 4 | `※-3`; `※-1`; `※-4`; `※1` | Existing `signed_frame` can be inner value; note wrapper required before parsing. |
| 11 | `value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69` | `advantage` | `hit_advantage` | `硬直差 > ヒット` | 1 | `-28～-23` | Reuse existing `frame_range` syntax; range reason remains unknown and not single-value calculation-safe. |

## Required Decisions

### Existing Kinds To Reuse

- `signed_frame`: reuse for plain signed advantage values after note handling
  is resolved. Do not strip `※` and parse as plain `signed_frame`.
- `frame_range`: reuse for official signed advantage ranges such as
  `-12～-1` and `-28～-23`; the schema already supports integer endpoints.
  The implementation needs a new parser rule for signed `～` ranges, not a new
  parsed kind.
- `integer`: reuse as the inner value for plain frame counts and damage values
  only after note handling is resolved.
- `gauge_amount`: reuse as the inner value for Super Art gain only after note
  handling is resolved, with `unit == "super_art"` for `sa_gain`.
- `percent`: do not reuse as the full parse for `combo_scaling`; scaling is a
  rule with type/trigger/target semantics, not a plain percent.

### New Schema Wrappers Required

Future implementation should add wrappers or structured variants only after
review approval:

- `annotated_value`: wraps an existing numeric value with a source note marker,
  note identifier, note-review status, and preserved raw marker placement.
  This is required for `※3000`, `※500`, `122※`, `※-4`, and similar values.
  The wrapper must keep annotated parsing separate from calculation safety.
- `timing_sequence`: preserves active windows, comma-separated components, and
  source note markers for official active-frame strings. It must not collapse
  components into a total.
- `official_active_notation`: a reviewed grammar variant for source-confirmed
  official strings such as `30-34.35`, `20-24.25`, and `23--33`. Until that
  grammar is approved, those values stay `review_required`.
- `scaling_rule`: represents `scaling_type`, `trigger`, `target`, `amount`,
  `unit`, and note/exception metadata. It is required before
  `combo_scaling` can become calculation-safe.

Wrapper names are planning labels, not approved public interfaces.

### Note Handling

Note-bearing official values must follow these rules:

- Preserve `raw_value` exactly, including marker placement and full-width
  percent signs.
- Parse only when the corresponding note text is available in a reviewed public
  artifact and linked deterministically to the marker.
- Track `note_marker`, `note_id`, `note_text`, `note_scope`, and
  `note_review_status` before any note-bearing value can become
  calculation-safe.
- If the note text is unavailable, unmatched, or ambiguous, keep the group
  `review_required` and emit no `parsed_value`.
- Do not infer note semantics from source column labels, SuperCombo prose, or
  LLM interpretation.
- For a bare marker such as `※`, keep `review_required` unless a reviewed
  note-only representation is explicitly approved.
- Do not strip `※` or `*` before parsing. `*` has multiple source roles,
  including official cancel-marker usage, so parser rules must be
  field-aware and evidence-backed.

### External Research Evidence

External research evidence recorded on 2026-05-23 informs schema design only.
It does not promote any parsed value to numeric authority, authorize
calculator implementation, or authorize SuperCombo as authority.

- `※` and `*` must not be stripped before parsing. They carry source meaning
  and may affect note, cancel, or value scope.
- `*` has multiple source roles, including official cancel-marker usage.
- Annotated numeric parsing and calculation safety must be separate states.
  A value may be syntax-parsed while still not calculation-safe.
- Note-bearing values require `note_marker`, `note_id`, `note_text`,
  `note_scope`, and `note_review_status` before becoming calculation-safe.
- `全体 N` should be modeled as `total_duration`, not recovery, even when it
  appears in the recovery-column surface.
- Scaling strings may contain multiple rules, such as starter plus combo
  scaling. `始動補正`, `コンボ補正`, and `即時補正` must be represented as
  distinct rule semantics.
- `%` and `％` may normalize to percent for structured fields, but the raw
  symbol must be preserved.
- Damage-like strings such as `※500` require cell and column boundary
  confirmation before parsing. In particular, the implementation must confirm
  `source_column_header_path == ダメージ` and that the cell boundary is intact.
- Official active strings such as `6-366-11, 13-18※,20-25, 34-36` should be
  treated as concatenated `visible_text` plus `hidden_detail_text`, not as a
  valid active grammar. The implementation should prefer the v3 artifact's
  separated `visible_text` and `hidden_detail_text` over
  `source_text_stripped` for these cells.
- `23--33` is confirmed in the current official Terry Japanese page, but
  `--` semantics remain unresolved and blocked.
- `30-34.35` and `20-24.25` are confirmed official raw notation, but dot
  semantics remain unresolved and blocked.
- Signed `～` ranges can be syntax-parsed as ranges, but the range reason is
  unknown and they are not single-value calculation-safe.

### Malformed-Looking Active Values

`30-34.35`, `20-24.25`, and `23--33` are source-confirmed official raw
notation. `23--33` is confirmed in the current official Terry Japanese page.
They are not pending source confirmation.

The implementation must not guess that `.` means a separator, that `--` means
an omitted endpoint, or that either can be normalized to a simple range. These
values require an explicit official-active grammar policy, source-semantics
review, and representative fixtures before any `parsed_value` is emitted.

### Blocked Pending Review

The first implementation slice should keep these blocked until the stated
evidence exists:

- All note-bearing official values without deterministic note-text linkage.
- Bare note-marker values such as `※`.
- Official active notation with dot or double-dash forms until a grammar policy
  and source-semantics review are complete.
- Active cells where visible summary and hidden detail have been concatenated
  into strings such as `6-366-11, 13-18※,20-25, 34-36`.
- Damage-like note-bearing values until the `ダメージ` column and cell boundary
  are confirmed.
- `全体 ※NN` values until `全体` is reviewed as `total_duration`, not
  recovery, in the target schema.
- `combo_scaling` values until `scaling_rule` semantics are reviewed and note
  linkage is available.

The plain signed `～` advantage ranges can be the first parseable target
because they need parser-rule support but no new parsed kind. They remain range
values with unknown reason and must not be consumed as single-value
calculation-safe advantage.

## Future Implementation Plan

A later implementation ExecPlan may touch:

- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- parser/classifier fixtures and tests
- validation tests for schema compatibility and calculation gating
- coverage artifacts generated by the classifier
- source text fixtures or acquisition-derived fixtures that expose separated
  `visible_text` and `hidden_detail_text` for active cells

It must not touch retrieval, answer behavior, normalized export generation,
calculators, live acquisition, or SuperCombo parser implementation.

## Fixture And Validator Evidence

Future fixtures should include, at minimum:

- valid official signed advantage ranges: `-12～-1`, `-4～-1`, `-39～-33`,
  and `-28～-23`;
- invalid range variants that must remain `review_required` until reviewed;
- note-prefixed and note-suffixed examples for each numeric family, proving
  they do not silently parse without note linkage;
- `30-34.35`, `20-24.25`, and `23--33` as blocked official source-confirmed
  notation;
- active-cell fixtures proving concatenated visible/hidden detail strings do
  not parse as valid active grammar;
- `全体 ※43` and `全体 ※42` as blocked until `total_duration` policy exists;
- `※500` and related damage examples as blocked unless `ダメージ` column and
  cell boundary evidence is present;
- scaling examples with ASCII and full-width percent signs, proving they do
  not become plain `percent` values;
- scaling examples with starter plus combo rules in one string;
- current-fact schema fixtures proving official records remain
  `authority_candidate` and raw-preserving.

Validators must be evidence-first. They may be grounded in current schemas,
the coverage artifact, source-review artifacts, synthetic contract fixtures,
and the reviewed mechanics summary as context. They must not be weakened to
fit generated output.

## Acceptance Criteria

- The ExecPlan covers exactly the `11` official `review_required` groups.
- SuperCombo remains out of implementation scope except non-authoritative
  comparison context.
- Existing parsed kinds and required new wrappers are explicitly identified.
- Note handling is blocked unless reviewed note text is linked.
- Syntax parsing and calculation safety are separate states.
- Source-confirmed malformed-looking active values remain unparsed unless an
  explicit grammar policy and source-semantics review are approved.
- `全体 N` is planned as `total_duration`, not recovery.
- Future fixture and validator evidence requirements are listed.
- No implementation changes are made in this docs-only planning unit.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-23-official-parser-schema-slice.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Created branch `plan/official-parser-schema-slice`.
- [x] (2026-05-23 JST) Extracted the `11` official `review_required` groups
  from the parsed-value classifier coverage artifact.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`.
- [x] (2026-05-23 JST) Mandatory local review passed:
  `codex review --uncommitted` reported no actionable defects.
- [x] (2026-05-23 JST) Recorded external research evidence as schema-design
  input only, with no parser/schema/calculator implementation.
- [x] (2026-05-23 JST) Validation passed after external evidence update:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`.
- [ ] Complete domain review before implementation approval.

## Decision Log

- Decision: Make official authority-candidate groups the first implementation
  slice.
  Rationale: These are the only remaining `review_required` groups that can
  become official numeric authority candidates after deterministic parsing and
  review. SuperCombo remains non-authoritative.
  Date/Author: 2026-05-23 / Codex

- Decision: Reuse `frame_range` for signed official advantage ranges.
  Rationale: The schema already supports integer endpoints; the missing piece
  is a deterministic parser rule for signed `～` ranges.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not parse note-bearing values without reviewed note linkage.
  Rationale: The `※` marker may change semantics. Stripping it would lose
  source meaning and violate raw-value preservation.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep source-confirmed malformed-looking active values blocked until
  a grammar policy is approved.
  Rationale: Source review confirms the raw strings, but not their
  deterministic parse semantics.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep SymPy out of this parser/schema slice.
  Rationale: This slice plans value structure, not arithmetic. SymPy belongs to
  a later calculator ExecPlan after formulas and parsed values are approved.
  Date/Author: 2026-05-23 / Codex

- Decision: Separate syntax parsing from calculation safety.
  Rationale: External evidence confirms note and range markers can carry
  source semantics. Parsing a shape does not make it safe for frame, damage,
  scaling, or advantage calculation.
  Date/Author: 2026-05-23 / Codex

- Decision: Model `全体 N` as `total_duration`, not recovery.
  Rationale: The source surface may place total-frame text in the recovery
  column, but the value meaning is total duration and should not be consumed as
  recovery.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat active visible/hidden-detail concatenation as an artifact
  issue, not valid grammar.
  Rationale: Strings such as `6-366-11, 13-18※,20-25, 34-36` represent a
  visible summary plus hidden detail and should be parsed from separated
  fields where available.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- Wrapper names are planning labels and require review before becoming public
  schema interfaces.
- Note text linkage may require a separate source-review artifact before most
  note-bearing official values can parse.
- The safe first parseable target may be limited to signed `～` advantage
  ranges if note linkage and active grammar remain unresolved.
- Signed `～` ranges are not single-value calculation-safe until range reason
  semantics are reviewed.
- Scaling schema design can easily grow beyond this slice; implementation must
  keep it blocked unless reviewed semantics are explicit.
- Damage-like note-bearing values may remain blocked if cell/column boundary
  evidence is unavailable.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only official slice plan | Drafted implementation-prep plan for the 11 official `review_required` groups | `docs/execplans/2026-05-23-official-parser-schema-slice.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; `codex review --uncommitted` before evidence update; `git status --short --branch` | Passed | None | Domain review pending | Wrapper names are planning labels |
| External evidence recording | Recorded external research as schema-design evidence only; no authority promotion or implementation authorization | `docs/execplans/2026-05-23-official-parser-schema-slice.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Domain review pending | Evidence constrains what parser must not silently accept |
| Scope exclusions | No parser/schema/calculator/retrieval/answer/export/live acquisition/SymPy implementation added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Later work must keep SuperCombo out of scope |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-23-official-parser-schema-slice.md.

Confirm whether it is acceptable as the implementation-prep ExecPlan for only
the 11 official authority-candidate review_required groups.

Check:
- it covers exactly official source_name records with classifier_decision == review_required;
- the official 11 group table matches the coverage artifact;
- existing parsed_value kinds are reused where appropriate;
- note-bearing values remain blocked unless reviewed note text is linked;
- annotated parsing remains separate from calculation safety;
- `全体 N` is modeled as total_duration, not recovery;
- concatenated active visible/hidden detail is not treated as valid grammar;
- damage-like annotated values require cell and column boundary confirmation;
- source-confirmed malformed-looking active values are not guessed;
- signed `～` ranges are not treated as single-value calculation-safe;
- SuperCombo stays non-authoritative comparison context only;
- no parser/schema/calculator/retrieval/answer/export/live acquisition/SymPy implementation is included.

Return blocking findings first, then PLAN deviations and remaining risks.
```
