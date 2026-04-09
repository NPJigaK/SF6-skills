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

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing distribution files: $($missing -join ', ')"
}

$marketplace = Get-Content '.claude-plugin/marketplace.json' -Raw | ConvertFrom-Json
if ($marketplace.plugins[0].name -ne 'sf6-skills') {
  throw 'Unexpected Claude plugin name'
}

$codex = Get-Content '.codex/INSTALL.md' -Raw
if ($codex -notmatch 'NPJigaK/SF6-skills') {
  throw 'Codex install guide missing repository URL'
}

Write-Host 'Distribution surface OK'
