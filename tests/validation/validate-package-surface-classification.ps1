Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$registryPath = 'data/repository-surfaces.json'
$packagePolicyPath = 'docs/architecture/package-surface-classification.md'
$packageReadmePath = 'packages/README.md'

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

$packageClassifications = [ordered]@{
  'packages/calculation-executor/README.md' = [pscustomobject]@{
    SurfaceId = 'calculation_executor_package'
    Package = 'calculation-executor/'
    Classification = 'active_repo_local'
  }
  'packages/knowledge-generation/README.md' = [pscustomobject]@{
    SurfaceId = 'knowledge_generation_package'
    Package = 'knowledge-generation/'
    Classification = 'active_repo_local'
  }
  'packages/skill-packaging/README.md' = [pscustomobject]@{
    SurfaceId = 'skill_packaging_package'
    Package = 'skill-packaging/'
    Classification = 'shared_infra'
  }
  'packages/skill-installers/README.md' = [pscustomobject]@{
    SurfaceId = 'skill_installers_package'
    Package = 'skill-installers/'
    Classification = 'deferred_distribution'
  }
  'packages/skill-validator/README.md' = [pscustomobject]@{
    SurfaceId = 'skill_validator_package'
    Package = 'skill-validator/'
    Classification = 'legacy'
  }
}

foreach ($relativePath in @($registryPath, $packagePolicyPath, $packageReadmePath) + @($packageClassifications.Keys)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing package classification file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $packagePolicyPath) -PathType Leaf) {
  $policyText = Read-Text $packagePolicyPath
  foreach ($needle in @(
    'tracking_issue: "#250"',
    'active_repo_local',
    'deferred_distribution',
    'legacy',
    'shared_infra',
    'packages/calculation-executor/',
    'packages/knowledge-generation/',
    'packages/skill-packaging/',
    'packages/skill-installers/',
    'packages/skill-validator/',
    'package_classification=<value>',
    'This design step does not move package files'
  )) {
    Assert-Contains $policyText $needle $packagePolicyPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $packageReadmePath) -PathType Leaf) {
  $packagesReadme = Read-Text $packageReadmePath
  Assert-Contains $packagesReadme $packagePolicyPath $packageReadmePath ([ref]$issues)
  foreach ($entry in $packageClassifications.GetEnumerator()) {
    Assert-Contains $packagesReadme $entry.Value.Package $packageReadmePath ([ref]$issues)
    Assert-Contains $packagesReadme $entry.Value.Classification $packageReadmePath ([ref]$issues)
  }
}

foreach ($entry in $packageClassifications.GetEnumerator()) {
  $relativePath = $entry.Key
  if (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf) {
    $readmeText = Read-Text $relativePath
    Assert-Contains $readmeText "Package classification: ``$($entry.Value.Classification)``." $relativePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  if (@($registry.policy_refs) -notcontains $packagePolicyPath) {
    $issues += "$registryPath must reference $packagePolicyPath"
  }

  foreach ($entry in $packageClassifications.GetEnumerator()) {
    $surfaceId = $entry.Value.SurfaceId
    $classification = $entry.Value.Classification
    $surface = @($registry.surfaces | Where-Object { $_.id -eq $surfaceId })
    if ($surface.Count -ne 1) {
      $issues += "$registryPath must contain exactly one $surfaceId surface"
      continue
    }

    if (@($surface[0].policy_refs) -notcontains $packagePolicyPath) {
      $issues += "$surfaceId must reference $packagePolicyPath"
    }
    if (-not ([string]$surface[0].notes).Contains("package_classification=$classification")) {
      $issues += "$surfaceId notes must record package_classification=$classification"
    }
  }

  $skillPackaging = @($registry.surfaces | Where-Object { $_.id -eq 'skill_packaging_package' })
  if ($skillPackaging.Count -eq 1) {
    Assert-Contains ([string]$skillPackaging[0].notes) 'build-release-bundle.ps1 is deferred_distribution' 'skill_packaging_package notes' ([ref]$issues)
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Package surface classification OK'
