Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adrPath = 'docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md'
$decisionsReadmePath = 'docs/architecture/decisions/README.md'
$architectureReadmePath = 'docs/architecture/README.md'
$readmePath = 'README.md'
$harnessPath = 'docs/architecture/harness-and-distribution-roles.md'
$distributionReadmePath = 'docs/distribution/README.md'
$installerReadmePath = 'packages/skill-installers/README.md'
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

foreach ($relativePath in @(
  $adrPath,
  $decisionsReadmePath,
  $architectureReadmePath,
  $readmePath,
  $harnessPath,
  $distributionReadmePath,
  $installerReadmePath,
  $packagingReadmePath,
  $registryPath,
  $policyPath
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing deferred distribution retirement file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $adrPath) -PathType Leaf) {
  $adr = Read-Text $adrPath
  foreach ($needle in @(
    'id: adr-0004',
    'status: accepted',
    'tracking_issue: "#248"',
    'selected_disposition: legacy_lane_until_public_adapter_removal_then_delete',
    'legacy_distribution_lane: interim_only',
    'retain_distribution_docs_long_term: false',
    'retain_installers_long_term: false',
    'retain_release_bundle_long_term: false',
    'immediate_deletion: false',
    'sf6.boundary.deferred_distribution_legacy_lane_interim_only',
    'sf6.boundary.deferred_distribution_surfaces_delete_after_adapter_removal',
    '.dist/sf6-agent-bundle.zip',
    'packages/skill-installers/*',
    'packages/skill-packaging/build-release-bundle.ps1',
    'docs/distribution/*',
    'legacy-distribution',
    'This ADR is design-only',
    'does not delete files',
    'does not change public `sf6-agent` behavior'
  )) {
    Assert-Contains $adr $needle $adrPath ([ref]$issues)
  }
}

foreach ($doc in @(
  $decisionsReadmePath,
  $architectureReadmePath,
  $readmePath,
  $harnessPath,
  $distributionReadmePath,
  $installerReadmePath,
  $packagingReadmePath,
  $policyPath
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    if ($doc -in @($decisionsReadmePath, $architectureReadmePath, $harnessPath)) {
      Assert-Contains $text '0004-retire-deferred-distribution-surfaces.md' $doc ([ref]$issues)
    } else {
      Assert-Contains $text $adrPath $doc ([ref]$issues)
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach ($id in @('release_bundle_dist', 'skill_installers_package', 'distribution_docs')) {
    $surface = @($registry.surfaces | Where-Object { $_.id -eq $id })
    if ($surface.Count -ne 1) {
      $issues += "$registryPath must contain exactly one $id surface"
      continue
    }
    if (@($surface[0].policy_refs) -notcontains $adrPath) {
      $issues += "$id must reference $adrPath"
    }
    if ($surface[0].public_distribution_status -ne 'deferred') {
      $issues += "$id must remain deferred"
    }
    if (-not ([string]$surface[0].notes).Contains('interim legacy-lane coverage')) {
      $issues += "$id notes must record interim legacy-lane coverage"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Deferred distribution retirement plan OK'
