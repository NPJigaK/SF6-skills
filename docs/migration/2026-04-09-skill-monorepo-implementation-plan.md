# Skill Monorepo Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the repository into a future-proof skill monorepo by making `skills/` the canonical public surface, separating maintainer-only workflows, and adding the minimum cross-agent distribution and authoring infrastructure needed to grow beyond the current SF6 skills.

**Architecture:** Treat `skills/<skill-name>/` as the source of truth for public skills, `maintainer-skills/` as the home for repo-only workflows, and `packages/` plus `shared/` as the small shared layer for packaging, validation, and templates. Keep `.agents/skills/` only as a repo-local compatibility mirror, not as an authoritative source, and stop this plan at the point where `kb-sf6-frame-current` has a documented packaging decision rather than forcing a premature migration.

**Tech Stack:** Markdown, PowerShell, Git, JSON metadata, existing `.agents/skills` content

---

## Planned File Map

**Create:**

- `E:\github\SF6-skills\skills\README.md`
- `E:\github\SF6-skills\maintainer-skills\README.md`
- `E:\github\SF6-skills\packages\README.md`
- `E:\github\SF6-skills\shared\README.md`
- `E:\github\SF6-skills\docs\architecture\README.md`
- `E:\github\SF6-skills\docs\authoring\README.md`
- `E:\github\SF6-skills\docs\authoring\automation-prompts\triage-new-notes.md`
- `E:\github\SF6-skills\docs\authoring\new-skill.md`
- `E:\github\SF6-skills\docs\distribution\README.md`
- `E:\github\SF6-skills\docs\distribution\codex.md`
- `E:\github\SF6-skills\docs\distribution\claude.md`
- `E:\github\SF6-skills\docs\distribution\cursor.md`
- `E:\github\SF6-skills\docs\distribution\opencode.md`
- `E:\github\SF6-skills\docs\distribution\repo-local-dogfooding.md`
- `E:\github\SF6-skills\docs\testing\README.md`
- `E:\github\SF6-skills\docs\architecture\kb-sf6-frame-current-packaging.md`
- `E:\github\SF6-skills\skills\kb-sf6-core\SKILL.md`
- `E:\github\SF6-skills\skills\kb-sf6-core\references\CORE_QUESTIONS.md`
- `E:\github\SF6-skills\skills\kb-sf6-core\references\KNOWLEDGE.md`
- `E:\github\SF6-skills\skills\kb-sf6-core\references\REVIEW_QUEUE.md`
- `E:\github\SF6-skills\skills\kb-sf6-core\references\SOURCE_POLICY.md`
- `E:\github\SF6-skills\maintainer-skills\sync-knowledge\SKILL.md`
- `E:\github\SF6-skills\maintainer-skills\sync-knowledge\references\SYNC_POLICY.md`
- `E:\github\SF6-skills\maintainer-skills\sync-knowledge\templates\ENTRY_TEMPLATE.md`
- `E:\github\SF6-skills\maintainer-skills\sync-knowledge\templates\REVIEW_TEMPLATE.md`
- `E:\github\SF6-skills\packages\skill-installers\README.md`
- `E:\github\SF6-skills\packages\skill-validator\README.md`
- `E:\github\SF6-skills\shared\templates\skill\SKILL.md.template`
- `E:\github\SF6-skills\shared\templates\skill\README.md`
- `E:\github\SF6-skills\shared\schemas\README.md`
- `E:\github\SF6-skills\scripts\dev\sync-dogfood-skills.ps1`
- `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`
- `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- `E:\github\SF6-skills\tests\integration\validate-kb-sf6-core-location.ps1`
- `E:\github\SF6-skills\tests\install\validate-dogfood-mirror.ps1`
- `E:\github\SF6-skills\tests\integration\validate-maintainer-surface.ps1`
- `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`
- `E:\github\SF6-skills\tests\packaging\validate-authoring-assets.ps1`
- `E:\github\SF6-skills\tests\integration\validate-frame-current-boundary.ps1`
- `E:\github\SF6-skills\.codex\INSTALL.md`
- `E:\github\SF6-skills\.opencode\INSTALL.md`
- `E:\github\SF6-skills\.claude-plugin\marketplace.json`
- `E:\github\SF6-skills\.cursor-plugin\README.md`

**Modify:**

- `E:\github\SF6-skills\README.md`
- `E:\github\SF6-skills\AGENTS.md`
- `E:\github\SF6-skills\.agents\AGENTS.md`

**Delete after migration:**

- `E:\github\SF6-skills\.agents\skills\sync-knowledge\`
- `E:\github\SF6-skills\.agents\automation-prompts\triage-new-notes.md`

## Scope Note

This plan intentionally handles the public-surface bootstrap and the first easy migration (`kb-sf6-core`), then stops after documenting the packaging boundary for `kb-sf6-frame-current`.

Do not fold the actual `kb-sf6-frame-current` migration into this plan. Once the boundary document exists and the runtime-input decision is explicit, write a separate follow-up implementation plan for that skill.

### Task 1: Scaffold The Monorepo Surface

**Files:**

- Create: `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`
- Create: `E:\github\SF6-skills\skills\README.md`
- Create: `E:\github\SF6-skills\maintainer-skills\README.md`
- Create: `E:\github\SF6-skills\packages\README.md`
- Create: `E:\github\SF6-skills\shared\README.md`
- Create: `E:\github\SF6-skills\docs\architecture\README.md`
- Create: `E:\github\SF6-skills\docs\authoring\README.md`
- Create: `E:\github\SF6-skills\docs\distribution\README.md`
- Create: `E:\github\SF6-skills\docs\testing\README.md`

- [ ] **Step 1: Write the failing layout validation script**

```powershell
$required = @(
  'skills',
  'maintainer-skills',
  'packages',
  'shared',
  'docs/architecture',
  'docs/authoring',
  'docs/distribution',
  'docs/testing',
  'tests/install',
  'tests/integration',
  'tests/packaging',
  'scripts/dev'
)

