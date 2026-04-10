$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'README.md'; MustContain = 'skills/'; MustNotContain = '.agents/skills/' },
  @{ Path = 'README.md'; MustContain = 'monorepo migration is in progress' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = 'Repo-local dogfooding uses `.agents/skills/` as an exact top-level mirror of `skills/`.' },
  @{ Path = 'AGENTS.md'; MustContain = 'The sync refresh removes stale extra directories.' },
  @{ Path = '.agents/AGENTS.md'; MustContain = '`skills/` is the canonical public source.'; MustNotContain = 'skills and related assets only' },
  @{ Path = '.agents/AGENTS.md'; MustContain = '`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'The sync refresh removes stale extra directories.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = '`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = 'The sync refresh removes stale extra directories.' }
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
