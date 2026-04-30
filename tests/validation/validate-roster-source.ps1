Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$rosterPath = Join-Path $repoRoot 'data/roster/current-character-roster.json'

if (-not (Test-Path -LiteralPath $rosterPath -PathType Leaf)) {
  throw 'Missing canonical roster source: data/roster/current-character-roster.json'
}

$roster = Get-Content -LiteralPath $rosterPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($null -eq $roster.verified_from) {
  throw 'Roster must include verified_from metadata'
}
if ($roster.verified_from.PSObject.Properties.Name -contains 'source_tier') {
  throw 'Roster metadata must not preserve source_tier'
}
foreach ($field in @('source_kind', 'source_role', 'evidence_basis')) {
  if ($roster.verified_from.PSObject.Properties.Name -notcontains $field) {
    throw "Roster verified_from missing generic metadata field: $field"
  }
  if ($null -eq $roster.verified_from.$field) {
    throw "Roster verified_from missing generic metadata field: $field"
  }
}

$sharedRosterPath = Join-Path $repoRoot 'shared/roster'
if (Test-Path -LiteralPath $sharedRosterPath) {
  throw 'shared/roster must not remain in the v2 tree'
}

$references = @()
$scanRoots = @('AGENTS.md', 'README.md', 'contracts', 'data', 'docs', 'evals', 'ingest', 'knowledge', 'packages', 'packs', 'skills', 'tests', 'workflows')
foreach ($scanRoot in $scanRoots) {
  $path = Join-Path $repoRoot $scanRoot
  if (-not (Test-Path -LiteralPath $path)) {
    continue
  }

  $items = if (Test-Path -LiteralPath $path -PathType Leaf) {
    @(Get-Item -LiteralPath $path)
  }
  else {
    @(Get-ChildItem -LiteralPath $path -Recurse -File)
  }

  foreach ($item in $items) {
    $relativePath = $item.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    if ($relativePath -like 'tests/validation/*') {
      continue
    }
    $content = Get-Content -LiteralPath $item.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($content -match 'shared/roster') {
      $references += $relativePath
    }
  }
}
if (@($references).Count -gt 0) {
  throw "Found shared/roster references: $($references -join '; ')"
}

Write-Host 'Roster source OK'
