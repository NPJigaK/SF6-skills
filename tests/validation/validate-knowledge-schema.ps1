Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$knowledgeRoots = @(
  'knowledge/curated',
  'knowledge/review'
)

$requiredFields = @(
  'id',
  'title',
  'claim_kind',
  'source_kind',
  'source_role',
  'evidence_basis',
  'verification_state',
  'confidence',
  'volatility',
  'patch_sensitivity',
  'review_status',
  'source_refs',
  'review_after'
)

$allowedClaimKinds = @('stable_concept', 'strategy_or_matchup', 'observation', 'unresolved')
$allowedSourceKinds = @('official', 'reproducible_observation', 'maintained_third_party', 'community', 'maintainer_note', 'unknown')
$allowedVerificationStates = @('verified', 'partially_verified', 'unverified', 'conflicting', 'not_applicable')
$allowedVolatility = @('stable', 'patch_sensitive', 'volatile', 'unknown')
$allowedPatchSensitivity = @('none', 'low', 'medium', 'high', 'unknown')
$allowedReviewStatus = @('accepted', 'needs_review', 'rejected', 'deprecated')

function ConvertFrom-ScalarValue {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed -eq 'null') {
    return $null
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

$files = @()
foreach ($relativeRoot in $knowledgeRoots) {
  $root = Join-Path $repoRoot $relativeRoot
  if (Test-Path -LiteralPath $root -PathType Container) {
    $files += Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md' |
      Where-Object {
        $normalizedPath = $_.FullName.Replace('\', '/')
        ($_.Name -ne 'README.md') -and
        ($normalizedPath -notmatch '/knowledge/review/current-fact-candidates/')
      }
  }
}

if (@($files).Count -eq 0) {
  throw 'No knowledge pages found'
}

$violations = @()
foreach ($file in $files) {
  $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $metadata = Read-FrontMatter $file

  foreach ($field in $requiredFields) {
    if (-not $metadata.Contains($field)) {
      $violations += "$relativePath missing metadata field: $field"
    }
  }

  if ($metadata.Contains('claim_kind') -and $metadata['claim_kind'] -notin $allowedClaimKinds) {
    $violations += "$relativePath has invalid claim_kind: $($metadata['claim_kind'])"
  }
  if ($metadata.Contains('source_kind') -and $metadata['source_kind'] -notin $allowedSourceKinds) {
    $violations += "$relativePath has invalid source_kind: $($metadata['source_kind'])"
  }
  if ($metadata.Contains('verification_state') -and $metadata['verification_state'] -notin $allowedVerificationStates) {
    $violations += "$relativePath has invalid verification_state: $($metadata['verification_state'])"
  }
  if ($metadata.Contains('volatility') -and $metadata['volatility'] -notin $allowedVolatility) {
    $violations += "$relativePath has invalid volatility: $($metadata['volatility'])"
  }
  if ($metadata.Contains('patch_sensitivity') -and $metadata['patch_sensitivity'] -notin $allowedPatchSensitivity) {
    $violations += "$relativePath has invalid patch_sensitivity: $($metadata['patch_sensitivity'])"
  }
  if ($metadata.Contains('review_status') -and $metadata['review_status'] -notin $allowedReviewStatus) {
    $violations += "$relativePath has invalid review_status: $($metadata['review_status'])"
  }

  if ($metadata.Contains('confidence')) {
    $confidence = 0.0
    if (-not [double]::TryParse([string]$metadata['confidence'], [ref]$confidence) -or $confidence -lt 0 -or $confidence -gt 1) {
      $violations += "$relativePath confidence must be a number from 0 to 1"
    }
  }

  $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
  if ($relativePath -match '^knowledge/curated/' -and $content -notmatch '(?m)^\s+path:\s*') {
    $violations += "$relativePath source_refs must include a reviewable path"
  }
  foreach ($forbidden in @('source_tier', '[概念のみ]', 'T1 / T2 / T3 / T4', 'core / mixed / current-fact')) {
    if ($content -match [regex]::Escape($forbidden)) {
      $violations += "$relativePath contains legacy canonical taxonomy text: $forbidden"
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Knowledge schema OK'
