# Official Raw Snapshot Acquisition Planning

Status: Draft; planning-only ExecPlan.

## Purpose

Plan Phase 1 roadmap unit 2: official all-character raw snapshot acquisition.

This ExecPlan defines how a future implementation should acquire or refresh
official all-character raw snapshots while preserving exact raw source values
and authority boundaries. It does not implement fetching, Scrapling,
parsing, schemas, validators, retrieval, answer behavior, generated DBs, or
runtime changes.

## Scope

Included:

- Define official all-character acquisition scope from
  `data/roster/current-character-roster.json`.
- Define exact raw value preservation requirements.
- Define transient Git-outside acquisition workspace boundaries.
- Define reviewed public raw snapshot artifact boundaries.
- Define required source metadata for each character/source.
- Define manifest requirements for future official raw snapshots.
- Define hash requirements for reviewed raw snapshots.
- Define source freshness checks.
- Define locale, source-version, and patch metadata questions.
- Define privacy and no-local-path rules.
- Define validation strategy for future acquisition artifacts.
- Define how existing `data/exports/*/official_raw.json` relates to future
  snapshots.
- Preserve the authority/evidence policy from `docs/PLAN.md` and the Phase 1
  roadmap.

Excluded:

- No fetching implementation.
- No Scrapling dependency.
- No SuperCombo acquisition.
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

- The plan scopes official acquisition across every character in
  `data/roster/current-character-roster.json`.
- The plan states that missing `sources.official` entries are coverage failures
  or review items, not silent exclusions.
- The plan states that raw source values must be preserved exactly, including
  punctuation, whitespace-significant cell text, missing values, source labels,
  locale-specific text, and conditional notes.
- The plan separates transient Git-outside acquisition work from reviewed
  public raw snapshot artifacts.
- The plan adds a source-boundary gate before any full raw HTML or equivalent
  source document can be committed to the public repository.
- The plan defines the minimum source metadata required per character/source.
- The plan defines future manifest and hash requirements without implementing
  a schema.
- The plan defines source freshness checks and unresolved locale/source-version
  questions.
- The plan records privacy and no-local-path rules.
- The plan states that existing `data/exports/*/official_raw.json` remains the
  current daily-answer authority until a later approved workflow publishes a
  replacement.
- The plan states that official raw snapshots may become
  `current_fact_authority` only after deterministic acquisition,
  parser/schema validation, and review.
- Planning validation passes.

## Files / Interfaces

Changed by this ExecPlan:

- `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md`

Existing inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
- `data/roster/current-character-roster.json`
- `data/exports/README.md`

Future implementation artifacts are planned, not created here. A later
ExecPlan must approve exact paths, formats, schemas, and validators before any
new raw snapshot artifacts are committed.

## Official Acquisition Scope

The future official acquisition scope is all roster entries in
`data/roster/current-character-roster.json`.

Every roster character is in scope. If any roster entry lacks
`sources.official`, future acquisition must record that character as a coverage
failure or review item. It must not silently drop the character from the run.

For each roster character, future acquisition should record:

- `character_slug`
- `display_name`
- `official_url`
- `source_family`: `official`
- `source_role`: `current_fact_authority_candidate`
- `evidence_basis`: `official`
- `patch_sensitivity`: `high`
- `expected_content`: official SF6 frame/current-fact page
- `acquisition_candidate`: `scrapling`, subject to later verification

JP is one character in this all-character scope. It remains the initial active
character package for product use, not a hardcoded global acquisition
assumption.

## Exact Raw Value Preservation

Future official acquisition must preserve source values exactly before any
normalization or interpretation.

Preserve exactly:

- Raw HTML or equivalent source document content selected for review.
- Raw table labels and section labels.
- Raw column/header labels.
- Raw row order and row grouping.
- Raw move names.
- Raw input notation.
- Raw cell values, including signs, dashes, parentheses, percent symbols,
  locale-specific text, conditional note text, punctuation, and null/missing
  distinctions.
- Raw notes and footnotes.
- Source-visible locale text.

Do not rewrite during acquisition:

- Frame values.
- Damage values.
- Scaling values.
- Punish/counter notes.
- Total/recovery expressions such as `全体 55`.
- Multihit or conditional expressions.
- Blank, missing, unknown, or source-empty cells.

Normalization, parsed values, canonical move identity, and authority promotion
belong to later schema/parser/review units.

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
<git-outside-cache-root>/sf6-knowledge-coach/official-raw/<run_id>/
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
data/sources/official/<run_id>/source-snapshot-manifest.json
data/sources/official/<run_id>/<character_slug>/source-rows.json
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

Full raw HTML or equivalent source documents may be listed as transient
Git-outside evidence refs, but public repository refs require the explicit
source-boundary approval described above.

