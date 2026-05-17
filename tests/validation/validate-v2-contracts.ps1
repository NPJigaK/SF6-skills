Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredJsonSchemas = @(
  'contracts/source-metadata.schema.json',
  'contracts/claim.schema.json',
  'contracts/knowledge-page.schema.json',
  'contracts/generated-surface.schema.json',
  'contracts/eval-case.schema.json',
  'contracts/eval-score-report.schema.json',
  'contracts/video-observation.schema.json',
  'contracts/answer-intent.schema.json',
  'contracts/evidence-card.schema.json',
  'contracts/answer-plan.schema.json',
  'contracts/hermes-delegation-sanitized-trace.schema.json',
  'contracts/calculation-backend-handoff.schema.json',
  'contracts/calculation-trace.schema.json',
  'contracts/normalization-aliases.schema.json',
  'contracts/agent-toolchain.schema.json',
  'contracts/repository-surface.schema.json',
  'contracts/current-fact-export-manifest.schema.json',
  'contracts/manual-review-debt-index.schema.json'
)

$requiredDocs = @(
  'contracts/frame-current-runtime-assets.md',
  'contracts/hermes-delegation-sanitized-trace.md',
  'contracts/calculation-executor-trace.md',
  'contracts/video-observation.md',
  'contracts/evidence-gate.md',
  'contracts/web-research-policy.md'
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
foreach ($needle in @('source_kind', 'source_role', 'evidence_basis', 'verification_state', 'confidence', 'volatility', 'patch_sensitivity', 'review_status', 'source_refs', 'review_after', 'source_revision')) {
  if ($sourceSchema -notmatch [regex]::Escape($needle)) {
    throw "source metadata contract missing field: $needle"
  }
}
$sourceSchemaObject = $sourceSchema | ConvertFrom-Json
$sourceRequired = @($sourceSchemaObject.required)
if ($sourceRequired -notcontains 'review_after') {
  throw 'source metadata contract must require review_after; use null when no review date is needed'
}

if ($sourceSchema -match '"source_tier"') {
  throw 'source metadata contract must not preserve source_tier as canonical metadata'
}

$knowledgeSchema = Get-Content -LiteralPath (Join-Path $repoRoot 'contracts/knowledge-page.schema.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$knowledgeRequired = @($knowledgeSchema.required)
foreach ($field in @('source_kind', 'source_role', 'evidence_basis', 'verification_state', 'confidence', 'volatility', 'patch_sensitivity', 'review_status', 'source_refs', 'review_after')) {
  if ($knowledgeRequired -notcontains $field) {
    throw "knowledge page contract must use flat front matter field: $field"
  }
}
if ($knowledgeRequired -contains 'evidence') {
  throw 'knowledge page contract must not require nested evidence object while authored pages use flat front matter'
}

$generatedSchema = Get-Content -LiteralPath (Join-Path $repoRoot 'contracts/generated-surface.schema.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$generatedRequired = @($generatedSchema.required)
foreach ($field in @('generated', 'generator', 'source_paths', 'target_path')) {
  if ($generatedRequired -notcontains $field) {
    throw "generated surface contract missing required field: $field"
  }
}

Write-Host 'V2 contracts OK'
