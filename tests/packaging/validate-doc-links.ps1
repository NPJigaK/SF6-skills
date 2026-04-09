$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'README.md'; MustContain = 'skills/'; MustNotContain = '.agents/skills/' },
  @{ Path = 'README.md'; MustContain = 'monorepo migration is in progress' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'repo-local compatibility copies may still remain during migration and should not be treated as canonical' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'generated compatibility output'; MustNotContain = 'skills and related assets only' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'some skills may still only exist there until the migration tasks copy them into `skills/`' }
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
