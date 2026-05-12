Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$templateRelativePath = 'docs/testing/smoke-runs/video-analysis-learning-report-template.md'
$templatePath = Join-Path $repoRoot $templateRelativePath

function Assert-Contains {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$Needle,
    [Parameter(Mandatory = $true)][string]$Description,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if ($Content -notmatch [regex]::Escape($Needle)) {
    $Issues.Value += "Missing $Description`: $Needle"
  }
}

function Assert-Matches {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$Pattern,
    [Parameter(Mandatory = $true)][string]$Description,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if ($Content -notmatch $Pattern) {
    $Issues.Value += "Missing $Description"
  }
}

function Assert-RequiredSections {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string[]]$Headings,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($heading in $Headings) {
    if ($Content -notmatch "(?m)^$([regex]::Escape($heading))\s*$") {
      $Issues.Value += "Missing required section: $heading"
    }
  }
}

function Assert-NoRawTranscriptMarkers {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($marker in @('RAW TRANSCRIPT', 'assistant:', 'user:', 'tool_call')) {
    if ($Content -cmatch [regex]::Escape($marker)) {
      $Issues.Value += "Template contains raw transcript marker: $marker"
    }
  }
}

function Assert-NoLiveUrls {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($pattern in @(
    '(?i)https?://',
    '(?i)\byoutube\.com\b',
    '(?i)\byoutu\.be\b',
    '(?i)\btwitch\.tv\b'
  )) {
    if ($Content -match $pattern) {
      $Issues.Value += 'Template contains a live or fetchable URL; use non-fetching placeholders or repo source references'
    }
  }
}

function Assert-NoBinaryMediaPaths {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $binaryPathPattern = '(?i)(^|["''\s:/\\])([A-Za-z0-9_.-]+[\\/])+[A-Za-z0-9_.-]+\.(gif|png|jpg|jpeg|webp|mp4|mov|avi|mkv)(["''\s,)}\]]|$)'
  if ($Content -match $binaryPathPattern) {
    $Issues.Value += 'Template contains a path-like binary media reference'
  }
}

function Assert-NoActiveForbiddenStorage {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $verbPattern = '\b(commit|store|save|persist|add|include|write|retain)\b'
  $objectPattern = '\b(raw video|frames?|screenshots?|gifs?|contact sheets?|browser cache|full transcripts?|raw hermes output|raw `?video_analyze`? output|local hermes sessions?|sessions?|memory|local skills?|curator output|logs?|caches?|credentials?|secrets?)\b'
  $negationPattern = '\b(do not|must not|not|no|none|never|forbid|forbidden|exclude|excluded|without|is not|are not)\b'

  foreach ($line in ($Content -split "`r?`n")) {
    if ($line -match "(?i)$verbPattern" -and $line -match "(?i)$objectPattern" -and $line -notmatch "(?i)$negationPattern") {
      $Issues.Value += "Potential active forbidden storage instruction: $line"
    }
  }
}

$issues = @()

if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) {
  throw "Missing video learning report template: $templateRelativePath"
}

$raw = Get-Content -LiteralPath $templatePath -Raw -Encoding UTF8

Assert-Contains $raw 'TEMPLATE ONLY' 'template-only marker' ([ref]$issues)
Assert-Contains $raw 'not an executed report' 'not-executed marker' ([ref]$issues)
Assert-Contains $raw 'executed learning report' 'executed learning report distinction' ([ref]$issues)
Assert-Contains $raw 'historical smoke report' 'historical smoke report distinction' ([ref]$issues)
Assert-Contains $raw 'docs/testing/smoke-runs/video-analysis-learning-report-YYYYMMDD-<slug>.md' 'executed report naming convention' ([ref]$issues)
Assert-Contains $raw 'Historical smoke reports are not rewritten' 'historical smoke rewrite boundary' ([ref]$issues)
Assert-Contains $raw 'Existing Video Smoke Report Audit' 'existing smoke report audit section' ([ref]$issues)

foreach ($auditedReport in @(
  'docs/testing/smoke-runs/2026-05-03-video-observation-youtube-shorts-sycyvw6h8wi.md',
  'docs/testing/smoke-runs/2026-05-04-jp-combo-damage-oracle-fixture.md',
  'docs/testing/smoke-runs/2026-05-04-jp-combo-damage-oracle-coverage.md',
  'docs/testing/smoke-runs/hermes-bridge-smoke-gap-report.md'
)) {
  Assert-Contains $raw $auditedReport 'audited smoke report path' ([ref]$issues)
}

Assert-RequiredSections $raw @(
  '## Report Metadata',
  '## Raw Media And Local State Status',
  '## Tool Availability',
  '## Source And Reference Policy',
  '## Video Taxonomy Classification',
  '## Visual Layout',
  '## Audio And Commentary Context',
  '## Analysis Capability',
  '## Observed-Safe Notes',
  '## Not-Inferred Notes',
  '## Gap / Failure Findings',
  '## Follow-Up Candidates',
  '## Authority Boundaries',
  '## Cleanup And Verification'
) ([ref]$issues)

foreach ($taxonomyField in @('video_type', 'unknown_or_mixed', 'exact_current_fact', 'official_raw')) {
  Assert-Contains $raw $taxonomyField 'taxonomy or authority field' ([ref]$issues)
}
Assert-Matches $raw '(?is)exact_current_fact.{0,160}forbidden|forbidden.{0,160}exact_current_fact' 'exact_current_fact forbidden boundary' ([ref]$issues)

foreach ($requiredText in @(
  'raw video',
  'frames',
  'screenshots',
  'GIFs',
  'contact sheets',
  'browser cache',
  'full transcripts',
  'raw Hermes output',
  'raw `video_analyze` output',
  'local Hermes sessions',
  'memory',
  'local skills',
  'Curator output',
  'logs',
  'caches',
  'credentials',
  'secrets',
  'observations are review input',
  'observed damage labels are review/eval context only',
  'Training UI observations are not current-system authority by default',
  'Exact current facts not inferred',
  '`official_raw` not overridden',
  'Video observations are observation/review input only',
  'Hermes/video outputs are draft input',
  'External visual atlas sources are not current-fact authority',
  '`official_raw` remains current-fact authority',
  'No public `sf6-agent` behavior change'
)) {
  Assert-Contains $raw $requiredText 'required boundary text' ([ref]$issues)
}

foreach ($gapCategory in @(
  'overlay blocks important area',
  'subtitles cover input/HUD',
  'vertical crop removes HUD',
  'compilation cuts destroy timing',
  'replay speed unknown',
  'commentary claims not visible',
  'low resolution',
  'compression artifacts',
  'ambiguous character/move',
  'mixed source/context',
  'unknown/mixed source format'
)) {
  Assert-Contains $raw $gapCategory 'gap/failure category' ([ref]$issues)
}

foreach ($followUp in @('taxonomy update candidate', 'fixture candidate', 'validator candidate', 'policy candidate', 'later issue candidate', 'unsupported/hold', '#135', '#137', '#140', '#141')) {
  Assert-Contains $raw $followUp 'follow-up mapping text' ([ref]$issues)
}

Assert-NoRawTranscriptMarkers $raw ([ref]$issues)
Assert-NoLiveUrls $raw ([ref]$issues)
Assert-NoBinaryMediaPaths $raw ([ref]$issues)
Assert-NoActiveForbiddenStorage $raw ([ref]$issues)

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Video learning report template OK'
