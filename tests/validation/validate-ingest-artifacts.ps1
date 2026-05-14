Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

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

function Assert-RequiredFields {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Metadata,
    [Parameter(Mandatory = $true)][string[]]$RequiredFields,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($field in $RequiredFields) {
    if (-not $Metadata.Contains($field)) {
      $Violations.Value += "$RelativePath missing metadata field: $field"
    } elseif ($null -ne $Metadata[$field] -and "$($Metadata[$field])".Trim().Length -eq 0) {
      $Violations.Value += "$RelativePath metadata field is empty: $field"
    }
  }
}

function Assert-EnumValue {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Metadata,
    [Parameter(Mandatory = $true)][string]$Field,
    [Parameter(Mandatory = $true)][string[]]$AllowedValues,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  if ($Metadata.Contains($Field) -and $Metadata[$Field] -notin $AllowedValues) {
    $Violations.Value += "$RelativePath has invalid $Field`: $($Metadata[$Field])"
  }
}

function Assert-Confidence {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Metadata,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  if ($Metadata.Contains('confidence')) {
    $confidence = 0.0
    if (-not [double]::TryParse([string]$Metadata['confidence'], [ref]$confidence) -or $confidence -lt 0 -or $confidence -gt 1) {
      $Violations.Value += "$RelativePath confidence must be a number from 0 to 1"
    }
  }
}

function Assert-NoReviewOnlyBoundaryBreaks {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($pattern in @(
    'generated_allowed:\s*true',
    '"generated_allowed"\s*:\s*true',
    'review_status:\s*accepted',
    '"review_status"\s*:\s*"accepted"'
  )) {
    if ($Content -match $pattern) {
      $Violations.Value += "$RelativePath violates review-only ingest boundary: $pattern"
    }
  }
}

$violations = @()

$sourceRoot = Join-Path $repoRoot 'knowledge/sources/articles'
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
  $violations += 'Missing source artifact directory: knowledge/sources/articles'
}
else {
  $sourceFiles = @(Get-ChildItem -LiteralPath $sourceRoot -File -Filter '*.md')
  if ($sourceFiles.Count -eq 0) {
    $violations += 'No source article artifacts found under knowledge/sources/articles'
  }

  $sourceRequiredFields = @(
    'id',
    'title',
    'source_kind',
    'source_role',
    'url',
    'accessed_at',
    'copyright_policy',
    'review_status',
    'review_after'
  )

  foreach ($file in $sourceFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $metadata = Read-FrontMatter $file
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8

    Assert-RequiredFields $relativePath $metadata $sourceRequiredFields ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'source_kind' $allowedSourceKinds ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'review_status' $allowedReviewStatus ([ref]$violations)

    foreach ($heading in @('# Source Summary', '## Extracted Scope', '## Reviewer Notes')) {
      if ($content -notmatch "(?m)^$([regex]::Escape($heading))\s*$") {
        $violations += "$relativePath missing required section: $heading"
      }
    }

    foreach ($needle in @('no full article text', 'final public answer evidence')) {
      if ($content -notmatch [regex]::Escape($needle)) {
        $violations += "$relativePath missing source boundary text: $needle"
      }
    }

    Assert-NoReviewOnlyBoundaryBreaks $relativePath $content ([ref]$violations)
  }
}

$claimsRoot = Join-Path $repoRoot 'knowledge/evidence/claims'
if (-not (Test-Path -LiteralPath $claimsRoot -PathType Container)) {
  $violations += 'Missing claim artifact directory: knowledge/evidence/claims'
}
else {
  $claimFiles = @(Get-ChildItem -LiteralPath $claimsRoot -File -Filter '*.claims.md')
  if ($claimFiles.Count -eq 0) {
    $violations += 'No evidence claim artifacts found under knowledge/evidence/claims'
  }

  $claimRequiredFields = @(
    'id',
    'title',
    'source_kind',
    'source_role',
    'verification_state',
    'confidence',
    'volatility',
    'patch_sensitivity',
    'review_status',
    'review_after',
    'source_refs'
  )

  foreach ($file in $claimFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $metadata = Read-FrontMatter $file
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8

    Assert-RequiredFields $relativePath $metadata $claimRequiredFields ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'source_kind' $allowedSourceKinds ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'verification_state' $allowedVerificationStates ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'volatility' $allowedVolatility ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'patch_sensitivity' $allowedPatchSensitivity ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'review_status' $allowedReviewStatus ([ref]$violations)
    Assert-Confidence $relativePath $metadata ([ref]$violations)

    if ($content -notmatch '(?m)^# Candidate Claims\s*$') {
      $violations += "$relativePath missing required section: # Candidate Claims"
    }

    foreach ($needle in @('review only', 'not accepted curated knowledge', 'must not feed generated references')) {
      if ($content -notmatch [regex]::Escape($needle)) {
        $violations += "$relativePath missing claim boundary text: $needle"
      }
    }

    foreach ($needle in @('"claim_kind"', '"statement"', '"evidence"', '"review_status"', '"source_refs"')) {
      if ($content -notmatch [regex]::Escape($needle)) {
        $violations += "$relativePath missing candidate claim field: $needle"
      }
    }

    if ($content -notmatch '(?m)^\s+path:\s*"knowledge/sources/(articles|videos)/') {
      $violations += "$relativePath source_refs must include a reviewable source artifact path"
    }

    Assert-NoReviewOnlyBoundaryBreaks $relativePath $content ([ref]$violations)
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Ingest artifacts OK'
