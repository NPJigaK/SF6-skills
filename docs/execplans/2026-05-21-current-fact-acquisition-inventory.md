# Current-Fact Acquisition Inventory Planning

Status: Draft; planning-only ExecPlan.

## Purpose

Plan Phase 1 unit 1 from `docs/execplans/2026-05-20-phase1-roadmap.md`:
current-fact acquisition inventory planning.

This ExecPlan decides the inventory shape for official and SuperCombo
current-fact sources before any fetching, scraping, parsing, schema,
retrieval, or answer behavior changes. It preserves the Phase 1 retrieval
contract that numeric/current-fact answers must come from deterministic
tools/tables, not prose, FTS, manual review text, or model memory.

## Scope

Included:

- Define official source inventory scope for SF6 frame/current-fact pages.
- Define SuperCombo source inventory scope as enrichment/cross-reference
  candidate material.
- Decide the later acquisition-tool default candidate for HTML acquisition.
- Define a source list format.
- Define a per-character source descriptor format.
- Define a field inventory template.
- Define the raw snapshot artifact boundary for future acquisition work.
- Record planning assumptions for future `source_snapshot` and `source_row`
  records without implementing schemas.
- Preserve the public/private and authority/evidence boundaries in
  `docs/PLAN.md`, `AGENTS.md`, and the Phase 1 roadmap.

Excluded:

- No fetching implementation.
- No scraping implementation.
- No parsing or classifier implementation.
- No schema implementation.
- No generated DB or persistent DB implementation.
- No retrieval changes.
- No answer behavior changes.
- No validator changes.
- No dependency changes.
- No private vault, Discord, VLM, video pipeline, web daily-answer mode, API
  fallback, vector search, or `sf6 ask`.
- No restoration of deleted legacy runtime, package, adapter, or workflow
  surfaces.

## Acceptance Criteria

- The plan identifies official sources as the only source family that may
  later become `current_fact_authority` after deterministic acquisition,
  parsing, validation, and review.
- The plan identifies SuperCombo sources as enrichment, cross-reference, or
  candidate evidence only.
- The plan states that raw source values must be preserved exactly.
- The plan states that manual review, prose, FTS, and LLM memory are not
  numeric authority.
- The plan defines the source list format enough for a later implementation
  ExecPlan to create a reviewed inventory artifact.
- The plan defines the per-character source descriptor enough to cover all
  roster characters without hardcoding JP as a global assumption.
- The plan defines the field inventory template enough to record source field
  names, raw examples, value-shape examples, and authority eligibility without
  implementing a parser.
- The plan records that Scrapling is selected as the preferred later HTML
  acquisition candidate, but no dependency or fetching behavior is added in
  this ExecPlan.
- The plan defines the raw snapshot artifact boundary without introducing a
  new checked-in raw snapshot schema.
- Planning validation passes.

## Files / Interfaces

Changed by this ExecPlan:

- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`

Existing inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-20-phase1-retrieval-contract.md`
- `data/roster/current-character-roster.json`
- `data/exports/README.md`
- `data/aliases/README.md`

Future inventory artifacts are planned, not created here. A later ExecPlan may
choose exact paths. The preferred shape is a human-reviewable source inventory
with optional machine-readable records, for example:

- `docs/current-facts/source-inventory.md`
- `data/current-facts/source-inventory.json`
- `data/current-facts/field-inventory.json`

Those future paths are not approved by this planning-only ExecPlan.

## Source Inventory Scope

### Official

Official inventory scope starts from the Capcom SF6 frame/current-fact pages
listed under `data/roster/current-character-roster.json`.

Official source role:

- `source_family`: `official`
- `source_role`: `current_fact_authority_candidate`
- `evidence_basis`: `official`
- `review_status`: `inventory_only` until acquisition and validation exist
- `patch_sensitivity`: `high`

Official source values may later become daily-answer current-fact authority
only after a later implementation deterministically captures source snapshots,
preserves raw values, parses approved value shapes, validates outputs, and
passes mandatory review.

### SuperCombo

