param(
  [switch]$Update
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$reportRelativePath = 'data/knowledge-lineage.json'
$reportPath = Join-Path $repoRoot $reportRelativePath
$generatorRelativePath = 'tests/validation/validate-knowledge-lineage-report.ps1 -Update'
$knowledgeRoots = @(
  'knowledge/sources',
  'knowledge/evidence',
  'knowledge/review',
  'knowledge/curated'
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

function Get-Stage {
  param([Parameter(Mandatory = $true)][string]$RelativePath)

  if ($RelativePath -like 'knowledge/sources/*') {
    return 'source'
  }
  if ($RelativePath -like 'knowledge/evidence/claims/*') {
    return 'evidence_claim'
  }
  if ($RelativePath -like 'knowledge/evidence/video-observations/*') {
    return 'evidence_observation'
  }
  if ($RelativePath -like 'knowledge/review/current-fact-candidates/*') {
    return 'review_current_fact_candidate'
  }
  if ($RelativePath -like 'knowledge/review/*') {
    return 'review'
  }
  if ($RelativePath -like 'knowledge/curated/*') {
    return 'curated'
  }
  return 'unknown'
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

function ConvertTo-CanonicalJson {
  param([Parameter(Mandatory = $true)][object]$Value)
  return (($Value | ConvertTo-Json -Depth 100) + "`n")
}

function New-KnowledgeLineageReport {
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

  $pathToArtifact = @{}
  foreach ($artifact in $artifacts) {
    $pathToArtifact[$artifact.RelativePath] = $artifact
  }

  $edgeMap = [ordered]@{}
  $danglingRefs = @()
  foreach ($artifact in $artifacts) {
    $sourceRefPaths = @(Get-SourceRefPaths $artifact.FrontMatter)
    foreach ($refPath in $sourceRefPaths) {
      if ($refPath -eq $artifact.RelativePath) {
        continue
      }
      $key = "$refPath -> $($artifact.RelativePath) [source_refs.path]"
      if (-not $edgeMap.Contains($key)) {
        $edgeMap[$key] = [ordered]@{
          from_path = $refPath
          to_path = $artifact.RelativePath
          relation = 'source_refs.path'
          referenced_path_exists = $pathToArtifact.ContainsKey($refPath)
        }
      }
      if (-not $pathToArtifact.ContainsKey($refPath)) {
        $danglingRefs += [ordered]@{
          artifact_path = $artifact.RelativePath
          referenced_path = $refPath
          relation = 'source_refs.path'
        }
      }
    }

    $repoLocalRefs = @(Get-RepoLocalReferencePaths $artifact.Content)
    foreach ($refPath in $repoLocalRefs) {
      if ($refPath -eq $artifact.RelativePath -or $sourceRefPaths -contains $refPath) {
        continue
      }
      $key = "$refPath -> $($artifact.RelativePath) [repo_local_reference]"
      if (-not $edgeMap.Contains($key)) {
        $edgeMap[$key] = [ordered]@{
          from_path = $refPath
          to_path = $artifact.RelativePath
          relation = 'repo_local_reference'
          referenced_path_exists = $pathToArtifact.ContainsKey($refPath)
        }
      }
      if (-not $pathToArtifact.ContainsKey($refPath)) {
        $danglingRefs += [ordered]@{
          artifact_path = $artifact.RelativePath
          referenced_path = $refPath
          relation = 'repo_local_reference'
        }
      }
    }
  }

  $edges = @(
    $edgeMap.Values |
      Sort-Object from_path, to_path, relation |
      ForEach-Object { $_ }
  )

  $incomingByPath = @{}
  $outgoingByPath = @{}
  foreach ($edge in $edges) {
    if ($edge.referenced_path_exists -ne $true) {
      continue
    }
    if (-not $incomingByPath.ContainsKey($edge.to_path)) {
      $incomingByPath[$edge.to_path] = @()
    }
    if (-not $outgoingByPath.ContainsKey($edge.from_path)) {
      $outgoingByPath[$edge.from_path] = @()
    }
    $incomingByPath[$edge.to_path] += $edge
    $outgoingByPath[$edge.from_path] += $edge
  }

  $nodes = @(
    $artifacts |
      ForEach-Object {
        $metadata = $_.Metadata
        $relativePath = $_.RelativePath
        $id = if ($metadata.Contains('id')) { [string]$metadata['id'] } else { $null }
        $title = if ($metadata.Contains('title')) { [string]$metadata['title'] } else { $null }
        $reviewStatus = if ($metadata.Contains('review_status')) { [string]$metadata['review_status'] } else { $null }
        $reviewAfter = if ($metadata.Contains('review_after')) { $metadata['review_after'] } else { $null }
        $generatedAllowed = if ($metadata.Contains('generated_allowed')) { $metadata['generated_allowed'] } else { $null }
        [ordered]@{
          path = $relativePath
          id = $id
          title = $title
          stage = Get-Stage $relativePath
          review_status = $reviewStatus
          review_after = $reviewAfter
          generated_allowed = $generatedAllowed
          upstream_ref_count = if ($incomingByPath.ContainsKey($relativePath)) { @($incomingByPath[$relativePath]).Count } else { 0 }
          downstream_ref_count = if ($outgoingByPath.ContainsKey($relativePath)) { @($outgoingByPath[$relativePath]).Count } else { 0 }
        }
      } |
      Sort-Object path
  )

  $nodesByPath = @{}
  foreach ($node in $nodes) {
    $nodesByPath[$node.path] = $node
  }

  $stageCounts = [ordered]@{}
  foreach ($stage in @(
    'source',
    'evidence_claim',
    'evidence_observation',
    'review',
    'review_current_fact_candidate',
    'curated',
    'unknown'
  )) {
    $stageCounts[$stage] = [int]@($nodes | Where-Object { $_.stage -eq $stage }).Count
  }

  $reviewStatusCounts = [ordered]@{}
  foreach ($status in @($nodes | ForEach-Object { $_.review_status } | Where-Object { $null -ne $_ -and "$_".Length -gt 0 } | Sort-Object -Unique)) {
    $reviewStatusCounts[$status] = [int]@($nodes | Where-Object { $_.review_status -eq $status }).Count
  }

  $curatedLineage = @(
    $nodes |
      Where-Object { $_.stage -eq 'curated' } |
      ForEach-Object {
        $curatedNode = $_
        $upstream = if ($incomingByPath.ContainsKey($curatedNode.path)) {
          @($incomingByPath[$curatedNode.path] | ForEach-Object { $_.from_path } | Sort-Object -Unique)
        } else {
          @()
        }
        $upstreamStages = @(
          $upstream |
            ForEach-Object {
              if ($nodesByPath.ContainsKey($_)) {
                $nodesByPath[$_].stage
              }
            } |
            Sort-Object -Unique
        )
        [ordered]@{
          curated_path = $curatedNode.path
          curated_id = $curatedNode.id
          upstream_paths = @($upstream)
          has_source_upstream = [bool]($upstreamStages -contains 'source')
          has_evidence_upstream = [bool](@($upstreamStages | Where-Object { $_ -like 'evidence_*' }).Count -gt 0)
          has_review_upstream = [bool](@($upstreamStages | Where-Object { $_ -like 'review*' }).Count -gt 0)
        }
      } |
      Sort-Object curated_path
  )

  return [ordered]@{
    schema_version = 'knowledge-lineage-report/v1'
    generated = $true
    generator = $generatorRelativePath
    last_generated = '2026-05-18'
    tracking_issue = '#262'
    source_paths = @($artifacts | ForEach-Object { $_.RelativePath } | Sort-Object)
    not_gameplay_authority = $true
    normal_public_answer_authority = $false
    summary = [ordered]@{
      node_count = [int]$nodes.Count
      edge_count = [int]$edges.Count
      dangling_ref_count = [int]$danglingRefs.Count
      stage_counts = $stageCounts
      review_status_counts = $reviewStatusCounts
    }
    nodes = @($nodes)
    edges = @($edges)
    dangling_refs = @($danglingRefs | Sort-Object artifact_path, referenced_path, relation)
    curated_lineage = @($curatedLineage)
  }
}

$expected = New-KnowledgeLineageReport
$expectedJson = ConvertTo-CanonicalJson $expected

if ($Update) {
  [System.IO.Directory]::CreateDirectory((Split-Path -Parent $reportPath)) | Out-Null
  $utf8NoBom = New-Object System.Text.UTF8Encoding $false
  [System.IO.File]::WriteAllText($reportPath, $expectedJson, $utf8NoBom)
  Write-Host "Knowledge lineage report updated: $reportRelativePath"
  return
}

if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
  throw "Missing knowledge lineage report: $reportRelativePath"
}

$actualJson = ConvertTo-CanonicalJson (Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json)
if ($actualJson -ne $expectedJson) {
  throw "Knowledge lineage report is stale. Regenerate with: pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-lineage-report.ps1 -Update"
}

if ($expected.normal_public_answer_authority -ne $false -or $expected.not_gameplay_authority -ne $true) {
  throw 'Knowledge lineage report must remain observability only, not answer authority'
}

Write-Host 'Knowledge lineage report OK'
