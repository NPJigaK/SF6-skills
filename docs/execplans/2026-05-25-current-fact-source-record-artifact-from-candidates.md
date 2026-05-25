# Current-Fact Source-Record Artifact From Candidates

Status: Implementation complete; validation passed; mandatory review pending.

## Purpose

Plan generation of the first production
`current_fact_source_record_input/v1` artifact from the reviewed production
row/move/cell candidate artifact added by PR #366.

This plan is the next step after the candidate artifact. It must not jump to
`current_fact_export/v2` generation, runtime lookup, answer behavior, or
legacy raw export retirement. It only defines how to transform the reviewed
candidate input into a source-record input artifact that can later feed the
already-reviewed fixture-contract export generator path.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`
- `docs/execplans/2026-05-25-current-fact-production-source-record-artifact.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`
- `docs/execplans/2026-05-25-current-fact-production-candidate-artifact.md`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/source_reference.schema.json`
- `src/sf6_knowledge_coach/current_fact_candidate_generator.py`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json`
- `docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md`
- `data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

PR #366 produced one schema-valid production candidate artifact:

- `data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json`;
- `docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md`.

It contains exactly 13 reviewed official records from PR #365 evidence:

- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`.

Those records have reviewed row/move/cell identity and parsed values, but they
are candidate input records, not source-record input records. The next safe
step is to generate a production `current_fact_source_record_input/v1`
artifact from that candidate artifact while preserving non-scalar, authority,
privacy, and source-boundary contracts.

## Scope

Included in this docs-only plan and future implementation slice:

- generate one production `current_fact_source_record_input/v1` JSON artifact
  from the PR #366 production candidate artifact;
- generate one summary-safe Markdown companion;
- add a deterministic in-memory source-record generator/helper if needed;
- add focused unit tests for the helper if added;
- update `validate_current_fact_source_records.py` to validate the approved
  production source-record artifact;
- update `validate_current_fact_export_generator.py` only to stop treating the
  approved source-record artifact as a forbidden current-fact export artifact;
- update validator audit artifacts for changed tests/validators;
- update this ExecPlan Progress, Decision Log, and Completion Review Table.

Excluded:

- No production current-fact export artifact generation.
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
- No calculation-safe promotion.
- No Issue #343 raw-value expansion.
- No legacy raw export retirement.

## Artifact Paths

Planned production source-record JSON:

- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`

Planned summary Markdown:

- `docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md`

The source-record artifact top-level `run_id` should be `20260525T000000Z`,
matching the already schema-valid candidate artifact run ID. This keeps the
candidate-to-source-record transformation in one reviewed artifact lineage. PR
#365's date-only evidence identifier `20260525` remains a referenced
source-review artifact identity only; it must not become a source-record
artifact `run_id`.

## Allowed Source Inputs

Allowed implementation inputs:

- `data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json`;
- `docs/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.md`;
- `contracts/current-facts/current_fact_source_record_input.schema.json`;
- current-fact schemas and guard helpers;
- public reviewed artifacts already carried by the candidate artifact.

The implementation must not rebuild facts from lower-level raw source
materials. Candidate records are the reviewed public input boundary for this
slice.

Forbidden implementation inputs:

- legacy `data/exports/*/official_raw.json`;
- ignored `.local` artifacts;
- raw HTML;
- full rows;
- screenshots as authority;
- ChatGPT/VLM output as authority;
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

## Source-Record Mapping

For each production candidate record, the source-record generator or artifact
builder must create one source-record object.

Top-level source-record artifact fields:

- `artifact_schema_version == "current_fact_source_record_input/v1"`;
- `run_id == "20260525T000000Z"`;
- `generated_from` includes the PR #366 candidate JSON and summary;
- `authority_boundary` is copied from the candidate artifact;
- `source_record_boundary` preserves parsed-value-only, legacy/raw/local
  exclusion, reviewer-observation, and SuperCombo enrichment boundaries;
