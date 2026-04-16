Set-StrictMode -Version Latest

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'AGENTS.md'; MustNotContain = '## 回答ラベル' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[検証済み]' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[概念のみ]' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[保留]' },
  @{ Path = 'skills/kb-sf6-core/SKILL.md'; MustContain = '[概念のみ]' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = '[検証済み]' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = '[保留]' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'snapshot_manifest.json' },
  @{ Path = 'skills/README.md'; MustContain = 'Canonical public source for distributed skills lives here.' }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw -Encoding UTF8 -ErrorAction Stop
  if ($check.ContainsKey('MustContain') -and $content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($check.ContainsKey('MustNotContain') -and $content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
