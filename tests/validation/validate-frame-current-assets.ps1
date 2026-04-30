Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$assetRoot = Join-Path $repoRoot 'skills/sf6-agent/assets/frame-current'
$rosterPath = Join-Path $repoRoot 'data/roster/current-character-roster.json'
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (-not (Test-Path -LiteralPath $assetRoot -PathType Container)) {
  throw 'Missing frame-current asset root: skills/sf6-agent/assets/frame-current'
}
if (-not (Test-Path -LiteralPath $rosterPath -PathType Leaf)) {
  throw 'Missing roster source: data/roster/current-character-roster.json'
}

$manifestPath = Join-Path $assetRoot 'runtime_manifest.json'
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
  throw 'Missing frame-current runtime_manifest.json'
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$roster = Get-Content -LiteralPath $rosterPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedCharacterSlugs = @($roster.characters.character_slug)

if ($manifest.source_root -ne 'data/exports') {
  throw 'runtime_manifest.json source_root must be data/exports'
}
if ($manifest.asset_root -ne 'skills/sf6-agent/assets/frame-current') {
  throw 'runtime_manifest.json asset_root must be skills/sf6-agent/assets/frame-current'
}
if ($manifest.roster_source -ne 'data/roster/current-character-roster.json') {
  throw 'runtime_manifest.json roster_source must be data/roster/current-character-roster.json'
}
if ((@($manifest.characters.character_slug) -join "`n") -ne ($expectedCharacterSlugs -join "`n")) {
  throw 'runtime_manifest.json character order must match data/roster/current-character-roster.json'
}

$actualInventory = @(
  Get-ChildItem -LiteralPath $assetRoot -Recurse -File |
    ForEach-Object { $_.FullName.Substring($assetRoot.Length + 1).Replace('\', '/') }
)
$expectedInventory = @('runtime_manifest.json')
$manifestEntries = @{}

foreach ($characterEntry in @($manifest.characters)) {
  foreach ($fileEntry in @($characterEntry.files)) {
    if ($manifestEntries.ContainsKey($fileEntry.target)) {
      throw "Duplicate manifest target: $($fileEntry.target)"
    }
    $manifestEntries[$fileEntry.target] = $fileEntry
  }
}

foreach ($characterSlug in $expectedCharacterSlugs) {
  $sourceCharacterRoot = Join-Path $repoRoot (Join-Path 'data/exports' $characterSlug)
  $snapshotPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'
  if (-not (Test-Path -LiteralPath $snapshotPath -PathType Leaf)) {
    throw "Missing source snapshot manifest: data/exports/$characterSlug/snapshot_manifest.json"
  }

  $snapshot = Get-Content -LiteralPath $snapshotPath -Raw -Encoding UTF8 | ConvertFrom-Json
  $expectedFiles = @(
    [ordered]@{
      target = "published/$characterSlug/snapshot_manifest.json"
      source = "data/exports/$characterSlug/snapshot_manifest.json"
      path = $snapshotPath
    }
  )

  foreach ($dataset in $datasets) {
    $datasetInfo = $snapshot.datasets.$dataset
    if ($null -eq $datasetInfo) {
      throw "Missing dataset state in snapshot manifest: $characterSlug/$dataset"
    }
    if ($datasetInfo.publication_state -eq 'available') {
      $expectedFiles += [ordered]@{
        target = "published/$characterSlug/$dataset.json"
        source = "data/exports/$characterSlug/$dataset.json"
        path = Join-Path $sourceCharacterRoot "$dataset.json"
      }
    }
  }

  foreach ($expectedFile in $expectedFiles) {
    $entry = $manifestEntries[$expectedFile.target]
    if ($null -eq $entry) {
      throw "Missing runtime manifest target: $($expectedFile.target)"
    }
    if ($entry.source -ne $expectedFile.source) {
      throw "Runtime manifest source mismatch for $($expectedFile.target)"
    }

    $packagedPath = Join-Path $assetRoot $expectedFile.target
    if (-not (Test-Path -LiteralPath $packagedPath -PathType Leaf)) {
      throw "Missing packaged runtime file: $($expectedFile.target)"
    }

    $sourceHash = (Get-FileHash -LiteralPath $expectedFile.path -Algorithm SHA256).Hash.ToLowerInvariant()
    $packagedHash = (Get-FileHash -LiteralPath $packagedPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($entry.sha256 -ne $sourceHash -or $entry.sha256 -ne $packagedHash) {
      throw "Runtime manifest hash mismatch for $($expectedFile.target)"
    }
  }

  $expectedInventory += $expectedFiles.target
}

$forbiddenPackaged = @($actualInventory | Where-Object { $_ -match '\.csv$|_manual_review\.' })
if ($forbiddenPackaged.Count -gt 0) {
  throw "Forbidden frame-current packaged files: $($forbiddenPackaged -join ', ')"
}

if (Compare-Object ($actualInventory | Sort-Object) ($expectedInventory | Sort-Object)) {
  throw 'Frame-current runtime inventory does not match generated expected inventory'
}

Write-Host 'Frame-current assets OK'
