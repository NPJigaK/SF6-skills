# Current-Fact Candidate Public Artifact Source Review

Status: Drafted for review; validation passed.

## Purpose

Decide whether existing committed public summaries can support
`current_fact_row_move_cell_candidate_input/v1` production candidate records,
or whether a source-review/acquisition amendment is required before any
candidate artifact generation.

This is a docs-only source-review planning step. It does not generate
candidate artifacts, source-record artifacts, current-fact export artifacts,
or runtime lookup behavior.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md`
- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`
- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

PR #363 added the contract for
`current_fact_row_move_cell_candidate_input/v1` plus synthetic fixtures and a
focused validator. Those fixtures intentionally do not prove source truth.

The next production question is whether committed public artifacts can already
populate candidate records. Candidate records require exact row/move/cell
identity, source/header context, raw value, parsed value, source/evidence
references, authority status, and calculation status.

Current public inputs provide partial evidence:

- parsed-value classifier coverage gives group-level and raw-variant-level
  parser/status policy;
- official note-linkage source review gives representative examples, reviewed
  source-review results, and v4 row-note evidence summaries;
- acquisition reports give run identity, per-character summary counts, and
  hashes for ignored raw captures;
- schemas and validators define contracts and guard boundaries;
- validator audits define what validators are allowed to prove.

They do not yet provide a committed, summary-safe list of every candidate
row/move/cell record.

## Scope

Included in this docs-only plan:

- inventory public inputs available after PR #363;
- define the exact evidence required to populate candidate records from
  committed public artifacts;
- identify supported and missing candidate fields;
- decide whether candidate artifact implementation can start now;
- define the required source-review/acquisition amendment if public evidence
  is insufficient;
- preserve Issue #343 double-check gate for future value-handling decisions;
- preserve summary-safe and source-boundary rules.

Excluded:

- No candidate artifact generation.
- No source-record artifact generation.
- No current-fact export artifact generation.
- No generated artifact under `data/current-facts/`.
- No generated summary under `docs/current-facts/`.
- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier behavior change.
- No parser/classifier expansion.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No source acquisition implementation.
- No live acquisition.
- No authority promotion.

## Public Input Inventory

### Parsed-Value Classifier Coverage

Artifact:

- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`

Useful fields:

- `run_id`;
- `review_item_id`;
- `source_name`;
- `source_role`;
- `source_header_path`;
- `proposed_field_key`;
- `semantic_source_family`;
- `parser_rule_ids`;
- `calculation_input_status`;
- `value_shape_classifier_status`;
- raw-value variant `raw_value`, `raw_value_length`, and `raw_value_sha256`
  for partial coverage groups.

Limits:

- group-level or raw-value-variant-level only;
- no committed `character_slug`;
- no committed `move_id`;
- no committed `display_label_ja`;
- no committed source row/cell/value keys;
- no committed row/cell order;
- no complete per-candidate `evidence` object;
- no full candidate `parsed_value` payload for every row/move/cell record;
- raw-value hash includes `sha256:` prefix while candidate schema expects the
  raw 64-character hex digest.

### Official Note-Linkage Source Review

Artifacts:

- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`

Useful fields:

- `run_id`;
- source-review result counts;
- `review_item_id`;
- `source_review_id`;
- `source_name`;
- `source_role`;
- `source_header_path`;
- `proposed_field_key`;
- representative raw examples with length and hash;
- reviewed statuses such as `structured_row_note_evidence_found`,
  `structured_row_note_evidence_ambiguous`, and
  `source_confirmed_non_note_grammar_blocked`;
- `later_parser_eligibility` values.

Limits:

- representative examples only, not a complete candidate record list;
- `affected_count` and `representative_match_count` are counts, not
  candidate identities;
- no committed `character_slug` per representative;
- no committed `move_id`;
- no committed `display_label_ja`;
- no committed source row/cell/value keys;
- no committed row/cell order;
- ambiguous groups remain blocked;
- later parser eligibility is not candidate artifact approval.

### Acquisition Report

Artifact:

- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

Useful fields:

- `run_id`;
- captured source families;
- official/SuperCombo capture success counts;
- per-character public metadata hashes and row/table counts in the machine
  report;
- `official_table_rows_schema_version == "official_table_rows_raw/v4"`;
- `official_table_rows_hash`;
- source URLs and source revision labels.

Limits:

- raw table rows are explicitly ignored local captures;
- no public row payload;
- no public row/cell/value keys;
- no public candidate raw values per row;
- no parser decisions;
- no candidate `parsed_value`;
- no authority promotion.

### Schemas, Validators, And Audit

Artifacts:

- `contracts/current-facts/*.schema.json`;
- `tests/validation/validate_current_fact_row_move_cell_candidates.py`;
- `tests/validation/validate_current_fact_source_records.py`;
- `tests/validation/validate_current_fact_export_generator.py`;
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`;
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`.

