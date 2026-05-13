# External Frame Atlas Source Evaluation

This directory is metadata-only.

No external assets are fetched or stored here. The matrix evaluates source
suitability before any fetch, cache, scrape, manifest, binary, descriptor, or
runtime workflow.

SF6Frames and Ultimate Frame Data are visual reference candidates, not numeric frame-data ingestion sources.
They are not exact current-fact authority, and they do not override
`official_raw`.

Matrix statuses are recommendations or holds. They do not authorize scraping,
downloading, caching, hashing, redistributing, or storing external visual
assets. Binary storage and redistribution require later explicit permission,
storage scope, and validator coverage.

Normal public user answer generation must not scrape or cache SF6Frames,
Ultimate Frame Data, or other external atlas assets. Public `sf6-agent`
behavior is unchanged by this evaluation.

## Future Cache Boundary

Future maintainer-local cache sync, if ever implemented, must be:

- explicit
- repo-external
- disabled from CI
- excluded from public `sf6-agent` behavior and bundles
- respectful of source terms, robots, rate limits, and attribution
- validated against binary leakage
- non-canonical

Future cache feasibility is recorded only as evaluation metadata. A
`candidate` or `hold` status does not approve cache sync.

## Existing Fetch Tooling Alignment

This evaluation does not add a scraper, downloader, or cache-sync workflow.

If a later scoped issue approves maintainer-local external frame-atlas
acquisition, that workflow should first align with the existing
`ingest/frame_data` Scrapling-based fetch stack and fetch-profile discipline
rather than introducing a separate scraper dependency.

That future alignment does not authorize #138 to fetch or cache assets, and it
does not make external visual atlas binaries part of the checked-in frame-data
raw snapshot or published export surface. External visual atlas binaries remain repo-external by default and
non-canonical unless a later explicit permission and storage issue decides
otherwise.

## Authority Boundary

The matrix distinguishes visual reference candidates from current-fact
authority.

- `official_raw` remains the current-fact authority.
- External visual sources do not override `official_raw`.
- External visual sources do not provide authoritative numeric frame data.
- Conflicts with `official_raw` become review items, holds, or frame-data
  refresh prompts, not automatic replacements.

## Current Matrix

`source-evaluation-matrix.json` includes:

- SF6Frames
- Ultimate Frame Data
- maintainer-local captured references
- official/current-fact authority comparison boundary
- SuperCombo or equivalent non-visual reference context

The matrix intentionally avoids source-specific scrape selectors, direct asset
paths, local cache paths, asset hashes, dimensions, and frame counts that would
imply asset retrieval.
