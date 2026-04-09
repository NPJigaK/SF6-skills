$checks = @(
  @{ Path = 'README.md'; MustContain = 'skills/'; MustNotContain = '.agents/skills/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'generated compatibility output'; MustNotContain = 'skills and related assets only' }
)

foreach ($check in $checks) {
  $content = Get-Content $check.Path -Raw
  if ($content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
