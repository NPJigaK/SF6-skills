param(
  [switch]$Update,
  [string]$AsOfDate = $null
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$reportRelativePath = 'data/knowledge-integrity.json'
$reportPath = Join-Path $repoRoot $reportRelativePath
$generatorRelativePath = 'tests/validation/validate-knowledge-integrity-report.ps1 -Update'
$knowledgeRoots = @(
  'knowledge/sources',
  'knowledge/evidence',
  'knowledge/review',
  'knowledge/curated'
)
$generatedReferenceGlob = 'skills/sf6-agent/references/generated-*'
$generatedContaminationPatterns = @(
  'knowledge/evidence/',
  'knowledge/review/',
  'knowledge/sources/',
  'data/exports/',
  'official_raw',
  'snapshot_manifest.json',
  '_manual_review'
)

function ConvertTo-RelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $resolved = (Resolve-Path -LiteralPath $Path).Path
  return $resolved.Substring($repoRoot.Length + 1).Replace('\', '/')
}

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

function Read-MarkdownArtifact {
  param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

  $relativePath = ConvertTo-RelativePath $File.FullName
  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8
  $normalized = $raw -replace "`r`n", "`n"
  $frontMatter = ''
  $metadata = [ordered]@{}

  if ($normalized.StartsWith("---`n")) {
    $frontMatterEnd = $normalized.IndexOf("`n---`n", 4)
    if ($frontMatterEnd -lt 0) {
      throw "$relativePath front matter is not closed"
    }

    $frontMatter = $normalized.Substring(4, $frontMatterEnd - 4)
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
  }

  return [pscustomobject]@{
    RelativePath = $relativePath
    Content = $normalized
    FrontMatter = $frontMatter
    Metadata = $metadata
  }
}

function Get-SourceRefPaths {
  param([Parameter(Mandatory = $true)][string]$FrontMatter)

  $paths = @()
  foreach ($match in [regex]::Matches($FrontMatter, '(?m)^\s+path:\s*"?([^"`r`n]+)"?\s*$')) {
    $paths += [string]$match.Groups[1].Value.Trim()
  }
  return @($paths | Sort-Object -Unique)
}

function Get-RepoLocalReferencePaths {
  param([Parameter(Mandatory = $true)][string]$Content)

  $paths = @()
  foreach ($match in [regex]::Matches($Content, 'knowledge/(?:sources|evidence|review|curated)/[A-Za-z0-9._/\-]+\.md')) {
    $paths += [string]$match.Value
  }
  return @($paths | Sort-Object -Unique)
}

function Get-GeneratedReferenceFiles {
  $referenceRoot = Join-Path $repoRoot 'skills/sf6-agent/references'
  if (-not (Test-Path -LiteralPath $referenceRoot -PathType Container)) {
    return @()
  }
  return @(
    Get-ChildItem -LiteralPath $referenceRoot -File -Filter 'generated-*' |
      Sort-Object FullName
  )
}

function ConvertTo-CanonicalJson {
  param([Parameter(Mandatory = $true)][object]$Value)
  return (($Value | ConvertTo-Json -Depth 100) + "`n")
}

function Test-RelativePathExists {
  param([Parameter(Mandatory = $true)][string]$RelativePath)

  $fullPath = Join-Path $repoRoot $RelativePath
  return Test-Path -LiteralPath $fullPath -PathType Leaf
}

function New-KnowledgeIntegrityReport {
  param([Parameter(Mandatory = $true)][string]$ReportAsOfDate)

  $artifactFiles = @()
  foreach ($rootRelativePath in $knowledgeRoots) {
    $root = Join-Path $repoRoot $rootRelativePath
    if (Test-Path -LiteralPath $root -PathType Container) {
      $artifactFiles += Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md' |
        Where-Object { $_.Name -ne 'README.md' }
    }
  }

  if ($artifactFiles.Count -eq 0) {
    throw 'No knowledge artifacts found'
  }

  $artifacts = @(
    $artifactFiles |
      Sort-Object FullName |
      ForEach-Object { Read-MarkdownArtifact $_ }
  )

  $generatedReferences = @(
    Get-GeneratedReferenceFiles |
      ForEach-Object { Read-MarkdownArtifact $_ }
  )

  $duplicateIds = @()
  $idGroups = @{}
  foreach ($artifact in $artifacts) {
    if (-not $artifact.Metadata.Contains('id')) {
      continue
    }
    $id = [string]$artifact.Metadata['id']
    if ([string]::IsNullOrWhiteSpace($id)) {
      continue
    }
    if (-not $idGroups.ContainsKey($id)) {
      $idGroups[$id] = @()
    }
    $idGroups[$id] += $artifact.RelativePath
  }
  foreach ($id in @($idGroups.Keys | Sort-Object)) {
    $paths = @($idGroups[$id] | Sort-Object)
    if ($paths.Count -gt 1) {
      $duplicateIds += [ordered]@{
        id = $id
        paths = $paths
      }
    }
  }

  $danglingRefs = @()
  foreach ($artifact in $artifacts) {
    foreach ($refPath in @(Get-SourceRefPaths $artifact.FrontMatter)) {
      if (-not (Test-RelativePathExists $refPath)) {
        $danglingRefs += [ordered]@{
          artifact_path = $artifact.RelativePath
          referenced_path = $refPath
          relation = 'source_refs.path'
        }
      }
    }

    foreach ($refPath in @(Get-RepoLocalReferencePaths $artifact.Content)) {
      if ($refPath -eq $artifact.RelativePath) {
        continue
      }
      if (-not (Test-RelativePathExists $refPath)) {
        $danglingRefs += [ordered]@{
          artifact_path = $artifact.RelativePath
          referenced_path = $refPath
          relation = 'repo_local_reference'
        }
      }
    }
  }
  $danglingRefs = @(
    $danglingRefs |
      Sort-Object artifact_path, referenced_path, relation |
      ForEach-Object { $_ }
  )

  $invalidReviewAfter = @()
  $reviewAfterOverdue = @()
  $asOf = [datetime]::ParseExact($ReportAsOfDate, 'yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture)
  foreach ($artifact in $artifacts) {
    if (-not $artifact.Metadata.Contains('review_after')) {
      continue
    }
    $reviewAfterValue = $artifact.Metadata['review_after']
    if ($null -eq $reviewAfterValue -or [string]::IsNullOrWhiteSpace([string]$reviewAfterValue)) {
      continue
    }

    try {
      $reviewAfter = [datetime]::ParseExact([string]$reviewAfterValue, 'yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture)
    } catch {
      $invalidReviewAfter += [ordered]@{
        artifact_path = $artifact.RelativePath
        review_after = [string]$reviewAfterValue
        expected_format = 'yyyy-MM-dd'
      }
      continue
    }

    if ($reviewAfter.Date -lt $asOf.Date) {
      $reviewAfterOverdue += [ordered]@{
        artifact_path = $artifact.RelativePath
        review_after = $reviewAfter.ToString('yyyy-MM-dd')
        as_of_date = $asOf.ToString('yyyy-MM-dd')
      }
    }
  }
  $invalidReviewAfter = @(
    $invalidReviewAfter |
      Sort-Object artifact_path |
      ForEach-Object { $_ }
  )
  $reviewAfterOverdue = @(
    $reviewAfterOverdue |
      Sort-Object review_after, artifact_path |
      ForEach-Object { $_ }
  )

  $generatedContamination = @()
  foreach ($reference in $generatedReferences) {
    foreach ($refPath in @(Get-SourceRefPaths $reference.FrontMatter)) {
      if (-not $refPath.StartsWith('knowledge/curated/')) {
        $generatedContamination += [ordered]@{
          path = $reference.RelativePath
          contamination_kind = 'front_matter_source_path'
          pattern_or_source_path = $refPath
        }
      }
    }

    foreach ($pattern in $generatedContaminationPatterns) {
      if ($reference.Content.Contains($pattern)) {
        $generatedContamination += [ordered]@{
          path = $reference.RelativePath
          contamination_kind = 'generated_content_pattern'
          pattern_or_source_path = $pattern
        }
      }
    }
  }
  $generatedContamination = @(
    $generatedContamination |
      Sort-Object path, contamination_kind, pattern_or_source_path |
      ForEach-Object { $_ }
  )

  $sourcePaths = @(
    @($artifacts | ForEach-Object { $_.RelativePath }) +
    @($generatedReferences | ForEach-Object { $_.RelativePath }) |
      Sort-Object -Unique
  )

  return [ordered]@{
    schema_version = 'knowledge-integrity-report/v1'
    generated = $true
    generator = $generatorRelativePath
    last_generated = $ReportAsOfDate
    tracking_issue = '#264'
    as_of_date = $ReportAsOfDate
    source_paths = $sourcePaths
    not_gameplay_authority = $true
    normal_public_answer_authority = $false
    summary = [ordered]@{
      knowledge_artifact_count = @($artifacts).Count
      generated_reference_count = @($generatedReferences).Count
      duplicate_id_count = @($duplicateIds).Count
      dangling_ref_count = @($danglingRefs).Count
      invalid_review_after_count = @($invalidReviewAfter).Count
      review_after_overdue_count = @($reviewAfterOverdue).Count
      generated_contamination_count = @($generatedContamination).Count
    }
    duplicate_ids = $duplicateIds
    dangling_refs = $danglingRefs
    invalid_review_after = $invalidReviewAfter
    review_after_overdue = $reviewAfterOverdue
    generated_contamination = $generatedContamination
  }
}

if ($Update) {
  if ([string]::IsNullOrWhiteSpace($AsOfDate)) {
    $AsOfDate = (Get-Date).ToString('yyyy-MM-dd')
  }
  $report = New-KnowledgeIntegrityReport -ReportAsOfDate $AsOfDate
  [System.IO.File]::WriteAllText($reportPath, (ConvertTo-CanonicalJson $report), [System.Text.UTF8Encoding]::new($false))
  Write-Host "Updated $reportRelativePath"
}

if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
  throw "Missing knowledge integrity report: $reportRelativePath. Run $generatorRelativePath"
}

$existingReport = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]::IsNullOrWhiteSpace($AsOfDate)) {
  $AsOfDate = [string]$existingReport.as_of_date
}

