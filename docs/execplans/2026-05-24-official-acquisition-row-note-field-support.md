# Official Acquisition Row Note Field Support

Status: Drafted for review.

## Purpose

Plan the acquisition-field support needed to expose official row-local note
text in deterministic ignored structured artifacts before any note-bearing
official value can move toward parser/schema work.

This ExecPlan is docs-only. It does not implement acquisition code, parser,
schema, classifier, calculator, retrieval, answer, export, runtime, generated
coverage artifact, live acquisition, or SymPy changes.

## Inputs

- `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`
- `docs/execplans/2026-05-24-official-note-linkage-source-review.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `src/sf6_knowledge_coach/source_acquisition.py`
- `tests/test_source_acquisition.py`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- Existing ignored `.local/source-acquisition/` official HTML captures, if
  available, as implementation input only.

## Context

PR #337 found that official row-local note evidence is visible in ignored
official HTML captures, but it is not represented in
`official_table_rows.raw.json`.

Current source-review result:

- `row_note_text_seen_in_ignored_reviewer_html_capture == true`
- `row_note_text_in_structured_table_row_artifact == false`
- `table_cell_boundaries_seen_in_structured_table_row_artifact == true`
- `visible_hidden_detail_fields_seen_in_structured_table_row_artifact == true`
- `blocked_pending_acquisition_fields == 8`
- `not_note_linkage_target == 1`

Therefore note-bearing official groups must remain blocked. The next safe step
is not a parser. It is a source-acquisition artifact update that preserves
row-local note text as structured source evidence.

## Scope

Included:

- Plan row-local official note extraction into ignored structured acquisition
  artifacts.
- Preserve source-native note text, note order, row identity, source column
  path, `visible_text`, and `hidden_detail_text`.
- Define how note text is linked to row, cell, and field without parser
  inference.
- Define artifact-version, validation, and public-boundary expectations for a
  later implementation.
- Plan optional reviewer-only sanitized ChatGPT/VLM observation as external
  review aid only.
- Keep all note-bearing values blocked until structured row notes are
  available and reviewed.

Excluded:

- No acquisition code implementation in this docs-only plan.
- No parser implementation.
- No schema implementation.
- No classifier behavior changes.
- No generated coverage artifact changes.
- No calculator implementation.
- No SymPy calculation logic.
- No retrieval, answer, export, or runtime changes.
- No current-fact authority promotion.
- No numeric authority promotion.
- No SuperCombo authority promotion.
- No live official acquisition in this planning step.
- No screenshots, full raw HTML, full raw rows, cookies, browser profiles,
  traces, debug dumps, local paths, or private data committed to Git.

## Required Design Decisions

### Artifact Surface

The later implementation should update official local raw row artifacts from
`official_table_rows_raw/v3` to a new version, tentatively
`official_table_rows_raw/v4`.

The updated ignored artifact should add row-local note structure while
preserving the existing v3 cell fidelity:

- `source_column_header_path`
- `source_column_leaf_header`
- `visible_text`
- `source_text`
- `source_text_stripped`
- `hidden_detail_text`
- `image_src`
- `image_alt`
- `table_index`
- `row_index`
- `group_heading`
- `cell_count`
- `input_images`

The new row-note fields should be source-fidelity fields only. They must not
emit parsed values or calculation semantics.

### Row Note Fields

Each official data row should expose row-local notes with deterministic
source-order preservation.

Planned row-level fields:

- `row_note_count`
- `row_notes`
- `row_note_extraction_status`

Each `row_notes[]` entry should include:

- `note_index`: zero-based order within the row-local note list.
- `note_marker`: exact marker glyph when visible, such as `※` or `*`, or
  `null` when the source note is markerless.
- `note_id`: explicit source id such as `※2`, or `null`.
- `note_text`: source-native note text exactly as extracted after minimal
  whitespace normalization.
- `note_text_stripped`: normalized exact-source comparison text.
- `note_source_scope`: a source-fidelity label such as `row_local_note`.
- `source_order`: same ordering basis as `note_index`.

Planning labels are not public schemas. The implementation may adjust names in
the ExecPlan Decision Log before coding if source inspection proves a better
deterministic shape is required.

### Cell Linkage Fields

Cells should not infer note meaning. They may only record deterministic marker
presence and row-note references that can be proven from source structure.

Planned cell-level additions:

- `cell_note_markers`: exact marker tokens observed in the cell text.
- `cell_note_ids`: explicit ids observed in the cell text, such as `※2`.
- `row_note_reference_candidates`: ids or marker candidates available from
  the same row-local note list.
- `note_linkage_status`: source-structural status only, such as
  `same_row_note_candidates_available`, `no_row_notes`, or
  `ambiguous_marker_without_id`.

The implementation must not decide that a note changes a numeric value, does
not change a numeric value, makes a value calculation-safe, or authorizes a
parser. Those are later source-review and parser/schema decisions.

### Row And Field Identity

The updated artifact must keep enough row and field identity for later
source-review summary artifacts to link notes without raw row dumps.

Required identity fields:

- `character_slug`
- public source URL and final URL metadata already present at artifact level
- `table_index`
- `row_index`
- `group_heading`
- move identity from the source move-name cell
- each cell's `source_column_header_path`
- each cell's `source_column_leaf_header`

Move identity may be recorded from the first cell as source-native text, but
the implementation must not split, normalize, alias, or canonicalize the move
name.

### Visible And Hidden Text

The implementation must preserve the v3 distinction between:

- browser-rendered `visible_text`;
- full `source_text`;
- exact-comparison `source_text_stripped`;
- `hidden_detail_text`.

Row note extraction must not fold row note text into `visible_text` or
`hidden_detail_text` for value cells. Row notes should be stored in row-note
fields, not appended to cell values.

### Public Report Boundary

The ignored `.local/source-acquisition/` artifacts may contain row-local note
text because they are source-fidelity local acquisition artifacts. Public Git
artifacts must remain summary-only.

A later implementation may update the public acquisition report only to record
summary-safe metadata such as:

- artifact schema version;
- row-note extraction field availability;
- counts of rows with row notes;
- hashes of ignored local artifacts;
- validation status.

The public report must not include full row note lists, full rows, raw HTML,
screenshots, local paths, cookies, browser profiles, traces, debug dumps,
answer logs, training logs, or private data.

### Reviewer-Only Sanitized Observation

Reviewer-only sanitized ChatGPT/VLM observation may be used to cross-check
targeted screenshots and values, but it is observation_candidate only. The
implementation authority remains deterministic structured artifacts and
reviewed public summaries.

If used, reviewer bundles and screenshots must be stored only under:

```text
.local/reviewer-evidence/official-note-linkage/
```

Reviewer bundles may include only:

- targeted official value examples;
- source-native header path;
- character, move, and row identity;
- short row note excerpt if needed;
- cropped page screenshot of the exact row, cell, and note area;
- raw value length/hash.

They must not include:

- screenshots committed to Git;
- full raw HTML;
- full raw rows;
- browser profiles;
- cookies or session data;
- request headers;
- local paths in public artifacts;
- traces or debug dumps.

Any ChatGPT/VLM output remains:

- not numeric authority;
- not source truth by itself;
- not validator evidence;
- not parser/schema approval;
- not calculation-safe promotion.

## Future Implementation Plan

A later implementation ExecPlan may touch only the files required for
acquisition-field support:

- `src/sf6_knowledge_coach/source_acquisition.py`
- `tests/test_source_acquisition.py`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`,
  only if ignored local artifacts are regenerated and the public hash/count
  report must be refreshed.
