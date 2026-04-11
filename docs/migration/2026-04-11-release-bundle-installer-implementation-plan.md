# Release Bundle Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a release-bundle installer flow that lets end users install the `sf6-skills` public library into `Codex`, `OpenCode`, `Claude`, and `Cursor` without cloning the whole source repo.

**Architecture:** Keep `skills/` as the single canonical public source, build a `.dist/sf6-skills-bundle.zip` artifact from it, and drive all supported agents through one shared PowerShell installer. Agent-specific `INSTALL.md` files remain the user-facing front doors, but they all route to the same bundle and installer contract.

**Tech Stack:** PowerShell, GitHub Releases URL conventions, ZIP packaging via .NET compression, existing repo validators

---

## Planned File Map

**Create:**

- `E:\github\SF6-skills\docs\distribution\release-bundle.md`
- `E:\github\SF6-skills\packages\skill-packaging\build-release-bundle.ps1`
- `E:\github\SF6-skills\packages\skill-installers\install-sf6-skills.ps1`
- `E:\github\SF6-skills\packages\skill-installers\resolve-install-target.ps1`
- `E:\github\SF6-skills\tests\packaging\validate-release-bundle.ps1`
- `E:\github\SF6-skills\tests\install\validate-installer-contract.ps1`
- `E:\github\SF6-skills\.claude-plugin\INSTALL.md`
- `E:\github\SF6-skills\.cursor-plugin\INSTALL.md`

**Modify:**

- `E:\github\SF6-skills\.gitignore`
- `E:\github\SF6-skills\packages\skill-packaging\README.md`
- `E:\github\SF6-skills\packages\skill-installers\README.md`
- `E:\github\SF6-skills\.codex\INSTALL.md`
- `E:\github\SF6-skills\.opencode\INSTALL.md`
- `E:\github\SF6-skills\.cursor-plugin\README.md`
- `E:\github\SF6-skills\docs\distribution\README.md`
- `E:\github\SF6-skills\docs\distribution\codex.md`
- `E:\github\SF6-skills\docs\distribution\opencode.md`
- `E:\github\SF6-skills\docs\distribution\claude.md`
- `E:\github\SF6-skills\docs\distribution\cursor.md`
- `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`

**Generated, not committed:**

- `E:\github\SF6-skills\.dist\sf6-skills-bundle.zip`
- `E:\github\SF6-skills\.dist\installer-fixtures\...`

## Task 1: Define The Release Bundle Contract

**Files:**

- Modify: `E:\github\SF6-skills\.gitignore`
- Create: `E:\github\SF6-skills\docs\distribution\release-bundle.md`
- Create: `E:\github\SF6-skills\tests\packaging\validate-release-bundle.ps1`

- [ ] **Step 1: Ignore local bundle output**

Append this line to `.gitignore`:

```gitignore
.dist/
```

- [ ] **Step 2: Write the release-bundle contract doc**

Create `docs/distribution/release-bundle.md` with:

```markdown
# Release Bundle

Phase 1 distributes the public skill library as a GitHub Release artifact named `sf6-skills-bundle.zip`.

## Build Command

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

## Output

- local build path: `.dist/sf6-skills-bundle.zip`
- release asset name: `sf6-skills-bundle.zip`

## Bundle Layout

```text
sf6-skills/
  skills/
    kb-sf6-core/
    kb-sf6-frame-current/
```

## Excluded Content

The release bundle must not include:

- `maintainer-skills/`
- `.agents/`
- `data/`
- `docs/`
- `ingest/`
- `packages/`
- `scripts/`
- `shared/`
- `tests/`
```

- [ ] **Step 3: Write the failing release-bundle validator**

Create `tests/packaging/validate-release-bundle.ps1` with:

```powershell
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$bundleDoc = Join-Path $repoRoot 'docs\distribution\release-bundle.md'
$buildScript = Join-Path $repoRoot 'packages\skill-packaging\build-release-bundle.ps1'
$bundlePath = Join-Path $repoRoot '.dist\sf6-skills-bundle.zip'

if (-not (Test-Path -LiteralPath $bundleDoc -PathType Leaf)) {
  throw "Missing release bundle doc: $bundleDoc"
}

if (-not (Test-Path -LiteralPath $buildScript -PathType Leaf)) {
  throw "Missing bundle build script: $buildScript"
}

if (-not (Test-Path -LiteralPath $bundlePath -PathType Leaf)) {
  throw "Missing release bundle: $bundlePath"
}

$zip = [System.IO.Compression.ZipFile]::OpenRead($bundlePath)
try {
  $entries = @(
    $zip.Entries |
      Where-Object { -not [string]::IsNullOrWhiteSpace($_.FullName) -and -not $_.FullName.EndsWith('/') } |
      ForEach-Object { $_.FullName.Replace('\', '/') }
  )
}
finally {
  $zip.Dispose()
}

$requiredEntries = @(
  'sf6-skills/skills/kb-sf6-core/SKILL.md'
  'sf6-skills/skills/kb-sf6-frame-current/SKILL.md'
)

foreach ($entry in $requiredEntries) {
  if ($entries -notcontains $entry) {
    throw "Release bundle missing required entry: $entry"
  }
}

$disallowedPrefixes = @(
  'sf6-skills/.agents/'
  'sf6-skills/data/'
  'sf6-skills/docs/'
  'sf6-skills/ingest/'
  'sf6-skills/maintainer-skills/'
  'sf6-skills/packages/'
  'sf6-skills/scripts/'
  'sf6-skills/shared/'
  'sf6-skills/tests/'
)

foreach ($prefix in $disallowedPrefixes) {
  if (($entries | Where-Object { $_.StartsWith($prefix) }).Count -gt 0) {
    throw "Release bundle contains disallowed content under: $prefix"
  }
}

Write-Host 'Release bundle OK'
```

- [ ] **Step 4: Run the validator and verify it fails**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-release-bundle.ps1
```

Expected: FAIL because `packages/skill-packaging/build-release-bundle.ps1` and `.dist/sf6-skills-bundle.zip` do not exist yet.

- [ ] **Step 5: Commit**

```bash
git add .gitignore docs/distribution/release-bundle.md tests/packaging/validate-release-bundle.ps1
git commit -m "test: define release bundle contract"
```

## Task 2: Build The Release Bundle

**Files:**

- Modify: `E:\github\SF6-skills\packages\skill-packaging\README.md`
- Create: `E:\github\SF6-skills\packages\skill-packaging\build-release-bundle.ps1`
- Generate: `E:\github\SF6-skills\.dist\sf6-skills-bundle.zip`

- [ ] **Step 1: Update the packaging README**

Replace `packages/skill-packaging/README.md` with:

```markdown
# skill-packaging

Shared packaging scripts live here.

Current entrypoints:

- `build-frame-current-runtime-assets.ps1`
- `build-release-bundle.ps1`
```

- [ ] **Step 2: Create the release bundle builder**

Create `packages/skill-packaging/build-release-bundle.ps1` with:

```powershell
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillsRoot = Join-Path $repoRoot 'skills'
$distRoot = Join-Path $repoRoot '.dist'
$archiveRoot = Join-Path $distRoot 'bundle-root'
$stagedRepoRoot = Join-Path $archiveRoot 'sf6-skills'
$bundlePath = Join-Path $distRoot 'sf6-skills-bundle.zip'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
  throw "Missing public skills root: $skillsRoot"
}

if (Test-Path -LiteralPath $bundlePath -PathType Leaf) {
  Remove-Item -LiteralPath $bundlePath -Force
}

