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

$bootstrapScript = Join-Path $repoRoot 'scripts/dev/bootstrap-local-trial-workspace.ps1'
$bootstrapRuns = @(
  @{ Label = 'powershell run 1'; Command = 'powershell'; Arguments = @('-ExecutionPolicy', 'Bypass', '-File', $bootstrapScript) },
  @{ Label = 'powershell run 2'; Command = 'powershell'; Arguments = @('-ExecutionPolicy', 'Bypass', '-File', $bootstrapScript) },
  @{ Label = 'pwsh run'; Command = 'pwsh'; Arguments = @('-NoProfile', '-File', $bootstrapScript) }
)

foreach ($bootstrapRun in $bootstrapRuns) {
  & $bootstrapRun.Command @($bootstrapRun.Arguments)
  if ($LASTEXITCODE -ne 0) {
    throw "Bootstrap failed for $($bootstrapRun.Label)"
  }
}

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

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'local/.agents/skills/sf6-skills'))) {
  $validationIssues += 'Bootstrap must create local/.agents/skills/sf6-skills'
}

& git -C $repoRoot check-ignore -q -- 'local/.agents/skills/sf6-skills'
if ($LASTEXITCODE -ne 0) {
  $validationIssues += 'local/.agents/skills/sf6-skills must be ignored by git'
}

if (@($validationIssues).Count -gt 0) {
  throw ($validationIssues -join '; ')
}

Write-Host 'Local trial surface OK'