SuperCombo inventory scope starts from the SuperCombo data pages listed under
`data/roster/current-character-roster.json`.

SuperCombo source role:

- `source_family`: `supercombo`
- `source_role`: `enrichment_candidate`
- `evidence_basis`: `community`
- `review_status`: `inventory_only` until acquisition and validation exist
- `patch_sensitivity`: `high`

SuperCombo starts as enrichment, cross-reference, or candidate evidence only.
It must not override official current facts or become deterministic numeric
authority in Phase 1 without a later explicit promotion policy.

## Acquisition Tool Decision

Scrapling is selected as the preferred later HTML acquisition candidate for the
official and SuperCombo source families.

This is a planning decision only:

- This ExecPlan does not add Scrapling as a dependency.
- This ExecPlan does not run Scrapling.
- A later acquisition implementation ExecPlan must verify installation,
  version pinning, license suitability, offline testability, deterministic
  output expectations, and whether static HTTP fetching is sufficient for any
  source before adding the dependency.
- If Scrapling is unsuitable during later implementation, the later ExecPlan
  must record the reason in its Decision Log before selecting an alternative.

Rationale: retained planning context notes prior Scrapling-based acquisition
alignment, and both official and SuperCombo sources are HTML-like pages whose
structure may need robust extraction. Selecting it now gives later acquisition
planning a default candidate without introducing runtime behavior.

## Proposed Source List Format

The source list should be reviewable as data, not embedded in parser code.
This ExecPlan proposes the following record shape for a later inventory
artifact:

```yaml
source_list:
  schema_version: inventory-only-v1
  generated_from:
    roster_path: data/roster/current-character-roster.json
    generated_at: null
    generator: manual-or-future-tool
  sources:
    - source_id: official_frame_pages_ja
      source_family: official
      source_role: current_fact_authority_candidate
      evidence_basis: official
      patch_sensitivity: high
      acquisition_candidate: scrapling
      url_template: https://www.streetfighter.com/6/ja-jp/character/{character_slug}/frame
      raw_snapshot_policy: preserve_raw_html_and_extracted_rows_exactly
      authority_policy: may_become_current_fact_authority_after_validation
      daily_answer_policy: not_used_until_published_current_fact_authority
      review_questions: []
    - source_id: supercombo_data_pages
      source_family: supercombo
      source_role: enrichment_candidate
      evidence_basis: community
      patch_sensitivity: high
      acquisition_candidate: scrapling
      url_template: roster-provided
      raw_snapshot_policy: preserve_raw_html_and_extracted_rows_exactly
      authority_policy: enrichment_cross_reference_candidate_only
      daily_answer_policy: not_numeric_authority
      review_questions: []
```

## Proposed Per-Character Source Descriptor

Each roster character should receive a descriptor so the system remains
character-agnostic. JP may appear as one descriptor, not as a hardcoded global
assumption.

```yaml
character_source:
  character_slug: jp
  display_name: JP
  active_character_package_initial: true
  sources:
    official:
      source_id: official_frame_pages_ja
      url: https://www.streetfighter.com/6/ja-jp/character/jp/frame
      expected_content: frame_data_tables
      source_role: current_fact_authority_candidate
      acquisition_candidate: scrapling
      raw_snapshot_boundary: public_reviewed_snapshot_after_future_approval
      review_questions:
        - Is the page static enough for deterministic capture?
        - Does the page expose source version or patch timestamp?
        - Are all fields visible without user interaction?
    supercombo:
      source_id: supercombo_data_pages
      url: https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data
      expected_content: frame_data_reference_tables
      source_role: enrichment_candidate
      acquisition_candidate: scrapling
      raw_snapshot_boundary: public_reviewed_snapshot_after_future_approval
      review_questions:
        - Does the page structure differ from other characters?
        - Which fields are cross-reference only?
        - Which values conflict with official exports?
```

## Proposed Field Inventory Template

The field inventory records observed source fields and raw value shapes. It
does not parse, normalize, or authorize values.

