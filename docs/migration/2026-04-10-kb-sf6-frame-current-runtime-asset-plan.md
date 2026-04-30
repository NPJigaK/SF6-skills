# KB-SF6 Frame Current Runtime Asset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move `kb-sf6-frame-current` into `skills/` as a public skill by shipping a generated JSON-only runtime asset subset derived from published exports for the supported baseline characters `jp` and `luke`.

**Architecture:** Keep `data/exports/<character_slug>/` as the repo-level source of truth, then generate a reduced distributable subset under `skills/kb-sf6-frame-current/assets/`. The public skill reads only its packaged assets, while `.agents/skills/kb-sf6-frame-current/` becomes a repo-local compatibility mirror produced by `scripts/dev/sync-dogfood-skills.ps1`.

**Tech Stack:** Markdown, PowerShell, Git, JSON, existing `data/exports` manifests, existing skill sync validators

---

## Planned File Map

**Create:**

- `E:\github\SF6-skills\packages\skill-packaging\README.md`
- `E:\github\SF6-skills\packages\skill-packaging\build-frame-current-runtime-assets.ps1`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\SKILL.md`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\references\export-contract.md`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\agents\openai.yaml`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\runtime_manifest.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\jp\snapshot_manifest.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\jp\official_raw.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\jp\derived_metrics.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\jp\supercombo_enrichment.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\luke\snapshot_manifest.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\luke\official_raw.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\luke\derived_metrics.json`
- `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\published\luke\supercombo_enrichment.json`
- `E:\github\SF6-skills\tests\packaging\validate-frame-current-runtime-assets.ps1`
- `E:\github\SF6-skills\tests\integration\validate-kb-sf6-frame-current-location.ps1`

**Modify:**

- `E:\github\SF6-skills\docs\architecture\kb-sf6-frame-current-packaging.md`
- `E:\github\SF6-skills\tests\integration\validate-frame-current-boundary.ps1`

**Generated compatibility output after sync:**

- `E:\github\SF6-skills\.agents\skills\kb-sf6-frame-current\SKILL.md`
- `E:\github\SF6-skills\.agents\skills\kb-sf6-frame-current\references\export-contract.md`
- `E:\github\SF6-skills\.agents\skills\kb-sf6-frame-current\agents\openai.yaml`
- `E:\github\SF6-skills\.agents\skills\kb-sf6-frame-current\assets\...`

## Runtime Asset Contract

This follow-up plan resolves the open packaging decision by choosing a generated runtime subset with these rules:

- Ship only JSON runtime files, not CSV sidecars.
- Ship only published main exports, never `*_manual_review.*`.
- Generate from `data/exports/<character_slug>/` only, never from `data/raw/...` or `data/normalized/...`.
- Keep `snapshot_manifest.json` plus available `official_raw.json`, `derived_metrics.json`, and `supercombo_enrichment.json`.
- Record the source file mapping and hashes in `skills/kb-sf6-frame-current/assets/runtime_manifest.json`.

### Task 1: Replace The Provisional Boundary Doc With The Resolved Contract

**Files:**

- Modify: `E:\github\SF6-skills\tests\integration\validate-frame-current-boundary.ps1`
- Modify: `E:\github\SF6-skills\docs\architecture\kb-sf6-frame-current-packaging.md`

- [ ] **Step 1: Rewrite the boundary validator so the old pre-migration doc fails**

Replace `tests/integration/validate-frame-current-boundary.ps1` with:

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$docPath = Join-Path $repoRoot 'docs\architecture\kb-sf6-frame-current-packaging.md'

if (-not (Test-Path -LiteralPath $docPath)) {
  throw "Missing boundary doc: $docPath"
}

$content = (Get-Content -LiteralPath $docPath -Raw).Replace("`r`n", "`n").Replace("`r", "`n")
$requiredHeadings = @(
  '## Runtime Asset Layout'
  '## Source Mapping'
  '## Regeneration'
  '## Publication Rules'
)

