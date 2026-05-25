# Current-Fact Row/Move/Cell Candidate Input

Status: Drafted for review; validation passed.

## Purpose

Define the reviewed public row/move/cell candidate input artifact required
before production current-fact source-record artifact generation.

The previous production source-record plan established that production
`current_fact_source_record_input/v1` artifacts remain blocked until a
reviewed public input exists with row, move, cell, raw value, parsed value,
source, authority, and status evidence. This plan defines that intermediate
candidate artifact boundary without generating any production artifact.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`
- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`
- `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

## Context

The repository has a tested contract for source-record inputs and an in-memory
fixture-contract generator, but no production row/move/cell input.

Current blockers:

- parsed-value classifier coverage is group-level and raw-value-variant-level,
  not row/move/cell-level;
- source-review summaries record reviewed decisions and blocked cases, not a
  full lookup-ready candidate list;
- acquisition reports expose summary hashes and counts, not public row
  records;
- legacy `data/exports/<character>/official_raw.json` is technical debt and
  cannot be used as the replacement source input;
- ignored `.local` artifacts may help reviewers, but they cannot be committed
  or cited as public artifact authority.

This plan creates the missing design step: a summary-safe candidate input that
maps reviewed parsed values to row/move/cell identity before any production
source-record artifact is generated.

## Scope

Included in this docs-only plan:

- define candidate artifact path and schema/version direction;
- define candidate artifact public/private boundary;
- define row/move/cell identity fields;
- define lookup-ready candidate requirements;
- define how candidate records cross-check classifier coverage, source-review
  summaries, acquisition reports, schemas, and guard contracts;
- define whether blocked/review-required records are included;
- define validators required before any candidate artifact implementation;
- preserve parsed-value-only admission for the eventual source-record input;
- preserve non-scalar `annotated_numeric_candidate` and `frame_range`
  boundaries;
- preserve Issue #343 double-check gate for any new value-handling decision.

Excluded:

- No candidate artifact implementation.
- No production source-record artifact generation.
- No production current-fact export artifact generation.
- No generated artifact under `data/current-facts/`.
- No generated summary under `docs/current-facts/`.
- No generator code changes.
- No file-writing wrapper.
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

## Candidate Artifact Path And Schema

The candidate input should be a distinct reviewed public artifact, separate
from both the final source-record input and the final current-fact export.

Planned JSON path:

- `data/current-facts/candidate-inputs/<run_id>-row-move-cell-candidates.json`

Optional summary-safe Markdown path:

- `docs/current-facts/candidate-inputs/<run_id>-row-move-cell-candidates.md`

Planned schema path for a future implementation:

- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`

Planned artifact schema version:

- `current_fact_row_move_cell_candidate_input/v1`

The candidate artifact is not lookup output. It is a reviewed bridge from
public evidence to `current_fact_source_record_input/v1`. A later
implementation may transform approved candidate records into source records
only after this candidate artifact is reviewed and validated.

## Boundary

The candidate artifact must be summary-safe.

Allowed committed public inputs:

- parsed-value classifier coverage and policy artifacts;
- official source-review summary artifacts;
- acquisition reports for public hashes, counts, and run metadata;
- current-fact schemas and validators;
- current-fact guard contracts;
- reviewed public Markdown summaries;
- future reviewed public candidate summaries.

Excluded inputs and fields:

- legacy `data/exports/<character>/official_raw.json`;
- `.local` paths or payloads;
- raw HTML;
- full raw rows;
- screenshots;
- ChatGPT/VLM observations as authority;
- ChatGPT/VLM full output;
- local absolute paths;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, answer logs,
  training logs, or private data;
- SuperCombo numeric authority.

Screenshots and VLM observations may remain reviewer-only
`observation_candidate` material under approved `.local` workflows. They must
not be committed, listed in `generated_from`, or used as authority evidence in
the candidate artifact.

## Candidate Record Shape

The future candidate schema should use this high-level shape:

- `artifact_schema_version`;
- `run_id`;
- `generated_from`;
- `authority_boundary`;
- `candidate_boundary`;
- `records`.

Each candidate record should carry source identity and a nested
current-fact-like payload, without publishing full rows.