- `records` contains exactly 13 source-record objects.

For each record:

- set `source_record_id` deterministically from `candidate_record_id`, for
  example by replacing the `candidate:` prefix with `source-record:`;
- copy source-record sidecar fields:
  - `source_row_key`;
  - `source_cell_key`;
  - `source_value_key`;
  - `source_row_order`;
  - `source_cell_order`;
  - `source_header_path`;
  - `raw_value_length`;
  - `raw_value_sha256`;
- create `current_fact_record` with:
  - `record_id` deterministically derived from the candidate identity, for
    example by replacing the `candidate:` prefix with `current-fact:`;
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

The source-record generator must not add facts, infer missing source context,
or reinterpret raw values. It is a deterministic shape transformation from
candidate records into source-record records.

## Admission Rules

The first production source-record artifact must contain exactly the 13 records
from the PR #366 production candidate artifact.

Allowed records:

- records present in the PR #366 candidate artifact;
- records with `parsed_value`;
- records with top-level `calculation_input_status`;
- official records with `source_role == "authority_candidate"` and
  `authority_status == "authority_candidate"`;
- records whose `calculation_input_status` is either
  `annotated_candidate_not_calculation_safe` or
  `parsed_range_not_single_value_calculation_safe`;
- records preserving `annotated_numeric_candidate` as a wrapper;
- records preserving `frame_range` as a range.

Forbidden records:

- any value not present in the PR #366 candidate artifact;
- review-required or blocked raw variants;
- records with no `parsed_value`;
- records sourced from legacy raw exports;
- SuperCombo scalar numeric authority;
- any raw-value expansion or changed semantics without the Issue #343 gate.

This artifact is source-record-ready, not scalar-calculation-ready. Exact scalar
answer paths and calculators must still reject the 13 non-scalar records
through `current_fact_guards`.

## Validator Changes

Required validator behavior:

- `validate_current_fact_source_records.py` must validate:
  - synthetic fixture contracts still pass;
  - production source-record path contains only the approved JSON;
  - Markdown summary path contains only the approved summary;
  - production artifact is schema-valid;
  - production artifact has exactly 13 records;
  - all records come from the PR #366 candidate artifact;
  - raw hashes and lengths match;
  - source-record IDs, row/cell/value keys, and current-fact record IDs are
    stable and unique;
  - `current_fact_record` payloads validate against the current-fact record
    schema;
  - `annotated_numeric_candidate` remains wrapped;
  - `frame_range` remains a range;
  - non-scalar statuses are not scalar calculation inputs;
  - no legacy raw exports, local paths, raw HTML, full rows, screenshots, VLM
    output, or private data are referenced.
- `validate_current_fact_export_generator.py` must continue rejecting
  production current-fact export artifacts, but must not reject the approved
  source-record input artifact.
- `validate_current_fact_row_move_cell_candidates.py` must continue validating
  the approved candidate artifact and its `candidate-inputs/` boundary. It may
  be narrowly updated to allow the approved source-record artifact to coexist
  under `data/current-facts/source-records/` and
  `docs/current-facts/source-records/`; source-record artifact semantics remain
  the responsibility of `validate_current_fact_source_records.py`.
- `validate_validator_test_audit.py` must cover any new or modified
  test/validator boundaries.

## Issue #343 Gate

Issue #343 remains mandatory for any future value-handling decision.

This implementation must not add raw values beyond the 13 PR #366 candidate
records. Because the implementation only transforms already-reviewed candidate
records into source-record records, no new screenshot/ChatGPT/VLM double-check
is required.

If implementation attempts to include any additional raw value, same-grammar
expansion, or changed semantics, it must stop and complete the Issue #343
double-check gate first.

## Acceptance Criteria

- PR begins as docs-only and remains draft after plan review.
- After mandatory plan review, implementation commits may be added to this
  same draft PR if the reviewer approves that flow.
