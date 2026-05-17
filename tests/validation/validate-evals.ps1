Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
. (Join-Path $PSScriptRoot 'eval-case-helpers.ps1')

$schemaRelativePath = 'contracts/eval-case.schema.json'
$rubricFiles = @(
  'evals/rubrics/answer-modes.md',
  'evals/rubrics/grounding.md'
)

foreach ($relativePath in @($schemaRelativePath) + $rubricFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    throw "Missing eval contract file: $relativePath"
  }
}

$schema = Get-Content -LiteralPath (Join-Path $repoRoot $schemaRelativePath) -Raw -Encoding UTF8 | ConvertFrom-Json
$requiredCaseKeys = @($schema.required | ForEach-Object { [string]$_ })
$allowedCaseKeys = @($schema.properties.PSObject.Properties.Name | ForEach-Object { [string]$_ })
$allowedAnswerModes = @($schema.properties.expected_answer_mode.enum | ForEach-Object { [string]$_ })

foreach ($requiredKey in @('id', 'question', 'expected_answer_mode', 'evidence_boundary', 'must_not_include')) {
  if ($requiredCaseKeys -notcontains $requiredKey) {
    throw "$schemaRelativePath missing required eval case key: $requiredKey"
  }
}

$issues = @()
$caseIndex = Get-EvalCaseIndex -RepoRoot $repoRoot -Issues ([ref]$issues)

foreach ($caseId in @($caseIndex.Keys | Sort-Object)) {
  $case = $caseIndex[$caseId]
  $context = "$($case.source_file)#$caseId"
  $caseKeys = @(
    $case.PSObject.Properties.Name |
      Where-Object { $_ -ne 'source_file' } |
      ForEach-Object { [string]$_ }
  )

  foreach ($key in $caseKeys) {
    if ($allowedCaseKeys -notcontains $key) {
      $issues += "$context has unsupported eval case key: $key"
    }
  }

  foreach ($key in $requiredCaseKeys) {
    if ($caseKeys -notcontains $key) {
      $issues += "$context missing eval case key: $key"
    }
  }

  foreach ($key in @('id', 'question', 'expected_answer_mode', 'evidence_boundary')) {
    if (($caseKeys -contains $key) -and [string]::IsNullOrWhiteSpace([string]$case.$key)) {
      $issues += "$context has empty eval case key: $key"
    }
  }

  if (($caseKeys -contains 'expected_answer_mode') -and $allowedAnswerModes -notcontains [string]$case.expected_answer_mode) {
    $issues += "$context has unsupported expected_answer_mode: $($case.expected_answer_mode)"
  }

  $mustNotInclude = if ($caseKeys -contains 'must_not_include') { @(ConvertTo-StringArray $case.must_not_include) } else { @() }
  if ($mustNotInclude.Count -eq 0) {
    $issues += "$context must include at least one must_not_include entry"
  }
}

$answerModes = Get-Content -LiteralPath (Join-Path $repoRoot 'evals/rubrics/answer-modes.md') -Raw -Encoding UTF8
foreach ($mode in $allowedAnswerModes) {
  if ($answerModes -notmatch [regex]::Escape($mode)) {
    $issues += "answer mode rubric missing mode: $mode"
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Evals OK'