Required candidate identity fields:

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
- `raw_value`;
- `raw_value_length`;
- `raw_value_sha256`.

Required reviewed source fields:

- `source_name`;
- `source_role`;
- `source_family`;
- `source_label`;
- `authority_status`;
- `evidence`;
- `source_review_refs`;
- `coverage_refs`;
- `acquisition_report_refs`.

Required parsed/status fields for lookup-ready candidates:

- `parsed_value`;
- `value_shape`;
- `parser_rule_ids`;
- `calculation_input_status`.

Candidate identity keys must not embed full raw row text, local paths, raw
HTML, screenshots, cookies, profiles, traces, logs, or private data.

## Admission Decision

The first candidate artifact should be lookup-ready and parsed-value-only.

Allowed candidate records:

- records with a reviewed `parsed_value`;
- records with source/header/raw-value evidence that can be linked to public
  summaries without exposing full rows;
- records whose `calculation_input_status` is compatible with current-fact
  schema and guard expectations;
- official records that remain `authority_candidate`;
- SuperCombo records only when enrichment/cross-reference and not scalar
  numeric authority;
- `annotated_numeric_candidate` records only as non-scalar wrappers;
- `frame_range` records only as ranges.

Excluded candidate records:

- `review_required_not_calculation_safe`;
- `out_of_scope_not_emitted`;
- records with no `parsed_value`;
- records whose only row/move/cell evidence is legacy raw export data;
- records whose evidence depends on `.local`, raw HTML, screenshots, or VLM
  output as authority;
- records whose row/move/cell identity is ambiguous in public reviewed
  artifacts;
- same-grammar raw variants not covered by the Issue #343 double-check gate
  when new value handling is introduced.

Blocked and review-required values remain in classifier/source-review
artifacts until a separate reviewed plan changes their status. They must not
be included in the lookup-ready candidate artifact as placeholders.

## Cross-Checks

Future candidate generation or validation must cross-check each record:

- `raw_value_length` equals the exact raw value length;
- `raw_value_sha256` equals the exact raw value hash;
- `source_header_path` matches the reviewed source column path;
- `field_key` matches classifier/source-review expectations;
- `parser_rule_ids` match parsed-value classifier coverage;
- `parsed_value.kind` matches classifier coverage and guard expectations;
- `calculation_input_status` matches classifier coverage and current-fact
  schema;
- `annotated_numeric_candidate` is not flattened into `integer` or
  `signed_frame`;
- `frame_range` is not collapsed into a single scalar value;
- official source role remains `authority_candidate`;
- SuperCombo records cannot be scalar numeric authority;
- `generated_from` and evidence references point only to committed public
  `data/`, `docs/`, or `contracts/` artifacts;
- no legacy raw export path, `.local`, raw HTML, screenshot, VLM output, local
  path, or private-data marker appears in the artifact.

## Relationship To Source-Record Input

The candidate artifact is allowed to carry candidate-review fields that are
not part of `current_fact_source_record_input/v1`.

A later implementation may transform candidate records into
`current_fact_source_record_input/v1` records only if:

- the candidate artifact validates against its own schema;
- all candidate records are lookup-ready and parsed-value-only;
- the transform strips candidate-only review fields;
- source-record records validate against
  `current_fact_source_record_input.schema.json`;
- guard checks reject non-scalar values in scalar contexts;
- no production current-fact export artifact is generated in the same PR
  unless separately approved.

## Issue #343 Gate

Issue #343 remains mandatory for any new value-handling decision.

If a candidate artifact introduces new semantics, newly included raw variants,
or a same-grammar expansion beyond already reviewed values, implementation must
first create a sanitized reviewer bundle under:

- `.local/reviewer-evidence/value-double-check/<run-id>/`

The bundle may include screenshots, a manifest, target value summary, and
ChatGPT/VLM prompt. Human upload remains manual. Output is
`observation_candidate` only.

Any mismatch, unreadable target, uncertainty, or unreviewed same-grammar
variant blocks candidate artifact approval until the public source-review or
coverage artifact is updated. The bundle, zip, screenshots, raw HTML, full
rows, local paths, and ChatGPT full output must not be committed.

## Future Implementation Slices

This plan does not authorize implementation. Future work should be split into
small reviewed PRs:

1. Candidate schema/fixtures/validator:
   Add `current_fact_row_move_cell_candidate_input/v1` schema, synthetic
   fixtures, focused validator, and validator audit entries.

2. Candidate public artifact source-review plan:
   Decide whether existing public summaries can support candidate records, or
   whether a source-review/acquisition amendment is required first.

3. Candidate artifact generation:
   Generate the first public candidate artifact only from reviewed public
   inputs and validate privacy/source boundaries.

4. Source-record artifact generation:
   Transform reviewed candidates into
   `data/current-facts/source-records/<run_id>-current-fact-source-records.json`.

5. Current-fact export generation:
   Use the existing fixture-contract generator path only after the production
   source-record artifact is reviewed.

6. Runtime transition:
   Plan lookup parity, rollback, and legacy raw export retirement before
   touching `current_facts.py` or answer behavior.

## Acceptance Criteria

- The plan is docs-only.
- The plan defines candidate artifact path/schema/version direction.
- The plan keeps candidate artifacts summary-safe.
- The plan rejects legacy `data/exports/*/official_raw.json` as replacement
  source input.
- The plan does not authorize production source-record or export artifact
  generation.
- The plan preserves parsed-value-only admission.
- The plan keeps blocked/review-required records out of lookup-ready
  candidate artifacts.
- The plan preserves `annotated_numeric_candidate` and `frame_range`
  non-scalar guard boundaries.
- The plan keeps Issue #343 double-check gate mandatory for new
  value-handling decisions.
- The plan does not change runtime lookup, `current_facts.py`, `answering.py`,
  parser/classifier behavior, retrieval, answer, calculator, SymPy, source
  acquisition, or live acquisition.

## Files / Interfaces

This docs-only PR should change only:

- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`

Future implementation plans may touch schema, fixture, validator, or artifact
files only after mandatory review approval.

## Validation Commands

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-25: Drafted docs-only candidate input plan after PR #360 merged. No
  implementation or generated artifact changes included.
- 2026-05-25: Ran validation commands. They passed with only this new
  ExecPlan file untracked.

## Decision Log

- 2026-05-25: Candidate input gets its own artifact/schema boundary instead
  of being folded into source-record or export artifacts.
- 2026-05-25: First candidate artifact remains parsed-value-only and
  lookup-ready; blocked/review-required records stay in classifier and
  source-review artifacts.
- 2026-05-25: Legacy raw exports remain rejected as replacement source input.
- 2026-05-25: `.local` and screenshot/VLM materials remain reviewer-only and
  never public authority.

## Deviations

- None.

## Risks

- Existing public artifacts may still be insufficient to populate candidate
  records without another acquisition/source-review amendment.
- Production source-record artifact generation remains blocked until candidate
  input exists and is reviewed.
- Runtime remains legacy raw export backed.
- First production candidate coverage may be limited because lookup-ready
  records require parsed values and reviewed public row/move/cell identity.
- Candidate schema field names are still planning labels until the schema
  implementation ExecPlan is approved.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only candidate input plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md` | `git diff --check` | Pass | None | Mandatory review pending | Candidate implementation not started |
| Runtime and artifact boundary | No runtime or generated artifact changes | Same | `git status --short --branch` | Pass; one untracked ExecPlan file only | None | Mandatory review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only.
- Candidate artifact path/schema/version boundary is defined.
- Candidate artifact remains summary-safe.
- No production source-record artifact generation is authorized.
- No production current-fact export artifact generation is authorized.
- Legacy data/exports/*/official_raw.json is rejected as replacement source input.
- .local, raw HTML, full rows, screenshots/VLM as authority, local paths, cookies, profiles, traces, logs, private data, and ChatGPT full output are excluded from public artifacts.
- Parsed-value-only admission is preserved.
- review_required/no parsed_value records stay out of lookup-ready candidate artifacts.
- annotated_numeric_candidate and frame_range non-scalar guard boundaries are preserved.
- Issue #343 double-check gate remains required for new value-handling decisions.
- No runtime lookup, current_facts.py, answering.py, parser/classifier behavior, retrieval, answer, calculator, SymPy, source acquisition, or live acquisition changes are included.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining risks, and whether docs-only stage/commit is approved.
```
