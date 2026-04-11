Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredFiles = @(
  'shared/templates/skill/SKILL.md.template'
  'shared/templates/skill/README.md'
  'shared/schemas/README.md'
  'docs/authoring/README.md'
  'docs/authoring/new-skill.md'
  'packages/skill-validator/README.md'
)

$missing = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if (@($missing).Count -gt 0) {
  throw "Missing authoring assets: $($missing -join ', ')"
}

$templatePath = Join-Path $repoRoot 'shared/templates/skill/SKILL.md.template'
$template = Get-Content -LiteralPath $templatePath -Raw

if (-not $template.StartsWith('---')) {
  throw 'shared/templates/skill/SKILL.md.template must begin with frontmatter (`---`)'
}

$checks = @(
  @{
    Path = 'shared/templates/skill/SKILL.md.template'
    MustContain = @(
      '## Purpose',
      '## When To Use',
      '## Required Inputs',
      '## Workflow',
      '## Constraints',
      'Do not depend on another skill directory.',
      'Move shared artifacts out only after a second real consumer exists.'
    )
  },
  @{
    Path = 'shared/templates/skill/README.md'
    MustContain = @(
      'Required:',
      'Optional:',
      'Keep skill-specific references, assets, and agent metadata inside the skill directory until a second skill needs the same artifact.',
      'Prefer repo-level tests only when a boundary contract needs protection.'
    )
  },
  @{
    Path = 'shared/schemas/README.md'
    MustContain = @(
      'cross-skill schemas here only after more than one skill depends on the same contract'
    )
  },
  @{
    Path = 'packages/skill-validator/README.md'
    MustContain = @(
      'checking skill metadata, directory shape, and packaging outputs'
    )
  },
  @{
    Path = 'docs/authoring/README.md'
    MustContain = @(
      'independent skill first',
      'shared later',
      'local validator first',
      'new-skill.md'
    )
  },
  @{
    Path = 'docs/authoring/new-skill.md'
    MustContain = @(
      '## When to create a new skill',
      '## How to scaffold it',
      '## When to extract shared pieces',
      '## Public vs maintainer-only',
      '## What not to add to a public skill',
      'Add only the references, assets, and agent metadata that this skill needs.',
      'If a repo-level contract really needs protection, add the minimum validator under `tests/`.',
      'Do not add dependencies on another skill directory, ingestion code, installer or bundle machinery, or raw/review artifacts to a public skill.'
    )
  }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw
  foreach ($needle in $check.MustContain) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$($check.Path) missing: $needle"
    }
  }
}

Write-Host 'Authoring assets OK'
