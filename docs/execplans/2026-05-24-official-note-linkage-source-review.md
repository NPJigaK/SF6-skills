# Official Note Linkage Source Review

Status: Implementation complete; review pending.

## Purpose

Review and represent official note linkage for `※` and `*` annotated official
values before any note-bearing parser can become calculation-safe.

This ExecPlan produced source-review summary artifacts and a focused validator.
It does not implement parser, schema, classifier, calculator, retrieval,
answer, export, generated coverage artifact, live acquisition, or SymPy
changes.

## Inputs

- `docs/execplans/2026-05-23-official-parser-schema-slice.md`
- `docs/execplans/2026-05-23-review-required-parser-schema-expansion.md`
- `docs/execplans/2026-05-23-official-signed-range-parser.md`
- `docs/execplans/2026-05-23-frame-range-consumer-guard.md`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- Existing ignored `.local/` reviewer artifacts, if available, as reviewer
  input only.

Live official page checks are not part of this implementation. If later source
review needs live official page checks, they must be run only in reviewer or
update mode, never in CI or daily-answer mode.

## Context

After the official signed range parser slice, the parsed-value classifier
coverage has:

- `review_required`: `205`
- `review_required_not_calculation_safe`: `205`
- `parsed_range_not_single_value_calculation_safe`: `2`

The two parsed official signed `～` range groups are already out of the
remaining official `review_required` set. This plan covers the remaining
official `review_required` groups that contain note-bearing or note-adjacent
source shapes.

Known risks:

- `※` and `*` cannot be stripped before parsing.
- `*` has multiple source roles, including official cancel-marker usage.
- `※` may appear as prefix, suffix, bracketed note id, standalone marker, or
  inside concatenated visible/hidden active text.
- Some raw strings may reflect `visible_text` plus `hidden_detail_text`
  concatenation rather than valid grammar.
- Damage-like `※500` values require cell and column boundary confirmation
  before parsing.
- Note linkage must be row, page, and cell aware.

## Scope

Included:

- Implement source-review summary artifacts only.
- Define how to link `note_marker`, `note_id`, `note_text`, `note_scope`,
  `source_column_header_path`, row/move identity, and raw value.
- Define how to distinguish:
  - note marker on value;
  - cancel marker;
  - bracketed note id such as `[※2]`;
  - standalone marker;
  - visible/hidden detail concatenation;
  - actual source note text.
- Define public summary artifact boundaries.
- Keep raw HTML, full raw rows, screenshots, cookies, browser profiles,
  traces, debug dumps, local paths, and private data out of Git.
- Use ignored `.local/` artifacts only as reviewer input.
- Plan live official page checks, if needed, as reviewer/update-mode work only.

Excluded:

- No parser implementation.
- No schema implementation.
- No classifier behavior changes.
- No validator changes except the focused source-review summary validator and
  its evidence-audit entry.
- No generated coverage artifact changes.
- No calculator implementation.
- No SymPy calculation logic.
- No retrieval, answer, export, or runtime changes.
- No numeric authority promotion.
- No SuperCombo authority promotion.
- No live acquisition in this implementation.
- No weakening validators to fit current artifacts.

## Exact Official Groups Covered

This plan covers the `9` official groups that remain
`classifier_decision == "review_required"` after the signed range parser slice.

