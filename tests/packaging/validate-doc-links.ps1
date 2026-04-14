Set-StrictMode -Version Latest

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/video-analysis-core/'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = '`local/` is the personal trial workspace for trying distributed skills.' },
  @{ Path = 'README.md'; MustContain = '`skills/<skill-name>/`' },
  @{ Path = 'README.md'; MustContain = '`local/`' },
  @{ Path = 'skills/README.md'; MustContain = 'There is no tracked repo-root `.agents/skills/` mirror.' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = '`local/` is the personal trial workspace.' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = 'bootstrap-local-trial-workspace.ps1' },
  @{ Path = 'docs/testing/README.md'; MustContain = 'validate-local-trial-surface.ps1' }
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
