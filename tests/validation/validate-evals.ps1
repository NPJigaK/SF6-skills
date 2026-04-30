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

foreach ($relativePath in $questionFiles) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $relativePath) -Raw -Encoding UTF8
  foreach ($needle in @('id:', 'question:', 'expected_answer_mode:', 'evidence_boundary:', 'must_not_include:')) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$relativePath missing eval metadata: $needle"
    }
  }
  $modeMatches = [regex]::Matches($content, 'expected_answer_mode:\s*([A-Za-z0-9_/-]+)')
  foreach ($modeMatch in $modeMatches) {
    $mode = $modeMatch.Groups[1].Value
    if ($mode -notin @('stable_concept', 'verified_current_fact', 'strategy_or_matchup_knowledge', 'observation', 'unresolved_or_hold')) {
      throw "$relativePath has unsupported expected_answer_mode: $mode"
    }
  }
  if ($content -match '\[\u6982\u5ff5\u306e\u307f\]|\[\u691c\u8a3c\u6e08\u307f\]|\[\u4fdd\u7559\]') {
    throw "$relativePath must check answer modes, not legacy bracket labels"
  }
  if ($content -match '\bT[1-4]\b|source_tier|core / mixed / current-fact') {
    throw "$relativePath must not preserve legacy taxonomy in eval metadata"
  }
}

$answerModes = Get-Content -LiteralPath (Join-Path $repoRoot 'evals/rubrics/answer-modes.md') -Raw -Encoding UTF8
foreach ($mode in @('stable_concept', 'verified_current_fact', 'strategy_or_matchup_knowledge', 'observation', 'unresolved_or_hold')) {
  if ($answerModes -notmatch [regex]::Escape($mode)) {
    throw "answer mode rubric missing mode: $mode"
  }
}

Write-Host 'Evals OK'