| # | Review item | Family | Field | Source header | Affected | Representative official raw values | Note-linkage review need |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | `value-shape:official--source_specific_expression--sa` | `gauge` | `sa_gain` | `SAゲージ増加` | 8 | `※3000`; `※2150` | Link prefix marker to reviewed note text and scope before Super Art gauge amount can be syntax-parsed or considered calculation-safe. |
| 2 | `value-shape:official--source_specific_expression--u_55d872f6091a` | `scaling` | `combo_scaling` | `コンボ補正値` | 55 | `※即時補正10%`; `※即時補正10％`; `※始動補正30%コンボ補正20%`; `※即時補正10％コンボ補正20%` | Link marker and preserve percent glyphs before any scaling-rule parser can distinguish starter, combo, immediate, and combined rules. |
| 3 | `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | `damage` | `ダメージ` | 36 | `※500`; `※600`; `※700`; `※900`; `※1000` | Confirm source cell and `ダメージ` column boundary, then link marker to note text before damage can be parsed. |
| 4 | `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `timing` | `active` | `動作フレーム > 持続` | 3 | `30-34.35`; `20-24.25`; `23--33` | Not a note-linkage parser target, but same active-cell source review must preserve boundary evidence and keep dot/double-dash semantics blocked. |
| 5 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `timing` | `active` | `動作フレーム > 持続` | 44 | `※`; `[※2] 1-12`; `6-366-11, 13-18※,20-25, 34-36` | Distinguish standalone marker, bracketed note id, suffix marker on component, and visible/hidden detail concatenation before active parsing. |
| 6 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `timing` | `startup` | `動作フレーム > 発生` | 6 | `122※`; `124※`; `128※` | Link suffix marker to note text and scope before integer startup can be wrapped as annotated timing. |
| 7 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `timing` | `recovery` | `動作フレーム > 硬直` | 28 | `全体 ※43`; `全体 ※42`; `※16`; `※17`; `※20` | Link marker and decide whether label `全体` makes the value `total_duration` rather than recovery before parsing. |
| 8 | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `advantage` | `block_advantage` | `硬直差 > ガード` | 6 | `※-4`; `※-15`; `※-5`; `※-10`; `※-2` | Link prefix marker to reviewed note text and scope before signed block advantage can be wrapped as annotated value. |
| 9 | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `advantage` | `hit_advantage` | `硬直差 > ヒット` | 4 | `※-3`; `※-1`; `※-4`; `※1` | Link prefix marker to reviewed note text and scope before signed hit advantage can be wrapped as annotated value. |

Explicitly excluded from this note-linkage source-review scope:

- `value-shape:official--unclassified_expression--u_c135db53355f--u_522ba9f47afb`
- `value-shape:official--unclassified_expression--u_c135db53355f--u_7acd6c7b6e69`

Those two official signed `～` advantage range groups are already parsed as
`frame_range` and remain not single-value calculation-safe under the frame
range consumer guard plan.

## Source-Review Artifacts

This implementation creates:

- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`

Those artifacts must be public summaries only. They must not include full raw
source dumps or private/local evidence.

### Public Markdown Summary

The Markdown summary includes:

- run id and source-review summary version;
- input coverage and disposition artifact paths;
- the exact review-item table from this ExecPlan, updated only with reviewed
  source-review decisions;
- marker-role decisions for each group;
- whether source evidence is sufficient for later annotated parsing;
- which groups remain blocked and why;
- acquisition-field gaps, if any;
- boundary notes confirming no full raw rows, raw HTML, screenshots, cookies,
  browser profiles, traces, debug dumps, local paths, answer logs, training
  logs, or private data are included.

### Public JSON Summary

The JSON summary uses a small deterministic structure:

```json
{
  "artifact_schema_version": "official_note_linkage_source_review_summary/v1",
  "artifact_boundary": "source_review_summary_only",
  "authority_status": "review_decision_only_not_authority",
  "run_id": "20260524",
  "input_coverage": "data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json",
  "input_disposition": "data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json",
  "source_boundary": {
    "full_raw_rows_public_commit": "forbidden",
    "raw_html_public_commit": "forbidden",
    "local_artifacts_public_commit": "forbidden"
  },
  "review_records": []
}
```

Each `review_records` entry should contain only reviewed public summary fields:

- `source_review_id`
- `review_item_id`
- `source_name`
- `source_role`
- `semantic_source_family`
- `proposed_field_key`
- `source_header_path`
- `affected_count`
- `marker_roles`
- `representative_examples` with targeted `raw_value`, length, and hash only
- `required_source_fields_checked`
- `note_marker`
- `note_id`
- `note_text_status`
- `note_text_excerpt`, only if short, public, reviewed, and necessary
- `note_scope`
- `note_review_status`
- `row_identity_status`
- `cell_boundary_status`
- `visible_hidden_detail_status`
- `source_review_result`
- `later_parser_eligibility`
- `reviewer_notes`

The JSON summary must not contain raw HTML, full raw rows, screenshots, local
paths, cookies, browser profiles, traces, debug dumps, answer logs, training
logs, private vault paths, secrets, or full browser/source dumps.

## Note-Linkage Model

Future source review should record note linkage before parser work using these
fields:

- `note_marker`: the exact marker glyph observed in the value cell, such as
  `※` or `*`.
- `note_id`: an explicit id when the source has one, such as `※2` from
  `[※2]`; otherwise `null` or an explicit no-id status.
- `note_text`: reviewed source note text, or a status saying unavailable,
  ambiguous, or not applicable.
- `note_scope`: where the note applies, such as page, character, move row,
  move group, specific source column, specific active component, or cancel
  legend.
- `note_review_status`: one of the later reviewed statuses, such as
  `linked_reviewed`, `unlinked`, `ambiguous`, `not_applicable`, or
  `blocked_pending_source_review`.
- `source_column_header_path`: the source-native header path for the cell.
- `row_identity`: a public row or move identity reference, not a full raw row.
- `raw_value`: the exact source value for targeted examples, with length/hash
  where useful.

Planning labels in this section are not schema changes. They define what the
source-review artifact must be able to say before a future parser/schema
implementation can be approved.

## Marker Role Decisions To Review

### Note Marker On Value

A marker attached to a numeric or structured value, such as `※-4`, `122※`, or
`※即時補正10%`, must be represented as an annotated value candidate. It is not
allowed to strip the marker and parse the remaining numeric text as
calculation-safe.

The source review must prove:

- which marker is attached to the value;
- whether the marker has an explicit id;
- where the note text is found;
- what source scope the note applies to;
- whether the note changes value semantics or only display/cancel context;
- whether the underlying value cell and column boundary are intact.

### Cancel Marker

`*` can be an official cancel marker. It must not be treated as equivalent to
`※` without source-role evidence.

The source review must distinguish cancel markers by source location and
legend text. A `*` in a cancel column, cancel legend, or cancel-related cell
must not authorize numeric parsing of frame, damage, gauge, or scaling values.

### Bracketed Note Id

Bracketed ids such as `[※2]` should be treated as explicit note identifiers,
not as removable decoration. Source review must link the id to reviewed note
text and note scope before any inner active value can become parse-eligible.

If the bracketed id cannot be linked deterministically, the value remains
blocked.

### Standalone Marker

A standalone marker such as `※` is not a numeric value. It remains blocked
unless a later schema/parser plan approves a note-only representation. It must
not be converted to zero, blank, or a missing value.

### Visible/Hidden Detail Concatenation

Active strings such as `6-366-11, 13-18※,20-25, 34-36` should be reviewed as
possible concatenation of rendered `visible_text` and `hidden_detail_text`, not
as valid active grammar.

The source review must prefer separated fields, when available:

- `visible_text`
- `source_text`
- `source_text_stripped`
- `hidden_detail_text`
- `source_column_header_path`
- row or move identity

If only concatenated text is available, the group remains blocked pending
better acquisition or source review.

### Actual Source Note Text

Source note text must come from official source evidence, not from LLM
interpretation, SuperCombo prose, source column guesses, or inferred
semantics.

If the current ignored reviewer artifacts do not expose note text in a
deterministic way, the source-review result should record an acquisition-field
gap rather than guessing.

## Source-Review Procedure

This implementation:

1. Inventoried the current ignored reviewer artifacts without committing them.
2. Located representative official rows and cells for each target review item.
3. Confirmed `source_column_header_path` and cell boundary for each targeted
   example, especially `damage` examples such as `※500`.
4. Recorded row or move identity using public summary-safe identifiers only.
5. Extracted marker role and marker placement from the value cell.
6. Linked marker/id to source note text when deterministic evidence exists.
7. Recorded note scope and note review status.
8. Compared separated `visible_text` and
   `hidden_detail_text` against concatenated `source_text_stripped`.
9. Marked every note-bearing group blocked pending acquisition-field support
   because row note text is not structured in the table-row artifact.
10. Emitted public Markdown and JSON summaries only.

No live official page checks were run. Later live checks require a separate
reviewer/update-mode ExecPlan.

## Required Review Decisions

The source-review artifacts must answer:

- Which note-bearing official groups have enough source evidence to later parse
  as annotated values?
- Which groups remain blocked pending source review?
- Whether `note_text` can be linked deterministically from current ignored
  reviewer artifacts.
- Whether extra acquisition fields are needed before parser implementation.
- Whether `visible_text` and `hidden_detail_text` separation is sufficient for
  active cells.
- Whether damage-like `※500` examples are confirmed inside intact `ダメージ`
  cells, not created by column or cell boundary loss.
- Whether `*` usage in reviewed official evidence is a cancel marker, a note
  marker, or another source-specific marker.
- Whether `全体 ※NN` belongs to a later `total_duration` parser surface rather
  than `recovery`.

## Parser Eligibility After Review

Source review can make a later parser implementation possible, but it must not
itself emit parser output or promote authority.

Allowed source-review outcomes:

- `later_annotated_parser_eligible`: note marker, note text, scope, row/cell
  identity, and source column boundary are reviewed.
- `blocked_pending_source_review`: evidence is missing, ambiguous, or not
  public-summary-safe.
- `blocked_pending_acquisition_fields`: current artifacts do not expose fields
  needed for deterministic linkage.
- `not_note_linkage_target`: the group is source-confirmed but the blocker is
  a non-note grammar issue, such as dot/double-dash active notation.
- `raw_preserved_or_display_only_candidate`: source review finds the marker is
  display-only for a field that a later parser should not consume.

Even `later_annotated_parser_eligible` does not mean calculation-safe. A later
approved parser/schema ExecPlan must still define the parsed representation,
fixtures, validators, and calculation gating.

## Public Artifact Boundary

Public source-review summaries may include targeted raw values and short
reviewed note excerpts only when needed for deterministic review. They must
preserve raw marker placement and source-native header paths.

Public summaries must not include:

- full raw rows;
- full raw source table dumps;
- raw HTML;
- screenshots;
- browser profiles;
- cookies, credentials, headers, tokens, or secrets;
- traces or debug dumps;
- local absolute paths;
- answer logs, training logs, private vault paths, or private user data;
- generated parser outputs;
- current-fact authority promotions.

Ignored `.local/` artifacts may be used as reviewer input, but they must remain
uncommitted. The public summary should describe evidence status without
leaking local artifact paths or full private/local dumps.

## Implementation Files

This source-review implementation touches:

- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `tests/validation/validate_official_note_linkage_source_review.py`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

This implementation does not touch parser, schema, classifier, calculator,
retrieval, answer, export, runtime, generated coverage artifacts, or live
acquisition.

## Acceptance Criteria

- The ExecPlan covers the `9` official `review_required` groups that remain
  after the signed range parser slice.
- The ExecPlan defines how to link `note_marker`, `note_id`, `note_text`,
  `note_scope`, `source_column_header_path`, row/move identity, and raw value.
- The ExecPlan distinguishes note markers, cancel markers, bracketed note ids,
  standalone markers, visible/hidden detail concatenation, and actual source
  note text.
- The ExecPlan defines public Markdown and JSON source-review summary
  boundaries.
- The ExecPlan keeps ignored `.local/` artifacts as reviewer input only.
- The ExecPlan does not implement parser/schema/classifier/calculator/
  retrieval/answer/export/runtime changes.
- The source-review validator checks only the public summary boundary and is
  grounded in this ExecPlan and parsed-value coverage.
- The implementation does not modify generated coverage artifacts.
- Validation commands pass.

## Files / Interfaces

This source-review implementation changes only:

- `docs/execplans/2026-05-24-official-note-linkage-source-review.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `tests/validation/validate_official_note_linkage_source_review.py`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) Created branch
  `plan/official-note-linkage-source-review`.