if (Test-Path -LiteralPath $archiveRoot) {
  Remove-Item -LiteralPath $archiveRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $stagedRepoRoot -Force | Out-Null
Copy-Item -LiteralPath $skillsRoot -Destination (Join-Path $stagedRepoRoot 'skills') -Recurse -Force

[System.IO.Compression.ZipFile]::CreateFromDirectory($archiveRoot, $bundlePath)
Remove-Item -LiteralPath $archiveRoot -Recurse -Force

Write-Host 'Release bundle built'
```

- [ ] **Step 3: Build the bundle**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

Expected: PASS with `Release bundle built`.

- [ ] **Step 4: Run the bundle validator**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-release-bundle.ps1
```

Expected: PASS with `Release bundle OK`.

- [ ] **Step 5: Commit**

```bash
git add packages/skill-packaging/README.md packages/skill-packaging/build-release-bundle.ps1
git commit -m "feat: add release bundle builder"
```

## Task 3: Add The Shared Installer Contract

**Files:**

- Modify: `E:\github\SF6-skills\packages\skill-installers\README.md`
- Create: `E:\github\SF6-skills\packages\skill-installers\resolve-install-target.ps1`
- Create: `E:\github\SF6-skills\packages\skill-installers\install-sf6-skills.ps1`
- Create: `E:\github\SF6-skills\tests\install\validate-installer-contract.ps1`

- [ ] **Step 1: Write the failing installer validator**

Create `tests/install/validate-installer-contract.ps1` with:

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$bundlePath = Join-Path $repoRoot '.dist\sf6-skills-bundle.zip'
$resolverPath = Join-Path $repoRoot 'packages\skill-installers\resolve-install-target.ps1'
$installerPath = Join-Path $repoRoot 'packages\skill-installers\install-sf6-skills.ps1'
$readmePath = Join-Path $repoRoot 'packages\skill-installers\README.md'
$fixtureRoot = Join-Path $repoRoot '.dist\installer-fixtures'

foreach ($path in @($bundlePath, $resolverPath, $installerPath, $readmePath)) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing installer contract file: $path"
  }
}

if (Test-Path -LiteralPath $fixtureRoot) {
  Remove-Item -LiteralPath $fixtureRoot -Recurse -Force
}

$expectedSuffix = @{
  codex = '.agents/skills/sf6-skills'
  opencode = '.config/opencode/skills/sf6-skills'
  claude = '.claude/skills/sf6-skills'
  cursor = '.cursor/skills/sf6-skills'
}

foreach ($agent in @('codex', 'opencode', 'claude', 'cursor')) {
  $dryRunJson = powershell -ExecutionPolicy Bypass -File $installerPath -Agent $agent -DryRun
  $dryRun = $dryRunJson | ConvertFrom-Json

  if ($dryRun.agent -ne $agent) {
    throw "Dry-run agent mismatch for $agent"
  }

  if ($dryRun.source -notmatch 'sf6-skills-bundle\.zip$') {
    throw "Dry-run bundle source missing release bundle name for $agent"
  }

  $normalizedTargetPath = $dryRun.target_path.Replace('\', '/')
  if ($normalizedTargetPath -notlike "*$($expectedSuffix[$agent])") {
    throw "Dry-run target path mismatch for $agent: $($dryRun.target_path)"
  }

  $agentFixtureRoot = Join-Path $fixtureRoot $agent
  $installOutput = powershell -ExecutionPolicy Bypass -File $installerPath -Agent $agent -Source $bundlePath -TargetRoot $agentFixtureRoot

  if ($installOutput -notmatch [regex]::Escape("Installed sf6-skills for $agent")) {
    throw "Installer success output mismatch for $agent"
  }

  $installedRoot = Join-Path $agentFixtureRoot 'sf6-skills'
  foreach ($relativePath in @('kb-sf6-core\SKILL.md', 'kb-sf6-frame-current\SKILL.md')) {
    $fullPath = Join-Path $installedRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
      throw "Installed skill file missing for $agent: $relativePath"
    }
  }
}

Write-Host 'Installer contract OK'
```

- [ ] **Step 2: Run the validator and verify it fails**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-installer-contract.ps1
```

Expected: FAIL because the installer scripts do not exist yet.

- [ ] **Step 3: Update the installer README**

Replace `packages/skill-installers/README.md` with:

```markdown
# skill-installers

Shared installer scripts live here for Codex, OpenCode, Claude, and Cursor.

Current entrypoints:

- `resolve-install-target.ps1`
- `install-sf6-skills.ps1`
```

- [ ] **Step 4: Create the target resolver**

Create `packages/skill-installers/resolve-install-target.ps1` with:

```powershell
Set-StrictMode -Version Latest

param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'opencode', 'claude', 'cursor')]
  [string]$Agent,

  [string]$LibraryName = 'sf6-skills',

  [string]$TargetRoot
)

if (-not [string]::IsNullOrWhiteSpace($TargetRoot)) {
  return (Join-Path $TargetRoot $LibraryName)
}

switch ($Agent) {
  'codex' {
    return (Join-Path $HOME '.agents\skills\sf6-skills')
  }
  'opencode' {
    return (Join-Path $HOME '.config\opencode\skills\sf6-skills')
  }
  'claude' {
    return (Join-Path $HOME '.claude\skills\sf6-skills')
  }
  'cursor' {
    return (Join-Path $HOME '.cursor\skills\sf6-skills')
  }
}
```

