# Root README Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the repository-root `README.md` into a superpowers-style onboarding document that still states the SF6 current-fact trust model clearly and accurately.

**Architecture:** Tighten the README contract first by updating the existing documentation validators to require the new section order and trust-model references. Then replace the root `README.md` with the new onboarding-first copy, and finish by running broader layout and distribution-surface validators so the rewrite stays aligned with the rest of the repository contract.

**Tech Stack:** Markdown, PowerShell 7, existing validators `tests/packaging/validate-doc-links.ps1`, `tests/packaging/validate-layout.ps1`, and `tests/install/validate-distribution-surface.ps1`.

---

## File Map

- Modify: `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- Modify: `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`
- Modify: `E:\github\SF6-skills\README.md`

### Task 1: Turn The New README Contract Red

**Files:**
- Modify: `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- Modify: `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`
- Test: `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- Test: `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`

- [ ] **Step 1: Replace `validate-doc-links.ps1` with the new README-aware documentation contract**

Replace `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1` with:

```powershell
Set-StrictMode -Version Latest

function New-Text {
  param(
    [Parameter(Mandatory = $true)]
    [int[]]$CodePoints
  )

  -join ($CodePoints | ForEach-Object { [char]$_ })
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

$AnswerLabelsHeading = New-Text 35, 35, 32, 0x56DE, 0x7B54, 0x30E9, 0x30D9, 0x30EB
$LabelVerified = New-Text 91, 0x691C, 0x8A3C, 0x6E08, 0x307F, 93
$LabelConcept = New-Text 91, 0x6982, 0x5FF5, 0x306E, 0x307F, 93
$LabelPending = New-Text 91, 0x4FDD, 0x7559, 93

$checks = @(
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustContain = 'skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'AGENTS.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'AGENTS.md'; MustContain = '`skills/` is the canonical public source.' },
  @{ Path = 'AGENTS.md'; MustContain = '`local/` is the personal trial workspace for trying distributed skills.' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/sync-knowledge/' },
  @{ Path = 'AGENTS.md'; MustContain = 'maintainer-skills/update-frame-data/' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'snapshot_manifest.json' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'publication_state = available' },
  @{ Path = 'AGENTS.md'; MustNotContain = 'lookup order は `official_raw` -> `derived_metrics` -> `supercombo_enrichment`' },
  @{ Path = 'AGENTS.md'; MustNotContain = $AnswerLabelsHeading },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelVerified },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelConcept },
  @{ Path = 'AGENTS.md'; MustNotContain = $LabelPending },
  @{ Path = 'skills/kb-sf6-core/SKILL.md'; MustContain = $LabelConcept },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = $LabelConcept },
  @{ Path = 'skills/kb-sf6-core/references/SOURCE_POLICY.md'; MustContain = 'kb-sf6-frame-current' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = $LabelVerified },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = $LabelPending },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'snapshot_manifest.json' },
  @{ Path = 'skills/kb-sf6-frame-current/SKILL.md'; MustContain = 'Do not use T3 alone as the final authority when packaged official data exists.' },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = $LabelVerified },
  @{ Path = 'skills/kb-sf6-frame-current/references/export-contract.md'; MustContain = $LabelPending },
  @{ Path = 'skills/video-analysis-core/SKILL.md'; MustContain = "Do not label observations as ``$LabelVerified`` current fact." },
  @{ Path = 'README.md'; MustContain = '# SF6 Skills' },
  @{ Path = 'README.md'; MustContain = '## How it works' },
  @{ Path = 'README.md'; MustContain = '## Installation' },
  @{ Path = 'README.md'; MustContain = '## Verify installation' },
  @{ Path = 'README.md'; MustContain = '## Basic usage' },
  @{ Path = 'README.md'; MustContain = '## Current fact policy' },
  @{ Path = 'README.md'; MustContain = '## What''s inside' },
  @{ Path = 'README.md'; MustContain = '## Contributing' },
  @{ Path = 'README.md'; MustContain = '## Updating' },
  @{ Path = 'README.md'; MustContain = 'The agent can usually choose a matching skill automatically.' },
  @{ Path = 'README.md'; MustContain = 'You can also mention a skill by name explicitly.' },
  @{ Path = 'README.md'; MustContain = '.codex/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.claude-plugin/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.cursor-plugin/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '.opencode/INSTALL.md' },
  @{ Path = 'README.md'; MustContain = '`kb-sf6-core`' },
  @{ Path = 'README.md'; MustContain = '`kb-sf6-frame-current`' },
  @{ Path = 'README.md'; MustContain = 'data/exports/<character_slug>/snapshot_manifest.json' },
  @{ Path = 'README.md'; MustContain = 'publication_state = available' },
  @{ Path = 'README.md'; MustContain = 'shared/roster/current-character-roster.json' },
  @{ Path = 'README.md'; MustContain = '`official_raw` is canonical' },
  @{ Path = 'README.md'; MustContain = '`derived_metrics` is official-only computed output' },
  @{ Path = 'README.md'; MustContain = '`supercombo_enrichment` is supplemental only' },
  @{ Path = 'README.md'; MustContain = '`data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface' },
  @{ Path = 'README.md'; MustContain = '[ingest/frame_data/README.md](./ingest/frame_data/README.md)' },
  @{ Path = 'README.md'; MustContain = '[repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'README.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = '`local/` is the personal trial workspace.' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustContain = 'bootstrap-local-trial-workspace.ps1' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'docs/distribution/local-trial-workspace.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'docs/testing/README.md'; MustContain = 'validate-local-trial-surface.ps1' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'docs/testing/README.md'; MustNotContain = '.agents/skills/video-analysis-core/' },
  @{ Path = 'skills/README.md'; MustContain = 'Canonical public source for distributed skills lives here.' },
  @{ Path = 'skills/README.md'; MustContain = 'Runtime guidance belongs in each skill''s `SKILL.md` and local references.' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/kb-sf6-core/' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/kb-sf6-frame-current/' },
  @{ Path = 'skills/README.md'; MustNotContain = '.agents/skills/video-analysis-core/' }
)

foreach ($check in $checks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw -Encoding UTF8 -ErrorAction Stop
  if ($check.ContainsKey('MustContain') -and $content -notmatch [regex]::Escape($check.MustContain)) {
    throw "$($check.Path) missing: $($check.MustContain)"
  }
  if ($check.ContainsKey('MustNotContain') -and $content -match [regex]::Escape($check.MustNotContain)) {
    throw "$($check.Path) still contains: $($check.MustNotContain)"
  }
}

Write-Host 'Docs OK'
```

- [ ] **Step 2: Replace `validate-layout.ps1` so the coarse README layout contract matches the new section order**

Replace `E:\github\SF6-skills\tests\packaging\validate-layout.ps1` with:

```powershell
Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$requiredDirectories = @(
  'skills',
  'maintainer-skills',
  'local',
  'local/.codex',
  'local/.agents',
  'packages',
  'packages/skill-installers',
  'packages/skill-validator',
  'packages/skill-packaging',
  'shared',
  'shared/templates',
  'shared/templates/skill',
  'shared/schemas',
  'ingest',
  'data',
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

$contentChecks = @(
  @{
    Path = 'README.md'
    MustContain = @(
      '## Installation',
      '## Current fact policy',
      '## What''s inside',
      '[repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)',
      '[ingest/frame_data/README.md](./ingest/frame_data/README.md)',
      '`local/`'
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

$validationIssues = @()

foreach ($check in $contentChecks) {
  $content = Get-Content -LiteralPath (Join-Path $repoRoot $check.Path) -Raw
  foreach ($needle in $check.MustContain) {
    if ($content -notmatch [regex]::Escape($needle)) {
      $validationIssues += "$($check.Path) missing: $needle"
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

$legacyDogfoodRoot = Join-Path $repoRoot '.agents'

$missingDirectories = foreach ($relativePath in $requiredDirectories) {
  $fullPath = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
    $relativePath
  }
}

if (@($missingDirectories).Count -gt 0) {
  $validationIssues += "Missing required paths: $($missingDirectories -join ', ')"
}

if (@($missingFiles).Count -gt 0) {
  $validationIssues += "Missing required files: $($missingFiles -join ', ')"
}

if (Test-Path -LiteralPath $legacyDogfoodRoot -PathType Container) {
  $validationIssues += 'Repo-root .agents must not exist'
}

if (@($validationIssues).Count -gt 0) {
  throw ($validationIssues -join '; ')
}

Write-Host 'Layout OK'
```

- [ ] **Step 3: Run the documentation validators and verify the repo is red for the new README contract**

Run:

```powershell
pwsh -File tests/packaging/validate-doc-links.ps1
pwsh -File tests/packaging/validate-layout.ps1
```

Expected:
- the first command FAILS with `README.md missing: # SF6 Skills`
- the second command FAILS with `README.md missing: ## Installation`

- [ ] **Step 4: Commit the red validator changes**

```bash
git add tests/packaging/validate-doc-links.ps1 tests/packaging/validate-layout.ps1
git commit -m "test: require new root README contract"
```

### Task 2: Rewrite The Root README To Match The Approved Spec

**Files:**
- Modify: `E:\github\SF6-skills\README.md`
- Test: `E:\github\SF6-skills\tests\packaging\validate-doc-links.ps1`
- Test: `E:\github\SF6-skills\tests\packaging\validate-layout.ps1`

- [ ] **Step 1: Replace the root `README.md` with the new onboarding-first document**

Replace `E:\github\SF6-skills\README.md` with:

```markdown
# SF6 Skills

SF6 Skills is a repository of concept-first Street Fighter 6 knowledge and published current-fact surfaces for agent workflows. It distributes public skills from `skills/`, keeps current roster facts grounded in published exports, and exposes install front doors for Codex, Claude, Cursor, and OpenCode.

## How it works

After installation, this repo exposes SF6 knowledge as agent-readable skills. The agent can usually choose a matching skill automatically. You can also mention a skill by name explicitly.

Use `kb-sf6-core` for stable concepts and terminology that should not depend on the current patch. Use `kb-sf6-frame-current` when the task needs exact current values for supported current roster characters. Use `video-analysis-core` for observation-first video analysis from raw footage.

Concept explanation and current-fact lookup are intentionally separated. Current facts are grounded in published exports rather than raw or audit surfaces.

## Installation

Installation differs by agent. This root README currently documents Codex, Claude, Cursor, and OpenCode.

### Codex

Ask Codex:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent codex using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Codex discovery target to that source.
```

Detailed docs: [.codex/INSTALL.md](./.codex/INSTALL.md)

### Claude

Ask Claude:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent claude using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Claude discovery target to that source.
```

Detailed docs: [.claude-plugin/INSTALL.md](./.claude-plugin/INSTALL.md)

### Cursor

Ask Cursor:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent cursor using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Cursor discovery target to that source.
```

Detailed docs: [.cursor-plugin/INSTALL.md](./.cursor-plugin/INSTALL.md)

### OpenCode

Ask OpenCode:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent opencode using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the OpenCode discovery target to that source.
```

Detailed docs: [.opencode/INSTALL.md](./.opencode/INSTALL.md)

## Verify installation

Start a new session in your agent, then try one concept question and one current-fact question.

Concept check:

```text
Explain what plus frames mean in SF6 and why they matter on offense.
```

Current-fact check:

```text
Use kb-sf6-frame-current to check the current published frame data for Luke's crouching medium punch.
```

If the agent selects the expected public skill automatically or responds correctly when you name the skill directly, installation is working.

## Basic usage

The agent can usually choose a matching skill automatically. You can also mention a skill by name explicitly.

### Concept-first usage with `kb-sf6-core`

```text
Use kb-sf6-core to explain what a shimmy is in SF6 and why it beats throw tech attempts.
```

### Current-fact usage with `kb-sf6-frame-current`

```text
Use kb-sf6-frame-current to check the current published startup and block advantage for Luke's crouching medium punch.
```

## Current fact policy

For current roster characters, current fact is grounded in published exports only.

- Start from `data/exports/<character_slug>/snapshot_manifest.json`.
- Use only datasets whose `publication_state = available`.
- The current roster canonical source is `shared/roster/current-character-roster.json`.
- `official_raw` is canonical.
- `derived_metrics` is official-only computed output.
- `supercombo_enrichment` is supplemental only.
- `data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface for normal current-fact answers.
- Packaged runtime assets under `skills/kb-sf6-frame-current/assets/published/...` are generated from repo-level canonical published data under `data/exports/...`.

For more detail, see [ingest/frame_data/README.md](./ingest/frame_data/README.md) and [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md).

## What's inside

- `skills/`
  - canonical public source for distributable skills
- `maintainer-skills/`
  - repository-only workflows for maintainers
- `shared/`
  - shared non-code artifacts such as roster and stable vocabulary
- `data/exports/`
  - repo-level canonical published current-fact surface
- `ingest/`
  - ingestion, normalization, and publishing implementation
- `local/`
  - tracked personal trial workspace for trying distributed skills

## Contributing

Contributors should work from the repository checkout rather than only from installed discovery links.

- New public skills belong under `skills/<skill-name>/`.
- Maintainer-only workflows belong under `maintainer-skills/`.
- Ingestion and publication code belongs under `ingest/frame_data/`.
- Read [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md) before changing repository surfaces.

## Updating

- Installed users should follow the current install or update flow for their agent, using the linked install docs above.
- Contributors should pull the repository directly and work from the repo checkout.
- If an agent-specific flow changes, treat the linked install docs as the source of truth.
```

- [ ] **Step 2: Run the documentation validators and verify the new README turns them green**

Run:

```powershell
pwsh -File tests/packaging/validate-doc-links.ps1
pwsh -File tests/packaging/validate-layout.ps1
```

Expected:
- `Docs OK`
- `Layout OK`

- [ ] **Step 3: Commit the README rewrite**

```bash
git add README.md
git commit -m "docs: rewrite root README for current design"
```

### Task 3: Run Broader Verification And Final Readthrough

**Files:**
- Test: `E:\github\SF6-skills\tests\install\validate-distribution-surface.ps1`
- Test: `E:\github\SF6-skills\README.md`

- [ ] **Step 1: Run the distribution-surface validator to confirm the README rewrite did not drift install expectations**

Run:

```powershell
pwsh -File tests/install/validate-distribution-surface.ps1
```

Expected:
- `Distribution surface OK`

- [ ] **Step 2: Perform a manual readthrough against the approved spec**

Confirm all of the following in `E:\github\SF6-skills\README.md`:

- the section order is `SF6 Skills`, `How it works`, `Installation`, `Verify installation`, `Basic usage`, `Current fact policy`, `What's inside`, `Contributing`, `Updating`
- installation only documents Codex, Claude, Cursor, and OpenCode
- `Basic usage` shows public skills only
- `Current fact policy` mentions `data/exports/<character_slug>/snapshot_manifest.json`, `publication_state = available`, and `shared/roster/current-character-roster.json`
- `What's inside` explains `skills/`, `maintainer-skills/`, `shared/`, `data/exports/`, `ingest/`, and `local/`

## Self-Review

- Spec coverage:
  - superpowers-style onboarding front half: covered by Task 2 Step 1
  - supported install surfaces limited to Codex, Claude, Cursor, and OpenCode: covered by Task 2 Step 1 and Task 3 Step 2
  - automatic or explicit skill selection guidance: covered by Task 2 Step 1
  - public-skill examples for `kb-sf6-core` and `kb-sf6-frame-current`: covered by Task 2 Step 1
  - medium-depth current-fact trust model: covered by Task 2 Step 1
  - top-level surface responsibilities: covered by Task 2 Step 1
  - contributor guidance and update guidance: covered by Task 2 Step 1
  - README contract protected by validators: covered by Task 1 and Task 2 Step 2
- Placeholder scan:
  - no `TODO`, `TBD`, or deferred wording remains
  - each code-changing step includes exact file content
  - each verification step includes an exact command and expected output
- Type consistency:
  - README section names are consistent between spec, validators, and manual review
  - install-doc paths are consistent: `.codex/INSTALL.md`, `.claude-plugin/INSTALL.md`, `.cursor-plugin/INSTALL.md`, `.opencode/INSTALL.md`
  - current-fact source names are consistent: `snapshot_manifest.json`, `publication_state = available`, `official_raw`, `derived_metrics`, `supercombo_enrichment`
