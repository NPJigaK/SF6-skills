# Export Contract

Supported baseline characters for this skill are `jp` and `luke`.

## Files

- `assets/runtime_manifest.json`
  - Provenance map for the generated runtime package.
  - Records which files were copied from `data/exports/<character_slug>/`.
- `assets/published/<character_slug>/snapshot_manifest.json`
  - Publish index for the packaged dataset set.
  - Check each dataset's `publication_state`, `published_run_id`, `published_snapshot_ids`, and published counts.
- `assets/published/<character_slug>/official_raw.json`
  - Primary current-fact source.
  - Safe-only published official data.
- `assets/published/<character_slug>/derived_metrics.json`
  - Machine-derived helper values computed from `official_raw`.
  - Safe-only published derived data.
- `assets/published/<character_slug>/supercombo_enrichment.json`
  - Supplemental third-party enrichment only.
  - Packaged only when `snapshot_manifest.json` says it is `available`.

## Lookup Order

1. Read `assets/published/<character_slug>/snapshot_manifest.json`.
2. Read `assets/published/<character_slug>/official_raw.json`.
3. Join `assets/published/<character_slug>/derived_metrics.json` by `move_id` if derived values are needed.
4. Join `assets/published/<character_slug>/supercombo_enrichment.json` by `move_id` only when available and only after matching `official_raw.json`.

## Source Policy

- The packaged runtime assets are generated only from published exports under `data/exports/<character_slug>/`.
- `official_raw` is the source of truth and maps to the repo's T1 preference.
- `derived_metrics` is acceptable only because it is computed mechanically from `official_raw`.
- `supercombo_enrichment` is T3 supplemental data. Never let it override official.
- `*_manual_review.*`, `data/raw/...`, and `data/normalized/...` are intentionally excluded from the packaged runtime subset.

## Selection Rules

- If the user explicitly names a supported character, use that character.
- If strong thread context fixes the question to one supported character, infer it only when that inference is clear.
- Otherwise ask which supported character the user means.
- Do not silently default to `jp`.
- Prefer matching by exact `move_id` when it is already known.
- Otherwise match by `input`, then `move_name`.
- If multiple rows still match, do not guess. Ask for the exact variant or answer `[保留]`.

## Fallback Rules

- If the needed dataset is `unavailable`, say so and answer `[保留]`.
- If a requested value would require manual-review outputs that are not packaged with the skill, answer `[保留]`.
- If the user asks to audit parser behavior, selector drift, or ingestion state, leave this skill and inspect repo-local data directly.
