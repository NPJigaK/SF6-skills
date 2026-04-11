# Repo Structure Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align repository docs, authoring guidance, and the minimum local validators with the new repo structure contract so the repo consistently enforces "independent skill first, shared later" without adding unnecessary complexity.

**Architecture:** Keep the implementation intentionally small. Update the discovery docs so the top-level structure is explicit, update the authoring/template docs so new skills follow the contract by default, and strengthen only the existing minimum validators (`validate-layout.ps1` and `validate-authoring-assets.ps1`) rather than introducing a new test stack.

**Tech Stack:** Markdown, PowerShell validators, existing repo docs and templates

---

## Planned File Map

This implementation modifies existing files only.

**Modify:**

- `E:\github\SF6-skills\.worktrees\repo-structure-contract\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\architecture\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\packages\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\skills\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\maintainer-skills\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\authoring\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\authoring\new-skill.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\templates\skill\README.md`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\templates\skill\SKILL.md.template`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-layout.ps1`
- `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-authoring-assets.ps1`

## Task 1: Define The Failing Repo Structure Contract Validators

**Files:**

- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-layout.ps1`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-authoring-assets.ps1`

- [ ] **Step 1: Replace `tests/packaging/validate-layout.ps1` with the stricter structure contract validator**

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredDirectories = @(
  'skills',
  'maintainer-skills',
  '.agents',
  '.agents/skills',
  'packages',
  'packages/skill-installers',
  'packages/skill-validator',
  'packages/skill-packaging',
  'shared',
  'shared/templates',
  'shared/templates/skill',
  'shared/schemas',
  'docs/architecture',
  'docs/authoring',
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

$missingDirectories = foreach ($relativePath in $requiredDirectories) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
    $relativePath
  }
}

if (@($missingDirectories).Count -gt 0) {
  throw "Missing required paths: $($missingDirectories -join ', ')"
}

$requiredFiles = @(
  'README.md',
  'docs/architecture/README.md',
  'docs/architecture/repo-structure-contract.md',
  'packages/README.md',
  'shared/README.md',
  'skills/README.md',
  'maintainer-skills/README.md'
)

$missingFiles = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if (@($missingFiles).Count -gt 0) {
  throw "Missing required files: $($missingFiles -join ', ')"
}

$contentChecks = @(
  @{
    Path = 'README.md'
    MustContain = @(
      '## Repository Structure',
      '## Repo Structure Contract',
      '[repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)',
      '`.agents/skills/`'
    )
  },
  @{
    Path = 'docs/architecture/README.md'
    MustContain = @(
      'repo-structure-contract.md',
      'kb-sf6-frame-current-packaging.md'
    )
  },
  @{
    Path = 'packages/README.md'
    MustContain = @(
      'Use `packages/` only after a second real consumer exists.'
    )
  },
  @{
    Path = 'shared/README.md'
    MustContain = @(
      'Use `shared/` only after a second real consumer exists.'
    )
  },
  @{
    Path = 'skills/README.md'
    MustContain = @(
      'Each direct child under `skills/` is an independent public skill unit.',
      'Required per skill: `SKILL.md`.',
      'Optional per skill: `references/`, `assets/`, `agents/`.'
    )
  },
  @{
    Path = 'maintainer-skills/README.md'
    MustContain = @(
      'These skills are repository-only workflows.',
      'They are not public distribution units.'
    )
  }
)

foreach ($check in $contentChecks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw
  foreach ($needle in $check.MustContain) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$($check.Path) missing: $needle"
    }
  }
}

function Get-DirectChildDirectoryNames {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Root
  )

  return @(
    Get-ChildItem -LiteralPath $Root -Directory |
      Sort-Object Name |
      ForEach-Object { $_.Name }
  )
}

$publicSkillsRoot = Join-Path $repoRoot 'skills'
$publicSkillNames = Get-DirectChildDirectoryNames -Root $publicSkillsRoot

foreach ($skillName in $publicSkillNames) {
  $skillManifest = Join-Path $publicSkillsRoot (Join-Path $skillName 'SKILL.md')
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Public skill missing SKILL.md: skills/$skillName"
  }
}

$maintainerSkillsRoot = Join-Path $repoRoot 'maintainer-skills'
$maintainerSkillNames = Get-DirectChildDirectoryNames -Root $maintainerSkillsRoot

foreach ($skillName in $maintainerSkillNames) {
  $skillManifest = Join-Path $maintainerSkillsRoot (Join-Path $skillName 'SKILL.md')
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Maintainer skill missing SKILL.md: maintainer-skills/$skillName"
  }
}

