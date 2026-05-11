Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$assetRootRelativePath = 'skills/sf6-agent/assets/normalization'
$frameCurrentRelativePath = 'skills/sf6-agent/assets/frame-current'
$assetRoot = Join-Path $repoRoot $assetRootRelativePath
$manifestRelativePath = "$assetRootRelativePath/runtime_manifest.json"
$aliasesRelativePath = "$assetRootRelativePath/aliases.json"
$generatorRelativePath = 'packages/skill-packaging/build-normalization-runtime-assets.ps1'
$aliasesSourceRootRelativePath = 'data/aliases'
$aliasesSourceRoot = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $aliasesSourceRootRelativePath))

function Read-Json {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8 | ConvertFrom-Json
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

function Test-PathUnderDirectory {
  param(
    [Parameter(Mandatory = $true)][string]$CandidatePath,
    [Parameter(Mandatory = $true)][string]$DirectoryPath
  )

  $resolvedCandidate = [System.IO.Path]::GetFullPath($CandidatePath)
  $resolvedDirectory = [System.IO.Path]::GetFullPath($DirectoryPath).TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
  )
  $directoryPrefix = $resolvedDirectory + [System.IO.Path]::DirectorySeparatorChar

  return (
    $resolvedCandidate.Equals($resolvedDirectory, [System.StringComparison]::OrdinalIgnoreCase) -or
    $resolvedCandidate.StartsWith($directoryPrefix, [System.StringComparison]::OrdinalIgnoreCase)
  )
}

function Assert-DataAliasesSourcePath {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues,
    [AllowNull()][string]$ExpectedSha256 = $null
  )

  if ([System.IO.Path]::IsPathRooted($RelativePath)) {
    $Issues.Value += "$Context source path must be repo-relative under data/aliases/: $RelativePath"
    return
  }

  $candidatePath = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $RelativePath))
  if (-not (Test-PathUnderDirectory $candidatePath $aliasesSourceRoot)) {
    $Issues.Value += "$Context source path must resolve under data/aliases/: $RelativePath"
    return
  }

  if (-not (Test-Path -LiteralPath $candidatePath -PathType Leaf)) {
    $Issues.Value += "$Context source path does not exist: $RelativePath"
    return
  }

  if ($null -ne $ExpectedSha256 -and $ExpectedSha256 -ne '') {
    $expectedHash = ([string]$ExpectedSha256).ToLowerInvariant()
    $actualHash = (Get-FileHash -LiteralPath $candidatePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($expectedHash -ne $actualHash) {
      $Issues.Value += "$Context source hash mismatch: $RelativePath"
    }
  }
}

$issues = @()
$forbiddenTokens = @(
  'startup',
  'active',
  'recovery',
  'hit_adv',
  'block_adv_value',
  'damage',
  'frame_value',
  'patch',
  'tier',
  'strategy',
  'recommendation'
)

foreach ($relativePath in @($generatorRelativePath, $manifestRelativePath, $aliasesRelativePath)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing normalization runtime path: $relativePath"
  }
}

if (-not (Test-Path -LiteralPath $assetRoot -PathType Container)) {
  $issues += "Missing normalization runtime asset root: $assetRootRelativePath"
}

