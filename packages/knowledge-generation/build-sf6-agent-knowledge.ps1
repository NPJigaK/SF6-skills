param(
  [string]$OutputRoot = $null
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$generatorRelativePath = 'packages/knowledge-generation/build-sf6-agent-knowledge.ps1'
$sourceRootRelativePath = 'knowledge/curated'
$targetRootRelativePath = 'skills/sf6-agent/references'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$sourceRoot = Join-Path $repoRoot $sourceRootRelativePath
$targetRoot = if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
  Join-Path $repoRoot $targetRootRelativePath
}
elseif ([System.IO.Path]::IsPathRooted($OutputRoot)) {
  $OutputRoot
}
else {
  Join-Path $repoRoot $OutputRoot
}

function ConvertTo-RepoRelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $resolved = (Resolve-Path -LiteralPath $Path).Path
  if (-not $resolved.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Path is outside repository root: $Path"
  }

  return $resolved.Substring($repoRoot.Length + 1).Replace('\', '/')
}

function ConvertFrom-FrontMatterValue {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed -eq 'null') {
    return ''
  }

  if ($trimmed.Length -ge 2 -and $trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }

  return $trimmed
}

function Read-CuratedPage {
  param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8
  $normalized = $raw -replace "`r`n", "`n"

  if (-not $normalized.StartsWith("---`n")) {
    throw "Curated page is missing front matter: $(ConvertTo-RepoRelativePath $File.FullName)"
  }

  $frontMatterEnd = $normalized.IndexOf("`n---`n", 4)
  if ($frontMatterEnd -lt 0) {
    throw "Curated page front matter is not closed: $(ConvertTo-RepoRelativePath $File.FullName)"
  }

  $frontMatter = $normalized.Substring(4, $frontMatterEnd - 4)
  $body = $normalized.Substring($frontMatterEnd + 5).Trim()
  $metadata = [ordered]@{}

  foreach ($line in ($frontMatter -split "`n")) {
    if ($line -match '^([A-Za-z0-9_]+):\s*(.*)$') {
      $metadata[$Matches[1]] = ConvertFrom-FrontMatterValue $Matches[2]
    }
  }

  foreach ($requiredKey in @(
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
    'review_after',
    'summary',
    'generated_allowed'
  )) {
    if (-not $metadata.Contains($requiredKey)) {
      throw "Curated page missing metadata '$requiredKey': $(ConvertTo-RepoRelativePath $File.FullName)"
    }
  }

  if ($metadata['generated_allowed'] -ne 'true') {
    throw "Curated page is not marked generated_allowed: $(ConvertTo-RepoRelativePath $File.FullName)"
  }

  $relativePath = ConvertTo-RepoRelativePath $File.FullName
  $section = if ($relativePath -match '/glossary/') {
    'Glossary'
  }
  elseif ($relativePath -match '/mechanics/') {
    'Mechanics'
  }
  else {
    'Concepts'
  }
  $bodyWithoutTitle = ($body -replace '(?m)^# .+\n?', '').Trim()
  $bodyWithoutTitle = $bodyWithoutTitle -replace '(?m)^### ', '#### '
  $bodyWithoutTitle = $bodyWithoutTitle -replace '(?m)^## ', '### '

  return [pscustomobject]@{
    Id = $metadata['id']
    Title = $metadata['title']
    ClaimKind = $metadata['claim_kind']
    SourceKind = $metadata['source_kind']
    SourceRole = $metadata['source_role']
    VerificationState = $metadata['verification_state']
    Confidence = $metadata['confidence']
    Volatility = $metadata['volatility']
    PatchSensitivity = $metadata['patch_sensitivity']
    ReviewStatus = $metadata['review_status']
    ReviewAfter = $metadata['review_after']
    Summary = $metadata['summary']
    RelativePath = $relativePath
    Section = $section
    Body = $bodyWithoutTitle
  }
}