- Production source-record artifact is generated only from PR #366 production
  candidate artifact.
- Production source-record artifact top-level `run_id` is `20260525T000000Z`.
- Production source-record artifact has exactly 13 records.
- No production current-fact export artifact is generated.
- No runtime lookup, parser/classifier behavior, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition changes are made.
- Legacy raw exports and private/local evidence are not used as replacement
  source input.
- `annotated_numeric_candidate` and `frame_range` remain non-scalar.
- Official records remain `authority_candidate`.
- Issue #343 gate remains required for future raw-value expansion.

## Files / Interfaces

Plan-only initial PR should change only:

- `docs/execplans/2026-05-25-current-fact-source-record-artifact-from-candidates.md`

Future implementation commits in the same draft PR may change only:

- `docs/execplans/2026-05-25-current-fact-source-record-artifact-from-candidates.md`
- `src/sf6_knowledge_coach/current_fact_source_record_generator.py` if helper
  is needed
- `tests/test_current_fact_source_record_generator.py` if helper is added
- `tests/validation/validate_current_fact_source_records.py`
- `tests/validation/validate_current_fact_export_generator.py` if needed
- `tests/validation/validate_current_fact_row_move_cell_candidates.py` only
  for approved source-record artifact coexistence compatibility
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- `docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md`
- validator audit JSON/MD if tests or validators change

Any additional file requires ExecPlan amendment and mandatory review before
implementation continues.

## Validation Commands

Plan-only validation:

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

Implementation validation:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- 2026-05-25: Drafted plan after PR #366 merged. No implementation or
  production source-record artifact generated yet.
- 2026-05-25: Ran plan-only validation. All checks passed.
- 2026-05-26: During local implementation, full validation exposed that
  `validate_current_fact_row_move_cell_candidates.py` treats the new approved
  source-record artifacts as unexpected production artifacts. That validator
  was not in this plan's approved implementation file list, so implementation
  was paused.
- 2026-05-26: Amended the plan to allow a narrow
  `validate_current_fact_row_move_cell_candidates.py` compatibility update.
  The candidate validator's responsibility remains candidate artifact
  validation; source-record artifact validation remains in
  `validate_current_fact_source_records.py`.
- 2026-05-26: Implemented the deterministic source-record generator helper,
  focused unit tests, production source-record JSON/Markdown artifacts, source
  record validator checks, export-generator coexistence guard, candidate
  validator coexistence compatibility, and validator audit updates.
- 2026-05-26: Ran implementation validation. All checks passed.

## Decision Log

- 2026-05-25: The production source-record artifact will use the PR #366
  candidate artifact as the input boundary.
- 2026-05-25: The first production source-record artifact is limited to the 13
  candidate records already reviewed in PR #366.
- 2026-05-25: Current-fact export generation and runtime lookup transition
  remain out of scope.
- 2026-05-25: Source-record `run_id` will use the schema-valid candidate run
  ID `20260525T000000Z`; PR #365's `20260525` remains only a source-review
  evidence reference.
- 2026-05-26: Source-record IDs and current-fact record IDs are derived by
  replacing the candidate prefix with `source-record:` and `current-fact:`;
  no source facts or value semantics are inferred.
- 2026-05-26: The committed production source-record JSON must match the
  deterministic generator output from the PR #366 candidate artifact.
- 2026-05-26: `validate_current_fact_export_generator.py` may allow the
  approved candidate/source-record input artifacts under `data/current-facts`
  and `docs/current-facts`, but still rejects production current-fact export
  artifacts.
- 2026-05-26: `validate_current_fact_row_move_cell_candidates.py` also needs a
  narrow compatibility update to continue validating candidate artifacts while
  allowing the approved source-record artifacts. This file was not listed in
  the approved implementation file set and therefore requires amendment before
  editing.