```yaml
field_inventory:
  schema_version: inventory-only-v1
  fields:
    - field_key: startup
      semantic_group: frame
      source_family: official
      raw_source_label: startup
      raw_headers_seen:
        - startup
      raw_value_examples:
        - "4"
        - "22"
        - null
      observed_shape_classes:
        - integer_string
        - missing
      numeric_authority_candidate: true
      parser_required_before_authority: true
      raw_value_must_be_preserved: true
      notes: []
    - field_key: active
      semantic_group: frame
      source_family: official
      raw_source_label: active
      raw_headers_seen:
        - active
      raw_value_examples:
        - "6-8"
        - "12-31"
        - null
      observed_shape_classes:
        - range_string
        - multirange_string
        - missing
      numeric_authority_candidate: true
      parser_required_before_authority: true
      raw_value_must_be_preserved: true
      notes: []
    - field_key: notes_official
      semantic_group: prose_note
      source_family: official
      raw_source_label: notes_official
      raw_headers_seen:
        - notes_official
      raw_value_examples:
        - "Punish counter values appear here in Japanese source text"
        - null
      observed_shape_classes:
        - prose
        - missing
      numeric_authority_candidate: false
      parser_required_before_authority: false
      raw_value_must_be_preserved: true
      notes:
        - Prose notes may explain conditional values but are not numeric authority alone.
```

Minimum field inventory columns for a later implementation:

- `field_key`
- `semantic_group`
- `source_family`
- `raw_source_label`
- `raw_headers_seen`
- `raw_value_examples`
- `observed_shape_classes`
- `null_or_missing_tokens`
- `numeric_authority_candidate`
- `parser_required_before_authority`
- `raw_value_must_be_preserved`
- `conflict_policy`
- `notes`

## Raw Snapshot Artifact Boundary

Future acquisition should separate transient acquisition output from reviewed
public artifacts.

Transient acquisition output:

- Lives outside the public repo by default while fetching and debugging.
- May include HTML captures, request logs, screenshots, cache files, and tool
  diagnostics.
- Is not daily-answer authority.
- Must not include private user data.

Reviewed public raw snapshot artifacts:

- May be committed only after a later ExecPlan approves exact paths, formats,
  validators, and privacy checks.
- Must preserve raw source values exactly.
- Must keep source metadata separate from parsed value interpretation.
- Must include deterministic hashes for reviewed snapshot files.
- Must not include browser cache, local logs, personal paths, credentials, or
  private vault data.

Existing `data/exports/*/official_raw.json` remains the current checked-in
public current-fact authority until a later approved workflow replaces or
refreshes it.

## Future `source_snapshot` Planning Assumptions

No schema is implemented here. A later schema ExecPlan should consider at
least these fields:

```yaml
source_snapshot:
  snapshot_id: string
  source_id: string
  source_family: official | supercombo
  source_role: current_fact_authority_candidate | enrichment_candidate
  character_slug: string
  source_url: string
  captured_at: string
  acquisition_tool: scrapling | static_http | manual | other
  acquisition_tool_version: string | null
  source_version_label: string | null
  locale: string | null
  raw_artifact_refs: []
  content_hash: string
  review_status: inventory_only | acquired | validated | rejected
  authority_policy: string
```

## Future `source_row` Planning Assumptions

No schema is implemented here. A later schema ExecPlan should consider at
least these fields:

```yaml
source_row:
  source_row_id: string
  snapshot_id: string
  character_slug: string
  source_family: official | supercombo
  table_label_raw: string | null
  row_index: integer
  move_identity_candidate:
    move_name_raw: string | null
    input_raw: string | null
    move_group_raw: string | null
  raw_cells: object
  row_hash: string
  extraction_notes: []
  review_status: inventory_only | acquired | validated | rejected
```

`source_row.raw_cells` must preserve source cell values exactly. Parsed values
belong to a later `current_fact_record` or `parsed_value` design, not to this
inventory plan.

## Authority And Evidence Policy

- Official source values may later become `current_fact_authority` only through
  deterministic acquisition, parser/schema validation, and review.
