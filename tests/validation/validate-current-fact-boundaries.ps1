Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$scopedRoots = @(
  'knowledge/curated',
  'skills/sf6-agent/references'
)

$files = @()
foreach ($relativeRoot in $scopedRoots) {
  $root = Join-Path $repoRoot $relativeRoot
  if (Test-Path -LiteralPath $root -PathType Container) {
    $files += Get-ChildItem -LiteralPath $root -Recurse -File |
      Where-Object {
        ($_.Extension -in @('.md', '.yaml', '.yml', '.json')) -and
        (
          ($_.Name -like 'generated-*') -or
          ($_.FullName.Replace('\', '/') -match '/knowledge/curated/')
        )
      }
  }
}

$forbiddenPatterns = @(
  'data/exports/',
  'snapshot_manifest\.json',
  'official_raw',
  'derived_metrics',
  'supercombo_enrichment',
  'published_run_id',
  'publication_state',
  '_manual_review',
  '\bmove_id\b',
  '[+-]?\d+F\b',
  '(startup|block advantage|hit advantage)\s*[:=]\s*[+-]?\d+'
)

$violations = @()
foreach ($file in $files) {
  $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
  foreach ($pattern in $forbiddenPatterns) {
    if ($content -match $pattern) {
      $violations += "$relativePath matches forbidden current-fact pattern: $pattern"
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Current-fact boundaries OK'
