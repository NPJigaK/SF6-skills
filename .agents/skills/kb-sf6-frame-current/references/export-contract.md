# Export Contract

Supported baseline characters for this skill are `jp` and `luke`.

## Files

- `data/exports/<character_slug>/snapshot_manifest.json`
  - Publish index for the current supported character dataset set.
  - Check each dataset's `publication_state`, `published_run_id`, `published_snapshot_ids`, and published counts.
- `data/exports/<character_slug>/official_raw.json`
  - Primary current-fact source.
  - Safe-only published official data.
- `data/exports/<character_slug>/derived_metrics.json`
  - Machine-derived helper values computed from `official_raw`.
  - Safe-only published derived data.
- `data/exports/<character_slug>/supercombo_enrichment.json`
  - Supplemental third-party enrichment only.
  - Published main is anchored to published `official_raw` safe rows by `move_id`.
  - Read only when `snapshot_manifest.json` says it is `available`.
- `*_manual_review.*`
  - Review-only sidecars with fixed schema.
  - For `supercombo_enrichment`, this includes every row withheld from main, including missing-official-anchor rows.
  - Do not use for normal answers.

## Lookup Order

1. Read `snapshot_manifest.json`.
2. Read `official_raw.json`.
3. Join `derived_metrics.json` by `move_id` if derived values are needed.
4. Join `supercombo_enrichment.json` by `move_id` only when available and only after matching `official_raw.json`.

## Source Policy

- `official_raw` is the source of truth and maps to the repo's T1 preference.
- `derived_metrics` is acceptable only because it is computed mechanically from `official_raw`.
- `supercombo_enrichment` is T3 supplemental data. Never let it override official.
- Absence from `supercombo_enrichment.json` does not imply no source row existed; it may have been withheld into `*_manual_review.*`.

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
- If a requested value exists only in `manual_review` outputs, answer `[保留]`.
- If the user asks to audit parser behavior, selector drift, or ingestion state, leave this skill and inspect `data/normalized/...` or `data/raw/...` directly.
