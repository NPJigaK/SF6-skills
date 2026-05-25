# Current-Fact Candidate Evidence Amendment

Status: Drafted for review; validation passed.

## Purpose

Define the source-review/acquisition amendment needed to expose public,
committed, summary-safe row/move/cell candidate evidence.

PR #364 concluded that existing public summaries are insufficient to populate
production `current_fact_row_move_cell_candidate_input/v1` records. This plan
defines what evidence a future amendment must emit from existing ignored v4
official artifacts or from a derived acquisition/source-review summary before
any production candidate artifact generation can start.

This is a docs-only planning step. It does not implement the amendment and
does not generate candidate, source-record, or current-fact export artifacts.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-candidate-public-artifact-source-review.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md`
- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`
- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

The repository now has:

- a candidate input schema and synthetic contract fixtures;
- source-record schema and fixture-contract export generator support;
- consumer guards for non-scalar parsed values;
- public classifier, source-review, acquisition, and validator audit summaries.

Those artifacts still do not provide a committed public mapping from a parsed
raw value to a specific character, move, source row, source cell, and value
slot. The ignored `official_table_rows_raw/v4` artifacts may contain enough
structure for a reviewer to derive that mapping, but ignored artifacts are not
public authority. A summary-safe public artifact is needed before production
candidate records can be populated.

## Scope

Included in this docs-only plan:

- define exact row/move/cell candidate evidence fields required for a future
  public amendment artifact;
- decide where the amendment should live;
- define privacy and source-boundary rules;
- define how future amendment output cross-checks classifier, source-review,
  acquisition, schema, and validator audit artifacts;
- define admission requirements for candidate-generation readiness;
- preserve Issue #343 double-check gate for any new value-handling decision;
- keep production candidate/source-record/export generation blocked.

Excluded:

- No amendment implementation.
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

## Amendment Placement Decision

The next implementation should create a new summary-safe public source-review
artifact, supported by acquisition-derived structural fields where needed.

Recommended future artifact family:

- JSON: `data/source-reviews/<run_id>-current-fact-row-move-cell-candidate-evidence.json`
- Markdown: `docs/source-reviews/<run_id>-current-fact-row-move-cell-candidate-evidence.md`
- Optional future schema:
  `contracts/source-reviews/current_fact_candidate_evidence.schema.json`
- Planned artifact schema version:
  `current_fact_candidate_evidence/v1`

Rationale:

- This output is reviewer evidence, not the production candidate input itself.
- It may be derived from ignored v4 acquisition artifacts, but the committed
  output must be summary-safe and reviewer-approved.
- It belongs closer to source review than to the acquisition report because it
  records reviewed candidate identity evidence and source-boundary decisions.
- Acquisition may need a later implementation amendment only if existing v4
  fields cannot deterministically expose the required row/cell/value keys
  without publishing full rows.

Candidate artifact generation must wait until this evidence artifact is
reviewed and validated.

## Required Evidence Fields

The amendment must emit enough public evidence to populate every required
`current_fact_row_move_cell_candidate_input/v1` record field later.

Required candidate identity evidence:

- `character_slug`;
- `move_id`;
- `display_label_ja`;
- `field_key`;
- `source_row_key`;
- `source_cell_key`;
- `source_value_key`;
- `source_row_order`;
- `source_cell_order`;
- `source_header_path`;
- `source_label`;
- `raw_value`;
- `raw_value_length`;
- `raw_value_sha256`.

Required source and review linkage:

- `source_name`;
- `source_role`;
- `source_family`;
- `authority_status`;
- `parser_rule_ids`;
- `calculation_input_status`;
- classifier coverage reference IDs;
- source-review reference IDs;
- acquisition report references;
- source artifact run ID and public hash references;
- evidence status for each candidate row/cell/value binding.

Required parsed-value linkage:

- candidate `parsed_value` payload or a deterministic public reference to the
  reviewed parsed payload that the future candidate artifact can reproduce;
- `value_shape` metadata needed by the candidate schema;
- explicit confirmation that blocked/review-required records remain excluded
  from lookup-ready candidate records.

The amendment must not emit full raw rows. Any public snippet must be the
minimal value/header/identity excerpt required to verify the candidate
binding.

## Evidence Record Boundary

The future evidence records should be source-review records, not final
candidate records.

Each evidence record should carry:

- stable evidence ID;
- run ID;
- candidate identity fields listed above;
- minimal raw value fields listed above;
- reviewed public source/header references;
- source-review status such as `candidate_identity_evidence_found`,
  `candidate_identity_evidence_ambiguous`, or
  `candidate_identity_evidence_missing`;
- blocker reason when ambiguous or missing;
- references to classifier coverage, source-review summaries, and acquisition
  report hashes;
- explicit non-authority statements for reviewer-only observations.

The evidence artifact may include records that remain blocked, but the later
`current_fact_row_move_cell_candidate_input/v1` artifact may admit only
lookup-ready records with `parsed_value`. Blocked evidence records must remain
in source-review evidence and must not be promoted into candidate input.

## Public Source Inputs

Allowed public inputs for the amendment:

- parsed-value classifier coverage and policy artifacts;
- official note-linkage source-review summaries;
- acquisition reports for run metadata, schema version, counts, and hashes;
- current-fact schemas and validators;
- validator audit artifacts;
- reviewed public Markdown summaries;
- future reviewed source-review evidence summaries.

Allowed reviewer input, if explicitly approved by the future implementation
ExecPlan:

- ignored v4 acquisition artifacts as local reviewer input;
- sanitized local reviewer bundles under approved `.local` paths;
- Scrapling screenshots as reviewer-only observation material.

Reviewer input must be converted into summary-safe public evidence before it
can support production candidate generation.

## Forbidden Inputs And Published Content

The amendment must not use or publish:

- legacy `data/exports/*/official_raw.json` as replacement source input;
- `.local` paths or payloads;
- raw HTML;
- full raw rows;
- screenshots as authority;
- ChatGPT/VLM observations as authority;
- ChatGPT/VLM full output;
- local absolute paths;
- cookies;
- browser profiles;
- request/response headers;
- tokens;
- traces;
- debug dumps;
- logs;
- answer logs;
- training logs;
- private data;
- SuperCombo numeric authority.

Screenshots and ChatGPT/VLM output remain `observation_candidate` only. They
may guide reviewer attention but cannot prove source truth, validator
evidence, parser/schema approval, calculation safety, or authority.

## Candidate Readiness Checks

The future amendment must let reviewers answer these questions before
candidate artifact generation:

- Does each candidate raw value have a public character and move identity?
- Does each candidate raw value have stable row/cell/value keys and order?
- Does the public raw value length and hash match the reviewed source binding?
- Does the source header path match the intended `field_key`?
- Does the candidate link to the expected classifier coverage and
  source-review IDs?
- Is the candidate parsed-value-only and not review-required?
- Are `annotated_numeric_candidate` and `frame_range` preserved as non-scalar
  values?
- Are official records still `authority_candidate`?
- Is SuperCombo still enrichment/cross-reference only?
- Are ambiguous or missing bindings blocked outside the candidate artifact?
- Are all public references committed artifacts rather than ignored local
  evidence?

If any answer is missing or ambiguous, production candidate artifact
generation remains blocked.

## Issue #343 Double-Check Gate

Issue #343 remains mandatory for any new value-handling decision.

The future amendment does not by itself authorize new parsing, new parsed raw
variants, same-grammar expansion, calculation-safe promotion, or authority
promotion.

If the amendment introduces new raw-value semantics, newly included raw
variants, or same-grammar expansion, the implementation must first create a
sanitized reviewer bundle under:

- `.local/reviewer-evidence/value-double-check/<run-id>/`

Human upload remains manual. ChatGPT/VLM output is
`observation_candidate` only. It is not source truth, validator evidence,
parser/schema approval, calculation-safe promotion, or numeric authority.

The bundle, zip, screenshots, raw HTML, full rows, local paths, and ChatGPT
full output must not be committed.

## Future Validation Plan

A future implementation PR for the amendment should add focused validation
that checks:

- public artifact schema and required field coverage;
- summary-safe public paths only;
- no legacy raw export source input;
- no `.local`, raw HTML, full rows, screenshots, local paths, logs, or private
  data in committed artifacts;
- raw value length and hash consistency;
- row/cell/value key format and deterministic uniqueness;
- source header path and field key consistency;
- coverage/source-review/acquisition reference consistency;
- blocked/ambiguous evidence cannot enter lookup-ready candidate input;
- non-scalar parsed values are not flattened;
- SuperCombo numeric authority is rejected.

Validators must be evidence-first and grounded in public artifacts, approved
contract fixtures, or privacy/source-boundary rules.