- [ ] **Step 5: Create the shared installer**

Create `packages/skill-installers/install-sf6-skills.ps1` with:

```powershell
Set-StrictMode -Version Latest

param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'opencode', 'claude', 'cursor')]
  [string]$Agent,

  [string]$Version = 'latest',

  [string]$Source,

  [string]$TargetRoot,

  [switch]$DryRun
)

$repoOwner = 'NPJigaK'
$repoName = 'SF6-skills'
$bundleName = 'sf6-skills-bundle.zip'
$resolverPath = Join-Path $PSScriptRoot 'resolve-install-target.ps1'

if (-not (Test-Path -LiteralPath $resolverPath -PathType Leaf)) {
  throw "Missing install target resolver: $resolverPath"
}

if ([string]::IsNullOrWhiteSpace($Source)) {
  if ($Version -eq 'latest') {
    $Source = "https://github.com/$repoOwner/$repoName/releases/latest/download/$bundleName"
  }
  else {
    $Source = "https://github.com/$repoOwner/$repoName/releases/download/$Version/$bundleName"
  }
}

$targetPath = powershell -ExecutionPolicy Bypass -File $resolverPath -Agent $Agent -TargetRoot $TargetRoot
$libraryLeaf = Split-Path -Leaf $targetPath

if ($libraryLeaf -ne 'sf6-skills') {
  throw "Installer target must resolve to the sf6-skills library root: $targetPath"
}

if ($DryRun) {
  @{
    agent = $Agent
    source = $Source
    target_path = $targetPath
  } | ConvertTo-Json -Depth 4
  return
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('sf6-skills-install-' + [guid]::NewGuid().ToString('N'))
$bundlePath = Join-Path $tempRoot $bundleName
$extractRoot = Join-Path $tempRoot 'extract'

New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
New-Item -ItemType Directory -Path $extractRoot -Force | Out-Null

try {
  if ($Source -match '^https?://') {
    Invoke-WebRequest -Uri $Source -OutFile $bundlePath
  }
  else {
    Copy-Item -LiteralPath (Resolve-Path $Source).Path -Destination $bundlePath -Force
  }

  Expand-Archive -LiteralPath $bundlePath -DestinationPath $extractRoot -Force
  $bundledSkillsRoot = Join-Path $extractRoot 'sf6-skills\skills'

  if (-not (Test-Path -LiteralPath $bundledSkillsRoot -PathType Container)) {
    throw "Bundled skills root missing from release bundle: $bundledSkillsRoot"
  }

  $targetParent = Split-Path -Parent $targetPath
  New-Item -ItemType Directory -Path $targetParent -Force | Out-Null

  if (Test-Path -LiteralPath $targetPath) {
    Remove-Item -LiteralPath $targetPath -Recurse -Force
  }

  New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
  Get-ChildItem -LiteralPath $bundledSkillsRoot | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $targetPath -Recurse -Force
  }
}
finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}

Write-Host "Installed sf6-skills for $Agent to $targetPath"
```

- [ ] **Step 6: Run the installer validator**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-installer-contract.ps1
```

Expected: PASS with `Installer contract OK`.

- [ ] **Step 7: Commit**

```bash
git add packages/skill-installers/README.md packages/skill-installers/resolve-install-target.ps1 packages/skill-installers/install-sf6-skills.ps1 tests/install/validate-installer-contract.ps1
git commit -m "feat: add release bundle installer"
```

## Task 4: Wire The Agent Entry Surfaces

**Files:**

- Modify: `E:\github\SF6-skills\.codex\INSTALL.md`
- Modify: `E:\github\SF6-skills\.opencode\INSTALL.md`
- Create: `E:\github\SF6-skills\.claude-plugin\INSTALL.md`
- Create: `E:\github\SF6-skills\.cursor-plugin\INSTALL.md`
- Modify: `E:\github\SF6-skills\.cursor-plugin\README.md`
- Modify: `E:\github\SF6-skills\docs\distribution\README.md`
- Modify: `E:\github\SF6-skills\docs\distribution\codex.md`
- Modify: `E:\github\SF6-skills\docs\distribution\opencode.md`
- Modify: `E:\github\SF6-skills\docs\distribution\claude.md`
- Modify: `E:\github\SF6-skills\docs\distribution\cursor.md`
- Modify: `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`

- [ ] **Step 1: Tighten the distribution validator so the old docs fail**

Replace `tests/install/validate-distribution-surface.ps1` with:

```powershell
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