foreach ($heading in $requiredHeadings) {
  $pattern = '(?m)^' + [regex]::Escape($heading) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required heading: $heading"
  }
}

$requiredLines = @(
  '- `skills/kb-sf6-frame-current/assets/runtime_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/snapshot_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/official_raw.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/derived_metrics.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/supercombo_enrichment.json`'
  '- generated only from `data/exports/<character_slug>/...`'
  '- never from `data/raw/...` or `data/normalized/...`'
  '- exclude `*.csv` and `*_manual_review.*`'
  '- `powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1`'
  '- rerun after published exports change for `jp` or `luke`'
  '- only supported characters `jp`, `luke`'
  '- copy dataset files only when `publication_state = available`'
  '- `official_raw` remains the source of truth'
  '- `derived_metrics` remains official-only machine derivation'
  '- `supercombo_enrichment` remains supplemental and must never override official'
)

foreach ($line in $requiredLines) {
  $pattern = '(?m)^' + [regex]::Escape($line) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required contract line: $line"
  }
}

Write-Host 'Frame-current boundary doc OK'
```

- [ ] **Step 2: Run the boundary validator and verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1`  
Expected: FAIL because the current boundary doc still contains the provisional pre-migration decision.

- [ ] **Step 3: Replace the boundary doc with the resolved runtime asset contract**

Replace `docs/architecture/kb-sf6-frame-current-packaging.md` with:

```markdown
# kb-sf6-frame-current Packaging Boundary

## Runtime Asset Layout

- `skills/kb-sf6-frame-current/assets/runtime_manifest.json`
- `skills/kb-sf6-frame-current/assets/published/<character_slug>/snapshot_manifest.json`
- `skills/kb-sf6-frame-current/assets/published/<character_slug>/official_raw.json`
- `skills/kb-sf6-frame-current/assets/published/<character_slug>/derived_metrics.json`
- `skills/kb-sf6-frame-current/assets/published/<character_slug>/supercombo_enrichment.json`

## Source Mapping

- generated only from `data/exports/<character_slug>/...`
- never from `data/raw/...` or `data/normalized/...`
- exclude `*.csv` and `*_manual_review.*`

## Regeneration

- `powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1`
- rerun after published exports change for `jp` or `luke`

## Publication Rules

- only supported characters `jp`, `luke`
- copy dataset files only when `publication_state = available`
- `official_raw` remains the source of truth
- `derived_metrics` remains official-only machine derivation
- `supercombo_enrichment` remains supplemental and must never override official
```

- [ ] **Step 4: Run the boundary validator and verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1`  
Expected: PASS with `Frame-current boundary doc OK`.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/kb-sf6-frame-current-packaging.md tests/integration/validate-frame-current-boundary.ps1
git commit -m "docs: resolve frame-current runtime asset contract"
```

### Task 2: Create The Canonical Public Skill Shell

**Files:**

- Create: `E:\github\SF6-skills\tests\integration\validate-kb-sf6-frame-current-location.ps1`
- Create: `E:\github\SF6-skills\skills\kb-sf6-frame-current\SKILL.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-frame-current\references\export-contract.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-frame-current\agents\openai.yaml`

- [ ] **Step 1: Write the failing public-skill location validator**

Create `tests/integration/validate-kb-sf6-frame-current-location.ps1` with:

```powershell
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
```

- [ ] **Step 2: Run the location validator and verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`  
Expected: FAIL because `skills/kb-sf6-frame-current/` does not exist yet.

- [ ] **Step 3: Create the public skill shell**

Create `skills/kb-sf6-frame-current/SKILL.md` with:

```markdown
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
```

Create `skills/kb-sf6-frame-current/references/export-contract.md` with:

```markdown
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
```

Create `skills/kb-sf6-frame-current/agents/openai.yaml` with:

```yaml
interface:
  display_name: "SF6 Frame Current"
  short_description: "Read generated frame-data runtime assets for supported baseline current-fact answers."
  default_prompt: "Use $kb-sf6-frame-current to answer current-fact questions for the supported baseline characters (`jp`, `luke`) from generated runtime assets."
