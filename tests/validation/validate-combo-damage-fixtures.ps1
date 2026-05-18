Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixtureRoot = Join-Path $repoRoot 'evals/fixtures/combo-damage'

function ConvertFrom-ScalarValue {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed -eq 'null') {
    return $null
  }
  if ($trimmed.Length -ge 2 -and $trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }
  if ($trimmed.Length -ge 2 -and $trimmed.StartsWith("'") -and $trimmed.EndsWith("'")) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }
  return $trimmed
}

function Get-SectionLines {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$Section
  )

  $lines = @(($Content -replace "`r`n", "`n") -split "`n")
  $sectionLines = @()
  $inSection = $false

  foreach ($line in $lines) {
    if ($line -match "^$([regex]::Escape($Section)):\s*$") {
      $inSection = $true
      continue
    }

    if ($inSection -and $line -match '^[A-Za-z0-9_]+:') {
      break
    }

    if ($inSection) {
      $sectionLines += $line
    }
  }

  return $sectionLines
}

function Read-TopLevelKeys {
  param([Parameter(Mandatory = $true)][string]$Content)

  $keys = @()
  foreach ($line in (($Content -replace "`r`n", "`n") -split "`n")) {
    if ($line -match '^([A-Za-z0-9_]+):') {
      $keys += $Matches[1]
    }
  }
  return $keys
}

function Read-ScalarMapSection {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$Section
  )

  $result = [ordered]@{}
  foreach ($line in (Get-SectionLines $Content $Section)) {
    if ($line -match '^  ([A-Za-z0-9_]+):\s*(.*)$') {
      $result[$Matches[1]] = ConvertFrom-ScalarValue $Matches[2]
    }
  }
  return $result
}

function Read-SourceRefs {
  param([Parameter(Mandatory = $true)][string]$Content)

  $refs = @()
  foreach ($line in (Get-SectionLines $Content 'source_refs')) {
    if ($line -match '^\s+-\s+(.+)$') {
      $refs += ConvertFrom-ScalarValue $Matches[1]
    }
  }
  return $refs
}

function Read-Cases {
  param([Parameter(Mandatory = $true)][string]$Content)

  $cases = @()
  $current = $null

  foreach ($line in (Get-SectionLines $Content 'cases')) {
    if ($line -match '^  -\s+id:\s*(.*)$') {
      if ($null -ne $current) {
        $cases += $current
      }
      $current = [ordered]@{}
      $current['id'] = ConvertFrom-ScalarValue $Matches[1]
      continue
    }

    if ($null -ne $current -and $line -match '^    ([A-Za-z0-9_]+):\s*(.*)$') {
      $current[$Matches[1]] = ConvertFrom-ScalarValue $Matches[2]
    }
  }

  if ($null -ne $current) {
    $cases += $current
  }

  return $cases
}

function Assert-RequiredKeys {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)]$Map,
    [Parameter(Mandatory = $true)][string[]]$RequiredKeys,
    [Parameter(Mandatory = $true)][ref]$Violations,
    [Parameter(Mandatory = $false)][string]$Context = 'metadata'
  )

  foreach ($key in $RequiredKeys) {
    if ($Map -notcontains $key -and -not ($Map -is [System.Collections.IDictionary] -and $Map.Contains($key))) {
      $Violations.Value += "$RelativePath missing $Context field: $key"
      continue
    }

    if ($Map -is [System.Collections.IDictionary]) {
      $value = $Map[$key]
      if ($null -ne $value -and "$value".Trim().Length -eq 0) {
        $Violations.Value += "$RelativePath has empty $Context field: $key"
      }
    }
  }
}

function Assert-NoBoundaryBreaks {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][ref]$Violations
  )

  foreach ($pattern in @(
    "(?m)^\s*generated_allowed:\s*['""]?true['""]?\s*$",
    '"generated_allowed"\s*:\s*true',
    "(?m)^\s*generated_references_allowed:\s*['""]?true['""]?\s*$",
    '"generated_references_allowed"\s*:\s*true',
    "(?m)^\s*review_status:\s*['""]?accepted['""]?\s*$",
    '"review_status"\s*:\s*"accepted"'
  )) {
    if ($Content -match $pattern) {
      $Violations.Value += "$RelativePath violates combo damage fixture boundary: $pattern"
    }
  }
}

$violations = @()