- `docs/execplans/2026-05-24-official-acquisition-row-note-field-support.md`

Potential implementation steps:

1. Add synthetic official HTML fixture coverage for a row with row-local notes.
2. Extend official row extraction to emit row-note fields in
   `official_table_rows.raw.json`.
3. Add artifact validation for row-note field presence, type, ordering, and
   public-boundary safety.
4. Reprocess existing ignored official HTML captures into updated ignored
   structured artifacts, if available.
5. Refresh the public acquisition report only with summary-safe hashes/counts
   if regenerated local artifacts change report-bound hashes.
6. Run source-acquisition tests and validators.

Live official page acquisition is not required for the implementation if
existing ignored captures are sufficient. If live acquisition is needed, the
implementation ExecPlan must say so explicitly and keep it in update/research
mode, not CI or daily-answer mode.

## Downstream Handoff

After row-local notes are available in ignored structured artifacts, a separate
source-review implementation may update:

- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `tests/validation/validate_official_note_linkage_source_review.py`

That later source-review update may move specific groups from
`blocked_pending_acquisition_fields` to a reviewed source-review status such
as `later_annotated_parser_eligible`, but still must not emit parser output or
calculation-safe values.

Parser/schema implementation remains blocked until:

- row-local notes are present in deterministic structured artifacts;
- public source-review summaries are updated and reviewed;
- a separate parser/schema ExecPlan is approved.

## Acceptance Criteria

- The ExecPlan targets row-local official note extraction into ignored
  structured acquisition artifacts.
- The ExecPlan keeps raw HTML, full raw rows, screenshots, cookies, browser
  profiles, traces, debug dumps, local paths, and private data out of Git.
