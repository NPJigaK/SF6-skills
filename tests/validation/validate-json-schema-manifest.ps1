param(
  [string]$ManifestPath = 'tests/validation/schema-validation-manifest.json'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

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

function Get-TrackedPaths {
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git is required for manifest glob expansion'
  }

  $paths = @(& git -C $repoRoot ls-files)
  if ($LASTEXITCODE -ne 0) {
    throw 'Unable to list tracked repository files'
  }

  return @($paths | ForEach-Object { [string]$_ })
}

function Get-TrackedMatches {
  param(
    [Parameter(Mandatory = $true)][string[]]$TrackedPaths,
    [Parameter(Mandatory = $true)][string]$Glob
  )

  $normalizedGlob = $Glob.Replace('\', '/')
  return @($TrackedPaths | Where-Object {
    $_ -eq $normalizedGlob -or $_ -like $normalizedGlob
  })
}

function Add-Issue {
  param(
    [Parameter(Mandatory = $true)][ref]$Issues,
    [Parameter(Mandatory = $true)][string]$Message
  )
  $Issues.Value += $Message
}

$issues = @()
$manifestRelativePath = $ManifestPath.Replace('\', '/')

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $manifestRelativePath) -PathType Leaf)) {
  throw "Missing schema validation manifest: $manifestRelativePath"
}

$manifest = Read-Json $manifestRelativePath

foreach ($field in @(
  'schema_version',
  'last_reviewed',
  'tracking_issue',
  'runner',
  'validation_scope',
  'semantic_validators_remain_authority',
  'entries'
)) {
  if (-not (Test-Property $manifest $field)) {
    Add-Issue ([ref]$issues) "$manifestRelativePath missing field: $field"
  }
}

if ((Test-Property $manifest 'schema_version') -and $manifest.schema_version -ne 'schema-validation-manifest/v1') {
  Add-Issue ([ref]$issues) "$manifestRelativePath must use schema_version schema-validation-manifest/v1"
}
if ((Test-Property $manifest 'runner') -and $manifest.runner -ne 'tests/validation/validate-json-schema-manifest.ps1') {
  Add-Issue ([ref]$issues) "$manifestRelativePath must point to tests/validation/validate-json-schema-manifest.ps1"
}
if ((Test-Property $manifest 'validation_scope') -and $manifest.validation_scope -ne 'json_schema_structural_validation_only') {
  Add-Issue ([ref]$issues) "$manifestRelativePath must keep validation_scope json_schema_structural_validation_only"
}
if ((Test-Property $manifest 'semantic_validators_remain_authority') -and $manifest.semantic_validators_remain_authority -ne $true) {
  Add-Issue ([ref]$issues) "$manifestRelativePath must keep semantic_validators_remain_authority true"
}

$trackedPaths = Get-TrackedPaths
$seenIds = @{}

foreach ($entry in @($manifest.entries)) {
  $id = if (Test-Property $entry 'id') { [string]$entry.id } else { '<missing-id>' }
  foreach ($field in @('id', 'schema_path', 'document_globs', 'notes')) {
    if (-not (Test-Property $entry $field)) {
      Add-Issue ([ref]$issues) "$manifestRelativePath entry $id missing field: $field"
    }
  }

  if ($seenIds.ContainsKey($id)) {
    Add-Issue ([ref]$issues) "$manifestRelativePath duplicate entry id: $id"
  } else {
    $seenIds[$id] = $true
  }

  if (-not (Test-Property $entry 'schema_path')) {
    continue
  }

  $schemaRelativePath = ([string]$entry.schema_path).Replace('\', '/')
  $schemaPath = Join-Path $repoRoot $schemaRelativePath
  if (-not (Test-Path -LiteralPath $schemaPath -PathType Leaf)) {
    Add-Issue ([ref]$issues) "$id schema_path does not exist: $schemaRelativePath"
    continue
  }

  $schemaText = Read-Text $schemaRelativePath
  $schema = $null
  try {
    $schema = $schemaText | ConvertFrom-Json
  } catch {
    Add-Issue ([ref]$issues) "$schemaRelativePath is not valid JSON: $($_.Exception.Message)"
    continue
  }

  foreach ($field in @('$schema', '$id', 'title')) {
    if (-not (Test-Property $schema $field)) {
      Add-Issue ([ref]$issues) "$schemaRelativePath missing schema field: $field"
    }
  }

  if (-not (Test-Property $entry 'document_globs')) {
    continue
  }

  $documentMatches = @()
  foreach ($glob in @($entry.document_globs)) {
    $matches = @(Get-TrackedMatches $trackedPaths ([string]$glob))
    if ($matches.Count -eq 0) {
      Add-Issue ([ref]$issues) "$id document_glob has no tracked matches: $glob"
    }
    $documentMatches += $matches
  }

  foreach ($documentRelativePath in @($documentMatches | Sort-Object -Unique)) {
    $documentPath = Join-Path $repoRoot $documentRelativePath
    try {
      $valid = Test-Json -LiteralPath $documentPath -Schema $schemaText -ErrorAction Stop
      if ($valid -ne $true) {
        Add-Issue ([ref]$issues) "$documentRelativePath failed schema validation against $schemaRelativePath"
      }
    } catch {
      Add-Issue ([ref]$issues) "$documentRelativePath failed schema validation against $schemaRelativePath`: $($_.Exception.Message)"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join "`n")
}

Write-Host 'JSON schema manifest OK'
