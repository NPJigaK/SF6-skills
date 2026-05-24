# Current-Fact Source-Record Input Artifact

Status: Drafted for review; validation passed.

## Purpose

Define the reviewed row/move/cell-level source-record input artifact required
before production `current_fact_export/v2` generation.

This plan is docs-only. It does not implement source-record extraction,
generator code, generated artifacts, runtime lookup, answer behavior,
parser/classifier behavior, retrieval, calculators, SymPy logic, or live
acquisition.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `docs/execplans/2026-05-25-current-fact-export-generator.md`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/validation/validate_current_fact_consumer_guards.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

## Context

The repository now has the current-fact status carrier and a planned export
generator path:

- `current_fact_record.schema.json` requires top-level
  `calculation_input_status`;
- `current_fact_export.schema.json` requires
  `artifact_schema_version == "current_fact_export/v2"`;
- lookup-ready export records require `parsed_value`;
- export `generated_from` rejects legacy `data/exports/*` paths;
- PR #355 documented that group-level parsed-value classifier coverage is not
  enough to generate production current-fact records.

The remaining blocker is a reviewed public input artifact that carries
row/move/cell identity alongside reviewed parsed-value and source-boundary
metadata. This plan defines that missing input surface.

## Scope

Included in this docs-only plan:

- choose the source-record artifact path and schema/version direction;
- define allowed and excluded source inputs;
- define row/move/cell identity requirements;
- define required source-record fields for lookup-ready current facts;
- decide parsed-value-only admission for the first lookup-ready source-record
  artifact;
- decide how blocked/review-required records are represented outside the
  lookup-ready source-record artifact;
- define source/evidence/authority/status carry-forward rules;
- define privacy, source-boundary, and guard validator requirements;
- preserve the Issue #343 screenshot plus ChatGPT/VLM double-check gate for
  future value semantics changes;
- preserve the legacy raw export retirement boundary.

Excluded:

- No source-record extraction implementation.
- No export generator implementation.
- No generated production current-fact export artifact.
- No generated production source-record artifact.
- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier expansion.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No live acquisition.
- No authority promotion.

## Artifact Path And Schema Decision

Future reviewed source-record input artifacts should live under a distinct
current-fact input path, not under the legacy raw export tree.

Planned JSON artifact path:

- `data/current-facts/source-records/<run_id>-current-fact-source-records.json`

Optional summary-safe Markdown path:

- `docs/current-facts/source-records/<run_id>-current-fact-source-records.md`

Planned schema path for the future implementation:

- `contracts/current-facts/current_fact_source_record_input.schema.json`

Planned artifact schema version:

- `current_fact_source_record_input/v1`

The source-record artifact is an input contract, not the final normalized
export. It may carry source-row identity fields that are not part of
`current_fact_record.schema.json`. A later export generator must strip
source-record-only identity fields when writing `current_fact_export/v2`
records and must validate the output against the current-fact export schema.

The future schema should use this high-level shape:

- `artifact_schema_version`;
- `run_id`;
- `generated_from`;
- `authority_boundary`;
- `source_record_boundary`;
- `records`.

This plan does not implement that schema.

## Allowed Public Inputs

The future source-record artifact may be built only from reviewed public
inputs:

- parsed-value classifier coverage for approved parsed values, value-shape
  policy, parser rule IDs, and calculation status compatibility;
- official source-review artifacts for reviewed note/linkage decisions;
- acquisition reports for public hashes/counts and run metadata;
- current-fact schemas;
- current-fact guard contracts and validators;
- reviewed public source-review summaries.

These inputs can be referenced in `generated_from` and in record `evidence`
only when the referenced path is public, summary-safe, and committed under
`data/`, `docs/`, or `contracts/`.

## Excluded Inputs

The future source-record artifact must not use these as authority or source
inputs:

- legacy `data/exports/<character>/official_raw.json`;
- `.local` raw rows;
- raw HTML;
- full raw row dumps;
- screenshots;
- ChatGPT/VLM observations as authority;
- cookies, browser profiles, headers, tokens, traces, debug dumps, logs, or
  private data;
