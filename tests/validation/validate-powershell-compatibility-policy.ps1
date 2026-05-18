Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$policyPath = 'docs/architecture/powershell-compatibility-policy.md'

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Assert-PathExists {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $RelativePath) -PathType Leaf)) {
    $Issues.Value += "Missing required PowerShell compatibility policy file: $RelativePath"
  }
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

$requiredDocs = @(
  $policyPath,
  'README.md',
  'docs/architecture/README.md',
  'docs/testing/README.md',
  'workflows/manage-maintainer-toolchain.md',
  'workflows/github-management.md',
  'workflows/maintainer-agent-session.md',
  'workflows/check-agent-toolchain-freshness.md'
)

foreach ($relativePath in $requiredDocs) {
  Assert-PathExists $relativePath ([ref]$issues)
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $policyPath) -PathType Leaf) {
  $policy = Read-Text $policyPath
  foreach ($requiredText in @(
    'pwsh',
    'powershell.exe',
    'Windows PowerShell',
    'PowerShell Core',
    'supported maintainer validation command',
    'fallback / legacy-compatible runner',
    'Git Visibility',
    'git status --porcelain',
    'git diff --check',
    'origin/main...HEAD',
    'runtime/generated-knowledge',
    'runtime/frame-current',
    'runtime/normalization',
    '-NoProfile',
    '-ExecutionPolicy Bypass'
  )) {
    Assert-Contains $policy $requiredText $policyPath ([ref]$issues)
  }
}

foreach ($relativePath in @(
  'README.md',
  'docs/testing/README.md',
  'workflows/manage-maintainer-toolchain.md',
  'workflows/github-management.md',
  'workflows/maintainer-agent-session.md',
  'workflows/check-agent-toolchain-freshness.md'
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf) {
    $text = Read-Text $relativePath
    Assert-Contains $text 'docs/architecture/powershell-compatibility-policy.md' $relativePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/README.md') -PathType Leaf) {
  $architectureReadme = Read-Text 'docs/architecture/README.md'
  Assert-Contains $architectureReadme 'powershell-compatibility-policy.md' 'docs/architecture/README.md' ([ref]$issues)
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/testing/README.md') -PathType Leaf) {
  $testingReadme = Read-Text 'docs/testing/README.md'
  if ($testingReadme.Contains('`powershell -ExecutionPolicy Bypass -File tests/validation/')) {
    $issues += 'docs/testing/README.md maintainer validator examples must use pwsh, not bare powershell'
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'PowerShell compatibility policy OK'
