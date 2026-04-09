Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$docPath = Join-Path $repoRoot 'docs\architecture\kb-sf6-frame-current-packaging.md'

if (-not (Test-Path -LiteralPath $docPath)) {
  throw "Missing boundary doc: $docPath"
}

$content = Get-Content -LiteralPath $docPath -Raw
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

Write-Host 'Frame-current boundary doc OK'