- The ExecPlan preserves source-native note text, note order, row identity,
  source column path, `visible_text`, and `hidden_detail_text`.
- The ExecPlan defines note linkage to row, cell, and field without parser
  inference.
- The ExecPlan includes reviewer-only sanitized ChatGPT/VLM observation as
  optional `observation_candidate` only.
- The ExecPlan stores any reviewer screenshots or bundles under ignored
  `.local/reviewer-evidence/official-note-linkage/` only.
- The ExecPlan prohibits parser/schema/classifier/calculator/retrieval/
  answer/export/runtime changes.
- The ExecPlan keeps all note-bearing values blocked until structured row
  notes are available and reviewed.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-official-acquisition-row-note-field-support.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) PR #337 was marked ready and merged with normal merge
  commit `57d2685e7a0461f33fae9f223f88d39e8cd5614d`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at the PR
  #337 merge commit.
- [x] (2026-05-24 JST) Created branch
  `plan/official-acquisition-row-note-field-support`.
- [x] (2026-05-24 JST) Confirmed main CI for the PR #337 merge commit passed:
  run `26342245016`.
- [x] (2026-05-24 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-24 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py`,
  and `git status --short --branch`. New-file whitespace check produced no
  whitespace error output.
- [ ] Complete mandatory review before any acquisition-field implementation.

## Decision Log

- Decision: The next implementation surface is official acquisition field
  support, not parser/schema work.
  Rationale: PR #337 proved row-local note evidence exists in ignored HTML but
  not in deterministic structured row artifacts. Parser work would require
  inference without this field support.
  Date/Author: 2026-05-24 / Codex

- Decision: Add row notes to ignored acquisition artifacts, not public source
  review summaries directly.
  Rationale: The extraction must preserve source-native note text and row
  order while keeping raw source detail out of Git. Public artifacts can then
  summarize reviewed decisions.
  Date/Author: 2026-05-24 / Codex

- Decision: Treat cell-to-note linkage as source-structural evidence only.
  Rationale: Acquisition can show marker presence and same-row note
  candidates; it must not infer numeric semantics, parser eligibility, or
  calculation safety.
  Date/Author: 2026-05-24 / Codex

- Decision: Allow sanitized ChatGPT/VLM observation only as reviewer-side
  `observation_candidate`.
  Rationale: Screenshot cross-checks may help human review, but deterministic
  implementation authority must remain structured artifacts and reviewed
  public summaries.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Risks

- Existing ignored official HTML captures may not be present in every reviewer
  environment.
- The official DOM may expose row notes through source structures that require
  selector review before deterministic extraction.
- Row-note text can be source text; public summaries must avoid excessive
  quoting and raw-row leakage.
- Marker-to-note matching may remain ambiguous when a row has multiple markers
  without explicit ids.
- Updating ignored artifact schema from v3 to v4 may require public
  acquisition report hash refresh while still keeping raw note lists out of
  Git.
- Note-bearing values remain blocked until a later reviewed source-review
  update consumes the new acquisition fields.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official row-note field support plan | Drafted docs-only plan for exposing row-local notes in ignored structured official acquisition artifacts | `docs/execplans/2026-05-24-official-acquisition-row-note-field-support.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; official note-linkage source-review validator; `git status --short --branch` | Passed | None | Review pending | Future acquisition-field implementation still required |
| Scope exclusions | No parser/schema/classifier/calculator/retrieval/answer/export/runtime/acquisition implementation added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Note-bearing values remain blocked |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-24-official-acquisition-row-note-field-support.md.

Confirm whether it is acceptable as the docs-only planner for official
acquisition row-note field support.

Check:
- it starts from PR #337's result that row-local note evidence exists in
  ignored HTML but is not structured in official_table_rows.raw.json;
- it targets row-local official note extraction into ignored structured
  acquisition artifacts;
- it keeps raw HTML, full raw rows, screenshots, cookies, browser profiles,
  traces, debug dumps, local paths, and private data out of Git;
- it preserves source-native note text, note order, row identity,
  source_column_header_path, visible_text, and hidden_detail_text;
- it defines note linkage to row/cell/field without parser inference;
- it includes reviewer-only sanitized ChatGPT/VLM observation as optional
  observation_candidate only;
- it stores any screenshots/bundles only under
  .local/reviewer-evidence/official-note-linkage/;
- it prohibits parser/schema/classifier/calculator/retrieval/answer/export/
  runtime changes;
- it keeps all note-bearing values blocked until structured row notes are
  available and reviewed.

Return blocking findings first, then validation checked, PLAN deviations, and
remaining risks.
```