- local absolute paths;
- SuperCombo numeric values as authority.

Ignored `.local` artifacts may be reviewer input for an explicitly approved
source-review or acquisition-update workflow, but they must not appear in the
public source-record artifact, its `generated_from`, or its public evidence
paths.

## Row/Move/Cell Identity Requirements

The source-record artifact must identify the source row, move, cell, and value
without publishing full raw rows or raw HTML.

Future source records should include deterministic input-only identity fields,
for example:

- `source_record_id`;
- `source_row_key`;
- `source_cell_key`;
- `source_value_key`;
- `source_row_order`;
- `source_cell_order`;
- `source_header_path`;
- `raw_value_sha256`;
- `raw_value_length`.

Identity requirements:

- `source_record_id` must be stable for the same character, move, field,
  source cell, and raw value;
- `source_row_key` must identify the source row without embedding full row
  text;
- `source_cell_key` must identify the source column/cell without embedding
  full cell payloads beyond the reviewed raw value;
- `source_value_key` must distinguish multiple values inside one source cell
  when raw-value-level partial acceptance is needed;
- row/cell order fields may be included for deterministic sorting but must not
  be the only identity;
- `source_header_path` must preserve source-native column/header context;
- `raw_value` must be preserved exactly in the current-fact record payload;
- hashes and lengths may be used to cross-check raw values without publishing
  full rows.

The final `current_fact_export/v2` record does not carry these source-record
identity fields unless a later schema plan explicitly adds them.

## Required Source-Record Fields

Every lookup-ready source record must carry a current-fact record payload with
the existing current-fact fields required for export generation.

Required current-fact payload fields:

- `record_id`;
- `character_slug`;
- `move_id`;
- `field_key`;
- `display_label_ja`;
- `raw_value`;
- `parsed_value`;
- `value_shape`;
- `source_name`;
- `source_role`;
- `source_family`;
- `source_label`;
- `source_header_path`;
- `authority_status`;
- `evidence`;
- `calculation_input_status`.

The payload must be valid as, or directly transformable into, a
`current_fact_record.schema.json` record after source-record-only identity
fields are removed.

## Parsed-Value-Only Admission

Decision for the first lookup-ready source-record input artifact:

- admit only records with `parsed_value`;
- admit only records with top-level `calculation_input_status`;
- reject review-required/no-parsed-value records from the lookup-ready
  source-record artifact;
- reject `out_of_scope_not_emitted` records;
- reject records whose source input depends on legacy raw exports;
- preserve `raw_value` exactly;
- preserve `value_shape` and parser/policy status metadata;
- preserve source, authority, evidence, and calculation status fields.

Rationale:

- lookup-ready source records are the direct input to the production
  `current_fact_export/v2` generator;
- admitting no-parsed-value records would recreate legacy raw lookup under a
  new artifact name;
- blocked values already have reviewed homes in classifier coverage and
  source-review artifacts.

## Blocked And Review-Required Records

Decision for the first source-record artifact:

- blocked/review-required records remain in parsed-value classifier coverage
  and source-review artifacts;
- no separate blocked current-fact source-record artifact is created in this
  first slice;
- if future hold-message, audit, or reviewer UI needs blocked current-fact
  metadata, it must use a separate docs-only plan for a blocked-metadata
  artifact or a reviewed nullable parsed-value schema.

The lookup-ready source-record artifact must not use
`review_required_not_calculation_safe` to smuggle raw-only records into the
current-fact export. That status may remain valid in record-shape fixtures, but
not in lookup-ready source records unless a later plan changes admission
rules.

## Carry-Forward Rules

Source records must carry forward source, evidence, authority, and status
fields without promotion.

Required carry-forward behavior:

- `raw_value` is copied exactly from the reviewed value record;
- `parsed_value` is copied as structured data, not flattened;
- `value_shape` is copied with parser rule, disposition, policy, and
  calculation status context where present;
