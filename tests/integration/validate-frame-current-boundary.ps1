Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$docPath = Join-Path $repoRoot 'docs\architecture\kb-sf6-frame-current-packaging.md'

if (-not (Test-Path -LiteralPath $docPath)) {
  throw "Missing boundary doc: $docPath"
}

$content = (Get-Content -LiteralPath $docPath -Raw).Replace("`r`n", "`n").Replace("`r", "`n")
$requiredHeadings = @(
  '## Runtime Asset Layout'
  '## Source Mapping'
  '## Regeneration'
  '## Publication Rules'
)

foreach ($heading in $requiredHeadings) {
  $pattern = '(?m)^' + [regex]::Escape($heading) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required heading: $heading"
  }
}

$requiredLines = @(
  '- `skills/kb-sf6-frame-current/assets/runtime_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/snapshot_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/official_raw.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/derived_metrics.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/supercombo_enrichment.json`'
  '- generated only from `data/exports/<character_slug>/...`'
  '- never from `data/raw/...` or `data/normalized/...`'
  '- exclude `*.csv` and `*_manual_review.*`'
  '- `powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1`'
  '- rerun after published exports change for `jp` or `luke`'
  '- only supported characters `jp`, `luke`'
  '- copy dataset files only when `publication_state = available`'
  '- `official_raw` remains the source of truth'
  '- `derived_metrics` remains official-only machine derivation'
  '- `supercombo_enrichment` remains supplemental and must never override official'
)

foreach ($line in $requiredLines) {
  $pattern = '(?m)^' + [regex]::Escape($line) + '$'
  if ($content -notmatch $pattern) {
    throw "Missing required contract line: $line"
  }
}

Write-Host 'Frame-current boundary doc OK'
