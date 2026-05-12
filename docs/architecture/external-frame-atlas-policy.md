# External Frame Atlas Policy

## Purpose

This document plans how external SF6 frame and hitbox atlas sources may support
Codex/Hermes video analysis. It is planning and policy documentation only.

External frame and hitbox atlas sources may support SF6 video observation,
candidate move identification, move frequency aggregation, hit/block/whiff
observation, winning/losing phase comparison, and `official_raw` consistency
checks.

External visual atlas sources are visual reference inputs only. They are not
exact current-fact authority, they do not replace packaged `official_raw`, and
they do not become public `sf6-agent` answer behavior by default.

This policy does not scrape, download, cache, store, authorize, or redistribute
external visual assets.

## Background

SF6 video analysis can become stronger if Codex or Hermes can compare match
footage against visual references for each move.

Potential external visual sources include:

- move GIFs
- per-frame move images
- hitbox-overlay animations
- clean/no-hitbox move animations
- sprite sheets
- frame atlases
- frame-numbered visual references
- locally extracted frame sequences
- visual descriptors derived from local cache

These assets differ from text frame-data tables. GIFs, images, sprite sheets,
and frame atlases may be copyrighted, large, stale, difficult to diff in Git,
and unsafe to include in public bundles. Planning is required before
collection, caching, storage, descriptor extraction, or analysis implementation
begins.

## Relationship To Existing Work

This policy:

- builds on #103 video observation planning
- aligns with #123 SF6 video-analysis protocol
- should inform #120 Codex-Hermes pack resources and guards
- should inform #115 Codex-to-Hermes dry-run delegation fixtures
- should align with #121 Hermes CLI capability reference
- must preserve #114 invariants

The relevant #114 invariants are:

- Codex remains the repo implementation entrypoint.
- Hermes is optional repo-local growth delegation support.
- `skills/sf6-agent/` remains the public answer adapter.
- Hermes output remains draft input.
- Stale PRs, old branches, and old observations are not active
  implementation sources.

## External Frame And Hitbox Atlas Sources

External frame and hitbox atlas sources are visual reference inputs, not repo
authority.

Examples include:

- move GIFs
- per-frame move images
- hitbox-overlay animations
- clean/no-hitbox move animations
- sprite sheets or frame atlases
- frame-numbered visual references
- locally extracted frame sequences
- visual descriptors derived from local cache

They may support review and observation. They must not become:

- exact current-fact authority
- official frame-data authority
- replacement for packaged `official_raw`
- public `sf6-agent` answer behavior
- canonical SF6 knowledge by default

## Candidate Source Roles

External visual source roles must stay narrow:

- SF6Frames is a primary candidate for visual hitbox and hurtbox frame-atlas
  reference, not a numeric frame-data ingestion source.
- Ultimate Frame Data is a candidate broad move-table and hitbox image
  reference source for source evaluation and cross-check context only, not a
  numeric frame-data ingestion source in this policy.
- Packaged `official_raw` remains current-fact authority.
- SuperCombo, when referenced by existing repo workflows, is an auxiliary
  text/reference source only and is not an external visual atlas source by
  default.

## Dual Visual Variants

### Hitbox-Overlay Variant

Use hitbox-overlay variants for:

- human review
- spacing explanation
- active and hurtbox visual discussion
- observation review support
- explaining why a candidate interaction may matter

Do not use hitbox-overlay variants for:

- direct match-video template matching as the primary method
- exact frame fact authority
- `official_raw` override

### Clean/No-Hitbox Visual Variant

Use clean or no-hitbox visual variants for:

- match-video visual similarity
- candidate move identification
- motion or pose comparison
- move usage counting support

Do not use clean or no-hitbox variants for:

- exact move confirmation without review
- exact startup, active, or recovery inference
- exact hit, block, or whiff conclusion without uncertainty
- current-system authority

## Numeric Frame-Data Boundary

External visual atlas sources must not be used as new numeric frame-data
ingestion sources in this policy.

External visual atlas sources may provide visual reference support, frame
labels, animation frame counts, or review hints. Do not ingest startup,
active, recovery, total frames, hit advantage, block advantage, damage,
invulnerability, or patch values as authoritative data through this policy.

Packaged `official_raw` remains the current-fact authority. If numeric values
from an external visual source appear to conflict with packaged
`official_raw`, the result is a consistency review item, hold, or frame-data
refresh workflow, not automatic replacement.

## Storage Options And Policy

### External Link Only

External link only storage records source URL and metadata without storing
binary assets.

This is the safest default. The weakness is that the source may change or
disappear.

### Repo-External Local Cache

Repo-external local cache stores GIF, image, or frame assets outside the repo.

This can support personal analysis and repeatability, but it must be ignored
by Git, must not become canonical, and must not enter public bundles.

### Manifest + Hash Only

Manifest + hash storage records source metadata, retrieved date, hashes,
dimensions, frame counts, and cache policy without storing binary assets.

This is a good repo-managed representation and is the preferred initial
direction.

