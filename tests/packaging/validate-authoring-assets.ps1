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

Write-Host 'Authoring assets OK'