- SuperCombo starts as enrichment, cross-reference, or candidate evidence only.
- Raw source values must be preserved exactly.
- Manual review sidecars, prose notes, FTS search results, and LLM memory are
  not numeric authority.
- Current-fact conflicts between official and SuperCombo sources become review
  items. They do not allow SuperCombo to override official values.
- Existing `data/exports/*/official_raw.json` remains the only current
  daily-answer numeric authority during this planning unit.

## Validation Commands

Run from the repository root:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-21 JST) Verified PR #299 was merged into `main` with merge
  commit `46ec03930f63755dc2968ccb8861daec9041d6ab`.
- [x] (2026-05-21 JST) Verified main branch CI passed for merge commit
  `46ec03930f63755dc2968ccb8861daec9041d6ab`.
- [x] (2026-05-21 JST) Preserved paused retrieval runtime work in a local stash
  before creating this planning branch.
- [x] (2026-05-21 JST) Created branch
  `plan/current-fact-acquisition-inventory` from updated `main`.
- [x] (2026-05-21 JST) Reviewed `docs/PLAN.md`, Phase 1 roadmap,
  retrieval-contract ExecPlan, `data/roster/current-character-roster.json`,
  `data/exports/README.md`, and `data/aliases/README.md`.
- [x] (2026-05-21 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-21 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [ ] Mandatory review.

## Decision Log

- Decision: This unit creates only the acquisition inventory plan, not the
  inventory artifact itself.
  Rationale: The user requested `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
  only, and the Phase 1 roadmap requires reviewable units before
  implementation.
  Date/Author: 2026-05-21 / Codex

- Decision: Use `data/roster/current-character-roster.json` as the starting
  seed for official and SuperCombo source inventory.
  Rationale: It already contains character-agnostic source URLs for all current
  roster characters, but later acquisition must still verify each source rather
  than treating the roster file as fresh source truth.
  Date/Author: 2026-05-21 / Codex

- Decision: Select Scrapling as the preferred later HTML acquisition candidate.
  Rationale: Retained planning context points future acquisition toward
  Scrapling alignment, and both source families are HTML-like. This does not
  add a dependency or prevent a later ExecPlan from rejecting Scrapling after
  version, license, determinism, and source-structure checks.
  Date/Author: 2026-05-21 / Codex

- Decision: Official and SuperCombo are inventoried together but kept in
  different authority roles.
  Rationale: Shared inventory fields make coverage review easier, while
  `docs/PLAN.md` and the roadmap require official current facts to stay
  separate from SuperCombo enrichment/candidate evidence.
  Date/Author: 2026-05-21 / Codex

- Decision: Preserve raw values exactly and defer parsing/value semantics.
  Rationale: The Phase 1 roadmap requires source and value-shape inventory
  before schema and parser work. Normalizing values during acquisition would
  blur source evidence with interpretation.
  Date/Author: 2026-05-21 / Codex

## Deviations

- None.

## Risks

- `data/roster/current-character-roster.json` may be stale relative to the live
  game or source websites; later acquisition must verify source availability.
- Official site structure or locale behavior may require source-specific
  acquisition policy.
- SuperCombo page structure may vary by character and may need per-page
  extraction notes.
- Scrapling suitability is not verified in this planning unit.
- Future raw snapshot placement is intentionally not finalized here; a later
  ExecPlan must decide exact paths and validators.
- Paused retrieval runtime work remains local outside this branch in a stash
  and must not be reintroduced without explicit review.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Current-fact acquisition inventory planning | Planned official and SuperCombo inventory scope only. | `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md` | `git diff --check` | Pass | None | Mandatory review pending | Source freshness still unverified |
| Authority/evidence policy | Recorded official as future authority candidate and SuperCombo as enrichment/candidate only. | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | No schema or parser yet | Later implementation must enforce policy |
| Scrapling decision | Selected Scrapling as later preferred candidate without adding dependency. | Same | Review | Pending | None | Tool suitability unverified | Later ExecPlan may need alternative |
| Raw value preservation | Defined raw snapshot and source row assumptions without schema implementation. | Same | Review | Pending | None | No artifact paths approved | Future raw snapshot validators needed |
