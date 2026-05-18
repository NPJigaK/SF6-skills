Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adrPath = 'docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md'
$readmePath = 'README.md'
$harnessPath = 'docs/architecture/harness-and-distribution-roles.md'
$packagingReadmePath = 'packages/skill-packaging/README.md'
$registryPath = 'data/repository-surfaces.json'
$policyPath = 'docs/architecture/repository-surface-registry-policy.md'

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

foreach ($relativePath in @($adrPath, $readmePath, $harnessPath, $packagingReadmePath, $registryPath, $policyPath)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing deferred distribution retirement file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $adrPath) -PathType Leaf) {
  $adr = Read-Text $adrPath
  foreach ($needle in @(
    'id: adr-0004',
    'status: accepted',
    'selected_disposition: legacy_lane_until_public_adapter_removal_then_delete',
    'retain_distribution_docs_long_term: false',
    'retain_installers_long_term: false',
    'retain_release_bundle_long_term: false',
    'docs/distribution/*',
    'packages/skill-installers/*',
    'packages/skill-packaging/build-release-bundle.ps1'
  )) {
    Assert-Contains $adr $needle $adrPath ([ref]$issues)
  }
}

foreach ($removedPath in @(
  'docs/distribution',
  'packages/skill-installers',
  'packages/skill-packaging/build-release-bundle.ps1',
  'tests/validation/validate-distribution.ps1'
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $removedPath)) {
    $issues += "Deferred distribution path must be removed: $removedPath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach ($removedSurfaceId in @('release_bundle_dist', 'skill_installers_package', 'distribution_docs')) {
    if (@($registry.surfaces | Where-Object { $_.id -eq $removedSurfaceId }).Count -ne 0) {
      $issues += "$registryPath must not retain removed deferred distribution surface: $removedSurfaceId"
    }
  }
}

foreach ($doc in @($readmePath, $harnessPath, $packagingReadmePath, $policyPath)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    Assert-Contains $text $adrPath $doc ([ref]$issues)
    Assert-Contains $text 'deferred distribution surfaces were removed' $doc ([ref]$issues)
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Deferred distribution retirement plan OK'
