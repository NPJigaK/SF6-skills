Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$required = @(
  '.codex/INSTALL.md',
  '.opencode/INSTALL.md',
  '.claude-plugin/marketplace.json',
  '.claude-plugin/INSTALL.md',
  '.cursor-plugin/README.md',
  '.cursor-plugin/INSTALL.md',
  'docs/distribution/README.md',
  'docs/distribution/codex.md',
  'docs/distribution/opencode.md',
  'docs/distribution/claude.md',
  'docs/distribution/cursor.md',
  'docs/distribution/release-bundle.md',
  'packages/skill-installers/README.md',
  'packages/skill-installers/install-sf6-skills.ps1',
  'packages/skill-packaging/build-release-bundle.ps1'
)

$missing = @()
foreach ($path in $required) {
  $fullPath = Join-Path $repoRoot $path
  if (-not (Test-Path -LiteralPath $fullPath)) {
    $missing += $path
  }
}
if ($missing.Count -gt 0) {
  throw "Missing distribution files: $($missing -join ', ')"
}

$installDocs = @(
  '.codex/INSTALL.md',
  '.opencode/INSTALL.md',
  '.claude-plugin/INSTALL.md',
  '.cursor-plugin/INSTALL.md'
)

foreach ($path in $installDocs) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $path) -Raw
  if ($content -notmatch [regex]::Escape('install-sf6-skills.ps1')) {
    throw "$path missing installer reference"
  }
  if ($content -notmatch [regex]::Escape('sf6-skills-bundle.zip')) {
    throw "$path missing bundle reference"
  }
}

$codex = Get-Content -LiteralPath (Join-Path $repoRoot '.codex/INSTALL.md') -Raw
if ($codex -notmatch [regex]::Escape('private source checkout')) {
  throw '.codex/INSTALL.md missing private source checkout wording'
}
if ($codex -notmatch [regex]::Escape('links the Codex discovery target to that source')) {
  throw '.codex/INSTALL.md missing source-plus-link wording'
}
if ($codex -match [regex]::Escape('git clone')) {
  throw '.codex/INSTALL.md still contains git clone'
}

$opencode = Get-Content -LiteralPath (Join-Path $repoRoot '.opencode/INSTALL.md') -Raw
if ($opencode -match [regex]::Escape('@git+https://github.com/NPJigaK/SF6-skills.git')) {
  throw '.opencode/INSTALL.md still contains legacy git URL install flow'
}

$marketplace = Get-Content -LiteralPath (Join-Path $repoRoot '.claude-plugin/marketplace.json') -Raw | ConvertFrom-Json
if ($marketplace.plugins[0].name -ne 'sf6-skills') {
  throw 'Unexpected Claude plugin name'
}

Write-Host 'Distribution surface OK'
