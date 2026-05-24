# Current-Fact Export Design Amendment

Status: Drafted for review; validation passed.

## Purpose

Decide the reviewed current-fact export design required before
`current_facts.py` can move away from the legacy
`data/exports/<character>/official_raw.json` lookup.

This plan is docs-only. It does not change runtime behavior, answer behavior,
schemas, export generation, parser/classifier behavior, retrieval, calculators,
SymPy usage, or live acquisition.

## Inputs

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-25-current-fact-lookup-parsed-value-transition.md`
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

## Context

The current daily-answer scaffold uses a legacy raw export:

- `current_facts.py` reads
  `data/exports/<character>/official_raw.json`;
- `answering.py` calls `lookup_current_fact()` and emits
  `deterministic_current_fact_lookup` evidence;
- the lookup returns raw field values directly from legacy export rows;
- no parsed-value-backed runtime lookup exists yet.

PR #350 documented that this legacy raw export path is technical debt. It is
retained only because current runtime code still depends on it. Before a
replacement lookup can exist, the repository needs a reviewed current-fact
export design with explicit path, schema/status carrier, source boundaries,
validator boundaries, and debt retirement sequence.

## Scope

Included in this docs-only amendment:

- choose the future export artifact path and naming convention;
- decide the first status-carrier direction for `calculation_input_status`;
- define required record fields for lookup-ready records;
- define allowed and excluded source inputs;
- define validator expectations for future export implementation;
- define how `current_fact_guards.is_scalar_calculation_input` applies to
  exported records;
- define the debt retirement sequence for legacy `official_raw.json`.

Excluded:

- No runtime behavior change.
- No `current_facts.py` change.
- No `answering.py` change.
- No export generator implementation.
- No parser/classifier change.
- No schema change in this PR.
- No generated artifact change.
- No calculator implementation.
- No retrieval implementation.
- No answer implementation.
- No SymPy logic.
- No live acquisition.
- No authority promotion.

## Export Path Decision

Future reviewed current-fact exports should live outside the legacy
`data/exports/` tree so the replacement surface is not confused with the raw
technical debt surface.

Chosen design direction for the first export implementation:

- immutable JSON artifact:
  `data/current-facts/<run_id>-current-fact-export.json`;
- optional summary-safe Markdown report:
  `docs/current-facts/<run_id>-current-fact-export.md`;
- `run_id` uses the existing timestamp shape:
  `YYYYMMDDTHHMMSSZ`;
- `artifact_schema_version` starts from the existing
  `current_fact_export/v1` contract if no schema blocker remains, or a
  reviewed `current_fact_export/v2` if the required status field forces a
  schema revision;
- no runtime "latest" pointer is introduced in the first export generator PR.

The first runtime lookup change must reference an explicitly reviewed export
path or a separately reviewed active-manifest design. This plan does not
authorize adding a mutable latest file.

## Calculation Status Carrier Decision

`current_fact_guards.is_scalar_calculation_input(parsed_value,
calculation_input_status)` requires `calculation_input_status`. The current
`current_fact_record.schema.json` does not require that field.

Decision for the next implementation plan:

- prefer a top-level required `calculation_input_status` field on each
  current-fact export record;
- reject a companion index for the first implementation slice unless a schema
  blocker is found during review;
- keep the status enum closed and aligned with parsed-value classifier
  coverage and current-fact guard tests;
- do not infer scalar safety from `parsed_value.kind` alone.

Rationale:

- scalar-safety is record-local and must travel with the record into any
  future lookup, export, retrieval, answer, or calculator surface;
- a companion index creates join and drift risk before runtime lookup is
  stable;
- top-level status is easier for validators to require and for future
  consumers to carry forward.

This docs-only PR does not modify schemas. A future schema/export
implementation ExecPlan must update `current_fact_record.schema.json` or stop
with a documented blocker.

## Required Record Fields

The first lookup-ready current-fact export record must carry these fields:

- `record_id`;
- `character_slug`;
- `move_id`;
- `field_key`;
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

Additional fields may remain from the existing schema when already required,
including `display_label_ja`.

For the first export implementation, records admitted to the lookup-ready
export must have a reviewed `parsed_value`. Review-required values with no
parsed value should stay in parsed-value coverage and source-review artifacts,
not in the lookup-ready current-fact export. If later consumers need blocked
metadata for better hold messages, that should be a separate metadata export
or a schema-reviewed nullable parsed-value design.

## Allowed Source Inputs

The future export generator may use only reviewed public artifacts:

- parsed-value classifier coverage;
- official source-review artifacts;
- acquisition report hashes/counts;
- current-fact schemas;
- approved guard contracts and validators.

The export may include official records as `authority_candidate` only. It must
not promote current-fact authority by being present in the export.

SuperCombo records may be included only if their existing boundary remains
enforced:

- `source_name == "supercombo"` remains enrichment or cross-reference only;
- SuperCombo numeric values must not become numeric authority;
- SuperCombo values must not be used for exact scalar answers.

## Excluded Inputs

The future export generator must not use these as authority inputs:

- `.local` raw rows;
- raw HTML;
- screenshots;
- ChatGPT/VLM observations;
- full raw row dumps;
- cookies, profiles, headers, tokens, traces, debug dumps, logs, or private
  data;
- legacy `data/exports/<character>/official_raw.json` as an input source for
  the new export;
- SuperCombo numeric values as authority.

Legacy raw exports may be used by a later parity validator only as the current
technical-debt behavior being compared against. They must not appear in
`generated_from` for the new current-fact export.

## Validator Plan

The future export implementation must add validators before runtime lookup
changes. Required validator coverage:

- JSON Schema validation for the export artifact;
- schema validation for every record;
- closed `calculation_input_status` validation;
- `current_fact_guards.is_scalar_calculation_input` validation for any record
  that claims scalar lookup eligibility;
- rejection of `annotated_numeric_candidate` in exact scalar contexts;
- rejection of `frame_range` in exact scalar contexts;
- proof that `annotated_numeric_candidate.numeric_candidate` is not flattened
  into `integer`, `signed_frame`, or exact answer output;
- proof that `frame_range.start` and `frame_range.end` are not collapsed into a
  single frame value, best/worst value, or representative value;
- authority/source boundary validation for `source_name`, `source_role`,
  `authority_status`, `source_family`, `source_header_path`, and `evidence`;
- proof that `generated_from` excludes legacy `data/exports/*/official_raw.json`
  paths;
- proof that `.local`, raw HTML, screenshots, full raw rows, local paths,
  cookies, profiles, traces, debug dumps, logs, and private data are not
  committed into public artifacts.

Validators must be evidence-first. They may be grounded in current-fact
schemas, parsed-value classifier coverage, source-review artifacts, acquisition
report hashes/counts, synthetic contract fixtures, and privacy/security
boundaries. They must not be weakened to match generated output.

## Guard Contract

Any future exact scalar current-fact lookup must apply:

```python
is_scalar_calculation_input(parsed_value, calculation_input_status)
```

before returning a scalar answer value.

Rejected in exact scalar contexts:

- `calculation_input_status == "annotated_candidate_not_calculation_safe"`;
- `calculation_input_status ==
  "parsed_range_not_single_value_calculation_safe"`;
- `calculation_input_status == "review_required_not_calculation_safe"`;
- `calculation_input_status == "not_numeric_authority"`;
- missing or unknown `calculation_input_status`;
- `parsed_value.kind == "annotated_numeric_candidate"`;
- `parsed_value.kind == "frame_range"`;
- non-scalar parsed kinds such as `enum_token`, `ordered_pair`, and
  `raw_note`;
- records with no `parsed_value`.

Accepted scalar values still require authority/source/domain/unit checks in
later lookup code. The guard returning `True` is necessary but not sufficient
for daily-answer authority.

## Runtime Boundary

This design amendment does not authorize changing runtime lookup.

Before `current_facts.py` changes, a later implementation sequence must:

1. update schemas if required for top-level `calculation_input_status`;
2. implement the export generator and validators with no answer behavior
   change;
3. review the generated export artifact and public summary;
4. implement a parsed-value-backed lookup helper behind tests;
5. review parity, fallback, and evidence packet format;
6. only then change `current_facts.py` or `answering.py`.

During this sequence, daily-answer behavior must not broaden authority or
answer more exact numeric facts from parsed values.

## Debt Retirement Plan

Legacy `data/exports/<character>/official_raw.json` remains technical debt.

Retention reason:

- current dependent code path: `current_facts.py` and `answering.py`;
- replacement requirement: reviewed current-fact export, scalar guard,
  authority/source validation, and runtime parity;
- retirement blocker: no replacement export, lookup helper, parity validator,
  rollback criteria, or answer integration review exists yet.

Intended removal sequence:

1. Add schema/status-carrier change if approved.
2. Add reviewed current-fact export generator and validators.
3. Add lookup helper tests comparing safe key coverage where appropriate.
4. Switch runtime lookup in a reviewed PR.
5. Keep rollback to legacy raw lookup only as long as parity review requires.
6. Remove or demote legacy raw lookup and legacy raw export dependency in a
   final retirement PR.

No new code should treat `data/exports/<character>/official_raw.json` as a
stable API.

## Future Implementation Slices

Recommended next PRs:

1. Schema/status carrier ExecPlan or implementation PR.
   Add top-level `calculation_input_status` to the current-fact record schema
   and related fixtures/validators, or record a blocker if review rejects that
   design.
2. Current-fact export generator PR.
   Generate `data/current-facts/<run_id>-current-fact-export.json` and optional
   `docs/current-facts/<run_id>-current-fact-export.md` from reviewed public
   inputs only, with validators.
3. Export review PR.
   Review generated records, guard behavior, authority/source boundaries, and
   absence of legacy raw dependencies.
4. Parsed-value-backed lookup helper PR.
   Add helper/tests without changing `answering.py`.
5. Runtime switch plan and implementation PR.
   Switch exact current-fact lookup only after mandatory review.
6. Legacy raw retirement PR.
   Remove or demote the old raw lookup once replacement parity and rollback
   criteria are satisfied.

## Acceptance Criteria

- The ExecPlan is docs-only.
- The ExecPlan chooses `data/current-facts/<run_id>-current-fact-export.json`
  as the future immutable export path direction.
- The ExecPlan chooses top-level `calculation_input_status` as the preferred
  first status-carrier design.
- The ExecPlan lists required record fields for lookup-ready records.
- The ExecPlan lists allowed and excluded inputs.
- The ExecPlan requires schema, guard, authority/source, privacy, and
  no-legacy-raw-dependency validators.
- The ExecPlan keeps `annotated_numeric_candidate` from being flattened.
- The ExecPlan keeps `frame_range` from being collapsed.
- The ExecPlan records legacy `official_raw.json` as technical debt with
  retention reason, replacement requirement, retirement blocker, and intended
  removal sequence.
- No runtime, schema, generated artifact, retrieval, answer, export,
  calculator, parser, classifier, SymPy, or live acquisition changes are made.
- Validation commands pass.

## Files / Interfaces

This docs-only plan changes only:

- `docs/execplans/2026-05-25-current-fact-export-design-amendment.md`

Future implementation plans may touch, after review:

- `contracts/current-facts/current_fact_record.schema.json`;
- current-fact schema fixtures and validators;
- current-fact export generator code;
- `data/current-facts/<run_id>-current-fact-export.json`;
- `docs/current-facts/<run_id>-current-fact-export.md`;
- focused validators and tests.

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
  `plan/current-fact-export-design-amendment`.
- [x] (2026-05-25 JST) Inspected PR #350 transition ExecPlan, current-fact
  schemas, and `current_fact_guards.is_scalar_calculation_input`.
- [x] (2026-05-25 JST) Drafted this docs-only design amendment ExecPlan.
- [x] (2026-05-25 JST) Validation passed: `git diff --check`,
  `uv lock --check`, clean-slate validator, parsed-value classifier coverage
  validator, and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Use `data/current-facts/<run_id>-current-fact-export.json` as the
  future immutable export path direction.
  Rationale: It separates reviewed current-fact exports from legacy raw
  `data/exports/` technical debt and avoids a mutable runtime pointer in the
  first implementation.
  Date/Author: 2026-05-25 / Codex

- Decision: Prefer top-level `calculation_input_status` on current-fact
  records over a companion index.
  Rationale: Scalar-safety is record-local, and top-level schema validation
  avoids join drift before runtime lookup is stable.
  Date/Author: 2026-05-25 / Codex

- Decision: Require `parsed_value` for lookup-ready records in the first
  current-fact export.
  Rationale: The replacement for exact current-fact lookup must not recreate
  raw-value answer behavior under a new filename.
  Date/Author: 2026-05-25 / Codex

- Decision: Exclude legacy `official_raw.json` from `generated_from`.
  Rationale: The new export must not depend on the technical-debt surface it
  is intended to replace. Legacy raw exports may only be used in later parity
  validation.
  Date/Author: 2026-05-25 / Codex

- Decision: Keep SymPy out of scope.
  Rationale: This plan defines export/schema/lookup boundaries, not
  arithmetic.
  Date/Author: 2026-05-25 / Codex

## Deviations

- None.

## Remaining Risks

- Top-level `calculation_input_status` still requires a future schema change
  and review.
- The exact enum list for `calculation_input_status` must be fixed in the
  schema implementation PR.
- The first export may have limited lookup coverage because review-required
  raw values without `parsed_value` are not admitted to lookup-ready records.
- No runtime lookup helper or parity validator exists yet.
- `current_facts.py` remains backed by legacy raw export data until later
  reviewed PRs land.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only export design amendment | Drafted design for future current-fact export path, status carrier, source boundaries, validators, and debt retirement | `docs/execplans/2026-05-25-current-fact-export-design-amendment.md` | `git diff --check`; `uv lock --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch` | Passed | None | Review pending | Future implementation still required |
| Export path decision | Chose `data/current-facts/<run_id>-current-fact-export.json` as future immutable JSON path direction with optional docs summary | This ExecPlan only | Diff/status review | Passed | None | Review pending | Runtime active-manifest design remains future work |
| Status carrier decision | Preferred top-level `calculation_input_status` over companion index | This ExecPlan only | Diff/status review | Passed | None | Future schema change required | Enum list must be reviewed |
| Source and validator boundaries | Defined allowed/excluded inputs and validator expectations for schema, guard, authority/source, privacy, and no legacy raw dependency | This ExecPlan only | Diff/status review | Passed | None | Review pending | Export generator not implemented |
| Scope exclusions | Kept runtime/schema/generated artifact/retrieval/answer/export/calculator/parser/classifier/SymPy/live acquisition changes out of scope | This ExecPlan only | Diff/status review | Passed | None | Review pending | None for docs-only PR |

## Next Reviewer Prompt

```text
Review docs/execplans/2026-05-25-current-fact-export-design-amendment.md.

Check:
- PR diff contains exactly one ExecPlan file.
- The plan is docs-only and includes no runtime/schema/generated artifact/
  retrieval/answer/export/calculator/parser/classifier/SymPy/live acquisition
  changes.
- Export path direction is `data/current-facts/<run_id>-current-fact-export.json`
  with optional `docs/current-facts/<run_id>-current-fact-export.md`.
- `calculation_input_status` is planned as a top-level current-fact record
  field unless implementation review finds a schema blocker.
- Required lookup record fields include record/source/authority/evidence/raw/
  parsed/value_shape/calculation status fields.
- Allowed inputs are reviewed public artifacts only.
- Excluded inputs include `.local` raw rows, raw HTML, screenshots/VLM as
  authority, legacy `official_raw.json` as source input, and SuperCombo
  numeric authority.
- Validator plan covers schema validation, scalar guard validation,
  authority/source boundaries, no flattened annotated_numeric_candidate, no
  collapsed frame_range, and no legacy raw export dependency.
- Legacy `official_raw.json` is treated as technical debt with retention
  reason, replacement requirement, retirement blocker, and intended removal
  sequence.

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
