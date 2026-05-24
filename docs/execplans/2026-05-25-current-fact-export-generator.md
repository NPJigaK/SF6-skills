# Current-Fact Export Generator

Status: Drafted for review; validation passed.

## Purpose

Plan a deterministic current-fact export generator for the reviewed
`current_fact_export/v2` contract, without implementing the generator or
creating generated export artifacts in this docs-only PR.

This plan follows:

- PR #352 current-fact export design amendment;
- PR #354 current-fact calculation status schema implementation;
- the AGENTS debt retirement rule for legacy raw exports.

The generator must not use the legacy
`data/exports/<character>/official_raw.json` surface as source input. Runtime
lookup must remain unchanged until a later lookup plan and parity review.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/validation/validate_current_fact_consumer_guards.py`
- `tests/validation/validate_parsed_value_classifier.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

## Context

The current repository now has the schema/status carrier needed for a v2
current-fact export:

- current-fact records require top-level `calculation_input_status`;
- `current_fact_export.schema.json` requires
  `artifact_schema_version == "current_fact_export/v2"`;
- lookup-ready export records require `parsed_value`;
- export `generated_from` rejects legacy `data/exports/*` paths.

The remaining blocker for a production current-fact export is input shape. The
public reviewed artifacts currently provide group-level policy and source
review evidence, plus acquisition hashes/counts. They do not yet provide a
public reviewed row/move/cell-level source-record artifact with:

- `character_slug`;
- `move_id`;
- `display_label_ja`;
- source column/header path;
- raw value;
- parsed value;
- source evidence fields;
- authority/status fields.

Therefore the first generator plan must keep source input boundaries explicit.
It must not quietly fall back to legacy raw exports or ignored `.local`
acquisition rows.

## Scope

Included in this docs-only plan:

- define the generator contract and output paths;
- define allowed and excluded input surfaces;
- decide how to handle the current public source-record input gap;
- define fixture-only generator validation for the first implementation;
- define validator expectations before any generated public export artifact is
  committed;
- preserve scalar guard, authority, and legacy debt boundaries.

Excluded from this docs-only PR:

- No export generator implementation.
- No generated current-fact export artifact.
- No generated Markdown summary.
- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier behavior change.
- No source acquisition or live acquisition.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No authority promotion.

## Output Artifact Contract

The production export artifact path remains:

- JSON: `data/current-facts/<run_id>-current-fact-export.json`
- optional summary: `docs/current-facts/<run_id>-current-fact-export.md`

The JSON artifact must validate against
`contracts/current-facts/current_fact_export.schema.json` and therefore must:

- use `artifact_schema_version == "current_fact_export/v2"`;
- set `authority_boundary.official == "authority_candidate_only"`;
- set `authority_boundary.supercombo ==
  "enrichment_or_cross_reference_only"`;
- list only reviewed public `generated_from` paths;
- exclude all `data/exports/*` legacy raw paths from `generated_from`;
- contain records that validate against the current-fact record schema;
- include `parsed_value` in every exported record;
- include top-level `calculation_input_status` in every exported record.

The optional Markdown summary must be summary-safe only. It may include counts,
source paths, status distributions, and validation summaries. It must not
include raw HTML, full rows, screenshots, local paths, cookies, profiles,
traces, debug dumps, logs, or private data.

## Source Input Decision

The generator may use only reviewed public source inputs.

Allowed source inputs:

- a future reviewed source-record input artifact under `data/` that already
  contains lookup-ready row/move/cell records conforming to the v2
  current-fact record contract;
- parsed-value classifier coverage for status compatibility, parser rule,
  value-shape, and policy cross-checks;
- official source-review artifacts for reviewed note/linkage status;
- acquisition reports for summary hashes/counts and run metadata;
- current-fact schemas and validators;
- synthetic fixture inputs under `tests/fixtures/current-facts/` for
  generator contract tests only.

Excluded source inputs:

- legacy `data/exports/<character>/official_raw.json`;
- `.local` raw rows;
- raw HTML;
- full raw row dumps;
- screenshots;
- ChatGPT/VLM observations as authority;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, or private
  data;
- SuperCombo numeric values as authority.