```

- [ ] **Step 4: Run the location validator and verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`  
Expected: PASS with `kb-sf6-frame-current public shell OK`.

- [ ] **Step 5: Commit**

```bash
git add tests/integration/validate-kb-sf6-frame-current-location.ps1 skills/kb-sf6-frame-current
git commit -m "feat: add frame-current public skill shell"
```

### Task 3: Add The Runtime Asset Generator And Materialize The Assets

**Files:**

- Create: `E:\github\SF6-skills\packages\skill-packaging\README.md`
- Create: `E:\github\SF6-skills\packages\skill-packaging\build-frame-current-runtime-assets.ps1`
- Create: `E:\github\SF6-skills\tests\packaging\validate-frame-current-runtime-assets.ps1`
- Create via generator: `E:\github\SF6-skills\skills\kb-sf6-frame-current\assets\...`

- [ ] **Step 1: Write the failing runtime-asset validator**

Create `tests/packaging/validate-frame-current-runtime-assets.ps1` with:

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$assetRoot = Join-Path $repoRoot 'skills\kb-sf6-frame-current\assets'
$runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'
$characters = @('jp', 'luke')
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (-not (Test-Path -LiteralPath $runtimeManifestPath -PathType Leaf)) {
  throw 'Missing runtime asset file: runtime_manifest.json'
}

