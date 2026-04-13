#requires -Version 7.0

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [ValidateNotNullOrEmpty()]
  [string]$CaseId,

  [Parameter(Mandatory = $true)]
  [ValidateNotNullOrEmpty()]
  [string]$InputVideoPath,

  [string]$TranscriptPath,

  [string]$OutputDir,

  [string]$AnalysisJsonPath,

  [switch]$WhatIf
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$caseRoot = Join-Path $repoRoot 'maintainer-skills\smoke-video-analysis\references\smoke-cases'
$schemaPath = Join-Path $repoRoot 'skills\video-analysis-core\assets\video-analysis-v0.schema.json'
$contractPath = Join-Path $repoRoot 'skills\video-analysis-core\references\output-contract.md'
$skillPath = Join-Path $repoRoot 'skills\video-analysis-core\SKILL.md'

function Resolve-ExistingPath {
  param(
    [Parameter(Mandatory = $true)]
    [string]$PathValue,

    [Parameter(Mandatory = $true)]
    [string]$Label
  )

  if (-not (Test-Path -LiteralPath $PathValue)) {
    throw "$Label not found: $PathValue"
  }

  return (Resolve-Path -LiteralPath $PathValue).Path
}

function Get-CasePath {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SelectedCaseId
  )

  $candidate = Join-Path $caseRoot "$SelectedCaseId.json"
  if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
    $available = @(
      Get-ChildItem -LiteralPath $caseRoot -Filter '*.json' |
        Sort-Object BaseName |
        ForEach-Object { $_.BaseName }
    )
    throw "Unknown CaseId '$SelectedCaseId'. Available cases: $($available -join ', ')"
  }

  return $candidate
}

function New-InputPresenceMap {
  param(
    [string]$ResolvedTranscriptPath
  )

  return @{
    video = $true
    transcript = [bool]$ResolvedTranscriptPath
  }
}

function Assert-InputsMatchManifest {
  param(
    [Parameter(Mandatory = $true)]
    [pscustomobject]$Manifest,

    [Parameter(Mandatory = $true)]
    [hashtable]$InputPresence
  )

  foreach ($requiredInput in @($Manifest.required_inputs)) {
    if (-not $InputPresence.ContainsKey($requiredInput)) {
      throw "Unsupported required input '$requiredInput' in case manifest '$($Manifest.case_id)'"
    }

    if (-not $InputPresence[$requiredInput]) {
      throw "Case '$($Manifest.case_id)' requires input '$requiredInput'"
    }
  }
}

function Find-ObjectPropertyPaths {
  param(
    [Parameter()]
    [AllowNull()]
    $Value,

    [Parameter(Mandatory = $true)]
    [string[]]$NamePatterns,

    [string]$CurrentPath = '$'
  )

  $matches = New-Object System.Collections.Generic.List[string]

  if ($null -eq $Value) {
    return $matches
  }

  if ($Value -is [System.Collections.IDictionary]) {
    foreach ($entry in $Value.GetEnumerator()) {
      $entryName = [string]$entry.Key
      $entryPath = "$CurrentPath.$entryName"
      foreach ($pattern in $NamePatterns) {
        if ($entryName -match $pattern) {
          $matches.Add($entryPath)
          break
        }
      }
      foreach ($nested in Find-ObjectPropertyPaths -Value $entry.Value -NamePatterns $NamePatterns -CurrentPath $entryPath) {
        $matches.Add($nested)
      }
    }
    return $matches
  }

  if ($Value -is [System.Management.Automation.PSCustomObject]) {
    foreach ($property in $Value.PSObject.Properties) {
      $entryName = [string]$property.Name
      $entryPath = "$CurrentPath.$entryName"
      foreach ($pattern in $NamePatterns) {
        if ($entryName -match $pattern) {
          $matches.Add($entryPath)
          break
        }
      }
      foreach ($nested in Find-ObjectPropertyPaths -Value $property.Value -NamePatterns $NamePatterns -CurrentPath $entryPath) {
        $matches.Add($nested)
      }
    }
    return $matches
  }

  if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
    $index = 0
    foreach ($item in $Value) {
      foreach ($nested in Find-ObjectPropertyPaths -Value $item -NamePatterns $NamePatterns -CurrentPath "$CurrentPath[$index]") {
        $matches.Add($nested)
      }
      $index += 1
    }
  }

  return $matches
}

function Test-UniqueValues {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Values
  )

  return (@($Values | Group-Object | Where-Object Count -gt 1).Count -eq 0)
}

