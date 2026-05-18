Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$scopedRoots = @(
  'knowledge/curated',
  'knowledge/review'
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

function ConvertFrom-ScalarValue {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed -eq 'null') {
    return $null
  }
  if ($trimmed -eq 'true') {
    return $true
  }
  if ($trimmed -eq 'false') {
    return $false
  }
  if ($trimmed.Length -ge 2 -and $trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }
  return $trimmed
}

function Read-FrontMatter {
  param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

  $relativePath = $File.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8
  $normalized = $raw -replace "`r`n", "`n"

  if (-not $normalized.StartsWith("---`n")) {
    throw "$relativePath is missing front matter"
  }

  $frontMatterEnd = $normalized.IndexOf("`n---`n", 4)
  if ($frontMatterEnd -lt 0) {
    throw "$relativePath front matter is not closed"
  }

  $frontMatter = $normalized.Substring(4, $frontMatterEnd - 4)
  $metadata = [ordered]@{}
  $currentKey = $null

  foreach ($line in ($frontMatter -split "`n")) {
    if ($line -match '^([A-Za-z0-9_]+):\s*(.*)$') {
      $currentKey = $Matches[1]
      $metadata[$currentKey] = ConvertFrom-ScalarValue $Matches[2]
      continue
    }

    if ($null -ne $currentKey -and $line -match '^\s+-\s+(.+)$') {
      if (-not ($metadata[$currentKey] -is [System.Collections.IList])) {
        $previous = $metadata[$currentKey]
        $metadata[$currentKey] = @()
        if ($null -ne $previous -and "$previous".Trim().Length -gt 0) {
          $metadata[$currentKey] += $previous
        }
      }
      $metadata[$currentKey] += ConvertFrom-ScalarValue $Matches[1]
    }
  }

  return $metadata
}

$requiredCandidateMetadata = [ordered]@{
  authority_status = 'review_only'
  authority_role = 'review_only_current_fact_candidate'
  public_answer_allowed = $false
  generated_reference_allowed = $false
  accepted_current_fact_authority = $false
}

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
      'resolved into the current-fact data surfaces or kept on hold',
      'authority_status: review_only',
      'authority_role: review_only_current_fact_candidate',
      'public_answer_allowed: false',
      'generated_reference_allowed: false',
      'accepted_current_fact_authority: false',
      'do not verify, accept, promote, or publish current facts'
    )) {
      if ($candidateReadmeText -notmatch [regex]::Escape($needle)) {
        $violations += "knowledge/review/current-fact-candidates/README.md missing boundary text: $needle"
      }
    }
  }

  $candidateFiles = Get-ChildItem -LiteralPath $candidateRoot -Recurse -File |
    Where-Object {
      ($_.Name -ne 'README.md') -and
      ($_.Extension -in @('.md', '.yaml', '.yml', '.json'))
    }
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

    try {
      $metadata = Read-FrontMatter $candidateFile
    }
    catch {
      $violations += $_.Exception.Message
      continue
    }

    foreach ($field in $requiredCandidateMetadata.Keys) {
      $expected = $requiredCandidateMetadata[$field]
      if (-not $metadata.Contains($field)) {
        $violations += "$relativePath missing current-fact candidate metadata: $field"
        continue
      }

      $actual = $metadata[$field]
      if ($expected -is [bool]) {
        if (-not ($actual -is [bool]) -or $actual -ne $expected) {
          $violations += "$relativePath metadata $field must be $($expected.ToString().ToLowerInvariant())"
        }
        continue
      }

      if ($actual -ne $expected) {
        $violations += "$relativePath metadata $field must be $expected"
      }
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Current-fact boundaries OK'
