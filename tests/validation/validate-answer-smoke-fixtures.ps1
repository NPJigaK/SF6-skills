Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixtureRootRelativePath = 'tests/fixtures/answer-smoke'
$fixtureRoot = Join-Path $repoRoot $fixtureRootRelativePath
$templateRelativePath = 'docs/testing/smoke-runs/answer-smoke-template.md'
$normalizationManifestRelativePath = 'runtime/normalization/runtime_manifest.json'
$normalizationAssetRelativePath = 'runtime/normalization/aliases.json'

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

function Assert-ValueIn {
  param(
    [Parameter(Mandatory = $true)][object]$Value,
    [Parameter(Mandatory = $true)][string[]]$AllowedValues,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if ($AllowedValues -notcontains [string]$Value) {
    $Issues.Value += "$Context has invalid value: $Value"
  }
}

function Assert-PathExists {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $RelativePath) -PathType Leaf)) {
    $Issues.Value += "$Context path does not exist: $RelativePath"
  }
}

function Get-StringArray {
  param([AllowNull()][object]$Value)
  if ($null -eq $Value) {
    return @()
  }
  return @($Value | ForEach-Object { [string]$_ })
}

function Test-NormalizedValue {
  param(
    [Parameter(Mandatory = $true)][object]$Normalized,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string]$Expected
  )

  return (
    (Test-Property $Normalized $Name) -and
    [string]$Normalized.$Name -eq $Expected
  )
}

$requiredCoverage = @(
  'current_fact',
  'stable_concept',
  'strategy',
  'hold',
  'web_needed',
  'japanese_query_normalization'
)

$allowedCoverage = $requiredCoverage
$allowedSmokeLevel = 'contract_fixture'
$answerModes = @(
  'current_fact',
  'stable_concept',
  'strategy',
  'observation',
  'hold',
  'web_needed'
)
$evidenceFamilies = @(
  'frame_current_official_raw',
  'frame_current_derived_metrics',
  'generated_curated_reference',
  'review_claim',
  'video_observation',
  'official_web',
  'third_party_community_web',
  'hermes_memory_session_profile_state',
  'repo_policy',
  'unknown'
)
$authorityRoles = @(
  'primary_current_fact_authority',
  'derived_current_fact_support',
  'stable_concept_support',
  'strategy_support',
  'observation_only',
  'review_only',
  'official_metadata',
  'supplemental_context',
  'forbidden_non_canonical',
  'unresolved_context'
)
$canonicalityValues = @(
  'canonical_repo_source',
  'packaged_runtime_authority',
  'derived_reference',
  'review_only',
  'observation_only',
  'supplemental',
  'non_canonical',
  'forbidden'
)
$sourceAuthorityValues = @(
  'none',
  'official_sources_required',
  'supplemental_sources_allowed'
)
$forbiddenRawPatterns = @(
  '"startup"\s*:',
  '"active"\s*:',
  '"recovery"\s*:',
  '"hit_adv"\s*:',
  '"block_adv_value"\s*:',
  '"damage"\s*:',
  '"frame_value"\s*:',
  '"patch_value"\s*:',
  '"tier"\s*:',
  '"matchup_judgment"\s*:',
  '"matchup_verdict"\s*:',
  '"strategy_conclusion_authority"\s*:\s*true',
  '"answer_text"\s*:',
  '"executed_output"\s*:'
)

$issues = @()
$coverageSeen = @{}
foreach ($coverage in $requiredCoverage) {
  $coverageSeen[$coverage] = $false
}

if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  $issues += "Missing answer smoke fixture directory: $fixtureRootRelativePath"
}

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $templateRelativePath) -PathType Leaf)) {
  $issues += "Missing answer smoke template: $templateRelativePath"
} else {
  $templateText = Get-Content -LiteralPath (Join-Path $repoRoot $templateRelativePath) -Raw -Encoding UTF8
  foreach ($requiredText in @(
    'template, not an executed smoke report',
    'does not represent live Hermes execution',
    'does not represent live web research',
    'Fixture Set',
    'Validators Run',
    'Warnings',
    'Unresolved Items',
    'Generated-Surface Status'
  )) {
    if ($templateText -notmatch [regex]::Escape($requiredText)) {
      $issues += "$templateRelativePath must mention: $requiredText"
    }
  }
}

