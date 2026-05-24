# Current-Fact Calculation Status Schema

Status: Implemented; validation passed.

## Purpose

Plan the schema/status-carrier change required before current-fact export
generation: add top-level `calculation_input_status` to current-fact records
and align the closed status enum with `current_fact_guards` and parsed-value
classifier coverage.

This is a docs-only planning PR. It does not implement schema changes,
generated exports, export generators, runtime lookup, answer behavior, parser
or classifier behavior, retrieval, calculators, SymPy, or live acquisition.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`
- `contracts/current-facts/current_fact_record.schema.json`
- `contracts/current-facts/current_fact_export.schema.json`
- `contracts/current-facts/parsed_value.schema.json`
- `src/sf6_knowledge_coach/current_fact_guards.py`
- `tests/validation/validate_current_fact_schemas.py`
- `tests/validation/validate_current_fact_consumer_guards.py`
- `tests/fixtures/current-facts/records/valid/*.json`
- `tests/fixtures/current-facts/records/invalid/*.json`
- `tests/fixtures/current-facts/exports/valid/*.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`

## Context

PR #352 selected a top-level `calculation_input_status` field as the preferred
status carrier for future current-fact export records.

Current state:

- `current_fact_record.schema.json` has no `calculation_input_status` field;
- `current_fact_export.schema.json` has
  `artifact_schema_version == "current_fact_export/v1"`;
- `current_fact_record.schema.json` currently permits records without
  `parsed_value`;
- `current_fact_guards.is_scalar_calculation_input(parsed_value,
  calculation_input_status)` already requires a status argument;
- current-fact schema fixtures include review-required/no-parsed-value records
  that are useful schema fixtures but are not safe lookup-ready export records.

The next implementation must make the status field explicit before any export
generator is added.

## Scope

Included in this docs-only plan:

- decide schema version strategy for the status carrier change;
- define the closed `calculation_input_status` enum;
- decide whether first current-fact export records may include
  review-required/no-parsed-value records;
- define how `current_fact_guards.is_scalar_calculation_input` consumes the
  schema field;
- define validators and fixture updates for the future schema implementation;
- preserve the legacy raw export debt boundary.

Excluded:

- No schema implementation.
- No generated export artifact.
- No export generator.
- No runtime change.
- No `current_facts.py` change.
- No `answering.py` change.
- No parser/classifier change.
- No retrieval implementation.
- No calculator implementation.
- No SymPy logic.
- No live acquisition.
- No authority promotion.

## Schema Version Decision

Decision for the future implementation PR:

- amend existing schema files in place;
- bump `current_fact_export.schema.json` artifact schema const from
  `current_fact_export/v1` to `current_fact_export/v2`;
- do not introduce parallel v2 schema filenames or duplicate schema IDs in the
  first implementation slice;
- update fixtures and validators to expect `current_fact_export/v2`.

Rationale:

- no production normalized current-fact export artifact exists yet;
- current schema files are repository contracts rather than runtime-loaded
  public API endpoints;
- adding the top-level status field is a breaking artifact contract change and
  should be visible through `artifact_schema_version`;
- parallel schema files would add maintenance overhead before there is more
  than one real export artifact generation path.

Implementation review must stop and amend the plan if an external consumer or
existing generated artifact is found that requires preserving
`current_fact_export/v1`.

## Calculation Status Enum Decision

Future `current_fact_record.schema.json` must add:

```json
"calculation_input_status": {
  "enum": [
    "eligible_only_after_domain_source_and_unit_checks",
    "annotated_candidate_not_calculation_safe",
    "parsed_range_not_single_value_calculation_safe",
    "review_required_not_calculation_safe",
    "enum_only_not_arithmetic",
    "raw_preserved_not_calculation",
    "not_numeric_authority",
    "out_of_scope_not_emitted"
  ]
}
```

The field must be top-level and required on current-fact records. The enum must
remain closed.

Status meaning for first schema implementation:

- `eligible_only_after_domain_source_and_unit_checks`: scalar-shaped parsed
  value may be considered by scalar consumers only after domain, source,
  authority, and unit checks also pass;
- `annotated_candidate_not_calculation_safe`: parsed annotated numeric
  candidate; display/search metadata only;
- `parsed_range_not_single_value_calculation_safe`: parsed range; not a scalar
  exact value;
- `review_required_not_calculation_safe`: source/value still requires review;
- `enum_only_not_arithmetic`: enum token; not arithmetic input;
- `raw_preserved_not_calculation`: raw value preserved but not parsed for
  calculation;
- `not_numeric_authority`: parsed or candidate value is not numeric authority;
- `out_of_scope_not_emitted`: policy status for values that must not be emitted
  as current-fact lookup records.

The enum is aligned with current guard constants and parsed-value classifier
coverage. Adding, removing, or renaming a status requires an ExecPlan and
validator update.

## Review-Required Record Decision

Decision for the first lookup-ready current-fact export:

- first export stays parsed-value-only;
- records without `parsed_value` are not admitted to the lookup-ready export;
- review-required/no-parsed-value records remain in parsed-value classifier
  coverage and source-review artifacts;
- if future hold-message or review-metadata consumers need blocked records,
  they must use a separate metadata export or a reviewed nullable
  `parsed_value` design.

Schema implementation direction:

- `current_fact_record.schema.json` should define and require
  `calculation_input_status`;
- the lookup-ready export schema or export validator must require
  `parsed_value` for records in `data/current-facts/<run_id>-current-fact-export.json`;
- do not rely on runtime code to filter out missing `parsed_value`.

This keeps the first export from recreating legacy raw-value lookup behavior
under a new filename.

## Guard Usage Decision

Future current-fact consumers must read `calculation_input_status` directly
from the record:

```python
is_scalar_calculation_input(
    record.get("parsed_value"),
    record.get("calculation_input_status"),
)
```

Consumers must not:

- derive status from `value_shape`;
- infer scalar safety from `parsed_value.kind`;
- fall back to legacy raw export values when the status is missing;
- flatten nested `annotated_numeric_candidate.numeric_candidate`;
- collapse `frame_range.start` and `frame_range.end` into a scalar.

The guard returning `True` is necessary but not sufficient. Future lookup code
must still check field domain, source role, source name, authority status, and
unit compatibility before exact answers or calculators consume a value.

## Validator Plan

The future schema implementation must add or update validators in a
boundary-based way.

Required validation updates:

- `tests/validation/validate_current_fact_schemas.py`
  - validates `current_fact_export/v2`;
  - validates `calculation_input_status` is required and closed;
  - validates lookup-ready export records include `parsed_value`;
  - rejects unknown status strings;
  - keeps the public privacy scan.
- `tests/validation/validate_current_fact_consumer_guards.py`
  - verifies every schema status is recognized by the guard tests;
  - verifies `eligible_only_after_domain_source_and_unit_checks` is the only
    scalar-accepted status;
  - verifies blocked/non-scalar statuses are rejected.
- Parsed-value classifier compatibility validation
  - samples current coverage statuses and ensures each status is either in the
    schema enum or intentionally not emitted;
  - verifies coverage statuses for annotated candidates, frame ranges,
    review-required values, raw-preserved values, enum-only values,
    non-authority values, and out-of-scope values remain compatible.
- Privacy/no-local-path validation
  - schema fixtures and generated public artifacts must not include `.local`,
    raw HTML, screenshots, full raw rows, local absolute paths, cookies,
    profiles, traces, debug dumps, logs, or private data.

Validators must not be weakened to fit current fixtures. Fixture updates must
follow this plan's status and parsed-value requirements.

## Fixture Strategy

Future schema implementation must update fixtures deliberately.

Accepted valid fixtures:

- synthetic scalar signed-frame or integer current-fact record with
  `calculation_input_status ==
  "eligible_only_after_domain_source_and_unit_checks"`;
- official authority-candidate scalar fixture must remain synthetic contract
  evidence unless a later authority review approves production use;
- v2 current-fact export fixture containing lookup-ready records with
  `parsed_value` and top-level `calculation_input_status`.

Rejected invalid fixtures:

- `annotated_numeric_candidate` with
  `annotated_candidate_not_calculation_safe` in scalar context;
- `frame_range` with
  `parsed_range_not_single_value_calculation_safe` in scalar context;
- review-required/no-parsed-value record inside lookup-ready export;
- `not_numeric_authority` record in scalar context;
- record missing `calculation_input_status`;
- record with unknown `calculation_input_status`;
- export with legacy `data/exports/*/official_raw.json` in `generated_from`.

Existing review-required record fixtures may remain as record-level schema
fixtures only if they satisfy the new required status field and are not used as
lookup-ready export records. If this distinction becomes confusing in tests,
implementation should split fixture directories between record-shape fixtures
and lookup-ready export fixtures.

## Debt Rule

Do not add compatibility fields just to support legacy
`data/exports/<character>/official_raw.json`.

Legacy raw exports remain technical debt:

- current dependent code path: `current_facts.py` and `answering.py`;
- replacement requirement: v2 current-fact export with top-level status,
  parsed values, guard validation, authority/source validation, parity review,
  and rollback criteria;
- retirement blocker: export generator, lookup helper, runtime switch, and
  parity validators are not implemented yet;
- intended removal: remove or demote legacy raw lookup after replacement
  current-fact lookup is reviewed and stable.

No new schema field should exist only to mirror legacy raw export columns.

## Future Implementation Slices

Recommended next sequence:

1. Schema/status carrier implementation.
   Update current-fact schemas, fixtures, schema validator, consumer guard
   validator, and validator audit if needed.
2. Current-fact export generator ExecPlan.
   Plan the generator from reviewed public artifacts only.
3. Current-fact export generator implementation.
   Emit v2 export and optional summary with no runtime behavior change.
4. Export artifact mandatory review.
   Confirm status, guard behavior, authority/source boundaries, privacy, and
   no legacy raw dependency.
5. Parsed-value-backed lookup helper plan/implementation.
   Add helper/tests without answer behavior change.
6. Runtime switch plan/implementation.
   Switch `current_facts.py` or `answering.py` only after parity and rollback
   review.

## Acceptance Criteria

- The ExecPlan is docs-only.
- The ExecPlan chooses the schema version strategy.
- The ExecPlan defines the exact closed `calculation_input_status` enum.
- The ExecPlan decides first export stays parsed-value-only and excludes
  review-required/no-parsed-value records.
- The ExecPlan defines how `is_scalar_calculation_input` consumes the
  top-level schema field.
- The ExecPlan defines validators for schema fixtures, consumer guard
  behavior, parsed-value classifier compatibility, and privacy/no local paths.
- The ExecPlan defines accepted and rejected fixture strategy.
- The ExecPlan records the legacy raw export debt rule.
- No schema, generated export, export generator, runtime, answer, parser,
  classifier, retrieval, calculator, SymPy, or live acquisition changes are
  made.
- Validation commands pass.

## Files / Interfaces

The reviewed docs-only planning PR changed only:

- `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md`

This implementation may touch only:

- `contracts/current-facts/current_fact_record.schema.json`;
- `contracts/current-facts/current_fact_export.schema.json`;
- `tests/fixtures/current-facts/records/valid/*.json`;
- `tests/fixtures/current-facts/records/invalid/*.json`;
- `tests/fixtures/current-facts/exports/valid/*.json`;
- current-fact schema validators;
- current-fact consumer guard validators;
- validator audit artifacts if new or changed test/validator files require it.

This implementation does not authorize export generation or runtime changes.

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
  `plan/current-fact-calculation-status-schema`.
- [x] (2026-05-25 JST) Inspected current-fact schemas, schema fixtures,
  schema validator, consumer guard validator, current-fact guard helper, and
  PR #352 export design amendment.
- [x] (2026-05-25 JST) Drafted this docs-only schema/status carrier ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [x] (2026-05-25 JST) Completed mandatory review for the docs-only PR #353
  with no blocking findings.
- [x] (2026-05-25 JST) PR #353 was marked ready and merged with normal merge
  commit `b8ca11b89399fb87da2470a1c4ccd90a1b421a0b`; local `main` was
  fast-forwarded to `origin/main`.
- [x] (2026-05-25 JST) Created implementation branch
  `impl/current-fact-calculation-status-schema`.
- [x] (2026-05-25 JST) Added top-level required
  `calculation_input_status` to `current_fact_record.schema.json` with the
  approved closed eight-value enum.
- [x] (2026-05-25 JST) Bumped current-fact export artifact version to
  `current_fact_export/v2` and required lookup-ready export records to include
  `parsed_value`.
- [x] (2026-05-25 JST) Updated current-fact record/export fixtures with
  status values, v2 export version, and invalid fixtures for unknown status,
  legacy raw `generated_from`, and review-required/no-parsed-value export
  records.
- [x] (2026-05-25 JST) Updated focused schema and consumer guard validators
  for the closed status enum, v2 export version, invalid export fixtures, and
  coverage/status compatibility.
- [x] (2026-05-25 JST) Updated parsed-value classifier compatibility
  validation so current-fact-compatible sample records include top-level
  `calculation_input_status` from `ClassificationResult`.
- [x] (2026-05-25 JST) Final implementation validation passed:
  `git diff --check`, `git diff --cached --check`, `uv lock --check`,
  unittest discovery, clean-slate validator, all validation scripts,
  parsed-value classifier coverage validator, and `git status --short
  --branch`.
- [ ] Complete implementation review.

## Decision Log

- Decision: Amend existing schema files in place but bump export artifact
  schema version to `current_fact_export/v2`.
  Rationale: No production normalized export exists yet, but the required
  status field is a breaking artifact contract and should be visible in the
  artifact version.
  Date/Author: 2026-05-25 / Codex

- Decision: Use top-level required `calculation_input_status` with a closed
  enum.
  Rationale: Scalar-safety is record-local and must travel with records into
  future export, lookup, retrieval, answer, and calculator surfaces.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep the first lookup-ready export parsed-value-only.
  Rationale: Allowing review-required/no-parsed-value records would recreate
  raw lookup behavior and weaken the transition away from legacy exports.
  Date/Author: 2026-05-25 / Codex

- Decision: Do not add compatibility fields for legacy `official_raw.json`.
  Rationale: Legacy raw exports are technical debt, not a stable target for
  the replacement schema.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: This plan concerns schema/status carrier validation, not
  arithmetic.
  Date/Author: 2026-05-25 / Codex

- Decision: Require `parsed_value` from `current_fact_export/v2.records[]`
  while keeping record-shape fixtures able to represent review-required
  records.
  Rationale: This keeps lookup-ready exports parsed-value-only without
  deleting useful record-level schema fixtures for blocked values.
  Date/Author: 2026-05-25 / Codex

- Decision: Reject legacy raw export paths in `generated_from` at schema level.
  Rationale: The replacement export must not depend on the technical-debt raw
  export surface it is intended to retire.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- Existing review-required/no-parsed-value record-shape fixtures remain valid
  only outside lookup-ready export fixtures.
- The first export may have limited coverage because lookup-ready records
  require reviewed `parsed_value`.
- Runtime lookup helper, export generator, parity validator, rollback
  criteria, and legacy raw retirement remain future work.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only schema/status carrier plan | Drafted plan for top-level `calculation_input_status`, v2 export artifact version, validators, fixtures, and debt rule | `docs/execplans/2026-05-25-current-fact-calculation-status-schema.md` | `git diff --check`; `uv lock --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future schema implementation still required |
| Schema version strategy | Chose in-place schema file amendment with `current_fact_export/v2` artifact version | This ExecPlan only | Diff/status review | Passed | None | Review pending | External consumer discovery could require amendment |
| Closed status enum | Listed eight closed status values aligned with current guard and classifier coverage | This ExecPlan only | Diff/status review | Passed | None | Future schema validator update required | Enum drift if classifier policy changes |
| Export record admission | Chose parsed-value-only first lookup-ready export and excluded review-required/no-parsed-value records | This ExecPlan only | Diff/status review | Passed | None | Future export validator required | Limited first-export coverage |
| Scope exclusions | Kept schema/export/runtime/parser/classifier/retrieval/calculator/SymPy/live acquisition implementation out of scope | This ExecPlan only | Diff/status review | Passed | None | Review pending | None for docs-only PR |
| Current-fact record schema | Added required top-level `calculation_input_status` with the approved eight-value closed enum | `contracts/current-facts/current_fact_record.schema.json` | current-fact schema validator | Passed | None | Review pending | Future enum changes require an ExecPlan |
| Current-fact export schema | Bumped export artifact const to `current_fact_export/v2`, required `parsed_value` in export records, and rejected legacy raw `generated_from` paths | `contracts/current-facts/current_fact_export.schema.json` | current-fact schema validator | Passed | None | Review pending | Runtime export generator still absent |
| Fixtures | Updated record/export fixtures for required statuses and added invalid fixtures for unknown status, no parsed value in export, and legacy raw generated_from | `tests/fixtures/current-facts/**` | current-fact schema validator | Passed | None | Review pending | First lookup-ready export coverage remains limited |
| Validators | Updated schema, guard, and parsed-value classifier compatibility validators for status enum, v2 export, export invalid fixtures, classifier status compatibility, and top-level status in current-fact-compatible sample records | `tests/validation/validate_current_fact_schemas.py`; `tests/validation/validate_current_fact_consumer_guards.py`; `tests/validation/validate_parsed_value_classifier.py` | schema validator; guard validator; parsed-value classifier validator; all validation scripts; validator audit | Passed | None | Review pending | Validators cover contracts, not runtime lookup |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-calculation-status-schema.md.

Check:
- PR diff contains exactly one ExecPlan file.
- Plan is docs-only and does not implement schema/export/runtime/parser/
  classifier/retrieval/calculator/SymPy/live acquisition changes.
- Schema version strategy is explicit: amend existing schema files in place,
  but bump export artifact schema version to current_fact_export/v2.
- `calculation_input_status` is planned as a top-level required current-fact
  record field.
- Closed enum exactly contains:
  - eligible_only_after_domain_source_and_unit_checks
  - annotated_candidate_not_calculation_safe
  - parsed_range_not_single_value_calculation_safe
  - review_required_not_calculation_safe
  - enum_only_not_arithmetic
  - raw_preserved_not_calculation
  - not_numeric_authority
  - out_of_scope_not_emitted
- First lookup-ready export remains parsed-value-only; review-required/no
  parsed_value records are excluded from that export.
- `current_fact_guards.is_scalar_calculation_input` consumes the top-level
  schema field and remains necessary but not sufficient for authority.
- Validator plan covers schema fixtures, consumer guard validation,
  parsed-value classifier compatibility samples, and privacy/no local path
  scans.
- Fixture plan covers accepted synthetic scalar and rejected annotated,
  frame_range, review_required/no parsed_value, and not_numeric_authority
  cases.
- Debt rule does not add compatibility fields for legacy official_raw.json.

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
