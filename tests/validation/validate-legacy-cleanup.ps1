Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$legacyPaths = @(
  'skills/kb-sf6-core',
  'skills/kb-sf6-frame-current',
  'skills/video-analysis-core',
  'maintainer-skills',
  'shared',
  'shared/roster',
  'local',
  '.codex',
  '.claude-plugin',
  '.cursor-plugin',
  '.opencode'
)

$violations = @()
foreach ($relativePath in $legacyPaths) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath)) {
    $violations += "Legacy path still exists: $relativePath"
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Legacy cleanup OK'
