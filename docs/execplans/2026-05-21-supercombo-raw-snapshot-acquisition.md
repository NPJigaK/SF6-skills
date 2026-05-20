# SuperCombo Raw Snapshot Acquisition Planning

Status: Draft; planning-only ExecPlan.

## Purpose

Plan Phase 1 roadmap unit 3: SuperCombo all-character raw snapshot
acquisition.

This ExecPlan defines how a future implementation should acquire or inventory
SuperCombo all-character raw snapshots as enrichment, cross-reference, or
candidate evidence only. It does not promote SuperCombo to daily-answer
numeric authority, and it does not implement fetching, Scrapling, parsing,
schemas, validators, retrieval, answer behavior, generated DBs, or data
artifacts.

## Scope

Included:

- Define SuperCombo all-character acquisition scope from
  `data/roster/current-character-roster.json`.
- Define SuperCombo authority and evidence boundaries.
- Define exact raw value preservation requirements for SuperCombo evidence.
- Define transient Git-outside acquisition workspace boundaries.
- Define reviewed public raw snapshot artifact boundaries.
- Mirror the official-source caution that full raw HTML or equivalent source
  documents require source-boundary review before public commit.
- Define required source metadata for each character/source.
- Define manifest requirements for future SuperCombo raw snapshots.
- Define hash requirements for reviewed SuperCombo raw snapshots.
- Define source freshness and page-structure checks.
- Define privacy and no-local-path rules.
- Define validation strategy for future acquisition artifacts.
- Define relationship to existing `data/exports/*/supercombo_enrichment.json`
  and `data/exports/*/official_raw.json`.

Excluded:

- No fetching implementation.
- No Scrapling dependency.
- No official acquisition.
- No official/SuperCombo reconciliation implementation.
- No promotion policy.
- No schema implementation.
- No parser or classifier.
- No normalized export.
- No retrieval changes.
- No answer behavior changes.
- No validator changes.
- No private vault, Discord, VLM, video pipeline, web daily-answer mode, API
  fallback, vector search, persistent DB, generated DB, or `sf6 ask`.
- No restoration of deleted legacy runtime, package, adapter, or workflow
  surfaces.

## Acceptance Criteria

- The plan scopes SuperCombo acquisition across every character in
  `data/roster/current-character-roster.json`.
- The plan states that missing `sources.supercombo_data` entries are coverage
  failures or review items, not silent exclusions.
- The plan states that SuperCombo values are enrichment, cross-reference, or
  candidate evidence only.
- The plan states that SuperCombo is not daily-answer numeric authority in this
  unit.
- The plan states that raw source values must be preserved exactly before any
  normalization or interpretation.
- The plan separates transient Git-outside acquisition work from reviewed
  public raw snapshot artifacts.
- The plan adds a source-boundary gate before any full raw HTML or equivalent
  source document can be committed to the public repository.
- The plan defines source metadata, manifest, and hash requirements without
  implementing schemas.
- The plan defines validation expectations without adding validators.
- The plan does not change daily answer behavior or current-fact authority.
- Planning validation passes.

## Files / Interfaces

Changed by this ExecPlan:

- `docs/execplans/2026-05-21-supercombo-raw-snapshot-acquisition.md`

Existing inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
- `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md`
- `data/roster/current-character-roster.json`
- `data/exports/README.md`

Future implementation artifacts are planned, not created here. A later
ExecPlan must approve exact paths, formats, schemas, validators, and
source-boundary gates before any new SuperCombo raw snapshot artifacts are
committed.

## SuperCombo Acquisition Scope

The future SuperCombo acquisition scope is all roster entries in
`data/roster/current-character-roster.json`.

Every roster character is in scope. If any roster entry lacks
`sources.supercombo_data`, future acquisition must record that character as a
coverage failure or review item. It must not silently drop the character from
the run.

For each roster character, future acquisition should record:

- `character_slug`
- `display_name`
- `supercombo_url`
- `source_family`: `supercombo`
- `source_role`: `enrichment_candidate`
- `evidence_basis`: `community`
- `patch_sensitivity`: `high`
- `expected_content`: SuperCombo SF6 data page
- `acquisition_candidate`: `scrapling`, subject to later verification

JP is one character in this all-character scope. It remains the initial active
character package for product use, not a hardcoded global acquisition
assumption.

## Authority Boundary

SuperCombo values are not daily-answer numeric authority in this unit.

Allowed future uses:

- Enrichment evidence.
- Cross-reference evidence.
- Candidate evidence.
- Conflict discovery against official current facts.
- Review prompts for official refresh or parser review.

Disallowed future uses in this unit:

- Overriding `data/exports/*/official_raw.json`.
- Answering frame, damage, scaling, punish, combo damage, patch delta, or
  current move facts as definitive daily-answer values.
- Promoting SuperCombo rows to `current_fact_authority`.
- Treating prose, FTS, manual review, or LLM memory as numeric authority.

If SuperCombo conflicts with official data, the result is a review item, not an
automatic replacement.

## Exact Raw Value Preservation

Future SuperCombo acquisition must preserve source values exactly before any
normalization or interpretation.

Preserve exactly:

- Raw table labels and section labels.
- Raw column/header labels.
- Raw row order and row grouping.
- Raw move names.
- Raw input notation.
- Raw cell values, including signs, dashes, parentheses, percent symbols,
  conditional note text, punctuation, and null/missing distinctions.
- Raw notes, page-visible qualifiers, and footnotes.
- Source-visible page text needed to understand row context.

Do not rewrite during acquisition:

- Frame values.
- Damage values.
- Scaling values.
- Punish/counter notes.
- Move names or aliases.
- Multihit or conditional expressions.
- Blank, missing, unknown, or source-empty cells.

Normalization, parsed values, official comparison, and any promotion decision
belong to later reviewed units.

## Transient Git-Outside Workspace Boundary

Future acquisition should use a transient workspace outside the public repo by
default.

Allowed transient contents:

- Fetch/cache files.
- Raw HTML captures before review.
- Extraction diagnostics.
- Tool logs.
- Screenshots or browser traces if needed for debugging.
- Candidate extracted rows before review.

Rules:

- Do not commit transient workspace paths.
- Do not commit browser cache, cookies, credentials, or request headers that
  could contain secrets.
- Do not commit local absolute paths.
- Do not use transient files as daily-answer authority.
- Do not store private user data in the acquisition workspace.

Suggested local naming pattern for a later implementation:

```text
<git-outside-cache-root>/sf6-knowledge-coach/supercombo-raw/<run_id>/
```

The exact path is not approved by this ExecPlan and must remain configurable in
a later implementation.

## Reviewed Public Raw Snapshot Artifact Boundary

Reviewed public raw snapshot artifacts may be committed only after a later
implementation ExecPlan approves exact paths, formats, schemas, validators, and
source-boundary rules.

By default, future public artifacts should be limited to extracted raw rows,
source metadata, manifests, and hashes. Full raw HTML or equivalent source
documents remain Git-outside unless a later ExecPlan explicitly approves public
storage after reviewing source terms, license, robots policy, attribution
requirements, and source-specific redistribution limits. Privacy checks and
hashes are necessary but not sufficient to approve committing full raw source
documents.

Potential future public surfaces:

```text
data/sources/supercombo/<run_id>/source-snapshot-manifest.json
data/sources/supercombo/<run_id>/<character_slug>/source-rows.json
```

These paths are examples, not approved implementation paths.

Public artifacts must:

- Contain only reviewed extracted raw rows, source metadata, manifests, and
  hashes by default.
- Preserve raw source values exactly.
- Use repository-relative artifact references.
- Include content hashes.
- Include source URL and capture metadata.
- Exclude local absolute paths.
- Exclude credentials, cookies, private vault content, answer logs, and user
  training data.
- Remain separate from parsed or normalized current-fact exports.
- Carry `source_role` values that keep SuperCombo out of daily-answer numeric
  authority.

Full raw HTML or equivalent source documents may be listed as transient
Git-outside evidence refs, but public repository refs require explicit
source-boundary approval.

## Required Source Metadata

Each future character/source record should include at minimum:

```yaml
supercombo_source_metadata:
  character_slug: jp
  display_name: JP
  source_family: supercombo
  source_role: enrichment_candidate
  evidence_basis: community
  source_url: https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Data
  locale: null
  captured_at: 2026-05-21T00:00:00Z
  acquisition_tool: scrapling | static_http | manual | other
  acquisition_tool_version: null
  request_method: GET
  source_version_label: null
  page_revision_label: null
  http_status: null
  content_type: null
  raw_artifact_refs: []
  content_hashes: {}
  review_status: acquired_unreviewed
  daily_answer_numeric_authority: false
```

`captured_at` must be UTC in the future implementation. Local timezone may be
recorded only as secondary metadata if needed.

## Manifest Requirements

