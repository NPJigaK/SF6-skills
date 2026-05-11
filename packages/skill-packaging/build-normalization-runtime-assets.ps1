Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$sourceRootRelativePath = 'data/aliases'
$assetRootRelativePath = 'skills/sf6-agent/assets/normalization'
$generatorRelativePath = 'packages/skill-packaging/build-normalization-runtime-assets.ps1'
$sourceRoot = Join-Path $repoRoot $sourceRootRelativePath
$assetRoot = Join-Path $repoRoot $assetRootRelativePath
$aliasesOutputPath = Join-Path $assetRoot 'aliases.json'
$manifestOutputPath = Join-Path $assetRoot 'runtime_manifest.json'

function ConvertTo-RepoRelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $resolved = (Resolve-Path -LiteralPath $Path).Path
  if (-not $resolved.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Path is outside repository root: $Path"
  }

  return $resolved.Substring($repoRoot.Length + 1).Replace('\', '/')
}

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
  throw "Missing normalization alias source root: $sourceRootRelativePath"
}

if (Test-Path -LiteralPath $assetRoot) {
  Remove-Item -LiteralPath $assetRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $assetRoot -Force | Out-Null

$sourceFiles = @(
  Get-ChildItem -LiteralPath $sourceRoot -File -Filter '*.json' |
    Sort-Object Name
)

if ($sourceFiles.Count -eq 0) {
  throw "No normalization alias JSON files found under $sourceRootRelativePath"
}

$sourceRecords = @()
$runtimeEntries = @()

foreach ($sourceFile in $sourceFiles) {
  $sourceRelativePath = ConvertTo-RepoRelativePath $sourceFile.FullName
  $sourceRecords += [ordered]@{
    path = $sourceRelativePath
    sha256 = (Get-FileHash -LiteralPath $sourceFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  }

  $document = Get-Content -LiteralPath $sourceFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($document.schema_version -ne 'normalization-aliases/v1') {
    throw "Unsupported normalization alias schema_version in $sourceRelativePath"
  }
  if ($document.kind -ne 'query_normalization_aliases') {
    throw "Unsupported normalization alias kind in $sourceRelativePath"
  }
  if ($document.authority -ne 'query_normalization_only') {
    throw "Normalization alias source must be query_normalization_only: $sourceRelativePath"
  }
  if ($document.not_current_fact_authority -ne $true) {
    throw "Normalization alias source must set not_current_fact_authority true: $sourceRelativePath"
  }

  foreach ($entry in @($document.entries)) {
    $normalized = [ordered]@{}
    foreach ($property in @($entry.normalized.PSObject.Properties | Sort-Object Name)) {
      $normalized[$property.Name] = $property.Value
    }

    $runtimeEntries += [ordered]@{
      id = [string]$entry.id
      alias_kind = [string]$entry.alias_kind
      aliases = @($entry.aliases)
      normalized = $normalized
      source_path = $sourceRelativePath
    }
  }
}

$runtimeEntries = @($runtimeEntries | Sort-Object { $_.source_path }, { $_.id })

$aliasesDocument = [ordered]@{
  generated = $true
  schema_version = 'normalization-runtime/v1'
  kind = 'query_normalization_runtime_assets'
  authority = 'query_normalization_only'
  not_current_fact_authority = $true
  generator = $generatorRelativePath
  source_paths = @($sourceRecords.path)
  target_path = "$assetRootRelativePath/aliases.json"
  entries = $runtimeEntries
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$aliasesJson = ((($aliasesDocument | ConvertTo-Json -Depth 10) -replace "`r`n", "`n").TrimEnd() + "`n")
[System.IO.File]::WriteAllText($aliasesOutputPath, $aliasesJson, $utf8NoBom)

$manifestDocument = [ordered]@{
  generated = $true
  schema_version = 'normalization-runtime-manifest/v1'
  kind = 'query_normalization_runtime_manifest'
  authority = 'query_normalization_only'
  not_current_fact_authority = $true
  generator = $generatorRelativePath
  source_root = $sourceRootRelativePath
  asset_root = $assetRootRelativePath
  source_paths = $sourceRecords
  target_path = "$assetRootRelativePath/runtime_manifest.json"
  files = @(
    [ordered]@{
      target = 'aliases.json'
      target_path = "$assetRootRelativePath/aliases.json"
      source_paths = @($sourceRecords.path)
      sha256 = (Get-FileHash -LiteralPath $aliasesOutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
  )
}

$manifestJson = ((($manifestDocument | ConvertTo-Json -Depth 10) -replace "`r`n", "`n").TrimEnd() + "`n")
[System.IO.File]::WriteAllText($manifestOutputPath, $manifestJson, $utf8NoBom)

Write-Host 'Normalization runtime assets built'
