Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredJsonSchemas = @(
  'contracts/source-metadata.schema.json',
  'contracts/claim.schema.json',
  'contracts/knowledge-page.schema.json',
  'contracts/generated-surface.schema.json',
  'contracts/eval-case.schema.json',
  'contracts/video-observation.schema.json'
)

$requiredDocs = @(
  'contracts/frame-current-runtime-assets.md',
  'contracts/video-observation.md'
)

foreach ($relativePath in $requiredJsonSchemas) {
  $path = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing contract schema: $relativePath"
  }

  $json = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
  if (-not $json.'$schema') {
    throw "Contract schema missing `$schema: $relativePath"
  }
  if (-not $json.title) {
    throw "Contract schema missing title: $relativePath"
  }
}

foreach ($relativePath in $requiredDocs) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    throw "Missing contract doc: $relativePath"
  }
}

$sourceSchema = Get-Content -LiteralPath (Join-Path $repoRoot 'contracts/source-metadata.schema.json') -Raw -Encoding UTF8
foreach ($needle in @('source_kind', 'source_role', 'evidence_basis', 'verification_state', 'confidence', 'volatility', 'patch_sensitivity', 'review_status', 'source_refs', 'review_after')) {
  if ($sourceSchema -notmatch [regex]::Escape($needle)) {
    throw "source metadata contract missing field: $needle"
  }
}

if ($sourceSchema -match '"source_tier"') {
  throw 'source metadata contract must not preserve source_tier as canonical metadata'
}

Write-Host 'V2 contracts OK'
