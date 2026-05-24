# Current Fact Lookup Parsed-Value Transition

Status: Drafted for review; validation passed.

## Purpose

Plan the transition from the legacy
`data/exports/<character>/official_raw.json` lookup in `current_facts.py` to a
reviewed parsed-value/current-fact-backed lookup, without changing answer
behavior in this planning PR.

The transition must preserve daily-answer authority boundaries. It must not
make raw, parsed, annotated, or ranged values answerable as exact scalar facts
until a reviewed current-fact export exists, validators pass, and a later
implementation ExecPlan approves the runtime switch.

## Inputs

- `docs/PLAN.md`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `docs/execplans/2026-05-23-frame-range-consumer-guard.md`
- `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard.md`
- `docs/execplans/2026-05-24-annotated-numeric-candidate-consumer-guard-implementation.md`

## Context

`current_facts.py` currently implements a legacy raw lookup:

- `AUTHORITY_DATASET == "official_raw"`;
- `official_raw_path(character_slug)` resolves to
  `data/exports/<character>/official_raw.json`;
- `load_official_raw()` reads a list of raw official export rows;
- `lookup_current_fact(character_slug, move_input, field)` matches the raw
  `input` string and returns a `CurrentFact` whose `value` is the raw field
  value from that file;
- `search_moves()` also scans the same legacy raw export files.

`answering.py` currently uses this lookup for deterministic numeric/current
fact answers:

- it detects numeric/current-fact-like queries;
- it requires `character_slug`, `move_input`, and `field`;
- it calls `lookup_current_fact`;
- on success it returns an answered packet with
  `deterministic_current_fact_lookup` evidence.

This behavior is intentionally simple and raw-export-backed. This plan does
not change it.

## Scope

Included in this docs-only plan:

- identify the existing lookup and answer behavior;
- identify reviewed artifacts that can be inputs to a future parsed-value
  current-fact export;
- define the data/export artifact needed before runtime lookup can switch;
- define how `current_fact_guards.is_scalar_calculation_input` must be used
  by future exact scalar lookup paths;
- keep `annotated_numeric_candidate` and `frame_range` excluded from exact
  scalar answers;
- require authority, source, raw, parsed, and calculation-status fields to be
  carried through any future export;
- require legacy raw export files to remain in place until replacement lookup
  is validated;
- define future implementation slices.

Excluded:

- No runtime behavior change.
- No retrieval implementation.
- No answer behavior change.
- No export implementation.
- No calculator implementation.
- No parser or classifier change.
- No current-fact schema change.
- No generated artifact change.
- No live acquisition.
- No SymPy logic.
- No calculation-safe promotion.
- No numeric authority or current-fact authority promotion.

## Reviewed Input Boundaries

A future parsed-value-backed lookup may use only reviewed public artifacts and
schemas. Candidate inputs include:

- parsed-value classifier coverage, including `classifier_decision`,
  `calculation_input_status`, `parsed_value`, `raw_value`, source identifiers,
  and raw-value variant coverage where present;
- source-review summaries, including note-linkage decisions and blocked
  statuses;
- acquisition reports and hashes as summary evidence that identify which
  acquisition artifacts were used, without exposing raw HTML or full rows;
- current-fact schemas under `contracts/current-facts/`;
- approved consumer guard contracts for `frame_range` and
  `annotated_numeric_candidate`.

These inputs are not enough by themselves to switch runtime lookup. They first
need a reviewed current-fact export artifact that is schema-valid and carries
all fields required for authority and scalar-safety checks.

## Required Export Artifact

Before `current_facts.py` can move away from legacy `official_raw.json`, a
future implementation must create a normalized, reviewed current-fact export.

The expected artifact should be versioned and schema-validated against
`contracts/current-facts/current_fact_export.schema.json`, or a reviewed schema
revision if a blocker is found. It must contain records with at least:

- `record_id`;
- `character_slug`;
- `move_id`;
- `display_label_ja`;
- `field_key`;
- `raw_value`;
- `parsed_value` when a reviewed parsed value exists;
- `value_shape`;
- `source_name`;
- `source_role`;
- `source_family`;
- `source_label`;
- `source_header_path`;
- `authority_status`;
- `evidence`;
- a deterministic way to carry `calculation_input_status`.

`calculation_input_status` is required by the consumer guard, but it is not
currently a top-level required field in `current_fact_record.schema.json`.
Therefore the next export-design implementation must either:

- add a reviewed schema field for `calculation_input_status`; or
- define a reviewed companion policy/index that is joined by `record_id` and
  validated before lookup.

Runtime lookup must not switch until this status-carrier decision is resolved.

Potential artifact path and naming should be fixed in the export design
ExecPlan. A conservative direction is:

- immutable JSON export under a `data/` path;
- optional public Markdown summary under a `docs/` path;
- no `.local` input, raw HTML, full rows, screenshots, cookies, profiles,
  traces, debug dumps, logs, private paths, or private data in Git.

