# Official Note Linkage V4 Source Review Update

Status: Implemented; ready for review.

## Purpose

Plan the update to official note-linkage source-review artifacts using the
`official_table_rows_raw/v4` row-note fields introduced by PR #339.

This plan keeps the work in the source-review layer. It does not implement
parser, schema, classifier, calculator, retrieval, answer, export, runtime, or
authority changes.

## Inputs

- `docs/execplans/2026-05-24-official-note-linkage-source-review.md`
- `docs/execplans/2026-05-24-official-acquisition-row-note-field-support.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `tests/validation/validate_official_note_linkage_source_review.py`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `src/sf6_knowledge_coach/source_acquisition.py`
- Existing ignored `.local/source-acquisition/` official v4 artifacts as
  reviewer input only.

## Context

PR #337 source review concluded that row-local note evidence existed in ignored
official HTML captures, but was not structured in `official_table_rows.raw.json`.
All note-bearing official groups therefore stayed
`blocked_pending_acquisition_fields`.

PR #339 implemented acquisition-field support:

- `official_table_rows_raw/v4`
- row-level `row_note_count`, `row_notes`, and
  `row_note_extraction_status`
- cell-level `cell_note_markers`, `cell_note_ids`,
  `row_note_reference_candidates`, and `note_linkage_status`
- public acquisition report summary counts/hashes only
- local reviewer-only Scrapling screenshot bundle support

The next safe step is to update source-review summary artifacts to consume the
v4 structured row-note evidence. This still does not approve any parser,
schema, calculation-safe value, or numeric authority.

## Scope

Included:

- Use existing ignored `.local` official v4 artifacts as reviewer input.
- Update official note-linkage source-review summary artifacts only.
- Re-evaluate the `9` official note-bearing or note-adjacent groups against
  structured `row_notes` and cell note candidate fields.
- Keep unresolved or ambiguous cases blocked.
- Update the focused source-review validator so it validates the new reviewed
  source-review outcomes from v4 evidence.
- Update the validator audit only if the validator contract changes.
- Preserve public summary boundaries.
- Record whether reviewer-only ChatGPT/VLM observation was used; if used, keep
  it `observation_candidate` only.

Excluded:

- No parser implementation.
- No schema implementation.
- No classifier behavior changes.
- No generated classifier coverage artifact changes.
- No calculator implementation.
- No SymPy calculation logic.
- No retrieval, answer, export, or runtime changes.
- No calculation-safe promotion.
- No numeric authority promotion.
- No current-fact authority promotion.
- No SuperCombo authority promotion.
- No live acquisition by default.
- No screenshots, raw HTML, full rows, local paths, cookies, profiles, traces,
  debug dumps, answer logs, training logs, private data, or `.local` artifacts
  committed to Git.

## Exact Review Scope

The update must cover the same `9` official records currently covered by
`data/source-reviews/20260524-official-note-linkage-source-review-summary.json`:

| # | Review item | Field | Current result | Current eligibility |
| ---: | --- | --- | --- | --- |
| 1 | `value-shape:official--source_specific_expression--sa` | `sa_gain` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 2 | `value-shape:official--source_specific_expression--u_55d872f6091a` | `combo_scaling` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 3 | `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 4 | `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `source_confirmed_non_note_grammar_blocked` | `not_note_linkage_target` |
| 5 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 6 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `startup` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 7 | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `recovery` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 8 | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `block_advantage` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |
| 9 | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `hit_advantage` | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` |

The malformed active notation group remains a non-note grammar blocker unless
v4 evidence shows a separate note-linkage issue. This ExecPlan does not resolve
dot or double-dash active grammar.

## Source-Review Decisions To Record

For each target group, the source-review update should record:

- whether v4 row-note fields are present for representative rows;
- whether target value cells have `cell_note_markers` and/or
  `cell_note_ids`;
- whether `row_note_reference_candidates` are empty, single, or multiple;
- whether `note_linkage_status` is deterministic or ambiguous;
- whether `row_notes[].note_text` and `note_text_stripped` are enough for a
  later annotated parser design;
- whether source column and cell boundary remain confirmed;
- whether visible/hidden detail separation remains sufficient;
- whether the case remains blocked, becomes later source-review eligible for a
  future annotated parser, or remains a non-note grammar blocker.

Allowed source-review outcomes for this update:

- `structured_row_note_evidence_found`
- `structured_row_note_evidence_ambiguous`
- `structured_row_note_evidence_missing`
- `source_confirmed_non_note_grammar_blocked`

Allowed later parser eligibility statuses:

- `later_annotated_parser_eligible`
- `blocked_pending_source_review`
- `blocked_pending_acquisition_fields`
- `not_note_linkage_target`

The update must not introduce a status that means calculation-safe,
current-fact authority, numeric authority, parsed value, or calculator input.

## Public Artifact Boundary

The public source-review artifacts may include:

- reviewed summary counts;
- target review item IDs;
- source-native header paths;
- representative raw values with length/hash;
- short note excerpts only when needed for deterministic review;
- reviewed status labels;
- references to v4 structured field names.

The public source-review artifacts must not include:

- full row notes;
- full raw rows;
- raw HTML;
- `official_table_rows.raw.json` contents;
- screenshots or image files;
- `.local` paths;
- cookies, browser profiles, headers, tokens, secrets;
- traces or debug dumps;
- answer logs, training logs, private vault paths, or private user data.

If reviewer-only ChatGPT/VLM bundles are used, the source-review update may
record only that observation-candidate review occurred. It must not quote
ChatGPT/VLM output as source truth, validator evidence, parser/schema approval,
calculation-safe promotion, or numeric authority.

## Validator Direction

The existing validator currently requires the source-review artifact to keep
note-bearing groups at `blocked_pending_acquisition_fields`. This update must
adjust that validator only to the extent needed to validate reviewed v4
source-review outcomes.

Validator requirements:

- continue checking that the `9` official coverage IDs are present;
- continue checking public artifact boundary;
- continue checking representative raw value length/hash;
- continue forbidding parsed values and authority promotion;
- validate only allowed v4 source-review result statuses;
- validate that no value is marked calculation-safe or numeric authority;
- require unresolved/ambiguous groups to remain blocked;
- require non-note active grammar group to remain non-note grammar blocked;
- stay grounded in coverage artifacts, v4 acquisition report/artifact
  contracts, and reviewed source-review summary artifacts.

The validator must not prove parser correctness, infer note meaning, or accept
generated output merely because it exists.

## Future Implementation Files

A later implementation ExecPlan may touch:

- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `tests/validation/validate_official_note_linkage_source_review.py`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`,
  only if the validator contract changes.
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`,
  only if the validator contract changes.
- `docs/execplans/2026-05-24-official-note-linkage-v4-source-review-update.md`

It must not touch acquisition code, parser/schema/classifier/calculator/
retrieval/answer/export/runtime files, or generated classifier coverage
artifacts.

## Acceptance Criteria

- The ExecPlan plans only official note-linkage source-review artifact updates.
- It consumes v4 official row-note fields from ignored `.local` artifacts as
  reviewer input only.
- It re-evaluates the `9` target official records.
- It keeps unresolved and ambiguous cases blocked.
- It does not authorize parser/schema/classifier/calculator/retrieval/answer/
  export/runtime changes.
- It does not promote any value to calculation-safe or numeric authority.
- It does not run live acquisition by default.
- It does not commit screenshots, raw HTML, full rows, local paths, cookies,
  profiles, traces, debug dumps, answer logs, training logs, private data, or
  `.local` artifacts.
