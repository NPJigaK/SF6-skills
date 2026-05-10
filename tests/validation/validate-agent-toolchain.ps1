Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$toolchainRootRelative = 'data/toolchain'
$toolchainRoot = Join-Path $repoRoot $toolchainRootRelative
$schemaPath = 'contracts/agent-toolchain.schema.json'
$manifestPath = 'data/toolchain/maintainer-agent-toolchain.json'

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

function Get-ToolchainRelativePath {
  param([Parameter(Mandatory = $true)][string]$FullPath)

  $root = (Resolve-Path $toolchainRoot).Path.TrimEnd([char[]]@('\', '/'))
  $relative = $FullPath.Substring($root.Length)
  $relative = $relative -replace '^[\\/]+', ''
  return "$toolchainRootRelative/$($relative -replace '\\', '/')"
}

$issues = @()
$requiredFiles = @(
  'docs/architecture/agent-toolchain-freshness.md',
  $schemaPath,
  'data/toolchain/README.md',
  $manifestPath,
  'workflows/check-agent-toolchain-freshness.md'
)
$forbiddenManifestFields = @(
  'local_installed_version',
  'installed_version',
  'current_version',
  'local_version',
  'detected_version',
  'home_path',
  'config_path',
  'cache_path',
  'session_path',
  'log_path'
)

foreach ($relativePath in $requiredFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing agent toolchain file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $schemaPath) -PathType Leaf) {
  $schema = Read-Json $schemaPath
  foreach ($field in @('$schema', '$id', 'title')) {
    Assert-Property $schema $field $schemaPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'data/toolchain/README.md') -PathType Leaf) {
  $readme = Read-Text 'data/toolchain/README.md'
  foreach ($needle in @(
    'not SF6 gameplay knowledge',
    'not exact current-fact authority',
    'local installed versions',
    'credentials',
    'secrets',
    'local configs',
    'sessions',
    'caches',
    'logs'
  )) {
    if ($readme -notmatch [regex]::Escape($needle)) {
      $issues += "data/toolchain/README.md missing boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $manifestPath) -PathType Leaf) {
  $manifestRaw = Get-Content -LiteralPath (Join-Path $repoRoot $manifestPath) -Raw -Encoding UTF8
  $manifest = $manifestRaw | ConvertFrom-Json

  foreach ($field in @('schema_version', 'last_reviewed', 'tools', 'boundaries')) {
    Assert-Property $manifest $field $manifestPath ([ref]$issues)
  }

  if ((Test-Property $manifest 'schema_version') -and $manifest.schema_version -ne 'agent-toolchain/v1') {
    $issues += "$manifestPath must use schema_version agent-toolchain/v1"
  }

  foreach ($field in $forbiddenManifestFields) {
    if ($manifestRaw -match ('"(?i:' + [regex]::Escape($field) + ')"\s*:')) {
      $issues += "$manifestPath contains forbidden local-state field: $field"
    }
  }

  if (Test-Property $manifest 'tools') {
    $tools = @($manifest.tools)
    $toolsById = @{}
    foreach ($tool in $tools) {
      if (Test-Property $tool 'id') {
        $toolsById[[string]$tool.id] = $tool
      }
    }

    foreach ($toolId in @('codex-cli', 'hermes-cli')) {
      if (-not $toolsById.ContainsKey($toolId)) {
        $issues += "$manifestPath missing tool entry: $toolId"
      }
    }

    if ($toolsById.ContainsKey('codex-cli')) {
      $codex = $toolsById['codex-cli']
      if ((Test-Property $codex 'role') -and $codex.role -ne 'repo_implementation_executor') {
        $issues += 'codex-cli must use role repo_implementation_executor'
      }
    }

    if ($toolsById.ContainsKey('hermes-cli')) {
      $hermes = $toolsById['hermes-cli']
      if ((Test-Property $hermes 'role') -and $hermes.role -ne 'repo_local_growth_engine') {
        $issues += 'hermes-cli must use role repo_local_growth_engine'
      }
    }

    foreach ($tool in $tools) {
      $toolId = if (Test-Property $tool 'id') { [string]$tool.id } else { '<missing-id>' }
      foreach ($field in @(
        'recommended_channel',
        'known_good_version',
        'required_capabilities',
        'planned_capabilities',
        'version_command',
        'version_command_review_note',
        'update_guidance',
        'freshness_review_cadence'
      )) {
        Assert-Property $tool $field "$manifestPath tool $toolId" ([ref]$issues)
      }

      if ((Test-Property $tool 'required_capabilities') -and @($tool.required_capabilities).Count -eq 0) {
        $issues += "$manifestPath tool $toolId must include required_capabilities"
      }
      if ((Test-Property $tool 'version_command') -and $null -ne $tool.version_command) {
        if (-not (Test-Property $tool 'version_command_review_note') -or [string]::IsNullOrWhiteSpace([string]$tool.version_command_review_note)) {
          $issues += "$manifestPath tool $toolId with version_command must include version_command_review_note"
        }
      }
    }

    if ($toolsById.ContainsKey('hermes-cli')) {
      $hermes = $toolsById['hermes-cli']
      $capabilities = @()
      if (Test-Property $hermes 'required_capabilities') {
        $capabilities += @($hermes.required_capabilities)
      }
      if (Test-Property $hermes 'planned_capabilities') {
        $capabilities += @($hermes.planned_capabilities)
      }
      $capabilityText = (($capabilities | ForEach-Object { [string]$_ }) -join ' ').ToLowerInvariant()

      $capabilityChecks = @{
        'subagents or delegation' = @('subagent', 'delegation')
        'local skills' = @('skill')
        'Curator' = @('curator')
        'session search' = @('session_search', 'session search')
        '/goal or checkpoints' = @('goal', 'checkpoint')
        'cron or freshness audits' = @('cron', 'freshness')
      }

      foreach ($label in $capabilityChecks.Keys) {
        $found = $false
        foreach ($needle in $capabilityChecks[$label]) {
          if ($capabilityText.Contains($needle)) {
            $found = $true
          }
        }
        if (-not $found) {
          $issues += "hermes-cli capabilities must include $label"
        }
      }
    }
  }

  if (Test-Property $manifest 'boundaries') {
    $boundaryText = (@($manifest.boundaries) -join ' ')
    foreach ($needle in @(
      'toolchain policy is not SF6 gameplay knowledge',
      'local tool state is non-canonical',
      'CI must not call the internet for latest-version checks'
    )) {
      if ($boundaryText -notmatch [regex]::Escape($needle)) {
        $issues += "$manifestPath missing boundary: $needle"
      }
    }
  }
}

if (-not (Test-Path -LiteralPath $toolchainRoot -PathType Container)) {
  $issues += "Missing toolchain root: $toolchainRootRelative"
} else {
  foreach ($item in Get-ChildItem -LiteralPath $toolchainRoot -Force -Recurse -File) {
    $name = $item.Name.ToLowerInvariant()
    $relativePath = Get-ToolchainRelativePath $item.FullName
    $relativePathLower = $relativePath.ToLowerInvariant()

    if (
      $name -eq '.env' -or
      $name -like '.env.*' -or
      $name -eq '.envrc' -or
      $name -like '*secret*' -or
      $name -like '*token*' -or
      $name -like '*credential*' -or
      $name -like '*session*' -or
      $name -like '*cache*' -or
      $name -like '*log*' -or
      $relativePathLower -like '*/.env' -or
      $relativePathLower -like '*/.env.*' -or
      $relativePathLower -like '*/.envrc' -or
      $relativePathLower -like '*secret*' -or
      $relativePathLower -like '*token*' -or
      $relativePathLower -like '*credential*' -or
      $relativePathLower -like '*session*' -or
      $relativePathLower -like '*cache*' -or
      $relativePathLower -like '*log*'
    ) {
      $issues += "Forbidden toolchain local-state or secret-like file: $relativePath"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Agent toolchain OK'
