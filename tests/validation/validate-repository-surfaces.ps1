Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$schemaPath = 'contracts/repository-surface.schema.json'
$registryPath = 'data/repository-surfaces.json'
$policyDocPath = 'docs/architecture/repository-surface-registry-policy.md'
$readmePath = 'README.md'
$contractsReadmePath = 'contracts/README.md'

function Read-Json {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Assert-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )
  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
  }
}

function Get-TrackedMatches {
  param(
    [Parameter(Mandatory = $true)][string[]]$TrackedPaths,
    [Parameter(Mandatory = $true)][string]$Glob
  )

  $normalizedGlob = $Glob.Replace('\', '/')
  if ($normalizedGlob.EndsWith('/')) {
    $normalizedGlob = "$normalizedGlob*"
  }

  return @($TrackedPaths | Where-Object {
    $_ -eq $normalizedGlob -or
    $_ -like $normalizedGlob -or
    $_ -like "$normalizedGlob/*"
  })
}

function Assert-TextContains {
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
$requiredSurfaceIds = @(
  'knowledge',
  'knowledge_curated',
  'knowledge_lineage_report',
  'data_exports',
  'data_roster',
  'contracts',
  'workflows',
  'evals',
  'generated_knowledge_references',
  'sf6_agent_adapter_policy_references',
  'frame_current_runtime_assets',
  'normalization_runtime_assets',
  'release_bundle_dist',
  'distribution_docs',
  'sf6_agent_public_adapter',
  'validation_scripts',
  'knowledge_generation_package',
  'skill_packaging_package',
  'skill_installers_package',
  'skill_validator_package',
  'calculation_executor_package',
  'hermes_sf6_pack',
  'codex_hermes_sf6_pack',
  'raw_snapshots',
  'normalized_intermediate_state',
  'manual_review_sidecars',
  'manual_review_debt_index'
)

foreach ($relativePath in @($schemaPath, $registryPath, $policyDocPath, $readmePath, $contractsReadmePath)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing repository surface file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $schemaPath) -PathType Leaf) {
  $schema = Read-Json $schemaPath
  foreach ($field in @('$schema', '$id', 'title')) {
    Assert-Property $schema $field $schemaPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $registryPath) -PathType Leaf) {
  $registry = Read-Json $registryPath
  foreach ($field in @('schema_version', 'last_reviewed', 'registry_status', 'policy_refs', 'surfaces')) {
    Assert-Property $registry $field $registryPath ([ref]$issues)
  }

  if ((Test-Property $registry 'schema_version') -and $registry.schema_version -ne 'repository-surfaces/v1') {
    $issues += "$registryPath must use schema_version repository-surfaces/v1"
  }
  if ((Test-Property $registry 'registry_status') -and $registry.registry_status -ne 'seed_index_of_existing_reviewed_boundaries') {
    $issues += "$registryPath must remain a seed index of existing reviewed boundaries"
  }

  $trackedPaths = @()
  $pathTrackingAvailable = $false
  if (Get-Command git -ErrorAction SilentlyContinue) {
    $trackedPaths = @(& git -C $repoRoot ls-files)
    if ($LASTEXITCODE -ne 0) {
      throw 'Unable to list tracked repository files'
    }
    $pathTrackingAvailable = $true
  } else {
    Write-Host 'WARNING: git is unavailable; skipping repository surface tracked-path checks'
  }

  $surfaces = @($registry.surfaces)
  $seenIds = @{}
  foreach ($surface in $surfaces) {
    $id = if (Test-Property $surface 'id') { [string]$surface.id } else { '<missing-id>' }
    foreach ($field in @(
      'id',
      'title',
      'path_globs',
      'path_state',
      'surface_role',
      'authority_scope',
      'source_of_truth',
      'generated',
      'generator',
      'source_paths',
      'allowed_to_edit_directly',
      'public_distribution_status',
      'normal_public_answer_authority',
      'validation_expectation',
      'policy_refs',
      'notes'
    )) {
      Assert-Property $surface $field "$registryPath surface $id" ([ref]$issues)
    }

    if ($seenIds.ContainsKey($id)) {
      $issues += "$registryPath duplicate surface id: $id"
    } else {
      $seenIds[$id] = $true
    }

    $pathMatches = @()
    foreach ($glob in @($surface.path_globs)) {
      $matches = @()
      if ($pathTrackingAvailable) {
        $matches = @(Get-TrackedMatches $trackedPaths ([string]$glob))
      }
      $pathMatches += $matches
      if ($pathTrackingAvailable) {
        if ($surface.path_state -eq 'tracked_present' -and $matches.Count -eq 0) {
          $issues += "$registryPath surface $id path_glob has no tracked match: $glob"
        }
        if ($surface.path_state -eq 'documented_absent' -and $matches.Count -gt 0) {
          $issues += "$registryPath surface $id is documented_absent but has tracked matches for: $glob"
        }
        if ($surface.path_state -eq 'generated_untracked' -and $matches.Count -gt 0) {
          $issues += "$registryPath surface $id is generated_untracked but tracked files match: $glob"
        }
      }
    }

    if ($surface.generated -eq $true) {
      if ($null -eq $surface.generator -or [string]::IsNullOrWhiteSpace([string]$surface.generator)) {
        $issues += "$registryPath generated surface $id must declare generator"
      }
      if (@($surface.source_paths).Count -eq 0) {
        $issues += "$registryPath generated surface $id must declare source_paths"
      }
      if (@($surface.source_of_truth) -contains 'self') {
        $issues += "$registryPath generated surface $id must not use source_of_truth self"
      }
      if ($surface.allowed_to_edit_directly -ne $false) {
        $issues += "$registryPath generated surface $id must not allow direct edits"
      }
    }

    if ($surface.surface_role -eq 'canonical' -and $surface.generated -ne $false) {
      $issues += "$registryPath canonical surface $id must not be generated"
    }
    if ($surface.surface_role -eq 'derived' -and $surface.generated -ne $true) {
      $issues += "$registryPath derived surface $id must be generated"
    }
    if ($surface.surface_role -eq 'non_canonical' -and $surface.normal_public_answer_authority -ne $false) {
      $issues += "$registryPath non-canonical surface $id must not be normal public answer authority"
    }
    if ($id -eq 'sf6_agent_public_adapter' -and $surface.public_distribution_status -ne 'deferred') {
      $issues += "$registryPath must represent skills/sf6-agent as deferred"
    }
    if ($id -eq 'release_bundle_dist' -and $surface.path_state -ne 'generated_untracked') {
      $issues += "$registryPath must represent .dist release bundle as generated_untracked"
    }
    if ($id -eq 'normalized_intermediate_state' -and $surface.path_state -ne 'documented_absent') {
      $issues += "$registryPath must represent data/normalized as documented_absent until tracked files exist"
    }
  }

  foreach ($requiredId in $requiredSurfaceIds) {
    if (-not $seenIds.ContainsKey($requiredId)) {
      $issues += "$registryPath missing required seed surface: $requiredId"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $policyDocPath) -PathType Leaf) {
  $policyDoc = Read-Text $policyDocPath
  foreach ($requiredText in @(
    'data/repository-surfaces.json',
    'repository-surfaces/v1',
    'surface_role',
    'path_state',
    'validation_expectation',
    'read-only',
    'derived-build',
    'legacy-distribution',
    'all',
    'canonical',
    'derived',
    'deferred_legacy',
    'repo_local_support',
    'historical',
    'non_canonical',
    'generated_knowledge_references',
    'knowledge_lineage_report',
    'sf6_agent_adapter_policy_references',
    'frame_current_runtime_assets',
    'normalization_runtime_assets',
    'release_bundle_dist',
    'distribution_docs',
    'sf6_agent_public_adapter',
    'skill_installers_package',
    'raw_snapshots',
    'normalized_intermediate_state',
    'manual_review_sidecars',
    'manual_review_debt_index'
  )) {
    Assert-TextContains $policyDoc $requiredText $policyDocPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $readmePath) -PathType Leaf) {
  $readme = Read-Text $readmePath
  foreach ($requiredText in @(
    'data/repository-surfaces.json',
    'docs/architecture/repository-surface-registry-policy.md',
    'read-only',
    'derived-build',
    'legacy-distribution'
  )) {
    Assert-TextContains $readme $requiredText $readmePath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $contractsReadmePath) -PathType Leaf) {
  $contractsReadme = Read-Text $contractsReadmePath
  foreach ($requiredText in @(
    'repository-surface.schema.json',
    'data/repository-surfaces.json',
    'docs/architecture/repository-surface-registry-policy.md'
  )) {
    Assert-TextContains $contractsReadme $requiredText $contractsReadmePath ([ref]$issues)
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'Repository surfaces OK'