- It keeps ChatGPT/VLM bundles, if used, local reviewer-only
  `observation_candidate`.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-24-official-note-linkage-v4-source-review-update.md`

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) PR #339 was marked ready and merged with normal merge
  commit `25341e10c491064e521f772a66f4daf73eab5220`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at the PR
  #339 merge commit.
- [x] (2026-05-24 JST) Confirmed main CI for the PR #339 merge commit passed:
  run `26351850252`.
- [x] (2026-05-24 JST) Created branch
  `plan/official-note-linkage-v4-source-review-update`.
- [x] (2026-05-24 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-24 JST) Validation passed:
  `git diff --check`, `uv lock --check`, official note-linkage source-review
  validator, source-acquisition `validate-report`, source-acquisition
  `validate-artifacts`, parsed-value classifier validator, clean-slate
  validator, and `git status --short --branch`. New-file whitespace check
  produced no whitespace error output.
- [x] (2026-05-24 JST) Completed mandatory review for PR #340 with no blocking
  findings.
- [x] (2026-05-24 JST) PR #340 was marked ready and merged with normal merge
  commit `c11a18fee4aa8e281eed03bf6ebb0334c54156f3`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at the PR
  #340 merge commit.
- [x] (2026-05-24 JST) Confirmed main CI for the PR #340 merge commit passed:
  run `26352319121`.
- [x] (2026-05-24 JST) Created branch
  `impl/official-note-linkage-v4-source-review-update`.
- [x] (2026-05-24 JST) Updated source-review summary artifacts using existing
  ignored official v4 row-note artifacts as reviewer input.
- [x] (2026-05-24 JST) Updated the focused source-review validator to enforce
  v4 source-review statuses, public artifact boundaries, and blocked ambiguous
  cases.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  `git diff --cached --check`, `uv lock --check`, official note-linkage
  source-review validator, source-acquisition `validate-report`,
  source-acquisition `validate-artifacts`, parsed-value classifier validator,
  clean-slate validator, and `git status --short --branch`.

## Decision Log

- Decision: Use PR #339 v4 acquisition artifacts as the next source-review
  input.
  Rationale: v4 exposes deterministic row-local note fields that PR #337
  identified as missing.
  Date/Author: 2026-05-24 / Codex

- Decision: Keep this as source-review artifact work, not parser/schema work.
  Rationale: v4 fields can prove note linkage evidence, but do not define
  parsed representations, numeric semantics, calculation safety, or authority.
  Date/Author: 2026-05-24 / Codex

- Decision: Allow `later_annotated_parser_eligible` only as a future
  source-review readiness status, not as parser approval.
  Rationale: A later parser/schema ExecPlan still must define annotated value
  schema, parser rules, fixtures, validators, and calculation gating.
  Date/Author: 2026-05-24 / Codex

- Decision: Update the source-review validator only if grounded in reviewed v4
  source-review outcomes.
  Rationale: Validator changes must be evidence-first and must not track output
  without a boundary contract.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Risks

- Some groups may remain ambiguous even with v4 row notes, especially rows with
  multiple `※` markers and no explicit note id.
- Public note excerpts may need trimming to avoid overexposing source text.
- The current validator is intentionally strict about blocked statuses and
  will need a focused evidence-based update if reviewed outcomes change.
- The v4 acquisition artifacts are ignored local artifacts; reviewers without
  the local workspace may need regenerated artifacts before independently
  checking the source-review update.
- Parser/schema/calculator work remains blocked until the updated source
  review is completed and separately approved.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official note-linkage v4 source-review update plan | Drafted docs-only plan for updating source-review artifacts using v4 row-note fields | `docs/execplans/2026-05-24-official-note-linkage-v4-source-review-update.md` | `git diff --check`; `uv lock --check`; source-review validator; validate-report; validate-artifacts; parsed-value classifier validator; clean-slate validator; status check | Passed | None | Complete | Future parser/schema ExecPlan still required |
| Source-review artifact update | Re-evaluated the 9 official note-bearing or note-adjacent records using v4 row-note evidence | `docs/source-reviews/20260524-official-note-linkage-source-review.md`; `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`; `tests/validation/validate_official_note_linkage_source_review.py`; this ExecPlan | Requested validation suite | Passed | None | Complete | Ambiguous groups remain blocked pending source review |
| Scope exclusions | No parser/schema/classifier/calculator/retrieval/answer/export/runtime implementation added | Source-review artifacts, focused validator, and this ExecPlan only | Diff/status review | Passed | None | Complete | No value is calculation-safe or numeric authority |

## Next Reviewer Prompt

```text
Review the implementation of docs/execplans/2026-05-24-official-note-linkage-v4-source-review-update.md.

Check:
- changed files are limited to source-review summary artifacts, the focused
  source-review validator, and this ExecPlan;
- it uses existing ignored official v4 artifacts as reviewer input only;
- it re-evaluates exactly the 9 official note-bearing or note-adjacent groups;
- unresolved and ambiguous cases remain blocked;
- it does not implement parser/schema/classifier/calculator/retrieval/answer/
  export/runtime behavior;
- it does not promote any value to calculation-safe or numeric authority;
- it does not run live acquisition by default;
- it does not commit screenshots, raw HTML, full rows, local paths, cookies,
  profiles, traces, debug dumps, answer logs, training logs, private data, or
  .local artifacts;
- ChatGPT/VLM bundles, if used, remain local reviewer-only observation_candidate;
- validator updates remain evidence-first and boundary-based.

Return findings, unresolved cases, PLAN deviations, and whether the
implementation is stage-ready.
```
