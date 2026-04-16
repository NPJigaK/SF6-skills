Set-StrictMode -Version Latest

function New-Text {
  param(
    [Parameter(Mandatory = $true)]
    [int[]]$CodePoints
  )

  -join ($CodePoints | ForEach-Object { [char]$_ })
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$AnswerLabelsHeading = New-Text 35, 35, 32, 0x56DE, 0x7B54, 0x30E9, 0x30D9, 0x30EB
$LabelVerified = New-Text 91, 0x691C, 0x8A3C, 0x6E08, 0x307F, 93
$LabelConcept = New-Text 91, 0x6982, 0x5FF5, 0x306E, 0x307F, 93
$LabelPending = New-Text 91, 0x4FDD, 0x7559, 93

$checks = @(
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = '`local/` is the personal trial workspace for trying distributed skills.' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/update-frame-data/' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'snapshot_manifest.json' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'publication_state = available' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'lookup order は `official_raw` -> `derived_metrics` -> `supercombo_enrichment`' },
  @{ Path = 'AGENTS.md'; MustNotContain = $AnswerLabelsHeading },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelVerified },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelConcept },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelPending },
  @{ Path = 'skills/kb-sf6-core/SKILL.md'; MustContain = $LabelConcept },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = $LabelConcept },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = 'kb-sf6-frame-current' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = $LabelVerified },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = $LabelPending },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'snapshot_manifest.json' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'Do not use T3 alone as the final authority when packaged official data exists.' },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = $LabelVerified },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = $LabelPending },
  @{ Path = 'skills/video-analysis-core/SKILL.md'; MustContain = "Do not label observations as ``$LabelVerified`` current fact." },
  @{ Path = 'README.md'; MustContain = '# SF6 Skills' },
  @{ Path = 'README.md'; MustContain = '## How it works' },
  @{ Path = 'README.md'; MustContain = '## Installation' },
  @{ Path = 'README.md'; MustContain = '## Verify installation' },
  @{ Path = 'README.md'; MustContain = '## Basic usage' },
  @{ Path = 'README.md'; MustContain = '## Current fact policy' },
  @{ Path = 'README.md'; MustContain = '## What''s inside' },
  @{ Path = 'README.md'; MustContain = '## Contributing' },
  @{ Path = 'README.md'; MustContain = '## Updating' },
  @{ Path = 'README.md'; MustContain = 'The agent can usually choose a matching skill automatically.' },
  @{ Path = 'README.md'; MustContain = 'You can also mention a skill by name explicitly.' },
  @{ Path = 'README.md'; MustContain = '.codex/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.claude-plugin/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.cursor-plugin/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.opencode/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '`kb-sf6-core`' },
  @{ Path = 'README.md'; MustContain = '`kb-sf6-frame-current`' },
  @{ Path = 'README.md'; MustContain = 'data/exports/<character_slug>/snapshot_manifest.json' },
  @{ Path = 'README.md'; MustContain = 'publication_state = available' },
  @{ Path = 'README.md'; MustContain = 'shared/roster/current-character-roster.json' },
  @{ Path = 'README.md'; MustContain = '`official_raw` is canonical' },
  @{ Path = 'README.md'; MustContain = '`derived_metrics` is official-only computed output' },
  @{ Path = 'README.md'; MustContain = '`supercombo_enrichment` is supplemental only' },
  @{ Path = 'README.md'; MustContain = '`data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface' },
  @{ Path = 'README.md'; MustContain = '[ingest/frame_data/README.md](./ingest/frame_data/README.md)' },
  @{ Path = 'README.md'; MustContain = '[repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = '`local/` is the personal trial workspace.' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = 'bootstrap-local-trial-workspace.ps1' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'docs/testing/README.md'; MustContain = 'validate-local-trial-surface.ps1' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'skills/README.md'; MustContain = 'Canonical public source for distributed skills lives here.' },
  @{ Path = 'skills/README.md'; MustContain = 'Runtime guidance belongs in each skill''s `SKILL.md` and local references.' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/video-analysis-core/' }
)

$readme = Get-Content -LiteralPath (Join-Path $repoRoot 'README.md') -Raw -Encoding UTF8 -ErrorAction Stop
if ($readme -notmatch '(?m)^# SF6 Skills$') {
  throw 'README.md missing: # SF6 Skills'
}

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
