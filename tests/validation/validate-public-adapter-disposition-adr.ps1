Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adrPath = 'docs/architecture/decisions/0003-retire-public-sf6-agent-adapter.md'
$decisionsReadmePath = 'docs/architecture/decisions/README.md'
$architectureReadmePath = 'docs/architecture/README.md'
$readmePath = 'README.md'
$harnessPath = 'docs/architecture/harness-and-distribution-roles.md'
$registryPath = 'data/repository-surfaces.json'

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
  $registryPath
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing public adapter disposition file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $adrPath) -PathType Leaf) {
  $adr = Read-Text $adrPath
  foreach ($needle in @(
    'id: adr-0003',
    'status: accepted',
    'tracking_issue: "#246"',
    'selected_disposition: remove_after_runtime_relocation',
    'reactivate_public_distribution: false',
    'immediate_deletion: false',
    'sf6.boundary.public_adapter_remove_after_runtime_relocation',
    'sf6.boundary.public_adapter_not_reactivated',
    'skills/sf6-agent/',
    'remove after runtime surface relocation',
    'runtime/frame-current/',
    'runtime/generated-knowledge/',
    'runtime/normalization/',
    'frame-current-runtime-separation-plan.md',
    'generated-reference-responsibility-plan.md',
    'Do not reactivate public `sf6-agent` distribution',
    'This ADR is design-only',
    'does not delete files',
    'does not change public `sf6-agent` behavior'
  )) {
    Assert-Contains $adr $needle $adrPath ([ref]$issues)
  }
}

foreach ($doc in @($decisionsReadmePath, $architectureReadmePath, $readmePath, $harnessPath)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    if ($doc -in @($decisionsReadmePath, $architectureReadmePath, $harnessPath)) {
      Assert-Contains $text '0003-retire-public-sf6-agent-adapter.md' $doc ([ref]$issues)
    } else {
      Assert-Contains $text $adrPath $doc ([ref]$issues)
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  $adapter = @($registry.surfaces | Where-Object { $_.id -eq 'sf6_agent_public_adapter' })
  if ($adapter.Count -ne 1) {
    $issues += "$registryPath must contain exactly one sf6_agent_public_adapter surface"
  } else {
    $surface = $adapter[0]
    if ($surface.public_distribution_status -ne 'deferred') {
      $issues += 'sf6_agent_public_adapter must remain deferred until implementation removes it'
    }
    if (@($surface.policy_refs) -notcontains $adrPath) {
      $issues += "sf6_agent_public_adapter must reference $adrPath"
    }
    if (-not ([string]$surface.notes).Contains('ADR-0003 selects removal after reusable runtime payloads are relocated')) {
      $issues += 'sf6_agent_public_adapter notes must record the ADR-0003 removal-after-relocation decision'
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Public adapter disposition ADR OK'
