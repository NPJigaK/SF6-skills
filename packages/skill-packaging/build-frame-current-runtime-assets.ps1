$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillRoot = Join-Path $repoRoot 'skills/kb-sf6-frame-current/assets'
$assetRoot = $skillRoot
$publishedRoot = Join-Path $assetRoot 'published'
$runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'

$characters = @('jp', 'luke')
$datasets = @('official_raw', 'derived_metrics', 'supercombo_enrichment')

if (Test-Path -LiteralPath $publishedRoot) {
  Remove-Item -LiteralPath $publishedRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $assetRoot -Force | Out-Null
New-Item -ItemType Directory -Path $publishedRoot -Force | Out-Null

$runtimeManifest = [ordered]@{
  source_root = 'data/exports'
  skill_root = 'skills/kb-sf6-frame-current/assets'
  characters = @()
}

foreach ($characterSlug in $characters) {
  $sourceCharacterRoot = Join-Path $repoRoot (Join-Path 'data/exports' $characterSlug)
  $sourceSnapshotManifestPath = Join-Path $sourceCharacterRoot 'snapshot_manifest.json'

  if (-not (Test-Path -LiteralPath $sourceSnapshotManifestPath -PathType Leaf)) {
    throw "Missing snapshot manifest: data/exports/$characterSlug/snapshot_manifest.json"
  }

  $targetCharacterRoot = Join-Path $publishedRoot $characterSlug
  New-Item -ItemType Directory -Path $targetCharacterRoot -Force | Out-Null

  $targetSnapshotManifestPath = Join-Path $targetCharacterRoot 'snapshot_manifest.json'
  Copy-Item -LiteralPath $sourceSnapshotManifestPath -Destination $targetSnapshotManifestPath -Force

  $snapshotManifest = Get-Content -LiteralPath $sourceSnapshotManifestPath -Raw | ConvertFrom-Json
  $fileRecords = @(
    [ordered]@{
      target = 'skills/kb-sf6-frame-current/assets/published/' + $characterSlug + '/snapshot_manifest.json'
      source = 'data/exports/' + $characterSlug + '/snapshot_manifest.json'
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
        throw "Missing published dataset: data/exports/$characterSlug/$datasetName.json"
      }

      $targetDatasetPath = Join-Path $targetCharacterRoot "$datasetName.json"
      Copy-Item -LiteralPath $sourceDatasetPath -Destination $targetDatasetPath -Force

      $fileRecords += [ordered]@{
        target = 'skills/kb-sf6-frame-current/assets/published/' + $characterSlug + '/' + $datasetName + '.json'
        source = 'data/exports/' + $characterSlug + '/' + $datasetName + '.json'
        sha256 = (Get-FileHash -LiteralPath $targetDatasetPath -Algorithm SHA256).Hash.ToLowerInvariant()
      }
    }
  }

  $runtimeManifest.characters += [ordered]@{
    character_slug = $characterSlug
    files = $fileRecords
  }
}

$runtimeManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $runtimeManifestPath -Encoding utf8

Write-Host 'Frame-current runtime assets built'
