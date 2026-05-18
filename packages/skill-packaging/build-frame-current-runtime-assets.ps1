Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$sourceRootRelativePath = 'data/exports'
$assetRootRelativePath = 'runtime/frame-current'
$compatibilityAssetRootRelativePath = 'skills/sf6-agent/assets/frame-current'
$rosterSourceRelativePath = 'data/roster/current-character-roster.json'
$generatorRelativePath = 'packages/skill-packaging/build-frame-current-runtime-assets.ps1'

$rosterPath = Join-Path $repoRoot $rosterSourceRelativePath
if (-not (Test-Path -LiteralPath $rosterPath -PathType Leaf)) {
  throw "Missing canonical roster source: $rosterSourceRelativePath"
}

$roster = Get-Content -LiteralPath $rosterPath -Raw | ConvertFrom-Json
$characters = @($roster.characters.character_slug)
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

function Write-FrameCurrentRuntimeAssets {
  param([Parameter(Mandatory = $true)][string]$TargetRootRelativePath)

  $assetRoot = Join-Path $repoRoot $TargetRootRelativePath
  $publishedRoot = Join-Path $assetRoot 'published'
  $runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'

  if (Test-Path -LiteralPath $assetRoot) {
    Remove-Item -LiteralPath $assetRoot -Recurse -Force
  }

  New-Item -ItemType Directory -Path $assetRoot -Force | Out-Null
  New-Item -ItemType Directory -Path $publishedRoot -Force | Out-Null

  $runtimeManifest = [ordered]@{
    generated = $true
    schema_version = 'frame-current-runtime-manifest/v1'
    kind = 'frame_current_runtime_manifest'
    source_root = $sourceRootRelativePath
    asset_root = $TargetRootRelativePath
    roster_source = $rosterSourceRelativePath
    generator = $generatorRelativePath
    characters = @()
  }

  foreach ($characterSlug in $characters) {
    $sourceCharacterRoot = Join-Path $repoRoot (Join-Path $sourceRootRelativePath $characterSlug)
    $sourceSnapshotManifestPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'

    if (-not (Test-Path -LiteralPath $sourceSnapshotManifestPath -PathType Leaf)) {
      throw "Missing snapshot manifest: $sourceRootRelativePath/$characterSlug/snapshot_manifest.json"
    }

    $targetCharacterRoot = Join-Path $publishedRoot $characterSlug
    New-Item -ItemType Directory -Path $targetCharacterRoot -Force | Out-Null

    $targetSnapshotManifestPath = Join-Path $targetCharacterRoot 'snapshot_manifest.json'
    Copy-Item -LiteralPath $sourceSnapshotManifestPath -Destination $targetSnapshotManifestPath -Force

    $snapshotManifest = Get-Content -LiteralPath $sourceSnapshotManifestPath -Raw | ConvertFrom-Json
    $fileRecords = @(
      [ordered]@{
        target = 'published/' + $characterSlug + '/snapshot_manifest.json'
        source = $sourceRootRelativePath + '/' + $characterSlug + '/snapshot_manifest.json'
        sha256 = (Get-FileHash -LiteralPath $targetSnapshotManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
      }
    )

    foreach ($datasetName in $datasets) {
      $datasetManifest = $snapshotManifest.datasets.$datasetName
      if ($null -eq $datasetManifest) {
        throw "Missing dataset entry in snapshot manifest: $characterSlug/$datasetName"
      }

      if ($datasetManifest.publication_state -eq 'available') {
        $sourceDatasetPath = Join-Path $sourceCharacterRoot "$datasetName.json"
        if (-not (Test-Path -LiteralPath $sourceDatasetPath -PathType Leaf)) {
          throw "Missing published dataset: $sourceRootRelativePath/$characterSlug/$datasetName.json"
        }

        $targetDatasetPath = Join-Path $targetCharacterRoot "$datasetName.json"
        Copy-Item -LiteralPath $sourceDatasetPath -Destination $targetDatasetPath -Force

        $fileRecords += [ordered]@{
          target = 'published/' + $characterSlug + '/' + $datasetName + '.json'
          source = $sourceRootRelativePath + '/' + $characterSlug + '/' + $datasetName + '.json'
          sha256 = (Get-FileHash -LiteralPath $targetDatasetPath -Algorithm SHA256).Hash.ToLowerInvariant()
        }
      }
    }

    $runtimeManifest.characters += [ordered]@{
      character_slug = $characterSlug
      files = $fileRecords
    }
  }

  $runtimeManifestJson = ((($runtimeManifest | ConvertTo-Json -Depth 8) -replace "`r`n", "`n").TrimEnd() + "`n")
  [System.IO.File]::WriteAllText($runtimeManifestPath, $runtimeManifestJson, $utf8NoBom)
}

Write-FrameCurrentRuntimeAssets $assetRootRelativePath
Write-FrameCurrentRuntimeAssets $compatibilityAssetRootRelativePath

Write-Host 'Frame-current runtime assets built'
