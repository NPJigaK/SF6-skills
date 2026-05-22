# SuperCombo Field Mapping Artifacts

Status: Drafted for review.

## Purpose

Plan generation and review artifacts for all 403 SuperCombo field-summary
mappings from the latest source value-shape inventory.

This ExecPlan implements the planning step after
`2026-05-23-supercombo-canonical-field-mapping-review.md`. It is still
docs-only. It does not implement the mapping generator, mapping validator,
schemas, parsers, classifiers, normalized exports, retrieval changes, answer
behavior, runtime behavior, or authority promotion.

JSON Schema redesign remains blocked until SuperCombo mapping artifacts are
implemented and reviewed, and value-shape review item disposition is also
completed and reviewed.

## Scope

Included:

- Plan artifacts that cover exactly 403 SuperCombo field summaries.
- Plan one mapping record per SuperCombo `source_header_path` group.
- Plan exactly one `mapping_status` per mapping record.
- Reuse the mapping statuses approved in the SuperCombo canonical mapping
  review.
- Define public Markdown and JSON mapping summary outputs.
- Define validation requirements for coverage, status exclusivity, authority
  boundary, privacy, and source-boundary guard.
- Define optional generator module boundaries if implementation needs code.
- Keep SuperCombo source labels and header paths source-native.

Excluded:

- Do not implement this plan yet.
- Do not implement JSON Schema redesign.
- Do not implement parser or classifier behavior.
- Do not implement normalized export.
- Do not change retrieval or answer behavior.
- Do not modify runtime code.
- Do not run live official or SuperCombo acquisition.
- Do not use `solve_cloudflare=True`.
- Do not promote SuperCombo to numeric authority.
- Do not create parsed values.
- Do not use string-similarity auto-mapping.
- Do not commit `.local/`, `.venv/`, `.agents/`, raw HTML, raw rows,
  screenshots, cookies, browser profiles, traces, debug dumps, answer logs,
  training logs, private data, or ignored local artifacts.

## Acceptance Criteria

- The plan names all required input artifacts and policy ExecPlans.
- The plan names the future Markdown and JSON mapping artifacts.
- The plan names the future validator path.
- The plan allows a generator module only if needed.
- The plan requires exactly 403 SuperCombo field summaries to be covered.
- The plan requires one mapping record per `source_header_path` group.
- The plan requires exactly one `mapping_status` per record.
- The plan uses the mapping statuses from PR #311.
- The plan keeps `source_label` and `source_header_path` source-native.
- The plan keeps `source_family` as a semantic category only.
- The plan keeps `source_name: supercombo`.
- The plan keeps `source_role` limited to `enrichment_candidate` or
  `cross_reference_candidate`.
- The plan forbids SuperCombo numeric authority promotion.
- The plan forbids string-similarity auto-mapping.
- The plan forbids parsed values.
- The plan forbids schema/parser/retrieval/answer behavior changes.
- The plan states that public artifacts are mapping summaries only, not raw
  source dumps.
- The plan keeps JSON Schema redesign blocked.
- Planning validation passes.

## Files / Interfaces

Created in this planning step:

- `docs/execplans/2026-05-23-supercombo-field-mapping-artifacts.md`

Required inputs for the later implementation:

- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md`
- `docs/execplans/2026-05-23-supercombo-canonical-field-mapping-review.md`
- `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md`

Planned public outputs:

- `docs/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-review.md`
- `data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json`

Planned validation file:

- `tests/validation/validate_supercombo_field_mapping.py`

Optional implementation file if needed:

- `src/sf6_knowledge_coach/supercombo_field_mapping.py`

No files are implemented by this planning step beyond this ExecPlan.

## Input Inventory Facts

The latest value-shape inventory run is:

```text
20260521T025403Z
```

SuperCombo input facts:

- SuperCombo field summaries: 403
- SuperCombo observations: 78,501
- SuperCombo review item groups: 231
- SuperCombo authority role:
  `enrichment_cross_reference_candidate_only`

Section coverage from the input inventory:

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

The later implementation must fail validation if the input SuperCombo field
summary count is not exactly 403 for run `20260521T025403Z`.

## Mapping Statuses

Each mapping record must use exactly one status from PR #311:

1. `maps_to_existing_official_field_key`
   - mapped as a SuperCombo cross-reference candidate to an existing official
     field key;
   - never authoritative.

2. `supercombo_source_specific_field_key`
   - included as a SuperCombo-specific normalized/enrichment field;
   - has its own stable `proposed_field_key`.

3. `enrichment_only_no_current_fact_mapping`
   - included only as first-release enrichment/review context;
   - no current-fact `field_key`.

4. `out_of_scope_first_normalized_export`
   - excluded from first-release normalized and enrichment outputs;
   - represented only by an out-of-scope deferral record.

5. `blocked_pending_human_review`
   - no safe mapping or deferral decision yet;
   - must not be guessed.

Status exclusivity rules:

- exactly one status per mapping record;
- `enrichment_only_no_current_fact_mapping` and
  `out_of_scope_first_normalized_export` are mutually exclusive;
- included first-release context cannot be out of scope;
- excluded first-release context cannot be enrichment-only;
- unresolved fields must use `blocked_pending_human_review`.

## Mapping Record Contract

Future JSON records should use this structure:

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
- `source_family` is a semantic category and must not be `supercombo`.
- `source_name` must be `supercombo`.
- `source_role` must be `enrichment_candidate` or
  `cross_reference_candidate`.
- `source_role` must never be `authority`, `authority_candidate`, or
  `current_fact_authority`.
- `official_field_key_target` may be set only when `mapping_status` is
  `maps_to_existing_official_field_key`.
- `proposed_field_key` is required for
  `maps_to_existing_official_field_key` and
  `supercombo_source_specific_field_key`.
- `proposed_field_key` must be null for
  `enrichment_only_no_current_fact_mapping`,
  `out_of_scope_first_normalized_export`, and
  `blocked_pending_human_review`.
- `display_label_ja` is optional in this artifact and remains a display
  concern, not source identity.
- No record may include `parsed_value`.

## Mapping Authoring Policy

The later mapping implementation may seed records by grouping existing
inventory data, but the mapping decisions must remain reviewable and
conservative.

Allowed:

- copy source-native `source_header_path`, `source_label`, observation counts,
  shape classes, and review item counts from the inventory;
- group repeated labels across SuperCombo sections for reviewer convenience;
- set initial statuses when the source section and label clearly match an
  approved policy from the mapping ExecPlan;
- use explicit manual mapping tables committed in the mapping artifact.

Forbidden:

- string-similarity auto-mapping;
- column-position auto-mapping;
- assigning official equivalence without reviewed rationale;
- assigning SuperCombo numeric authority;
- generating parsed values;
- adding schema/parser/retrieval/answer behavior;
- hiding unresolved fields behind guessed statuses.

## Public Artifact Boundary

Public mapping artifacts are mapping summaries only.

Allowed public content:

- source-native SuperCombo section and label names;
- mapping statuses;
- proposed canonical field keys;
- official target field keys when reviewed;
- semantic `source_family` categories;
- observation counts;
- shape class summaries;
- review item counts;
- human-readable rationale;
- JSON Schema redesign blocker flags.

Forbidden public content:

- raw HTML;
- full raw row dumps;
- full source table dumps;
- complete per-move frame tables;
- cookies;
- request headers with secrets;
- credentials, tokens, or auth headers;
- local absolute paths;
- private vault references;
- real user profile data;
- answer logs;
- training logs;
- browser profiles;
- screenshots;
- traces;
- debug dumps.

## Validation Requirements

The planned validator must fail if:

- the input inventory run ID is not `20260521T025403Z`;
- there are not exactly 403 SuperCombo field summaries;
- any SuperCombo `source_header_path` group is missing from the mapping;
- any mapping record has a duplicate `source_header_path`;
- any mapping record has zero or more than one `mapping_status`;
- `mapping_status` is not one of the five approved statuses;
- `source_label` or `source_header_path` is translated or normalized instead
  of source-native;
- `source_family` is `official` or `supercombo` instead of a semantic
  category;
- `source_name` is not `supercombo`;
- `source_role` is outside `enrichment_candidate` or
  `cross_reference_candidate`;
- any record claims numeric authority or `current_fact_authority`;
- any record includes `parsed_value`;
- `official_field_key_target` is set for a status other than
  `maps_to_existing_official_field_key`;
- `proposed_field_key` is missing for records that map to official or
  SuperCombo-specific field keys;
- `proposed_field_key` is present for enrichment-only, out-of-scope, or
  blocked records;
- `enrichment_only_no_current_fact_mapping` and
  `out_of_scope_first_normalized_export` semantics are collapsed;
- public artifacts contain raw HTML, raw rows, source dumps, local paths,
  secrets, private data, logs, screenshots, traces, or debug dumps.

The validator must also emit a summary equivalent to:

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

## Implementation Slice Boundaries

The later implementation may include:

- a generator or manual artifact builder for the mapping summary;
- the Markdown mapping review artifact;
- the JSON mapping summary artifact;
- `tests/validation/validate_supercombo_field_mapping.py`;
- focused unit tests only if an implementation module is added;
- ExecPlan progress/decision/risk updates.

The later implementation must not include:

- JSON Schema redesign;
- parser/classifier semantics;
- normalized export;
- retrieval or answer behavior changes;
- live acquisition;
- `solve_cloudflare=True`;
- authority promotion;
- raw source artifact commits.

## JSON Schema Redesign Gate

JSON Schema redesign remains blocked until:

- these SuperCombo mapping artifacts are implemented and reviewed;
- all 403 SuperCombo field summaries have one validated mapping record;
- all blocked SuperCombo mappings are resolved or explicitly scoped out;
- value-shape review item disposition is completed and reviewed;
- reviewer confirms SuperCombo remains enrichment/cross-reference/candidate
  only;
- a later schema-specific ExecPlan is approved.

This mapping artifact plan does not itself unblock schema implementation.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Confirmed `main` and `origin/main` are at
  `71b2f9bcb64f0b8caeda230cbef44e15ac539213`.
- [x] (2026-05-23 JST) Created branch
  `plan/supercombo-field-mapping-artifacts`.
- [x] (2026-05-23 JST) Confirmed the target ExecPlan did not already exist.
- [x] (2026-05-23 JST) Read latest inventory counts and confirmed exactly 403
  SuperCombo field summaries.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Future mapping output should be both Markdown and JSON.
  Rationale: Markdown supports human review of 403 mappings, while JSON
  supports deterministic validation before schema work.
  Date/Author: 2026-05-23 / Codex

- Decision: Plan a validator as part of the later implementation.
  Rationale: Coverage of exactly 403 field summaries and status exclusivity
  are too important to rely on manual review alone.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep the implementation slice separate from value-shape review
  item disposition.
  Rationale: Field mapping and value-shape disposition are different blockers;
  combining them would obscure schema redesign gates.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not allow string-similarity auto-mapping.
  Rationale: Similar labels can have source-specific semantics, and
  SuperCombo must not be promoted by accidental equivalence.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Actual mapping status for each of the 403 SuperCombo field summaries.
- Which SuperCombo fields map to existing official field keys.
- Which SuperCombo fields receive source-specific canonical field keys.
- Which SuperCombo fields remain enrichment-only context.
- Which SuperCombo fields are out of scope for the first normalized export.
- Which SuperCombo fields remain blocked pending human review.
- Exact implementation choice: manual artifact authoring only, generator
  module, or a small hybrid.

## Deviations

- None.

## Risks

- Mapping all 403 summaries may be broad; implementation should keep the
  generated artifact reviewable and validate full coverage.
- Over-eager mapping to official keys could imply authority equivalence.
- Too many out-of-scope mappings could reduce SuperCombo cross-reference
  value.
- Too many blocked mappings could delay JSON Schema redesign.
- The mapping artifact may need follow-up review before value-shape
  disposition can fill `proposed_field_key` reliably.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan SuperCombo mapping artifacts | Drafted docs-only ExecPlan | `docs/execplans/2026-05-23-supercombo-field-mapping-artifacts.md` | `git diff --check` | Pass | None | Mandatory review pending | 403 mappings not assigned |
| Preserve mapping boundaries | Planned source-native labels, semantic `source_family`, `source_name: supercombo`, and non-authority roles | ExecPlan only | reviewer check | Pending | None | Implementation not started | None |
| Plan validation | Required coverage/status/privacy/source-boundary validator | ExecPlan only | reviewer check | Pending | None | Validator not implemented | Coverage errors possible later |
| Keep schema blocked | Explicitly blocks JSON Schema redesign until mapping artifacts and value-shape disposition are reviewed | ExecPlan only | reviewer check | Pending | None | Value-shape disposition still pending | Schema work must wait |