### Git LFS

Git LFS is allowed only if explicit permission and separate scope exist. It
must not be enabled casually and must be excluded from the public `sf6-agent`
bundle unless explicitly approved.

### Separate Dataset Repo

A separate dataset repo is a possible future direction only if binary storage
is legally and operationally approved. It must have its own license, storage,
and bundle boundaries, and is not part of this issue.

### Recommended Default

The default policy is:

- the repo stores metadata, manifest, descriptor, hash, and freshness metadata
  only
- binary assets stay in repo-external cache by default
- binary repo storage requires a future explicit permission, storage, LFS, or
  dataset decision

## Source Manifest Expectations

Future source manifests should include:

- `schema_version`
- `source_id`
- `source_name`
- `source_url`
- `source_owner`
- `source_credit`
- `permission_status`
- `license_status`
- `redistribution_status`
- `character_slug`
- `move_id`
- `move_name`
- `variant_type`
  - `hitbox_overlay`
  - `clean_visual`
  - `unknown`
- `asset_type`
  - `gif`
  - `png_sequence`
  - `webp`
  - `sprite_sheet`
  - `frame_sequence`
  - `metadata_only`
- `retrieved_at`
- `last_checked`
- `source_freshness_note`
- `patch_context`
- `frame_count`
- `fps_assumption`
- `dimensions`
- `asset_sha256`
- `perceptual_hash`
- `feature_descriptor_policy`
- `local_cache_policy`
- `local_cache_path_policy`
- `not_current_fact_authority`
- `may_override_official_raw`
- `public_bundle_allowed`
- `analysis_use`
- `forbidden_use`
- `numeric_frame_data_ingestion_allowed`
- `official_raw_consistency_check`
  - `not_checked`
  - `consistent`
  - `inconsistent`
  - `inconclusive`
- `consistency_review_notes`
- `frame_count_source`
  - `visual_frame_count`
  - `visible_frame_labels`
  - `source_claim`
  - `unknown`

Required boundary values:

- `not_current_fact_authority: true`
- `may_override_official_raw: false`
- `public_bundle_allowed: false` by default
- `numeric_frame_data_ingestion_allowed: false` by default
- `permission_status` must be explicit
- `license_status` must be explicit
- `redistribution_status` must be explicit before any binary storage decision

Binary-derived fields such as `asset_sha256`, `perceptual_hash`,
`frame_count`, `dimensions`, and some `fps_assumption` values are conditional.
They may be null until an approved repo-external cache or dataset workflow
obtains the asset under explicit scope and permission review. Their presence
must not imply that this issue authorizes fetching, downloading, storing, or
redistributing binary assets.

## Repo-External Cache Policy

Fetching on every analysis run is discouraged.

Future local cache workflows should:

- fetch only during explicit cache-sync or refresh workflow
- respect source terms, robots, rate limits, and attribution
- store assets outside the repo
- record local cache path only in non-canonical local state or approved
  manifest format
- never commit raw binary cache by default
- never include cache in public bundle
- support clean deletion and refresh
- record hash and freshness metadata when in scope
- mark cache as analysis support only

Suggested ignored paths for future implementation:

- `.external-cache/`
- `.external-assets/`
- `.local-media/`
- `.video-cache/`
- `.frame-atlas-cache/`

Actual `.gitignore` changes are not part of this issue unless explicitly
scoped in a later implementation issue.

## Refresh Workflow Relationship

Frame-data refresh may check external atlas metadata freshness.

Frame-data refresh must not:

- silently commit GIFs or images
- modify `frame-current`
- modify packaged `official_raw`
- change public `sf6-agent` answer behavior

Source manifest or hash updates may be committed only if explicitly in scope.
External visual cache sync is local and optional by default. Binary asset
storage requires a future explicit issue.

## Visual Atlas Consistency Check

Future workflows may compare visual atlas metadata against packaged
`official_raw`.

Allowed comparison inputs include:

- visual frame count
- visible frame labels
- animation date or patch/freshness notes
- move identifier
- variant type
- visible active, hitbox, or hurtbox frame ranges when available
- source metadata and hashes

The comparison output must be review status only:

- `consistent`
- `inconsistent`
- `inconclusive`
- `not_checked`

The comparison must not promote visual atlas data into exact current facts.
Inconsistent or inconclusive results require hold, reviewer notes, or a
frame-data refresh workflow.

## Video-Analysis Use Cases

Allowed future use cases include:

- candidate move identification
- candidate hit/block/whiff labeling
- move frequency aggregation
- winning/losing phase comparison
- round-state and score-state comparison
- player tendency analysis
- matchup observation support
- Hermes `video_analyze` result review
- human reviewer visual confirmation
- `official_raw` consistency check
- detecting possible source or patch mismatch for review

Example future analysis questions:

- Which moves did this player use most often?
- Which candidate moves hit most often?
- Which moves were blocked or punished?
- What changed between winning and losing rounds?
- Did the player use different moves while ahead or behind?
- Which observed interactions need official frame-data lookup?
- Are observed timings consistent, inconsistent, or inconclusive relative to
  packaged `official_raw`?

