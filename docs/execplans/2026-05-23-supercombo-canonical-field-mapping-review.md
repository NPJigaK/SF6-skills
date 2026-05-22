# SuperCombo Canonical Field Mapping Review

Status: Drafted for review.

## Purpose

Plan review of all 403 SuperCombo field summaries before current-fact JSON
Schema redesign and before final value-shape review-item disposition.

This ExecPlan is docs-only. It does not implement schemas, parsers,
classifiers, normalized exports, retrieval changes, answer behavior, runtime
behavior, data artifacts, or authority promotion.

The immediate goal is to decide how SuperCombo source-native
`source_header_path` groups may map to future English canonical `field_key`
values without using string-similarity auto-mapping and without making
SuperCombo numeric authority.

JSON Schema redesign remains blocked until this mapping review and the
value-shape review item disposition work are both reviewed.

## Scope

Included:

- Plan review coverage for all 403 SuperCombo source header path groups from
  the latest source inventory.
- Define how to propose canonical `field_key` values for SuperCombo fields.
- Define how to keep `source_label` and `source_header_path` source-native.
- Define separation of `source_family`, `source_name`, and `source_role`.
- Define required mapping statuses.
- Define category-specific review approach for Character Vitals, mobility,
  timing, advantage, damage, gauge, cancel, guard, armor, invulnerability,
  airborne, projectile, throw, notes, and prose fields.
- Define how unresolved mappings block JSON Schema redesign or become
  explicit review items.
- Decide future public mapping artifact shape.

Excluded:

- Do not implement JSON Schema redesign.
- Do not implement parser or classifier code.
- Do not implement normalized export.
- Do not change retrieval or answer behavior.
- Do not modify runtime code.
- Do not generate data artifacts in this planning step.
- Do not run live official or SuperCombo acquisition.
- Do not use `solve_cloudflare=True`.
- Do not promote official data to current-fact authority.
- Do not promote SuperCombo beyond enrichment, cross-reference, or candidate
  evidence.
- Do not commit `.local/`, `.venv/`, `.agents/`, raw HTML, raw rows,
  screenshots, cookies, browser profiles, traces, debug dumps, answer logs,
  training logs, private data, or ignored local artifacts.

## Acceptance Criteria

- The plan identifies the exact SuperCombo inventory inputs.
- The plan covers all 403 SuperCombo field summaries.
- The plan defines mapping statuses.
- The plan defines required fields for future mapping records.
- The plan keeps source labels and header paths source-native.
- The plan separates `source_family`, `source_name`, and `source_role`.
- The plan prevents string-similarity auto-mapping.
- The plan prevents SuperCombo numeric authority promotion.
- The plan states how unresolved mappings block schema redesign or become
  explicit review items.
- The plan decides whether future public mapping output is Markdown, JSON, or
  both.
- No implementation, schema, parser, retrieval, answer, or data artifact
  changes are made in this planning step.
- Planning validation passes.

## Files / Interfaces

Created in this step:

- `docs/execplans/2026-05-23-supercombo-canonical-field-mapping-review.md`

Required input artifacts:

- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md`
- `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md`

Reference context:

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md`

Future public mapping artifacts should be both Markdown and JSON:

- Markdown review table:
  `docs/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-review.md`
- JSON summary:
  `data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json`

Rationale:

- Markdown is needed for human review of field groups and rationale.
- JSON is needed for deterministic coverage validation before schema work.
- Both together match the current inventory and disposition artifact pattern.

This ExecPlan does not create those future artifacts.

## Input Inventory Facts

The latest value-shape inventory run is:

```text
20260521T025403Z
```

SuperCombo inventory facts:

- SuperCombo field summaries: 403
- SuperCombo observations: 78,501
- SuperCombo review item groups: 231
- SuperCombo authority role:
  `enrichment_cross_reference_candidate_only`

SuperCombo sections in the inventory:

| Section | Field summary count |
| --- | ---: |
| `Command Normals` | 35 |
| `Drive Moves` | 35 |
| `Hidden Arts` | 35 |
| `Normals` | 35 |
| `Prowler Stance` | 35 |
| `Serenity Stream` | 35 |
| `Special Moves` | 35 |
| `Super Arts` | 35 |
| `Target Combos` | 35 |
| `Taunts` | 35 |
| `Throws` | 35 |
| `Character Vitals` | 17 |
| `SF6 Navigation` | 1 |