A future SuperCombo raw snapshot manifest should describe the whole
acquisition run and each character snapshot. It should be reviewable without
opening every raw artifact.

Minimum run-level manifest fields:

- `manifest_schema_version`
- `run_id`
- `source_family`
- `source_role`
- `started_at`
- `completed_at`
- `roster_source_path`
- `roster_source_hash`
- `character_count_expected`
- `character_count_acquired`
- `coverage_failure_count`
- `coverage_review_items`
- `acquisition_tool`
- `acquisition_tool_version`
- `network_required`
- `artifact_root`
- `privacy_review_status`
- `source_boundary_review_status`
- `validation_status`
- `daily_answer_numeric_authority`: `false`

Minimum character-level manifest fields:

- `character_slug`
- `display_name`
- `source_url`
- `captured_at`
- `http_status`
- `final_url`
- `coverage_status`
- `source_version_label`
- `page_revision_label`
- `source_rows_ref`
- `source_rows_sha256`
- `raw_row_count`
- `extraction_warning_count`
- `missing_required_field_count`
- `review_status`
- `daily_answer_numeric_authority`: `false`

## Hash Requirements

Future reviewed SuperCombo raw snapshot artifacts must include deterministic
hashes.

Hash rules:

- Use SHA-256 unless a later ExecPlan records a stronger project-wide choice.
- Hash extracted raw row artifacts after deterministic serialization.
- Hash any full source document only if a later source-boundary review approves
  public storage for that source document.
- Include hashes in the manifest using repository-relative artifact refs.
- Recompute hashes in validation and fail on mismatch.
- Do not hash transient local paths as identity.

Hashing proves artifact integrity only. It does not make SuperCombo numeric
authority and does not prove that a source is current.

## Source Freshness And Page-Structure Checks

Future acquisition must record freshness and page-structure information before
using SuperCombo as enrichment or candidate evidence.

Freshness and structure checks to plan for:

- Confirm the SuperCombo source URL resolves for every roster character.
- Record HTTP status and final URL after redirects.
- Record capture timestamp in UTC.
- Look for page revision, update timestamp, or visible version labels when
  available.
- Compare roster source URLs with `data/roster/current-character-roster.json`.
- Record table labels, row counts, and missing expected sections.
- Record added, removed, or renamed rows as review items.
- Record source-structure differences between characters.
- Treat missing or ambiguous freshness metadata as a review risk, not a reason
  to promote SuperCombo to authority.

Freshness checks do not authorize numeric answers by themselves.

## Privacy And No-Local-Path Rules

Future acquisition artifacts must not contain:

- Local absolute paths.
- User names or home directory paths.
- Browser profile paths.
- Cookies, credentials, tokens, headers with secrets, or session identifiers.
- Private vault references.
- Answer logs or training logs.
- Personal notes.

Public artifacts should use repository-relative paths only. Transient logs may
contain local paths while outside Git, but validators for reviewed public
artifacts must reject local path leakage.

## Future Validation Strategy

A future implementation ExecPlan should add focused validators before
publishing SuperCombo raw snapshots.

Planned validation categories:

- Manifest structure validation.
- Artifact existence checks for repository-relative refs.
- SHA-256 recomputation.
- No local absolute paths.
- No credential/cookie/header leakage.
- Expected character coverage from `data/roster/current-character-roster.json`.
- Failure when a roster character has no `sources.supercombo_data` and the run
  does not record a coverage failure or review item.
- Source URL coverage and duplicate URL detection.
- Source-boundary validation ensuring public artifacts do not include full raw
  HTML or equivalent source documents unless a later explicit approval records
  source terms, license, robots, and attribution review.
- Raw row count presence.
- Required raw field presence by source table when known.
- Authority boundary checks ensuring SuperCombo snapshots are not treated as
  parsed daily-answer numeric facts.

This ExecPlan does not add those validators.

## Relationship To Existing `data/exports`

Existing `data/exports/*/official_raw.json` remains the current checked-in
daily-answer numeric authority during this planning unit.

Existing `data/exports/*/supercombo_enrichment.json` remains an enrichment
surface. It does not become daily-answer numeric authority here, and this
planning unit does not change its content, schema, or generation path.

Future SuperCombo raw snapshots may support enrichment refresh, conflict
discovery, or candidate review only after later units approve:

- Raw snapshot artifact placement and validation.
- SuperCombo extraction policy.
- Field and value-shape inventory.
- Official/SuperCombo comparison policy.
- Review workflow.

Until then, future SuperCombo raw snapshots are acquisition evidence, not a
change to daily answer behavior.

