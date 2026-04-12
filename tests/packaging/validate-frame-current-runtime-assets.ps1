Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillRoot = Join-Path $repoRoot 'skills/kb-sf6-frame-current'
$assetRoot = Join-Path $skillRoot 'assets'
$rosterPath = Join-Path $repoRoot 'shared/roster/current-character-roster.json'
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (-not (Test-Path -LiteralPath $skillRoot -PathType Container)) {
  throw "Missing public skill root: skills/kb-sf6-frame-current"
}

if (-not (Test-Path -LiteralPath $rosterPath -PathType Leaf)) {
  throw 'Missing canonical roster source: shared/roster/current-character-roster.json'
}

$forbiddenFiles = @()
if (Test-Path -LiteralPath $assetRoot -PathType Container) {
  $forbiddenFiles = @(
    Get-ChildItem -LiteralPath $assetRoot -Recurse -File |
    Where-Object { $_.Extension -eq '.csv' -or $_.Name -like '*_manual_review.*' }
  )
}

if ($forbiddenFiles.Count -gt 0) {
  $relativeForbidden = $forbiddenFiles | ForEach-Object {
    $_.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  }
  throw "Forbidden packaged files found: $($relativeForbidden -join ', ')"
}

$runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'
if (-not (Test-Path -LiteralPath $runtimeManifestPath -PathType Leaf)) {
  throw 'Missing runtime manifest: runtime_manifest.json'
}

$runtimeManifest = Get-Content -LiteralPath $runtimeManifestPath -Raw | ConvertFrom-Json
$roster = Get-Content -LiteralPath $rosterPath -Raw | ConvertFrom-Json
$expectedCharacterSlugs = @($roster.characters.character_slug)

if ($runtimeManifest.source_root -ne 'data/exports') {
  throw "runtime_manifest.json source_root must be data/exports"
}

if ($runtimeManifest.skill_root -ne 'skills/kb-sf6-frame-current/assets') {
  throw "runtime_manifest.json skill_root must be skills/kb-sf6-frame-current/assets"
}

$characterSlugs = @($runtimeManifest.characters.character_slug)
if ($runtimeManifest.roster_source -ne 'shared/roster/current-character-roster.json') {
  throw "runtime_manifest.json roster_source must be shared/roster/current-character-roster.json"
}

if ((@($characterSlugs) -join "`n") -ne (@($expectedCharacterSlugs) -join "`n")) {
  throw "runtime_manifest.json characters must match shared/roster/current-character-roster.json"
}

$manifestEntries = @{}
foreach ($characterEntry in @($runtimeManifest.characters)) {
  foreach ($fileEntry in @($characterEntry.files)) {
    if ([string]::IsNullOrWhiteSpace($fileEntry.target) -or [string]::IsNullOrWhiteSpace($fileEntry.source) -or [string]::IsNullOrWhiteSpace($fileEntry.sha256)) {
      throw "runtime_manifest.json contains incomplete file entry"
    }

    if ($manifestEntries.ContainsKey($fileEntry.target)) {
      throw "Duplicate runtime_manifest.json target: $($fileEntry.target)"
    }

    $manifestEntries[$fileEntry.target] = [ordered]@{
      character_slug = $characterEntry.character_slug
      target = $fileEntry.target
      source = $fileEntry.source
      sha256 = $fileEntry.sha256
    }
  }
}

