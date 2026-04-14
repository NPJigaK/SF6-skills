Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredPaths = @(
  'local/AGENTS.md',
  'local/.gitignore',
  'local/.codex/INSTALL.md',
  'local/.agents/AGENTS.md',
  'local/.agents/.gitignore',
  'scripts/dev/bootstrap-local-trial-workspace.ps1'
)

$missingPaths = foreach ($relativePath in $requiredPaths) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

$blockedPaths = @(
  '.agents',
  'scripts/dev/sync-dogfood-skills.ps1',
  'tests/install/validate-dogfood-mirror.ps1'
)

$validationIssues = @()

if (@($missingPaths).Count -gt 0) {
  $validationIssues += "Missing local trial surface files: $($missingPaths -join ', ')"
}

foreach ($relativePath in $blockedPaths) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (Test-Path -LiteralPath $fullPath) {
    $validationIssues += "Legacy path must not exist: $relativePath"
  }
}

if (@($validationIssues).Count -gt 0) {
  throw ($validationIssues -join '; ')
}

Write-Host 'Local trial surface OK'