$dogfoodRoot = Join-Path $repoRoot '.agents/skills'
$dogfoodSkillNames = Get-DirectChildDirectoryNames -Root $dogfoodRoot

if (Compare-Object ($publicSkillNames | Sort-Object) ($dogfoodSkillNames | Sort-Object)) {
  throw 'Dogfood mirror top-level skill inventory does not match skills/'
}

Write-Host 'Layout OK'
```

- [ ] **Step 2: Replace `tests/packaging/validate-authoring-assets.ps1` with the stricter authoring contract validator**

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredFiles = @(
  'shared/templates/skill/SKILL.md.template'
  'shared/templates/skill/README.md'
  'shared/schemas/README.md'
  'docs/authoring/README.md'
  'docs/authoring/new-skill.md'
  'packages/skill-validator/README.md'
)

$missing = foreach ($relativePath in $requiredFiles) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    $relativePath
  }
}

if (@($missing).Count -gt 0) {
  throw "Missing authoring assets: $($missing -join ', ')"
}

$templatePath = Join-Path $repoRoot 'shared/templates/skill/SKILL.md.template'
$template = Get-Content -LiteralPath $templatePath -Raw

if (-not $template.StartsWith('---')) {
  throw 'shared/templates/skill/SKILL.md.template must begin with frontmatter (`---`)'
}

$checks = @(
  @{
    Path = 'shared/templates/skill/SKILL.md.template'
    MustContain = @(
      '## Purpose',
      '## When To Use',
      '## Required Inputs',
      '## Workflow',
      '## Constraints',
      'Do not depend on another skill directory.',
      'Move shared artifacts out only after a second real consumer exists.'
    )
  },
  @{
    Path = 'shared/templates/skill/README.md'
    MustContain = @(
      'Required:',
      'Optional:',
      'Keep skill-specific references, assets, and agent metadata inside the skill directory until a second skill needs the same artifact.',
      'Prefer repo-level tests only when a boundary contract needs protection.'
    )
  },
  @{
    Path = 'shared/schemas/README.md'
    MustContain = @(
      'cross-skill schemas here only after more than one skill depends on the same contract'
    )
  },
  @{
    Path = 'packages/skill-validator/README.md'
    MustContain = @(
      'checking skill metadata, directory shape, and packaging outputs'
    )
  },
  @{
    Path = 'docs/authoring/README.md'
    MustContain = @(
      'independent skill first',
      'shared later',
      'local validator first',
      'new-skill.md'
    )
  },
  @{
    Path = 'docs/authoring/new-skill.md'
    MustContain = @(
      '## When to create a new skill',
      '## How to scaffold it',
      '## When to extract shared pieces',
      '## Public vs maintainer-only',
      '## What not to add to a public skill',
      'Add only the references, assets, and agent metadata that this skill needs.',
      'If a repo-level contract really needs protection, add the minimum validator under `tests/`.',
      'Do not add dependencies on another skill, ingestion code, installer or bundle machinery, or raw/review artifacts to a public skill.'
    )
  }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw
  foreach ($needle in $check.MustContain) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$($check.Path) missing: $needle"
    }
  }
}

Write-Host 'Authoring assets OK'
```

- [ ] **Step 3: Run both validators to verify the current docs fail the new contract**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1
```

Expected:

- `validate-layout.ps1` fails because the top-level README files do not yet contain the new repo-structure-contract wording.
- `validate-authoring-assets.ps1` fails because the authoring docs and template still describe the older skill-local scripts/tests guidance.

- [ ] **Step 4: Commit the failing contract tests**

```bash
git add tests/packaging/validate-layout.ps1 tests/packaging/validate-authoring-assets.ps1
git commit -m "test: define repo structure contract"
```

## Task 2: Update Top-Level Structure Discovery Docs

**Files:**

- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\architecture\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\packages\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\skills\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\maintainer-skills\README.md`

- [ ] **Step 1: Replace `README.md` with the repo-structure-first version**