## Required Source Metadata

Each future character/source record should include at minimum:

```yaml
official_source_metadata:
  character_slug: jp
  display_name: JP
  source_family: official
  source_role: current_fact_authority_candidate
  evidence_basis: official
  source_url: https://www.streetfighter.com/6/ja-jp/character/jp/frame
  locale: ja-jp
  captured_at: 2026-05-21T00:00:00Z
  acquisition_tool: scrapling | static_http | manual | other
  acquisition_tool_version: null
  request_method: GET
  source_version_label: null
  source_patch_label: null
  http_status: null
  content_type: null
  raw_artifact_refs: []
  content_hashes: {}
  review_status: acquired_unreviewed
```

`captured_at` must be UTC in the future implementation. Local timezone may be
recorded only as secondary metadata if needed.

## Manifest Requirements

A future official raw snapshot manifest should describe the whole acquisition
run and each character snapshot. It should be reviewable without opening every
raw artifact.

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
- `validation_status`

Minimum character-level manifest fields:

- `character_slug`
- `display_name`
- `source_url`
- `locale`
- `captured_at`
- `http_status`
- `coverage_status`
- `source_version_label`
- `source_patch_label`
- `raw_document_ref`
- `raw_document_sha256`
- `source_rows_ref`
- `source_rows_sha256`
- `raw_row_count`
- `extraction_warning_count`
- `missing_required_field_count`
- `review_status`

## Hash Requirements

Future reviewed raw snapshot artifacts must include deterministic hashes.

Hash rules:

- Use SHA-256 unless a later ExecPlan records a stronger project-wide choice.
- Hash raw source documents after byte-level capture, before interpretation.
- Hash extracted raw row artifacts after deterministic serialization.
- Include hashes in the manifest using repository-relative artifact refs.
- Recompute hashes in validation and fail on mismatch.
- Do not hash transient local paths as identity.

Hashing proves artifact integrity only. It does not prove that parsed values
are correct or that a source is current.

## Source Freshness Checks

Future acquisition must check whether each source is likely current before any
daily-answer authority promotion.

Freshness checks to plan for:

- Confirm the source URL resolves for every roster character.
- Record HTTP status and final URL after redirects.
- Record capture timestamp in UTC.
- Look for source-visible patch/version/date labels when available.
- Compare roster source URLs with `data/roster/current-character-roster.json`.
- Compare new official raw row counts with existing
  `data/exports/<character_slug>/snapshot_manifest.json` counts.
- Record added, removed, or renamed source rows as review items.
- Treat missing or ambiguous source freshness metadata as a review risk, not a
  blocker to raw capture.

Freshness checks do not authorize numeric answers by themselves.

## Locale, Source-Version, And Patch Questions

Unresolved questions for the future acquisition implementation:

- Is `ja-jp` the canonical official locale for raw capture, or should another
  locale also be captured for cross-checking?
- Does the official page expose a source version, build version, update date,
  or patch label in machine-readable or visible text?
- Do frame pages differ by locale beyond display text?
- Are all frame/current-fact tables available from static HTML, or is browser
  execution required?
- Are hidden tabs or interactive sections present, and how should their raw
  values be captured without losing source grouping?
- What is the expected behavior if a roster URL exists but no frame table is
  present?

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
publishing official raw snapshots.

Planned validation categories:

- Manifest structure validation.
- Artifact existence checks for repository-relative refs.
- SHA-256 recomputation.
- No local absolute paths.
- No credential/cookie/header leakage.
- Expected character coverage from `data/roster/current-character-roster.json`.
- Failure when a roster character has no `sources.official` and the run does
  not record a coverage failure or review item.
- Source URL coverage and duplicate URL detection.
- Source-boundary validation ensuring public artifacts do not include full raw
  HTML or equivalent source documents unless a later explicit approval records
  source terms, license, robots, and attribution review.
- Raw row count presence.
- Required raw field presence by source table when known.
- Raw-value preservation checks comparing raw rows to raw document extraction
  evidence where practical.
- Authority boundary checks ensuring raw snapshots are not treated as parsed
  daily-answer facts until later gates pass.

This ExecPlan does not add those validators.

## Relationship To Existing `data/exports`

Existing `data/exports/*/official_raw.json` remains the current checked-in
daily-answer numeric authority during this planning unit.

Future official raw snapshots may be used to refresh or replace
`data/exports/*/official_raw.json` only after later units approve:

- Raw snapshot artifact placement and validation.
- Current-fact schemas.
- Deterministic parsed-value classifier behavior.
- Official raw to normalized export generation.
- Review and promotion workflow.

Until then, future raw snapshots are acquisition evidence, not a change to
daily answer behavior.

## Authority And Evidence Policy