- 2026-05-26: The candidate validator coexistence update is limited to scanning
  `data/current-facts/candidate-inputs/` and
  `docs/current-facts/candidate-inputs/` for approved candidate artifacts.
  Source-record artifact validation remains exclusively in
  `validate_current_fact_source_records.py`.

## Deviations

- None.

## Risks

- Production current-fact export artifact remains blocked.
- Runtime remains legacy raw export backed.
- The first production source-record artifact contains only non-scalar parsed
  values and is not calculation-safe.
- Source-record generation may reveal that candidate-to-source-record ID
  derivation needs review; if so, implementation must stop and amend this
  ExecPlan.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Production source-record artifact plan | Implementation progress, decisions, and review prompt updated | `docs/execplans/2026-05-25-current-fact-source-record-artifact-from-candidates.md` | `git diff --check`; `uv lock --check` | Pass | None | None | Runtime remains legacy raw export backed |
| Deterministic source-record helper | Candidate artifact to source-record artifact shape transform only | `src/sf6_knowledge_coach/current_fact_source_record_generator.py`; `tests/test_current_fact_source_record_generator.py` | `python -m unittest discover -s tests` | Pass | None | None | Helper does not prove source truth |
| Production source-record artifact | 13 source records generated from PR #366 candidate artifact | `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`; `docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md` | `validate_current_fact_source_records.py` | Pass | None | None | All 13 records remain non-scalar and not calculation-safe |
| Candidate validator compatibility | Candidate validator scans candidate-inputs directories only; source-record semantics remain elsewhere | `tests/validation/validate_current_fact_row_move_cell_candidates.py` | `validate_current_fact_row_move_cell_candidates.py` | Pass | None | None | Candidate validator must not validate source-record semantics |
| Runtime/export boundary | Export-generator validator allows approved input artifacts but no current-fact export artifact | `tests/validation/validate_current_fact_export_generator.py` | `validate_current_fact_export_generator.py` | Pass | None | None | Production current-fact export remains blocked |
| Validator audit | Audit records new helper test and updated validator evidence boundaries | `data/validator-audits/20260523-validator-test-fact-source-audit.json`; `docs/validator-audits/20260523-validator-test-fact-source-audit.md` | `validate_validator_test_audit.py` | Pass | None | None | Audit remains evidence-boundary metadata only |

## Next Reviewer Prompt

```text
Review PR #367 implementation for current-fact source-record artifact from candidates.

Check:
- PR diff contains only approved implementation files.
- Source-record artifact uses PR #366 production candidate artifact as the
  input boundary.
- Source-record generator output and committed JSON match.
- `tests/validation/validate_current_fact_row_move_cell_candidates.py` changes
  are limited to approved source-record artifact coexistence compatibility.
- Candidate validator responsibility remains limited to candidate artifact and
  `candidate-inputs/` boundary validation.
- Source-record artifact semantics remain assigned to
  `validate_current_fact_source_records.py`.
- No legacy data/exports/*/official_raw.json is used.
- No .local, raw HTML, full rows, screenshots, VLM output, or private data is
  used as authority.
- No current-fact export artifact, runtime lookup change, parser/classifier
  behavior change, retrieval, answer, calculator, SymPy, source acquisition, or
  live acquisition is included.
- Production source-record artifact has exactly 13 records from PR #366
  candidate input.
- Source-record artifact top-level run_id is schema-valid `20260525T000000Z`;
  PR #365's `20260525` evidence ID is retained only in references.
- `annotated_numeric_candidate` and `frame_range` remain non-scalar and not
  calculation-safe.
- Official records remain `authority_candidate`.
- Validator boundary changes are evidence-first and audit entries match the
  new helper/validator scope.
- Issue #343 double-check gate remains required for future raw-value
  expansion.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- git diff --cached --check
- uv lock --check
- PYTHONPATH=src uv run --locked python -m unittest discover -s tests
- for f in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$f" || exit $?; done
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether PR #367 is ready to mark ready and merge.
```
