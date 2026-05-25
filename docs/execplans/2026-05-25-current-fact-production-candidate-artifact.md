# Current-Fact Production Candidate Artifact

Status: Drafted for review; run_id schema amendment pending review; validation passed.

## Purpose

Plan generation of the first production
`current_fact_row_move_cell_candidate_input/v1` artifact from the reviewed
public candidate evidence artifact added by PR #365.

This uses the same draft-PR flow as PR #365: land this ExecPlan in a draft PR,
complete mandatory plan review, then add implementation commits to the same
draft PR. Do not merge the plan-only PR.

The implementation must not use legacy raw exports, ignored local artifacts,
raw HTML, screenshots, VLM output, or private data as authority.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-candidate-evidence-amendment.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-input.md`
- `docs/execplans/2026-05-25-current-fact-row-move-cell-candidate-schema.md`
- `contracts/current-facts/current_fact_row_move_cell_candidate_input.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/source_reference.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json`
- `docs/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.md`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

PR #365 produced summary-safe source-review evidence for 13 current parsed
official candidate cells:

- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`.

Those records prove public row/move/cell identity evidence, but they are not
the production candidate artifact. The next step is to transform that reviewed
evidence into a schema-valid candidate input artifact while preserving all
non-scalar and authority boundaries.

Existing validators still assume `data/current-facts/candidate-inputs/` is
empty. The implementation must deliberately change that boundary from "no
production candidate artifacts yet" to "only the approved candidate artifact
is allowed and validated."

## Scope

Included in this plan and future implementation slice:

- generate one production
  `current_fact_row_move_cell_candidate_input/v1` JSON artifact from the PR
  #365 reviewed public evidence artifact;
- generate one summary-safe Markdown companion;
- add a small deterministic in-memory candidate generator/helper if needed;
- add focused unit tests for generator behavior if a helper is added;
- update `validate_current_fact_row_move_cell_candidates.py` to validate the
  approved production candidate artifact instead of requiring the production
  candidate directory to stay empty;
- update `validate_current_fact_export_generator.py` only to stop treating the
  candidate artifact as a forbidden current-fact export/source-record
  artifact;
- update source/evidence schema only if required to represent a source-review
  evidence basis honestly;
- update validator audit artifacts for any new or changed tests/validators;
- update this ExecPlan Progress, Decision Log, and Completion Review Table.

Excluded:

- No production source-record artifact generation.
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

## Artifact Paths

Planned production candidate JSON:

- `data/current-facts/candidate-inputs/<candidate_run_id>-row-move-cell-candidates.json`

Planned summary Markdown:

- `docs/current-facts/candidate-inputs/<candidate_run_id>-row-move-cell-candidates.md`

`<candidate_run_id>` is the production candidate artifact run ID and must match
the schema-required UTC timestamp format `YYYYMMDDTHHMMSSZ`. The JSON
top-level `run_id` must exactly match `<candidate_run_id>`.

Do not reuse the PR #365 evidence artifact's date-only `20260525` identifier as
the candidate artifact `run_id`. Keep the PR #365 evidence artifact identity in
`generated_from`, `source_review_refs`, and `evidence`; keep source references
to the `20260521T025403Z` acquisition and classifier run through
`generated_from`, `coverage_refs`, `source_review_refs`,
`acquisition_report_refs`, and `evidence`.

## Allowed Source Inputs

Allowed implementation inputs:

- `data/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.json`;
- `docs/source-reviews/20260525-current-fact-row-move-cell-candidate-evidence.md`;
- parsed-value classifier coverage and disposition artifacts needed to
  deterministically reproduce `parsed_value` payloads;
- current-fact schemas and guard helpers;
- public acquisition report and source-review references already carried by
  the PR #365 evidence artifact.

The implementation may use `parsed_value_classifier.classify_raw_value` with
the evidence record's `raw_value` and `coverage_refs` review item ID to
reproduce `parsed_value`. The reproduced result must match the evidence
record's `parser_rule_ids`, `calculation_input_status`, and
`parsed_value_kind`.

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

## Candidate Record Mapping

For each reviewed evidence record, the generator or artifact builder must:

- copy row/move/cell identity fields:
  - `candidate_record_id`;
  - `character_slug`;
  - `move_id`;
  - `display_label_ja`;
  - `field_key`;
  - `source_row_key`;
  - `source_cell_key`;
  - `source_value_key`;
  - `source_row_order`;
  - `source_cell_order`;
- copy source context:
  - `source_name`;
  - `source_role`;
  - `source_family`;
  - `source_header_path`;
  - `source_label`;
