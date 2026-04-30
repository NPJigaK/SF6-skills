Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$docPath = Join-Path $repoRoot 'docs\architecture\kb-sf6-frame-current-packaging.md'

if (-not (Test-Path -LiteralPath $docPath)) {
  throw "Missing boundary doc: $docPath"
}

$content = (Get-Content -LiteralPath $docPath -Raw).Replace("`r`n", "`n").Replace("`r", "`n")
$expected = @(
  '# kb-sf6-frame-current Packaging Boundary'
  ''
  '## Runtime Asset Layout'
  ''
  '- `skills/kb-sf6-frame-current/assets/runtime_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/snapshot_manifest.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/official_raw.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/derived_metrics.json`'
  '- `skills/kb-sf6-frame-current/assets/published/<character_slug>/supercombo_enrichment.json`'
  ''
  '## Canonical Roster'
  ''
  '- `shared/roster/current-character-roster.json`'
  '- `skills/kb-sf6-frame-current/assets/runtime_manifest.json` records the packaged character inventory derived from that roster source'
  ''
  '## Source Mapping'
  ''
  '- generated only from `data/exports/<character_slug>/...`'
  '- character inventory derived from `shared/roster/current-character-roster.json`'
  '- never from `data/raw/...` or `data/normalized/...`'
  '- exclude `*.csv` and `*_manual_review.*`'
  ''
  '## Regeneration'
  ''
  '- `powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1`'
  '- rerun after published exports change for any character listed in `shared/roster/current-character-roster.json`'
  ''
  '## Publication Rules'
  ''
  '- package every character listed in `shared/roster/current-character-roster.json`'
  '- `runtime_manifest.json` is the packaged character inventory'
  '- copy dataset files only when `publication_state = available`'
  '- `official_raw` remains the source of truth'
  '- `derived_metrics` remains official-only machine derivation'
  '- `supercombo_enrichment` remains supplemental and must never override official'
) -join "`n"

if ($content -ne $expected -and $content -ne ($expected + "`n")) {
  throw @"
Boundary doc does not match the resolved contract exactly.
Expected exact content:
$expected
"@
}

Write-Host 'Frame-current boundary doc OK'
