# Value-Shape Review Item Disposition

Status: Drafted for review.

## Purpose

Plan review disposition for all 247 grouped value-shape review items before
current-fact JSON Schema redesign.

This corrected ExecPlan explicitly depends on the SuperCombo canonical field
mapping review for the 403 SuperCombo field summaries. The 247 review item
groups are value-shape and expression blockers. They do not cover all 403
SuperCombo field summaries and must not be treated as a substitute for
SuperCombo field mapping.

This ExecPlan is docs-only. It does not implement schemas, parsers,
classifiers, normalized exports, retrieval changes, answer behavior, runtime
behavior, data artifacts, or authority promotion.

JSON Schema redesign remains blocked until both are reviewed:

- SuperCombo 403 field-summary canonical mapping review;
- all 247 grouped value-shape review item dispositions.

## Scope

Included:

- Plan disposition coverage for every grouped review item emitted by the
  latest value-shape inventory.
- Define required disposition categories.
- Define required per-review-item fields.
- Define dependency on SuperCombo canonical field mapping review.
- Define future public disposition artifact shape.
- Preserve official and SuperCombo source boundaries.
- Preserve authority boundaries.
- Define validation expectations for a later disposition implementation.

Excluded:

- Do not implement JSON Schema redesign.
- Do not implement parser or classifier code.
- Do not implement normalized export.
- Do not change retrieval or answer behavior.
- Do not modify runtime code.
- Do not modify existing data artifacts in this planning step.
- Do not run live official or SuperCombo acquisition.
- Do not use `solve_cloudflare=True`.
- Do not promote official data to current-fact authority.
- Do not promote SuperCombo beyond enrichment, cross-reference, or candidate
  evidence.
- Do not commit `.local/`, `.venv/`, `.agents/`, raw HTML, raw rows,
  screenshots, cookies, browser profiles, traces, debug dumps, answer logs,
  training logs, private data, or ignored local artifacts.

## Acceptance Criteria

- The plan names the exact input inventory JSON and Markdown artifacts.
- The plan names the SuperCombo canonical mapping and normalized mapping policy
  dependencies.
- The plan states that 247 review item dispositions do not cover all 403
  SuperCombo field summaries.
- The plan covers all 247 grouped review item groups.
- The plan defines the required disposition categories.
- The plan defines required fields for each disposition record.
- The plan uses `inventory_source_family` for the inventory source identity.
- The plan keeps normalized-layer `source_family` as a semantic category and
  does not confuse it with official/SuperCombo source identity.
- The plan decides future disposition output should be both Markdown and JSON.
- The plan keeps official and SuperCombo separate.
- The plan keeps official as authority candidate only.
- The plan keeps SuperCombo as enrichment/cross-reference/candidate only.
- The plan forbids numeric authority promotion.
- The plan forbids parser/schema/runtime/retrieval/answer implementation.
- The plan keeps JSON Schema redesign blocked until both required reviews are
  complete.
- Planning validation passes.

## Files / Interfaces

Created in this step:

- `docs/execplans/2026-05-23-value-shape-review-item-disposition.md`

Required input inventory artifacts:

- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md`

Required dependency plans:

- `docs/execplans/2026-05-23-supercombo-canonical-field-mapping-review.md`
- `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md`

Reference plans:

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md`

Future disposition output should be both Markdown and JSON:

- Markdown review table:
  `docs/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition.md`
- JSON summary:
  `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`

Rationale:

- Markdown supports human review of 247 grouped items and rationale.
- JSON supports deterministic coverage validation and later schema/classifier
  planning.
- Both together match the inventory and SuperCombo mapping artifact pattern.

This ExecPlan does not create those future artifacts.

## Input Inventory Facts

The input inventory run is:

```text
20260521T025403Z
```

Review item summary:

- grouped review item count: 247
- emitted review item count: 247
- omitted review item count: 0
- truncated: false

Review items by inventory source family:

- official: 16
- SuperCombo: 231

Review items by kind:

- `unclassified_expression`: 234
- `source_specific_expression`: 12
- `malformed_looking_source_value`: 1

