Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$aliasesRoot = 'data/aliases'
$fixturePath = 'data/aliases/ja-query-fixtures.json'
$schemaPath = 'contracts/normalization-aliases.schema.json'

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

function Get-RelativePath {
  param(
    [Parameter(Mandatory = $true)][string]$RootPath,
    [Parameter(Mandatory = $true)][string]$FullPath
  )

  $root = (Resolve-Path $RootPath).Path.TrimEnd([char[]]@('\', '/'))
  $relative = $FullPath.Substring($root.Length)
  $relative = $relative -replace '^[\\/]+', ''
  return $relative -replace '\\', '/'
}

$issues = @()
$allowedAliasKinds = @('character', 'move_input', 'field', 'term', 'query_fixture')
$allowedNormalizedProperties = @(
  'character_slug',
  'move_input',
  'field',
  'term_key',
  'question_text'
)
$expectedQuery = -join ([int[]]@(
  0x30EA,
  0x30E5,
  0x30A6,
  0x306E,
  0x5C48,
  0x4E2D,
  0x0050,
  0x3063,
  0x3066,
  0x30AC,
  0x30FC,
  0x30C9,
  0x3067,
  0x4F55,
  0x0046,
  0xFF1F
) | ForEach-Object { [char]$_ })
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

foreach ($relativePath in @('data/aliases/README.md', $schemaPath, $fixturePath)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing normalization alias file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $schemaPath) -PathType Leaf) {
  $schema = Read-Json $schemaPath
  foreach ($field in @('$schema', '$id', 'title')) {
    Assert-Property $schema $field $schemaPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'data/aliases/README.md') -PathType Leaf) {
  $readme = Get-Content -LiteralPath (Join-Path $repoRoot 'data/aliases/README.md') -Raw -Encoding UTF8
  foreach ($needle in @(
    'canonical query-normalization support',
    'not exact current-fact authority',
    'data/exports/',
    'data/roster/',
    'skills/sf6-agent/assets/normalization/',
    'skills/sf6-agent/assets/frame-current/'
  )) {
    if ($readme -notmatch [regex]::Escape($needle)) {
      $issues += "data/aliases/README.md missing boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $fixturePath) -PathType Leaf) {
  $fixtureRaw = Get-Content -LiteralPath (Join-Path $repoRoot $fixturePath) -Raw -Encoding UTF8
  $fixture = $fixtureRaw | ConvertFrom-Json

  foreach ($field in @('schema_version', 'kind', 'authority', 'not_current_fact_authority', 'entries')) {
    Assert-Property $fixture $field $fixturePath ([ref]$issues)
  }

  if ((Test-Property $fixture 'schema_version') -and $fixture.schema_version -ne 'normalization-aliases/v1') {
    $issues += "$fixturePath must use schema_version normalization-aliases/v1"
  }
  if ((Test-Property $fixture 'kind') -and $fixture.kind -ne 'query_normalization_aliases') {
    $issues += "$fixturePath must use kind query_normalization_aliases"
  }
  if ((Test-Property $fixture 'authority') -and $fixture.authority -ne 'query_normalization_only') {
    $issues += "$fixturePath must use authority query_normalization_only"
  }
  if (
    (Test-Property $fixture 'not_current_fact_authority') -and
    ((-not ($fixture.not_current_fact_authority -is [bool])) -or $fixture.not_current_fact_authority -ne $true)
  ) {
    $issues += "$fixturePath must set not_current_fact_authority to boolean true"
  }

  foreach ($token in $forbiddenTokens) {
    $escapedToken = [regex]::Escape($token)
    if ($fixtureRaw -match ('(?i)"[^"]*' + $escapedToken + '[^"]*"')) {
      $issues += "$fixturePath contains forbidden exact-current-fact token: $token"
    }
  }

  if (Test-Property $fixture 'entries') {
    $entries = @($fixture.entries)
    if ($entries.Count -eq 0) {
      $issues += "$fixturePath must include at least one alias entry"
    }

    foreach ($entry in $entries) {
      $entryId = if (Test-Property $entry 'id') { [string]$entry.id } else { '<missing-id>' }
      foreach ($field in @('id', 'alias_kind', 'aliases', 'normalized')) {
        Assert-Property $entry $field "$fixturePath entry $entryId" ([ref]$issues)
      }

      if (Test-Property $entry 'alias_kind') {
        $aliasKind = [string]$entry.alias_kind
        if ($allowedAliasKinds -notcontains $aliasKind) {
          $issues += "$fixturePath entry $entryId has invalid alias_kind: $aliasKind"
        }
      }

      if ((Test-Property $entry 'aliases') -and @($entry.aliases).Count -eq 0) {
        $issues += "$fixturePath entry $entryId must include aliases"
      }

      if (Test-Property $entry 'normalized') {
        $normalizedProperties = @($entry.normalized.PSObject.Properties.Name)
        if ($normalizedProperties.Count -eq 0) {
          $issues += "$fixturePath entry $entryId must include normalized properties"
        }
        foreach ($propertyName in $normalizedProperties) {
          if ($allowedNormalizedProperties -notcontains $propertyName) {
            $issues += "$fixturePath entry $entryId has invalid normalized property: $propertyName"
          }
          if ($forbiddenTokens -contains $propertyName) {
            $issues += "$fixturePath entry $entryId uses forbidden normalized property: $propertyName"
          }
        }
      }
    }

    $queryFixture = @($entries | Where-Object {
      (Test-Property $_ 'alias_kind') -and
      $_.alias_kind -eq 'query_fixture' -and
      (Test-Property $_ 'aliases') -and
      @($_.aliases) -contains $expectedQuery
    })

    if ($queryFixture.Count -eq 0) {
      $issues += "$fixturePath must include the expected Japanese Ryu 2MP block query fixture"
    } else {
      $normalized = $queryFixture[0].normalized
      $expectedNormalized = @{
        character_slug = 'ryu'
        move_input = '2MP'
        field = 'block_adv'
      }
      foreach ($propertyName in $expectedNormalized.Keys) {
        if (-not (Test-Property $normalized $propertyName)) {
          $issues += "query fixture missing normalized property: $propertyName"
        } elseif ([string]$normalized.$propertyName -ne $expectedNormalized[$propertyName]) {
          $issues += "query fixture must map $propertyName to $($expectedNormalized[$propertyName])"
        }
      }
    }
  }
}

$aliasesPath = Join-Path $repoRoot $aliasesRoot
if (Test-Path -LiteralPath $aliasesPath -PathType Container) {
  foreach ($item in Get-ChildItem -LiteralPath $aliasesPath -Recurse -Force) {
    $relativePath = Get-RelativePath $aliasesPath $item.FullName
    $relativePathLower = $relativePath.ToLowerInvariant()
    if (
      $relativePathLower -like '*generated*' -or
      $relativePathLower -like '*runtime*' -or
      $relativePathLower -like '*compiled*' -or
      $relativePathLower -like '*.bundle*' -or
      $relativePathLower -like '*.min.json'
    ) {
      $issues += "data/aliases contains generated-runtime-looking path: $relativePath"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'skills/sf6-agent/assets/normalization')) {
  $issues += 'skills/sf6-agent/assets/normalization/ must not be created by this issue'
}

if (Get-Command git -ErrorAction SilentlyContinue) {
  $frameCurrentStatus = @(& git -C $repoRoot status --porcelain -- 'skills/sf6-agent/assets/frame-current')
  if ($LASTEXITCODE -ne 0) {
    $issues += 'Unable to inspect frame-current status'
  } elseif ($frameCurrentStatus.Count -gt 0) {
    $issues += 'skills/sf6-agent/assets/frame-current/ has residual diff'
  }
} else {
  Write-Host 'WARNING: git is unavailable; skipping frame-current status check'
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Normalization aliases OK'
