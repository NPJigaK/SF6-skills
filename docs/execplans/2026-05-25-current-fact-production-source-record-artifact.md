# Current-Fact Production Source-Record Artifact

Status: Drafted for review; validation passed.

## Purpose

Plan the reviewed public input boundary required before producing a
production current-fact source-record artifact.

The repository now has:

- `current_fact_source_record_input/v1` schema and synthetic contract fixtures;
- an in-memory fixture-contract export generator;
- `current_fact_export/v2` schema with top-level `calculation_input_status`;
- guard helpers that reject non-scalar parsed values in scalar contexts.

The remaining production blocker is not generator behavior. It is source input:
the repository still lacks a reviewed public row/move/cell-level input that can
produce source records without falling back to legacy raw exports, ignored
`.local` rows, raw HTML, screenshots, or VLM observations as authority.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `docs/execplans/2026-05-25-current-fact-export-generator.md`
- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`
- `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

## Context

PR #359 proved that a `current_fact_source_record_input/v1` payload can be
converted deterministically into a `current_fact_export/v2` payload without
leaking source-record sidecar fields or flattening non-scalar parsed values.
That PR intentionally used synthetic fixtures only.

Current public artifacts are still insufficient for production source-record
generation:

- parsed-value classifier coverage is grouped by value shape and raw variant;
- source-review summaries contain reviewed note/linkage outcomes but not full
  lookup-ready row/move/cell records;
- acquisition reports contain summary hashes and counts, not public row
  payloads;
- legacy `data/exports/<character>/official_raw.json` is technical debt and
  must not become the source input for the replacement artifact.

Therefore the next safe step is a docs-only plan that fixes what reviewed
public input must exist before any production
`data/current-facts/source-records/<run_id>-current-fact-source-records.json`
artifact can be generated.

## Scope

Included in this docs-only plan:

- define the reviewed public input boundary for production source-record
  generation;
- decide that group-level classifier coverage alone is not enough;
- decide that legacy raw exports are not valid source inputs;
- define source-record candidate review requirements for row/move/cell
  identity;
- define how parsed-value coverage, source reviews, acquisition report
  hashes/counts, and schemas can be cross-checked;
- define production source-record artifact generation prerequisites;
- define validators required before committing any production source-record
  artifact;
- preserve Issue #343 screenshot plus ChatGPT/VLM double-check gating for any
  new value semantics decision.

Excluded:

- No production source-record artifact generation.
- No production current-fact export artifact generation.
- No generator code changes.
- No file-writing wrapper.
- No runtime lookup change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier expansion.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No source acquisition implementation.
- No live acquisition.
- No authority promotion.

## Reviewed Public Input Decision

The first production source-record artifact must be built from a reviewed
public source-record input, not directly from legacy or ignored source rows.

Allowed committed public inputs:

- parsed-value classifier coverage for approved parser rule IDs, value-shape
  decisions, raw-value variant status, and `calculation_input_status`;
- official source-review summaries for reviewed note/linkage decisions and
  blocked status;
- acquisition reports for run identity, source-family counts, artifact hashes,
  and public acquisition boundary metadata;
- current-fact schemas and validators;
- current-fact guard contracts;
- a future reviewed source-record candidate summary artifact that lists
  row/move/cell identity and exact raw values without publishing raw HTML or
  full rows.

Excluded as source inputs or authority:

- `data/exports/<character>/official_raw.json`;
- `.local` raw row artifacts;
- raw HTML;
- full raw rows;
- screenshots as authority;
- ChatGPT/VLM observations as authority;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, or private
  data;
- local absolute paths;
- SuperCombo numeric authority.

Ignored `.local` artifacts may be used only as reviewer input in a separately
approved source-review or acquisition-update workflow. They must not appear in
the public production source-record artifact, `generated_from`, evidence
paths, or public Markdown summaries.

## Source-Record Candidate Review Requirement

