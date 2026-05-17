Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$boundaryDocPath = 'docs/architecture/noncanonical-data-authority-boundaries.md'
$registryPath = 'data/repository-surfaces.json'
$registryPolicyPath = 'docs/architecture/repository-surface-registry-policy.md'
$architectureReadmePath = 'docs/architecture/README.md'
$exportsReadmePath = 'data/exports/README.md'
$ingestReadmePath = 'ingest/frame_data/README.md'
$contractsReadmePath = 'contracts/README.md'
$agentsPath = 'AGENTS.md'
$validatorPath = 'tests/validation/validate-noncanonical-data-authority-boundaries.ps1'

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

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Get-Surface {
  param(
    [Parameter(Mandatory = $true)][object]$Registry,
    [Parameter(Mandatory = $true)][string]$Id,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $matches = @($Registry.surfaces | Where-Object { $_.id -eq $Id })
  if ($matches.Count -ne 1) {
    $Issues.Value += "$registryPath must contain exactly one surface: $Id"
    return $null
  }

  return $matches[0]
}

function Assert-SurfaceCommonBoundary {
  param(
    [Parameter(Mandatory = $true)][object]$Surface,
    [Parameter(Mandatory = $true)][string]$Id,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Surface 'normal_public_answer_authority') -or $Surface.normal_public_answer_authority -ne $false) {
    $Issues.Value += "$Id must not be normal public answer authority"
  }
  if (-not (Test-Property $Surface 'public_distribution_status') -or $Surface.public_distribution_status -ne 'not_distribution') {
    $Issues.Value += "$Id must remain not_distribution"
  }
  if (@($Surface.validation_expectation) -notcontains 'noncanonical_data_authority_boundary_valid') {
    $Issues.Value += "$Id validation_expectation must include noncanonical_data_authority_boundary_valid"
  }
  if (@($Surface.validation_expectation) -notcontains 'not_normal_public_answer_authority') {
    $Issues.Value += "$Id validation_expectation must include not_normal_public_answer_authority"
  }
  if (@($Surface.policy_refs) -notcontains $boundaryDocPath) {
    $Issues.Value += "$Id policy_refs must include $boundaryDocPath"
  }
}

$issues = @()

foreach ($relativePath in @(
  $boundaryDocPath,
  $registryPath,
  $registryPolicyPath,
  $architectureReadmePath,
  $exportsReadmePath,
  $ingestReadmePath,
  $contractsReadmePath,
  $agentsPath,
  $validatorPath
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing non-canonical authority boundary file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $boundaryDocPath) -PathType Leaf) {
  $boundaryDoc = Read-Text $boundaryDocPath
  foreach ($needle in @(
    'status: accepted',
    'tracking_issue: "#260"',
    'data/raw/',
    'raw_snapshots',
    'data/normalized/',
    'normalized_intermediate_state',
    '*_manual_review.*',
    'manual_review_sidecars',
    'data/exports/_index/manual-review-debt.json',
    'manual_review_debt_index',
    'normal public answer authority',
    'current-fact authority ではない',
    $validatorPath,
    'tests/validation/validate-raw-snapshot-minimality.ps1',
    'tests/validation/validate-manual-review-debt-index.ps1',
    'tests/validation/validate-current-fact-boundaries.ps1',
    'tests/validation/validate-frame-current-assets.ps1'
  )) {
    Assert-Contains $boundaryDoc $needle $boundaryDocPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $architectureReadmePath) -PathType Leaf) {
  Assert-Contains (Read-Text $architectureReadmePath) 'noncanonical-data-authority-boundaries.md' $architectureReadmePath ([ref]$issues)
}

foreach ($doc in @(
  $registryPolicyPath,
  $exportsReadmePath,
  $ingestReadmePath
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    Assert-Contains (Read-Text $doc) $boundaryDocPath $doc ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $exportsReadmePath) -PathType Leaf) {
  $exportsReadme = Read-Text $exportsReadmePath
  foreach ($needle in @(
    'data/raw/',
    'data/normalized/',
    '*_manual_review.*',
    'data/exports/_index/manual-review-debt.json',
    'not normal public answer authority',
    'Exact current facts must not be inferred from those surfaces alone.',
    $validatorPath
  )) {
    Assert-Contains $exportsReadme $needle $exportsReadmePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $ingestReadmePath) -PathType Leaf) {
  $ingestReadme = Read-Text $ingestReadmePath
  foreach ($needle in @(
    'data/raw/',
    'data/normalized/',
    'manual-review sidecars',
    'manual-review debt observability',
    'normal public answer authority',
    $boundaryDocPath
  )) {
    Assert-Contains $ingestReadme $needle $ingestReadmePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $contractsReadmePath) -PathType Leaf) {
  $contractsReadme = Read-Text $contractsReadmePath
  foreach ($needle in @(
    $validatorPath,
    'data/raw/',
    'data/normalized/',
    '*_manual_review.*',
    'data/exports/_index/manual-review-debt.json',
    'normal public answer authority'
  )) {
    Assert-Contains $contractsReadme $needle $contractsReadmePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $agentsPath) -PathType Leaf) {
  $agents = Read-Text $agentsPath
  foreach ($needle in @(
    'data/raw/...',
    'data/normalized/...',
    '*_manual_review.*',
    'not final evidence for normal public answers'
  )) {
    Assert-Contains $agents $needle $agentsPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json

  foreach ($id in @(
    'raw_snapshots',
    'normalized_intermediate_state',
    'manual_review_sidecars',
    'manual_review_debt_index'
  )) {
    $surface = Get-Surface $registry $id ([ref]$issues)
    if ($null -ne $surface) {
      Assert-SurfaceCommonBoundary $surface $id ([ref]$issues)
    }
  }

  foreach ($id in @(
    'raw_snapshots',
    'normalized_intermediate_state',
    'manual_review_sidecars'
  )) {
    $surface = Get-Surface $registry $id ([ref]$issues)
    if ($null -ne $surface -and $surface.surface_role -ne 'non_canonical') {
      $issues += "$id must remain non_canonical"
    }
  }

  $manualReviewDebtIndex = Get-Surface $registry 'manual_review_debt_index' ([ref]$issues)
  if ($null -ne $manualReviewDebtIndex) {
    if ($manualReviewDebtIndex.surface_role -ne 'derived') {
      $issues += 'manual_review_debt_index must remain derived'
    }
    if ($manualReviewDebtIndex.generated -ne $true) {
      $issues += 'manual_review_debt_index must remain generated'
    }
    if (-not ([string]$manualReviewDebtIndex.authority_scope).Contains('observability')) {
      $issues += 'manual_review_debt_index authority_scope must describe observability only'
    }
    if (-not ([string]$manualReviewDebtIndex.notes).Contains('not current-fact authority')) {
      $issues += 'manual_review_debt_index notes must state it is not current-fact authority'
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Non-canonical data authority boundaries OK'
