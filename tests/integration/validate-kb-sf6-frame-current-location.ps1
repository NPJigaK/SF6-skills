Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillRoot = Join-Path $repoRoot 'skills\kb-sf6-frame-current'
$requiredFiles = @(
  'SKILL.md'
  'references\export-contract.md'
  'agents\openai.yaml'
)

foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $skillRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    throw "Missing frame-current public skill file: $relativePath"
  }
}

$skillContent = Get-Content -LiteralPath (Join-Path $skillRoot 'SKILL.md') -Raw
if ($skillContent -notmatch [regex]::Escape('assets/published/<character_slug>/snapshot_manifest.json')) {
  throw 'Public frame-current SKILL.md must point at skill-local assets'
}
if ($skillContent -match [regex]::Escape('data/exports/<character_slug>/')) {
  throw 'Public frame-current SKILL.md must not depend on repo-root data/exports paths'
}

$referenceContent = Get-Content -LiteralPath (Join-Path $skillRoot 'references\export-contract.md') -Raw
$requiredReferenceLines = @(
  'assets/runtime_manifest.json'
  'assets/published/<character_slug>/snapshot_manifest.json'
  'assets/published/<character_slug>/official_raw.json'
  'assets/published/<character_slug>/derived_metrics.json'
  'assets/published/<character_slug>/supercombo_enrichment.json'
)

foreach ($line in $requiredReferenceLines) {
  if ($referenceContent -notmatch [regex]::Escape($line)) {
    throw "Public frame-current export contract missing: $line"
  }
}

Write-Host 'kb-sf6-frame-current public shell OK'
