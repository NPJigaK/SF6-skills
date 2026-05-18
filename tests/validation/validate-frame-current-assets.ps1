Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$primaryAssetRootRelativePath = 'runtime/frame-current'
$compatibilityAssetRootRelativePath = 'skills/sf6-agent/assets/frame-current'
$sourceRootRelativePath = 'data/exports'
$rosterSourceRelativePath = 'data/roster/current-character-roster.json'
$generatorRelativePath = 'packages/skill-packaging/build-frame-current-runtime-assets.ps1'
$rosterPath = Join-Path $repoRoot $rosterSourceRelativePath
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (-not (Test-Path -LiteralPath $rosterPath -PathType Leaf)) {
  throw "Missing roster source: $rosterSourceRelativePath"
}

$roster = Get-Content -LiteralPath $rosterPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedCharacterSlugs = @($roster.characters.character_slug)

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Assert-ManifestField {
  param(
    [Parameter(Mandatory = $true)][object]$Manifest,
    [Parameter(Mandatory = $true)][string]$Field,
    [Parameter(Mandatory = $true)][object]$ExpectedValue,
    [Parameter(Mandatory = $true)][string]$Context
  )

  if (-not (Test-Property $Manifest $Field)) {
    throw "$Context missing runtime_manifest.json field: $Field"
  }
  if ($Manifest.$Field -ne $ExpectedValue) {
    throw "$Context runtime_manifest.json $Field must be $ExpectedValue"
  }
}

