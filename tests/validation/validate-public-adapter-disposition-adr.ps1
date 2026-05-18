Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$adrPath = 'docs/architecture/decisions/0003-retire-public-sf6-agent-adapter.md'
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

foreach ($relativePath in @($adrPath, $readmePath, $harnessPath, $registryPath)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing public adapter disposition file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $adrPath) -PathType Leaf) {
  $adr = Read-Text $adrPath
  foreach ($needle in @(
    'id: adr-0003',
    'status: accepted',
    'selected_disposition: remove_after_runtime_relocation',
    'runtime/frame-current/',
    'runtime/generated-knowledge/',
    'runtime/normalization/',
    'Remove or archive the remaining `skills/sf6-agent/` adapter surface'
  )) {
    Assert-Contains $adr $needle $adrPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'skills/sf6-agent') -PathType Container) {
  $issues += 'skills/sf6-agent must be removed after runtime relocation'
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Get-Content -LiteralPath (Join-Path $repoRoot $registryPath) -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach ($removedSurfaceId in @('sf6_agent_public_adapter', 'sf6_agent_adapter_policy_references')) {
    if (@($registry.surfaces | Where-Object { $_.id -eq $removedSurfaceId }).Count -ne 0) {
      $issues += "$registryPath must not retain removed public adapter surface: $removedSurfaceId"
    }
  }
}

foreach ($doc in @($readmePath, $harnessPath)) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $doc) -PathType Leaf) {
    $text = Read-Text $doc
    Assert-Contains $text $adrPath $doc ([ref]$issues)
    Assert-Contains $text 'public adapter was removed' $doc ([ref]$issues)
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Public adapter disposition ADR OK'