Useful fields:

- record shapes and closed enum contracts;
- summary-safe public path requirements;
- non-scalar guard requirements for `annotated_numeric_candidate` and
  `frame_range`;
- validator evidence boundaries.

Limits:

- schema and synthetic fixtures are contract evidence only;
- validators do not prove source truth;
- no production candidate records are produced.

## Required Candidate Evidence

Every production candidate record needs committed public evidence for:

- `candidate_record_id`;
- `character_slug`;
- `move_id`;
- `field_key`;
- `display_label_ja`;
- `source_row_key`;
- `source_cell_key`;
- `source_value_key`;
- `source_row_order`;
- `source_cell_order`;
- `source_header_path`;
- exact `raw_value`;
- `raw_value_length`;
- 64-character `raw_value_sha256`;
- `source_name`;
- `source_role`;
- `source_family`;
- `source_label`;
- `authority_status`;
- `evidence`;
- `source_review_refs`;
- `coverage_refs`;
- `acquisition_report_refs`;
- `parsed_value`;
- `value_shape`;
- `parser_rule_ids`;
- `calculation_input_status`.

The evidence must be public, committed, and summary-safe. It must not depend
on legacy raw exports, `.local`, raw HTML, screenshots, VLM output, local
paths, cookies, profiles, traces, logs, or private data as authority.

## Field Support Review

| Candidate field group | Existing public support | Missing blocker |
| --- | --- | --- |
| Artifact version, run ID, authority/candidate boundaries | Supported by schemas and acquisition report run ID | None for planning |
| `generated_from` refs | Supported as public committed paths | Must be selected by future artifact implementation |
| `source_name`, `source_role`, `source_family`, `field_key`, `source_header_path`, parser rule/status policy | Partially supported by classifier coverage and source review | Needs per-candidate row/move/cell linkage |
| `raw_value`, `raw_value_length`, `raw_value_sha256` | Supported for raw variants and representative examples | Not complete for every row/move/cell candidate; hash format normalization must be reviewed |
| `character_slug`, `move_id`, `display_label_ja` | Acquisition report has character slugs; source review confirms public character/move reference in summary wording | No committed candidate-level mapping from raw value to character/move/display label |
| `source_row_key`, `source_cell_key`, `source_value_key`, row/cell order | Planned by schema | Not present in public artifacts |
| `parsed_value` | Deterministic parser/classifier can produce reviewed shapes in implementation surfaces; coverage records only expose kind/status and parser rule IDs | No committed per-candidate parsed payload tied to row/move/cell identity |
| `evidence`, `source_review_refs`, `coverage_refs`, `acquisition_report_refs` | Referenced artifacts exist | Per-candidate evidence object is not present |
| non-scalar guard status for `annotated_numeric_candidate` / `frame_range` | Supported by schema, guard helper, coverage status, and validators | Must be carried into future candidate artifact |
| blocked/review-required exclusion | Supported by coverage and source-review status | Candidate artifact implementation must enforce exclusion |

## Decision

Existing public summaries are not sufficient to generate a production
`current_fact_row_move_cell_candidate_input/v1` artifact.

The next step must be a source-review/acquisition amendment plan, not candidate
artifact generation.

Required amendment goal:

- produce a committed, summary-safe public candidate-source review input that
  maps reviewed parsed raw values to row/move/cell identity without exposing
  raw HTML, full rows, ignored `.local` paths, screenshots, VLM output, or
  private data.

The amendment must decide whether the row/move/cell candidate list can be
reviewed from existing ignored v4 artifacts, or whether acquisition needs an
additional summary-safe derived artifact. It must not treat legacy
`data/exports/<character>/official_raw.json` as the replacement source input.

## Candidate Artifact Generation Gate

Candidate artifact implementation remains blocked until the future amendment
provides public, reviewed evidence for the missing candidate fields.

Before generating a candidate artifact, mandatory review must confirm:

- every included record is lookup-ready and has `parsed_value`;
- blocked/review-required records remain out of valid candidate artifacts;
- each record has public row/move/cell identity evidence;
- exact raw values and hashes match reviewed public evidence;
- official records remain `authority_candidate`;
- SuperCombo remains enrichment/cross-reference only and never scalar numeric
  authority;
- `annotated_numeric_candidate` and `frame_range` remain non-scalar;
- source references are public committed artifacts only;
- no production artifact uses legacy raw exports, `.local`, raw HTML,
  screenshots/VLM as authority, local paths, logs, or private data.

## Issue #343 Gate

Issue #343 remains mandatory for any new value-handling decision.

