Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredDirectories = @(
  'skills',
  'maintainer-skills',
  '.agents',
  '.agents/skills',
  'packages',
  'packages/skill-installers',
  'packages/skill-validator',
  'packages/skill-packaging',
  'shared',
  'shared/templates',
  'shared/templates/skill',
  'shared/schemas',
  'ingest',
  'data',
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

$missingDirectories = foreach ($relativePath in $requiredDirectories) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
    $relativePath
  }
}

if (@($missingDirectories).Count -gt 0) {
  throw "Missing required paths: $($missingDirectories -join ', ')"
}

$requiredFiles = @(
  'README.md',
  'docs/architecture/README.md',
  'docs/architecture/repo-structure-contract.md',
  'packages/README.md',
  'shared/README.md',
  'skills/README.md',
  'maintainer-skills/README.md'
)

$missingFiles = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if (@($missingFiles).Count -gt 0) {
  throw "Missing required files: $($missingFiles -join ', ')"
}

$contentChecks = @(
  @{
    Path = 'README.md'
    MustContain = @(
      '## Repository Structure',
      '## Repo Structure Contract',
      '[repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)',
      '`.agents/skills/`'
    )
  },
  @{
    Path = 'docs/architecture/README.md'
    MustContain = @(
      'repo-structure-contract.md',
      'kb-sf6-frame-current-packaging.md'
    )
  },
  @{
    Path = 'packages/README.md'
    MustContain = @(
      'Use `packages/` only after a second real consumer exists.'
    )
  },
  @{
    Path = 'shared/README.md'
    MustContain = @(
      'Use `shared/` only after a second real consumer exists.'
    )
  },
  @{
    Path = 'skills/README.md'
    MustContain = @(
      'Each direct child under `skills/` is an independent public skill unit.',
      'Required per skill: `SKILL.md`.',
      'Optional per skill: `references/`, `assets/`, `agents/`.'
    )
  },
  @{
    Path = 'maintainer-skills/README.md'
    MustContain = @(
      'These skills are repository-only workflows.',
      'They are not public distribution units.'
    )
  }
)

foreach ($check in $contentChecks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw
  foreach ($needle in $check.MustContain) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$($check.Path) missing: $needle"
    }
  }
}

function Get-DirectChildDirectoryNames {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Root
  )

  return @(
    Get-ChildItem -LiteralPath $Root -Directory |
      Sort-Object Name |
      ForEach-Object { $_.Name }
  )
}

$publicSkillsRoot = Join-Path $repoRoot 'skills'
$publicSkillNames = Get-DirectChildDirectoryNames -Root $publicSkillsRoot

foreach ($skillName in $publicSkillNames) {
  $skillManifest = Join-Path $publicSkillsRoot (Join-Path $skillName 'SKILL.md')
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Public skill missing SKILL.md: skills/$skillName"
  }
}

$maintainerSkillsRoot = Join-Path $repoRoot 'maintainer-skills'
$maintainerSkillNames = Get-DirectChildDirectoryNames -Root $maintainerSkillsRoot

foreach ($skillName in $maintainerSkillNames) {
  $skillManifest = Join-Path $maintainerSkillsRoot (Join-Path $skillName 'SKILL.md')
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Maintainer skill missing SKILL.md: maintainer-skills/$skillName"
  }
}

$dogfoodRoot = Join-Path $repoRoot '.agents/skills'
$dogfoodSkillNames = Get-DirectChildDirectoryNames -Root $dogfoodRoot

if (Compare-Object ($publicSkillNames | Sort-Object) ($dogfoodSkillNames | Sort-Object)) {
  throw 'Dogfood mirror top-level skill inventory does not match skills/'
}

Write-Host 'Layout OK'
