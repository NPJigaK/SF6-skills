Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$questionFiles = @(
  'evals/questions/concepts.yaml',
  'evals/questions/current-fact.yaml',
  'evals/questions/strategy.yaml',
  'evals/questions/matchup.yaml',
  'evals/questions/video-observation.yaml',
  'evals/questions/uncertainty.yaml'
)

$rubricFiles = @(
  'evals/rubrics/answer-modes.md',
  'evals/rubrics/grounding.md'
)

foreach ($relativePath in $questionFiles + $rubricFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    throw "Missing eval file: $relativePath"
  }
}

$allowedTopLevelKeys = @('cases')
$allowedCaseKeys = @(
  'id',
  'question',
  'expected_answer_mode',
  'evidence_boundary',
  'must_not_include'
)

foreach ($relativePath in $questionFiles) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $relativePath) -Raw -Encoding UTF8
  $normalized = $content -replace "`r`n", "`n"
  $violations = @()

  foreach ($line in ($normalized -split "`n")) {
    if ($line -match '^([A-Za-z0-9_]+):') {
      $key = $Matches[1]
      if ($key -notin $allowedTopLevelKeys) {
        $violations += "$relativePath has unsupported top-level eval key: $key"
      }
    } elseif ($line -match '^ {4}([A-Za-z0-9_]+):') {
      $key = $Matches[1]
      if ($key -notin $allowedCaseKeys) {
        $violations += "$relativePath has unsupported eval case key: $key"
      }
    }
  }

  foreach ($needle in @('id:', 'question:', 'expected_answer_mode:', 'evidence_boundary:', 'must_not_include:')) {
    if ($content -notmatch [regex]::Escape($needle)) {
      $violations += "$relativePath missing eval metadata: $needle"
    }
  }
  $modeMatches = [regex]::Matches($content, 'expected_answer_mode:\s*([A-Za-z0-9_/-]+)')
  foreach ($modeMatch in $modeMatches) {
    $mode = $modeMatch.Groups[1].Value
    if ($mode -notin @('stable_concept', 'verified_current_fact', 'strategy_or_matchup_knowledge', 'observation', 'unresolved_or_hold')) {
      $violations += "$relativePath has unsupported expected_answer_mode: $mode"
    }
  }

  if ($violations.Count -gt 0) {
    throw ($violations -join '; ')
  }
}

$answerModes = Get-Content -LiteralPath (Join-Path $repoRoot 'evals/rubrics/answer-modes.md') -Raw -Encoding UTF8
foreach ($mode in @('stable_concept', 'verified_current_fact', 'strategy_or_matchup_knowledge', 'observation', 'unresolved_or_hold')) {
  if ($answerModes -notmatch [regex]::Escape($mode)) {
    throw "answer mode rubric missing mode: $mode"
  }
}

Write-Host 'Evals OK'
