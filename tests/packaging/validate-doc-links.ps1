Set-StrictMode -Version Latest

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$checks = @(
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/video-analysis-core/'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = '`local/` is the personal trial workspace for trying distributed skills.' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/update-frame-data/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '## 回答ラベル' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[検証済み]' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[概念のみ]' },
  @{ Path = 'AGENTS.md'; MustNotContain = '[保留]' },
  @{ Path = 'skills/kb-sf6-core/SKILL.md'; MustContain = '[概念のみ]' },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = 'current fact / exact 数値 / パッチ差分はここに混ぜない.' },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = 'T1: 公式一次情報' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = '[検証済み]' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = '[保留]' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'Do not use T3 alone as the final authority when packaged official data exists.' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'snapshot_manifest.json' },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = 'Supported characters for this skill are the `character_slug` entries recorded in `assets/runtime_manifest.json`.' },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = 'Never let it override official.' },
  @{ Path = 'skills/video-analysis-core/SKILL.md'; MustContain = 'Do not label observations as `[検証済み]` current fact.' },
  @{ Path = 'skills/README.md'; MustContain = 'Canonical public source for distributed skills lives here.' },
  @{ Path = 'skills/README.md'; MustContain = 'Runtime guidance belongs in each skill''s `SKILL.md` and local references.' }
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