Assert-PathExists $normalizationManifestRelativePath 'Japanese normalization smoke' ([ref]$issues)
Assert-PathExists $normalizationAssetRelativePath 'Japanese normalization smoke' ([ref]$issues)
$normalizationRuntimeAssets = $null
if (Test-Path -LiteralPath (Join-Path $repoRoot $normalizationAssetRelativePath) -PathType Leaf) {
  $normalizationRuntimeAssets = Read-Json $normalizationAssetRelativePath
}

if (Test-Path -LiteralPath $fixtureRoot -PathType Container) {
  $fixtureFiles = @(
    Get-ChildItem -LiteralPath $fixtureRoot -Filter '*.json' -File |
      Sort-Object Name
  )

  if ($fixtureFiles.Count -eq 0) {
    $issues += "$fixtureRootRelativePath must include answer smoke JSON fixtures"
  }

  foreach ($fixtureFile in $fixtureFiles) {
    $relativePath = $fixtureFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $raw = Get-Content -LiteralPath $fixtureFile.FullName -Raw -Encoding UTF8
    $fixture = $raw | ConvertFrom-Json

    foreach ($pattern in $forbiddenRawPatterns) {
      if ($raw -match $pattern) {
        $issues += "$relativePath contains forbidden executed-output or exact-current-fact field pattern: $pattern"
      }
    }

    foreach ($field in @('schema_version', 'fixture_id', 'coverage', 'smoke_level', 'execution', 'answer_plan', 'smoke_expectations')) {
      Assert-Property $fixture $field $relativePath ([ref]$issues)
    }

    if ((Test-Property $fixture 'schema_version') -and $fixture.schema_version -ne 'answer-smoke-fixture/v1') {
      $issues += "$relativePath must use schema_version answer-smoke-fixture/v1"
    }
    if ((Test-Property $fixture 'smoke_level') -and $fixture.smoke_level -ne $allowedSmokeLevel) {
      $issues += "$relativePath must use smoke_level $allowedSmokeLevel"
    }
    if (Test-Property $fixture 'coverage') {
      Assert-ValueIn $fixture.coverage $allowedCoverage "$relativePath coverage" ([ref]$issues)
      if ($coverageSeen.ContainsKey([string]$fixture.coverage)) {
        $coverageSeen[[string]$fixture.coverage] = $true
      }
    }

    if (Test-Property $fixture 'execution') {
      foreach ($field in @('requires_live_hermes', 'requires_live_web_research', 'is_executed_answer')) {
        Assert-Property $fixture.execution $field "$relativePath execution" ([ref]$issues)
      }
      if ((Test-Property $fixture.execution 'requires_live_hermes') -and [bool]$fixture.execution.requires_live_hermes) {
        $issues += "$relativePath must not require live Hermes execution"
      }
      if ((Test-Property $fixture.execution 'requires_live_web_research') -and [bool]$fixture.execution.requires_live_web_research) {
        $issues += "$relativePath must not require live web research"
      }
      if ((Test-Property $fixture.execution 'is_executed_answer') -and [bool]$fixture.execution.is_executed_answer) {
        $issues += "$relativePath must be a fixture skeleton, not an executed answer"
      }
    }

    if (-not (Test-Property $fixture 'answer_plan')) {
      continue
    }

    $plan = $fixture.answer_plan
    foreach ($field in @('schema_version', 'plan_id', 'answer_mode', 'intent', 'evidence_cards', 'web_research', 'hold_reasons', 'response_requirements')) {
      Assert-Property $plan $field "$relativePath answer_plan" ([ref]$issues)
    }
    if ((Test-Property $plan 'schema_version') -and $plan.schema_version -ne 'answer-plan/v1') {
      $issues += "$relativePath answer_plan must use schema_version answer-plan/v1"
    }
    if (Test-Property $plan 'answer_mode') {
      Assert-ValueIn $plan.answer_mode $answerModes "$relativePath answer_mode" ([ref]$issues)
    }

    if (Test-Property $plan 'intent') {
      foreach ($field in @('schema_version', 'question_text', 'intent_kind', 'answer_mode', 'entities')) {
        Assert-Property $plan.intent $field "$relativePath intent" ([ref]$issues)
      }
      if ((Test-Property $plan.intent 'schema_version') -and $plan.intent.schema_version -ne 'answer-intent/v1') {
        $issues += "$relativePath intent must use schema_version answer-intent/v1"
      }
      if (Test-Property $plan.intent 'intent_kind') {
        Assert-ValueIn $plan.intent.intent_kind $answerModes "$relativePath intent_kind" ([ref]$issues)
      }
      if (Test-Property $plan.intent 'answer_mode') {
        Assert-ValueIn $plan.intent.answer_mode $answerModes "$relativePath intent answer_mode" ([ref]$issues)
      }
    }

    $evidenceCards = @()
    if (Test-Property $plan 'evidence_cards') {
      $evidenceCards = @($plan.evidence_cards)
      if ($evidenceCards.Count -eq 0) {
        $issues += "$relativePath answer_plan must include at least one evidence card"
      }
      foreach ($card in $evidenceCards) {
        foreach ($field in @('id', 'evidence_family', 'authority_role', 'canonicality', 'source_ref', 'supports_exact_current_fact', 'may_override_official_raw', 'limitations')) {
          Assert-Property $card $field "$relativePath evidence card" ([ref]$issues)
        }

        $family = if (Test-Property $card 'evidence_family') { [string]$card.evidence_family } else { '' }
        $canonicality = if (Test-Property $card 'canonicality') { [string]$card.canonicality } else { '' }
        if ($family) {
          Assert-ValueIn $family $evidenceFamilies "$relativePath evidence_family" ([ref]$issues)
        }
        if (Test-Property $card 'authority_role') {
          Assert-ValueIn $card.authority_role $authorityRoles "$relativePath authority_role" ([ref]$issues)
        }
        if ($canonicality) {
          Assert-ValueIn $canonicality $canonicalityValues "$relativePath canonicality" ([ref]$issues)
        }

        $supportsExact = (Test-Property $card 'supports_exact_current_fact') -and [bool]$card.supports_exact_current_fact
        $mayOverride = (Test-Property $card 'may_override_official_raw') -and [bool]$card.may_override_official_raw

        if ($supportsExact -and $family -ne 'frame_current_official_raw') {
          $issues += "$relativePath allows non-official_raw evidence to support exact current facts: $family"
        }
        if ($family -eq 'generated_curated_reference' -and $supportsExact) {
          $issues += "$relativePath allows generated reference to support exact current facts"
        }
        if ($family -in @('official_web', 'third_party_community_web') -and $supportsExact) {
          $issues += "$relativePath allows web evidence to support exact current facts"
        }
        if ($family -in @('official_web', 'third_party_community_web') -and $mayOverride) {
          $issues += "$relativePath allows web evidence to override official_raw"
        }
        if ($mayOverride) {
          $issues += "$relativePath contains evidence that may override official_raw"
        }

        if (Test-Property $card 'source_ref') {
          if (Test-Property $card.source_ref 'path') {
            $sourcePath = [string]$card.source_ref.path
            if ($sourcePath -match '^runtime/frame-current/published/.+/official_raw\.json$') {
              Assert-PathExists $sourcePath "$relativePath official_raw evidence" ([ref]$issues)
            }
            if ($sourcePath -eq 'runtime/generated-knowledge/generated-concepts.md') {
              Assert-PathExists $sourcePath "$relativePath generated reference evidence" ([ref]$issues)
            }
          }
        }
      }
    }

    if (Test-Property $plan 'web_research') {
      foreach ($field in @('web_required', 'web_allowed', 'web_used', 'web_forbidden_for_current_fact_override', 'conflict_requires_hold')) {
        Assert-Property $plan.web_research $field "$relativePath web_research" ([ref]$issues)
      }
      if (Test-Property $plan.web_research 'required_source_authority') {
        Assert-ValueIn $plan.web_research.required_source_authority $sourceAuthorityValues "$relativePath required_source_authority" ([ref]$issues)
      }
      if ((Test-Property $plan.web_research 'web_used') -and [bool]$plan.web_research.web_used) {
        $issues += "$relativePath must not record live web research as already used"
      }
      if ((Test-Property $plan.web_research 'web_forbidden_for_current_fact_override') -and -not [bool]$plan.web_research.web_forbidden_for_current_fact_override) {
        $issues += "$relativePath must forbid web current-fact override"
      }
      if ((Test-Property $plan.web_research 'conflict_requires_hold') -and -not [bool]$plan.web_research.conflict_requires_hold) {
        $issues += "$relativePath must hold on web/current-fact conflict"
      }
    }

    if (Test-Property $plan 'response_requirements') {
      foreach ($field in @('cite_evidence', 'state_authority_boundary', 'state_confidence', 'boundary_notes')) {
        Assert-Property $plan.response_requirements $field "$relativePath response_requirements" ([ref]$issues)
      }
    }

    $coverage = if (Test-Property $fixture 'coverage') { [string]$fixture.coverage } else { '' }
    if ($coverage -eq 'current_fact') {
      $officialRawCards = @($evidenceCards | Where-Object {
        $sourcePath = if (Test-Property $_.source_ref 'path') { [string]$_.source_ref.path } else { '' }
        $_.evidence_family -eq 'frame_current_official_raw' -and
        $_.supports_exact_current_fact -eq $true -and
        $sourcePath -match '^runtime/frame-current/published/.+/official_raw\.json$' -and
        (Test-Path -LiteralPath (Join-Path $repoRoot $sourcePath) -PathType Leaf)
      })
      if ($officialRawCards.Count -eq 0) {
        $issues += "$relativePath current_fact fixture must reference packaged official_raw"
      }
      if ((Test-Property $plan.web_research 'web_required') -and [bool]$plan.web_research.web_required) {
        $issues += "$relativePath current_fact fixture must not require web research"
      }
    }

    if ($coverage -eq 'stable_concept') {
      $generatedCards = @($evidenceCards | Where-Object {
        $_.evidence_family -eq 'generated_curated_reference' -and
        $_.supports_exact_current_fact -eq $false
      })
      if ($generatedCards.Count -eq 0) {
        $issues += "$relativePath stable_concept fixture must use generated references without exact current-fact authority"
      }
    }

    if ($coverage -eq 'strategy') {
      if (-not (Test-Property $fixture.smoke_expectations 'assumptions') -or @($fixture.smoke_expectations.assumptions).Count -eq 0) {
        $issues += "$relativePath strategy fixture must list assumptions"
      }
      if (-not (Test-Property $fixture.smoke_expectations 'confidence_boundaries') -or @($fixture.smoke_expectations.confidence_boundaries).Count -eq 0) {
        $issues += "$relativePath strategy fixture must list confidence boundaries"
      }
      if ((Test-Property $fixture.smoke_expectations 'strategy_conclusion_as_authority') -and [bool]$fixture.smoke_expectations.strategy_conclusion_as_authority) {
        $issues += "$relativePath strategy fixture must not present conclusions as authority"
      }
    }

    if ($coverage -eq 'hold') {
      if (-not (Test-Property $plan 'hold_reasons') -or @($plan.hold_reasons).Count -eq 0) {
        $issues += "$relativePath hold fixture must include hold reasons"
      }
    }

    if ($coverage -eq 'web_needed') {
      if (-not ((Test-Property $plan.web_research 'web_required') -and [bool]$plan.web_research.web_required)) {
        $issues += "$relativePath web_needed fixture must mark web_required true"
      }
      if (-not ((Test-Property $plan.web_research 'web_forbidden_for_current_fact_override') -and [bool]$plan.web_research.web_forbidden_for_current_fact_override)) {
        $issues += "$relativePath web_needed fixture must forbid official_raw override"
      }
    }

    if ($coverage -eq 'japanese_query_normalization') {
      foreach ($field in @('source_manifest', 'source_asset', 'runtime_authority', 'not_current_fact_authority', 'structured_inputs')) {
        Assert-Property $fixture.normalization $field "$relativePath normalization" ([ref]$issues)
      }
      if ((Test-Property $fixture.normalization 'source_manifest') -and $fixture.normalization.source_manifest -ne $normalizationManifestRelativePath) {
        $issues += "$relativePath must reference $normalizationManifestRelativePath"
      }
      if ((Test-Property $fixture.normalization 'source_asset') -and $fixture.normalization.source_asset -ne $normalizationAssetRelativePath) {
        $issues += "$relativePath must reference $normalizationAssetRelativePath"
      }
      if ((Test-Property $fixture.normalization 'runtime_authority') -and $fixture.normalization.runtime_authority -ne 'query_normalization_only') {
        $issues += "$relativePath normalization authority must be query_normalization_only"
      }
      if ((Test-Property $fixture.normalization 'not_current_fact_authority') -and $fixture.normalization.not_current_fact_authority -ne $true) {
        $issues += "$relativePath normalization must be marked not_current_fact_authority"
      }
      if (Test-Property $fixture.normalization 'structured_inputs') {
        $structured = $fixture.normalization.structured_inputs
        foreach ($field in @('character_slug', 'move_input', 'field')) {
          Assert-Property $structured $field "$relativePath structured_inputs" ([ref]$issues)
        }
        if ((Test-Property $plan 'intent') -and (Test-Property $plan.intent 'entities')) {
          foreach ($field in @('character_slug', 'move_input')) {
            if ((Test-Property $structured $field) -and (Test-Property $plan.intent.entities $field)) {
              if ([string]$structured.$field -ne [string]$plan.intent.entities.$field) {
                $issues += "$relativePath structured input mismatch for $field"
              }
            }
          }
          if (
            (Test-Property $structured 'field') -and
            (Test-Property $plan.intent.entities 'requested_field') -and
            [string]$structured.field -ne [string]$plan.intent.entities.requested_field
          ) {
            $issues += "$relativePath normalization field must map to intent requested_field"
          }
        }
      }
      if (
        (Test-Property $plan 'intent') -and
        (Test-Property $plan.intent 'question_text') -and
        (Test-Property $fixture.normalization 'structured_inputs') -and
        $null -ne $normalizationRuntimeAssets -and
        (Test-Property $normalizationRuntimeAssets 'entries')
      ) {
        $structured = $fixture.normalization.structured_inputs
        $runtimeMatches = @($normalizationRuntimeAssets.entries | Where-Object {
          $_.alias_kind -eq 'query_fixture' -and
          @($_.aliases) -contains [string]$plan.intent.question_text -and
          (Test-Property $_ 'normalized') -and
          (Test-NormalizedValue $_.normalized 'character_slug' ([string]$structured.character_slug)) -and
          (Test-NormalizedValue $_.normalized 'move_input' ([string]$structured.move_input)) -and
          (Test-NormalizedValue $_.normalized 'field' ([string]$structured.field))
        })
        if ($runtimeMatches.Count -eq 0) {
          $issues += "$relativePath must match a query_fixture entry in $normalizationAssetRelativePath"
        }
      }
    }
  }
}

foreach ($coverage in $requiredCoverage) {
  if (-not $coverageSeen[$coverage]) {
    $issues += "$fixtureRootRelativePath missing coverage: $coverage"
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Answer smoke fixtures OK'