- [x] (2026-05-24 JST) Confirmed local `main` matched `origin/main` at
  `eeeba999382f632cf11396c4ea47a516924f21bb` before branching.
- [x] (2026-05-24 JST) Identified the `9` remaining official
  `review_required` groups from parsed-value classifier coverage.
- [x] (2026-05-24 JST) Drafted the docs-only ExecPlan.
- [x] (2026-05-24 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`. New-file whitespace check also produced
  no whitespace error output.
- [x] (2026-05-24 JST) PR #336 merged, approving this source-review plan.
- [x] (2026-05-24 JST) Created implementation branch
  `impl/official-note-linkage-source-review`.
- [x] (2026-05-24 JST) Reviewed ignored official artifacts. Structured
  table-row artifacts expose source-native column paths, raw cell text,
  visible text, hidden detail text, and row identity. Row-local note text is
  visible in ignored official HTML captures but is not structured in the
  table-row artifact.
- [x] (2026-05-24 JST) Added public source-review Markdown and JSON summary
  artifacts.
- [x] (2026-05-24 JST) Added a focused source-review summary validator.
- [x] (2026-05-24 JST) Updated the validator/test evidence audit for the new
  validator.
- [ ] Complete mandatory review before staging.

## Decision Log

- Decision: Cover the `9` remaining official `review_required` groups, not the
  two already parsed official signed `～` range groups.
  Rationale: PR #334 moved those signed ranges to `frame_range` with
  `parsed_range_not_single_value_calculation_safe`; they do not require note
  linkage.
  Date/Author: 2026-05-24 / Codex

- Decision: Treat note linkage as source-review evidence, not parser output.
  Rationale: The next blocker is determining what each marker applies to.
  Parsing before row/page/cell-aware note review would invite silent numeric
  misuse.
  Date/Author: 2026-05-24 / Codex

- Decision: Keep source-review public artifacts summary-only.
  Rationale: Repository policy forbids committing full raw rows, raw HTML,
  screenshots, local paths, browser profiles, cookies, traces, debug dumps,
  private vault paths, and private data.
  Date/Author: 2026-05-24 / Codex

- Decision: Do not run live official page acquisition in this plan.
  Rationale: Any live checks belong in a separate reviewer/update-mode
  source-review plan.
  Date/Author: 2026-05-24 / Codex

- Decision: Keep all note-bearing groups blocked pending acquisition-field
  support.
  Rationale: Reviewer evidence found row-local notes in ignored official HTML
  captures, but the structured table-row artifact does not expose row note
  text. A parser should not depend on ad hoc HTML review or group-level note
  assumptions.
  Date/Author: 2026-05-24 / Codex

- Decision: Treat the active dot/double-hyphen group as source-confirmed but
  not a note-linkage target.
  Rationale: The values are official active cells, but this source review does
  not establish dot or double-hyphen grammar or calculation meaning.
  Date/Author: 2026-05-24 / Codex

- Decision: Update the validator/test evidence audit for the new source-review
  validator.
  Rationale: Repository policy requires every test and validator to declare
  its evidence basis. The new validator is source-derived but proves only
  public summary consistency and boundary rules, not parser correctness.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Risks

- Current structured table-row artifacts do not expose official row-local note
  text, so note-bearing parser work remains blocked pending acquisition-field
  support.
- `*` can have multiple roles; treating it as a note marker without source
  location evidence would be unsafe.
- Active cells may require acquisition improvements if only concatenated text
  is available.
- Short public note excerpts may still need careful review to avoid committing
  excessive source text.
- Source-review eligibility will not make values calculation-safe until a
  later parser/schema ExecPlan defines annotated parsing and calculation
  gating.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official note-linkage source-review artifacts | Added public Markdown and JSON summaries for the 9 remaining official note-bearing or note-adjacent groups | Source-review Markdown and JSON summary | Source-review validator | Pending | None | Review pending | Note-bearing values remain blocked pending acquisition-field support |
| Source-review validator | Added focused validator grounded in this ExecPlan and coverage artifact | `tests/validation/validate_official_note_linkage_source_review.py` | Source-review validator | Pending | None | Review pending | Validator checks boundary and consistency, not parser correctness |
| Validator audit | Added evidence-basis audit entry for the new validator | Validator audit JSON/Markdown | `validate_validator_test_audit.py` | Pending | None | Review pending | Audit remains accepted-with-limits |
| Scope exclusions | No parser/schema/classifier/calculator/retrieval/answer/export/runtime/generated coverage/live acquisition changes added | Scoped files only | Diff/status review | Pending | None | Review pending | Note-bearing values remain blocked |

## Next Reviewer Prompt

```text
Review the official note-linkage source-review implementation.

Check:
- changed files are limited to the ExecPlan, public source-review Markdown,
  public source-review JSON, focused source-review validator, and
  validator/test evidence audit entries;
- the JSON covers exactly the 9 remaining official review_required records
  after the signed range parser slice;
- note-bearing records remain blocked pending acquisition-field support;
- the active dot/double-hyphen group is source-confirmed but not treated as a
  note-linkage target;
- no parser/schema/classifier/calculator/retrieval/answer/export/runtime,
  generated coverage artifact, live acquisition, or SymPy behavior was added;
- public artifacts include summaries only and no full source rows, raw HTML,
  browser images, cookies, profiles, traces, debug dumps, local paths, answer
  logs, training logs, or private data;
- official remains authority candidate only and no value becomes
  calculation-safe.

Run:
- `git diff --check`
- `git diff --cached --check`
- `PYTHONPATH=src uv run --locked python -m unittest discover -s tests`
- `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`
- `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`
- `PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py`
- `PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py`
- `git status --short --branch`

Return blocking findings first, then validation results, PLAN deviations,
remaining risks, and whether this is stage-ready.
```