Decision: the first generator implementation should be fixture-contract only
unless a reviewed public source-record input artifact is added in the same
reviewed implementation plan. It must not emit a production
`data/current-facts/<run_id>-current-fact-export.json` artifact from
insufficient group-level coverage alone.

## Source-Record Input Gap

Current public artifacts are not enough for production export generation:

- parsed-value classifier coverage is group-level and does not carry
  character/move/cell identity for every fact;
- source-review artifacts summarize decisions and blocked status, not
  full lookup-ready current-fact rows;
- acquisition reports contain hashes/counts and source metadata, not public
  row payloads;
- legacy `official_raw.json` contains row-like data but is the technical-debt
  surface being retired and must not be the new export source.

Required future input before production export artifact generation:

- a reviewed public current-fact source-record artifact, or an equivalent
  reviewed extraction artifact, that contains only summary-safe, lookup-ready
  records with no private/local/raw-source payloads;
- each source record must already preserve raw value exactly and carry enough
  deterministic metadata to produce a v2 current-fact record;
- the artifact must be generated without using legacy `official_raw.json` as
  authority input.

This plan does not create that input artifact. If implementation review
decides to add it together with the generator, the implementation plan must
explicitly amend scope before coding.

## Generator Contract

Future generator code should be deterministic and small.

Proposed behavior:

1. Load a reviewed source-record input artifact.
2. Validate every input record has required source, authority, raw value,
   parsed value, value-shape, and calculation status fields.
3. Reject records without `parsed_value`.
4. Reject records whose source path or generated source references
   `data/exports/`.
5. Reject records with `.local`, raw HTML, full rows, screenshots, local
   absolute paths, cookies, profiles, traces, debug dumps, logs, or private
   data.
6. Build a `current_fact_export/v2` payload.
7. Sort records deterministically by
   `(source_name, character_slug, move_id, field_key, record_id)`.
8. Validate the output against the current-fact export schema.
9. Validate guard/authority boundaries before writing any artifact.
10. Write JSON with stable key ordering and trailing newline.

The generator must not:

- call `current_facts.py`;
- read legacy `official_raw.json`;
- call live acquisition;
- mutate parser/classifier behavior;
- flatten `annotated_numeric_candidate`;
- collapse `frame_range`;
- promote official or SuperCombo authority;
- create a runtime latest pointer.

## Record Admission Rules

For the first production export:

- admit only records with `parsed_value`;
- admit only records with top-level `calculation_input_status`;
- preserve `raw_value` exactly;
- preserve `value_shape`;
- preserve `source_name`, `source_role`, `source_family`, `source_label`,
  `source_header_path`, `authority_status`, and `evidence`;
- keep official records as `authority_candidate`;
- keep SuperCombo records as enrichment or cross-reference only;
- reject review-required/no-parsed-value records;
- reject `out_of_scope_not_emitted` records;
- reject records that use legacy raw export paths as source input.

Non-scalar parsed values may be present only as display/search/review metadata
in the export. They are not exact scalar answer inputs.

## Guard And Authority Validation

The generator must validate scalar guard behavior for any exported record that
could later be consumed by exact lookup.

Required checks:

- call `is_scalar_calculation_input(parsed_value, calculation_input_status)`
  or use an equivalent validator for every exported record;
- records with `annotated_candidate_not_calculation_safe` must remain
  non-scalar;
- records with `parsed_range_not_single_value_calculation_safe` must remain
  non-scalar;
- `annotated_numeric_candidate.numeric_candidate` must not be flattened into
  `integer`, `signed_frame`, or exact answer text;
- `frame_range.start` and `frame_range.end` must not be collapsed into a
  scalar;
- `not_numeric_authority` records must not become scalar candidates;
- `eligible_only_after_domain_source_and_unit_checks` remains necessary but
  not sufficient for exact answers.

Authority checks:

- official remains `authority_candidate`;
- SuperCombo remains enrichment/cross-reference only;
- the export must not claim current-fact authority promotion;
- the export must not change daily-answer behavior.

## Fixture Strategy

The first generator implementation should use fixture-only tests unless a
reviewed production source-record input artifact is explicitly approved.

Fixture inputs should cover:

- accepted synthetic scalar signed frame with
  `eligible_only_after_domain_source_and_unit_checks`;