function Test-SegmentIntervals {
  param(
    [Parameter(Mandatory = $true)]
    [pscustomobject]$Payload
  )

  $problems = New-Object System.Collections.Generic.List[string]
  $totalFrames = [int]$Payload.clip_metadata.total_frames

  foreach ($segment in @($Payload.segments)) {
    if ([int]$segment.start_frame -ge [int]$segment.end_frame) {
      $problems.Add("segment:$($segment.segment_id) has non-positive interval [$($segment.start_frame), $($segment.end_frame))")
    }

    if ([int]$segment.end_frame -gt $totalFrames) {
      $problems.Add("segment:$($segment.segment_id) exceeds clip total_frames $totalFrames")
    }

    foreach ($evidence in @($segment.evidence_refs)) {
      if ([int]$evidence.frame_range.start_frame -ge [int]$evidence.frame_range.end_frame) {
        $problems.Add("evidence:$($evidence.evidence_id) has non-positive interval [$($evidence.frame_range.start_frame), $($evidence.frame_range.end_frame))")
      }

      if ([int]$evidence.frame_range.end_frame -gt $totalFrames) {
        $problems.Add("evidence:$($evidence.evidence_id) exceeds clip total_frames $totalFrames")
      }
    }
  }

  return $problems
}

function Test-ManifestInvariant {
  param(
    [Parameter(Mandatory = $true)]
    [pscustomobject]$Invariant,

    [Parameter(Mandatory = $true)]
    [pscustomobject]$Payload,

    [Parameter(Mandatory = $true)]
    [bool]$SchemaValid,

    [Parameter(Mandatory = $true)]
    [hashtable]$InputPresence
  )

  $result = [ordered]@{
    id = $Invariant.id
    description = $Invariant.description
    status = 'pass'
    details = ''
  }

  if ($Invariant.PSObject.Properties.Name -contains 'when_input') {
    $requiredInput = [string]$Invariant.when_input
    if (-not $InputPresence.ContainsKey($requiredInput)) {
      throw "Unsupported when_input '$requiredInput' in invariant '$($Invariant.id)'"
    }

    if (-not $InputPresence[$requiredInput]) {
      $result.status = 'skipped'
      $result.details = "Skipped because input '$requiredInput' was not supplied."
      return [pscustomobject]$result
    }
  }

  switch ([string]$Invariant.type) {
    'schema_valid' {
      if (-not $SchemaValid) {
        $result.status = 'fail'
        $result.details = 'Canonical schema validation failed.'
      }
    }
    'segments_non_empty' {
      $segmentCount = @($Payload.segments).Count
      if ($segmentCount -lt 1) {
        $result.status = 'fail'
        $result.details = 'segments is empty.'
      } else {
        $result.details = "segments count: $segmentCount"
      }
    }
    'track_present' {
      $track = [string]$Invariant.track
      $minimumCount = if ($Invariant.PSObject.Properties.Name -contains 'minimum_count') { [int]$Invariant.minimum_count } else { 1 }
      $count = @($Payload.segments | Where-Object { $_.track -eq $track }).Count
      if ($count -lt $minimumCount) {
        $result.status = 'fail'
        $result.details = "track '$track' count $count is below minimum $minimumCount."
      } else {
        $result.details = "track '$track' count: $count"
      }
    }
    'segment_intervals_valid' {
      $problems = @(Test-SegmentIntervals -Payload $Payload)
      if ($problems.Count -gt 0) {
        $result.status = 'fail'
        $result.details = $problems -join '; '
      }
    }
    'unique_ids' {
      $segmentIds = @($Payload.segments | ForEach-Object { [string]$_.segment_id })
      $evidenceIds = @($Payload.segments | ForEach-Object { @($_.evidence_refs | ForEach-Object { [string]$_.evidence_id }) })
      $eventIds = @($Payload.derived_events | ForEach-Object { [string]$_.event_id })

      $duplicates = New-Object System.Collections.Generic.List[string]
      if (-not (Test-UniqueValues -Values $segmentIds)) {
        $duplicates.Add('segment_id')
      }
      if (-not (Test-UniqueValues -Values $evidenceIds)) {
        $duplicates.Add('evidence_id')
      }
      if ($eventIds.Count -gt 0 -and -not (Test-UniqueValues -Values $eventIds)) {
        $duplicates.Add('event_id')
      }

      if ($duplicates.Count -gt 0) {
        $result.status = 'fail'
        $result.details = "Duplicate identifiers found for: $($duplicates -join ', ')"
      }
    }
    'derived_events_have_source_segment_ids' {
      $missing = @(
        $Payload.derived_events |
          Where-Object { @($_.source_segment_ids).Count -lt 1 } |
          ForEach-Object { [string]$_.event_id }
      )

      if ($missing.Count -gt 0) {
        $result.status = 'fail'
        $result.details = "Derived events missing source_segment_ids: $($missing -join ', ')"
      } else {
        $result.details = "derived_events count: $(@($Payload.derived_events).Count)"
      }
    }
    'no_saved_artifact_paths' {
      $matches = @(
        Find-ObjectPropertyPaths -Value $Payload -NamePatterns @(
          '(^|_)artifact_path(s)?$',
          '(^|_)frame_path(s)?$',
          '(^|_)crop_path(s)?$',
          '(^|_)output_path(s)?$'
        )
      )

      if ($matches.Count -gt 0) {
        $result.status = 'fail'
        $result.details = "Artifact-path-like fields found at: $($matches -join ', ')"
      }
    }
    default {
      throw "Unsupported invariant type '$($Invariant.type)' in case '$($Invariant.id)'"
    }
  }

  return [pscustomobject]$result
}

