Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$allowedSourceKinds = @('official', 'reproducible_observation', 'maintained_third_party', 'community', 'maintainer_note', 'unknown')
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

function Assert-FieldValue {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Metadata,
    [Parameter(Mandatory = $true)][string]$Field,
    [Parameter(Mandatory = $true)][string]$ExpectedValue,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  if ($Metadata.Contains($Field) -and $Metadata[$Field] -ne $ExpectedValue) {
    $Violations.Value += "$RelativePath $Field must be $ExpectedValue for video observation artifacts"
  }
}

function Assert-ReviewStatusNotAccepted {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][System.Collections.IDictionary]$Metadata,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  if ($Metadata.Contains('review_status') -and $Metadata['review_status'] -eq 'accepted') {
    $Violations.Value += "$RelativePath review_status must not be accepted for review-only video artifacts"
  }
}

function Assert-RequiredSections {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string[]]$Headings,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($heading in $Headings) {
    if ($Content -notmatch "(?m)^$([regex]::Escape($heading))\s*$") {
      $Violations.Value += "$RelativePath missing required section: $heading"
    }
  }
}

function Assert-RequiredText {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string[]]$Needles,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($needle in $Needles) {
    if ($Content -notmatch [regex]::Escape($needle)) {
      $Violations.Value += "$RelativePath missing required boundary text: $needle"
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
      $Violations.Value += "$RelativePath violates review-only video artifact boundary: $pattern"
    }
  }
}

function Assert-NoRepoStoredMediaClaims {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($pattern in @(
    'Raw media stored in repo:\s*yes',
    'Raw video stored in repo:\s*yes',
    'Raw frames or screenshots stored in repo:\s*yes',
    'Screenshots stored in repo:\s*yes',
    'Downloaded videos stored in repo:\s*yes',
    'Full transcript stored in repo:\s*yes',
    'Full captions stored in repo:\s*yes'
  )) {
    if ($Content -match $pattern) {
      $Violations.Value += "$RelativePath claims forbidden raw media/transcript repo storage: $pattern"
    }
  }
}

function Assert-VideoSourceRefsExist {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  $matches = @([regex]::Matches($Content, 'knowledge/sources/videos/[A-Za-z0-9._/-]+\.md'))
  if ($matches.Count -eq 0) {
    $Violations.Value += "$RelativePath must reference at least one video source artifact under knowledge/sources/videos"
    return
  }

  foreach ($match in $matches) {
    $sourcePath = $match.Value
    if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $sourcePath) -PathType Leaf)) {
      $Violations.Value += "$RelativePath references missing video source artifact: $sourcePath"
    }
  }
}

$violations = @()

$videoSourceRoot = Join-Path $repoRoot 'knowledge/sources/videos'
if (-not (Test-Path -LiteralPath $videoSourceRoot -PathType Container)) {
  $violations += 'Missing video source artifact directory: knowledge/sources/videos'
}
else {
  $videoSourceFiles = @(Get-ChildItem -LiteralPath $videoSourceRoot -File -Filter '*.md')
  if ($videoSourceFiles.Count -eq 0) {
    $violations += 'No video source artifacts found under knowledge/sources/videos'
  }

  $sourceRequiredFields = @(
    'id',
    'title',
    'source_kind',
    'source_role',
    'url',
    'accessed_at',
    'captured_at',
    'copyright_policy',
    'review_status',
    'review_after'
  )

  foreach ($file in $videoSourceFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $metadata = Read-FrontMatter $file
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8

    Assert-RequiredFields $relativePath $metadata $sourceRequiredFields ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'source_kind' $allowedSourceKinds ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'review_status' $allowedReviewStatus ([ref]$violations)
    Assert-ReviewStatusNotAccepted $relativePath $metadata ([ref]$violations)

    Assert-RequiredSections $relativePath $content @('# Source Summary', '## Extracted Scope', '## Media Handling', '## Reviewer Notes') ([ref]$violations)
    Assert-RequiredText $relativePath $content @(
      'not final public answer evidence',
      'Raw video, frames, screenshots',
      'full captions/transcript are not stored',
      'Scratch/cache handling followed'
    ) ([ref]$violations)

    Assert-NoReviewOnlyBoundaryBreaks $relativePath $content ([ref]$violations)
    Assert-NoRepoStoredMediaClaims $relativePath $content ([ref]$violations)
  }
}

$videoObservationRoot = Join-Path $repoRoot 'knowledge/evidence/video-observations'
if (-not (Test-Path -LiteralPath $videoObservationRoot -PathType Container)) {
  $violations += 'Missing video observation artifact directory: knowledge/evidence/video-observations'
}
else {
  $videoObservationFiles = @(Get-ChildItem -LiteralPath $videoObservationRoot -File -Filter '*.observations.md')
  if ($videoObservationFiles.Count -eq 0) {
    $violations += 'No video observation artifacts found under knowledge/evidence/video-observations'
  }

  $observationRequiredFields = @(
    'id',
    'title',
    'source_kind',
    'source_role',
    'review_status',
    'review_after'
  )

  foreach ($file in $videoObservationFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $metadata = Read-FrontMatter $file
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8

    Assert-RequiredFields $relativePath $metadata $observationRequiredFields ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'source_kind' $allowedSourceKinds ([ref]$violations)
    Assert-EnumValue $relativePath $metadata 'review_status' $allowedReviewStatus ([ref]$violations)
    Assert-FieldValue $relativePath $metadata 'review_status' 'needs_review' ([ref]$violations)

    Assert-RequiredSections $relativePath $content @('## Source', '## Timestamped Observations', '## Boundary Notes') ([ref]$violations)
    Assert-RequiredText $relativePath $content @(
      'not accepted strategy knowledge',
      'must not feed generated references',
      'Raw media stored in repo: no',
      'Full transcript stored in repo: no',
      'review-only observations',
      'not accepted current facts'
    ) ([ref]$violations)

    foreach ($needle in @('| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |', '"schema_version": "2.0.0"', '"clip_metadata"', '"actor_bindings"', '"segments"', '"segment_id"', '"confidence"')) {
      if ($content -notmatch [regex]::Escape($needle)) {
        $violations += "$relativePath missing video observation shape text: $needle"
      }
    }

    Assert-VideoSourceRefsExist $relativePath $content ([ref]$violations)
    Assert-NoReviewOnlyBoundaryBreaks $relativePath $content ([ref]$violations)
    Assert-NoRepoStoredMediaClaims $relativePath $content ([ref]$violations)
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Video artifacts OK'