## Lookup Transition Contract

A future parsed-value-backed lookup may replace legacy raw lookup only after a
separate implementation plan proves all of the following:

- the normalized current-fact export is generated from reviewed inputs;
- every record validates against the current-fact export schema and any
  calculation-status carrier contract;
- exact scalar lookup calls
  `current_fact_guards.is_scalar_calculation_input(parsed_value,
  calculation_input_status)` or passes an equivalent validator;
- lookup preserves `raw_value` and source metadata in evidence;
- lookup carries `authority_status`, `source_role`, `source_name`,
  `source_family`, `source_header_path`, and `evidence`;
- lookup distinguishes exact scalar answers from display/search metadata;
- lookup rejects records with no parsed value or blocked statuses in scalar
  answer contexts;
- lookup keeps legacy raw export fallback available until parity and rollback
  criteria are reviewed.

The runtime switch must be a later PR. This plan only defines the conditions.

## Scalar Guard Requirements

Future exact scalar answer, export, retrieval, and calculator paths must treat
`is_scalar_calculation_input` as the minimum guard for parsed values.

The following are not exact scalar answer inputs:

- `parsed_value.kind == "annotated_numeric_candidate"` with
  `calculation_input_status == "annotated_candidate_not_calculation_safe"`;
- `parsed_value.kind == "frame_range"` with
  `calculation_input_status ==
  "parsed_range_not_single_value_calculation_safe"`;
- review-required records with no parsed value;
- `enum_token`, `ordered_pair`, `raw_note`, or any other non-scalar parsed
  shape in scalar contexts;
- any parsed value with `not_numeric_authority`;
- any parsed value lacking an approved scalar calculation status.

Nested numeric content inside `annotated_numeric_candidate` must not be
flattened into `integer`, `signed_frame`, or exact answer text. `frame_range`
endpoints must not be collapsed to a single value, best/worst value, or
representative value without a later range-aware contract.

## Authority And Daily-Answer Boundary

Official records remain `authority_candidate` unless a later authority
promotion ExecPlan explicitly changes that boundary. SuperCombo records remain
enrichment or cross-reference only and must not become numeric authority.

During the transition:

- daily-answer behavior must not broaden authority;
- existing answer behavior must remain unchanged until a later runtime switch
  PR is reviewed;
- parsed values may be used for validation, display/search metadata, and
  planning only unless the scalar guard and authority checks pass;
- exact numeric answers must not use raw classifier output, source-review
  prose, VLM output, or reviewer notes as standalone authority;
- VLM or ChatGPT observations remain `observation_candidate` only when present.

## Legacy Raw Retention Plan

Legacy `data/exports/<character>/official_raw.json` files are technical debt,
not a stable long-term surface. They are retained only because
`current_facts.py` and `answering.py` still depend on them for current
deterministic answers.

Any retained legacy export path must have:

- current dependent code path: `current_facts.py` and the `answering.py`
  deterministic lookup flow;
- replacement requirement: reviewed current-fact export plus scalar guard and
  authority/status validation;
- retirement blocker: replacement lookup parity, evidence format, rollback,
  and daily-answer authority review are not complete;
- intended removal step: remove or demote the legacy raw lookup after the
  replacement export is the reviewed source of truth.

The files must remain retained until a replacement lookup is validated, but
the intended direction is active retirement.

The future retirement sequence should be:

1. Generate a reviewed current-fact export without changing runtime lookup.
2. Add validators that compare key lookup coverage against legacy raw export
   where comparison is safe and meaningful.
3. Add a parsed-value-backed lookup helper behind tests without changing
   `answering.py`.
4. Switch `current_facts.py` or introduce a new lookup entry point only after
   mandatory review confirms answer behavior and authority boundaries.
5. Keep rollback/fallback to legacy raw lookup until parity, error handling,
   and daily-answer evidence format are reviewed.
6. Retire legacy raw lookup only in a later ExecPlan after the replacement is
   the reviewed source of truth.

## Future Implementation Slices

This transition should be split into small PRs:

1. Current-fact export design amendment.
   Decide the exact artifact path, status carrier, schema changes if needed,
   and validator evidence.
2. Export generator implementation.
   Generate a reviewed current-fact export from existing public reviewed
   artifacts, with no runtime answer change.
3. Lookup helper implementation.
   Add a parsed-value-backed lookup helper that reads the new export and uses
   `is_scalar_calculation_input`, with focused tests only.
4. Answer integration plan.
   Plan the evidence packet, user-facing behavior, fallback, and parity checks
   before `answering.py` changes.
5. Runtime switch implementation.
   Switch exact current-fact answers only after mandatory review.
6. Legacy raw lookup retirement plan.
   Remove or demote the legacy lookup only after the replacement is validated
   and rollback criteria are no longer needed.

Parser expansion, calculator implementation, retrieval implementation, and
SymPy arithmetic remain separate plans.

## Acceptance Criteria

