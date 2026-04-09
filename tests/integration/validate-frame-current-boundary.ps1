Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$docPath = Join-Path $repoRoot 'docs\architecture\kb-sf6-frame-current-packaging.md'

if (-not (Test-Path -LiteralPath $docPath)) {
  throw "Missing boundary doc: $docPath"
}

$content = (Get-Content -LiteralPath $docPath -Raw).Replace("`r`n", "`n").Replace("`r", "`n")
$requiredHeadings = @(
  '## Current Runtime Inputs'
  '## Packaging Options'
  '## Recommended Decision'
  '## Next Plan Trigger'
)

foreach ($heading in $requiredHeadings) {
  $pattern = '(?m)^' + [regex]::Escape($heading) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required heading: $heading"
  }
}

$requiredLines = @(
  '- `snapshot_manifest.json`'
  '- published `official_raw.*`'
  '- published `derived_metrics.*`'
  '- published `supercombo_enrichment.*`'
  '- supported characters: `jp`, `luke`'
  '1. Bundle skill-local published snapshots under `skills/kb-sf6-frame-current/assets/`'
  '2. Generate a reduced runtime asset set during packaging'
  '3. Keep the skill repo-local only until asset packaging is solved'
  'For phase 1, do not migrate this skill into the public surface until a generated runtime asset subset is defined.'
  'The follow-up plan should compare bundled full exports versus generated reduced assets and choose one explicit packaging contract.'
  '- which files ship with the skill'
  '- how those files are regenerated'
  '- how published exports remain the final source of truth'
)

foreach ($line in $requiredLines) {
  $pattern = '(?m)^' + [regex]::Escape($line) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required contract line: $line"
  }
}

Write-Host 'Frame-current boundary doc OK'