$disallowed = Get-ChildItem -LiteralPath $assetRoot -Recurse -File | Where-Object {
  $_.Extension -eq '.csv' -or $_.Name -like '*_manual_review.*'
}
if ($disallowed.Count -gt 0) {
  $relativeDisallowed = $disallowed | ForEach-Object {
    $_.FullName.Substring($assetRoot.Length + 1).Replace('\', '/')
  }
  throw "Disallowed runtime assets present: $($relativeDisallowed -join ', ')"
}

$runtimeManifest = Get-Content -LiteralPath $runtimeManifestPath -Raw | ConvertFrom-Json
if ($runtimeManifest.source_root -ne 'data/exports') {
  throw 'runtime_manifest.json must record data/exports as the source root'
}
if ($runtimeManifest.skill_root -ne 'skills/kb-sf6-frame-current/assets') {
  throw 'runtime_manifest.json must record the public skill asset root'
}

$characterSet = @($runtimeManifest.characters | ForEach-Object { $_.character_slug })
if (($characterSet -join ',') -ne 'jp,luke') {
  throw "runtime_manifest.json must contain exactly jp and luke entries, got: $($characterSet -join ', ')"
}

$manifestEntries = @{}
foreach ($characterEntry in @($runtimeManifest.characters)) {
  foreach ($fileEntry in @($characterEntry.files)) {
    if ([string]::IsNullOrWhiteSpace($fileEntry.target) -or
        [string]::IsNullOrWhiteSpace($fileEntry.source) -or
        [string]::IsNullOrWhiteSpace($fileEntry.sha256)) {
      throw "runtime_manifest.json contains an incomplete file entry for character $($characterEntry.character_slug)"
    }

    if ($manifestEntries.ContainsKey($fileEntry.target)) {
      throw "runtime_manifest.json contains duplicate target entries: $($fileEntry.target)"
    }

    $manifestEntries[$fileEntry.target] = $fileEntry
  }
}

$expectedPackagedFiles = New-Object System.Collections.Generic.List[string]
$expectedPackagedFiles.Add('runtime_manifest.json') | Out-Null

foreach ($characterSlug in $characters) {
  $sourceCharacterRoot = Join-Path $repoRoot "data\exports\$characterSlug"
  $sourceSnapshotManifestPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'
  if (-not (Test-Path -LiteralPath $sourceSnapshotManifestPath -PathType Leaf)) {
    throw "Missing source snapshot manifest: $sourceSnapshotManifestPath"
  }

  $packagedSnapshotTarget = "published/$characterSlug/snapshot_manifest.json"
  $packagedSnapshotPath = Join-Path $assetRoot $packagedSnapshotTarget
  if (-not (Test-Path -LiteralPath $packagedSnapshotPath -PathType Leaf)) {
    throw "Missing packaged snapshot manifest: $packagedSnapshotTarget"
  }

  $expectedPackagedFiles.Add($packagedSnapshotTarget) | Out-Null
  if (-not $manifestEntries.ContainsKey($packagedSnapshotTarget)) {
    throw "runtime_manifest.json is missing target entry: $packagedSnapshotTarget"
  }

  $snapshotEntry = $manifestEntries[$packagedSnapshotTarget]
  if ($snapshotEntry.source -ne "data/exports/$characterSlug/snapshot_manifest.json") {
    throw "runtime_manifest.json has the wrong source for $packagedSnapshotTarget"
  }
  if ($snapshotEntry.sha256 -ne (Get-FileHash -LiteralPath $sourceSnapshotManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()) {
    throw "runtime_manifest.json has the wrong source hash for $packagedSnapshotTarget"
  }
  if ($snapshotEntry.sha256 -ne (Get-FileHash -LiteralPath $packagedSnapshotPath -Algorithm SHA256).Hash.ToLowerInvariant()) {
    throw "runtime_manifest.json has the wrong packaged hash for $packagedSnapshotTarget"
  }

  $sourceSnapshotManifest = Get-Content -LiteralPath $sourceSnapshotManifestPath -Raw | ConvertFrom-Json

  foreach ($datasetName in $datasets) {
    $datasetInfo = $sourceSnapshotManifest.datasets.$datasetName
    if ($null -eq $datasetInfo) {
      throw "Source snapshot manifest is missing dataset entry: $characterSlug/$datasetName"
    }

    $packagedDatasetTarget = "published/$characterSlug/$datasetName.json"
    $packagedDatasetPath = Join-Path $assetRoot $packagedDatasetTarget

    if ($datasetInfo.publication_state -eq 'available') {
      $sourceDatasetPath = Join-Path $sourceCharacterRoot "$datasetName.json"
      if (-not (Test-Path -LiteralPath $sourceDatasetPath -PathType Leaf)) {
        throw "Missing source dataset file: $sourceDatasetPath"
      }
      if (-not (Test-Path -LiteralPath $packagedDatasetPath -PathType Leaf)) {
        throw "Missing packaged dataset file: $packagedDatasetTarget"
      }

      $expectedPackagedFiles.Add($packagedDatasetTarget) | Out-Null
      if (-not $manifestEntries.ContainsKey($packagedDatasetTarget)) {
        throw "runtime_manifest.json is missing target entry: $packagedDatasetTarget"
      }

      $datasetEntry = $manifestEntries[$packagedDatasetTarget]
      if ($datasetEntry.source -ne "data/exports/$characterSlug/$datasetName.json") {
        throw "runtime_manifest.json has the wrong source for $packagedDatasetTarget"
      }
      if ($datasetEntry.target -notlike 'published/*') {
        throw "runtime_manifest.json target entries must stay relative to skill_root: $($datasetEntry.target)"
      }
      if ($datasetEntry.sha256 -ne (Get-FileHash -LiteralPath $sourceDatasetPath -Algorithm SHA256).Hash.ToLowerInvariant()) {
        throw "runtime_manifest.json has the wrong source hash for $packagedDatasetTarget"
      }
      if ($datasetEntry.sha256 -ne (Get-FileHash -LiteralPath $packagedDatasetPath -Algorithm SHA256).Hash.ToLowerInvariant()) {
        throw "runtime_manifest.json has the wrong packaged hash for $packagedDatasetTarget"
      }
    }
    elseif (Test-Path -LiteralPath $packagedDatasetPath -PathType Leaf) {
      throw "Packaged dataset should be absent when publication_state is not available: $packagedDatasetTarget"
    }
  }
}

$actualPackagedFiles = Get-ChildItem -LiteralPath $assetRoot -Recurse -File | ForEach-Object {
  $_.FullName.Substring($assetRoot.Length + 1).Replace('\', '/')
}

$expectedList = @($expectedPackagedFiles | Sort-Object)
$actualList = @($actualPackagedFiles | Sort-Object)
if ($expectedList.Count -ne $actualList.Count) {
  throw "Packaged runtime asset count mismatch: expected=$($expectedList.Count) actual=$($actualList.Count)"
}

for ($i = 0; $i -lt $expectedList.Count; $i++) {
  if ($expectedList[$i] -ne $actualList[$i]) {
    throw "Unexpected packaged runtime asset inventory mismatch at position $($i + 1): expected=$($expectedList[$i]) actual=$($actualList[$i])"
  }
}

Write-Host 'Frame-current runtime assets OK'
```

- [ ] **Step 2: Run the asset validator and verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-frame-current-runtime-assets.ps1`  
Expected: FAIL because the public skill has no generated assets yet.

- [ ] **Step 3: Create the packaging README and generator**

Create `packages/skill-packaging/README.md` with:

```markdown
# skill-packaging

Shared packaging scripts live here.

Current entrypoint:

- `build-frame-current-runtime-assets.ps1`
```

Create `packages/skill-packaging/build-frame-current-runtime-assets.ps1` with:

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillRoot = Join-Path $repoRoot 'skills\kb-sf6-frame-current'
$assetRoot = Join-Path $skillRoot 'assets'
$publishedRoot = Join-Path $assetRoot 'published'
$runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'
$characters = @('jp', 'luke')
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (-not (Test-Path -LiteralPath $skillRoot -PathType Container)) {
  throw "Missing public frame-current skill root: $skillRoot"
}

if (Test-Path -LiteralPath $publishedRoot) {
  Remove-Item -LiteralPath $publishedRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $publishedRoot | Out-Null

$runtimeManifest = [ordered]@{
  source_root = 'data/exports'
  skill_root = 'skills/kb-sf6-frame-current/assets'
  characters = @()
}

foreach ($character in $characters) {
  $sourceCharacterRoot = Join-Path $repoRoot "data\exports\$character"
  $targetCharacterRoot = Join-Path $publishedRoot $character
  $sourceSnapshotManifestPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'
  $targetSnapshotManifestPath = Join-Path $targetCharacterRoot 'snapshot_manifest.json'

  if (-not (Test-Path -LiteralPath $sourceSnapshotManifestPath -PathType Leaf)) {
    throw "Missing source snapshot manifest: $sourceSnapshotManifestPath"
  }

  New-Item -ItemType Directory -Force -Path $targetCharacterRoot | Out-Null
  Copy-Item -LiteralPath $sourceSnapshotManifestPath -Destination $targetSnapshotManifestPath -Force

  $snapshotManifest = Get-Content -LiteralPath $sourceSnapshotManifestPath -Raw | ConvertFrom-Json -AsHashtable
  $files = @(
    [ordered]@{
      target = "published/$character/snapshot_manifest.json"
      source = "data/exports/$character/snapshot_manifest.json"
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceSnapshotManifestPath).Hash
    }
  )

  foreach ($dataset in $datasets) {
    $datasetInfo = $snapshotManifest.datasets[$dataset]
    if ($null -eq $datasetInfo) {
      throw "snapshot_manifest.json missing dataset entry: $dataset"
    }

    if ($datasetInfo.publication_state -eq 'available') {
      $sourceDatasetPath = Join-Path $sourceCharacterRoot "$dataset.json"
      $targetDatasetPath = Join-Path $targetCharacterRoot "$dataset.json"

      if (-not (Test-Path -LiteralPath $sourceDatasetPath -PathType Leaf)) {
        throw "Missing published dataset file: $sourceDatasetPath"
      }

      Copy-Item -LiteralPath $sourceDatasetPath -Destination $targetDatasetPath -Force
      $files += [ordered]@{
        target = "published/$character/$dataset.json"
        source = "data/exports/$character/$dataset.json"
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceDatasetPath).Hash
      }
    }
  }

  $runtimeManifest.characters += [ordered]@{
    character_slug = $character
    files = $files
  }
}

$runtimeManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $runtimeManifestPath -Encoding utf8

Write-Host 'Frame-current runtime assets built'
```

- [ ] **Step 4: Generate the assets and run the validator**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-frame-current-runtime-assets.ps1
```

Expected:

- first command prints `Frame-current runtime assets built`
- second command prints `Frame-current runtime assets OK`

- [ ] **Step 5: Commit**

```bash
git add packages/skill-packaging/README.md packages/skill-packaging/build-frame-current-runtime-assets.ps1 tests/packaging/validate-frame-current-runtime-assets.ps1 skills/kb-sf6-frame-current/assets
git commit -m "feat: package frame-current runtime assets"
```

### Task 4: Replace The Legacy Repo-Local Copy With The Canonical Mirror

**Files:**

- Generated output: `E:\github\SF6-skills\.agents\skills\kb-sf6-frame-current\...`
- Modify: `E:\github\SF6-skills\scripts\dev\sync-dogfood-skills.ps1`
- Modify: `E:\github\SF6-skills\tests\install\validate-dogfood-mirror.ps1`
- Verify: `E:\github\SF6-skills\tests\install\validate-dogfood-mirror.ps1`
- Verify: `E:\github\SF6-skills\tests\integration\validate-kb-sf6-frame-current-location.ps1`
- Verify: `E:\github\SF6-skills\tests\packaging\validate-frame-current-runtime-assets.ps1`
- Verify: `E:\github\SF6-skills\tests\integration\validate-frame-current-boundary.ps1`

- [ ] **Step 1: Sync the repo-local compatibility mirror**

Before rerunning the sync, update the mirror tooling so `.agents/skills/` becomes a true root-level mirror of `skills/`:

- `scripts/dev/sync-dogfood-skills.ps1` must remove stale target skill directories whose names are present under `.agents/skills/` but not under `skills/`.
- `tests/install/validate-dogfood-mirror.ps1` must assert that the top-level directory set under `.agents/skills/` exactly matches the top-level directory set under `skills/` before checking per-skill inventory and hashes.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

Expected: PASS with `Synced 2 public skills to .agents/skills`.

- [ ] **Step 2: Run the migration verification set**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
python -m pytest ingest/frame_data/tests -q
```

Expected:

- `kb-sf6-frame-current public shell OK`
- `Frame-current runtime assets OK`
- `Frame-current boundary doc OK`
- `Dogfood mirror OK`
- `Distribution surface OK`
- `23 passed`

- [ ] **Step 3: Commit**

```bash
git add scripts/dev/sync-dogfood-skills.ps1 tests/install/validate-dogfood-mirror.ps1 .agents/skills/kb-sf6-frame-current
git commit -m "refactor: migrate frame-current to public skills surface"
```

## Spec Coverage Check

- Explicit generated runtime asset contract: covered by Tasks 1 and 3.
- Canonical public skill under `skills/`: covered by Task 2.
- Generated assets limited to published JSON exports: covered by Task 3.
- `.agents/skills/kb-sf6-frame-current` becomes compatibility output rather than authoritative source: covered by Task 4.
- Root `data/exports` remains source of truth: covered by Tasks 1 and 3.

## Placeholder Scan

- No implementation step depends on hand-written asset JSON. The plan generates those files via `build-frame-current-runtime-assets.ps1`.
- No task references unspecified file names or unspecified dataset subsets.

## Type And Naming Consistency

- Canonical public skill path is always `skills/kb-sf6-frame-current/`.
- Generated asset path is always `skills/kb-sf6-frame-current/assets/published/<character_slug>/`.
- Repo-local compatibility mirror path is always `.agents/skills/kb-sf6-frame-current/`.
- Generator entrypoint is always `packages/skill-packaging/build-frame-current-runtime-assets.ps1`.
