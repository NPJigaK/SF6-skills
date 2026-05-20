# Value-Shape Inventory Planning

Status: Draft; planning-only ExecPlan.

## Purpose

Plan Phase 1 roadmap unit 4: value-shape inventory across all fields.

This ExecPlan defines how a future implementation should inventory observed
raw value representations across all characters, fields, and approved raw
sources. It does not calculate totals, infer missing values, normalize exports,
promote SuperCombo to authority, implement schemas, implement parsers, change
retrieval, or change answer behavior.

## Scope

Included:

- Define the value-shape inventory scope across all characters, all fields,
  and approved official/SuperCombo raw source snapshots.
- Define observed value-shape classes for scalar, signed frame, parenthesized,
  plus-separated, range, multihit, conditional, missing/blank, nonnumeric note,
  raw-only, and unparsed values.
- Define per-field observed shape count expectations.
- Define raw example capture requirements.
- Define source-role and evidence metadata needed to keep official and
  SuperCombo boundaries separate.
- Define how inventory rows should reference raw source rows without copying
  private or transient data.
- Preserve exact raw source values.
- Keep SuperCombo as enrichment, cross-reference, or candidate evidence only.
- Preserve that manual review, prose, FTS, and LLM memory are not numeric
  authority.

Excluded:

- No fetching implementation.
- No Scrapling dependency.
- No schema implementation.
- No parser or classifier implementation.
- No normalized export.
- No value calculation.
- No total-frame calculation.
- No inferred values.
- No official/SuperCombo reconciliation implementation.
- No SuperCombo promotion policy.
- No retrieval changes.
- No answer behavior changes.
- No validator changes.
- No dependencies.
- No data artifacts.
- No private vault, Discord, VLM, video pipeline, web daily-answer mode, API
  fallback, vector search, persistent DB, generated DB, or `sf6 ask`.
- No restoration of deleted legacy runtime, package, adapter, or workflow
  surfaces.

## Acceptance Criteria

- The plan covers all fields observed in future approved official and
  SuperCombo raw snapshots.
- The plan covers all characters present in the approved raw source snapshots.
- The plan defines the required value-shape classes:
  `scalar`, `signed_frame`, `parenthesized`, `plus_separated`, `range`,
  `multihit`, `conditional`, `missing_blank`, `nonnumeric_note`, `raw_only`,
  and `unparsed`.
- The plan states that raw source values must be preserved exactly.
- The plan states that the inventory records observed shapes only and does not
  calculate totals or infer values.
- The plan states that SuperCombo remains enrichment/cross-reference/candidate
  evidence only.
- The plan states that LLM interpretation is not an authority source.
- The plan defines inventory record fields enough for a later implementation
  ExecPlan to create artifacts.
- The plan does not create schemas, validators, parsers, normalized exports,
  retrieval behavior, answer behavior, or data artifacts.
- Planning validation passes.

## Files / Interfaces

Changed by this ExecPlan:

- `docs/execplans/2026-05-21-value-shape-inventory.md`

Existing inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
- `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md`
- `docs/execplans/2026-05-21-supercombo-raw-snapshot-acquisition.md`
- `data/exports/README.md`

Future implementation inputs:

- Approved official raw snapshots from the official acquisition unit.
- Approved SuperCombo raw snapshots from the SuperCombo acquisition unit.
- Approved source manifests and source row refs.

Future artifacts are planned, not created here. A later ExecPlan may choose
exact paths. The preferred shape is a reviewed value-shape inventory, for
example:

- `docs/current-facts/value-shape-inventory.md`
- `data/current-facts/value-shape-inventory.json`

Those future paths are not approved by this planning-only ExecPlan.

## Inventory Scope

The value-shape inventory should cover:

- Every approved raw source family:
  - `official`
  - `supercombo`
- Every character represented in the approved raw snapshots.
- Every raw source field/header/cell key present in approved source rows.
- Every raw value representation observed for each field.
- Missing, blank, null, and source-empty values as first-class observations.

The inventory is descriptive. It records what shapes appear in source rows. It
does not decide whether a shape is safe to parse, safe to answer from, or safe
to promote.

## Shape Classes

The future inventory should use stable shape labels. A later implementation may
add subtypes, but it must not remove these top-level classes without review.

