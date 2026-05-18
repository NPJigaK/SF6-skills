# Frame-Current Runtime Assets Contract

Frame-current runtime assets are derived from `data/exports/` and `data/roster/`.
The primary runtime output is `runtime/frame-current/`. The legacy
`skills/sf6-agent/assets/frame-current/` path is a deferred public adapter
compatibility copy while that adapter remains.

## Layout

- `runtime/frame-current/runtime_manifest.json`
- `runtime/frame-current/published/<character_slug>/snapshot_manifest.json`
- `runtime/frame-current/published/<character_slug>/official_raw.json`
- `runtime/frame-current/published/<character_slug>/derived_metrics.json`
- `runtime/frame-current/published/<character_slug>/supercombo_enrichment.json`

Compatibility copy while `skills/sf6-agent/` remains:

- `skills/sf6-agent/assets/frame-current/runtime_manifest.json`
- `skills/sf6-agent/assets/frame-current/published/<character_slug>/snapshot_manifest.json`
- `skills/sf6-agent/assets/frame-current/published/<character_slug>/official_raw.json`
- `skills/sf6-agent/assets/frame-current/published/<character_slug>/derived_metrics.json`
- `skills/sf6-agent/assets/frame-current/published/<character_slug>/supercombo_enrichment.json`

## Rules

- Copy JSON files only when the source dataset is publishable.
- Exclude CSV sidecars, raw snapshots, normalized intermediate files, and manual-review outputs.
- Preserve source path and hash provenance in `runtime_manifest.json`.
- Keep official published rows as the final authority for exact current facts.
