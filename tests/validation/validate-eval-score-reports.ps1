Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'eval-case-helpers.ps1')

$schemaRelativePath = 'contracts/eval-score-report.schema.json'
$fixtureRootRelativePath = 'tests/fixtures/eval-score-reports'
$fixtureRoot = Join-Path $repoRoot $fixtureRootRelativePath
$forbiddenReportPatterns = @(
  '"raw_transcript"\s*:',
  '"raw_response"\s*:',
  '"full_response"\s*:',
  '"session_id"\s*:',
  '"hermes_memory"\s*:',
  '\.hermes/',
  '\.env',
  'auth\.json',
  'state\.db',
  'data/exports/',
  'official_raw',
  'runtime/frame-current',
  'runtime/generated-knowledge',
  'runtime/normalization'
)

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Add-Issue {
  param(
    [Parameter(Mandatory = $true)][ref]$Issues,
    [Parameter(Mandatory = $true)][string]$Message
  )
  $Issues.Value += $Message
}

function Assert-SummaryCount {
  param(
    [Parameter(Mandatory = $true)][object]$Summary,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][int]$Expected,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Summary $Name)) {
    Add-Issue $Issues "$Context summary missing count: $Name"
    return
  }
  if ([int]$Summary.$Name -ne $Expected) {
    Add-Issue $Issues "$Context summary $Name must be $Expected, got $($Summary.$Name)"
  }
}

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $schemaRelativePath) -PathType Leaf)) {
  throw "Missing eval score report schema: $schemaRelativePath"
}
if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  throw "Missing eval score report fixture directory: $fixtureRootRelativePath"
}

$schemaText = Get-Content -LiteralPath (Join-Path $repoRoot $schemaRelativePath) -Raw -Encoding UTF8
$issues = @()
$caseIndex = Get-EvalCaseIndex -RepoRoot $repoRoot -Issues ([ref]$issues)

$reportFiles = @(
  Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.json' |
    Sort-Object FullName
)
if ($reportFiles.Count -eq 0) {
  $issues += "No eval score report fixtures found under $fixtureRootRelativePath"
}

foreach ($reportFile in $reportFiles) {
  $relativePath = $reportFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $raw = Get-Content -LiteralPath $reportFile.FullName -Raw -Encoding UTF8
  try {
    $valid = Test-Json -LiteralPath $reportFile.FullName -Schema $schemaText -ErrorAction Stop
    if ($valid -ne $true) {
      $issues += "$relativePath failed schema validation against $schemaRelativePath"
    }
  } catch {
    $issues += "$relativePath failed schema validation against $schemaRelativePath`: $($_.Exception.Message)"
    continue
  }

  foreach ($pattern in $forbiddenReportPatterns) {
    if ($raw -match $pattern) {
      $issues += "$relativePath contains forbidden score-report content pattern: $pattern"
    }
  }

  $report = $raw | ConvertFrom-Json
  if ($report.not_gameplay_authority -ne $true) {
    $issues += "$relativePath must declare not_gameplay_authority true"
  }
  if ($report.normal_public_answer_authority -ne $false) {
    $issues += "$relativePath must not be normal public answer authority"
  }
  if ($report.raw_transcript_committed -ne $false) {
    $issues += "$relativePath must not commit raw transcripts"
  }
  if ($report.local_state_committed -ne $false) {
    $issues += "$relativePath must not commit local state"
  }

  $caseResults = @($report.case_results)
  foreach ($result in $caseResults) {
    $caseId = [string]$result.case_id
    $context = "$relativePath case_results[$caseId]"
    if (-not $caseIndex.ContainsKey($caseId)) {
      $issues += "$context references unknown eval case"
      continue
    }

    $canonicalCase = $caseIndex[$caseId]
    if ([string]$result.source_file -ne [string]$canonicalCase.source_file) {
      $issues += "$context source_file must be $($canonicalCase.source_file)"
    }
    if ([string]$result.expected_answer_mode -ne [string]$canonicalCase.expected_answer_mode) {
      $issues += "$context expected_answer_mode must be $($canonicalCase.expected_answer_mode)"
    }
  }

  $resultValues = @($caseResults | ForEach-Object { [string]$_.overall_result })
  $modePassValues = @($caseResults | Where-Object { $_.mode_pass -eq $true })
  $groundingPassValues = @($caseResults | Where-Object { $_.grounding_pass -eq $true })
  $mustNotIncludePassValues = @($caseResults | Where-Object { $_.must_not_include_pass -eq $true })

  Assert-SummaryCount $report.summary 'total_cases' $caseResults.Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'pass_count' @($resultValues | Where-Object { $_ -eq 'pass' }).Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'fail_count' @($resultValues | Where-Object { $_ -eq 'fail' }).Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'skip_count' @($resultValues | Where-Object { $_ -eq 'skip' }).Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'hold_review_count' @($resultValues | Where-Object { $_ -eq 'hold_review' }).Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'mode_pass_count' $modePassValues.Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'grounding_pass_count' $groundingPassValues.Count $relativePath ([ref]$issues)
  Assert-SummaryCount $report.summary 'must_not_include_pass_count' $mustNotIncludePassValues.Count $relativePath ([ref]$issues)
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Eval score reports OK'
