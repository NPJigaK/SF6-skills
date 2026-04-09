$required = @(
  'skills',
  'maintainer-skills',
  'packages',
  'shared',
  'docs/architecture',
  'docs/authoring',
  'docs/distribution',
  'docs/testing',
  'tests/install',
  'tests/integration',
  'tests/packaging',
  'scripts/dev'
)

$missing = $required | Where-Object { -not (Test-Path $_) }

if ($missing.Count -gt 0) {
  throw "Missing required paths: $($missing -join ', ')"
}

Write-Host 'Layout OK'
