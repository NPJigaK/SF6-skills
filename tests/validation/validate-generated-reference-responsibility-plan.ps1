Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$planPath = 'docs/architecture/generated-reference-responsibility-plan.md'
$registryPath = 'data/repository-surfaces.json'
$policyPath = 'docs/architecture/repository-surface-registry-policy.md'
$readmePath = 'README.md'
$architectureReadmePath = 'docs/architecture/README.md'
$skillsReadmePath = 'skills/README.md'

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Assert-Contains {
  param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$Needle,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not $Text.Contains($Needle)) {
    $Issues.Value += "$Context must mention: $Needle"
  }
}

$issues = @()

foreach ($relativePath in @(
  $planPath,
  $registryPath,
  $policyPath,
  $readmePath,
  $architectureReadmePath,
  $skillsReadmePath
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing generated reference responsibility file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $planPath) -PathType Leaf) {
  $plan = Read-Text $planPath
  foreach ($needle in @(
    'generated knowledge references',
    'public adapter policy references',
    'skills/sf6-agent/references/generated-*',
    'skills/sf6-agent/references/*-policy.md',
    'knowledge/curated/',
    'packages/knowledge-generation/build-sf6-agent-knowledge.ps1',
    'tests/validation/validate-generated-knowledge.ps1',
    'generated_knowledge_references',
    'sf6_agent_adapter_policy_references',
    'runtime/generated-knowledge/',
    'compatibility copy',
    'design-only',
    'do not move generated files',
    'public `sf6-agent` behavior',
    'canonical SF6 knowledge'
  )) {
    Assert-Contains $plan $needle $planPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  $generatedSurface = @($registry.surfaces | Where-Object { $_.id -eq 'generated_knowledge_references' })
  $adapterPolicySurface = @($registry.surfaces | Where-Object { $_.id -eq 'sf6_agent_adapter_policy_references' })

  if ($generatedSurface.Count -ne 1) {
    $issues += "$registryPath must contain exactly one generated_knowledge_references surface"
  } else {
    $surface = $generatedSurface[0]
    if ($surface.generated -ne $true) {
      $issues += 'generated_knowledge_references must remain generated'
    }
    if ($surface.generator -ne 'packages/knowledge-generation/build-sf6-agent-knowledge.ps1') {
      $issues += 'generated_knowledge_references must keep the knowledge generator'
    }
    if (@($surface.source_of_truth) -notcontains 'knowledge/curated') {
      $issues += 'generated_knowledge_references must source from knowledge/curated'
    }
    if (@($surface.policy_refs) -notcontains $planPath) {
      $issues += "generated_knowledge_references must reference $planPath"
    }
  }

  if ($adapterPolicySurface.Count -ne 1) {
    $issues += "$registryPath must contain exactly one sf6_agent_adapter_policy_references surface"
  } else {
    $surface = $adapterPolicySurface[0]
    if ($surface.generated -ne $false) {
      $issues += 'sf6_agent_adapter_policy_references must not be generated'
    }
    if ($surface.surface_role -ne 'deferred_legacy') {
      $issues += 'sf6_agent_adapter_policy_references must be deferred_legacy'
    }
    if ($surface.public_distribution_status -ne 'deferred') {
      $issues += 'sf6_agent_adapter_policy_references must have deferred public_distribution_status'
    }
    if ($surface.normal_public_answer_authority -ne $false) {
      $issues += 'sf6_agent_adapter_policy_references must not be normal public answer authority'
    }
    if (@($surface.path_globs) -notcontains 'skills/sf6-agent/references/*-policy.md') {
      $issues += 'sf6_agent_adapter_policy_references must cover skills/sf6-agent/references/*-policy.md'
    }
    if (@($surface.policy_refs) -notcontains $planPath) {
      $issues += "sf6_agent_adapter_policy_references must reference $planPath"
    }
  }
}

foreach ($doc in @($policyPath, $readmePath, $skillsReadmePath)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    Assert-Contains $text $planPath $doc ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $architectureReadmePath) -PathType Leaf) {
  $text = Read-Text $architectureReadmePath
  Assert-Contains $text 'generated-reference-responsibility-plan.md' $architectureReadmePath ([ref]$issues)
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Generated reference responsibility plan OK'
