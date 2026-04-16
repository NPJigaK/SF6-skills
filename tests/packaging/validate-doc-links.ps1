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
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
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
  @{ Path = 'README.md'; MustContain = 'skills/<skill-name>/' },
  @{ Path = 'README.md'; MustContain = 'local/' },
  @{ Path = 'README.md'; MustContain = 'exact runtime answer rules live in `skills/kb-sf6-frame-current/`' },
  @{ Path = 'README.md'; MustContain = 'concept-only runtime guidance lives in `skills/kb-sf6-core/`' },
  @{ Path = 'README.md'; MustNotContain = 'snapshot_manifest.json' },
  @{ Path = 'README.md'; MustNotContain = 'publication_state = available' },
  @{ Path = 'README.md'; MustNotContain = 'lookup order は `official_raw` -> `derived_metrics` -> `supercombo_enrichment`' },
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