$missing = $required | Where-Object { -not (Test-Path $_) }

if ($missing.Count -gt 0) {
  throw "Missing required paths: $($missing -join ', ')"
}

Write-Host 'Layout OK'
```

- [ ] **Step 2: Run the layout script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`  
Expected: FAIL with at least `skills` and `maintainer-skills` listed as missing.

- [ ] **Step 3: Create the monorepo directories and marker docs**

```powershell
$dirs = @(
  'skills',
  'maintainer-skills',
  'packages/skill-installers',
  'packages/skill-validator',
  'shared/templates/skill',
  'shared/schemas',
  'docs/architecture',
  'docs/authoring/automation-prompts',
  'docs/distribution',
  'docs/testing',
  'tests/install',
  'tests/integration',
  'tests/packaging',
  'scripts/dev',
  '.claude-plugin',
  '.cursor-plugin',
  '.codex',
  '.opencode'
)

$dirs | ForEach-Object {
  New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

Set-Content 'skills/README.md' "# Public Skills`n`nCanonical source for distributed skills lives here."
Set-Content 'maintainer-skills/README.md' "# Maintainer Skills`n`nRepository-only workflows live here."
Set-Content 'packages/README.md' "# Packages`n`nShared executable infrastructure for packaging, validation, and installers."
Set-Content 'shared/README.md' "# Shared`n`nShared non-code artifacts such as templates, schemas, and vocabulary."
Set-Content 'docs/architecture/README.md' "# Architecture Docs`n`nRepository-level architecture notes and dependency-boundary decisions."
Set-Content 'docs/authoring/README.md' "# Authoring Docs`n`nHow to add and maintain skills in this repository."
Set-Content 'docs/distribution/README.md' "# Distribution Docs`n`nAgent-specific installation and distribution guidance."
Set-Content 'docs/testing/README.md' "# Testing Docs`n`nHow to verify layout, packaging, and installation surfaces."
```

