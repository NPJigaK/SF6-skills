# Current-Fact JSON Schema Redesign

Status: Reviewed; ready for docs-only PR.

## Purpose

Plan the first current-fact JSON Schema redesign after the latest-source
inventory, SuperCombo mapping, value-shape disposition, classifier/enum
policy, validator/test evidence audit, and data-surface cleanup work.

This is a planning-only ExecPlan. It does not add schema files, parser code,
classifier code, normalized exports, generated DB files, retrieval behavior, or
answer behavior.

## Scope

Included:

- Define the schema artifact boundary for normalized current-fact records.
- Define how raw source labels, English canonical keys, value shapes, parser
  policy, and authority status remain separated.
- Decide the JSON Schema dialect candidate for later schema artifacts.
- Define fixture and validator requirements for the schema implementation
  ExecPlan.
- Preserve validator/test evidence limits from the validator audit.

Excluded:

- No JSON Schema files are created in this step.
- No parser/classifier implementation.
- No normalized export generation.
- No source acquisition or live web access.
- No retrieval DB work.
- No answer behavior changes.
- No SuperCombo numeric authority promotion.
- No private vault, overlay DB, Discord, VLM, vector search, API fallback, or
  `sf6 ask`.

## Inputs

Approved local inputs:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md`
- `docs/execplans/2026-05-23-supercombo-field-mapping-artifacts.md`
- `docs/execplans/2026-05-23-value-shape-review-item-disposition.md`
- `docs/execplans/2026-05-23-parsed-value-classifier-and-enum-policy.md`
- `docs/execplans/2026-05-23-validator-test-fact-source-audit.md`
- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`

External standards reference:

- JSON Schema official specification says the current version/meta-schema is
  `2020-12`, so later schema artifacts should use
  `https://json-schema.org/draft/2020-12/schema` unless implementation review
  finds a toolchain blocker.

## Schema Artifact Boundary

The later implementation ExecPlan should add schema artifacts only under a
new, explicit schema surface. Proposed paths:

```text
contracts/current-facts/current_fact_record.schema.json
contracts/current-facts/parsed_value.schema.json
contracts/current-facts/value_shape.schema.json
contracts/current-facts/source_reference.schema.json
contracts/current-facts/current_fact_export.schema.json
tests/fixtures/current-facts/
tests/validation/validate_current_fact_schemas.py
docs/schema-reviews/20260521T025403Z-current-fact-json-schema-redesign.md
```

The schema implementation must not write normalized data exports. Schema
fixtures should be minimal synthetic or source-derived examples selected for
coverage, not full source dumps.

## Record Design Rules

`current_fact_record` must separate these concerns:

| Field | Requirement |
| --- | --- |
| `record_id` | Stable generated identifier; no user/private data. |
| `character_slug` | Character-agnostic slug from reviewed roster/source data. |
| `move_id` | Stable move identifier when available; absent or null only by explicit schema rule. |
| `field_key` | English canonical key from reviewed mapping artifacts. |
| `source_label` | Source-native leaf label, not translated. |
| `source_header_path` | Source-native header path, not normalized. |
| `source_family` | Semantic category such as `timing`, `advantage`, `damage`, `gauge`, `metadata`, `mobility`, `throw`, `defense`; never `official` or `supercombo`. |
| `source_name` | Source identity such as `official` or `supercombo`. |
| `source_role` | Evidence role such as `authority_candidate`, `cross_reference_candidate`, or `enrichment_candidate`. |
| `display_label_ja` | Japanese display label for UI/answer rendering; not a source identity field. |
| `raw_value` | Exact source value as preserved by the source artifact. |
| `value_shape` | Deterministic shape metadata from reviewed inventory/policy. |
| `parsed_value` | Optional; allowed only for policy-approved parser outputs. |
| `authority_status` | Explicit answer boundary; schema does not promote authority. |
| `evidence` | Public source/reference metadata only; no local paths, screenshots, cookies, browser profiles, raw HTML, or row dumps. |

Every normalized fact must preserve `raw_value` even when `parsed_value` is
present.

## Parsed Value Boundary

`parsed_value` must be discriminated by a required `kind` field. The first
schema should support only shapes covered by the approved policy artifact and
fixtures.

Candidate `kind` values for the schema implementation review:

- `integer`
- `decimal`
- `signed_frame`
- `frame_range`
- `ordered_pair`
- `percent`
- `gauge_amount`
- `enum_token`
- `raw_note`

The schema may include `raw_preserved` or omit `parsed_value` for unsupported
or raw-only records. It must not infer totals, arithmetic, or semantic meaning
unless a reviewed parser policy and fixture approve that representation.

## Authority And Source Rules

