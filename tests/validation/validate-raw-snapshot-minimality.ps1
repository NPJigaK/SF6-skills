Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$datasetSourceMap = [ordered]@{
  official_raw = 'official'
  derived_metrics = 'official'
  supercombo_enrichment = 'supercombo'
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw 'git is required to validate checked-in raw snapshot minimality'
}

$trackedRawFiles = @(
  & git -C $repoRoot ls-files -- data/raw/official data/raw/supercombo |
    Where-Object { Test-Path -LiteralPath (Join-Path $repoRoot $_) -PathType Leaf }
)
if ($LASTEXITCODE -ne 0) {
  throw 'Unable to enumerate tracked raw snapshot files'
}

$trackedRawDirs = [System.Collections.Generic.HashSet[string]]::new()
$issues = @()

foreach ($relativePath in $trackedRawFiles) {
  $normalizedPath = $relativePath.Replace('\', '/')
  if ($normalizedPath -match '^data/raw/(official|supercombo)/([^/]+)/([^/]+)/(page\.html|metadata\.json)$') {
    [void]$trackedRawDirs.Add("data/raw/$($Matches[1])/$($Matches[2])/$($Matches[3])")
  }
  else {
    $issues += "Tracked raw snapshot file has unexpected layout: $normalizedPath"
  }
}

$referencedRawDirs = [System.Collections.Generic.HashSet[string]]::new()
$exportRoot = Join-Path $repoRoot 'data/exports'
if (-not (Test-Path -LiteralPath $exportRoot -PathType Container)) {
  throw 'Missing data/exports'
}

$manifestFiles = @(
  Get-ChildItem -LiteralPath $exportRoot -Recurse -File -Filter 'snapshot_manifest.json' |
    Sort-Object FullName
)

foreach ($manifestFile in $manifestFiles) {
  $manifestRelativePath = $manifestFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $characterSlug = Split-Path -Leaf (Split-Path -Parent $manifestFile.FullName)
  $manifest = Get-Content -LiteralPath $manifestFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json

  if ($manifest.character_slug -ne $characterSlug) {
    $issues += "$manifestRelativePath character_slug mismatch: $($manifest.character_slug) != $characterSlug"
    continue
  }

  foreach ($datasetName in $datasetSourceMap.Keys) {
    $dataset = $manifest.datasets.$datasetName
    if ($null -eq $dataset) {
      $issues += "$manifestRelativePath missing dataset: $datasetName"
      continue
    }

    if ($dataset.publication_state -eq 'available') {
      $snapshotIds = @($dataset.published_snapshot_ids)
      if ($snapshotIds.Count -eq 0) {
        $issues += "$manifestRelativePath available dataset missing published_snapshot_ids: $datasetName"
        continue
      }

      foreach ($snapshotId in $snapshotIds) {
        if ([string]::IsNullOrWhiteSpace([string]$snapshotId)) {
          $issues += "$manifestRelativePath has empty published_snapshot_id: $datasetName"
          continue
        }
        [void]$referencedRawDirs.Add("data/raw/$($datasetSourceMap[$datasetName])/$characterSlug/$snapshotId")
      }
    }
    elseif ($dataset.publication_state -ne 'unavailable') {
      $issues += "$manifestRelativePath invalid publication_state for ${datasetName}: $($dataset.publication_state)"
    }
  }
}

$trackedRawDirList = @($trackedRawDirs) | Sort-Object
$referencedRawDirList = @($referencedRawDirs) | Sort-Object
$unreferencedRawDirs = @($trackedRawDirList | Where-Object { -not $referencedRawDirs.Contains($_) })
$missingReferencedRawDirs = @($referencedRawDirList | Where-Object { -not $trackedRawDirs.Contains($_) })

foreach ($path in $missingReferencedRawDirs) {
  $issues += "Referenced raw snapshot is not tracked: $path"
}

foreach ($path in $unreferencedRawDirs) {
  $issues += "Tracked raw snapshot is not referenced by current published manifests: $path"
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host "Raw snapshot minimality OK: tracked=$($trackedRawDirList.Count) referenced=$($referencedRawDirList.Count)"
