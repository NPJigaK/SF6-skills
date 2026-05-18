Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$planPath = 'docs/architecture/frame-current-runtime-separation-plan.md'

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Assert-Contains {
  param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$Needle,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not $Text.Contains($Needle)) {
    $Issues.Value += "$Context must mention: $Needle"
  }
}

$issues = @()

foreach ($relativePath in @(
  $planPath,
  'README.md',
  'docs/architecture/README.md',
  'docs/architecture/repository-surface-registry-policy.md'
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing frame-current runtime separation reference file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $planPath) -PathType Leaf) {
  $plan = Read-Text $planPath
  foreach ($requiredText in @(
    'runtime/frame-current/',
    'data/exports/',
    'data/roster/',
    'packages/skill-packaging/build-frame-current-runtime-assets.ps1',
    'tests/validation/validate-frame-current-assets.ps1',
    'contracts/frame-current-runtime-assets.md',
    'frame_current_runtime_assets',
    'source authority',
    'derived runtime output',
    'public adapter was removed'
  )) {
    Assert-Contains $plan $requiredText $planPath ([ref]$issues)
  }
}

foreach ($relativePath in @(
  'README.md',
  'docs/architecture/repository-surface-registry-policy.md'
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf) {
    $text = Read-Text $relativePath
    Assert-Contains $text 'docs/architecture/frame-current-runtime-separation-plan.md' $relativePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/README.md') -PathType Leaf) {
  $architectureReadme = Read-Text 'docs/architecture/README.md'
  Assert-Contains $architectureReadme 'frame-current-runtime-separation-plan.md' 'docs/architecture/README.md' ([ref]$issues)
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Frame-current runtime separation plan OK'