if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  $violations += 'Missing combo damage fixture directory: evals/fixtures/combo-damage'
}
else {
  $fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.yaml')
  if ($fixtureFiles.Count -eq 0) {
    $violations += 'No combo damage oracle fixtures found under evals/fixtures/combo-damage'
  }

  foreach ($file in $fixtureFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    $topLevelKeys = @(Read-TopLevelKeys $content)

    Assert-RequiredKeys $relativePath $topLevelKeys @(
      'fixture_id',
      'fixture_kind',
      'schema_version',
      'source',
      'scope',
      'boundary',
      'source_refs',
      'cases'
    ) ([ref]$violations) 'top-level'

    if ($content -notmatch '(?m)^fixture_kind:\s*"?combo_damage_oracle"?\s*$') {
      $violations += "$relativePath fixture_kind must be combo_damage_oracle"
    }

    Assert-NoBoundaryBreaks $relativePath $content ([ref]$violations)

    $source = Read-ScalarMapSection $content 'source'
    Assert-RequiredKeys $relativePath $source @('type', 'url', 'video_id', 'title', 'channel', 'character', 'accessed_at') ([ref]$violations) 'source'

    $scope = Read-ScalarMapSection $content 'scope'
    Assert-RequiredKeys $relativePath $scope @('chapter', 'start_time', 'end_time') ([ref]$violations) 'scope'

    $boundary = Read-ScalarMapSection $content 'boundary'
    Assert-RequiredKeys $relativePath $boundary @(
      'not_curated_knowledge',
      'not_current_system_authority',
      'raw_media_stored_in_repo',
      'full_transcript_stored_in_repo',
      'generated_references_allowed'
    ) ([ref]$violations) 'boundary'

    foreach ($expected in @(
      @{ Key = 'not_curated_knowledge'; Value = 'true' },
      @{ Key = 'not_current_system_authority'; Value = 'true' },
      @{ Key = 'raw_media_stored_in_repo'; Value = 'false' },
      @{ Key = 'full_transcript_stored_in_repo'; Value = 'false' },
      @{ Key = 'generated_references_allowed'; Value = 'false' }
    )) {
      if ($boundary.Contains($expected.Key) -and $boundary[$expected.Key] -ne $expected.Value) {
        $violations += "$relativePath boundary.$($expected.Key) must be $($expected.Value)"
      }
    }

    $sourceRefs = @(Read-SourceRefs $content)
    if ($sourceRefs.Count -eq 0) {
      $violations += "$relativePath must include at least one source_refs path"
    }
    foreach ($sourceRef in $sourceRefs) {
      if ($sourceRef -match '^(runtime/generated-knowledge/|skills/sf6-agent/references/generated-)') {
        $violations += "$relativePath source_refs must not point to generated references: $sourceRef"
        continue
      }
      if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $sourceRef) -PathType Leaf)) {
        $violations += "$relativePath references missing source_ref: $sourceRef"
      }
    }

    $cases = @(Read-Cases $content)
    if ($cases.Count -eq 0) {
      $violations += "$relativePath must include at least one combo damage case"
    }

    $requiredCaseFields = @(
      'id',
      'timestamp',
      'combo_notation_jp',
      'combo_notation_normalized',
      'observed_damage',
      'observed_damage_source',
      'damage_visible',
      'enabled_for_damage_hidden_eval',
      'notation_confidence',
      'damage_confidence',
      'review_status',
      'notes'
    )

    foreach ($case in $cases) {
      $caseId = if ($case.Contains('id')) { $case['id'] } else { '<missing id>' }
      Assert-RequiredKeys $relativePath $case $requiredCaseFields ([ref]$violations) "case $caseId"

      if ($case.Contains('review_status') -and $case['review_status'] -eq 'accepted') {
        $violations += "$relativePath case $caseId review_status must not be accepted until fixture-specific accepted state is designed"
      }

      if ($case.Contains('observed_damage') -and $null -ne $case['observed_damage'] -and $case['observed_damage'] -notmatch '^[0-9]+$') {
        $violations += "$relativePath case $caseId observed_damage must be an integer"
      }

      $enabled = $case.Contains('enabled_for_damage_hidden_eval') -and $case['enabled_for_damage_hidden_eval'] -eq 'true'
      if ($enabled) {
        if (-not $case.Contains('combo_notation_normalized') -or $null -eq $case['combo_notation_normalized'] -or "$($case['combo_notation_normalized'])".Trim().Length -eq 0) {
          $violations += "$relativePath case $caseId enabled case requires non-empty combo_notation_normalized"
        }
        if (-not $case.Contains('notation_confidence') -or $case['notation_confidence'] -ne 'high') {
          $violations += "$relativePath case $caseId enabled case requires notation_confidence high"
        }
        if (-not $case.Contains('damage_confidence') -or $case['damage_confidence'] -ne 'high') {
          $violations += "$relativePath case $caseId enabled case requires damage_confidence high"
        }
        if (-not $case.Contains('damage_visible') -or $case['damage_visible'] -ne 'true') {
          $violations += "$relativePath case $caseId enabled case requires damage_visible true"
        }
        if (-not $case.Contains('observed_damage') -or $null -eq $case['observed_damage'] -or $case['observed_damage'] -notmatch '^[1-9][0-9]*$') {
          $violations += "$relativePath case $caseId enabled case requires positive integer observed_damage"
        }
        if (-not $case.Contains('review_status') -or $case['review_status'] -ne 'needs_review') {
          $violations += "$relativePath case $caseId enabled case requires review_status needs_review"
        }
      }
      else {
        if (-not $case.Contains('notes') -or $null -eq $case['notes'] -or "$($case['notes'])".Trim().Length -eq 0) {
          $violations += "$relativePath case $caseId disabled case requires notes explaining uncertainty"
        }
      }
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Combo damage fixtures OK'