if (
  (Test-Path -LiteralPath $assetRoot -PathType Container) -and
  (Test-Path -LiteralPath (Join-Path $repoRoot $frameCurrentRelativePath) -PathType Container)
) {
  $normalizationResolved = (Resolve-Path -LiteralPath $assetRoot).Path
  $frameCurrentResolved = (Resolve-Path -LiteralPath (Join-Path $repoRoot $frameCurrentRelativePath)).Path
  if ($normalizationResolved.StartsWith($frameCurrentResolved, [System.StringComparison]::OrdinalIgnoreCase)) {
    $issues += 'Normalization runtime assets must stay separate from frame-current assets'
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $manifestRelativePath) -PathType Leaf) {
  $manifestRaw = Get-Content -LiteralPath (Join-Path $repoRoot $manifestRelativePath) -Raw -Encoding UTF8
  $manifest = $manifestRaw | ConvertFrom-Json

  foreach ($field in @(
    'generated',
    'schema_version',
    'kind',
    'authority',
    'not_current_fact_authority',
    'generator',
    'source_root',
    'asset_root',
    'source_paths',
    'target_path',
    'files'
  )) {
    Assert-Property $manifest $field $manifestRelativePath ([ref]$issues)
  }

  if ((Test-Property $manifest 'generated') -and $manifest.generated -ne $true) {
    $issues += "$manifestRelativePath must include generated marker true"
  }
  if ((Test-Property $manifest 'schema_version') -and $manifest.schema_version -ne 'normalization-runtime-manifest/v1') {
    $issues += "$manifestRelativePath must use schema_version normalization-runtime-manifest/v1"
  }
  if ((Test-Property $manifest 'kind') -and $manifest.kind -ne 'query_normalization_runtime_manifest') {
    $issues += "$manifestRelativePath must use kind query_normalization_runtime_manifest"
  }
  if ((Test-Property $manifest 'authority') -and $manifest.authority -ne 'query_normalization_only') {
    $issues += "$manifestRelativePath must use authority query_normalization_only"
  }
  if ((Test-Property $manifest 'not_current_fact_authority') -and $manifest.not_current_fact_authority -ne $true) {
    $issues += "$manifestRelativePath must set not_current_fact_authority true"
  }
  if ((Test-Property $manifest 'generator') -and $manifest.generator -ne $generatorRelativePath) {
    $issues += "$manifestRelativePath generator must be $generatorRelativePath"
  }
  if ((Test-Property $manifest 'source_root') -and $manifest.source_root -ne 'data/aliases') {
    $issues += "$manifestRelativePath source_root must be data/aliases"
  }
  if ((Test-Property $manifest 'asset_root') -and $manifest.asset_root -ne $assetRootRelativePath) {
    $issues += "$manifestRelativePath asset_root must be $assetRootRelativePath"
  }
  if ((Test-Property $manifest 'target_path') -and $manifest.target_path -ne $manifestRelativePath) {
    $issues += "$manifestRelativePath target_path must be $manifestRelativePath"
  }

  if (Test-Property $manifest 'source_paths') {
    foreach ($sourcePathRecord in @($manifest.source_paths)) {
      foreach ($field in @('path', 'sha256')) {
        Assert-Property $sourcePathRecord $field "$manifestRelativePath source_paths entry" ([ref]$issues)
      }
      if ((Test-Property $sourcePathRecord 'path') -and (Test-Property $sourcePathRecord 'sha256')) {
        Assert-DataAliasesSourcePath `
          -RelativePath ([string]$sourcePathRecord.path) `
          -Context "$manifestRelativePath source_paths entry" `
          -Issues ([ref]$issues) `
          -ExpectedSha256 ([string]$sourcePathRecord.sha256)
      }
    }
  }

  if (Test-Property $manifest 'files') {
    $files = @($manifest.files)
    if ($files.Count -ne 1) {
      $issues += "$manifestRelativePath must describe exactly one runtime aliases file"
    }
    foreach ($fileEntry in $files) {
      foreach ($field in @('target', 'target_path', 'source_paths', 'sha256')) {
        Assert-Property $fileEntry $field "$manifestRelativePath files entry" ([ref]$issues)
      }
      if ((Test-Property $fileEntry 'target') -and $fileEntry.target -ne 'aliases.json') {
        $issues += "$manifestRelativePath file target must be aliases.json"
      }
      if ((Test-Property $fileEntry 'target_path') -and $fileEntry.target_path -ne $aliasesRelativePath) {
        $issues += "$manifestRelativePath file target_path must be $aliasesRelativePath"
      }
      if ((Test-Property $fileEntry 'source_paths')) {
        foreach ($sourcePath in @($fileEntry.source_paths)) {
          Assert-DataAliasesSourcePath `
            -RelativePath ([string]$sourcePath) `
            -Context "$manifestRelativePath files entry" `
            -Issues ([ref]$issues)
        }
      }
      if ((Test-Property $fileEntry 'sha256') -and (Test-Path -LiteralPath (Join-Path $repoRoot $aliasesRelativePath) -PathType Leaf)) {
        $actualHash = (Get-FileHash -LiteralPath (Join-Path $repoRoot $aliasesRelativePath) -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($fileEntry.sha256 -ne $actualHash) {
          $issues += "$manifestRelativePath aliases.json hash mismatch"
        }
      }
    }
  }

  foreach ($token in $forbiddenTokens) {
    $escapedToken = [regex]::Escape($token)
    if ($manifestRaw -match ('(?i)"[^"]*' + $escapedToken + '[^"]*"')) {
      $issues += "$manifestRelativePath contains forbidden exact-current-fact token: $token"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $aliasesRelativePath) -PathType Leaf) {
  $aliasesRaw = Get-Content -LiteralPath (Join-Path $repoRoot $aliasesRelativePath) -Raw -Encoding UTF8
  $aliases = $aliasesRaw | ConvertFrom-Json

  foreach ($field in @(
    'generated',
    'schema_version',
    'kind',
    'authority',
    'not_current_fact_authority',
    'generator',
    'source_paths',
    'target_path',
    'entries'
  )) {
    Assert-Property $aliases $field $aliasesRelativePath ([ref]$issues)
  }

  if ((Test-Property $aliases 'generated') -and $aliases.generated -ne $true) {
    $issues += "$aliasesRelativePath must include generated marker true"
  }
  if ((Test-Property $aliases 'schema_version') -and $aliases.schema_version -ne 'normalization-runtime/v1') {
    $issues += "$aliasesRelativePath must use schema_version normalization-runtime/v1"
  }
  if ((Test-Property $aliases 'kind') -and $aliases.kind -ne 'query_normalization_runtime_assets') {
    $issues += "$aliasesRelativePath must use kind query_normalization_runtime_assets"
  }
  if ((Test-Property $aliases 'authority') -and $aliases.authority -ne 'query_normalization_only') {
    $issues += "$aliasesRelativePath must use authority query_normalization_only"
  }
  if ((Test-Property $aliases 'not_current_fact_authority') -and $aliases.not_current_fact_authority -ne $true) {
    $issues += "$aliasesRelativePath must set not_current_fact_authority true"
  }
  if ((Test-Property $aliases 'generator') -and $aliases.generator -ne $generatorRelativePath) {
    $issues += "$aliasesRelativePath generator must be $generatorRelativePath"
  }
  if ((Test-Property $aliases 'target_path') -and $aliases.target_path -ne $aliasesRelativePath) {
    $issues += "$aliasesRelativePath target_path must be $aliasesRelativePath"
  }
  if (Test-Property $aliases 'source_paths') {
    foreach ($sourcePath in @($aliases.source_paths)) {
      Assert-DataAliasesSourcePath `
        -RelativePath ([string]$sourcePath) `
        -Context $aliasesRelativePath `
        -Issues ([ref]$issues)
    }
  }
  if ((Test-Property $aliases 'entries') -and @($aliases.entries).Count -eq 0) {
    $issues += "$aliasesRelativePath must include runtime alias entries"
  }

  foreach ($token in $forbiddenTokens) {
    $escapedToken = [regex]::Escape($token)
    if ($aliasesRaw -match ('(?i)"[^"]*' + $escapedToken + '[^"]*"')) {
      $issues += "$aliasesRelativePath contains forbidden exact-current-fact token: $token"
    }
  }
}

$actualInventory = @()
if (Test-Path -LiteralPath $assetRoot -PathType Container) {
  $actualInventory = @(
    Get-ChildItem -LiteralPath $assetRoot -Recurse -File |
      ForEach-Object { $_.FullName.Substring($assetRoot.Length + 1).Replace('\', '/') }
  )
}

$expectedInventory = @('aliases.json', 'runtime_manifest.json')
if (Compare-Object ($actualInventory | Sort-Object) ($expectedInventory | Sort-Object)) {
  $issues += 'Normalization runtime inventory must contain only aliases.json and runtime_manifest.json'
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Normalization runtime assets OK'
