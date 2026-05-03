Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$scopedRoots = @(
  'knowledge/curated',
  'knowledge/review',
  'skills/sf6-agent/references'
)

$files = @()
foreach ($relativeRoot in $scopedRoots) {
  $root = Join-Path $repoRoot $relativeRoot
  if (Test-Path -LiteralPath $root -PathType Container) {
    $files += Get-ChildItem -LiteralPath $root -Recurse -File |
      Where-Object {
        $normalizedPath = $_.FullName.Replace('\', '/')
        ($_.Extension -in @('.md', '.yaml', '.yml', '.json')) -and
        (
          ($_.Name -like 'generated-*') -or
          ($normalizedPath -match '/knowledge/curated/') -or
          (
            ($normalizedPath -match '/knowledge/review/') -and
            ($normalizedPath -notmatch '/knowledge/review/current-fact-candidates/')
          )
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

$candidateRoot = Join-Path $repoRoot 'knowledge/review/current-fact-candidates'
if (Test-Path -LiteralPath $candidateRoot -PathType Container) {
  $candidateReadme = Join-Path $candidateRoot 'README.md'
  if (-not (Test-Path -LiteralPath $candidateReadme -PathType Leaf)) {
    $violations += 'knowledge/review/current-fact-candidates must include README.md'
  }
  else {
    $candidateReadmeText = Get-Content -LiteralPath $candidateReadme -Raw -Encoding UTF8
    foreach ($needle in @(
      'not final public answer evidence',
      'must not feed generated knowledge references',
      'resolved into the current-fact data surfaces or kept on hold'
    )) {
      if ($candidateReadmeText -notmatch [regex]::Escape($needle)) {
        $violations += "knowledge/review/current-fact-candidates/README.md missing boundary text: $needle"
      }
    }
  }

  $candidateFiles = Get-ChildItem -LiteralPath $candidateRoot -Recurse -File |
    Where-Object { $_.Extension -in @('.md', '.yaml', '.yml', '.json') }
  foreach ($candidateFile in $candidateFiles) {
    $relativePath = $candidateFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $content = Get-Content -LiteralPath $candidateFile.FullName -Raw -Encoding UTF8
    foreach ($pattern in @(
      '(?m)^\s*generated_allowed:\s*"?true"?\s*$',
      '"generated_allowed"\s*:\s*true',
      '(?m)^\s*review_status:\s*"?accepted"?\s*$',
      '"review_status"\s*:\s*"accepted"'
    )) {
      if ($content -match $pattern) {
        $violations += "$relativePath violates current-fact candidate review-only boundary: $pattern"
      }
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Current-fact boundaries OK'
