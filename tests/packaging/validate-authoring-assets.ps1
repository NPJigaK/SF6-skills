$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredFiles = @(
  'shared/templates/skill/SKILL.md.template'
  'shared/templates/skill/README.md'
  'shared/schemas/README.md'
  'docs/authoring/new-skill.md'
  'packages/skill-validator/README.md'
)

$missing = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if ($missing.Count -gt 0) {
  throw "Missing authoring assets: $($missing -join ', ')"
}

$templatePath = Join-Path $repoRoot 'shared/templates/skill/SKILL.md.template'
$template = Get-Content -LiteralPath $templatePath -Raw

if (-not $template.StartsWith('---')) {
  throw 'shared/templates/skill/SKILL.md.template must begin with frontmatter (`---`)'
}

$checks = @(
  @{ Path = 'shared/templates/skill/SKILL.md.template'; MustContain = @('## Purpose', '## When To Use', '## Required Inputs', '## Workflow', '## Constraints') },
  @{ Path = 'shared/templates/skill/README.md'; MustContain = @('skills/<skill-name>/', 'Keep skill-specific references, assets, scripts, and tests inside the skill directory until at least two skills need the same artifact', 'Treat this README as starter guidance for the generated skill, then replace or adapt it with skill-specific documentation as needed.') },
  @{ Path = 'shared/schemas/README.md'; MustContain = @('cross-skill schemas here only after more than one skill depends on the same contract') },
  @{ Path = 'packages/skill-validator/README.md'; MustContain = @('checking skill metadata, directory shape, and packaging outputs') },
  @{ Path = 'docs/authoring/new-skill.md'; MustContain = @('## When to create a new skill', '## How to scaffold it', '## When to extract shared pieces', '## Public vs maintainer-only', 'Treat `shared/templates/skill/README.md` as a starting point, then replace or adapt it with skill-specific documentation.') }
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