Before committing a production source-record artifact, the repository needs a
reviewed public candidate input that carries row/move/cell identity.

The candidate input may be a summary-safe data artifact under `data/` with a
matching Markdown summary under `docs/`, or an explicitly reviewed extension
of an existing source-review artifact. It must provide enough information to
construct each `current_fact_source_record_input/v1` record while keeping
private and raw-source material out of Git.

For each candidate record, the reviewed public input must include:

- `character_slug`;
- stable `move_id`;
- `display_label_ja`;
- `field_key`;
- source-native `source_header_path`;
- exact `raw_value`;
- `raw_value_length`;
- `raw_value_sha256`;
- source row/cell/value keys that do not embed full raw row payloads;
- public evidence path;
- reviewed source name, role, family, and label;
- authority status;
- parser rule ID or blocked reason from coverage/source review;
- `calculation_input_status`;
- parsed value only when the record is lookup-ready.

The candidate input must not include:

- raw HTML;
- full source rows;
- screenshots;
- local filesystem paths;
- browser profiles, cookies, headers, tokens, traces, debug dumps, or logs;
- ChatGPT/VLM full output;
- private user data.

## Admission Rules

Production source-record artifacts remain lookup-ready and parsed-value-only.

Allowed records:

- records with a reviewed `parsed_value`;
- records whose `calculation_input_status` is one of the closed current-fact
  statuses allowed by the source-record schema;
- records whose official source role remains `authority_candidate`;
- records whose SuperCombo source role remains enrichment or cross-reference
  only and never scalar numeric authority;
- records that preserve `annotated_numeric_candidate` as a wrapper;
- records that preserve `frame_range` as a range.

Excluded records:

- `review_required_not_calculation_safe`;
- `out_of_scope_not_emitted`;
- records with no `parsed_value`;
- records sourced from legacy `data/exports/*`;
- records whose row/move/cell identity cannot be linked to reviewed public
  evidence;
- same-grammar raw-value variants not covered by the Issue #343 double-check
  gate when a new value-handling decision is introduced.

Blocked and review-required values remain in classifier and source-review
artifacts until they have their own reviewed parser/source-review plan. They
must not be inserted into lookup-ready source-record artifacts as placeholders.

## Cross-Checks

Future source-record artifact generation must cross-check each output record
against the reviewed public inputs:

- `raw_value_length` and `raw_value_sha256` match exact `raw_value`;
- `source_header_path` matches the reviewed source column path;
- parser rule IDs and `parsed_value.kind` match classifier coverage;
- `calculation_input_status` matches coverage and guard expectations;
- official records remain `authority_candidate`;
- SuperCombo records never become scalar numeric authority;
- `annotated_numeric_candidate` is not flattened to `integer` or
  `signed_frame`;
- `frame_range` is not collapsed to a single frame;
- evidence paths are public committed artifacts only;
- `generated_from` does not include legacy raw export paths, `.local`, raw
  HTML, screenshots, VLM output, or private paths.

## Issue #343 Gate

Issue #343 remains the value-semantics double-check gate.

When a future production source-record artifact introduces a new
value-handling decision, the implementation must first create a sanitized
reviewer bundle under:

- `.local/reviewer-evidence/value-double-check/<run-id>/`

The bundle may contain screenshots, a manifest, a target value summary, and a
ChatGPT/VLM prompt. Human upload remains manual. The output is
`observation_candidate` only.

Any mismatch, uncertainty, unreadable target, or unreviewed same-grammar
variant blocks the production source-record artifact until the reviewed public
source decision is updated.

The bundle, zip, screenshots, raw HTML, full rows, local paths, and ChatGPT
full output must not be committed.

## Future Implementation Slices

This plan intentionally does not authorize production artifact generation.

The next implementation should be chosen from one of these separately reviewed
paths:

1. Source-record candidate review artifact:
   Create a summary-safe public candidate artifact that maps reviewed parsed
   values to row/move/cell identity without using legacy raw exports as the
   source input.

