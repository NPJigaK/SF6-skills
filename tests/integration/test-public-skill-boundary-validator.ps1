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

  $crossSkillBackslashRoot = Join-Path $tempRoot 'cross-skill-backslash'
  New-FixtureRepo -Root $crossSkillBackslashRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `skills\beta\references\guide.md` before answering.
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
  Assert-FailsLike -FixtureRoot $crossSkillBackslashRoot -Pattern 'skills/alpha/SKILL\.md references public skill directory skills/beta/'

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

  $dogfoodBackslashRoot = Join-Path $tempRoot 'dogfood-backslash'
  New-FixtureRepo -Root $dogfoodBackslashRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `.agents\skills\beta\SKILL.md` before answering.
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
  Assert-FailsLike -FixtureRoot $dogfoodBackslashRoot -Pattern 'skills/alpha/SKILL\.md references repo-local dogfood skill directory \.agents/skills/beta/'

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

  $siblingTraversalBackslashRoot = Join-Path $tempRoot 'sibling-traversal-backslash'
  New-FixtureRepo -Root $siblingTraversalBackslashRoot -Skills @{
    'alpha' = @{
      'SKILL.md' = @'
---
name: alpha
description: Invalid skill.
---

Read `..\beta\references\guide.md` before answering.
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
  Assert-FailsLike -FixtureRoot $siblingTraversalBackslashRoot -Pattern 'skills/alpha/SKILL\.md references sibling skill directory traversal \.\./beta/'
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}

Write-Host 'Public skill boundary validator harness OK'
