# Current-Fact Export Generator Fixture-Contract Implementation

Status: Implemented; validation passed.

## Purpose

Plan the first deterministic current-fact export generator implementation
slice as fixture-contract only.

The original planning PR was docs-only. This implementation follow-up adds
the fixture-contract generator helper, focused tests, focused validator,
validator audit updates, and this ExecPlan progress update. It does not create
a production source-record artifact, a production current-fact export artifact,
or any runtime lookup behavior.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`
- `docs/execplans/2026-05-25-current-fact-export-generator.md`
- `docs/execplans/2026-05-25-current-fact-source-record-input-artifact.md`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_source_record_input.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `tests/fixtures/current-facts/source-records/valid/*.json`
- `tests/fixtures/current-facts/source-records/invalid/*.json`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/validation/validate_current_fact_source_records.py`
- `tests/validation/validate_current_fact_consumer_guards.py`

## Context

PR #357 added the reviewed source-record input schema, fixtures, and validator.
That gives the repository a contract for row/move/cell-level input records,
but it did not create a production source-record artifact and did not implement
an export generator.

Current state:

- `current_fact_export.schema.json` requires `current_fact_export/v2`;
- export records require `parsed_value`;
- current-fact records require top-level `calculation_input_status`;
- source-record input fixtures are synthetic contracts, not source truth;
- no `data/current-facts/source-records/` production artifact exists;
- no `data/current-facts/*-current-fact-export.json` production artifact
  exists;
- runtime lookup still reads the legacy raw export path.

The next safe implementation slice is a fixture-contract generator that proves
deterministic transformation from reviewed source-record input shape to
`current_fact_export/v2` shape without writing production artifacts.

## Scope

Included in this docs-only plan:

- define the fixture-contract generator implementation boundary;
- decide helper module shape and public functions;
- decide how source-record sidecar identity is stripped;
- decide deterministic output ordering;
- decide schema, guard, authority, and privacy validation;
- define tests and focused validator expectations;
- preserve production artifact, runtime, parser/classifier, answer, and
  calculator exclusions.

Excluded from this plan and the future implementation PR:

- No production source-record artifact generation under
  `data/current-facts/source-records/`.
- No production current-fact export artifact generation under
  `data/current-facts/`.
- No Markdown summary generation under `docs/current-facts/`.
- No runtime lookup switch.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier behavior change.
- No retrieval implementation.
- No answer implementation.
- No calculator implementation.
- No SymPy logic.
- No live acquisition.
- No source acquisition.
- No authority promotion.
- No mutable latest pointer.

## Implementation Boundary

Future implementation should add a small helper module, for example:

- `src/sf6_knowledge_coach/current_fact_export_generator.py`

The helper should expose deterministic in-memory functions only, for example:

- `build_current_fact_export(source_record_payload: Mapping[str, Any]) -> dict[str, Any]`
- `validate_current_fact_export_payload(payload: Mapping[str, Any]) -> list[str]`

The first implementation should not add a CLI command and should not write
files. A later production artifact PR may add a file-writing wrapper after a
reviewed production source-record input artifact exists.

The generator helper must:

1. accept a `current_fact_source_record_input/v1` payload;
2. validate the payload with the source-record input schema or an equivalent
   validator before transformation;
3. reject missing or invalid source-record fields;
4. extract each nested `current_fact_record`;
5. strip all source-record-only identity fields;
6. reject records without `parsed_value`;
7. preserve `raw_value`, `parsed_value`, `value_shape`, source fields,
   `authority_status`, `evidence`, and `calculation_input_status`;
8. sort output records deterministically by
   `(source_name, character_slug, move_id, field_key, record_id)`;
9. set `artifact_schema_version == "current_fact_export/v2"`;
10. carry forward `run_id` and authority boundary values;
11. construct `generated_from` from reviewed public source paths already
    present in the source-record input payload;
12. validate the output with `current_fact_export.schema.json`;
13. run guard/authority/privacy checks before returning output.

The generator must not:

- read `data/exports/<character>/official_raw.json`;
- read `.local` artifacts;
- read raw HTML or full rows;
- call live acquisition;
- infer current facts from group-level coverage alone;
- flatten `annotated_numeric_candidate`;
- collapse `frame_range`;
- promote official or SuperCombo authority;
- call `current_facts.py` or `answering.py`;
- write any artifact.

## Source Input Boundary

The fixture-contract implementation may use only synthetic fixtures under
`tests/fixtures/current-facts/source-records/`.

Allowed implementation inputs:

- valid source-record input fixtures;
- invalid source-record input fixtures;
- current-fact schemas;
- guard helper;
- synthetic expected payloads in unit tests or validators.

Excluded implementation inputs:

- production `data/current-facts/source-records/` artifacts, because none are
  approved yet;
- legacy `data/exports/<character>/official_raw.json`;
- `.local`;
- raw HTML;
- full raw rows;
- screenshots;
- ChatGPT/VLM observations as authority;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, or private
  data;
- SuperCombo numeric values as authority.

The implementation must not generate production source-record or current-fact
export artifacts from synthetic fixtures. Test outputs should be compared in
memory or written only to temporary directories created by the test runner.

## Record Transformation Rules

For each input source record:

- read only `current_fact_record` for export record content;
- do not emit `source_record_id`, `source_row_key`, `source_cell_key`,
  `source_value_key`, row/cell order, raw-value hash, or raw-value length in
  the final export record;
- require `parsed_value`;
- require top-level `calculation_input_status`;
- preserve nested non-scalar parsed-value wrappers exactly;
- preserve `frame_range.start` and `frame_range.end` exactly;
- preserve `annotated_numeric_candidate.numeric_candidate` inside the
  annotated wrapper only;
- reject `review_required_not_calculation_safe` and `out_of_scope_not_emitted`
  from lookup-ready output;
- keep official records as `authority_candidate`;
- keep SuperCombo records enrichment/cross-reference only and never scalar
  numeric authority;
- reject any output whose `generated_from` references `data/exports/`;
- reject any output that contains `.local`, raw HTML, screenshots, local paths,
  cookies, profiles, traces, debug dumps, logs, or private data.

## Guard And Authority Checks

The helper or focused validator must run guard checks equivalent to:

```python
is_scalar_calculation_input(
    record["parsed_value"],
    record["calculation_input_status"],
)
```

Required guard behavior:

- scalar accepted status remains only
  `eligible_only_after_domain_source_and_unit_checks`;
- `annotated_candidate_not_calculation_safe` remains non-scalar;
- `parsed_range_not_single_value_calculation_safe` remains non-scalar;
- `not_numeric_authority` remains non-scalar;
- no nested annotated numeric candidate can be consumed as a scalar;
- no frame range can be consumed as a scalar.

Authority checks:

- the export must keep `authority_boundary.official ==
  "authority_candidate_only"`;
- the export must keep `authority_boundary.supercombo ==
  "enrichment_or_cross_reference_only"`;
- official records remain `authority_candidate`;
- SuperCombo records must not use
  `eligible_only_after_domain_source_and_unit_checks`;
- no current-fact authority promotion is allowed.

## Tests

Future implementation must add focused unit tests, for example:

- valid minimal source-record fixture builds a valid `current_fact_export/v2`;
- valid non-scalar fixture builds valid records without flattening
  `annotated_numeric_candidate`;
- valid frame-range fixture builds valid records without collapsing
  `frame_range`;
- output record ordering is deterministic regardless of input order;
- source-record sidecar identity fields are stripped from output records;
- `generated_from` contains only reviewed public source paths and no
  `data/exports/`;
- invalid source-record fixtures are rejected;
- SuperCombo scalar authority fixture is rejected;
- review-required/no-parsed-value fixture is rejected;
- no artifact file is written under `data/current-facts/` or
  `docs/current-facts/`.

Unit tests should use synthetic fixtures only. They must not read legacy raw
exports, `.local`, raw HTML, screenshots, or live sources.

## Validator Plan

Future implementation must add a focused validator, for example:

- `tests/validation/validate_current_fact_export_generator.py`

Validator requirements:

- validate generator output against `current_fact_export.schema.json`;
- validate source inputs against
  `current_fact_source_record_input.schema.json`;
- verify deterministic ordering;
- verify no source-record sidecar fields leak into export records;
- verify `generated_from` rejects `data/exports/` and private/local paths;
- verify guard behavior for scalar, annotated, frame-range, and
  non-authority records;
- verify authority boundaries remain unchanged;
- verify no production artifacts are generated under `data/current-facts/` or
  `docs/current-facts/`;
- verify validator/test audit includes the new validator.

The validator is a synthetic contract and boundary validator. It does not
prove source truth and must not be treated as approval to generate production
exports.

## Future Production Artifact Gate

Production current-fact export generation remains blocked until a reviewed
public source-record artifact exists under the approved
`data/current-facts/source-records/` contract.

Before any production artifact PR:

- source-record artifact generation must be separately planned and reviewed;
- reviewed public source inputs must be explicit;
- legacy raw exports must remain excluded as source input;
- production source-record artifacts must pass source-record validators;
- production export artifacts must pass generator/export validators;
- no runtime lookup switch may occur until export artifact mandatory review,
  parity criteria, and rollback criteria are complete.

## Acceptance Criteria

- The ExecPlan is docs-only.
- The ExecPlan plans fixture-contract generator implementation only.
- The ExecPlan does not authorize production source-record artifacts.
- The ExecPlan does not authorize production current-fact export artifacts.
- The ExecPlan does not authorize runtime lookup or answer behavior changes.
- The ExecPlan excludes parser/classifier expansion, retrieval, answer,
  calculator, SymPy, source acquisition, and live acquisition.
- The planned generator consumes source-record input fixtures only.
- The planned generator emits `current_fact_export/v2` payloads in memory or
  temporary test outputs only.
- The planned generator strips source-record sidecar identity fields.
- The planned generator preserves raw values and structured parsed values.
- The plan requires no flattened `annotated_numeric_candidate`.
- The plan requires no collapsed `frame_range`.
- The plan rejects legacy raw export source paths and private/local artifacts.
- The plan requires guard, authority, schema, privacy, and deterministic
  ordering validation.
- Validation commands pass.

## Files / Interfaces

The original docs-only plan changed only:

- `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md`

This fixture-contract implementation touches only:

- `src/sf6_knowledge_coach/current_fact_export_generator.py`;
- `tests/test_current_fact_export_generator.py`;
- `tests/validation/validate_current_fact_export_generator.py`;
- validator audit artifacts;
- this ExecPlan progress/completion table.

Future implementation may touch, after review:

- optional synthetic generator fixtures under `tests/fixtures/current-facts/`.

This implementation must not touch:

- `data/current-facts/` production artifacts;
- `docs/current-facts/` production summaries;
- `src/sf6_knowledge_coach/current_facts.py`;
- `src/sf6_knowledge_coach/answering.py`;
- parser/classifier behavior files;
- retrieval, answer, calculator, SymPy, source acquisition, or live acquisition
  surfaces.

## Validation Commands

Run from repository root:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
git status --short --branch
```

## Progress

- [x] (2026-05-25 JST) PR #357 was marked ready and merged with normal merge
  commit `b18ea9b5dee780a511e1236868257aa19fd64ecd`.
- [x] (2026-05-25 JST) Local `main` was fast-forwarded to `origin/main` at
  `b18ea9b5dee780a511e1236868257aa19fd64ecd`; main CI passed in run
  `26377391169`.
- [x] (2026-05-25 JST) Created branch
  `plan/current-fact-export-generator-fixture-contract-implementation`.
- [x] (2026-05-25 JST) Inspected the current-fact export generator plan, the
  implemented source-record schema plan, source-record fixtures, source-record
  validator, and current-fact module inventory.
- [x] (2026-05-25 JST) Drafted this docs-only fixture-contract generator
  implementation ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, current-fact schema validator,
  current-fact source-record validator, current-fact consumer guard validator,
  parsed-value classifier validator, and `git status --short --branch`.
- [x] (2026-05-25 JST) PR #358 mandatory review passed and was merged with
  normal merge commit `323b56c3952ed39b9cea038b66689fce10701e58`.
- [x] (2026-05-25 JST) Local `main` was fast-forwarded to `origin/main` at
  `323b56c3952ed39b9cea038b66689fce10701e58`; main CI passed in run
  `26378555283`.
- [x] (2026-05-25 JST) Created branch
  `impl/current-fact-export-generator-fixture-contract`.
- [x] (2026-05-25 JST) Added
  `src/sf6_knowledge_coach/current_fact_export_generator.py` with in-memory
  source-record input validation, deterministic transformation to
  `current_fact_export/v2`, output validation, guard checks, authority checks,
  and public source-boundary checks.
- [x] (2026-05-25 JST) Added focused unit tests for minimal export
  generation, sidecar field stripping, non-scalar wrapper preservation,
  deterministic ordering, invalid fixture rejection, flattened annotated
  candidate rejection, collapsed frame-range rejection, and legacy
  `generated_from` rejection.
- [x] (2026-05-25 JST) Added focused generator validator for fixture-contract
  output, invalid fixture rejection, synthetic export boundary mutations, and
  absence of production artifacts under `data/current-facts/` and
  `docs/current-facts/`.
- [x] (2026-05-25 JST) Updated validator audit artifacts for the new focused
  unit test and validator.
- [x] (2026-05-25 JST) Full implementation validation passed: `git diff
  --check`, `git diff --cached --check`, `uv lock --check`, unittest,
  clean-slate validator, current-fact schema validator, current-fact
  source-record validator, current-fact consumer guard validator,
  parsed-value classifier validator, current-fact export generator validator,
  validator audit validator, `git status --short --branch`, and production
  artifact path check.
- [ ] Complete implementation mandatory review.

## Decision Log

- Decision: Implement the first generator as fixture-contract only.
  Rationale: Production source-record artifacts do not exist yet; fixture-only
  implementation can lock transformation, ordering, guard, authority, and
  privacy behavior without producing public data artifacts.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep generator helper in-memory and avoid a CLI in the first
  implementation.
  Rationale: A CLI implies file IO and production artifact paths before the
  production input gate is resolved.
  Date/Author: 2026-05-25 / Codex

- Decision: Strip source-record sidecar identity fields from export records.
  Rationale: The sidecar fields are input provenance helpers, while
  `current_fact_export/v2` records must remain compatible with the current
  export schema.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep production artifact generation out of scope.
  Rationale: Reviewed public row/move/cell source-record input artifacts are
  still missing.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: The generator transforms reviewed structured values; it performs
  no arithmetic.
  Date/Author: 2026-05-25 / Codex

- Decision: Validate source-record and export payloads in the helper before
  returning output.
  Rationale: The fixture-contract helper is the future production transform
  core; keeping schema, guard, authority, and source-boundary checks in the
  helper makes later file-writing wrappers harder to misuse.
  Date/Author: 2026-05-25 / Codex

- Decision: Do not add a CLI or file writer.
  Rationale: This slice proves in-memory transformation only. File IO and
  production artifact paths remain blocked until source-record artifact review.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- Production source-record artifact generation remains unplanned for
  implementation.
- Production current-fact export artifact generation remains blocked until the
  source-record artifact exists and is reviewed.
- Runtime lookup remains legacy raw export backed.
- Fixture-contract tests do not prove source truth.
- Future production generator wrappers will need file IO, parity, rollback,
  and artifact review plans.
- Validator/test coverage is synthetic contract coverage and does not prove
  source truth.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only fixture-contract generator plan | Drafted plan for in-memory current-fact export generator implementation from source-record fixtures | `docs/execplans/2026-05-25-current-fact-export-generator-fixture-contract-implementation.md` | `git diff --check`; `uv lock --check`; clean-slate validator; current-fact schema validator; source-record validator; consumer guard validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review complete via PR #358 | Production artifact generation remains blocked |
| Generator helper | Added in-memory source-record-to-export helper with source-record validation, sidecar stripping, deterministic ordering, v2 output construction, output validation, guard checks, authority checks, and source-boundary checks | `src/sf6_knowledge_coach/current_fact_export_generator.py` | Unit tests; export generator validator | Passed | None | Review pending | Future file-writing wrapper still blocked |
| Unit tests | Added focused tests for successful fixture generation, non-scalar wrapper preservation, deterministic ordering, invalid source fixture rejection, flattened annotated rejection, collapsed range rejection, and legacy generated_from rejection | `tests/test_current_fact_export_generator.py` | Unittest | Passed | None | Review pending | Synthetic fixtures do not prove source truth |
| Focused validator | Added fixture-contract validator for valid fixture outputs, invalid fixture rejection, synthetic output boundary mutations, and absence of production artifacts | `tests/validation/validate_current_fact_export_generator.py` | Export generator validator; validator audit | Passed | None | Review pending | Production artifact validation remains future work |
| Validator audit | Added evidence-boundary audit entries for the new unit test and focused validator | `data/validator-audits/20260523-validator-test-fact-source-audit.json`; `docs/validator-audits/20260523-validator-test-fact-source-audit.md` | Validator audit validator | Passed | None | Review pending | Audit is boundary metadata only |
| Input/output boundary | Implemented source-record fixture inputs and in-memory `current_fact_export/v2` payload outputs only | Generator helper, tests, validator, this ExecPlan | Unit tests; export generator validator; production artifact path check | Passed | None | Review pending | No production source-record artifact exists |
| Guard/authority/privacy behavior | Implemented schema, guard, authority, generated_from, privacy, and deterministic ordering checks for fixture-contract output | Generator helper, tests, validator, this ExecPlan | Unit tests; export generator validator; current-fact guard validator | Passed | None | Review pending | Future generators must preserve equivalent checks |
| Runtime exclusion | Kept `current_facts.py`, `answering.py`, retrieval, answer, calculator, SymPy, source acquisition, live acquisition, and parser/classifier behavior out of scope | No runtime/parser/source-acquisition files changed | Diff/status review | Passed | None | Review pending | Runtime remains legacy raw backed |

## Next Reviewer Prompt

```text
Review the fixture-contract current-fact export generator implementation.

Check:
- PR diff is limited to generator helper, focused unit test, focused
  validator, validator audit artifacts, and this ExecPlan.
- Generator accepts source-record fixture payloads and returns
  `current_fact_export/v2` payloads in memory.
- No production source-record artifact under data/current-facts/source-records/
  is generated.
- No production current-fact export artifact under data/current-facts/ is
  generated.
- Implementation consumes only source-record fixtures and current-fact schemas.
- Implementation emits only in-memory current_fact_export/v2 payloads.
- Source-record schema validation happens before transformation.
- Export schema validation happens before returning output.
- Source-record sidecar identity fields are stripped from export records.
- raw_value, parsed_value, value_shape, source fields,
  authority_status, evidence, and calculation_input_status are preserved.
- Output ordering is deterministic by source, character, move, field, and
  record ID.
- Generator rejects legacy data/exports/*, .local, raw HTML, screenshots/VLM as
  authority, local paths, private data, and SuperCombo numeric authority.
- annotated_numeric_candidate is not flattened.
- frame_range is not collapsed.
- Guard, authority, schema, privacy, and validator-audit checks are included.
- No CLI or file writer is added.
- Runtime lookup, current_facts.py, answering.py, parser/classifier behavior,
  retrieval, answer, calculator, SymPy, source acquisition, and live
  acquisition remain excluded.

Run:
- git status --short --branch
- git show --name-status --oneline --no-renames HEAD
- git diff --check origin/main...HEAD
- git diff --cached --check
- uv lock --check
- PYTHONPATH=src uv run --locked python -m unittest discover -s tests
- PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_source_records.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_consumer_guards.py
- PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
- PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_export_generator.py
- PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py

Return blocking findings first, validation results, PLAN deviations,
remaining risks, and whether the implementation is stage-ready.
```