## Authority And Evidence Policy

- SuperCombo raw snapshots are enrichment, cross-reference, or candidate
  evidence only.
- SuperCombo raw snapshots are not daily-answer numeric authority in this unit.
- Raw source values must be preserved exactly.
- Manual review sidecars, prose, FTS, SuperCombo, and LLM memory are not
  numeric authority.
- This unit must not change daily answer behavior.
- Conflicts between SuperCombo snapshots and official exports become review
  items, not automatic replacements.

## Validation Commands

Run from the repository root:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-21 JST) Verified PR #301 was merged into `main` with merge
  commit `7b9cacfc7ef33186e58142273bfcbfe068a380e1`.
- [x] (2026-05-21 JST) Verified main branch CI passed for merge commit
  `7b9cacfc7ef33186e58142273bfcbfe068a380e1`.
- [x] (2026-05-21 JST) Confirmed `stash@{0}` remains present and unapplied.
- [x] (2026-05-21 JST) Created branch
  `plan/supercombo-raw-snapshot-acquisition` from updated `main`.
- [x] (2026-05-21 JST) Reviewed current-fact acquisition inventory plan,
  official raw snapshot acquisition plan, Phase 1 roadmap, and
  `data/roster/current-character-roster.json`.
- [x] (2026-05-21 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-21 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [ ] Mandatory review.

## Decision Log

- Decision: This unit plans SuperCombo raw snapshot acquisition only.
  Rationale: The Phase 1 roadmap separates SuperCombo acquisition from
  official acquisition so enrichment/cross-reference/candidate evidence remains
  distinct from current-fact authority.
  Date/Author: 2026-05-21 / Codex

- Decision: Use `data/roster/current-character-roster.json` as the acquisition
  scope seed.
  Rationale: It is the retained character-agnostic roster surface with
  SuperCombo source URLs for all current roster characters. Future acquisition
  must still verify live source availability and freshness.
  Date/Author: 2026-05-21 / Codex

- Decision: Keep future transient acquisition output Git-outside by default.
  Rationale: Fetch diagnostics, caches, and raw debugging output are not
  reviewed public artifacts and may contain local paths or tool noise.
  Date/Author: 2026-05-21 / Codex

- Decision: Public raw snapshot artifacts default to extracted raw rows,
  metadata, manifests, and hashes; full raw HTML remains Git-outside unless a
  later source-boundary review explicitly approves it.
  Rationale: Source terms, license, robots, attribution, and redistribution
  constraints must be reviewed before committing full source documents. Privacy
  and hash checks alone do not answer those questions.
  Date/Author: 2026-05-21 / Codex

- Decision: SuperCombo cannot become daily-answer numeric authority in this
  unit.
  Rationale: `docs/PLAN.md` and the Phase 1 roadmap require deterministic
  numeric answers to come from approved official/current-fact authority paths.
  SuperCombo starts as enrichment/cross-reference/candidate evidence only.
  Date/Author: 2026-05-21 / Codex

## Deviations

- None.

## Risks

- SuperCombo source URLs in `data/roster/current-character-roster.json` may be
  stale or redirected by the time acquisition runs.
- Future roster entries may lack `sources.supercombo_data`; acquisition
  validators must report those as coverage failures or review items.
- SuperCombo page structure may vary by character.
- Source-visible revision or update metadata may be absent.
- Full raw HTML may not be suitable for public repository storage without
  source-boundary review.
- Future public raw snapshot paths and schemas are intentionally unresolved in
  this plan.
- `stash@{0}` contains paused retrieval runtime work and must remain separate
  from this planning branch.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SuperCombo all-character raw snapshot acquisition planning | Planned scope from `data/roster/current-character-roster.json` only. | `docs/execplans/2026-05-21-supercombo-raw-snapshot-acquisition.md` | `git diff --check` | Pass | None | Mandatory review pending | Source URLs may be stale |
| Enrichment/candidate-only authority boundary | Preserved SuperCombo as enrichment, cross-reference, or candidate evidence only. | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | No schema or validator yet | Later implementation must enforce policy |
| Raw preservation and artifact boundary | Planned Git-outside transient workspace, public extracted-row default, and source-boundary gate for full raw HTML. | Same | Review | Pending | None | No implementation yet | Public raw path unresolved |
| Manifest and hash requirements | Planned metadata, manifest, and SHA-256 requirements with `daily_answer_numeric_authority: false`. | Same | Review | Pending | None | No implementation yet | Future validator needed |