```markdown
# SF6 Skills Repo

SF6 の concept-first knowledge と、supported baseline characters `jp` / `luke` の v3 published frame-data exports を管理するリポジトリです。

## Supported Baseline Characters

- `jp`
- `luke`

## Repository Structure

- public skills
  - `skills/<skill-name>/`
  - canonical public source
- maintainer-only skills
  - `maintainer-skills/<skill-name>/`
  - repository-only workflows
- repo-local dogfooding mirror
  - `.agents/skills/<skill-name>/`
  - exact top-level mirror of `skills/`
  - derived, never canonical source
- shared executable infrastructure
  - `packages/`
- shared non-code artifacts
  - `shared/`
- repository docs and validators
  - `docs/`
  - `tests/`
  - `scripts/`
- data production code
  - `ingest/frame_data/`
- published current-fact artifacts
  - `data/exports/<character_slug>/`

## Repo Structure Contract

- simple, explicit structure beats flexible abstraction
- new public skills start as independent units under `skills/`
- move artifacts to `packages/` or `shared/` only after a second real consumer exists
- local PowerShell validators are the canonical structure guard

Detailed contract:

- [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)

## Not Durable Surface

- `.git/`
  - repository metadata
  - durable checked-in artifact surface ではない
- `data/normalized/<character_slug>/<run_id>/`
  - run-local audit state
  - durable checked-in artifact surface ではない
- `__pycache__/`, `.pytest_cache/`
  - local / generated state
- review zip artifacts
  - `SF6skill.zip` のような shared zip artifact を含む
  - durable checked-in artifact surface ではない

## Current Fact Policy

- current fact は `data/exports/<character_slug>/snapshot_manifest.json` を entrypoint に確認する
- `publication_state = available` の dataset だけを current-fact lookup に使う
- repo-level canonical published data は `data/exports/<character_slug>/...`
- public distributed `skills/kb-sf6-frame-current` は generated packaged runtime assets `skills/kb-sf6-frame-current/assets/published/<character_slug>/...` を read し、これらは `data/exports/<character_slug>/...` から生成される
- lookup order は `official_raw` -> `derived_metrics` -> `supercombo_enrichment`
- `official_raw` を canonical source として先に読む
- `derived_metrics` は official-only の機械計算結果として使う
- `supercombo_enrichment` は supplemental join のみで、official を上書きしない
- `*_manual_review.*`, `data/raw/...`, `data/normalized/...` は通常の current-fact 回答の最終根拠にしない

## Data Layout

- `data/exports/<character_slug>/`
  - shared published surface
  - `snapshot_manifest.json`
  - `official_raw.*`
  - `derived_metrics.*`
  - `supercombo_enrichment.*`
  - `*_manual_review.*`
- `data/raw/<source>/<character_slug>/<snapshot_id>/`
  - currently published datasets を裏づける minimal backing raw snapshots

詳説は `ingest/frame_data/README.md` を参照してください。
```

- [ ] **Step 2: Replace the top-level boundary README files**

```markdown
# Architecture Docs

Repository-level architecture notes and dependency-boundary decisions.

Primary entrypoints:

- `repo-structure-contract.md`
- `kb-sf6-frame-current-packaging.md`
```

```markdown
# Packages

Shared executable infrastructure for packaging, validation, and installers.

Use `packages/` only after a second real consumer exists.

Keep skill-specific logic inside its skill directory until shared demand is real.
```

```markdown
# Shared

Shared non-code artifacts such as templates, schemas, and stable vocabulary.

Use `shared/` only after a second real consumer exists.
```

```markdown
# Public Skills

Canonical public source for distributed skills lives here.

Each direct child under `skills/` is an independent public skill unit.

Required per skill: `SKILL.md`.

Optional per skill: `references/`, `assets/`, `agents/`.

`.agents/skills/` is a dogfooding mirror, not the canonical source.
```

```markdown
# Maintainer Skills

Repository-only workflows live here.

These skills are repository-only workflows.

They are not public distribution units.
```

Apply the blocks above to these files:

- `docs/architecture/README.md`
- `packages/README.md`
- `shared/README.md`
- `skills/README.md`
- `maintainer-skills/README.md`

- [ ] **Step 3: Run the structure validators**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Layout OK`
- `Docs OK`

- [ ] **Step 4: Commit the top-level structure docs**

```bash
git add README.md docs/architecture/README.md packages/README.md shared/README.md skills/README.md maintainer-skills/README.md
git commit -m "docs: align repo structure discovery docs"
```

## Task 3: Align Authoring Docs And Skill Template

**Files:**

- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\authoring\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\authoring\new-skill.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\templates\skill\README.md`
- Modify: `E:\github\SF6-skills\.worktrees\repo-structure-contract\shared\templates\skill\SKILL.md.template`

- [ ] **Step 1: Replace `docs/authoring/README.md` and `docs/authoring/new-skill.md`**

```markdown
# Authoring Docs

How to add and maintain skills in this repository.

Authoring principles:

- independent skill first
- shared later
- local validator first

Start here:

- `new-skill.md`
```