- accepted non-scalar `annotated_numeric_candidate` that remains
  `annotated_candidate_not_calculation_safe`;
- accepted non-scalar `frame_range` that remains
  `parsed_range_not_single_value_calculation_safe`;
- rejected review-required/no-parsed-value input;
- rejected `out_of_scope_not_emitted` input;
- rejected `data/exports/*/official_raw.json` source reference;
- rejected SuperCombo numeric authority promotion;
- rejected local/private/raw-source content.

Fixture output should be generated in a temporary test directory or compared
in memory. The first generator implementation should not commit a production
`data/current-facts/` artifact unless the reviewed production input blocker is
resolved first.

## Validator Plan

Future implementation must add focused validators before any production export
artifact is committed.

Required validators:

- generator fixture validator:
  - validates deterministic output ordering;
  - validates v2 JSON schema compliance;
  - rejects missing `parsed_value`;
  - rejects legacy raw source paths;
  - rejects local/private/raw-source content;
  - rejects authority boundary violations.
- export artifact validator:
  - validates any committed `data/current-facts/*-current-fact-export.json`;
  - validates optional `docs/current-facts/*-current-fact-export.md` summary
    boundary;
  - checks `generated_from` paths are reviewed public inputs only;
  - checks status distribution and guard behavior.
- compatibility validator:
  - confirms exported statuses are in the closed schema enum;
  - confirms exported parsed-value kinds remain compatible with guard
    behavior;
  - confirms no exported record comes from legacy `official_raw.json`.

Validators must be evidence-first and must not be weakened to match generated
output.

## Future Implementation Slices

Recommended sequence:

1. Generator fixture-contract implementation.
   Add generator code, tests, and validators using synthetic fixture inputs
   only; do not commit production export artifacts.
2. Source-record input artifact plan.
   Define the reviewed public source-record artifact needed for production
   export generation.
3. Source-record input artifact implementation.
   Produce the reviewed source-record artifact without legacy raw export
   dependency or private/raw source leakage.
4. Production export generation implementation.
   Generate `data/current-facts/<run_id>-current-fact-export.json` and
   optional `docs/current-facts/<run_id>-current-fact-export.md`, with no
   runtime lookup change.
5. Export artifact mandatory review.
   Review source inputs, schema, guard behavior, authority boundaries, privacy
   boundary, and no-legacy dependency.
6. Parsed-value-backed lookup helper plan/implementation.
   Add lookup helper/tests only after export artifact review.

The generator fixture-contract implementation may be skipped if review chooses
to plan the source-record input artifact first.

## Acceptance Criteria

- The ExecPlan is docs-only.
- The ExecPlan does not implement generator code or generated artifacts.
- The ExecPlan keeps runtime lookup and answer behavior unchanged.
- The ExecPlan defines JSON and optional Markdown output paths.
- The ExecPlan identifies the public source-record input gap.
- The ExecPlan excludes legacy `official_raw.json`, `.local`, raw HTML,
  screenshots/VLM as authority, private data, and SuperCombo numeric authority
  as source inputs.
- The ExecPlan requires v2 schema validation and top-level
  `calculation_input_status`.
- The ExecPlan requires parsed-value-only lookup-ready records.
- The ExecPlan requires guard validation for scalar/non-scalar status.
- The ExecPlan keeps no flattened `annotated_numeric_candidate` and no
  collapsed `frame_range`.
- The ExecPlan keeps export generator implementation before runtime lookup.
- Validation commands pass.

## Files / Interfaces

This docs-only plan changes only:

- `docs/execplans/2026-05-25-current-fact-export-generator.md`

Future implementation plans may touch, after review:

- generator module under `src/sf6_knowledge_coach/`;
- focused generator tests under `tests/`;
- focused validators under `tests/validation/`;
- generator input/output fixtures under `tests/fixtures/current-facts/`;
- validator audit artifacts if new tests/validators require audit entries;
- optional `data/current-facts/` and `docs/current-facts/` artifacts only
  after the source-record input blocker is explicitly resolved.

This plan does not authorize runtime lookup changes.

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

- [x] (2026-05-25 JST) PR #354 was marked ready and merged with normal merge
  commit `c9d92ff9a4e285b19fb2bfad0f817da4f7106afb`.