$casePath = Get-CasePath -SelectedCaseId $CaseId
$manifest = Get-Content -LiteralPath $casePath -Raw -Encoding UTF8 | ConvertFrom-Json

if ($manifest.case_id -ne $CaseId) {
  throw "Case manifest mismatch. Requested '$CaseId' but manifest contains '$($manifest.case_id)'"
}

$resolvedVideoPath = Resolve-ExistingPath -PathValue $InputVideoPath -Label 'InputVideoPath'
$resolvedTranscriptPath = if ($TranscriptPath) {
  Resolve-ExistingPath -PathValue $TranscriptPath -Label 'TranscriptPath'
} else {
  $null
}

$inputPresence = New-InputPresenceMap -ResolvedTranscriptPath $resolvedTranscriptPath
Assert-InputsMatchManifest -Manifest $manifest -InputPresence $inputPresence

$resolvedOutputDir = if ($OutputDir) {
  [System.IO.Path]::GetFullPath($OutputDir)
} else {
  Join-Path $repoRoot ("local\smoke-out\video-analysis\{0}\{1}" -f $CaseId, (Get-Date -Format 'yyyyMMdd-HHmmss'))
}

$resolvedAnalysisJsonPath = if ($AnalysisJsonPath) {
  [System.IO.Path]::GetFullPath($AnalysisJsonPath)
} else {
  Join-Path $resolvedOutputDir 'analysis-output.json'
}

$requestPath = Join-Path $resolvedOutputDir 'smoke-request.md'
$contextPath = Join-Path $resolvedOutputDir 'smoke-context.json'
$summaryPath = Join-Path $resolvedOutputDir 'smoke-summary.json'
$transcriptDisplay = if ($resolvedTranscriptPath) { $resolvedTranscriptPath } else { '(not provided)' }

$requestLines = @(
  "# Video Analysis Smoke Request: $($manifest.case_id)",
  '',
  'This is a maintainer-only smoke run for `skills/video-analysis-core/`.',
  'Produce canonical JSON only. Do not extend the public contract for smoke convenience.',
  '',
  '## Inputs',
  ('- video: `{0}`' -f $resolvedVideoPath),
  ('- transcript: `{0}`' -f $transcriptDisplay),
  '',
  '## Canonical References',
  ('- skill: `{0}`' -f $skillPath),
  ('- output contract: `{0}`' -f $contractPath),
  ('- schema: `{0}`' -f $schemaPath),
  '',
  '## Expected Output',
  ('- Save canonical JSON to `{0}`' -f $resolvedAnalysisJsonPath),
  '- Keep `segments` as the truth surface.',
  '- Do not require saved artifact paths in canonical output.',
  '',
  '## Case Summary',
  "- description: $($manifest.description)",
  "- expected use case: $($manifest.expected_use_case)",
  '',
  '## Expected Invariants'
)

foreach ($invariant in @($manifest.expected_invariants)) {
  $requestLines += "- [$($invariant.id)] $($invariant.description)"
}

$requestLines += ''
$requestLines += '## Notes'
foreach ($note in @($manifest.notes)) {
  $requestLines += "- $note"
}