- The ExecPlan documents current `current_facts.py` and `answering.py`
  behavior.
- The ExecPlan identifies reviewed artifacts that may feed a future
  current-fact export.
- The ExecPlan defines the need for a normalized reviewed export before
  runtime lookup changes.
- The ExecPlan requires `is_scalar_calculation_input` or equivalent validator
  coverage before exact scalar consumption.
- The ExecPlan keeps `annotated_numeric_candidate` and `frame_range` out of
  exact scalar answer paths.
- The ExecPlan requires authority/source metadata and
  `calculation_input_status` to be carried forward.
- The ExecPlan retains legacy raw exports until replacement lookup is
  validated.
- The ExecPlan prevents daily-answer authority changes during transition.
- No runtime, retrieval, answer, export, calculator, parser, classifier,
  schema, generated artifact, live acquisition, or SymPy changes are made.
- Validation commands pass.

## Files / Interfaces

This docs-only plan changes only:

- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`

Future implementation plans may later touch, after review:

- current-fact export generator code;
- current-fact export artifacts;
- current-fact schemas if the calculation-status carrier requires it;
- focused validators and tests;
- `current_facts.py` lookup helpers;
- `answering.py` only after a separate answer integration plan is approved.

This plan does not authorize those changes.

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-25 JST) Created branch
  `plan/current-fact-lookup-parsed-value-transition`.
- [x] (2026-05-25 JST) Inspected current lookup and answer surfaces:
  `current_facts.py`, `answering.py`, current-fact schemas, existing
  `official_raw.json` export layout, and current-fact guard validator.
- [x] (2026-05-25 JST) Drafted this docs-only transition ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Keep legacy `official_raw.json` lookup unchanged in this planning
  PR.
  Rationale: The replacement export does not exist yet, and daily-answer
  authority must not change during planning.
  Date/Author: 2026-05-25 / Codex

- Decision: Require a normalized reviewed current-fact export before runtime
  lookup can switch.
  Rationale: `current_facts.py` needs a stable deterministic data contract,
  not a direct join over classifier/source-review artifacts at answer time.
  Date/Author: 2026-05-25 / Codex

- Decision: Treat `calculation_input_status` as mandatory for scalar
  consumption.
  Rationale: `parsed_value.kind` alone cannot prove calculation or answer
  safety; the current guard requires both parsed shape and status.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep `annotated_numeric_candidate` and `frame_range` out of exact
  scalar answer paths.
  Rationale: They are parsed but non-scalar-safe until later condition-aware
  or range-aware contracts exist.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: This transition plans lookup/export authority boundaries, not
  arithmetic.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- The current-fact record schema does not currently require a top-level
  `calculation_input_status`; the status-carrier decision must be resolved
  before runtime lookup changes.
- Future export path and stable lookup index naming are not fixed by this
  plan.
- Existing `current_facts.py` still reads legacy raw export data until later
  implementation slices land.
- Future consumers can still bypass guard logic until surface-specific
  validators are added.
- Official remains authority-candidate only; a later authority model is still
  needed before stronger current-fact claims.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only transition plan | Drafted a plan for moving from legacy raw lookup to parsed-value/current-fact-backed lookup without answer behavior change | `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md` | `git diff --check`; `uv lock --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future implementation still required |
| Current behavior inventory | Documented legacy `official_raw.json` lookup and `answering.py` deterministic evidence flow | This ExecPlan only | Diff/status review | Passed | None | Review pending | Legacy raw lookup remains active |
| Guard and authority boundary | Required `is_scalar_calculation_input`, status carry-forward, non-scalar exclusions, and authority/source carry-forward | This ExecPlan only | Diff/status review | Passed | None | Export status-carrier decision unresolved | Future consumers could bypass guards |
| Scope exclusions | Kept runtime/retrieval/answer/export/calculator/parser/classifier/schema/generated artifact/live acquisition/SymPy changes out of scope | This ExecPlan only | Diff/status review | Passed | None | Review pending | None for docs-only PR |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md.

Check:
- PR diff contains exactly one ExecPlan file.
- The plan documents current current_facts.py and answering.py legacy raw
  lookup behavior.
- The plan does not change runtime, retrieval, answer, export, calculator,
  parser, classifier, schema, generated artifacts, live acquisition, or SymPy.
- The plan requires a reviewed normalized current-fact export before runtime
  lookup can switch.
- The plan requires calculation_input_status to be carried forward or a schema
  blocker to be resolved before implementation.
- The plan requires current_fact_guards.is_scalar_calculation_input or an
  equivalent validator before exact scalar consumption.
- annotated_numeric_candidate and frame_range remain excluded from exact
  scalar answers.
- authority_status, source_role, source_name, source metadata, raw_value,
  parsed_value, value_shape, and evidence must be preserved.
- legacy raw export files remain retained until replacement lookup is
  validated.
- daily-answer authority behavior does not change during transition.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations,
remaining risks, and whether docs-only stage/commit is approved.
```