- [x] (2026-05-25 JST) Local `main` was fast-forwarded to `origin/main` at
  `c9d92ff9a4e285b19fb2bfad0f817da4f7106afb`; main CI passed in run
  `26368738271`.
- [x] (2026-05-25 JST) Created branch `plan/current-fact-export-generator`.
- [x] (2026-05-25 JST) Inspected current-fact v2 schemas, PR #352 design,
  PR #354 schema/status carrier implementation, acquisition report summary,
  and parsed-value classifier coverage shape.
- [x] (2026-05-25 JST) Drafted this docs-only generator ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, current-fact schema validator,
  current-fact consumer guard validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Do not generate a production current-fact export from group-level
  classifier coverage alone.
  Rationale: Coverage lacks row/move/cell identity and would not be a
  lookup-ready source of current facts.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep the first generator implementation fixture-contract only
  unless a reviewed public source-record input artifact is approved.
  Rationale: This lets us lock generator determinism, schema, guard, and
  privacy behavior without smuggling legacy raw exports back in as source.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep legacy `official_raw.json` excluded from source inputs.
  Rationale: It is the technical-debt surface being retired and must not
  become the source of the replacement export.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep runtime lookup unchanged.
  Rationale: Export generation must be reviewed before any answer or lookup
  behavior changes.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: The generator writes reviewed records; it does not perform
  arithmetic.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- A production source-record input artifact does not exist yet.
- First generator implementation may be limited to fixture-contract validation
  until the source-record input gap is resolved.
- No `data/current-facts/` production export exists yet.
- Runtime lookup remains legacy raw export backed.
- Export coverage will be limited by parsed-value-only admission.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only generator plan | Drafted plan for deterministic current-fact export generator, source input boundaries, fixture-contract path, validators, and future slices | `docs/execplans/2026-05-25-current-fact-export-generator.md` | `git diff --check`; `uv lock --check`; clean-slate validator; current-fact schema validator; current-fact guard validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Source-record input blocker remains |
| Output artifact contract | Reaffirmed `data/current-facts/<run_id>-current-fact-export.json` and optional `docs/current-facts/<run_id>-current-fact-export.md` | This ExecPlan only | Diff/status review | Passed | None | Review pending | No artifact generated |
| Source input boundary | Allowed reviewed public source-record input and fixtures; excluded legacy raw exports, `.local`, raw HTML, screenshots/VLM as authority, private data, and SuperCombo numeric authority | This ExecPlan only | Diff/status review | Passed | None | Review pending | Production input artifact missing |
| Generator/validator strategy | Required v2 schema validation, deterministic ordering, parsed-value-only records, guard checks, authority checks, and privacy checks | This ExecPlan only | Diff/status review | Passed | None | Review pending | Generator implementation still future work |
| Runtime exclusion | Kept `current_facts.py`, `answering.py`, retrieval, answer, calculator, SymPy, live acquisition, and parser/classifier behavior out of scope | This ExecPlan only | Diff/status review | Passed | None | Review pending | Runtime remains legacy raw backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-export-generator.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only and does not implement generator code, generated artifacts,
  runtime lookup, answer behavior, parser/classifier behavior, retrieval,
  calculator, SymPy, or live acquisition.
- Output path contract is `data/current-facts/<run_id>-current-fact-export.json`
  with optional `docs/current-facts/<run_id>-current-fact-export.md`.
- The plan uses `current_fact_export/v2`, top-level
  `calculation_input_status`, and parsed-value-only lookup-ready records.
- The plan identifies the public source-record input gap and does not generate
  production export from group-level coverage alone.
- Legacy `data/exports/<character>/official_raw.json` is excluded as source
  input and from `generated_from`.
- `.local`, raw HTML, screenshots/VLM as authority, private data, and
  SuperCombo numeric authority are excluded as source inputs.
- Fixture-contract generator implementation is allowed only as a future
  implementation slice; production export artifact generation requires a
  reviewed public source-record input artifact first.
- Validators are planned for schema, deterministic ordering, guard behavior,
  authority/source boundary, privacy boundary, no flattened annotated
  candidate, and no collapsed frame_range.

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
