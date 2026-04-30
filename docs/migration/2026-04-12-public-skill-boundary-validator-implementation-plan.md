# Public Skill Boundary Validator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one lightweight validator that keeps public skills independent from other skill directories without freezing a rigid folder shape.

**Architecture:** Keep the implementation small and ecosystem-aligned. Add a single integration validator for public-skill boundary checks, add one regression harness that exercises valid and invalid fixture repos, and document the validator as part of the normal local verification set. Do not add a broader validation framework or new top-level skill-shape restrictions.

**Tech Stack:** PowerShell validators, Markdown docs, existing repo validation scripts

---

## Planned File Map

**Create:**

- `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\test-public-skill-boundary-validator.ps1`
- `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\validate-public-skill-boundaries.ps1`

**Modify:**

- `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\docs\architecture\repo-structure-contract.md`
- `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\docs\testing\README.md`

## Task 1: Add A Failing Boundary Validator Harness

**Files:**

- Create: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\test-public-skill-boundary-validator.ps1`

- [ ] **Step 1: Create the regression harness script**

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$validatorPath = Join-Path $repoRoot 'tests\integration\validate-public-skill-boundaries.ps1'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('sf6-public-skill-boundary-' + [guid]::NewGuid().ToString('N'))

function New-FixtureRepo {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Root,

    [Parameter(Mandatory = $true)]
    [hashtable]$Skills
  )

  $skillsRoot = Join-Path $Root 'skills'
  New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null

  foreach ($entry in $Skills.GetEnumerator()) {
    $skillRoot = Join-Path $skillsRoot $entry.Key
    New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null

    foreach ($file in $entry.Value.GetEnumerator()) {
      $fullPath = Join-Path $skillRoot $file.Key
      $parent = Split-Path -Parent $fullPath
      if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
      }
      Set-Content -LiteralPath $fullPath -Value $file.Value
    }
  }
}

function Assert-Passes {
  param(
    [Parameter(Mandatory = $true)]
    [string]$FixtureRoot
  )

  try {
    & $validatorPath -RepoRoot $FixtureRoot | Out-Null
  } catch {
    throw "Expected pass for fixture '$FixtureRoot', but validator failed: $($_.Exception.Message)"
  }
}

function Assert-FailsLike {
  param(
    [Parameter(Mandatory = $true)]
    [string]$FixtureRoot,

    [Parameter(Mandatory = $true)]
    [string]$Pattern
  )

  try {
    & $validatorPath -RepoRoot $FixtureRoot | Out-Null
    throw "Expected failure for fixture '$FixtureRoot'"
  } catch {
    if ($_.Exception.Message -notmatch $Pattern) {
      throw "Unexpected failure for fixture '$FixtureRoot': $($_.Exception.Message)"
    }
  }
}

try {
  $validRoot = Join-Path $tempRoot 'valid'
  New-FixtureRepo -Root $validRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Use together with beta when needed.
---

Read `references/local.md`.
'@
      'references/local.md' = 'local reference'
    }
    'beta' = @{
      'SKILL.md' = @'
---
name: beta
description: Standalone skill.
---

Use together with alpha when needed.
'@
    }
  }
  Assert-Passes -FixtureRoot $validRoot

  $missingManifestRoot = Join-Path $tempRoot 'missing-manifest'
  New-FixtureRepo -Root $missingManifestRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Valid skill.
---
'@
    }
    'beta' = @{
      'notes.md' = 'missing manifest'
    }
  }
  Assert-FailsLike -FixtureRoot $missingManifestRoot -Pattern 'Public skill missing SKILL\.md: skills/beta'

  $crossSkillRoot = Join-Path $tempRoot 'cross-skill-path'
  New-FixtureRepo -Root $crossSkillRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `skills/beta/references/guide.md` before answering.
'@
    }
    'beta' = @{
      'SKILL.md' = @'
---
name: beta
description: Standalone skill.
---
'@
    }
  }
  Assert-FailsLike -FixtureRoot $crossSkillRoot -Pattern 'skills/alpha/SKILL\.md references public skill directory skills/beta/'

  $dogfoodPathRoot = Join-Path $tempRoot 'dogfood-path'
  New-FixtureRepo -Root $dogfoodPathRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `.agents/skills/beta/SKILL.md` before answering.
'@
    }
    'beta' = @{
      'SKILL.md' = @'
---
name: beta
description: Standalone skill.
---
'@
    }
  }
  Assert-FailsLike -FixtureRoot $dogfoodPathRoot -Pattern 'skills/alpha/SKILL\.md references repo-local dogfood skill directory \.agents/skills/beta/'

  $siblingTraversalRoot = Join-Path $tempRoot 'sibling-traversal'
  New-FixtureRepo -Root $siblingTraversalRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `../beta/references/guide.md` before answering.
'@
    }
    'beta' = @{
      'SKILL.md' = @'
---
name: beta
description: Standalone skill.
---
'@
    }
  }
  Assert-FailsLike -FixtureRoot $siblingTraversalRoot -Pattern 'skills/alpha/SKILL\.md references sibling skill directory traversal \.\./beta/'
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}

Write-Host 'Public skill boundary validator harness OK'
```

- [ ] **Step 2: Run the harness before the validator exists**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/test-public-skill-boundary-validator.ps1
```

Expected:

- FAIL with an invocation error that mentions `validate-public-skill-boundaries.ps1`, because the validator file does not exist yet.

- [ ] **Step 3: Commit the failing harness**

```bash
git add tests/integration/test-public-skill-boundary-validator.ps1
git commit -m "test: add public skill boundary validator harness"
```

## Task 2: Implement The Boundary Validator And Document It

**Files:**

- Create: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\validate-public-skill-boundaries.ps1`
- Modify: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\docs\architecture\repo-structure-contract.md`
- Modify: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\docs\testing\README.md`

