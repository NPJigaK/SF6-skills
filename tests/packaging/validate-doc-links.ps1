$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'README.md'; MustContain = 'skills/'; MustNotContain = '.agents/skills/' },
  @{ Path = 'README.md'; MustContain = 'monorepo migration is in progress' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'repo-local compatibility copies may still remain during migration and should not be treated as canonical' },
  @{ Path = 'AGENTS.md'; MustContain = 'Use the canonical path when that skill has already been migrated; otherwise use the repo-local compatibility copy under `.agents/skills/` until that specific skill moves.' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'generated compatibility output'; MustNotContain = 'skills and related assets only' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'Some compatibility skills may still remain here until they are migrated into `skills/` or `maintainer-skills/` as appropriate.' }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw -ErrorAction Stop
  if ($content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($check.ContainsKey('MustNotContain') -and $content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