function Get-AssetInventory {
  param([Parameter(Mandatory = $true)][string]$AssetRoot)

  return @(
    Get-ChildItem -LiteralPath $AssetRoot -Recurse -File |
      ForEach-Object { $_.FullName.Substring($AssetRoot.Length + 1).Replace('\', '/') }
  )
}

function Assert-FrameCurrentAssetRoot {
  param(
    [Parameter(Mandatory = $true)][string]$AssetRootRelativePath,
    [Parameter(Mandatory = $true)][string]$Context
  )

  $assetRoot = Join-Path $repoRoot $AssetRootRelativePath
  if (-not (Test-Path -LiteralPath $assetRoot -PathType Container)) {
    throw "Missing frame-current asset root ($Context): $AssetRootRelativePath"
  }

  $manifestPath = Join-Path $assetRoot 'runtime_manifest.json'
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Missing frame-current runtime_manifest.json ($Context)"
  }

  $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

  Assert-ManifestField $manifest 'generated' $true $Context
  Assert-ManifestField $manifest 'schema_version' 'frame-current-runtime-manifest/v1' $Context
  Assert-ManifestField $manifest 'kind' 'frame_current_runtime_manifest' $Context
  Assert-ManifestField $manifest 'source_root' $sourceRootRelativePath $Context
  Assert-ManifestField $manifest 'asset_root' $AssetRootRelativePath $Context
  Assert-ManifestField $manifest 'roster_source' $rosterSourceRelativePath $Context
  Assert-ManifestField $manifest 'generator' $generatorRelativePath $Context

  if ((@($manifest.characters.character_slug) -join "`n") -ne ($expectedCharacterSlugs -join "`n")) {
    throw "$Context runtime_manifest.json character order must match $rosterSourceRelativePath"
  }

  $actualInventory = Get-AssetInventory $assetRoot
  $expectedInventory = @('runtime_manifest.json')
  $manifestEntries = @{}

  foreach ($characterEntry in @($manifest.characters)) {
    foreach ($fileEntry in @($characterEntry.files)) {
      if ($manifestEntries.ContainsKey($fileEntry.target)) {
        throw "$Context duplicate manifest target: $($fileEntry.target)"
      }
      $manifestEntries[$fileEntry.target] = $fileEntry
    }
  }

  foreach ($characterSlug in $expectedCharacterSlugs) {
    $sourceCharacterRoot = Join-Path $repoRoot (Join-Path $sourceRootRelativePath $characterSlug)
    $snapshotPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'
    if (-not (Test-Path -LiteralPath $snapshotPath -PathType Leaf)) {
      throw "Missing source snapshot manifest: $sourceRootRelativePath/$characterSlug/snapshot_manifest.json"
    }

    $snapshot = Get-Content -LiteralPath $snapshotPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $expectedFiles = @(
      [ordered]@{
        target = "published/$characterSlug/snapshot_manifest.json"
        source = "$sourceRootRelativePath/$characterSlug/snapshot_manifest.json"
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
          source = "$sourceRootRelativePath/$characterSlug/$dataset.json"
          path = Join-Path $sourceCharacterRoot "$dataset.json"
        }
      }
    }

    foreach ($expectedFile in $expectedFiles) {
      $entry = $manifestEntries[$expectedFile.target]
      if ($null -eq $entry) {
        throw "$Context missing runtime manifest target: $($expectedFile.target)"
      }
      if ($entry.source -ne $expectedFile.source) {
        throw "$Context runtime manifest source mismatch for $($expectedFile.target)"
      }

      $packagedPath = Join-Path $assetRoot $expectedFile.target
      if (-not (Test-Path -LiteralPath $packagedPath -PathType Leaf)) {
        throw "$Context missing packaged runtime file: $($expectedFile.target)"
      }

      $sourceHash = (Get-FileHash -LiteralPath $expectedFile.path -Algorithm SHA256).Hash.ToLowerInvariant()
      $packagedHash = (Get-FileHash -LiteralPath $packagedPath -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($entry.sha256 -ne $sourceHash -or $entry.sha256 -ne $packagedHash) {
        throw "$Context runtime manifest hash mismatch for $($expectedFile.target)"
      }
    }

    $expectedInventory += $expectedFiles.target
  }

  $forbiddenPackaged = @($actualInventory | Where-Object { $_ -match '\.csv$|_manual_review\.' })
  if ($forbiddenPackaged.Count -gt 0) {
    throw "$Context forbidden frame-current packaged files: $($forbiddenPackaged -join ', ')"
  }

  if (Compare-Object ($actualInventory | Sort-Object) ($expectedInventory | Sort-Object)) {
    throw "$Context frame-current runtime inventory does not match generated expected inventory"
  }

  $expectedManifestTargets = @($expectedInventory | Where-Object { $_ -ne 'runtime_manifest.json' })
  if (Compare-Object (@($manifestEntries.Keys) | Sort-Object) ($expectedManifestTargets | Sort-Object)) {
    throw "$Context runtime manifest targets do not match expected generated inventory"
  }
}

function Assert-CompatibilityCopyMatchesPrimary {
  param(
    [Parameter(Mandatory = $true)][string]$PrimaryRootRelativePath,
    [Parameter(Mandatory = $true)][string]$CompatibilityRootRelativePath
  )

  $primaryRoot = Join-Path $repoRoot $PrimaryRootRelativePath
  $compatibilityRoot = Join-Path $repoRoot $CompatibilityRootRelativePath

  $primaryFiles = @(Get-AssetInventory $primaryRoot | Where-Object { $_ -ne 'runtime_manifest.json' })
  $compatibilityFiles = @(Get-AssetInventory $compatibilityRoot | Where-Object { $_ -ne 'runtime_manifest.json' })

  if (Compare-Object ($primaryFiles | Sort-Object) ($compatibilityFiles | Sort-Object)) {
    throw 'Frame-current compatibility copy inventory must match primary runtime output'
  }

  foreach ($relativePath in $primaryFiles) {
    $primaryHash = (Get-FileHash -LiteralPath (Join-Path $primaryRoot $relativePath) -Algorithm SHA256).Hash.ToLowerInvariant()
    $compatibilityHash = (Get-FileHash -LiteralPath (Join-Path $compatibilityRoot $relativePath) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($primaryHash -ne $compatibilityHash) {
      throw "Frame-current compatibility copy hash mismatch: $relativePath"
    }
  }
}

Assert-FrameCurrentAssetRoot $primaryAssetRootRelativePath 'primary runtime'
Assert-FrameCurrentAssetRoot $compatibilityAssetRootRelativePath 'legacy adapter compatibility copy'
Assert-CompatibilityCopyMatchesPrimary $primaryAssetRootRelativePath $compatibilityAssetRootRelativePath

Write-Host 'Frame-current assets OK'
