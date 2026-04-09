$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$required = @(
  'skills',
  'maintainer-skills',
  'packages',
  'packages/skill-installers',
  'packages/skill-validator',
  'packages/skill-packaging',
  'shared',
  'shared/templates',
  'shared/templates/skill',
  'shared/schemas',
  'docs/architecture',
  'docs/authoring',
  'docs/authoring/automation-prompts',
  'docs/distribution',
  'docs/testing',
  'tests/install',
  'tests/integration',
  'tests/packaging',
  'scripts/dev',
  '.claude-plugin',
  '.cursor-plugin',
  '.codex',
  '.opencode'
)

$missing = foreach ($relativePath in $required) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
    $relativePath
  }
}

if ($missing.Count -gt 0) {
  throw "Missing required paths: $($missing -join ', ')"
}

Write-Host 'Layout OK'
