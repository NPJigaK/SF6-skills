param(
  [ValidateSet('read-only', 'derived-build', 'legacy-distribution', 'all')]
  [string]$Lane = 'all'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$derivedOutputPaths = @(
  'skills/sf6-agent/references/generated-knowledge-index.md',
  'skills/sf6-agent/references/generated-concepts.md',
  'skills/sf6-agent/assets/frame-current',
  'skills/sf6-agent/assets/normalization'
)

function Assert-NoDerivedOutputStatus {
  param([Parameter(Mandatory = $true)][string]$Context)

  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "WARNING: git is unavailable; skipping derived output status check after $Context"
    return
  }

  $status = @(& git -C $repoRoot status --porcelain -- $derivedOutputPaths)
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to inspect derived output status during $Context"
  }
  if ($status.Count -gt 0) {
    throw "Tracked or untracked derived outputs changed during $Context. Review and commit regenerated generated-* references and frame-current assets before relying on validation."
  }
}

$derivedBuildPreflightScripts = @(
  'packages/knowledge-generation/build-sf6-agent-knowledge.ps1',
  'packages/skill-packaging/build-frame-current-runtime-assets.ps1',
  'packages/skill-packaging/build-normalization-runtime-assets.ps1'
)

$legacyDistributionPreflightScripts = @(
  'packages/skill-packaging/build-release-bundle.ps1'
)

$allPreflightScripts = $derivedBuildPreflightScripts + $legacyDistributionPreflightScripts

$readOnlyValidationScripts = @(
  'tests/validation/validate-v2-surfaces.ps1',
  'tests/validation/validate-architecture-markers.ps1',
  'tests/validation/validate-hermes-pack.ps1',
  'tests/validation/validate-codex-hermes-pack.ps1',
  'tests/validation/validate-codex-hermes-delegation-fixtures.ps1',
  'tests/validation/validate-v2-contracts.ps1',
  'tests/validation/validate-agent-toolchain.ps1',
  'tests/validation/validate-repository-surfaces.ps1',
  'tests/validation/validate-powershell-compatibility-policy.ps1',
  'tests/validation/validate-frame-current-runtime-separation-plan.ps1',
  'tests/validation/validate-generated-reference-responsibility-plan.ps1',
  'tests/validation/validate-answer-orchestration-contracts.ps1',
  'tests/validation/validate-answer-smoke-fixtures.ps1',
  'tests/validation/validate-calculation-executor.ps1',
  'tests/validation/validate-normalization-aliases.ps1',
  'tests/validation/validate-normalization-runtime-assets.ps1',
  'tests/validation/validate-knowledge-schema.ps1',
  'tests/validation/validate-ingest-artifacts.ps1',
  'tests/validation/validate-video-artifacts.ps1',
  'tests/validation/validate-video-observation-taxonomy-fixtures.ps1',
  'tests/validation/validate-video-learning-report-template.ps1',
  'tests/validation/validate-external-frame-atlas-source-evaluation.ps1',
  'tests/validation/validate-external-frame-atlas-source-fixtures.ps1',
  'tests/validation/validate-no-video-binary-assets.ps1',
  'tests/validation/validate-combo-damage-fixtures.ps1',
  'tests/validation/validate-evals.ps1',
  'tests/validation/validate-roster-source.ps1',
  'tests/validation/validate-raw-snapshot-minimality.ps1',
  'tests/validation/validate-frame-current-assets.ps1',
  'tests/validation/validate-generated-knowledge.ps1',
  'tests/validation/validate-current-fact-boundaries.ps1',
  'tests/validation/validate-doc-links.ps1',
  'tests/validation/validate-legacy-cleanup.ps1'
)

$derivedBuildValidationScripts = @(
  'tests/validation/validate-generated-knowledge.ps1',
  'tests/validation/validate-frame-current-assets.ps1',
  'tests/validation/validate-normalization-runtime-assets.ps1',
  'tests/validation/validate-normalization-aliases.ps1',
  'tests/validation/validate-current-fact-boundaries.ps1',
  'tests/validation/validate-repository-surfaces.ps1'
)

$legacyDistributionValidationScripts = @(
  'tests/validation/validate-distribution.ps1',
  'tests/validation/validate-legacy-cleanup.ps1'
)

$allValidationScripts = @(
  $readOnlyValidationScripts | Where-Object {
    $_ -notin @(
      'tests/validation/validate-doc-links.ps1',
      'tests/validation/validate-legacy-cleanup.ps1'
    )
  }
) + @(
  'tests/validation/validate-distribution.ps1',
  'tests/validation/validate-doc-links.ps1',
  'tests/validation/validate-legacy-cleanup.ps1'
)

switch ($Lane) {
  'read-only' {
    $preflightScripts = @()
    $validationScripts = $readOnlyValidationScripts
  }
  'derived-build' {
    $preflightScripts = $derivedBuildPreflightScripts
    $validationScripts = $derivedBuildValidationScripts
  }
  'legacy-distribution' {
    $preflightScripts = $legacyDistributionPreflightScripts
    $validationScripts = $legacyDistributionValidationScripts
  }
  'all' {
    $preflightScripts = $allPreflightScripts
    $validationScripts = $allValidationScripts
  }
}

Write-Host "Running validation lane: $Lane"

foreach ($relativePath in @($preflightScripts + $validationScripts | Select-Object -Unique)) {
  $scriptPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
    throw "Missing validation script: $relativePath"
  }
}

foreach ($relativePath in $preflightScripts) {
  Write-Host "Running preflight: $relativePath"
  & (Join-Path $repoRoot $relativePath)
  Assert-NoDerivedOutputStatus $relativePath
}

foreach ($relativePath in $validationScripts) {
  Write-Host "Running validator: $relativePath"
  & (Join-Path $repoRoot $relativePath)
}

Write-Host "V2 validation suite OK ($Lane lane)"
