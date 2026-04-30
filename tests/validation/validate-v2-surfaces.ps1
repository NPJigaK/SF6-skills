Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

$requiredFiles = @(
  'README.md',
  'AGENTS.md',
  'docs/architecture/v2-architecture.md',
  'knowledge/README.md',
  'evals/README.md',
  'contracts/README.md',
  'workflows/README.md',
  'packs/README.md'
)

$requiredDirectories = @(
  'knowledge/curated/concepts',
  'knowledge/curated/glossary',
  'knowledge/sources',
  'knowledge/evidence/claims',
  'knowledge/evidence/video-observations',
  'knowledge/review',
  'knowledge/review/unresolved',
  'knowledge/review/contested',
  'knowledge/review/current-fact-candidates',
  'evals/questions',
  'evals/rubrics',
  'contracts',
  'workflows',
  'packs',
  'skills/sf6-agent/references',
  'skills/sf6-agent/assets/frame-current'
)

$issues = @()

foreach ($relativePath in $requiredFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing required v2 file: $relativePath"
  }
}

foreach ($relativePath in $requiredDirectories) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Container)) {
    $issues += "Missing required v2 directory: $relativePath"
  }
}

if ($issues.Count -eq 0) {
  $readme = Read-Text 'README.md'
  foreach ($needle in @(
    'SF6 Knowledge Agent Kit',
    '`knowledge/` is canonical',
    '`data/exports/` and `data/roster/` are the exact current-fact authority',
    '`skills/sf6-agent/references/generated-*` is derived',
    '`skills/sf6-agent/assets/frame-current/` is derived'
  )) {
    if ($readme -notmatch [regex]::Escape($needle)) {
      $issues += "README.md missing v2 boundary text: $needle"
    }
  }

  $agents = Read-Text 'AGENTS.md'
  foreach ($needle in @(
    'This repo is SF6 Knowledge Agent Kit.',
    '`knowledge/` is canonical.',
    '`data/exports/` and `data/roster/` are exact current fact authority.',
    '`workflows/` are canonical maintainer procedures.',
    'Do not put exact current values in `knowledge/curated/` or generated knowledge references.',
    'Hermes is optional maintainer harness, not canonical memory.'
  )) {
    if ($agents -notmatch [regex]::Escape($needle)) {
      $issues += "AGENTS.md missing v2 guidance: $needle"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'V2 surfaces OK'