Review items by source and kind:

- official `source_specific_expression`: 12
- official `unclassified_expression`: 3
- official `malformed_looking_source_value`: 1
- SuperCombo `unclassified_expression`: 231

SuperCombo field mapping scope:

- SuperCombo field summaries: 403
- SuperCombo review item groups: 231

The 231 SuperCombo review item groups are a subset of value-shape issues. They
do not cover every SuperCombo field summary. Canonical field mapping for all
403 SuperCombo field summaries remains a separate prerequisite.

## Dependency Gate

This disposition plan depends on two prior policy surfaces:

1. Normalized field mapping and classifier policy
   - defines source-native labels versus future English canonical keys;
   - separates `field_key`, `source_label`, `source_header_path`,
     normalized-layer semantic `source_family`, `source_name`, `source_role`,
     `display_label_ja`, `raw_value`, `parsed_value`, `value_shape`, and
     `authority_status`.

2. SuperCombo canonical field mapping review
   - defines mapping review for all 403 SuperCombo field summaries;
   - defines how SuperCombo fields map to official field keys, SuperCombo
     source-specific keys, enrichment-only context, out-of-scope deferrals, or
     blocked human review.

Future disposition implementation must use SuperCombo mapping outputs when a
SuperCombo review item needs `proposed_field_key`.

If SuperCombo mapping is incomplete:

- SuperCombo review items may still be dispositioned as
  `blocked_pending_source_review` or
  `out_of_scope_first_normalized_export`;
- SuperCombo review items must not invent `proposed_field_key` values by
  string similarity;
- JSON Schema redesign remains blocked.

## Terminology Boundary

Use `inventory_source_family` for the inventory source identity:

```text
official | supercombo
```

Do not use inventory `source_family` as the future normalized-layer semantic
category.

In the future normalized layer:

- `source_name` identifies origin, such as `official` or `supercombo`;
- `source_role` identifies evidence role, such as `authority_candidate`,
  `enrichment_candidate`, or `cross_reference_candidate`;
- normalized-layer `source_family` is a semantic category, such as `timing`,
  `advantage`, `damage`, `gauge`, `cancel`, `attribute`, `note`, `mobility`,
  `vital`, or `metadata`.

This separation prevents official/SuperCombo source identity from being mixed
with field semantics.

## Disposition Categories

Every review item must receive exactly one disposition:

1. `parse_rule_required_before_schema`
   - The value shape is required for the first normalized schema and needs a
     deterministic parse rule before schema implementation.
   - This is common for frame, damage, gauge, scaling, or advantage values
     whose shape cannot be represented by simple scalar parsing.

2. `schema_supports_raw_only`
   - The first schema should preserve the value as raw-only with no
     `parsed_value`.
   - This is appropriate for remarks, prose, or audit values that are needed
     but not part of deterministic numeric answers.

3. `source_specific_enum_required`
   - The value belongs to a finite source-specific category set that needs a
     reviewed enum before parser/schema work.
   - This is appropriate for cancel, guard, armor, invulnerability, airborne,
     attribute, or source marker values when they are finite categories.

4. `out_of_scope_first_normalized_export`
   - The review item belongs to a field or source area intentionally deferred
     from the first normalized export.
   - This requires a rationale and must not hide source drift.

5. `blocked_pending_source_review`
   - The review item cannot be safely dispositioned without additional source,
     domain, or mapping review.
   - This is the default for malformed-looking values, ambiguous source
     semantics, or unresolved SuperCombo mappings needed by first export.

No disposition may imply numeric authority promotion.

## Required Disposition Fields

Each future disposition record must include:

```yaml
review_item_disposition:
  review_item_id: string
  run_id: "20260521T025403Z"
  inventory_source_family: official | supercombo
  source_name: official | supercombo
  source_role: authority_candidate | enrichment_candidate | cross_reference_candidate
  source_header_path: [string]
  source_label: string
  proposed_field_key: string | null
  review_kind: unclassified_expression | source_specific_expression | malformed_looking_source_value
  shape_classes: [string]
  affected_count: integer
  representative_examples:
    - raw_value: string # omitted when truncated
      raw_value_excerpt: string
      raw_value_sha256: string
      raw_value_length: integer
      raw_value_truncated: boolean
  disposition: parse_rule_required_before_schema | schema_supports_raw_only | source_specific_enum_required | out_of_scope_first_normalized_export | blocked_pending_source_review
  rationale: string
  json_schema_redesign_blocked: boolean
  supercombo_mapping_dependency: string | null
  next_execplan_needed: string | null
  reviewer_notes: string
```

Rules:

- `inventory_source_family` is copied from the inventory and is either
  `official` or `supercombo`.
- `source_name` identifies the origin and must match the source.
- official `source_role` remains `authority_candidate`.
- SuperCombo `source_role` remains `enrichment_candidate` or
  `cross_reference_candidate`.
- `source_header_path` and `source_label` remain source-native.
- `proposed_field_key` may be null when mapping is unknown or not applicable.
- `supercombo_mapping_dependency` is required for SuperCombo review items when
  `proposed_field_key` depends on the 403-field mapping review.
- long examples must remain excerpt/hash/length metadata and must not expose
  full source prose.
- `json_schema_redesign_blocked` must be true when a parse rule, enum, source
  review, or SuperCombo mapping decision is required before schema redesign.

## Official Disposition Policy

Official review items must be treated with high priority because official is
the future authority candidate source.

Policy:

- official remains `source_name: official`;
- official remains `source_role: authority_candidate`;
- official is not `current_fact_authority` in this work;
- official numeric/current fields should usually become
  `parse_rule_required_before_schema` or
  `blocked_pending_source_review`;
- official categorical values may become `source_specific_enum_required`;
- official remarks/prose may become `schema_supports_raw_only`;
- malformed-looking official values default to
  `blocked_pending_source_review`;
- official Japanese labels must remain source-native in the disposition
  artifact.

## SuperCombo Disposition Policy

SuperCombo remains enrichment, cross-reference, or candidate evidence only.

Policy:

- SuperCombo remains `source_name: supercombo`;
- SuperCombo remains `source_role: enrichment_candidate` or
  `cross_reference_candidate`;
- SuperCombo must not become daily-answer numeric authority;
- SuperCombo review items must not invent canonical keys before mapping review;
- SuperCombo review items may reference mapping IDs or unresolved mapping
  blockers from the 403-field mapping review;
- SuperCombo fields out of first export may be
  `out_of_scope_first_normalized_export`;
- SuperCombo enrichment-only values may be `schema_supports_raw_only` when the
  future schema explicitly supports raw-only enrichment context;
- ambiguous SuperCombo values remain `blocked_pending_source_review`.

The 231 SuperCombo value-shape review item groups do not replace review of all
403 SuperCombo field summaries.

## JSON Schema Redesign Gate

JSON Schema redesign remains blocked until:

- all 403 SuperCombo field summaries have reviewed canonical mapping status;
- all 247 grouped value-shape review items have one reviewed disposition;
- every disposition artifact passes validation;
- official and SuperCombo remain separated;
- every `parse_rule_required_before_schema` item has a follow-up parser or
  classifier policy decision;
- every `source_specific_enum_required` item has a follow-up enum design
  decision;
- every `blocked_pending_source_review` item is resolved or explicitly scoped
  out of the first normalized export;
- every `out_of_scope_first_normalized_export` item has rationale;
- reviewer confirms the combined mapping and disposition surfaces are complete.

This disposition work may reduce schema risk, but it does not itself implement
JSON Schema redesign.

## Future Validation Strategy

The later disposition implementation should validate:

- input inventory run ID is `20260521T025403Z`;
- input review item count is exactly 247;
- every input review item has exactly one disposition;
- no duplicate review item IDs;
- all required fields are present;
- `inventory_source_family` is used instead of normalized-layer
  `source_family`;
- disposition value is one of the approved categories;
- `source_name` and `source_role` preserve source boundaries;
- official is not promoted to `current_fact_authority`;
- SuperCombo is not promoted beyond enrichment/cross-reference/candidate;
- SuperCombo review items that need `proposed_field_key` reference the
  SuperCombo mapping review output;
