Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$generatedRoot = Join-Path $repoRoot 'skills/sf6-agent/references'

$generatedFiles = @(
  'generated-knowledge-index.md',
  'generated-concepts.md'
)

foreach ($name in $generatedFiles) {
  $path = Join-Path $generatedRoot $name
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing generated knowledge file: skills/sf6-agent/references/$name"
  }

  $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  foreach ($needle in @(
    'GENERATED FILE - DO NOT EDIT',
    'generator: packages/knowledge-generation/build-sf6-agent-knowledge.ps1',
    'source_root: knowledge/curated'
  )) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$name missing generated marker: $needle"
    }
  }
}

Write-Host 'Generated knowledge OK'