function New-GeneratedHeader {
  param(
    [Parameter(Mandatory = $true)][string]$Title,
    [Parameter(Mandatory = $true)][string]$TargetPath,
    [Parameter(Mandatory = $true)][string[]]$SourcePaths
  )

  $lines = @(
    '---',
    'generated: true',
    "generator: $generatorRelativePath",
    'source_paths:'
  )
  foreach ($sourcePath in $SourcePaths) {
    $lines += "  - $sourcePath"
  }
  $lines += @(
    "target_path: $TargetPath",
    '---',
    '',
    "# $Title",
    '',
    'GENERATED FILE - DO NOT EDIT',
    "generator: $generatorRelativePath",
    "source_root: $sourceRootRelativePath",
    '',
    ('This file is derived from `' + $sourceRootRelativePath + '` and must be regenerated from curated source files.'),
    'It must not contain exact current frame values; exact current move values belong outside curated generated knowledge.',
    ''
  )

  return $lines
}

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
  throw "Missing source root: $sourceRootRelativePath"
}

$pages = Get-ChildItem -LiteralPath $sourceRoot -Recurse -File -Filter '*.md' |
  Where-Object { $_.Name -ne 'README.md' } |
  Sort-Object FullName |
  ForEach-Object { Read-CuratedPage $_ }

if (@($pages).Count -eq 0) {
  throw "No curated pages found under $sourceRootRelativePath"
}

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

$sourcePaths = @($pages | ForEach-Object { $_.RelativePath })
$indexTargetPath = "$targetRootRelativePath/generated-knowledge-index.md"
$conceptTargetPath = "$targetRootRelativePath/generated-concepts.md"

$indexLines = New-GeneratedHeader 'Generated Knowledge Index' $indexTargetPath $sourcePaths
$indexLines += @(
  '## Sources',
  '',
  '| Title | Section | Claim Kind | Source | Verification | Confidence | Volatility | Patch Sensitivity | Review |',
  '| --- | --- | --- | --- | --- | --- | --- | --- | --- |'
)

foreach ($page in $pages) {
  $indexLines += "| $($page.Title) | $($page.Section) | $($page.ClaimKind) | $($page.RelativePath) | $($page.VerificationState) | $($page.Confidence) | $($page.Volatility) | $($page.PatchSensitivity) | $($page.ReviewStatus) |"
}

$indexLines += @(
  '',
  '## Boundary',
  '',
  'This generated index is a derived navigation aid. Use the cited curated source files for review decisions, and do not add exact current frame values here.'
)

$conceptLines = New-GeneratedHeader 'Generated Concepts' $conceptTargetPath $sourcePaths
$conceptLines += @(
  '## Boundary',
  '',
  'The entries below are derived summaries and concept text from curated v2 knowledge. They are suitable for stable concept grounding only and must not be used as exact current frame data.',
  ''
)

foreach ($page in $pages) {
  $reviewAfter = if ([string]::IsNullOrWhiteSpace($page.ReviewAfter)) { 'null' } else { $page.ReviewAfter }
  $conceptLines += @(
    "## $($page.Title)",
    '',
    "- source: $($page.RelativePath)",
    "- claim_kind: $($page.ClaimKind)",
    "- source_kind: $($page.SourceKind)",
    "- source_role: $($page.SourceRole)",
    "- verification_state: $($page.VerificationState)",
    "- confidence: $($page.Confidence)",
    "- volatility: $($page.Volatility)",
    "- patch_sensitivity: $($page.PatchSensitivity)",
    "- review_status: $($page.ReviewStatus)",
    "- review_after: $reviewAfter",
    "- summary: $($page.Summary)",
    '',
    $page.Body,
    ''
  )
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$indexText = (($indexLines -join "`n").TrimEnd("`n") + "`n")
$conceptText = (($conceptLines -join "`n").TrimEnd("`n") + "`n")
[System.IO.File]::WriteAllText(
  (Join-Path $targetRoot 'generated-knowledge-index.md'),
  $indexText,
  $utf8NoBom
)
[System.IO.File]::WriteAllText(
  (Join-Path $targetRoot 'generated-concepts.md'),
  $conceptText,
  $utf8NoBom
)

Write-Host "Generated skills/sf6-agent/references/generated-knowledge-index.md"
Write-Host "Generated skills/sf6-agent/references/generated-concepts.md"