- Official records may be `authority_candidate`; they are not
  `current_fact_authority` until a later normalized export and answer-runtime
  ExecPlan promotes them.
- SuperCombo records remain `enrichment_candidate` or
  `cross_reference_candidate`.
- SuperCombo records must not be daily-answer numeric authority.
- Policy-derived and artifact-consistency validators cannot be cited as source
  truth. The validator audit remains binding.
- Source-native labels must stay source-native; English canonical keys are
  additional normalized-layer fields.

## Fixture Requirements

The later schema implementation must include fixtures covering at least:

- official scalar values;
- official signed frame values;
- official frame ranges and malformed-looking source values;
- official note-bearing move names and raw-only remarks;
- official categorical/enumerated fields;
- SuperCombo mapped cross-reference fields;
- SuperCombo source-specific enrichment fields;
- SuperCombo ordered-pair vitals/mobility review case;
- out-of-scope records that are excluded from first normalized export.

Fixtures must be small. They must not include full raw HTML, full raw rows, full
source table dumps, screenshots, cookies, browser profiles, traces, debug
dumps, answer logs, training logs, private vault references, or real user data.

## Validator Requirements

The later schema implementation must include a validator that:

- validates every schema against the chosen JSON Schema meta-schema;
- validates all fixtures;
- rejects `source_family` values that use source identity like `official` or
  `supercombo`;
- rejects SuperCombo numeric authority promotion;
- rejects `parsed_value` without a policy-approved `kind` and parser rule;
- rejects public evidence containing local paths, raw HTML, row dumps,
  screenshots, cookies, browser profiles, traces, secrets, answer logs,
  training logs, or private data;
- is itself recorded in the validator/test evidence audit.

## Acceptance Criteria

- This ExecPlan records the schema redesign boundary without implementation.
- JSON Schema `2020-12` is selected as the dialect candidate, with a later
  implementation check required before schema files are committed.
- Raw/source/canonical/display/authority fields are separated.
- `parsed_value` is optional and policy-gated.
- Official and SuperCombo authority boundaries remain unchanged.
- Fixture and validator requirements are explicit.
- JSON Schema implementation remains a later ExecPlan.
- Planning validation passes.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Confirmed local `main` is at
  `dd2325a02f71a4352d8db9ec35f41eee668b4f8f`.
- [x] (2026-05-23 JST) Created fresh branch
  `plan/current-fact-json-schema-redesign-20260523` because the older
  `plan/current-fact-json-schema-redesign` branch is stale and unsafe to reuse.
- [x] (2026-05-23 JST) Reviewed local prerequisite artifacts and counts:
  247 disposition records, 224 policy-covered parser/enum blockers, 403
  SuperCombo mapping records, and 12 audited test/validator files.
- [x] (2026-05-23 JST) Checked official JSON Schema documentation and selected
  Draft 2020-12 as the dialect candidate for the later schema implementation.
- [x] (2026-05-23 JST) Drafted this planning ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py`,
  and new-file whitespace check.
- [x] (2026-05-23 JST) Completed reviewer check: docs-only plan, no schema
  implementation, no parser/classifier/export/retrieval/answer changes, no
  authority promotion.

## Decision Log

- Decision: Create a fresh branch instead of reusing the stale
  `plan/current-fact-json-schema-redesign` branch.
  Rationale: The old branch predates the clean-slate data cleanup and would
  reintroduce deleted legacy data and remove current artifacts.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat JSON Schema Draft 2020-12 as the dialect candidate.
  Rationale: The official JSON Schema specification page identifies 2020-12 as
  the current version/meta-schema.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep this step planning-only.
  Rationale: Schema files, fixtures, and validators are multiple-file changes
  that need a focused implementation ExecPlan and review.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- The schema implementation could overclaim parser correctness if it ignores
  the validator/test evidence audit.
- The first schema may need to support raw-only records for values whose
  parser semantics are still intentionally conservative.
- JSON Schema validator tooling choice is not approved by this ExecPlan.
- Historical docs still say schema redesign was blocked before the later
  mapping/disposition/policy/audit work landed.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan schema redesign | Defined schema artifact boundary and field separation | This ExecPlan | reviewer check | Pass | None | Schema files not implemented | Later implementation must stay policy-gated |
| Preserve authority boundary | Official remains candidate; SuperCombo remains enrichment/cross-reference | This ExecPlan | reviewer check | Pass | None | No runtime promotion | Misuse would affect daily answers |
| Preserve validator rigor | Validator audit remains binding for later schema validator | This ExecPlan | `validate_validator_test_audit.py` | Pass | None | Later validator not implemented | Overclaiming remains possible if ignored |