```yaml
shape_classes:
  scalar:
    description: Single raw numeric-like token without an explicit sign or range.
    examples: ["4", "300", "55"]
  signed_frame:
    description: Single raw frame-like value with an explicit plus or minus sign.
    examples: ["+2", "-6", "±0"]
  parenthesized:
    description: Raw value whose relevant source representation includes parentheses.
    examples: ["(1656)", "始動補正(20%)"]
  plus_separated:
    description: Raw value made of multiple pieces separated by plus signs.
    examples: ["1000+500", "4+2"]
  range:
    description: Raw value representing a continuous range or span.
    examples: ["6-8", "12-31"]
  multihit:
    description: Raw value representing multiple hit windows, row parts, or repeated segments.
    examples: ["12-31 12-13, 18-19, 22", "9-27 9-11, 25-27"]
  conditional:
    description: Raw value or note whose meaning depends on a condition.
    examples: ["パニッシュカウンター時+25F", "密着で発動した場合"]
  missing_blank:
    description: Source missing, null, blank, dash-only, or intentionally empty value.
    examples: [null, "", "-"]
  nonnumeric_note:
    description: Textual note that is not itself a parseable numeric value.
    examples: ["D", "着地後3", "上・弾"]
  raw_only:
    description: Raw value must be preserved but is not approved for parsing in the current inventory.
    examples: ["source-specific note", "ambiguous cell"]
  unparsed:
    description: Raw value shape not yet classified by the inventory rules.
    examples: ["unexpected token"]
```

The examples are illustrative planning examples, not a complete source-derived
inventory.

## Proposed Inventory Record

The future value-shape inventory should be row-oriented and reviewable. It
should avoid embedding parser logic.

```yaml
value_shape_observation:
  inventory_schema_version: inventory-only-v1
  source_family: official | supercombo
  source_role: current_fact_authority_candidate | enrichment_candidate
  evidence_basis: official | community
  character_slug: jp
  source_snapshot_id: string
  source_row_id: string
  field_key: startup
  raw_field_label: startup
  raw_value: "6"
  raw_value_sha256: string
  normalized_for_grouping: null
  observed_shape_classes:
    - scalar
  shape_notes: []
  parser_status: not_implemented
  numeric_authority_status: not_authority
  review_status: inventory_only
```

Rules:

- `raw_value` must preserve the source value exactly.
- `normalized_for_grouping` is optional and may only support grouping display;
  it is not authority and must not replace `raw_value`.
- `observed_shape_classes` may contain multiple labels when a value belongs to
  multiple classes, for example `conditional` and `parenthesized`.
- `numeric_authority_status` must not mark SuperCombo values as daily-answer
  authority.

## Per-Field Summary

The future inventory should also summarize observed shapes per field. This is
for review coverage, not parsing.

```yaml
field_shape_summary:
  field_key: active
  raw_field_labels_seen:
    - active
  source_families_seen:
    - official
    - supercombo
  character_count_seen: 29
  row_count_seen: 1000
  shape_counts:
    scalar: 0
    signed_frame: 0
    parenthesized: 0
    plus_separated: 0
    range: 700
    multihit: 120
    conditional: 40
    missing_blank: 80
    nonnumeric_note: 10
    raw_only: 20
    unparsed: 30
  raw_examples_by_shape:
    range:
      - source_row_id: string
        raw_value: "6-8"
    multihit:
      - source_row_id: string
        raw_value: "12-31 12-13, 18-19, 22"
  review_questions: []
```

Counts are observed-shape counts. They are not calculated frame totals and do
not imply parse safety.

## Raw Preservation Rules

The future implementation must preserve:

- Exact raw cell text.
- Source null, blank, missing, dash-only, or unknown tokens.
- Source punctuation.
- Source signs.
- Source whitespace where it changes displayed meaning.
- Source percent symbols.
- Source parentheses.
- Source note text.
- Source locale-specific text.
- Source row grouping and table labels.

The future implementation must not:

- Convert `+2` to `2`.
- Convert `-6` to `6`.
- Convert `6-8` into an active-frame count.
- Convert `1000+500` into `1500`.
- Interpret conditional text as a definitive numeric value.
- Infer missing cells from nearby rows.
- Treat SuperCombo conflict candidates as official values.

## Authority And Evidence Policy

- Official raw values may later become `current_fact_authority` only through
  later deterministic parsing, schema validation, and review.
