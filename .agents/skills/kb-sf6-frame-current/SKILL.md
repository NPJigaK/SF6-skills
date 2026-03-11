---
name: kb-sf6-frame-current
description: Read published frame-data exports for the supported baseline characters (`jp`, `luke`) when the task needs exact or current move-specific values such as startup, active, recovery, total, hit or block advantage, cancel, damage, derived punish thresholds, or the current published snapshot status. Use together with kb-sf6-core when a question mixes concept explanation with current fact. Do not use for scraping, ingestion updates, manual review triage, or unsupported characters.
---

Read current facts for supported baseline characters from `data/exports/<character_slug>/` only.

## Supported Characters

- `jp`
- `luke`

## Character Resolution

1. If the user explicitly names a supported character, use that character.
2. If strong thread context fixes the question to one supported character, infer it only when that inference is clear.
3. Otherwise ask which character the user means.
4. Do not silently default to `jp`.

## Quick Start

1. Resolve `character_slug`.
2. Read `data/exports/<character_slug>/snapshot_manifest.json`.
3. Use only datasets whose `publication_state` is `available`.
4. Read `official_raw.json` first.
5. Read `derived_metrics.json` only for machine-derived helper values.
6. Read `supercombo_enrichment.json` only if it is `available`, only after `official_raw.json`, and never let it override official.

## Answer Rules

- Use `[検証済み]` when the answer is grounded in published exports.
- Use `[保留]` when the needed dataset or field is unavailable, ambiguous, or only present in manual-review outputs.
- When the user asks a concept question, explain the concept first and use `kb-sf6-core`.
- When official and supercombo differ, prefer official and describe supercombo as supplemental only.
- Mention the exact dataset used when it matters: `official_raw`, `derived_metrics`, or `supercombo_enrichment`.

## Safe-Use Rules

- `snapshot_manifest.json` is the required entrypoint.
- Use published main exports only. They are safe-only and exclude withheld review rows.
- Treat published `supercombo_enrichment` main as a supplemental subset anchored to published `official_raw` safe rows by `move_id`.
- Do not read `*_manual_review.*` for normal answers.
- Do not read `data/raw/...` or `data/normalized/...` for normal answers.
- Do not promote values out of `raw_row_json`.
- Do not answer unsupported characters from this skill.

## References

- Read `references/export-contract.md` for file roles, lookup order, and fallback rules.