$expectedReport = New-KnowledgeIntegrityReport -ReportAsOfDate $AsOfDate
$expectedJson = ConvertTo-CanonicalJson $expectedReport
$actualJson = ConvertTo-CanonicalJson $existingReport

if ($actualJson -ne $expectedJson) {
  throw "$reportRelativePath is stale. Run $generatorRelativePath"
}

$issues = @()
if ($existingReport.schema_version -ne 'knowledge-integrity-report/v1') {
  $issues += "$reportRelativePath must use schema_version knowledge-integrity-report/v1"
}
if ($existingReport.generated -ne $true) {
  $issues += "$reportRelativePath must be marked generated"
}
if ($existingReport.generator -ne $generatorRelativePath) {
  $issues += "$reportRelativePath must declare generator $generatorRelativePath"
}
if ($existingReport.not_gameplay_authority -ne $true) {
  $issues += "$reportRelativePath must declare not_gameplay_authority true"
}
if ($existingReport.normal_public_answer_authority -ne $false) {
  $issues += "$reportRelativePath must not be normal public answer authority"
}
if ($existingReport.summary.duplicate_id_count -gt 0) {
  $issues += "$reportRelativePath has duplicate knowledge artifact IDs"
}
if ($existingReport.summary.dangling_ref_count -gt 0) {
  $issues += "$reportRelativePath has dangling knowledge refs"
}
if ($existingReport.summary.invalid_review_after_count -gt 0) {
  $issues += "$reportRelativePath has invalid review_after values"
}
if ($existingReport.summary.generated_contamination_count -gt 0) {
  $issues += "$reportRelativePath has generated-reference contamination"
}

if ($issues.Count -gt 0) {
  $issues | ForEach-Object { Write-Host $_ }
  throw "Knowledge integrity report validation failed with $($issues.Count) issue(s)"
}

Write-Host "Knowledge integrity report OK"
