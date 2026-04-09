$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$required = @(
  '.codex/INSTALL.md',
  '.opencode/INSTALL.md',
  '.claude-plugin/marketplace.json',
  '.cursor-plugin/README.md',
  'docs/distribution/codex.md',
  'docs/distribution/claude.md',
  'docs/distribution/cursor.md',
  'docs/distribution/opencode.md',
  'packages/skill-installers/README.md'
)

$requiredPaths = $required | ForEach-Object { Join-Path $repoRoot $_ }
$missing = $requiredPaths | Where-Object { -not (Test-Path -LiteralPath $_) }
if ($missing.Count -gt 0) {
  throw "Missing distribution files: $($missing -join ', ')"
}

$marketplacePath = Join-Path $repoRoot '.claude-plugin/marketplace.json'
$marketplace = Get-Content -LiteralPath $marketplacePath -Raw | ConvertFrom-Json
if ($marketplace.plugins[0].name -ne 'sf6-skills') {
  throw 'Unexpected Claude plugin name'
}

$codexPath = Join-Path $repoRoot '.codex/INSTALL.md'
$codex = Get-Content -LiteralPath $codexPath -Raw
if ($codex -notmatch 'NPJigaK/SF6-skills') {
  throw 'Codex install guide missing repository URL'
}

Write-Host 'Distribution surface OK'