- Official raw snapshots may become `current_fact_authority` only after
  deterministic acquisition, parser/schema validation, and review.
- Raw source values must be preserved exactly.
- Manual review sidecars, prose, FTS, SuperCombo, and LLM memory are not
  numeric authority.
- This unit must not change daily answer behavior.
- Conflicts between future official raw snapshots and existing exports become
  review items, not automatic replacements.

## Validation Commands

Run from the repository root:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-21 JST) Verified PR #300 was merged into `main` with merge
  commit `4a6f7caf4a6662f0156469b7b7bff1650e3d29f0`.
- [x] (2026-05-21 JST) Verified main branch CI passed for merge commit
  `4a6f7caf4a6662f0156469b7b7bff1650e3d29f0`.
- [x] (2026-05-21 JST) Confirmed `stash@{0}` remains present and unapplied.
- [x] (2026-05-21 JST) Created branch
  `plan/official-raw-snapshot-acquisition` from updated `main`.
- [x] (2026-05-21 JST) Reviewed current-fact acquisition inventory plan,
  Phase 1 roadmap, `data/roster/current-character-roster.json`, and
  `data/exports/README.md`.
- [x] (2026-05-21 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-21 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [ ] Mandatory review.

## Decision Log

- Decision: This unit plans official raw snapshot acquisition only.
  Rationale: The Phase 1 roadmap separates official acquisition from
  SuperCombo acquisition so official authority candidates remain distinct from
  enrichment/cross-reference/candidate evidence.
  Date/Author: 2026-05-21 / Codex

- Decision: Use `data/roster/current-character-roster.json` as the acquisition
  scope seed.
  Rationale: It is the retained character-agnostic roster surface with official
  source URLs for all current roster characters. Future acquisition must still
  verify live source availability and freshness.
  Date/Author: 2026-05-21 / Codex

- Decision: Keep future transient acquisition output Git-outside by default.
  Rationale: Fetch diagnostics, caches, and raw debugging output are not
  reviewed public artifacts and may contain local paths or tool noise.
  Date/Author: 2026-05-21 / Codex

- Decision: Public raw snapshots require explicit reviewed artifact boundaries
  before commit.
  Rationale: Raw captures are public data surfaces with authority implications;
  paths, manifests, hashes, and validators must be approved before publishing.
  Date/Author: 2026-05-21 / Codex

- Decision: Existing `data/exports/*/official_raw.json` remains the current
  daily-answer authority until a later promotion workflow replaces it.
  Rationale: This planning unit must not change daily answer behavior, and raw
  snapshots alone are not parsed, validated current-fact records.
  Date/Author: 2026-05-21 / Codex

- Decision: Public raw snapshot artifacts default to extracted raw rows,
  metadata, manifests, and hashes; full raw HTML remains Git-outside unless a
  later source-boundary review explicitly approves it.
  Rationale: Source terms, license, robots, attribution, and redistribution
  constraints must be reviewed before committing full source documents. Privacy
  and hash checks alone do not answer those questions.
  Date/Author: 2026-05-21 / Codex

- Decision: All roster characters are in acquisition scope even when a future
  roster entry lacks `sources.official`.
  Rationale: Missing official URLs should be visible coverage failures or
  review items, not silent exclusions that make all-character validation look
  complete.
  Date/Author: 2026-05-21 / Codex

## Deviations

- None.

## Risks

- Official source URLs in `data/roster/current-character-roster.json` may be
  stale or redirected by the time acquisition runs.
- Future roster entries may lack `sources.official`; acquisition validators
  must report those as coverage failures or review items.
- The official page may require browser execution rather than static HTTP
  capture.
- Full raw HTML may not be suitable for public repository storage without
  source-boundary review.
- Source-visible version or patch metadata may be absent.
- Exact raw value preservation may require source-specific extraction rules.
- Future public raw snapshot paths and schemas are intentionally unresolved in
  this plan.
- `stash@{0}` contains paused retrieval runtime work and must remain separate
  from this planning branch.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Official all-character raw snapshot acquisition planning | Planned scope from `data/roster/current-character-roster.json` only. | `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md` | `git diff --check` | Pass | None | Mandatory review pending | Source URLs may be stale |
| Raw preservation and artifact boundary | Planned Git-outside transient workspace, public extracted-row default, and source-boundary gate for full raw HTML. | Same | Review | Pending | None | No schema or validator yet | Public raw path unresolved |
| Manifest and hash requirements | Planned metadata, manifest, and SHA-256 requirements. | Same | Review | Pending | None | No implementation yet | Future validator needed |
| Authority/evidence policy | Preserved official-only authority candidate policy and daily-answer no-change rule. | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | No parser/schema gates yet | Later promotion workflow required |
