Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adrPath = 'docs/architecture/decisions/0005-raw-snapshot-retention.md'
$decisionsReadmePath = 'docs/architecture/decisions/README.md'
$architectureReadmePath = 'docs/architecture/README.md'
$readmePath = 'README.md'
$ingestReadmePath = 'ingest/frame_data/README.md'
$workflowPath = 'workflows/update-frame-data.md'
$registryPath = 'data/repository-surfaces.json'
$registryPolicyPath = 'docs/architecture/repository-surface-registry-policy.md'

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
  $ingestReadmePath,
  $workflowPath,
  $registryPath,
  $registryPolicyPath
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing raw snapshot retention file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $adrPath) -PathType Leaf) {
  $adr = Read-Text $adrPath
  foreach ($needle in @(
    'id: adr-0005',
    'status: accepted',
    'tracking_issue: "#258"',
    'selected_retention_model: current_published_manifest_minimal_git_set',
    'git_tracked_raw_snapshot_role: minimal_reproducibility_artifact',
    'repo_external_raw_cache_role: future_metadata_reference_only',
    'retention_exception_artifact: required_for_unreferenced_git_raw_retention',
    'normal_public_answer_authority: false',
    'immediate_data_change: false',
    'sf6.boundary.raw_snapshots_git_tracked_minimal_reproducibility',
    'sf6.boundary.unreferenced_raw_snapshots_removable_without_exception',
    'sf6.boundary.repo_external_raw_cache_metadata_only',
    'sf6.boundary.raw_snapshots_not_public_answer_authority',
    'sf6.boundary.no_raw_snapshot_data_change_in_adr',
    'current published manifest minimal Git set',
    'data/exports/<character_slug>/snapshot_manifest.json',
    'tests/validation/validate-raw-snapshot-minimality.ps1',
    'repo-external raw caches',
    'sanitized metadata',
    'content hash',
    'This ADR is design-only',
    'does not add, delete, refetch, rewrite, normalize, or re-hash raw snapshots',
    'does not make `data/raw/` normal public answer authority'
  )) {
    Assert-Contains $adr $needle $adrPath ([ref]$issues)
  }
}

foreach ($doc in @(
  $decisionsReadmePath,
  $architectureReadmePath,
  $readmePath,
  $ingestReadmePath,
  $workflowPath,
  $registryPolicyPath
)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    if ($doc -in @($decisionsReadmePath, $architectureReadmePath)) {
      Assert-Contains $text '0005-raw-snapshot-retention.md' $doc ([ref]$issues)
    } else {
      Assert-Contains $text $adrPath $doc ([ref]$issues)
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  $rawSnapshots = @($registry.surfaces | Where-Object { $_.id -eq 'raw_snapshots' })
  if ($rawSnapshots.Count -ne 1) {
    $issues += "$registryPath must contain exactly one raw_snapshots surface"
  } else {
    $surface = $rawSnapshots[0]
    if ($surface.surface_role -ne 'non_canonical') {
      $issues += 'raw_snapshots must remain non_canonical'
    }
    if ($surface.normal_public_answer_authority -ne $false) {
      $issues += 'raw_snapshots must not be normal public answer authority'
    }
    if (@($surface.policy_refs) -notcontains $adrPath) {
      $issues += "raw_snapshots must reference $adrPath"
    }
    if (@($surface.validation_expectation) -notcontains 'raw_snapshot_retention_adr_valid') {
      $issues += 'raw_snapshots validation_expectation must include raw_snapshot_retention_adr_valid'
    }
    if (-not ([string]$surface.notes).Contains('ADR-0005 keeps broader raw cache or history storage repo-external by default')) {
      $issues += 'raw_snapshots notes must record the ADR-0005 repo-external cache boundary'
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Raw snapshot retention ADR OK'