## Future Implementation Slices

Recommended next PR:

1. Docs-only implementation ExecPlan for the candidate evidence source-review
   artifact.

Blocked until that plan is approved:

2. Candidate evidence source-review artifact implementation.
3. Production `current_fact_row_move_cell_candidate_input/v1` generation.
4. Production source-record artifact generation.
5. Production current-fact export generation.
6. Runtime lookup transition and legacy raw export retirement.

## Acceptance Criteria

- The plan is docs-only.
- The plan defines exact candidate evidence fields needed for future
  production candidate records.
- The plan decides that the evidence should be emitted as a summary-safe
  public source-review artifact, with acquisition amendment only if existing
  v4 fields are insufficient.
- The plan preserves privacy and source-boundary rules.
- The plan keeps Issue #343 double-check gate mandatory.
- The plan keeps production candidate/source-record/export generation blocked.
- The plan does not change runtime lookup, `current_facts.py`, `answering.py`,
  parser/classifier behavior, retrieval, answer, calculator, SymPy, source
  acquisition, or live acquisition.
- The plan does not use legacy `data/exports/*/official_raw.json`, `.local`,
  raw HTML, screenshots, VLM output, or private data as authority.

## Files / Interfaces

This docs-only PR should change only:

- `docs/execplans/2026-05-25-current-fact-candidate-evidence-amendment.md`

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

- 2026-05-25: Drafted docs-only source-review/acquisition amendment plan after
  PR #364 merged. No implementation or generated artifact changes included.
- 2026-05-25: Ran validation commands for docs-only plan. All checks passed.

## Decision Log

- 2026-05-25: The next evidence surface should be a summary-safe public
  source-review artifact, not the production candidate input itself.
- 2026-05-25: Acquisition amendment is deferred unless existing ignored v4
  fields cannot deterministically provide row/cell/value keys for a
  summary-safe public source-review artifact.
- 2026-05-25: Production candidate artifact generation remains blocked until
  public evidence proves row/move/cell identity for each included record.
- 2026-05-25: Legacy raw exports remain rejected as replacement source input.
- 2026-05-25: Validation passed without adding implementation, schemas,
  fixtures, validators, or generated artifacts.

## Deviations

- None.

## Risks

- Existing ignored v4 artifacts may not contain enough deterministic
  row/cell/value structure to derive summary-safe candidate evidence.
- The future source-review artifact may require an acquisition amendment
  before it can be implemented.
- Production candidate/source-record/export artifacts remain blocked.
- Runtime remains legacy raw export backed.
- First production candidate coverage may be limited by parsed-value-only
  admission and public identity evidence requirements.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Evidence field plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-candidate-evidence-amendment.md` | `git diff --check`; `uv lock --check` | Pass | None | Mandatory review pending | Future implementation may need acquisition amendment |
| Amendment placement decision | Draft plan chooses summary-safe public source-review artifact | Same | `validate_current_fact_row_move_cell_candidates.py`; `parsed_value_classifier validate` | Pass | None | Mandatory review pending | Production candidate artifact remains blocked |
| Runtime and artifact boundary | No runtime or generated artifact changes | Same | current-fact validators; `validate_clean_slate.py` | Pass | None | Mandatory review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-candidate-evidence-amendment.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only.
- It defines exact candidate evidence fields:
  - character_slug
  - move_id
  - display_label_ja
  - source_row_key / source_cell_key / source_value_key
  - source_row_order / source_cell_order
  - source_header_path / source_label
  - raw_value / raw_value_length / raw_value_sha256
  - parser/source-review/coverage/acquisition refs
- It decides whether the evidence belongs in acquisition amendment,
  source-review amendment, or a new summary-safe public source-review artifact.
- It preserves privacy/source-boundary rules:
  - no raw HTML
  - no full rows
  - no .local paths
  - no screenshots/VLM output as authority
  - no cookies/profiles/traces/logs/private data
  - no legacy data/exports/*/official_raw.json as replacement source input
- It keeps Issue #343 double-check gate mandatory for future value-handling
  decisions.
- It keeps production candidate/source-record/export generation blocked.
- It does not implement the amendment.
- It does not change runtime lookup, current_facts.py, answering.py,
  parser/classifier behavior, retrieval, answer, calculator, SymPy, source
  acquisition, or live acquisition.

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

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether docs-only stage/commit is approved.
```
