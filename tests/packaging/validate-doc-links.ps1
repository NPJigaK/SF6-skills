$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$videoAnalysisBehaviorGuidance = (
  '`skills/video-analysis-core/` ' +
  [char]0x306F + ' raw video ' + [char]0x3092 + ' 60fps ' +
  [char]0x306B + [char]0x6B63 + [char]0x898F + [char]0x5316 + [char]0x3057 + [char]0x305F +
  ' observation-first surface ' + [char]0x3092 + [char]0x8FD4 + [char]0x3059 + [char]0x3002
)

$checks = @(
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = $videoAnalysisBehaviorGuidance },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = 'Repo-local dogfooding uses `.agents/skills/` as an exact top-level mirror of `skills/`.' },
  @{ Path = 'AGENTS.md'; MustContain = 'The sync refresh removes stale extra directories.' },
  @{ Path = 'docs/architecture/README.md'; MustContain = 'video-analysis-v0-design.md' },
  @{ Path = 'docs/architecture/README.md'; MustContain = 'video-analysis-v0-implementation-plan.md' },
  @{ Path = '.agents/AGENTS.md'; MustContain = '`skills/` is the canonical public source.'; MustNotContain = 'skills and related assets only' },
  @{ Path = '.agents/AGENTS.md'; MustContain = '`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'The sync refresh removes stale extra directories.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = '`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.' },
  @{ Path = 'docs/distribution/repo-local-dogfooding.md'; MustContain = 'The sync refresh removes stale extra directories.' }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw -Encoding UTF8 -ErrorAction Stop
  if ($content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($check.ContainsKey('MustNotContain') -and $content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