## Forbidden Uses

This policy forbids:

- scraping external sites in this issue
- downloading GIF or image assets in this issue
- committing scraped GIF or image collections by default
- storing raw video, frames, screenshots, contact sheets, browser cache, or
  full transcripts by default
- using external visual atlas assets as exact current-fact authority
- overriding packaged `official_raw`
- including external GIFs or images in public `sf6-agent` bundles
- inferring exact startup, active, or recovery from visual matching alone
- inferring exact current facts from video alone
- treating visual descriptor or perceptual hash matches as exact move
  confirmation without review
- importing external visual-source numeric frame values as authoritative
  current facts
- replacing official frame data with external visual-source frame counts
- treating visual frame counts as exact startup, active, or recovery values
  without an accepted review path
- treating observed damage labels as current-system authority
- treating training UI observations as current-system authority by default
- using stale external assets without freshness review
- using stale PR #83 or old issue #82 as active source material
- changing public `sf6-agent` behavior
- modifying frame-current assets
- adding runtime lookup or answer behavior
- adding computer vision matching code in this issue

## Future Observation Output Shape

Future observation artifacts that use external visual references should record
candidate status, confidence, what was directly observed, and what was not
inferred.

External visual reference observations must preserve the #123 source-fps
boundary: game-native 60fps assumptions are not the same as source-video fps,
and exact frame-window inference must hold when source fps, dropped frames,
edits, or playback speed are uncertain.

Example:

```json
{
  "observation_id": "match1-r1-0123-blanka-rolling-candidate",
  "source_video": "match1",
  "segment": "round1",
  "timestamp": "01:23.400-01:24.100",
  "source_video_fps": "unknown",
  "effective_fps": "unknown",
  "game_fps_assumption": 60,
  "frame_window": {
    "kind": "candidate_window",
    "notes": "Source fps is unknown; do not infer exact frame count."
  },
  "candidate_move": "blanka_rolling_attack",
  "candidate_move_confidence": "medium",
  "visual_reference": {
    "source_id": "external-frame-atlas-source",
    "variant_used": "clean_visual",
    "hitbox_variant_used_for_review": true
  },
  "observed_result_candidate": "blocked_candidate",
  "directly_observed": [
    "Blanka ball-like approach",
    "guard spark visible"
  ],
  "not_inferred": [
    "exact startup",
    "exact active frames",
    "exact recovery",
    "exact block advantage",
    "current-system frame fact"
  ],
  "official_raw_check": {
    "required": true,
    "status": "not_checked"
  },
  "review_status": "needs_review"
}
```

`candidate_move` is not final authority. Confidence is required.
`not_inferred` is required. `official_raw_check` is required for current facts.
Observations require review before promotion.

## Feature Descriptor Policy

Future perceptual hashes, embeddings, visual descriptors, or sprite sheets
derived from external assets require:

- explicit scope
- permission and license review
- non-reconstructive descriptor review where applicable
- no public bundle inclusion by default
- source and freshness metadata
- no exact current-fact authority
- validator boundaries

Do not assume perceptual hashes or embeddings are automatically safe to
publish.

## Public Bundle Policy

External frame and hitbox visual assets must not be included in the public
`sf6-agent` release bundle by default.

Future validators should check public bundle paths for:

- `.gif`
- `.png` frame dumps
- `.webp` atlas images
- `.mp4`
- screenshots
- contact sheets
- external visual cache
- extracted frame directories

## Future Issue Sequence

Recommended future issue sequence:

1. Add external frame-atlas source manifest schema.
2. Add external frame-atlas source manifest fixtures.
3. Add repo-external local cache workflow documentation.
4. Add validator preventing GIF, image, or video atlas assets from entering
   the repo or public bundle.
5. Add refresh workflow integration for manifest, hash, and freshness metadata
   only.
6. Add dry-run video observation fixture using external atlas metadata only.
7. Add optional local cache sync script, disabled from CI.
8. Explore reviewed feature descriptors if legally and technically safe.
9. Explore candidate move-recognition pipeline after policy, validator, and
   cache boundaries are accepted.
10. Explore move frequency aggregation only after candidate observation schema
    and review workflow exist.

## Non-Goals

This policy does not implement #120, #115, or #119. It does not scrape Ultimate
Frame Data, SF6Frames, or any other site. It does not download external GIFs or
images, commit GIFs or images, create sprite sheets, add Git LFS assets, add a
dataset repo, add computer vision matching code, implement move-frequency
analytics, modify public `sf6-agent` behavior, modify frame-current assets,
modify normalization assets, treat external atlas data as exact current-fact
authority, override packaged `official_raw`, use external assets without
permission/freshness review, store raw match videos, screenshots, contact
sheets, browser cache, or full transcripts, revive stale PR #83 or old issue
#82 as active input, modify generated outputs, modify `.dist`, or rewrite
historical smoke reports.