```markdown
# Adding A New Skill

## When to create a new skill

Create a new skill when the workflow, data contract, or trigger conditions are distinct enough that stuffing them into an existing skill would blur its purpose.

## How to scaffold it

1. Copy `shared/templates/skill/` into `skills/<skill-name>/`.
2. Rename `SKILL.md.template` to `SKILL.md`.
3. Add only the references, assets, and agent metadata that this skill needs.
4. Keep skill-specific artifacts local to the skill directory.
5. If a repo-level contract really needs protection, add the minimum validator under `tests/`.

## When to extract shared pieces

If only one skill needs something, keep it inside that skill.

Move executable or code-like infrastructure to `packages/` only after a second skill needs the same contract.

Move non-code artifacts to `shared/` only after a second skill needs the same contract.

## Public vs maintainer-only

Put end-user skills under `skills/`.

Put repository-curation or editorial workflows under `maintainer-skills/`.

`.agents/skills/` is a dogfooding mirror, not a source surface.

## What not to add to a public skill

Do not add dependencies on another skill, ingestion code, installer or bundle machinery, or raw/review artifacts to a public skill.
```

Apply the blocks above to:

- `docs/authoring/README.md`
- `docs/authoring/new-skill.md`

- [ ] **Step 2: Replace `shared/templates/skill/README.md` and `shared/templates/skill/SKILL.md.template`**

```markdown
# Skill Template

Use this directory as the starting point for a new public skill under `skills/<skill-name>/`.

Required:

- `SKILL.md`

Optional:

- `references/`
- `assets/`
- `agents/`

Keep skill-specific references, assets, and agent metadata inside the skill directory until a second skill needs the same artifact.

Prefer repo-level tests only when a boundary contract needs protection.

Treat this README as starter guidance for the generated skill, then replace or adapt it with skill-specific documentation as needed.
```

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

1. Resolve scope and confirm this skill owns the request.
2. Read the minimum supporting references or assets.
3. Produce the answer or artifact.
4. If the request crosses this skill's boundary, stop and hand off.

## Constraints

- Do not depend on another skill directory.
- Keep outputs inside this skill's purpose.
- Move shared artifacts out only after a second real consumer exists.
```

Apply the blocks above to:

- `shared/templates/skill/README.md`
- `shared/templates/skill/SKILL.md.template`

- [ ] **Step 3: Run the authoring and docs validators**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Authoring assets OK`
- `Docs OK`

- [ ] **Step 4: Commit the authoring contract updates**

```bash
git add docs/authoring/README.md docs/authoring/new-skill.md shared/templates/skill/README.md shared/templates/skill/SKILL.md.template
git commit -m "docs: align skill authoring contract"
```

## Task 4: Run Final Contract Verification

**Files:**

- Verify only: `E:\github\SF6-skills\.worktrees\repo-structure-contract\README.md`
- Verify only: `E:\github\SF6-skills\.worktrees\repo-structure-contract\docs\architecture\repo-structure-contract.md`
- Verify only: `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-layout.ps1`
- Verify only: `E:\github\SF6-skills\.worktrees\repo-structure-contract\tests\packaging\validate-authoring-assets.ps1`

- [ ] **Step 1: Run the structure contract validators**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Layout OK`
- `Authoring assets OK`
- `Docs OK`

- [ ] **Step 2: Run existing skill-surface sanity checks**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
```

Expected:

- `kb-sf6-core public copy OK`
- `kb-sf6-frame-current public shell OK`
- `Dogfood mirror OK`
- `Distribution surface OK`

- [ ] **Step 3: Confirm the working tree is clean**

Run:

```powershell
git status --short
```

Expected: no tracked file changes.

## Spec Coverage Check

- top-level directory boundaries: covered by Tasks 1 and 2
- independent public skill unit contract: covered by Tasks 1 and 3
- authoring guidance for `shared later`: covered by Task 3
- local-validator-first policy: covered by Tasks 1 and 4
- keep the test surface minimal: covered by reusing `validate-layout.ps1` and `validate-authoring-assets.ps1` instead of adding a new validator stack

## Placeholder Scan

- No `TODO`, `TBD`, or deferred code markers remain in task steps.
- All commands are explicit and include expected outcomes.
- Every code-changing step includes concrete target content.

## Type And Naming Consistency

- canonical public root is always `skills/`
- maintainer-only root is always `maintainer-skills/`
- repo-local mirror root is always `.agents/skills/`
- shared executable root is always `packages/`
- shared non-code root is always `shared/`
- the minimum public skill required file is always `SKILL.md`
