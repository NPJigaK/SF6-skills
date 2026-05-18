Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$assetRootRelativePath = 'runtime/normalization'
$compatibilityAssetRootRelativePath = 'skills/sf6-agent/assets/normalization'
$frameCurrentRelativePath = 'runtime/frame-current'
$assetRoot = Join-Path $repoRoot $assetRootRelativePath
$manifestRelativePath = "$assetRootRelativePath/runtime_manifest.json"
$aliasesRelativePath = "$assetRootRelativePath/aliases.json"
$compatibilityAssetRoot = Join-Path $repoRoot $compatibilityAssetRootRelativePath
$compatibilityManifestRelativePath = "$compatibilityAssetRootRelativePath/runtime_manifest.json"
$compatibilityAliasesRelativePath = "$compatibilityAssetRootRelativePath/aliases.json"
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

function ConvertTo-OrderedNormalizedObject {
  param(
    [Parameter(Mandatory = $true)][object]$Normalized,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $orderedNormalized = [ordered]@{}
  if ($Normalized -isnot [pscustomobject]) {
    $Issues.Value += "$Context normalized must be an object"
    return $orderedNormalized
  }

  foreach ($property in @($Normalized.PSObject.Properties | Sort-Object Name)) {
    if ($allowedNormalizedProperties -notcontains $property.Name) {
      $Issues.Value += "$Context normalized contains unsupported property: $($property.Name)"
      continue
    }
    $orderedNormalized[$property.Name] = $property.Value
  }

  return $orderedNormalized
}

function ConvertTo-ComparableRuntimeEntry {
  param(
    [Parameter(Mandatory = $true)][object]$Entry,
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues,
    [switch]$RequireSourcePathProperty
  )

  $requiredFields = @('id', 'alias_kind', 'aliases', 'normalized')
  if ($RequireSourcePathProperty) {
    $requiredFields += 'source_path'
  }

  $hasRequiredFields = $true
  foreach ($field in $requiredFields) {
    if (-not (Test-Property $Entry $field)) {
      $Issues.Value += "$Context missing property: $field"
      $hasRequiredFields = $false
    }
  }
  if (-not $hasRequiredFields) {
    return $null
  }

  if ($allowedAliasKinds -notcontains ([string]$Entry.alias_kind)) {
    $Issues.Value += "$Context has unsupported alias_kind: $($Entry.alias_kind)"
  }

  Assert-DataAliasesSourcePath `
    -RelativePath $SourcePath `
    -Context $Context `
    -Issues $Issues

  return [ordered]@{
    id = [string]$Entry.id
    alias_kind = [string]$Entry.alias_kind
    aliases = @($Entry.aliases | ForEach-Object { [string]$_ })
    normalized = ConvertTo-OrderedNormalizedObject `
      -Normalized $Entry.normalized `
      -Context $Context `
      -Issues $Issues
    source_path = $SourcePath
  }
}

function ConvertTo-CompactJson {
  param([Parameter(Mandatory = $true)][object]$Value)
  return ConvertTo-Json -InputObject $Value -Depth 20 -Compress
}