- `calculation_input_status` is copied from the reviewed classifier/source
  decision and must be one of the closed schema enum values;
- `source_name`, `source_role`, `source_family`, `source_label`, and
  `source_header_path` are copied from reviewed public source metadata;
- `authority_status` is copied without promotion;
- official records remain `authority_candidate`;
- SuperCombo records remain enrichment or cross-reference only and must not
  provide numeric authority;
- `evidence` references only public reviewed artifacts and summary-safe
  source reports.

The source-record artifact must not:

- promote official `authority_candidate` to current-fact authority;
- promote SuperCombo values to numeric authority;
- derive status from `parsed_value.kind` alone;
- infer missing source context from move labels or raw text;
- use ChatGPT/VLM observations as evidence.

## Guard Requirements

Future validators and generators must keep parsed-but-non-scalar values from
being consumed as scalar facts.

Required guard checks:

- call `is_scalar_calculation_input(parsed_value, calculation_input_status)`
  or enforce an equivalent validator before any scalar consumer accepts a
  record;
- `annotated_numeric_candidate` remains display/search/review metadata only
  while status is `annotated_candidate_not_calculation_safe`;
- `annotated_numeric_candidate.numeric_candidate` must not be flattened into
  `integer`, `signed_frame`, or exact scalar answer text;
- `frame_range` remains an interval/range while status is
  `parsed_range_not_single_value_calculation_safe`;
- `frame_range.start` and `frame_range.end` must not be collapsed into a
  scalar, best/worst value, or representative value;
- `enum_token`, `ordered_pair`, raw-preserved, not-authority, and blocked
  statuses remain non-scalar;
- `eligible_only_after_domain_source_and_unit_checks` is necessary but not
  sufficient for exact scalar answers.

## Privacy And Source-Boundary Validators

Future implementation must add focused validators before committing any
production source-record artifact.

Required validators:

- schema validation for `current_fact_source_record_input/v1`;
- every lookup-ready source record includes `parsed_value` and top-level
  `calculation_input_status`;
- every current-fact payload validates as, or deterministically transforms
  into, a `current_fact_record.schema.json` record;
- `generated_from` uses reviewed public inputs only and rejects
  `data/exports/`, `.local`, raw HTML, screenshots, and private paths;
- source-record identity fields do not contain full raw rows or local absolute
  paths;
- evidence paths are public reviewed artifacts only;
- official and SuperCombo authority boundaries remain unchanged;
- no flattened `annotated_numeric_candidate`;
- no collapsed `frame_range`;
- privacy scan rejects raw HTML, screenshots, full rows, cookies, profiles,
  headers, tokens, traces, debug dumps, logs, local paths, and private data;
- deterministic ordering by source, character, move, field, source-row/cell
  key, and record ID.

Validators must be evidence-first. They must be grounded in public reviewed
artifacts, schema contracts, guard contracts, synthetic fixtures, or privacy
boundaries. They must not be weakened to match generated output.

## Issue #343 Double-Check Gate

Issue #343 screenshot plus ChatGPT/VLM double-check remains mandatory whenever
a future source-record implementation introduces new value-handling semantics
or expands raw-value admission beyond already reviewed values.

Gate requirements:

- create `.local/reviewer-evidence/value-double-check/<run-id>/`;
- use Scrapling screenshots for the target pages;
- include screenshots, manifest JSON, ChatGPT prompt, and target value
  summary;
- zip the bundle under `.local/reviewer-evidence/value-double-check/`;
- a human manually uploads the zip and prompt to ChatGPT;
- ChatGPT/VLM output is `observation_candidate` only;
- any mismatch, uncertainty, or unreadable target blocks the new
  value-handling decision until source review resolves it;
- do not commit `.local`, zip files, screenshots, raw HTML, full rows, local
  paths, or ChatGPT full output.

The double-check gate is reviewer support. It is not source truth, validator
evidence, parser approval, calculation-safe promotion, or numeric authority.

## Legacy Raw Export Retirement Boundary

Legacy `data/exports/<character>/official_raw.json` remains technical debt.