function Get-RelativePath {
  param(
    [Parameter(Mandatory = $true)]
    [string] $BasePath,
    [Parameter(Mandatory = $true)]
    [string] $FullPath
  )

  return $FullPath.Substring($BasePath.Length + 1).Replace('\', '/')
}

$expectedInventory = @('runtime_manifest.json')

foreach ($characterSlug in $expectedCharacterSlugs) {
  $sourceCharacterRoot = Join-Path $repoRoot (Join-Path 'data/exports' $characterSlug)
  $sourceSnapshotManifestPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'
  if (-not (Test-Path -LiteralPath $sourceSnapshotManifestPath -PathType Leaf)) {
    throw "Missing source snapshot manifest: data/exports/$characterSlug/snapshot_manifest.json"
  }

  $sourceSnapshotManifest = Get-Content -LiteralPath $sourceSnapshotManifestPath -Raw | ConvertFrom-Json
  $characterEntry = @($runtimeManifest.characters | Where-Object { $_.character_slug -eq $characterSlug } | Select-Object -First 1)
  if ($characterEntry.Count -ne 1) {
    throw "runtime_manifest.json missing character entry: $characterSlug"
  }

  $expectedFiles = @(
    [ordered]@{
      target = 'published/' + $characterSlug + '/snapshot_manifest.json'
      source = 'data/exports/' + $characterSlug + '/snapshot_manifest.json'
      sourcePath = $sourceSnapshotManifestPath
      packagedPath = Join-Path $assetRoot ('published/' + $characterSlug + '/snapshot_manifest.json')
    }
  )

  foreach ($datasetName in $datasets) {
    $datasetInfo = $sourceSnapshotManifest.datasets.$datasetName
    if ($null -eq $datasetInfo) {
      throw "Missing dataset entry in snapshot manifest: $characterSlug/$datasetName"
    }

    if ($datasetInfo.publication_state -eq 'available') {
      $expectedFiles += [ordered]@{
        target = 'published/' + $characterSlug + '/' + $datasetName + '.json'
        source = 'data/exports/' + $characterSlug + '/' + $datasetName + '.json'
        sourcePath = Join-Path $sourceCharacterRoot ($datasetName + '.json')
        packagedPath = Join-Path $assetRoot ('published/' + $characterSlug + '/' + $datasetName + '.json')
      }
    }
  }

  foreach ($expectedFile in $expectedFiles) {
    $runtimeRecord = $manifestEntries[$expectedFile.target]
    if ($null -eq $runtimeRecord) {
      throw "runtime_manifest.json missing target: $($expectedFile.target)"
    }

    if ($runtimeRecord.source -ne $expectedFile.source) {
      throw "runtime_manifest.json source mismatch for $($expectedFile.target)"
    }

    if (-not (Test-Path -LiteralPath $expectedFile.packagedPath -PathType Leaf)) {
      throw "Missing packaged file: $($expectedFile.target)"
    }

    $expectedHash = (Get-FileHash -LiteralPath $expectedFile.sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    $packagedHash = (Get-FileHash -LiteralPath $expectedFile.packagedPath -Algorithm SHA256).Hash.ToLowerInvariant()

    if ($runtimeRecord.sha256 -ne $expectedHash -or $runtimeRecord.sha256 -ne $packagedHash) {
      throw "runtime_manifest.json sha256 mismatch for $($expectedFile.target)"
    }

    if (-not $expectedFile.target.StartsWith('published/')) {
      throw "runtime_manifest.json target must be relative to skill_root: $($expectedFile.target)"
    }
  }

  $actualCharacterTargets = @($characterEntry.files.target)
  $expectedCharacterTargets = @($expectedFiles.target)
  if (Compare-Object ($actualCharacterTargets | Sort-Object) ($expectedCharacterTargets | Sort-Object)) {
    throw "runtime_manifest.json character inventory mismatch for $characterSlug"
  }

  foreach ($datasetName in $datasets) {
    $datasetInfo = $sourceSnapshotManifest.datasets.$datasetName
    $packagedDatasetPath = Join-Path $assetRoot ('published/' + $characterSlug + '/' + $datasetName + '.json')
    if ($datasetInfo.publication_state -ne 'available' -and (Test-Path -LiteralPath $packagedDatasetPath -PathType Leaf)) {
      throw "Packaged dataset exists despite non-available source state: $characterSlug/$datasetName"
    }
  }

  $expectedInventory += $expectedFiles.target
}

$actualInventory = @(
  Get-ChildItem -LiteralPath $assetRoot -Recurse -File | ForEach-Object {
    Get-RelativePath -BasePath $assetRoot -FullPath $_.FullName
  }
)

if (Compare-Object ($actualInventory | Sort-Object) ($expectedInventory | Sort-Object)) {
  throw 'Packaged inventory does not match the expected runtime subset'
}

Write-Host 'Frame-current runtime assets OK'