- SuperCombo values remain enrichment, cross-reference, or candidate evidence
  only.
- Manual review sidecars, prose, FTS, and LLM memory are not numeric authority.
- LLM interpretation is not an authority source for value-shape classification.
- This unit does not change daily answer behavior.
- The inventory may inform future parser design, but it does not implement that
  parser and does not approve any parsed value.

## Future Validation Strategy

A future implementation ExecPlan should add focused validators before
publishing value-shape inventory artifacts.

Planned validation categories:

- Inventory artifact structure.
- Source snapshot and source row refs resolve to approved raw snapshot
  artifacts.
- Raw value hashes match inventory rows when hashes are present.
- No local absolute paths.
- No private vault, answer log, training log, credential, cookie, or browser
  profile leakage.
- Every approved source family and character is represented or has a recorded
  coverage failure/review item.
- Every raw field seen in source rows is represented in field summaries.
- Required shape classes are present in the inventory vocabulary.
- SuperCombo rows cannot carry daily-answer numeric authority status.
- Inventory does not contain calculated totals or inferred values.
- Inventory does not mark parser output as implemented.

This ExecPlan does not add those validators.

## Validation Commands

Run from the repository root:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-21 JST) Verified PR #302 was merged into `main` with merge
  commit `ca72698120ef0ff128597943638823e903eb344b`.
- [x] (2026-05-21 JST) Verified main branch CI passed for merge commit
  `ca72698120ef0ff128597943638823e903eb344b`.
- [x] (2026-05-21 JST) Confirmed `stash@{0}` remains present and unapplied.
- [x] (2026-05-21 JST) Created branch `plan/value-shape-inventory` from
  updated `main`.
- [x] (2026-05-21 JST) Reviewed the Phase 1 roadmap, official raw snapshot
  acquisition plan, SuperCombo raw snapshot acquisition plan, and `docs/PLAN.md`.
- [x] (2026-05-21 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-21 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [ ] Mandatory review.

## Decision Log

- Decision: This unit plans value-shape inventory only.
  Rationale: Phase 1 roadmap unit 4 must classify observed raw representations
  before schema redesign and parser implementation.
  Date/Author: 2026-05-21 / Codex

- Decision: Include both official and SuperCombo raw snapshot sources in the
  inventory while preserving separate source roles.
  Rationale: Parser design needs to see both source families, but only official
  paths may later become current-fact authority after later gates.
  Date/Author: 2026-05-21 / Codex

- Decision: Treat shape classes as descriptive inventory labels, not parser
  output.
  Rationale: This unit must not implement parsing, calculate values, infer
  semantics, or approve normalized exports.
  Date/Author: 2026-05-21 / Codex

- Decision: Allow multiple shape labels per raw value.
  Rationale: A single source value may be both conditional and parenthesized,
  or both multihit and range-like. Forcing one label would lose review context.
  Date/Author: 2026-05-21 / Codex

## Deviations

- None.

## Risks

- Future raw snapshots may contain value shapes not listed here; those should
  be recorded as `unparsed` or require a later inventory update.
- Shape labels may need source-specific subtypes after real snapshots exist.
- Counts can be misleading if treated as parser readiness; review must keep
  counts descriptive.
- SuperCombo rows must remain blocked from daily-answer numeric authority even
  when their raw shapes look parseable.
- Future artifact paths and schemas are intentionally unresolved in this plan.
- `stash@{0}` contains paused retrieval runtime work and must remain separate
  from this planning branch.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Value-shape inventory planning | Planned descriptive shape inventory across approved raw sources. | `docs/execplans/2026-05-21-value-shape-inventory.md` | `git diff --check` | Pass | None | Mandatory review pending | Future sources may reveal more shapes |
| Raw value preservation | Planned exact raw preservation and no calculation/inference rules. | Same | Review | Pending | None | No implementation yet | Parser design must keep raw values |
| Required shape classes | Planned scalar, signed frame, parenthesized, plus-separated, range, multihit, conditional, missing/blank, nonnumeric note, raw-only, and unparsed classes. | Same | Review | Pending | None | No schema yet | Class names may need subtypes |
| Authority boundary | Preserved SuperCombo as enrichment/cross-reference/candidate only and LLM memory as non-authority. | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | No validator yet | Later implementation must enforce policy |