- copy raw fields:
  - `raw_value`;
  - `raw_value_length`;
  - `raw_value_sha256`;
- map `authority_status` from `authority_candidate_not_promoted` to
  candidate-schema `authority_candidate`;
- map public references:
  - `coverage_refs` must be public artifact paths, not review item IDs;
  - `source_review_refs` must include the PR #365 evidence JSON and may include
    other public source-review summary paths;
  - `acquisition_report_refs` must be public acquisition report paths;
- reproduce `parsed_value` deterministically;
- carry `value_shape`, `parser_rule_ids`, and top-level
  `calculation_input_status`;
- create an `evidence` object that points to the PR #365 evidence artifact.

## Schema Decision

`source_reference.schema.json` currently has no evidence basis for reviewed
source-review summaries. The implementation may add exactly one enum value if
needed:

- `source_review_summary`

This is preferred over misusing `source_acquisition_report`,
`value_shape_policy`, or `synthetic_contract_fixture` for production candidate
records.

No other schema change is planned. If a broader schema change is needed,
implementation must stop and amend this ExecPlan in the same draft PR before
continuing.

## Candidate Admission

The first production candidate artifact must contain exactly the 13 records
from the PR #365 evidence artifact.

Allowed records:

- `source_review_result == "candidate_identity_evidence_found"`;
- `candidate_generation_status == "blocked_until_candidate_artifact_execplan_review"`;
- `source_name == "official"`;
- `source_role == "authority_candidate"`;
- classifier outcome can deterministically reproduce a `parsed_value`;
- `calculation_input_status` is either
  `annotated_candidate_not_calculation_safe` or
  `parsed_range_not_single_value_calculation_safe`.

Forbidden records:

- review-required or blocked raw variants;
- `candidate_identity_evidence_ambiguous`;
- `candidate_identity_evidence_missing`;
- records with no `parsed_value`;
- SuperCombo scalar numeric authority;
- any value not present in the PR #365 reviewed evidence artifact.

This artifact is lookup-ready as a candidate input, but it does not make any
record calculation-safe. Exact scalar answer paths and calculators must still
reject these non-scalar statuses through `current_fact_guards`.

## Validator Changes

Required validator behavior:

- `validate_current_fact_row_move_cell_candidates.py` must validate:
  - synthetic fixture contracts still pass;
  - production candidate artifact path contains only the approved JSON;
  - Markdown summary path contains only the approved summary;
  - production artifact is schema-valid;
  - production artifact has exactly 13 records;
  - all records come from PR #365 evidence;
  - raw hashes and lengths match;
  - row/cell/value keys are stable and unique;
  - `annotated_numeric_candidate` remains wrapped;
  - `frame_range` remains a range;
  - non-scalar statuses are not scalar calculation inputs;
  - no legacy raw exports, local paths, raw HTML, full rows, screenshots,
    VLM output, or private data are referenced.
- `validate_current_fact_export_generator.py` must continue rejecting
  production source-record/current-fact export artifacts, but must not reject
  the approved candidate input artifact.
- `validate_current_fact_candidate_evidence.py` must continue passing.
- `validate_validator_test_audit.py` must cover any new or modified
  test/validator boundaries.

## Issue #343 Gate

Issue #343 remains mandatory for any future value-handling decision.

This implementation must not add raw values beyond the 13 PR #365 evidence
records. Because the implementation only transforms already-reviewed evidence
into candidate records, no new screenshot/ChatGPT/VLM double-check is required.

If implementation attempts to include any additional raw value, same-grammar
expansion, or changed semantics, it must stop and complete the Issue #343
double-check gate first.

## Acceptance Criteria

- PR begins as docs-only and remains draft after plan review.
- After mandatory plan review, implementation commits may be added to this
  same draft PR.
- Production candidate artifact is generated only from PR #365 reviewed public
  evidence.
- Production candidate artifact top-level `run_id` is a schema-valid
  `YYYYMMDDTHHMMSSZ` timestamp, not the PR #365 date-only evidence identifier.
- Production candidate artifact has exactly 13 records.
- No production source-record or current-fact export artifact is generated.
- No runtime lookup, parser/classifier behavior, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition changes are made.
- Legacy raw exports and private/local evidence are not used as replacement
  source input.
- `annotated_numeric_candidate` and `frame_range` remain non-scalar.
- Official records remain `authority_candidate`.
- Issue #343 gate remains required for future raw-value expansion.

## Files / Interfaces

Plan-only initial PR should change only:

- `docs/execplans/2026-05-25-current-fact-production-candidate-artifact.md`