The 11 move-data sections share 35 source labels each. `Character Vitals` and
`SF6 Navigation` are structurally separate and must not be forced into the same
mapping pattern.

## Mapping Statuses

Every future SuperCombo field mapping record must use exactly one mapping
status:

1. `maps_to_existing_official_field_key`
   - The SuperCombo field is a cross-reference candidate for an existing
     official canonical key.
   - This does not make SuperCombo authoritative.
   - Requires human-reviewed semantic equivalence, not string similarity.

2. `supercombo_source_specific_field_key`
   - The SuperCombo field should receive its own canonical key because it is
     useful but does not match an official field.
   - Example area: SuperCombo-specific juggle, drive-rush, hitconfirm, or
     character-vital fields.

3. `enrichment_only_no_current_fact_mapping`
   - The field remains part of the first public enrichment/review context
     output, but it does not receive a normalized current-fact `field_key`.
   - Use this when the field is useful for coach explanation, review, or
     cross-reference context even though it is not a current-fact field.

4. `out_of_scope_first_normalized_export`
   - The field is excluded from both the first normalized current-fact export
     and the first public enrichment/review context output.
   - Use this when the field is intentionally deferred and should not appear
     in first-release normalized artifacts except as an out-of-scope record.
   - Requires a rationale.

5. `blocked_pending_human_review`
   - The field cannot be mapped safely without source, domain, or semantic
     review.
   - This status blocks JSON Schema redesign if the field is needed by the
     first normalized export.

No status may promote SuperCombo to numeric authority.

Decision rule:

| Question | Status |
| --- | --- |
| Is the field safely mapped as a SuperCombo cross-reference candidate to an existing official `field_key`? | `maps_to_existing_official_field_key` |
| Is the field included in the first normalized/enrichment output with a SuperCombo-specific canonical key? | `supercombo_source_specific_field_key` |
| Is the field included only as first-release enrichment/review context, with no current-fact field key? | `enrichment_only_no_current_fact_mapping` |
| Is the field excluded from first-release normalized and enrichment outputs, with only a deferral record? | `out_of_scope_first_normalized_export` |
| Is there no safe mapping or deferral decision yet? | `blocked_pending_human_review` |

Validation rule:

- each of the 403 SuperCombo field summaries must have exactly one status;
- `enrichment_only_no_current_fact_mapping` and
  `out_of_scope_first_normalized_export` are mutually exclusive;
- a field included in first-release enrichment/review output cannot be
  `out_of_scope_first_normalized_export`;
- a field excluded from first-release outputs cannot be
  `enrichment_only_no_current_fact_mapping`;
- unresolved fields must use `blocked_pending_human_review`, not a guessed
  enrichment or out-of-scope status.

## Required Mapping Record Fields

Future mapping records must include:

```yaml
supercombo_field_mapping:
  mapping_id: string
  run_id: "20260521T025403Z"
  source_name: supercombo
  source_role: enrichment_candidate | cross_reference_candidate
  source_header_path: [string]
  source_label: string
  source_section: string
  source_family: timing | advantage | damage | gauge | cancel | guard | defense | projectile | throw | mobility | vital | identity | note | metadata | unknown
  proposed_field_key: string | null
  official_field_key_target: string | null
  mapping_status: maps_to_existing_official_field_key | supercombo_source_specific_field_key | enrichment_only_no_current_fact_mapping | out_of_scope_first_normalized_export | blocked_pending_human_review
  display_label_ja: string | null
  affected_field_summary_count: integer
  observation_count: integer
  shape_classes: [string]
  review_item_count: integer
  rationale: string
  json_schema_redesign_blocked: boolean
  value_shape_disposition_dependency: string | null
```

Rules:

- `source_header_path` and `source_label` remain source-native English.
- `source_name` must be `supercombo`.
- `source_role` must be `enrichment_candidate` or
  `cross_reference_candidate`, never authority.
- `source_family` is a semantic category and must not be `supercombo`.
- `proposed_field_key` may be null when mapping is unresolved.
- `official_field_key_target` may be set only when the mapping status is
  `maps_to_existing_official_field_key`.
- `display_label_ja` is a future answer/display concern, not source identity.

## Review Method

The mapping review must be manual and evidence-based.

Do:

- group fields by source section and source label;
- review source label meaning before choosing a canonical key;
- compare against official mapping seed from the normalized mapping policy;
- record when a SuperCombo field is only enrichment or out of scope;
- record blockers explicitly;
- keep raw source labels visible in review artifacts.

Do not:

- map fields by string similarity alone;
- map by column position alone;
- assume a SuperCombo label with the same English word as an official concept
  has the same semantics;
- merge official and SuperCombo authority;
- use SuperCombo as daily-answer numeric authority;
- create parsed values;
- infer numeric meaning.

## Category Review Policy

### Character Vitals And Mobility

Examples:

- `Character Vitals > HP`
- `Forward Walk Speed`
- `Back Walk Speed`
- `Forward Dash Distance`
- `Jump Speed`
- `Throw Range / Hurtbox`

Policy:

- likely `source_family`: `vital` or `mobility`;
- likely mapping status:
  `supercombo_source_specific_field_key` or
  `enrichment_only_no_current_fact_mapping`;
- do not map to official move-frame fields;
- do not create daily-answer numeric authority from these values.

### Timing

Examples:

- `Startup`
- `Active`
- `Recovery`
- `Total`
- `Blockstun`
- `Hitstun`
- `Hitstop`

Policy:

- likely `source_family`: `timing`;
- may map to existing official keys for `startup`, `active`, and `recovery`
  only after semantic review;
- `Total`, `Blockstun`, `Hitstun`, and `Hitstop` likely need
  SuperCombo-specific field keys or explicit out-of-scope decisions.

### Advantage

Examples:

- `Block Advantage`
- `Hit Advantage`
- `Punish Advantage`
- `After DR Blk`
- `After DR Hit`
- `DR Cancel Blk`
- `DR Cancel Hit`
- `Perfect Parry Advantage`

Policy:

- likely `source_family`: `advantage`;
- `Block Advantage` and `Hit Advantage` may map to official keys only after
  review;
- drive-rush and perfect-parry variants likely need source-specific field keys;
- SuperCombo remains cross-reference/candidate only.

### Damage And Scaling

Examples:

- `Damage`
- `Chip Dmg`
- `Dmg Scaling`

Policy:

- likely `source_family`: `damage` or `scaling`;
- `Damage` may be a cross-reference candidate for official `damage`;
- chip damage and scaling likely require source-specific keys or enum/schema
  review;
- no damage authority promotion occurs here.

### Gauge And Resources

Examples:

- `Drive Gain`
- `DriveDmg Blk`
- `DriveDmg Hit [PC]`
- `Super Gain Blk`
- `Super Gain Hit`

Policy:

- likely `source_family`: `gauge`;
- must be reviewed against official drive/SA fields before any shared key;
- bracketed or context-specific labels such as `[PC]` must remain explicit in
  source labels and mapping rationale.

### Cancel And Action Metadata

Examples:

- `Cancel`
- `Hitconfirm Window`
- `Juggle Start`
- `Juggle Increase`
- `Juggle Limit`

Policy:

- likely `source_family`: `cancel`, `metadata`, or `advantage`;
- requires source-specific enum or schema decisions before parsing;
- do not fold these into numeric fields.

### Guard, Armor, Invulnerability, Airborne, Projectile

Examples:

- `Guard`
- `Armor`
- `Invuln`
- `Airborne`
- `Projectile Speed`

Policy:

- likely `source_family`: `guard`, `defense`, `projectile`, or `metadata`;
- categorical or range-like values need reviewed enum/range support;
- unresolved meanings should become `blocked_pending_human_review`.

### Throw Fields

Examples:

- `Throw Range / Hurtbox`
- throw-section timing, damage, and advantage labels.

Policy:

- throw-vital fields should not be mapped to move timing without review;
- throw-section move rows may map to timing/damage/advantage categories only
  after section-aware review;
- if source semantics are ambiguous, block pending human review.

### Notes And Prose

Examples:

- `Notes`
- source text values that are prose or long contextual notes.

Policy:

- likely `source_family`: `note`;
- default mapping status should be `schema_supports_raw_only` in value-shape
  disposition or `enrichment_only_no_current_fact_mapping` in field mapping;
- no parser or numeric authority.

## JSON Schema Redesign Gate

JSON Schema redesign remains blocked until:

- all 403 SuperCombo field summaries have a mapping status;
- every `blocked_pending_human_review` item is resolved or explicitly scoped
  out of the first normalized export;