If a future source-review/acquisition amendment or candidate artifact includes
new raw-value semantics, newly included raw variants, or same-grammar
expansion, the implementation must first create a sanitized reviewer bundle
under:

- `.local/reviewer-evidence/value-double-check/<run-id>/`

Human upload remains manual. ChatGPT/VLM output is
`observation_candidate` only. It is not source truth, validator evidence,
parser/schema approval, calculation-safe promotion, or numeric authority.

The bundle, zip, screenshots, raw HTML, full rows, local paths, and ChatGPT
full output must not be committed.

## Future Implementation Slices

Recommended next PR:

1. Docs-only source-review/acquisition amendment plan for candidate public row
   identity evidence.

Blocked until that plan is approved:

2. Candidate public source-review artifact implementation.
3. Production candidate artifact generation.
4. Production source-record artifact generation.
5. Production current-fact export generation.
6. Runtime lookup transition and legacy raw export retirement.

## Acceptance Criteria

- The plan is docs-only.
- The plan inventories public inputs available after PR #363.
- The plan defines exact evidence needed to populate candidate records.
- The plan identifies supported and missing candidate fields.
- The plan decides whether candidate artifact implementation can start.
- The plan keeps Issue #343 double-check gate mandatory for future
  value-handling decisions.
- The plan does not generate candidate, source-record, or export artifacts.
- The plan does not change runtime lookup, `current_facts.py`, `answering.py`,
  parser/classifier behavior, retrieval, answer, calculator, SymPy, source
  acquisition, or live acquisition.
- The plan does not use legacy `data/exports/*/official_raw.json` as
  replacement source input.
- The plan does not use `.local`, raw HTML, screenshots, VLM output, or
  private data as authority.

## Files / Interfaces

This docs-only PR should change only:

- `docs/execplans/2026-05-25-current-fact-candidate-public-artifact-source-review.md`

Future implementation plans may touch additional files only after mandatory
review approval.

## Validation Commands

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-25: Drafted docs-only source-review plan after PR #363 merged. No
  implementation or generated artifact changes included.
- 2026-05-25: Ran validation commands for docs-only plan. All checks passed.

## Decision Log

- 2026-05-25: Existing public summaries are insufficient for production
  candidate artifact generation because they do not provide complete
  row/move/cell candidate identity.
- 2026-05-25: Candidate artifact generation remains blocked.
- 2026-05-25: Next step is a source-review/acquisition amendment plan for
  summary-safe public row/move/cell candidate evidence.
- 2026-05-25: Legacy raw exports remain rejected as replacement source input.
- 2026-05-25: Validation passed without adding implementation, schemas,
  fixtures, validators, or generated artifacts.

## Deviations

- None.

## Risks

- A source-review/acquisition amendment may still find that current ignored
  v4 artifacts lack enough deterministic row/move/cell identity for a public
  candidate artifact.
- Production candidate/source-record/export artifacts remain blocked.
- Runtime remains legacy raw export backed.
- First production candidate coverage may be limited by parsed-value-only
  admission and reviewed public identity requirements.
- Candidate population may require careful hash normalization from
  `sha256:<hex>` policy artifacts to raw 64-character schema hashes.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Public input inventory | Draft plan only | `docs/execplans/2026-05-25-current-fact-candidate-public-artifact-source-review.md` | `git diff --check`; `uv lock --check` | Pass | None | Mandatory review pending | Existing public inputs may require amendment |
| Candidate generation decision | Draft plan decides candidate generation remains blocked | Same | `validate_current_fact_row_move_cell_candidates.py`; `parsed_value_classifier validate` | Pass | None | Mandatory review pending | Production candidate artifact remains blocked |
| Runtime and artifact boundary | No runtime or generated artifact changes | Same | `validate_clean_slate.py`; current-fact validators | Pass | None | Mandatory review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-candidate-public-artifact-source-review.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only.
- It inventories public inputs after PR #363:
  - parsed-value classifier coverage
  - official note-linkage source-review summaries
  - acquisition reports
  - current-fact schemas/validators
  - validator audit boundaries
- It defines exact evidence required to populate current_fact_row_move_cell_candidate_input/v1 records from committed public artifacts.
- It identifies which required candidate fields are supported and which are missing.
- It decides whether candidate artifact implementation can start.
- It keeps Issue #343 double-check gate mandatory for future value-handling decisions.
- It does not generate candidate artifacts, source-record artifacts, or current-fact export artifacts.
- It does not change runtime lookup, current_facts.py, answering.py, parser/classifier behavior, retrieval, answer, calculator, SymPy, source acquisition, or live acquisition.
- It rejects legacy data/exports/*/official_raw.json as replacement source input.
- It does not use .local, raw HTML, screenshots, VLM output, or private data as authority.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining risks, and whether docs-only stage/commit is approved.
```