Future implementation commits in the same draft PR may change only:

- `docs/execplans/2026-05-25-current-fact-production-candidate-artifact.md`
- `src/sf6_knowledge_coach/current_fact_candidate_generator.py` if helper is
  needed
- `tests/test_current_fact_candidate_generator.py` if helper is added
- `tests/validation/validate_current_fact_row_move_cell_candidates.py`
- `tests/validation/validate_current_fact_export_generator.py` if needed
- `tests/validation/validate_current_fact_candidate_evidence.py` if needed
- `contracts/current-facts/source_reference.schema.json` only for
  `source_review_summary` evidence basis if needed
- current-fact schema fixtures only if a schema enum change requires them
- `data/current-facts/candidate-inputs/<candidate_run_id>-row-move-cell-candidates.json`
- `docs/current-facts/candidate-inputs/<candidate_run_id>-row-move-cell-candidates.md`
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
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_candidate_evidence.py
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

- 2026-05-25: Drafted plan after PR #365 merged. No implementation or
  production candidate artifact generated yet.
- 2026-05-25: Ran plan-only validation. All checks passed.
- 2026-05-25: Amended candidate artifact path and top-level `run_id` plan to
  use schema-valid `YYYYMMDDTHHMMSSZ` timestamps while retaining PR #365
  `20260525` only as a source-review evidence reference.

## Decision Log

- 2026-05-25: The production candidate artifact will use PR #365 candidate
  evidence as the input boundary.
- 2026-05-25: The first production candidate artifact is limited to 13 records.
- 2026-05-25: Source-record/export generation and runtime lookup transition
  remain out of scope.
- 2026-05-25: `source_review_summary` is the only planned schema enum addition
  if a source-review evidence basis is needed.
- 2026-05-25: Plan-only validation passed without implementation or generated
  candidate artifact changes.
- 2026-05-25: Candidate artifact `run_id` must be a schema-valid timestamp and
  must not reuse PR #365's date-only source-review evidence identifier.

## Deviations

- None.

## Risks

- A schema enum addition may be required to represent source-review evidence
  honestly.
- Candidate artifact generation may reveal that a reviewed evidence record
  cannot reproduce a valid `parsed_value`; if so, implementation must stop and
  amend the plan.
- Production source-record/export artifacts remain blocked.
- Runtime remains legacy raw export backed.
- The first production candidate artifact contains only non-scalar parsed
  values and is not calculation-safe.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Production candidate artifact plan | Draft plan only | `docs/execplans/2026-05-25-current-fact-production-candidate-artifact.md` | `git diff --check`; `uv lock --check` | Pass | None | Mandatory plan review pending | Schema enum may be needed later |
| Input boundary | Plan restricts input to PR #365 public evidence | Same | `validate_current_fact_candidate_evidence.py` | Pass | None | Mandatory plan review pending | Candidate generation remains unimplemented |
| Candidate run ID | Plan requires schema-valid timestamp `run_id` and keeps PR #365 `20260525` as evidence reference only | Same | `validate_current_fact_schemas.py` | Pass | None | Mandatory plan review pending | Implementation must choose one stable timestamp for JSON and Markdown paths |
| Runtime/export boundary | No runtime/source-record/export changes | Same | current-fact validators | Pass | None | Mandatory plan review pending | Runtime remains legacy raw export backed |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-production-candidate-artifact.md.

Check:
- PR diff initially contains exactly one ExecPlan file.
- Plan uses PR #365 reviewed public candidate evidence as the input boundary.
- Plan does not use legacy data/exports/*/official_raw.json.
- Plan does not use .local, raw HTML, full rows, screenshots, VLM output, or
  private data as authority.
- Plan generates no source-record artifact, current-fact export artifact,
  runtime lookup change, parser/classifier behavior change, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition.
- Planned production candidate artifact is exactly 13 records from PR #365
  evidence.
- Candidate artifact JSON top-level `run_id` and artifact filename use a
  schema-valid `YYYYMMDDTHHMMSSZ` candidate run ID; PR #365's `20260525`
  evidence ID is retained only in references.
- annotated_numeric_candidate and frame_range remain non-scalar and not
  calculation-safe.
- validator boundary changes are explicitly planned.
- any schema change is limited to source_review_summary evidence basis if
  needed.
- Issue #343 double-check gate remains required for future raw-value
  expansion.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- uv lock --check
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_row_move_cell_candidates.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_candidate_evidence.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate

Return blocking findings first, validation results, PLAN deviations, remaining
risks, and whether docs-only plan is approved for same-PR implementation.
```
