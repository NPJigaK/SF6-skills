# Value-Shape Review Item Disposition

Status: Implementation complete; review pending.

## Purpose

Plan review disposition for all 247 grouped value-shape review items before
current-fact JSON Schema redesign.

This corrected ExecPlan explicitly depends on the SuperCombo canonical field
mapping review for the 403 SuperCombo field summaries. The 247 review item
groups are value-shape and expression blockers. They do not cover all 403
SuperCombo field summaries and must not be treated as a substitute for
SuperCombo field mapping.

This ExecPlan now implements the review disposition artifacts for all 247
grouped value-shape review items. It does not implement schemas, parsers,
classifiers, normalized exports, retrieval changes, answer behavior, daily
runtime behavior, or authority promotion.

JSON Schema redesign remains blocked until both are reviewed:

- SuperCombo 403 field-summary canonical mapping review;
- all 247 grouped value-shape review item dispositions.

## Scope

Included:

- Implement disposition coverage for every grouped review item emitted by the
  latest value-shape inventory.
- Define required disposition categories.
- Define required per-review-item fields.
- Define dependency on SuperCombo canonical field mapping review.
- Create public Markdown and JSON disposition artifacts.
- Add a deterministic generator and validator for the disposition artifacts.
- Add focused tests for coverage, source boundaries, authority boundaries, and
  public example limits.
- Preserve official and SuperCombo source boundaries.
- Preserve authority boundaries.
- Define validation expectations for later schema/classifier planning.

Excluded:

- Do not implement JSON Schema redesign.
- Do not implement parser or classifier code.
- Do not implement normalized export.
- Do not change retrieval or answer behavior.
- Do not change daily-answer runtime behavior.
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
- The implementation assigns exactly one disposition to each of the 247 grouped
  review item groups.
- The implementation produces Markdown and JSON public artifacts.
- The implementation validates coverage, status exclusivity, source boundaries,
  authority boundaries, SuperCombo mapping dependencies, and public example
  limits.
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

Created in the planning step:

- `docs/execplans/2026-05-23-value-shape-review-item-disposition.md`

Created in the implementation step:

- `src/sf6_knowledge_coach/value_shape_disposition.py`
- `tests/test_value_shape_disposition.py`
- `tests/validation/validate_value_shape_disposition.py`
- `docs/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition.md`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`

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

Disposition output is both Markdown and JSON:

- Markdown review table:
  `docs/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition.md`
- JSON summary:
  `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`

Rationale:

- Markdown supports human review of 247 grouped items and rationale.
- JSON supports deterministic coverage validation and later schema/classifier
  planning.
- Both together match the inventory and SuperCombo mapping artifact pattern.

These artifacts are public summaries only. They do not contain raw HTML, full
raw rows, full source table dumps, screenshots, local paths, cookies, browser
profiles, traces, debug dumps, answer logs, training logs, or private data.

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

Implemented disposition summary:

- total dispositions: 247
- official dispositions: 16
- SuperCombo dispositions: 231
- `parse_rule_required_before_schema`: 208
- `source_specific_enum_required`: 16
- `schema_supports_raw_only`: 6
- `out_of_scope_first_normalized_export`: 17
- `blocked_pending_source_review`: 0
- SuperCombo mapping dependencies: 231
- JSON Schema redesign blocked records: 224

Resolved source-review items:

- official `動作フレーム > 持続` malformed-looking value group;
- official `技名` note-bearing move-name variant group;
- SuperCombo `Character Vitals > Throw Range / Hurtbox`.

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

This disposition implementation uses SuperCombo mapping outputs when a
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

## Validation Strategy

The disposition implementation validates:

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

The implementation also provides a review summary:

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
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_inventory.py
PYTHONPATH=src uv run --locked python tests/validation/validate_supercombo_field_mapping.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.value_shape_disposition build
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_disposition.py
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
- [x] (2026-05-23 JST) Created implementation branch
  `impl/value-shape-review-item-disposition`.
- [x] (2026-05-23 JST) Implemented deterministic disposition generator and
  validator.
- [x] (2026-05-23 JST) Generated Markdown and JSON disposition artifacts.
- [x] (2026-05-23 JST) Added focused disposition tests and validation script.
- [ ] Complete mandatory implementation review.

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

- Decision: Disposition output should be both Markdown and JSON.
  Rationale: Markdown supports human review of 247 groups, while JSON supports
  deterministic coverage validation and later schema/classifier planning.
  Date/Author: 2026-05-23 / Codex

- Decision: Require exactly one disposition per grouped review item.
  Rationale: Multiple dispositions would make schema gating ambiguous; missing
  dispositions would hide blockers.
  Date/Author: 2026-05-23 / Codex

- Decision: Consume source-review resolutions for official malformed-looking
  `動作フレーム > 持続`, official note-bearing `技名`, and SuperCombo
  `Character Vitals > Throw Range / Hurtbox`.
  Rationale: Source review resolved those items enough for disposition:
  active-frame notation and the SuperCombo pair need parser policy; note-bearing
  move names can remain raw-only in the first schema.
  Date/Author: 2026-05-23 / Codex

- Decision: Mark source-specific cancel/attribute/guard/defense categorical
  groups as `source_specific_enum_required`.
  Rationale: They are finite source-native categories and need reviewed enum
  design before parser/schema work.
  Date/Author: 2026-05-23 / Codex

- Decision: Mark notes/prose enrichment groups as
  `schema_supports_raw_only`.
  Rationale: They should be preserved for review context without emitting
  parsed values or numeric authority.
  Date/Author: 2026-05-23 / Codex

- Decision: Mark mapped numeric/current-fact-like special shapes as
  `parse_rule_required_before_schema`.
  Rationale: Parentheses, brackets, ranges, note markers, knockdown notation,
  gauge variants, and other expression shapes require deterministic parse or
  classifier policy before normalized schema work.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Exact parse/classifier rules for the 208
  `parse_rule_required_before_schema` groups.
- Exact enum design for the 16 `source_specific_enum_required` groups.
- Whether any of the 17 `out_of_scope_first_normalized_export` groups should be
  pulled into a later normalized export.
- Whether the 6 `schema_supports_raw_only` groups need additional display or
  review-context schema fields.

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
- JSON Schema redesign remains blocked because 224 disposition records still
  require parse/classifier or enum follow-up before schema work.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Implement review item disposition | Generated 247 disposition records | `src/sf6_knowledge_coach/value_shape_disposition.py`, disposition artifacts | `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.value_shape_disposition build` | Pass | None | Mandatory review pending | 224 records still block schema redesign |
| Validate coverage and boundaries | Added validator and tests | `tests/test_value_shape_disposition.py`, `tests/validation/validate_value_shape_disposition.py` | `PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_disposition.py` | Pass | None | Mandatory review pending | None |
| Preserve mapping dependency | SuperCombo 231 review items reference mapping IDs | disposition JSON/Markdown | validator | Pass | None | None | SuperCombo remains non-authority |
| Preserve source boundaries | Uses `inventory_source_family`; official and SuperCombo remain separate | disposition JSON/Markdown | validator | Pass | None | None | None |
| Keep JSON Schema blocked | Disposition gate and SuperCombo mapping gate block schema redesign | ExecPlan and disposition artifacts | reviewer check | Pending | None | Parser/enum/source-review follow-ups unresolved | Schema work must wait |