$contextPayload = [ordered]@{
  case_id = $manifest.case_id
  case_manifest_path = $casePath
  schema_path = $schemaPath
  output_contract_path = $contractPath
  skill_path = $skillPath
  input_video_path = $resolvedVideoPath
  transcript_path = $resolvedTranscriptPath
  output_dir = $resolvedOutputDir
  analysis_json_path = $resolvedAnalysisJsonPath
  required_inputs = @($manifest.required_inputs)
  optional_inputs = @($manifest.optional_inputs)
  expected_invariants = @($manifest.expected_invariants)
  notes = @($manifest.notes)
}

if ($WhatIf) {
  Write-Host "Smoke dry-run for case '$CaseId'"
  Write-Host "Video: $resolvedVideoPath"
  Write-Host "Transcript: $transcriptDisplay"
  Write-Host "OutputDir: $resolvedOutputDir"
  Write-Host "AnalysisJsonPath: $resolvedAnalysisJsonPath"
  Write-Host "Manifest: $casePath"
  Write-Host 'Expected invariants:'
  foreach ($invariant in @($manifest.expected_invariants)) {
    Write-Host "- $($invariant.id): $($invariant.description)"
  }
  return
}

New-Item -ItemType Directory -Force -Path $resolvedOutputDir | Out-Null
$requestLines -join [Environment]::NewLine | Set-Content -LiteralPath $requestPath -Encoding UTF8
$contextPayload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $contextPath -Encoding UTF8

if (-not (Test-Path -LiteralPath $resolvedAnalysisJsonPath -PathType Leaf)) {
  Write-Host "Prepared smoke packet for case '$CaseId'."
  Write-Host "Request: $requestPath"
  Write-Host "Context: $contextPath"
  Write-Host "Save canonical JSON to: $resolvedAnalysisJsonPath"
  Write-Host 'No analysis JSON found yet, so schema/invariant validation was skipped.'
  return
}

$analysisJsonText = Get-Content -LiteralPath $resolvedAnalysisJsonPath -Raw -Encoding UTF8
$schemaWarnings = $null
$schemaError = $null
$jsonParseError = $null
$payload = $null

try {
  $schemaValid = Test-Json -Json $analysisJsonText -SchemaFile $schemaPath -WarningVariable schemaWarnings -ErrorAction Stop
} catch {
  $schemaValid = $false
  $schemaError = $_.Exception.Message
}

try {
  $payload = $analysisJsonText | ConvertFrom-Json -Depth 100
} catch {
  $jsonParseError = $_.Exception.Message
}

$invariantResults = @()
if ($null -eq $payload) {
  foreach ($invariant in @($manifest.expected_invariants)) {
    $status = if ($invariant.type -eq 'schema_valid') { 'fail' } else { 'skipped' }
    $details = if ($invariant.type -eq 'schema_valid') {
      if ($schemaError) { $schemaError } else { $jsonParseError }
    } else {
      'Skipped because analysis JSON could not be parsed.'
    }

    $invariantResults += [pscustomobject][ordered]@{
      id = $invariant.id
      description = $invariant.description
      status = $status
      details = $details
    }
  }
} else {
  $invariantResults = @(
    foreach ($invariant in @($manifest.expected_invariants)) {
      Test-ManifestInvariant -Invariant $invariant -Payload $payload -SchemaValid:$schemaValid -InputPresence $inputPresence
    }
  )
}

$failedInvariants = @($invariantResults | Where-Object { $_.status -eq 'fail' })
$overallStatus = if ($schemaValid -and $failedInvariants.Count -eq 0) { 'passed' } else { 'failed' }

$summaryPayload = [ordered]@{
  case_id = $manifest.case_id
  output_dir = $resolvedOutputDir
  analysis_json_path = $resolvedAnalysisJsonPath
  schema_path = $schemaPath
  status = $overallStatus
  schema = [ordered]@{
    valid = $schemaValid
    error = $schemaError
    json_parse_error = $jsonParseError
    warnings = @($schemaWarnings)
  }
  invariant_results = $invariantResults
}

$summaryPayload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $summaryPath -Encoding UTF8

Write-Host "Smoke validation status: $overallStatus"
Write-Host "Summary: $summaryPath"

if (-not $schemaValid) {
  Write-Host "Schema validation failed: $schemaError"
  if (@($schemaWarnings).Count -gt 0) {
    Write-Host "Schema warnings: $(@($schemaWarnings) -join '; ')"
  }
}

foreach ($result in $invariantResults) {
  Write-Host "[$($result.status)] $($result.id): $($result.description)"
  if ($result.details) {
    Write-Host "  $($result.details)"
  }
}

if ($overallStatus -ne 'passed') {
  throw "Video-analysis smoke validation failed for case '$CaseId'"
}