- [ ] **Step 1: Create the validator script**

```powershell
param(
  [string]$RepoRoot = (Join-Path $PSScriptRoot '..\..')
)

Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$skillsRoot = Join-Path $repoRoot 'skills'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
  throw "Missing public skills root: $skillsRoot"
}

$skillDirs = @(
  Get-ChildItem -LiteralPath $skillsRoot -Directory |
    Sort-Object Name
)

$skillNames = @($skillDirs | ForEach-Object { $_.Name })

function Assert-SkillManifest {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [Parameter(Mandatory = $true)]
    [string]$SkillRoot
  )

  $skillManifest = Join-Path $SkillRoot 'SKILL.md'
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Public skill missing SKILL.md: skills/$SkillName"
  }

  return $skillManifest
}

function Assert-NoCrossSkillDirectoryDependency {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [Parameter(Mandatory = $true)]
    [string]$SkillManifest,

    [Parameter(Mandatory = $true)]
    [string[]]$AllSkillNames
  )

  $content = Get-Content -LiteralPath $SkillManifest -Raw
  $otherSkillNames = @($AllSkillNames | Where-Object { $_ -ne $SkillName })

  foreach ($otherSkillName in $otherSkillNames) {
    $escaped = [regex]::Escape($otherSkillName)
    $checks = @(
      @{
        Label = 'public skill directory'
        Pattern = "(?im)(?:^|[^A-Za-z0-9_.-])skills/$escaped/"
        Example = "skills/$otherSkillName/"
      }
      @{
        Label = 'repo-local dogfood skill directory'
        Pattern = "(?im)(?:^|[^A-Za-z0-9_.-])\.agents/skills/$escaped/"
        Example = ".agents/skills/$otherSkillName/"
      }
      @{
        Label = 'sibling skill directory traversal'
        Pattern = "(?im)(?:^|[^A-Za-z0-9_.-])(?:\.\./)+$escaped/"
        Example = "../$otherSkillName/"
      }
    )

    foreach ($check in $checks) {
      if ($content -match $check.Pattern) {
        throw "Public skill boundary violation: skills/$SkillName/SKILL.md references $($check.Label) $($check.Example)"
      }
    }
  }
}

foreach ($skillDir in $skillDirs) {
  $skillManifest = Assert-SkillManifest -SkillName $skillDir.Name -SkillRoot $skillDir.FullName
  Assert-NoCrossSkillDirectoryDependency -SkillName $skillDir.Name -SkillManifest $skillManifest -AllSkillNames $skillNames
}

Write-Host 'Public skill boundaries OK'
```

- [ ] **Step 2: Update the contract and testing docs**

Replace the `## Validator Policy` bullet list in `docs/architecture/repo-structure-contract.md` with:

```markdown
## Validator Policy

This repository keeps only the minimum validator set needed to protect structure:

- layout contract
- public skill dependency boundary checks
- public skill location and mirror integrity
- distribution surface boundary checks
- release bundle boundary checks
- packaged runtime asset boundary checks where a skill needs packaged data

The repository does not aim to exhaustively test every wording detail of every skill.
Tests should exist only when a broken boundary would cause real confusion or bad distribution behavior.
```

Replace `docs/testing/README.md` with:

```markdown
# Testing Docs

How to verify layout, packaging, installation, and public-skill boundaries.

Core local verification set:

- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`
```

- [ ] **Step 3: Run the harness and the directly affected validators**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/test-public-skill-boundary-validator.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected:

- `Public skill boundary validator harness OK`
- `Public skill boundaries OK`
- `Layout OK`
- `Docs OK`

- [ ] **Step 4: Commit the validator and doc updates**

```bash
git add tests/integration/test-public-skill-boundary-validator.ps1 tests/integration/validate-public-skill-boundaries.ps1 docs/architecture/repo-structure-contract.md docs/testing/README.md
git commit -m "test: add public skill boundary validator"
```

## Task 3: Run Final Verification

**Files:**

- Verify only: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\test-public-skill-boundary-validator.ps1`
- Verify only: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\tests\integration\validate-public-skill-boundaries.ps1`
- Verify only: `E:\github\SF6-skills\.worktrees\public-skill-boundary-validator\docs\testing\README.md`

- [ ] **Step 1: Run the full local verification set**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/test-public-skill-boundary-validator.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
```

Expected:

- `Public skill boundary validator harness OK`
- `Public skill boundaries OK`
- `Layout OK`
- `Authoring assets OK`
- `Docs OK`
- `kb-sf6-core public copy OK`
- `kb-sf6-frame-current public shell OK`
- `Dogfood mirror OK`
- `Distribution surface OK`

- [ ] **Step 2: Confirm the working tree is clean**

Run:

```powershell
git status --short
```

Expected: no tracked file changes.

## Spec Coverage Check

- lightweight validator only: covered by Task 2
- no rigid public-skill top-level shape restriction: covered by Task 2 and the lack of folder-shape checks in the validator code
- explicit path dependency rejection only: covered by Task 2
- allow bare skill-name mentions: covered by Task 1 valid fixture and Task 2 path-based matching rules
- add validator to the normal local verification set: covered by Task 2 docs update and Task 3 full verification

## Placeholder Scan

- No `TODO`, `TBD`, or deferred implementation markers remain.
- All code-writing steps contain exact target code.
- All verification steps include explicit commands and expected success signals.

## Type And Naming Consistency

- validator path is always `tests/integration/validate-public-skill-boundaries.ps1`
- harness path is always `tests/integration/test-public-skill-boundary-validator.ps1`
- success line is always `Public skill boundaries OK`
- public-skill root is always `skills/`
- forbidden dependency target is always another skill directory, not a bare skill-name mention
