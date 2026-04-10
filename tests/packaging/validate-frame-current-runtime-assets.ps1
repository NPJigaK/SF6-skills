$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$assetRoot = Join-Path $repoRoot 'skills/kb-sf6-frame-current/assets'

$requiredFiles = @(
  'runtime_manifest.json'
  'published/jp/snapshot_manifest.json'
  'published/jp/official_raw.json'
  'published/jp/derived_metrics.json'
  'published/jp/supercombo_enrichment.json'
  'published/luke/snapshot_manifest.json'
  'published/luke/official_raw.json'
  'published/luke/derived_metrics.json'
  'published/luke/supercombo_enrichment.json'
)

$missingFiles = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $assetRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if ($missingFiles.Count -gt 0) {
  throw "Missing runtime asset files: $($missingFiles -join ', ')"
}

$forbiddenFiles = @()
if (Test-Path -LiteralPath $assetRoot -PathType Container) {
  $forbiddenFiles = Get-ChildItem -LiteralPath $assetRoot -Recurse -File |
    Where-Object { $_.Extension -eq '.csv' -or $_.Name -like '*_manual_review.*' }
}

if ($forbiddenFiles.Count -gt 0) {
  $relativeForbidden = $forbiddenFiles | ForEach-Object {
    $_.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  }
  throw "Forbidden packaged files found: $($relativeForbidden -join ', ')"
}

$runtimeManifestPath = Join-Path $assetRoot 'runtime_manifest.json'
$runtimeManifest = Get-Content -LiteralPath $runtimeManifestPath -Raw | ConvertFrom-Json

if ($runtimeManifest.source_root -ne 'data/exports') {
  throw "runtime_manifest.json source_root must be data/exports"
}

$characterSlugs = @($runtimeManifest.characters.character_slug)
if ($characterSlugs.Count -ne 2 -or $characterSlugs[0] -ne 'jp' -or $characterSlugs[1] -ne 'luke') {
  throw "runtime_manifest.json characters must be exactly jp,luke"
}

Write-Host 'Frame-current runtime assets OK'