- [ ] **Step 4: Run the layout script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`  
Expected: PASS with `Layout OK`.

- [ ] **Step 5: Commit**

```bash
git add tests/packaging/validate-layout.ps1 skills maintainer-skills packages shared docs tests scripts .claude-plugin .cursor-plugin .codex .opencode
git commit -m "chore: scaffold skill monorepo layout"
```

### Task 2: Rewrite Canonical Path Documentation

**Files:**

- Create: `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- Modify: `E:\github\SF6-skills\README.md`
- Modify: `E:\github\SF6-skills\AGENTS.md`
- Modify: `E:\github\SF6-skills\.agents\AGENTS.md`

- [ ] **Step 1: Write the failing docs validation script**

```powershell
$checks = @(
  @{ Path = 'README.md'; MustContain = 'skills/'; MustNotContain = '.agents/skills/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/'; MustNotContain = '.agents/skills/sync-knowledge/' },
  @{ Path = '.agents/AGENTS.md'; MustContain = 'generated compatibility output'; MustNotContain = 'skills and related assets only' }
)

foreach ($check in $checks) {
  $content = Get-Content $check.Path -Raw
  if ($content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
```

- [ ] **Step 2: Run the docs validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`  
Expected: FAIL because the current docs still point to `.agents/skills/*` as canonical.

- [ ] **Step 3: Update the root docs and compatibility note**

Update `README.md` so the durable checked-in surface calls out:

```markdown
## Durable Checked-In Surface

- public skills
  - `skills/<skill-name>/`
- maintainer-only skills
  - `maintainer-skills/<skill-name>/`
- shared infrastructure
  - `packages/`
  - `shared/`
  - `docs/`
  - `tests/`
  - `scripts/`
- code
  - `ingest/frame_data/`
- published current-fact artifacts
  - `data/exports/<character_slug>/`
```

Update `AGENTS.md` so the skills section reads:

```markdown
## Knowledge と Skills
- 不変概念は `skills/kb-sf6-core/` に寄せる。
- supported baseline characters の current fact は `skills/kb-sf6-frame-current/` を使い、published exports だけを読む。
- knowledge の統合作業は `maintainer-skills/sync-knowledge/` を使う。
```

Replace `.agents/AGENTS.md` with:

```markdown
# Compatibility Layer

Repo-wide guidance is defined in the root `AGENTS.md`.

`.agents/skills/` is generated compatibility output for repo-local dogfooding.
Do not treat `.agents/skills/` as the canonical source for distributed skills.
```

- [ ] **Step 4: Run the docs validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`  
Expected: PASS with `Docs OK`.

- [ ] **Step 5: Commit**

```bash
git add README.md AGENTS.md .agents/AGENTS.md tests/packaging/validate-doc-links.ps1
git commit -m "docs: point repo guidance at monorepo structure"
```

### Task 3: Create The Public `kb-sf6-core` Canonical Copy

**Files:**

- Create: `E:\github\SF6-skills\tests\integration\validate-kb-sf6-core-location.ps1`
- Create: `E:\github\SF6-skills\skills\kb-sf6-core\SKILL.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-core\references\CORE_QUESTIONS.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-core\references\KNOWLEDGE.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-core\references\REVIEW_QUEUE.md`
- Create: `E:\github\SF6-skills\skills\kb-sf6-core\references\SOURCE_POLICY.md`

- [ ] **Step 1: Write the failing location validation script**

```powershell
$required = @(
  'skills/kb-sf6-core/SKILL.md',
  'skills/kb-sf6-core/references/CORE_QUESTIONS.md',
  'skills/kb-sf6-core/references/KNOWLEDGE.md',
  'skills/kb-sf6-core/references/REVIEW_QUEUE.md',
  'skills/kb-sf6-core/references/SOURCE_POLICY.md'
)

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing kb-sf6-core public files: $($missing -join ', ')"
}

$oldFiles = Get-ChildItem '.agents/skills/kb-sf6-core' -Recurse -File | ForEach-Object { $_.Name } | Sort-Object
$newFiles = Get-ChildItem 'skills/kb-sf6-core' -Recurse -File | ForEach-Object { $_.Name } | Sort-Object

if (@($oldFiles) -join '|' -ne @($newFiles) -join '|') {
  throw 'Public kb-sf6-core file set does not match legacy source'
}

Write-Host 'kb-sf6-core public copy OK'
```

- [ ] **Step 2: Run the validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`  
Expected: FAIL because `skills/kb-sf6-core/` does not exist yet.

- [ ] **Step 3: Copy the current public skill into `skills/`**

```powershell
New-Item -ItemType Directory -Force -Path 'skills/kb-sf6-core/references' | Out-Null
Copy-Item '.agents/skills/kb-sf6-core/SKILL.md' 'skills/kb-sf6-core/SKILL.md'
Copy-Item '.agents/skills/kb-sf6-core/references/CORE_QUESTIONS.md' 'skills/kb-sf6-core/references/CORE_QUESTIONS.md'
Copy-Item '.agents/skills/kb-sf6-core/references/KNOWLEDGE.md' 'skills/kb-sf6-core/references/KNOWLEDGE.md'
Copy-Item '.agents/skills/kb-sf6-core/references/REVIEW_QUEUE.md' 'skills/kb-sf6-core/references/REVIEW_QUEUE.md'
Copy-Item '.agents/skills/kb-sf6-core/references/SOURCE_POLICY.md' 'skills/kb-sf6-core/references/SOURCE_POLICY.md'
```

- [ ] **Step 4: Run the validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`  
Expected: PASS with `kb-sf6-core public copy OK`.

- [ ] **Step 5: Commit**

```bash
git add skills/kb-sf6-core tests/integration/validate-kb-sf6-core-location.ps1
git commit -m "feat: add kb-sf6-core to public skills surface"
```

### Task 4: Add Repo-Local Dogfooding Sync For Public Skills

**Files:**

- Create: `E:\github\SF6-skills\scripts\dev\sync-dogfood-skills.ps1`
- Create: `E:\github\SF6-skills\tests\install\validate-dogfood-mirror.ps1`
- Create: `E:\github\SF6-skills\docs\distribution\repo-local-dogfooding.md`
- Modify: `E:\github\SF6-skills\.agents\AGENTS.md`

- [ ] **Step 1: Write the failing dogfood-mirror test**

```powershell
$sourceRoot = 'skills/kb-sf6-core'
$targetRoot = '.agents/skills/kb-sf6-core'

if (-not (Test-Path 'scripts/dev/sync-dogfood-skills.ps1')) {
  throw 'Missing sync script'
}

if (-not (Test-Path $sourceRoot)) {
  throw 'Missing public source skill'
}

if (-not (Test-Path $targetRoot)) {
  throw 'Missing dogfood mirror target'
}

$sourceHash = Get-FileHash "$sourceRoot/SKILL.md"
$targetHash = Get-FileHash "$targetRoot/SKILL.md"

if ($sourceHash.Hash -ne $targetHash.Hash) {
  throw 'Dogfood mirror is out of sync with public source'
}

Write-Host 'Dogfood mirror OK'
```

- [ ] **Step 2: Run the dogfood-mirror test to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`  
Expected: FAIL because the sync script does not exist yet.

- [ ] **Step 3: Implement the sync script and usage note**

Create `scripts/dev/sync-dogfood-skills.ps1` with:

```powershell
$sourceRoot = Resolve-Path 'skills'
$targetRoot = Join-Path (Resolve-Path '.agents').Path 'skills'

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$publicSkills = Get-ChildItem $sourceRoot -Directory
$publicNames = $publicSkills.Name

foreach ($skill in $publicSkills) {
  $destination = Join-Path $targetRoot $skill.Name
  if (Test-Path $destination) {
    Remove-Item -LiteralPath $destination -Recurse -Force
  }
  Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse
}

Get-ChildItem $targetRoot -Directory |
  Where-Object { $_.Name -notin $publicNames } |
  ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

Write-Host "Synced $($publicSkills.Count) public skills to .agents/skills"
```

Create `docs/distribution/repo-local-dogfooding.md` with:

````markdown
# Repo-Local Dogfooding

`skills/` is the canonical public source.

For repo-local Codex discovery, mirror the public skills into `.agents/skills/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

Only distributed skills are mirrored. Maintainer-only skills stay outside `.agents/skills/`.
````

- [ ] **Step 4: Run the sync script and re-run the test**

Run: `powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1`  
Expected: PASS with `Synced 1 public skills to .agents/skills`

Run: `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`  
Expected: PASS with `Dogfood mirror OK`.

- [ ] **Step 5: Commit**

```bash
git add scripts/dev/sync-dogfood-skills.ps1 tests/install/validate-dogfood-mirror.ps1 docs/distribution/repo-local-dogfooding.md .agents/AGENTS.md .agents/skills/kb-sf6-core
git commit -m "chore: add dogfood sync for public skills"
```

### Task 5: Move Maintainer-Only Assets Out Of The Public Surface

**Files:**

- Create: `E:\github\SF6-skills\maintainer-skills\sync-knowledge\SKILL.md`
- Create: `E:\github\SF6-skills\maintainer-skills\sync-knowledge\references\SYNC_POLICY.md`
- Create: `E:\github\SF6-skills\maintainer-skills\sync-knowledge\templates\ENTRY_TEMPLATE.md`
- Create: `E:\github\SF6-skills\maintainer-skills\sync-knowledge\templates\REVIEW_TEMPLATE.md`
- Create: `E:\github\SF6-skills\docs\authoring\automation-prompts\triage-new-notes.md`
- Create: `E:\github\SF6-skills\tests\integration\validate-maintainer-surface.ps1`
- Delete: `E:\github\SF6-skills\.agents\skills\sync-knowledge\`
- Delete: `E:\github\SF6-skills\.agents\automation-prompts\triage-new-notes.md`

- [ ] **Step 1: Write the failing maintainer-surface validation script**

```powershell
$required = @(
  'maintainer-skills/sync-knowledge/SKILL.md',
  'maintainer-skills/sync-knowledge/references/SYNC_POLICY.md',
  'maintainer-skills/sync-knowledge/templates/ENTRY_TEMPLATE.md',
  'maintainer-skills/sync-knowledge/templates/REVIEW_TEMPLATE.md',
  'docs/authoring/automation-prompts/triage-new-notes.md'
)

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing maintainer assets: $($missing -join ', ')"
}

if (Test-Path '.agents/skills/sync-knowledge') {
  throw 'Legacy maintainer skill still present in .agents/skills'
}

if (Test-Path '.agents/automation-prompts/triage-new-notes.md') {
  throw 'Legacy automation prompt still present under .agents'
}

Write-Host 'Maintainer surface OK'
```

- [ ] **Step 2: Run the validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-maintainer-surface.ps1`  
Expected: FAIL because the new maintainer path does not exist and the old `.agents` path still does.

- [ ] **Step 3: Move the maintainer-only skill and automation prompt**

```powershell
New-Item -ItemType Directory -Force -Path 'maintainer-skills/sync-knowledge/references' | Out-Null
New-Item -ItemType Directory -Force -Path 'maintainer-skills/sync-knowledge/templates' | Out-Null
New-Item -ItemType Directory -Force -Path 'docs/authoring/automation-prompts' | Out-Null

Move-Item '.agents/skills/sync-knowledge/SKILL.md' 'maintainer-skills/sync-knowledge/SKILL.md'
Move-Item '.agents/skills/sync-knowledge/references/SYNC_POLICY.md' 'maintainer-skills/sync-knowledge/references/SYNC_POLICY.md'
Move-Item '.agents/skills/sync-knowledge/templates/ENTRY_TEMPLATE.md' 'maintainer-skills/sync-knowledge/templates/ENTRY_TEMPLATE.md'
Move-Item '.agents/skills/sync-knowledge/templates/REVIEW_TEMPLATE.md' 'maintainer-skills/sync-knowledge/templates/REVIEW_TEMPLATE.md'
Move-Item '.agents/automation-prompts/triage-new-notes.md' 'docs/authoring/automation-prompts/triage-new-notes.md'

Remove-Item -LiteralPath '.agents/skills/sync-knowledge' -Recurse -Force
```

- [ ] **Step 4: Run the validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-maintainer-surface.ps1`  
Expected: PASS with `Maintainer surface OK`.

- [ ] **Step 5: Commit**

```bash
git add -A maintainer-skills/sync-knowledge docs/authoring/automation-prompts/triage-new-notes.md .agents/skills/sync-knowledge .agents/automation-prompts/triage-new-notes.md tests/integration/validate-maintainer-surface.ps1
git commit -m "refactor: separate maintainer-only skill assets"
```

### Task 6: Add Minimum Distribution Surface For Codex, Claude, Cursor, And OpenCode

**Files:**

- Create: `E:\github\SF6-skills\.codex\INSTALL.md`
- Create: `E:\github\SF6-skills\.opencode\INSTALL.md`
- Create: `E:\github\SF6-skills\.claude-plugin\marketplace.json`
- Create: `E:\github\SF6-skills\.cursor-plugin\README.md`
- Create: `E:\github\SF6-skills\docs\distribution\codex.md`
- Create: `E:\github\SF6-skills\docs\distribution\claude.md`
- Create: `E:\github\SF6-skills\docs\distribution\cursor.md`
- Create: `E:\github\SF6-skills\docs\distribution\opencode.md`
- Create: `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`
- Create: `E:\github\SF6-skills\packages\skill-installers\README.md`

- [ ] **Step 1: Write the failing distribution validation script**

```powershell
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
```

- [ ] **Step 2: Run the distribution validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`  
Expected: FAIL because none of the distribution files exist yet.

- [ ] **Step 3: Create the distribution files and installer package note**

Create `.claude-plugin/marketplace.json` with:

```json
{
  "name": "sf6-skills-dev",
  "description": "Development marketplace for the SF6 skills monorepo",
  "owner": {
    "name": "devkey",
    "email": "noreply@example.invalid"
  },
  "plugins": [
    {
      "name": "sf6-skills",
      "description": "SF6 skill library for concept-first knowledge, current-fact lookups, and future analysis skills",
      "version": "0.1.0",
      "source": "./",
      "author": {
        "name": "devkey",
        "email": "noreply@example.invalid"
      }
    }
  ]
}
```

Create `.codex/INSTALL.md` with:

````markdown
# Installing SF6 Skills for Codex

## Prerequisites
- Git

## Installation
1. Clone the repository:
   `git clone https://github.com/NPJigaK/SF6-skills.git ~/.codex/sf6-skills`
2. Create the skills junction:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills" | Out-Null
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\sf6-skills" "$env:USERPROFILE\.codex\sf6-skills\skills"
```

3. Restart Codex.
````

Create `.opencode/INSTALL.md` with:

````markdown
# Installing SF6 Skills for OpenCode

Add this repository to the `plugin` array in `opencode.json`:

```json
{
  "plugin": ["sf6-skills@git+https://github.com/NPJigaK/SF6-skills.git"]
}
```

Restart OpenCode and verify the skills are discovered.
````

Create `.cursor-plugin/README.md` with:

```markdown
# Cursor Distribution

Cursor documentation is maintained first under `docs/distribution/cursor.md`.

Do not add marketplace metadata here until the repository has a verified Cursor plugin schema and a tested install path.
```

Create `packages/skill-installers/README.md` with:

```markdown
# skill-installers

Shared installer and packaging notes for Codex, Claude, Cursor, and OpenCode distribution surfaces.
```

Create `docs/distribution/codex.md` with:

```markdown
# Codex Distribution

Canonical public skills live under `skills/`.

Install by cloning the repository into `~/.codex/sf6-skills` and creating a junction from `~/.agents/skills/sf6-skills` to the repo's `skills/` directory.

For repo-local workspace testing, use `scripts/dev/sync-dogfood-skills.ps1`.
```

Create `docs/distribution/claude.md` with:

```markdown
# Claude Distribution

Claude distribution metadata lives in `.claude-plugin/marketplace.json`.

The plugin source is the repository root and the public skill source is `skills/`.

Update the plugin version whenever the first user-visible skill package changes.
```

Create `docs/distribution/cursor.md` with:

```markdown
# Cursor Distribution

Cursor support is documentation-first in phase 1.

Do not publish Cursor marketplace metadata until the install path and schema are verified against a working example.

Until then, treat this repository as the source layout and keep Cursor-specific notes here.
```

Create `docs/distribution/opencode.md` with:

```markdown
# OpenCode Distribution

OpenCode installs this repository through the `plugin` array in `opencode.json`.

The repository is the install unit and `skills/` is the public skill source inside that install.
```

- [ ] **Step 4: Run the distribution validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`  
Expected: PASS with `Distribution surface OK`.

- [ ] **Step 5: Commit**

```bash
git add .codex/INSTALL.md .opencode/INSTALL.md .claude-plugin/marketplace.json .cursor-plugin/README.md docs/distribution packages/skill-installers/README.md tests/install/validate-distribution-surface.ps1
git commit -m "feat: add multi-agent distribution surface"
```

### Task 7: Add Shared Authoring Assets For Future Skills

**Files:**

- Create: `E:\github\SF6-skills\shared\templates\skill\SKILL.md.template`
- Create: `E:\github\SF6-skills\shared\templates\skill\README.md`
- Create: `E:\github\SF6-skills\shared\schemas\README.md`
- Create: `E:\github\SF6-skills\docs\authoring\new-skill.md`
- Create: `E:\github\SF6-skills\tests\packaging\validate-authoring-assets.ps1`
- Create: `E:\github\SF6-skills\packages\skill-validator\README.md`

- [ ] **Step 1: Write the failing authoring-assets validation script**

```powershell
$required = @(
  'shared/templates/skill/SKILL.md.template',
  'shared/templates/skill/README.md',
  'shared/schemas/README.md',
  'docs/authoring/new-skill.md',
  'packages/skill-validator/README.md'
)

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing authoring assets: $($missing -join ', ')"
}

$template = Get-Content 'shared/templates/skill/SKILL.md.template' -Raw
if ($template -notmatch '^---') {
  throw 'Skill template missing frontmatter'
}

Write-Host 'Authoring assets OK'
```

- [ ] **Step 2: Run the validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`  
Expected: FAIL because none of the authoring assets exist yet.

- [ ] **Step 3: Create the new-skill template and docs**

Create `shared/templates/skill/SKILL.md.template` with:

```markdown
---
name: your-skill-name
description: One sentence describing when the agent should use this skill.
---

## Purpose

State the stable purpose of the skill in 2-3 sentences.

## When To Use

- Case 1
- Case 2

## Required Inputs

- Input A
- Input B

## Workflow

1. Resolve scope.
2. Read the minimum supporting references.
3. Produce the answer or artifact.

## Constraints

- Constraint 1
- Constraint 2
```

Create `shared/templates/skill/README.md` with:

```markdown
# Skill Template

Use this directory as the starting point for a new public skill under `skills/<skill-name>/`.

Keep skill-specific references, assets, scripts, and tests inside the skill directory until at least two skills need the same artifact.
```

Create `shared/schemas/README.md` with:

```markdown
# Shared Schemas

Store cross-skill schemas here only after more than one skill depends on the same contract.
```

Create `packages/skill-validator/README.md` with:

```markdown
# skill-validator

Shared validation notes and future code for checking skill metadata, directory shape, and packaging outputs.
```

Create `docs/authoring/new-skill.md` with:

```markdown
# Adding A New Skill

## When to create a new skill

Create a new skill when the workflow, data contract, or trigger conditions are distinct enough that stuffing them into an existing skill would blur its purpose.

## How to scaffold it

1. Copy `shared/templates/skill/` into `skills/<skill-name>/`.
2. Rename `SKILL.md.template` to `SKILL.md`.
3. Add only the references, assets, scripts, and tests that this skill needs.

## When to extract shared pieces

If only one skill needs something, keep it inside that skill.

Move code to `packages/` or non-code artifacts to `shared/` only after a second skill needs the same contract.

## Public vs maintainer-only

Put end-user skills under `skills/`.

Put repository-curation or editorial workflows under `maintainer-skills/`.
```

- [ ] **Step 4: Run the validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`  
Expected: PASS with `Authoring assets OK`.

- [ ] **Step 5: Commit**

```bash
git add shared/templates/skill shared/schemas/README.md docs/authoring/new-skill.md packages/skill-validator/README.md tests/packaging/validate-authoring-assets.ps1
git commit -m "feat: add shared authoring assets for future skills"
```

### Task 8: Document The `kb-sf6-frame-current` Packaging Boundary

**Files:**

- Create: `E:\github\SF6-skills\docs\architecture\kb-sf6-frame-current-packaging.md`
- Create: `E:\github\SF6-skills\tests\integration\validate-frame-current-boundary.ps1`

- [ ] **Step 1: Write the failing boundary-doc validation script**

```powershell
$path = 'docs/architecture/kb-sf6-frame-current-packaging.md'

if (-not (Test-Path $path)) {
  throw 'Missing frame-current packaging boundary doc'
}

$content = Get-Content $path -Raw

$requiredSections = @(
  '## Current Runtime Inputs',
  '## Packaging Options',
  '## Recommended Decision',
  '## Next Plan Trigger'
)

foreach ($section in $requiredSections) {
  if ($content -notmatch [regex]::Escape($section)) {
    throw "Missing section: $section"
  }
}

Write-Host 'Frame-current boundary doc OK'
```

- [ ] **Step 2: Run the validation script to verify it fails**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1`  
Expected: FAIL because the boundary doc does not exist yet.

- [ ] **Step 3: Write the boundary document from the current skill and data layout**

Build the doc from these inspection commands:

```powershell
Get-Content '.agents/skills/kb-sf6-frame-current/SKILL.md'
Get-Content '.agents/skills/kb-sf6-frame-current/references/export-contract.md'
Get-ChildItem 'data/exports/jp'
Get-ChildItem 'data/exports/luke'
```

Write `docs/architecture/kb-sf6-frame-current-packaging.md` with these exact sections:

```markdown
# kb-sf6-frame-current Packaging Boundary

## Current Runtime Inputs

- `snapshot_manifest.json`
- published `official_raw.*`
- published `derived_metrics.*`
- published `supercombo_enrichment.*`
- supported characters: `jp`, `luke`

## Packaging Options

1. Bundle skill-local published snapshots under `skills/kb-sf6-frame-current/assets/`
2. Generate a reduced runtime asset set during packaging
3. Keep the skill repo-local only until asset packaging is solved

## Recommended Decision

For phase 1, do not migrate this skill into the public surface until a generated runtime asset subset is defined.

The follow-up plan should compare bundled full exports versus generated reduced assets and choose one explicit packaging contract.

## Next Plan Trigger

Write the follow-up plan only after the runtime asset contract is explicit enough to answer:

- which files ship with the skill
- how those files are regenerated
- how published exports remain the final source of truth
```

- [ ] **Step 4: Run the validation script to verify it passes**

Run: `powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1`  
Expected: PASS with `Frame-current boundary doc OK`.

- [ ] **Step 5: Commit**

```bash
git add docs/architecture/kb-sf6-frame-current-packaging.md tests/integration/validate-frame-current-boundary.ps1
git commit -m "docs: capture frame-current packaging boundary"
```

## Spec Coverage Check

- Public canonical source under `skills/`: covered by Tasks 1, 2, and 3.
- Maintainer-only separation: covered by Task 5.
- Multi-agent distribution surface: covered by Task 6.
- Future new-skill onboarding and shared-layer discipline: covered by Task 7.
- `kb-sf6-frame-current` runtime-boundary investigation: covered by Task 8.
- `.agents/skills` as compatibility output rather than canonical source: covered by Task 4.

## Placeholder Scan

The only intentional deferral is the actual migration of `kb-sf6-frame-current`, which is explicitly excluded from this plan and replaced with a concrete boundary-document task in Task 8.

## Type And Naming Consistency

- Public skills always live under `skills/<skill-name>/`.
- Maintainer-only workflows always live under `maintainer-skills/<skill-name>/`.
- Repo-local compatibility mirror always targets `.agents/skills/`.
- Cross-agent distribution docs always live under `docs/distribution/`.