function Assert-StringListEqual {
  param(
    [Parameter(Mandatory = $true)][string[]]$Expected,
    [Parameter(Mandatory = $true)][object[]]$Actual,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $actualList = @($Actual | ForEach-Object { [string]$_ })
  if ($Expected.Count -ne $actualList.Count) {
    $Issues.Value += "$Context must match data/aliases source path count"
    return
  }

  for ($index = 0; $index -lt $Expected.Count; $index++) {
    if ($Expected[$index] -ne $actualList[$index]) {
      $Issues.Value += "$Context source path mismatch at index $index`: expected $($Expected[$index]), got $($actualList[$index])"
    }
  }
}

$issues = @()
$allowedAliasKinds = @(
  'character',
  'move_input',
  'field',
  'term',
  'query_fixture'
)
$allowedNormalizedProperties = @(
  'character_slug',
  'move_input',
  'field',
  'term_key',
  'question_text'
)
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

$expectedSourcePaths = @()
$expectedRuntimeEntries = @()

if (-not (Test-Path -LiteralPath $aliasesSourceRoot -PathType Container)) {
  $issues += "Missing normalization alias source root: $aliasesSourceRootRelativePath"
} else {
  $sourceFiles = @(
    Get-ChildItem -LiteralPath $aliasesSourceRoot -File -Filter '*.json' |
      Sort-Object Name
  )

  foreach ($sourceFile in $sourceFiles) {
    $sourceRelativePath = $sourceFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $expectedSourcePaths += $sourceRelativePath
    $sourceDocument = Get-Content -LiteralPath $sourceFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json

    foreach ($field in @(
      'schema_version',
      'kind',
      'authority',
      'not_current_fact_authority',
      'entries'
    )) {
      Assert-Property $sourceDocument $field $sourceRelativePath ([ref]$issues)
    }

    if ((Test-Property $sourceDocument 'schema_version') -and $sourceDocument.schema_version -ne 'normalization-aliases/v1') {
      $issues += "$sourceRelativePath must use schema_version normalization-aliases/v1"
    }
    if ((Test-Property $sourceDocument 'kind') -and $sourceDocument.kind -ne 'query_normalization_aliases') {
      $issues += "$sourceRelativePath must use kind query_normalization_aliases"
    }
    if ((Test-Property $sourceDocument 'authority') -and $sourceDocument.authority -ne 'query_normalization_only') {
      $issues += "$sourceRelativePath must use authority query_normalization_only"
    }
    if ((Test-Property $sourceDocument 'not_current_fact_authority') -and $sourceDocument.not_current_fact_authority -ne $true) {
      $issues += "$sourceRelativePath must set not_current_fact_authority true"
    }

    if (Test-Property $sourceDocument 'entries') {
      foreach ($entry in @($sourceDocument.entries)) {
        $comparableEntry = ConvertTo-ComparableRuntimeEntry `
          -Entry $entry `
          -SourcePath $sourceRelativePath `
          -Context "$sourceRelativePath entries entry" `
          -Issues ([ref]$issues)
        if ($null -ne $comparableEntry) {
          $expectedRuntimeEntries += $comparableEntry
        }
      }
    }
  }
}

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
    Assert-StringListEqual `
      -Expected ([string[]]$expectedSourcePaths) `
      -Actual @($manifest.source_paths | ForEach-Object { $_.path }) `
      -Context "$manifestRelativePath source_paths" `
      -Issues ([ref]$issues)
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
    Assert-StringListEqual `
      -Expected ([string[]]$expectedSourcePaths) `
      -Actual @($aliases.source_paths) `
      -Context "$aliasesRelativePath source_paths" `
      -Issues ([ref]$issues)
  }
  if ((Test-Property $aliases 'entries') -and @($aliases.entries).Count -eq 0) {
    $issues += "$aliasesRelativePath must include runtime alias entries"
  }
  if (Test-Property $aliases 'entries') {
    $actualRuntimeEntries = @()
    foreach ($entry in @($aliases.entries)) {
      $entrySourcePath = ''
      if (Test-Property $entry 'source_path') {
        $entrySourcePath = [string]$entry.source_path
      }

      $comparableEntry = ConvertTo-ComparableRuntimeEntry `
        -Entry $entry `
        -SourcePath $entrySourcePath `
        -Context "$aliasesRelativePath entries entry" `
        -Issues ([ref]$issues) `
        -RequireSourcePathProperty
      if ($null -ne $comparableEntry) {
        $actualRuntimeEntries += $comparableEntry
      }
    }

    $expectedSortedEntries = @(
      $expectedRuntimeEntries |
        Sort-Object @{ Expression = { $_['source_path'] } }, @{ Expression = { $_['id'] } }
    )
    $actualSortedEntries = @(
      $actualRuntimeEntries |
        Sort-Object @{ Expression = { $_['source_path'] } }, @{ Expression = { $_['id'] } }
    )

    $expectedEntriesJson = ConvertTo-CompactJson -Value @($expectedSortedEntries)
    $actualEntriesJson = ConvertTo-CompactJson -Value @($actualSortedEntries)
    if ($expectedEntriesJson -ne $actualEntriesJson) {
      $issues += "$aliasesRelativePath entries must exactly match entries derived from data/aliases/"
    }
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

if (Test-Path -LiteralPath $compatibilityAssetRoot -PathType Container) {
  foreach ($relativePath in @($compatibilityManifestRelativePath, $compatibilityAliasesRelativePath)) {
    if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
      $issues += "Missing normalization compatibility bridge path: $relativePath"
    }
  }

  if (
    (Test-Path -LiteralPath (Join-Path $repoRoot $aliasesRelativePath) -PathType Leaf) -and
    (Test-Path -LiteralPath (Join-Path $repoRoot $compatibilityAliasesRelativePath) -PathType Leaf)
  ) {
    $primaryAliases = Read-Json $aliasesRelativePath
    $compatibilityAliases = Read-Json $compatibilityAliasesRelativePath

    foreach ($field in @('generated', 'schema_version', 'kind', 'authority', 'not_current_fact_authority', 'generator', 'source_paths', 'entries')) {
      Assert-Property $compatibilityAliases $field $compatibilityAliasesRelativePath ([ref]$issues)
    }
    if ((Test-Property $compatibilityAliases 'target_path') -and $compatibilityAliases.target_path -ne $compatibilityAliasesRelativePath) {
      $issues += "$compatibilityAliasesRelativePath target_path must be $compatibilityAliasesRelativePath"
    }

    $primaryComparable = [ordered]@{
      generated = $primaryAliases.generated
      schema_version = $primaryAliases.schema_version
      kind = $primaryAliases.kind
      authority = $primaryAliases.authority
      not_current_fact_authority = $primaryAliases.not_current_fact_authority
      generator = $primaryAliases.generator
      source_paths = @($primaryAliases.source_paths)
      entries = @($primaryAliases.entries)
    }
    $compatibilityComparable = [ordered]@{
      generated = $compatibilityAliases.generated
      schema_version = $compatibilityAliases.schema_version
      kind = $compatibilityAliases.kind
      authority = $compatibilityAliases.authority
      not_current_fact_authority = $compatibilityAliases.not_current_fact_authority
      generator = $compatibilityAliases.generator
      source_paths = @($compatibilityAliases.source_paths)
      entries = @($compatibilityAliases.entries)
    }
    if ((ConvertTo-CompactJson $primaryComparable) -ne (ConvertTo-CompactJson $compatibilityComparable)) {
      $issues += "$compatibilityAliasesRelativePath must match primary runtime aliases except target_path"
    }
  }

  if (Test-Path -LiteralPath (Join-Path $repoRoot $compatibilityManifestRelativePath) -PathType Leaf) {
    $compatibilityManifest = Read-Json $compatibilityManifestRelativePath
    foreach ($field in @('generated', 'schema_version', 'kind', 'authority', 'not_current_fact_authority', 'generator', 'source_root', 'asset_root', 'source_paths', 'target_path', 'files')) {
      Assert-Property $compatibilityManifest $field $compatibilityManifestRelativePath ([ref]$issues)
    }
    if ((Test-Property $compatibilityManifest 'generated') -and $compatibilityManifest.generated -ne $true) {
      $issues += "$compatibilityManifestRelativePath must include generated marker true"
    }
    if ((Test-Property $compatibilityManifest 'schema_version') -and $compatibilityManifest.schema_version -ne 'normalization-runtime-manifest/v1') {
      $issues += "$compatibilityManifestRelativePath must use schema_version normalization-runtime-manifest/v1"
    }
    if ((Test-Property $compatibilityManifest 'kind') -and $compatibilityManifest.kind -ne 'query_normalization_runtime_manifest') {
      $issues += "$compatibilityManifestRelativePath must use kind query_normalization_runtime_manifest"
    }
    if ((Test-Property $compatibilityManifest 'authority') -and $compatibilityManifest.authority -ne 'query_normalization_only') {
      $issues += "$compatibilityManifestRelativePath must use authority query_normalization_only"
    }
    if ((Test-Property $compatibilityManifest 'not_current_fact_authority') -and $compatibilityManifest.not_current_fact_authority -ne $true) {
      $issues += "$compatibilityManifestRelativePath must set not_current_fact_authority true"
    }
    if ((Test-Property $compatibilityManifest 'generator') -and $compatibilityManifest.generator -ne $generatorRelativePath) {
      $issues += "$compatibilityManifestRelativePath generator must be $generatorRelativePath"
    }
    if ((Test-Property $compatibilityManifest 'source_root') -and $compatibilityManifest.source_root -ne 'data/aliases') {
      $issues += "$compatibilityManifestRelativePath source_root must be data/aliases"
    }
    if ((Test-Property $compatibilityManifest 'asset_root') -and $compatibilityManifest.asset_root -ne $compatibilityAssetRootRelativePath) {
      $issues += "$compatibilityManifestRelativePath asset_root must be $compatibilityAssetRootRelativePath"
    }
    if ((Test-Property $compatibilityManifest 'target_path') -and $compatibilityManifest.target_path -ne $compatibilityManifestRelativePath) {
      $issues += "$compatibilityManifestRelativePath target_path must be $compatibilityManifestRelativePath"
    }
    if (Test-Property $compatibilityManifest 'source_paths') {
      Assert-StringListEqual `
        -Expected ([string[]]$expectedSourcePaths) `
        -Actual @($compatibilityManifest.source_paths | ForEach-Object { $_.path }) `
        -Context "$compatibilityManifestRelativePath source_paths" `
        -Issues ([ref]$issues)
    }
    if (Test-Property $compatibilityManifest 'files') {
      $files = @($compatibilityManifest.files)
      if ($files.Count -ne 1) {
        $issues += "$compatibilityManifestRelativePath must describe exactly one runtime aliases file"
      }
      foreach ($fileEntry in $files) {
        foreach ($field in @('target', 'target_path', 'source_paths', 'sha256')) {
          Assert-Property $fileEntry $field "$compatibilityManifestRelativePath files entry" ([ref]$issues)
        }
        if ((Test-Property $fileEntry 'target') -and $fileEntry.target -ne 'aliases.json') {
          $issues += "$compatibilityManifestRelativePath file target must be aliases.json"
        }
        if ((Test-Property $fileEntry 'target_path') -and $fileEntry.target_path -ne $compatibilityAliasesRelativePath) {
          $issues += "$compatibilityManifestRelativePath file target_path must be $compatibilityAliasesRelativePath"
        }
        if ((Test-Property $fileEntry 'source_paths')) {
          foreach ($sourcePath in @($fileEntry.source_paths)) {
            Assert-DataAliasesSourcePath `
              -RelativePath ([string]$sourcePath) `
              -Context "$compatibilityManifestRelativePath files entry" `
              -Issues ([ref]$issues)
          }
        }
        if (
          (Test-Property $fileEntry 'sha256') -and
          (Test-Path -LiteralPath (Join-Path $repoRoot $compatibilityAliasesRelativePath) -PathType Leaf)
        ) {
          $actualHash = (Get-FileHash -LiteralPath (Join-Path $repoRoot $compatibilityAliasesRelativePath) -Algorithm SHA256).Hash.ToLowerInvariant()
          if ($fileEntry.sha256 -ne $actualHash) {
            $issues += "$compatibilityManifestRelativePath aliases.json hash mismatch"
          }
        }
      }
    }
  }

  $compatibilityInventory = @(
    Get-ChildItem -LiteralPath $compatibilityAssetRoot -Recurse -File |
      ForEach-Object { $_.FullName.Substring($compatibilityAssetRoot.Length + 1).Replace('\', '/') }
  )
  if (Compare-Object ($compatibilityInventory | Sort-Object) ($expectedInventory | Sort-Object)) {
    $issues += 'Normalization compatibility bridge inventory must contain only aliases.json and runtime_manifest.json'
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Normalization runtime assets OK'