- every field mapped to an official key has a human-reviewed rationale;
- every SuperCombo-specific key has a stable name and source family;
- every out-of-scope field has a rationale;
- value-shape review item disposition has also been reviewed;
- reviewer confirms SuperCombo remains enrichment/cross-reference/candidate
  only.

This mapping review does not itself implement schema or parser behavior.

## Future Validation Strategy

The later mapping artifact validator should check:

- input inventory run ID is `20260521T025403Z`;
- exactly 403 SuperCombo field summaries are covered;
- every source header path appears exactly once in the mapping output;
- every mapping has exactly one approved mapping status;
- `enrichment_only_no_current_fact_mapping` is used only for fields included
  in first-release enrichment/review output without a current-fact key;
- `out_of_scope_first_normalized_export` is used only for fields excluded from
  first-release normalized and enrichment outputs;
- every required mapping field is present;
- no mapping sets SuperCombo to authority;
- no mapping claims `current_fact_authority`;
- no mapping introduces parsed values;
- no mapping contains raw HTML, full raw rows, full source table dumps, local
  paths, cookies, secrets, screenshots, traces, answer logs, training logs, or
  private data.

The future mapping summary should include:

```yaml
supercombo_mapping_summary:
  run_id: "20260521T025403Z"
  total_supercombo_field_summaries: 403
  mapping_status_counts:
    maps_to_existing_official_field_key: integer
    supercombo_source_specific_field_key: integer
    enrichment_only_no_current_fact_mapping: integer
    out_of_scope_first_normalized_export: integer
    blocked_pending_human_review: integer
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
  `889c185f3a491c00ae0cd93f8408a6e6e6b05c8a`.
- [x] (2026-05-23 JST) Moved the superseded untracked disposition draft to
  `/tmp/sf6-codex-superseded-plans/` so it is not mixed into this branch.
- [x] (2026-05-23 JST) Created branch
  `plan/supercombo-canonical-field-mapping-review`.
- [x] (2026-05-23 JST) Read SuperCombo field summary counts from the latest
  inventory JSON.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Plan SuperCombo canonical mapping before assigning final
  value-shape review-item dispositions.
  Rationale: Review items need `proposed_field_key` where known. SuperCombo
  field-key mapping reduces ambiguity before disposition work.
  Date/Author: 2026-05-23 / Codex

- Decision: Future SuperCombo mapping output should be both Markdown and JSON.
  Rationale: Markdown supports human review; JSON supports deterministic
  coverage validation across all 403 field summaries.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not use string-similarity auto-mapping.
  Rationale: Similar labels can have source-specific semantics. Mapping must
  be human-reviewed and evidence-based.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep SuperCombo as enrichment/cross-reference/candidate only.
  Rationale: The PLAN authority model does not allow SuperCombo to become
  daily-answer numeric authority here.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- The actual mapping status for each of the 403 SuperCombo field summaries.
- Which SuperCombo labels should map to existing official field keys.
- Which SuperCombo labels need source-specific canonical keys.
- Which SuperCombo labels are out of scope for the first normalized export.
- Stable naming convention for SuperCombo-specific canonical keys.
- Japanese display labels for SuperCombo-specific fields.
- Which unresolved SuperCombo mappings block JSON Schema redesign versus
  become explicit out-of-scope review items.

## Deviations

- None.

## Risks

- Mapping all 403 summaries may still be broad; implementation should group
  repeated labels but validate full coverage.
- Mapping by familiar English labels could accidentally imply equivalence with
  official data.
- Too many out-of-scope decisions could leave SuperCombo cross-reference value
  low.
- Too many blocked mappings could delay schema redesign.
- The superseded disposition draft exists only under `/tmp` and is not part of
  this repo branch.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan SuperCombo canonical mapping review | Drafted docs-only ExecPlan | `docs/execplans/2026-05-23-supercombo-canonical-field-mapping-review.md` | `git diff --check` | Pass | None | Mandatory review pending | 403 mappings not yet assigned |
| Preserve SuperCombo boundary | SuperCombo remains enrichment/cross-reference/candidate only | ExecPlan only | reviewer check | Pending | None | Mapping implementation not started | None |
| Keep schema blocked | JSON Schema redesign waits for SuperCombo mapping and value-shape disposition review | ExecPlan only | reviewer check | Pending | None | Disposition work still pending | Schema work must wait |
