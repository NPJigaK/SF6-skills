Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$derivedOutputPaths = @(
  'skills/sf6-agent/references/generated-knowledge-index.md',
  'skills/sf6-agent/references/generated-concepts.md',
  'skills/sf6-agent/assets/frame-current'
)

function Assert-NoTrackedDerivedDiff {
  param([Parameter(Mandatory = $true)][string]$Context)

  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "WARNING: git is unavailable; skipping tracked derived output check after $Context"
    return
  }

  & git -C $repoRoot diff --exit-code -- $derivedOutputPaths
  if ($LASTEXITCODE -ne 0) {
    throw "Tracked derived outputs changed during $Context. Review and commit regenerated generated-* references and frame-current assets before relying on validation."
  }
}

$preflightScripts = @(
  'packages/knowledge-generation/build-sf6-agent-knowledge.ps1',
  'packages/skill-packaging/build-frame-current-runtime-assets.ps1',
  'packages/skill-packaging/build-release-bundle.ps1'
)

$validationScripts = @(
  'tests/validation/validate-v2-surfaces.ps1',
  'tests/validation/validate-v2-contracts.ps1',
  'tests/validation/validate-knowledge-schema.ps1',
  'tests/validation/validate-evals.ps1',
  'tests/validation/validate-roster-source.ps1',
  'tests/validation/validate-frame-current-assets.ps1',
  'tests/validation/validate-generated-knowledge.ps1',
  'tests/validation/validate-current-fact-boundaries.ps1',
  'tests/validation/validate-distribution.ps1',
  'tests/validation/validate-doc-links.ps1',
  'tests/validation/validate-legacy-cleanup.ps1'
)

foreach ($relativePath in $preflightScripts + $validationScripts) {
  $scriptPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
    throw "Missing validation script: $relativePath"
  }
}

foreach ($relativePath in $preflightScripts) {
  Write-Host "Running preflight: $relativePath"
  & (Join-Path $repoRoot $relativePath)
  Assert-NoTrackedDerivedDiff $relativePath
}

foreach ($relativePath in $validationScripts) {
  Write-Host "Running validator: $relativePath"
  & (Join-Path $repoRoot $relativePath)
}

Write-Host 'V2 validation suite OK'