foreach ($relativePath in $required) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath)) {
    throw "Missing distribution file: $relativePath"
  }
}

$installDocs = @(
  '.codex/INSTALL.md',
  '.opencode/INSTALL.md',
  '.claude-plugin/INSTALL.md',
  '.cursor-plugin/INSTALL.md'
)

foreach ($relativePath in $installDocs) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $relativePath) -Raw
  if ($content -notmatch [regex]::Escape('install-sf6-skills.ps1')) {
    throw "$relativePath missing installer script reference"
  }
  if ($content -notmatch [regex]::Escape('sf6-skills-bundle.zip')) {
    throw "$relativePath missing release bundle reference"
  }
}

$codex = Get-Content -LiteralPath (Join-Path $repoRoot '.codex/INSTALL.md') -Raw
if ($codex -match [regex]::Escape('git clone')) {
  throw 'Codex install doc still uses clone-first flow'
}

$opencode = Get-Content -LiteralPath (Join-Path $repoRoot '.opencode/INSTALL.md') -Raw
if ($opencode -match [regex]::Escape('@git+https://github.com/NPJigaK/SF6-skills.git')) {
  throw 'OpenCode install doc still uses direct git plugin flow'
}

$marketplace = Get-Content -LiteralPath (Join-Path $repoRoot '.claude-plugin/marketplace.json') -Raw | ConvertFrom-Json
if ($marketplace.plugins[0].name -ne 'sf6-skills') {
  throw 'Unexpected Claude plugin name'
}

Write-Host 'Distribution surface OK'
```

- [ ] **Step 2: Run the distribution validator and verify it fails**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
```

Expected: FAIL because the new Claude/Cursor install entrypoints do not exist and Codex/OpenCode still document the old source-repo flow.

- [ ] **Step 3: Update the agent front-door docs**

Replace `.codex/INSTALL.md` with:

```markdown
# Codex Install

Ask Codex to run this install flow:

```text
Fetch `https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1`, save it locally, and run it for agent `codex` using the latest `sf6-skills-bundle.zip` release from `NPJigaK/SF6-skills`.
```

Target install path:

- `~/.agents/skills/sf6-skills`
```

Replace `.opencode/INSTALL.md` with:

```markdown
# OpenCode Install

Ask OpenCode to run this install flow:

```text
Fetch `https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1`, save it locally, and run it for agent `opencode` using the latest `sf6-skills-bundle.zip` release from `NPJigaK/SF6-skills`.
```

Target install path:

- `~/.config/opencode/skills/sf6-skills`
```

Create `.claude-plugin/INSTALL.md` with:

```markdown
# Claude Install

Ask Claude to run this install flow:

```text
Fetch `https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1`, save it locally, and run it for agent `claude` using the latest `sf6-skills-bundle.zip` release from `NPJigaK/SF6-skills`.
```

Target install path:

- `~/.claude/skills/sf6-skills`
```

Create `.cursor-plugin/INSTALL.md` with:

```markdown
# Cursor Install

Ask Cursor to run this install flow:

```text
Fetch `https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1`, save it locally, and run it for agent `cursor` using the latest `sf6-skills-bundle.zip` release from `NPJigaK/SF6-skills`.
```

Target install path:

- `~/.cursor/skills/sf6-skills`
```

Replace `.cursor-plugin/README.md` with:

```markdown
# Cursor Plugin

Cursor distribution uses the shared release-bundle installer.

Primary install reference:

- `INSTALL.md`
```

- [ ] **Step 4: Update the distribution docs**

Replace `docs/distribution/README.md` with:

```markdown
# Distribution Docs

Agent-specific installation and distribution guidance.

Front doors:

- [`.codex/INSTALL.md`](../../.codex/INSTALL.md)
- [`.opencode/INSTALL.md`](../../.opencode/INSTALL.md)
- [`.claude-plugin/INSTALL.md`](../../.claude-plugin/INSTALL.md)
- [`.cursor-plugin/INSTALL.md`](../../.cursor-plugin/INSTALL.md)
- [`release-bundle.md`](./release-bundle.md)
```

Replace `docs/distribution/codex.md` with:

```markdown
# Codex Distribution

Codex distribution uses the shared release-bundle installer.

Primary install reference:

- [`.codex/INSTALL.md`](../../.codex/INSTALL.md)
```

Replace `docs/distribution/opencode.md` with:

```markdown
# OpenCode Distribution

OpenCode distribution uses the shared release-bundle installer.

Primary install reference:

- [`.opencode/INSTALL.md`](../../.opencode/INSTALL.md)
```

Replace `docs/distribution/claude.md` with:

```markdown
# Claude Distribution

Claude distribution uses the shared release-bundle installer plus the development marketplace manifest.

Primary install references:

- [`.claude-plugin/INSTALL.md`](../../.claude-plugin/INSTALL.md)
- [`.claude-plugin/marketplace.json`](../../.claude-plugin/marketplace.json)
```

Replace `docs/distribution/cursor.md` with:

```markdown
# Cursor Distribution

Cursor distribution uses the shared release-bundle installer.

Primary install reference:

- [`.cursor-plugin/INSTALL.md`](../../.cursor-plugin/INSTALL.md)
```

- [ ] **Step 5: Run the distribution validators**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Distribution surface OK`
- `Docs OK`

- [ ] **Step 6: Commit**

```bash
git add .codex/INSTALL.md .opencode/INSTALL.md .claude-plugin/INSTALL.md .cursor-plugin/INSTALL.md .cursor-plugin/README.md docs/distribution/README.md docs/distribution/codex.md docs/distribution/opencode.md docs/distribution/claude.md docs/distribution/cursor.md tests/install/validate-distribution-surface.ps1
git commit -m "docs: add release installer entry surfaces"
```

## Task 5: Run End-To-End Verification

**Files:**

- Verify only: `E:\github\SF6-skills\.dist\sf6-skills-bundle.zip`
- Verify only: `E:\github\SF6-skills\packages\skill-installers\install-sf6-skills.ps1`
- Verify only: `E:\github\SF6-skills\tests\packaging\validate-release-bundle.ps1`
- Verify only: `E:\github\SF6-skills\tests\install\validate-installer-contract.ps1`
- Verify only: `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`

- [ ] **Step 1: Rebuild the release bundle**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

Expected: `Release bundle built`

- [ ] **Step 2: Run packaging and installer verification**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-release-bundle.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-installer-contract.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Release bundle OK`
- `Installer contract OK`
- `Distribution surface OK`
- `Docs OK`

- [ ] **Step 3: Sanity-check existing public-skill surfaces**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
python -m pytest ingest/frame_data/tests -q
```

Expected:

- `kb-sf6-frame-current public shell OK`
- `Frame-current runtime assets OK`
- `Frame-current boundary doc OK`
- `Dogfood mirror OK`
- `23 passed`

- [ ] **Step 4: Confirm the working tree is clean apart from ignored `.dist/` output**

Run:

```powershell
git status --short
```

Expected: no tracked file changes.

## Spec Coverage Check

- release bundle artifact and contract: covered by Tasks 1 and 2
- shared installer implementation: covered by Task 3
- four agent-specific entry surfaces: covered by Task 4
- repo clone no longer being the primary end-user install story: covered by Task 4 docs
- validation of bundle contents and installer behavior: covered by Tasks 1, 3, and 5

## Placeholder Scan

- No task depends on unspecified bundle names, unspecified target paths, or unspecified release commands.
- The only generated artifact is `.dist/sf6-skills-bundle.zip`, created by the plan itself.

## Type And Naming Consistency

- bundle name is always `sf6-skills-bundle.zip`
- installed library name is always `sf6-skills`
- canonical source root is always `skills/`
- shared installer entrypoint is always `packages/skill-installers/install-sf6-skills.ps1`
- supported agents are always `codex`, `opencode`, `claude`, `cursor`
