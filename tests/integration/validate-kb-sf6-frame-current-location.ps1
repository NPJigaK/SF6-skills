Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillRoot = Join-Path $repoRoot 'skills\kb-sf6-frame-current'

function Normalize-Content {
  param(
    [Parameter(Mandatory = $true)]
    [string] $Content
  )

  return ($Content -replace "`r`n", "`n").TrimEnd("`r", "`n")
}

foreach ($relativePath in @(
  'SKILL.md'
  'references\export-contract.md'
  'agents\openai.yaml'
)) {
  $fullPath = Join-Path $skillRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    throw "Missing frame-current public skill file: $relativePath"
  }
}

$expectedSkillContent = @'
---
name: kb-sf6-frame-current
description: Read generated runtime assets for the supported baseline characters (`jp`, `luke`) when the task needs exact or current move-specific values such as startup, active, recovery, total, hit or block advantage, cancel, damage, derived punish thresholds, or the current published snapshot status. Use together with kb-sf6-core when a question mixes concept explanation with current fact. Do not use for scraping, ingestion updates, manual review triage, or unsupported characters.
---

Read current facts for supported baseline characters from `assets/published/<character_slug>/` only.

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
2. Read `assets/published/<character_slug>/snapshot_manifest.json`.
3. Use only datasets whose `publication_state` is `available`.
4. Read `official_raw.json` from `assets/published/<character_slug>/` first.
5. Read `derived_metrics.json` only for machine-derived helper values.
6. Read `supercombo_enrichment.json` only if it is `available`, only after `official_raw.json`, and never let it override official.

## Answer Rules

- Use `[検証済み]` when the answer is grounded in packaged published exports.
- Use `[保留]` when the needed dataset or field is unavailable, ambiguous, or only present in manual-review outputs that are not packaged with the skill.
- When the user asks a concept question, explain the concept first and use `kb-sf6-core`.
- When official and supercombo differ, prefer official and describe supercombo as supplemental only.
- Mention the exact dataset used when it matters: `official_raw`, `derived_metrics`, or `supercombo_enrichment`.

## Safe-Use Rules

- `assets/runtime_manifest.json` records which published export files were copied into the skill package.
- `snapshot_manifest.json` is the required entrypoint.
- Use packaged published main exports only. They are safe-only and exclude withheld review rows.
- Treat packaged `supercombo_enrichment.json` as a supplemental subset anchored to packaged `official_raw.json` safe rows by `move_id`.
- Do not infer missing review data from the absence of packaged rows.
- Do not answer unsupported characters from this skill.

## References

- Read `references/export-contract.md` for file roles, lookup order, and fallback rules.
'@

$expectedExportContractContent = @'
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
- `*_manual_review.*`, `*.csv` sidecars, `data/raw/...`, and `data/normalized/...` are intentionally excluded from the packaged runtime subset.

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
- If the user asks to audit parser behavior, selector drift, or ingestion state, stop here and hand off to a repo-local maintainer workflow instead.
'@

$expectedOpenAiYamlContent = @'
interface:
  display_name: "SF6 Frame Current"
  short_description: "Read generated frame-data runtime assets for supported baseline current-fact answers."
  default_prompt: "Use $kb-sf6-frame-current to answer current-fact questions for the supported baseline characters (`jp`, `luke`) from generated runtime assets."
'@

$actualSkillContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'SKILL.md') -Raw)
$actualExportContractContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'references\export-contract.md') -Raw)
$actualOpenAiYamlContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'agents\openai.yaml') -Raw)

if ($actualSkillContent -ne (Normalize-Content $expectedSkillContent)) {
  throw 'Public frame-current SKILL.md must match the exact public-shell contract'
}

if ($actualExportContractContent -ne (Normalize-Content $expectedExportContractContent)) {
  throw 'Public frame-current export contract must match the exact published contract'
}

if ($actualOpenAiYamlContent -ne (Normalize-Content $expectedOpenAiYamlContent)) {
  throw 'Public frame-current agents/openai.yaml must match the exact agent contract'
}

Write-Host 'kb-sf6-frame-current public shell OK'