- long examples remain excerpt/hash/length metadata;
- no raw HTML, full raw rows, full source table dumps, local paths, cookies,
  secrets, screenshots, traces, answer logs, training logs, or private data
  appear in public artifacts.

The future implementation should also provide a review summary:

```yaml
disposition_summary:
  run_id: "20260521T025403Z"
  total_review_items: 247
  disposition_counts:
    parse_rule_required_before_schema: integer
    schema_supports_raw_only: integer
    source_specific_enum_required: integer
    out_of_scope_first_normalized_export: integer
    blocked_pending_source_review: integer
  official_count: integer
  supercombo_count: integer
  supercombo_mapping_dependency_count: integer
  json_schema_redesign_blocked_count: integer
```

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Confirmed `main` and `origin/main` are at
  `f35336ee7fd3d1f4e45f735b2b6618c606dbfea4`.
- [x] (2026-05-23 JST) Confirmed the superseded draft under `/tmp` was not
  restored as-is.
- [x] (2026-05-23 JST) Created branch
  `plan/value-shape-review-item-disposition-corrected`.
- [x] (2026-05-23 JST) Read latest inventory review item counts and
  SuperCombo field summary count from the JSON summary.
- [x] (2026-05-23 JST) Drafted this corrected docs-only ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Make this disposition plan depend explicitly on SuperCombo 403
  field-summary mapping review.
  Rationale: SuperCombo review item dispositions may need `proposed_field_key`,
  and that cannot be guessed before canonical mapping review.
  Date/Author: 2026-05-23 / Codex

- Decision: Use `inventory_source_family` instead of `source_family` in
  disposition records.
  Rationale: The inventory uses `official` and `supercombo` as source family
  labels, while the normalized layer reserves `source_family` for semantic
  categories.
  Date/Author: 2026-05-23 / Codex

- Decision: Future disposition output should be both Markdown and JSON.
  Rationale: Markdown supports human review of 247 groups, while JSON supports
  deterministic coverage validation and later schema/classifier planning.
  Date/Author: 2026-05-23 / Codex

- Decision: Require exactly one disposition per grouped review item.
  Rationale: Multiple dispositions would make schema gating ambiguous; missing
  dispositions would hide blockers.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- The actual disposition for each of the 247 review item groups.
- Which official review items block the first normalized schema.
- Which SuperCombo review items depend on a completed canonical field mapping.
- Which SuperCombo review items are out of scope for the first normalized
  export.
- Which source-specific enum sets must be designed before schema work.
- Which parse rules are required before schema versus deferred parser work.
- Exact future artifact paths may be adjusted during implementation review if
  the proposed paths conflict with repository organization.

## Deviations

- None.

## Risks

- Dispositioning SuperCombo items before the 403-field mapping review is
  complete could create unstable `proposed_field_key` values.
- Marking too many items raw-only could defer important parser decisions and
  leave JSON Schema under-specified.
- Marking too many items as schema blockers could delay a useful first
  normalized export.
- Long example context is summarized; reviewers may need to consult the
  source inventory or ignored local artifacts for full context.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan corrected review item disposition | Drafted docs-only ExecPlan | `docs/execplans/2026-05-23-value-shape-review-item-disposition.md` | `git diff --check` | Pass | None | Mandatory review pending | 247 item dispositions not yet assigned |
| Preserve mapping dependency | SuperCombo 403 mapping review is explicit prerequisite | ExecPlan only | reviewer check | Pending | None | SuperCombo mapping output not implemented | Proposed field keys may be unavailable |
| Preserve source boundaries | Uses `inventory_source_family`; official and SuperCombo remain separate | ExecPlan only | reviewer check | Pending | None | Future disposition implementation needed | None |
| Keep JSON Schema blocked | Disposition gate and SuperCombo mapping gate explicitly block schema redesign | ExecPlan only | reviewer check | Pending | None | All dispositions unresolved | Schema work must wait |
