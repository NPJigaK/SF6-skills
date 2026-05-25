# Current-Fact Export Artifact From Source Records

Status: Implementation complete; validation passed; mandatory review pending.

## Purpose

Plan generation of the first production `current_fact_export/v2` artifact from
the reviewed production source-record artifact added by PR #367.

This plan is the next step after the production source-record artifact. It must
not switch runtime lookup, answer behavior, retrieval, parser/classifier
behavior, calculators, or legacy raw export retirement. It only defines how to
transform the reviewed source-record input into a committed current-fact export
artifact that can be reviewed before any runtime consumer uses it.

## Draft PR Flow

Use the same draft PR flow as PR #365 through PR #367:

1. Commit this docs-only plan and open a draft PR.
2. Complete mandatory plan review.
3. Add implementation commits to the same draft PR only after plan review
   passes.
4. Complete mandatory implementation review.
5. Ready and merge only after implementation review passes.

The plan-only draft PR must not be merged.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-export-generator.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md`
- `docs/execplans/2026-05-25-current-fact-source-record-artifact-from-candidates.md`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/source_reference.schema.json`
- `src/sf6_knowledge_coach/current_fact_export_generator.py`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- `docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`

## Context

PR #367 produced one schema-valid production source-record artifact:

- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`;
- `docs/current-facts/source-records/20260525T000000Z-current-fact-source-records.md`.

It contains exactly 13 reviewed official source records:

- 9 `annotated_numeric_candidate` records with
  `annotated_candidate_not_calculation_safe`;
- 4 `frame_range` records with
  `parsed_range_not_single_value_calculation_safe`.

Those records are lookup-ready source-record inputs, not scalar calculation
inputs. Exporting them into `current_fact_export/v2` preserves reviewed
metadata and makes the export artifact reviewable, but it does not make any
record exact-answer-ready, calculation-safe, or runtime-selected.

## Scope

Included in this docs-only plan and future implementation slice:

- generate one production `current_fact_export/v2` JSON artifact from the PR
  #367 production source-record JSON only;
- generate one summary-safe Markdown companion;
- add a deterministic production export helper or generator entry point if
  needed;
- add focused unit tests for the helper if changed;
- update `validate_current_fact_export_generator.py` to validate the approved
  production current-fact export artifact;
- update validator audit artifacts for changed tests/validators;
- update this ExecPlan Progress, Decision Log, and Completion Review Table.

Excluded:

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

Planned production current-fact export JSON:

- `data/current-facts/20260525T000000Z-current-fact-export.json`

Planned summary Markdown:

- `docs/current-facts/20260525T000000Z-current-fact-export.md`

The export artifact top-level `run_id` should be `20260525T000000Z`, matching
the reviewed source-record artifact lineage.

## Allowed Source Inputs

Allowed implementation input:

- `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`.

The implementation may use schemas and deterministic helper code to validate
and transform that source-record JSON. It must not rebuild records from lower
level source materials or from the candidate artifact.

Forbidden implementation inputs:

- legacy `data/exports/*/official_raw.json`;
- `data/current-facts/candidate-inputs/*` as direct production export input;
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

The source-record Markdown companion may be referenced in public summaries, but
the export artifact `generated_from` must use the source-record JSON as the
production input boundary.

## Export Mapping

For the production export:

- `artifact_schema_version == "current_fact_export/v2"`;
- `run_id == "20260525T000000Z"`;
- `generated_from == ["data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json"]`;
- `authority_boundary` is copied from the source-record artifact;
- `records` contains exactly 13 current-fact records copied from
  `source_record.current_fact_record`;
- records are deterministically sorted using the existing export generator
  ordering contract;
- source-record sidecar fields are not emitted in export records.

For each exported record:

- preserve `record_id`;
- preserve `character_slug`;
- preserve `move_id`;
- preserve `field_key`;
- preserve `display_label_ja`;
- preserve `raw_value`;
- preserve `parsed_value`;
- preserve `value_shape`;
- preserve `source_name`;
- preserve `source_role`;
- preserve `source_family`;
- preserve `source_label`;
- preserve `source_header_path`;
- preserve `authority_status`;
- preserve `evidence`;
- preserve top-level `calculation_input_status`.

The production export generator must not add facts, infer missing source
context, reinterpret raw values, collapse ranges, flatten annotated numeric
candidates, or promote authority/calculation status.

## Admission Rules

The first production current-fact export artifact must contain exactly the 13
records from the PR #367 source-record artifact.

Allowed records:

- records present in the PR #367 source-record artifact;
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

- any value not present in the PR #367 source-record artifact;
- review-required or blocked raw variants;
- records with no `parsed_value`;
- source-record sidecar fields in export records;
- records sourced directly from candidate artifacts or legacy raw exports;
- SuperCombo scalar numeric authority;
- any raw-value expansion or changed semantics without the Issue #343 gate.

This artifact is reviewed-export-ready, not scalar-calculation-ready. Exact
scalar answer paths and calculators must still reject all 13 non-scalar records
through `current_fact_guards`.

## Validator Changes

Required validator behavior:

- `validate_current_fact_export_generator.py` must validate:
  - synthetic fixture-contract generator behavior still passes;
  - production current-fact export path contains only the approved JSON;
  - Markdown summary path contains only the approved summary;
  - production export artifact is schema-valid;
  - production export has exactly 13 records;
  - production export `generated_from` points only to the PR #367
    source-record JSON;
  - committed production export JSON matches deterministic generator output
    from the PR #367 source-record JSON;
  - source-record sidecar fields do not leak into export records;
  - `annotated_numeric_candidate` remains wrapped;
  - `frame_range` remains a range;
  - non-scalar statuses are not scalar calculation inputs;
  - all records remain official `authority_candidate`;
  - no legacy raw exports, local paths, raw HTML, full rows, screenshots, VLM
    output, or private data are referenced.
- `validate_current_fact_source_records.py` must continue passing and must not
  validate current-fact export semantics.
- `validate_current_fact_row_move_cell_candidates.py` must continue passing
  and must not validate current-fact export semantics.
- `validate_validator_test_audit.py` must cover any new or modified
  test/validator boundaries.

## Issue #343 Gate

Issue #343 remains mandatory for any future value-handling decision.

This implementation must not add raw values beyond the 13 PR #367
source-records. Because the implementation only transforms already-reviewed
source-record current-fact records into export records, no new
screenshot/ChatGPT/VLM double-check is required.

If implementation attempts to include any additional raw value, same-grammar
expansion, or changed semantics, it must stop and complete the Issue #343
double-check gate first.

## Acceptance Criteria

- PR begins as docs-only and remains draft after plan review.
- After mandatory plan review, implementation commits may be added to this
  same draft PR if the reviewer approves that flow.
- Production current-fact export artifact is generated only from the PR #367
  production source-record JSON.
- Production current-fact export artifact top-level `run_id` is
  `20260525T000000Z`.
- Production current-fact export artifact has exactly 13 records.
- No runtime lookup, parser/classifier behavior, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition changes are made.
- Legacy raw exports and private/local evidence are not used as replacement
  source input.
- `annotated_numeric_candidate` and `frame_range` remain non-scalar.
- Official records remain `authority_candidate`.
- Issue #343 gate remains required for future raw-value expansion.

## Files / Interfaces

Plan-only initial PR should change only:

- `docs/execplans/2026-05-25-current-fact-export-artifact-from-source-records.md`

Future implementation commits in the same draft PR may change only:

- `docs/execplans/2026-05-25-current-fact-export-artifact-from-source-records.md`
- `src/sf6_knowledge_coach/current_fact_export_generator.py` if helper changes
  are needed
- `tests/test_current_fact_export_generator.py` if helper changes are made
- `tests/validation/validate_current_fact_export_generator.py`
- `data/current-facts/20260525T000000Z-current-fact-export.json`
- `docs/current-facts/20260525T000000Z-current-fact-export.md`
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

- 2026-05-25: Drafted plan after PR #367 merged. No implementation or
  production current-fact export artifact generated yet.
- 2026-05-26: Ran plan-only validation. All checks passed.
- 2026-05-26: Added a production export helper path that uses the PR #367
  source-record JSON as the only `generated_from` input boundary.
- 2026-05-26: Generated the production `current_fact_export/v2` JSON and
  summary Markdown artifacts from the PR #367 source-record JSON.
- 2026-05-26: Updated focused tests, export validator, and validator audit
  artifacts for the production export artifact boundary.
- 2026-05-26: Ran implementation validation. All checks passed.

## Decision Log

- 2026-05-25: The production current-fact export artifact will use the PR #367
  source-record JSON as the only production input boundary.
- 2026-05-25: The first production current-fact export artifact is limited to
  the 13 source records already reviewed in PR #367.
- 2026-05-25: Export `generated_from` will reference the source-record JSON,
  not the candidate artifacts that originally fed the source-record artifact.
- 2026-05-25: Runtime lookup transition, answer behavior, and legacy raw export
  retirement remain out of scope.
- 2026-05-26: The existing fixture-contract helper keeps its fixture behavior,
  while the production helper overrides `generated_from` to the PR #367
  source-record JSON only.
- 2026-05-26: The production export summary is generated from the committed
  production export JSON and remains summary-safe.

## Deviations

- None.

## Risks

- Runtime remains legacy raw export backed.
- The first production current-fact export artifact contains only non-scalar
  parsed values and is not calculation-safe.
- Export generation may reveal that the existing in-memory export helper needs
  a narrow production `generated_from` override; if so, implementation must
  stay within this plan's helper/test/validator scope.
- Switching `current_facts.py` to the production export requires a future
  lookup parity and rollback ExecPlan.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Production current-fact export artifact plan | Implementation progress, decisions, and review prompt updated | `docs/execplans/2026-05-25-current-fact-export-artifact-from-source-records.md` | `git diff --check`; `uv lock --check` | Pass | None | None | Runtime remains legacy raw export backed |
| Production export helper | Source-record payload to `current_fact_export/v2`; production path uses source-record JSON only | `src/sf6_knowledge_coach/current_fact_export_generator.py`; `tests/test_current_fact_export_generator.py` | `python -m unittest discover -s tests` | Pass | None | None | Helper does not switch runtime lookup |
| Production export artifact | 13 current-fact export records generated from PR #367 source-record JSON | `data/current-facts/20260525T000000Z-current-fact-export.json`; `docs/current-facts/20260525T000000Z-current-fact-export.md` | `validate_current_fact_export_generator.py` | Pass | None | None | All 13 records remain non-scalar and not calculation-safe |
| Input boundary | Export validator checks committed JSON/MD against deterministic helper output from source-record JSON | `tests/validation/validate_current_fact_export_generator.py` | `validate_current_fact_export_generator.py`; `validate_current_fact_source_records.py` | Pass | None | None | Runtime remains legacy raw export backed |
| Validator audit | Audit records updated helper test and export validator evidence boundaries | `data/validator-audits/20260523-validator-test-fact-source-audit.json`; `docs/validator-audits/20260523-validator-test-fact-source-audit.md` | `validate_validator_test_audit.py` | Pass | None | None | Audit remains evidence-boundary metadata only |

## Next Reviewer Prompt

```text
Review PR #368 implementation for production current-fact export artifact from source records.

Check:
- PR diff contains only approved implementation files.
- Implementation uses only
  data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json
  as production input.
- Output is current_fact_export/v2 under data/current-facts/ with a
  summary under docs/current-facts/.
- Committed production export JSON and Markdown match deterministic generator
  output.
- Implementation does not use legacy data/exports/*/official_raw.json.
- Implementation does not use candidate artifacts, .local, raw HTML, full rows,
  screenshots, VLM output, or private data as authority.
- Implementation includes no runtime lookup change, current_facts.py change,
  answering.py change, parser/classifier behavior change, retrieval, answer,
  calculator, SymPy, source acquisition, or live acquisition.
- Production current-fact export artifact is exactly 13 records from PR #367
  source-record input.
- `generated_from` points only to the PR #367 source-record JSON.
- Source-record sidecar fields do not leak into export records.
- annotated_numeric_candidate and frame_range remain non-scalar and not
  calculation-safe.
- Official records remain authority_candidate.
- validator boundary changes are explicitly planned.
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
risks, and whether PR #368 is ready to mark ready and merge.
```