2. Acquisition/source-review amendment:
   If current public artifacts are still insufficient, add a docs-only plan
   for the specific acquisition or source-review fields needed to expose
   summary-safe row/move/cell identity.

3. Production source-record artifact generation:
   Only after the reviewed public candidate input exists, generate
   `data/current-facts/source-records/<run_id>-current-fact-source-records.json`
   and validate it against `current_fact_source_record_input/v1`.

4. Production export generation:
   Only after a production source-record artifact is reviewed, use the
   fixture-contract generator path to produce a production
   `current_fact_export/v2` artifact.

5. Runtime lookup transition:
   Only after production export parity and rollback criteria are reviewed,
   plan the runtime lookup switch away from legacy raw exports.

## Acceptance Criteria

- The plan is docs-only.
- The plan does not authorize production source-record or export artifact
  generation.
- The plan identifies the reviewed public input blocker before production
  source-record generation.
- The plan rejects legacy raw exports as source input.
- The plan keeps `.local`, raw HTML, screenshots, VLM output, local paths, and
  private data out of public artifacts.
- The plan preserves parsed-value-only admission for lookup-ready
  source-record artifacts.
- The plan keeps blocked/review-required records out of lookup-ready
  production source-record artifacts.
- The plan preserves `annotated_numeric_candidate` and `frame_range` consumer
  guard boundaries.
- The plan does not change runtime, parser/classifier, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition behavior.

## Files / Interfaces

This docs-only PR should change only:

- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`

Future implementation plans may touch additional files only after mandatory
review approval.

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

- 2026-05-25: Drafted docs-only plan after PR #359 merged. No implementation
  or generated artifact changes included.
- 2026-05-25: Ran validation commands. They passed with only this new
  ExecPlan file untracked.

## Decision Log

- 2026-05-25: Production source-record generation remains blocked until a
  reviewed public row/move/cell input exists.
- 2026-05-25: Legacy `data/exports/<character>/official_raw.json` is rejected
  as source input for the replacement source-record artifact.
- 2026-05-25: Group-level classifier coverage can cross-check parsed-value
  decisions but cannot by itself create production row/move/cell records.
- 2026-05-25: `.local` artifacts and screenshots may support reviewer work
  only under approved workflows; they are not public artifact authority.

## Deviations

- None.

## Risks

- Production source-record artifact generation is still blocked by the lack of
  reviewed public row/move/cell candidate input.
- Current public artifacts may require an acquisition/source-review amendment
  before source-record candidates can be created.
- Runtime remains legacy raw export backed.
- Existing fixture-contract generator tests prove contract behavior, not
  source truth.
- First production coverage may be limited because lookup-ready records require
  parsed values and reviewed row/move/cell identity.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only production source-record input plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md` | `git diff --check` | Pass | None | Mandatory review pending | Source-record production remains blocked |
| Runtime and artifact boundary | No runtime or production artifact changes | Same | `git status --short --branch` | Pass; one untracked ExecPlan file only | None | Mandatory review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only.
- It does not authorize production source-record artifact generation yet.
- It fixes the reviewed public input blocker before production source-record generation.
- It rejects legacy data/exports/* official_raw.json as source input.
- It keeps .local, raw HTML, full rows, screenshots/VLM as authority, local paths, cookies, profiles, traces, debug dumps, logs, and private data out of public artifacts.
- It states group-level classifier coverage is cross-check input only, not enough to generate row/move/cell production records.
- It keeps lookup-ready source records parsed-value-only.
- It keeps review_required/no parsed_value records out of lookup-ready source-record artifacts.
- It preserves annotated_numeric_candidate and frame_range non-scalar guard boundaries.
- Issue #343 double-check gate remains required for new value-handling decisions.
- No generator code, generated artifacts, runtime lookup, current_facts.py, answering.py, parser/classifier behavior, retrieval, answer, calculator, SymPy, source acquisition, or live acquisition changes are included.

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