Boundary decisions:

- legacy raw exports are not source input for source-record artifacts;
- legacy raw exports must not appear in source-record `generated_from`;
- no compatibility fields should be added only to support legacy raw exports;
- legacy raw exports may be referenced by a later parity validator only as the
  current behavior being retired;
- retirement can happen only after source-record input, production export,
  lookup parity, rollback criteria, and runtime switch are reviewed.

Intended future sequence:

1. Implement source-record schema, fixtures, and validators.
2. Produce a reviewed source-record input artifact from public reviewed inputs.
3. Implement production current-fact export generation from that artifact.
4. Review generated export source, authority, status, guard, and privacy
   boundaries.
5. Plan and implement parsed-value-backed lookup with parity and rollback
   criteria.
6. Retire legacy raw export dependency in a dedicated PR.

## Acceptance Criteria

- The ExecPlan is docs-only.
- The ExecPlan defines the source-record artifact path and schema/version
  direction.
- The ExecPlan defines allowed public inputs and excluded inputs.
- The ExecPlan defines row/move/cell identity requirements.
- The ExecPlan lists required current-fact payload fields, including
  `display_label_ja`, `parsed_value`, `evidence`, `authority_status`, and
  `calculation_input_status`.
- The ExecPlan requires parsed-value-only admission for lookup-ready source
  records.
- The ExecPlan keeps blocked/review-required records in classifier and
  source-review artifacts unless a later plan approves a separate artifact.
- The ExecPlan defines source/evidence/authority/status carry-forward rules.
- The ExecPlan requires privacy and source-boundary validators.
- The ExecPlan requires no flattened `annotated_numeric_candidate` and no
  collapsed `frame_range`.
- The ExecPlan preserves the Issue #343 double-check gate for future value
  semantics changes.
- The ExecPlan excludes generator implementation, generated artifacts, runtime
  lookup, answer behavior, parser/classifier expansion, retrieval, calculator,
  SymPy, live acquisition, legacy raw exports as source input, `.local`, raw
  HTML, screenshots/VLM as authority, private data, and SuperCombo numeric
  authority.
- Validation commands pass.

## Files / Interfaces

This docs-only plan changes only:

- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`

Future implementation plans may touch, after review:

- `contracts/current-facts/current_fact_source_record_input.schema.json`;
- focused source-record fixtures under `tests/fixtures/current-facts/`;
- focused validators under `tests/validation/`;
- source-record generation code only if a later ExecPlan approves it;
- `data/current-facts/source-records/` and
  `docs/current-facts/source-records/` artifacts only after schema/validator
  review.

This plan does not authorize current-fact export generation or runtime lookup
changes.

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-25 JST) PR #355 was marked ready and merged with normal merge
  commit `cf11618b4e340bdda19057cdf2bba3487e5d9917`.
- [x] (2026-05-25 JST) Local `main` was confirmed at
  `cf11618b4e340bdda19057cdf2bba3487e5d9917`, matching `origin/main`, with a
  clean worktree.
- [x] (2026-05-25 JST) Created branch
  `plan/current-fact-source-record-input-artifact`.
- [x] (2026-05-25 JST) Inspected current-fact v2 schemas, the current-fact
  export generator plan, and current-fact export design decisions.
- [x] (2026-05-25 JST) Drafted this docs-only source-record input artifact
  ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, current-fact schema validator,
  current-fact consumer guard validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Use a dedicated source-record input artifact under
  `data/current-facts/source-records/`.
  Rationale: The source-record input needs row/cell identity that should not be
  confused with final normalized `current_fact_export/v2` records.
  Date/Author: 2026-05-25 / Codex

- Decision: Use future artifact schema version
  `current_fact_source_record_input/v1`.
  Rationale: This is a new input contract, not a revision of the final export
  contract.
  Date/Author: 2026-05-25 / Codex

- Decision: The first lookup-ready source-record artifact is parsed-value-only.
  Rationale: Review-required/no-parsed-value records would recreate legacy raw
  lookup behavior and already belong in classifier/source-review artifacts.
  Date/Author: 2026-05-25 / Codex

- Decision: Do not create a blocked/review-required current-fact source-record
  artifact in the first slice.
  Rationale: No current consumer needs that surface yet, and adding it now
  would expand schema and privacy review before lookup-ready export exists.
  Date/Author: 2026-05-25 / Codex

- Decision: Exclude legacy raw exports from source-record input.
  Rationale: `official_raw.json` is the technical-debt surface being retired
  and must not become the source of the replacement pipeline.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: Source-record input is evidence/status plumbing, not arithmetic.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- Exact source-record schema field names need implementation review.
- A production source-record artifact still does not exist.
- The first production source-record artifact may have limited coverage because
  it admits only records with reviewed `parsed_value`.
- Runtime lookup remains legacy raw export backed.
- Export generator, lookup parity, rollback criteria, and legacy raw export
  retirement remain future work.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only source-record plan | Drafted source-record input artifact plan, path/schema direction, input boundaries, identity requirements, admission rules, carry-forward rules, validators, and retirement boundary | `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md` | `git diff --check`; `uv lock --check`; clean-slate validator; current-fact schema validator; current-fact guard validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Production source-record artifact missing |
| Artifact path/schema direction | Planned `data/current-facts/source-records/<run_id>-current-fact-source-records.json`, optional Markdown summary, and future `current_fact_source_record_input/v1` schema | This ExecPlan only | Diff/status review | Passed | None | Review pending | Schema implementation still future work |
| Parsed-value-only admission | Required lookup-ready source records to include `parsed_value` and top-level `calculation_input_status`; blocked no-parsed records remain in classifier/source-review artifacts | This ExecPlan only | Diff/status review | Passed | None | Review pending | Coverage limited by parsed-value availability |
| Guard/privacy/source boundary | Required no flattened annotated candidates, no collapsed frame ranges, reviewed public evidence only, and privacy/source-boundary validators | This ExecPlan only | Diff/status review | Passed | None | Review pending | Validator implementation still future work |
| Runtime/generator exclusion | Kept current-fact export generation, runtime lookup, answers, retrieval, calculators, SymPy, live acquisition, and parser/classifier expansion out of scope | This ExecPlan only | Diff/status review | Passed | None | Review pending | Runtime remains legacy raw backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only and does not implement source-record extraction,
  generator code, generated artifacts, runtime lookup, answer behavior,
  parser/classifier behavior, retrieval, calculator, SymPy, or live
  acquisition.
- Artifact path is
  data/current-facts/source-records/<run_id>-current-fact-source-records.json
  with optional docs/current-facts/source-records/<run_id>-current-fact-source-records.md.
- Future schema/version direction is
  contracts/current-facts/current_fact_source_record_input.schema.json with
  artifact_schema_version current_fact_source_record_input/v1.
- Allowed inputs are reviewed public artifacts only.
- Excluded inputs include legacy data/exports/<character>/official_raw.json,
  .local, raw HTML, screenshots/VLM as authority, private data, and SuperCombo
  numeric authority.
- Row/move/cell identity requirements are defined without publishing full raw
  rows or raw HTML.
- Required fields include character_slug, move_id, field_key,
  display_label_ja, raw_value, parsed_value, value_shape, source_name,
  source_role, source_family, source_label, source_header_path, evidence,
  authority_status, and calculation_input_status.
- Lookup-ready source records are parsed-value-only.
- Blocked/review-required records remain in classifier/source-review artifacts
  unless a later plan approves a separate metadata artifact.
- Source/evidence/authority/status carry-forward rules do not promote
  authority.
- Privacy/source-boundary validators are evidence-first.
- Guard checks require no flattened annotated_numeric_candidate and no
  collapsed frame_range.
- Issue #343 screenshot plus ChatGPT/VLM double-check gate remains required
  for new value semantics decisions.
- Legacy raw export retirement boundary is preserved.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations,
remaining risks, and whether docs-only stage/commit is approved.
```
