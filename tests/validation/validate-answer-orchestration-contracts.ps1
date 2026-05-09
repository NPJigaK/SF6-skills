Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixtureRoot = 'tests/fixtures/answer-orchestration'

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

$requiredSchemas = @(
  'contracts/answer-intent.schema.json',
  'contracts/evidence-card.schema.json',
  'contracts/answer-plan.schema.json'
)

$requiredDocs = @(
  'contracts/evidence-gate.md',
  'contracts/web-research-policy.md'
)

$requiredFixtures = @(
  'current-fact.json',
  'stable-concept.json',
  'strategy.json',
  'observation.json',
  'hold.json',
  'web-needed.json'
)

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

$issues = @()

foreach ($relativePath in $requiredSchemas) {
  $path = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    $issues += "Missing answer orchestration schema: $relativePath"
    continue
  }

  $schema = Read-Json $relativePath
  foreach ($field in @('$schema', '$id', 'title')) {
    if (-not (Test-Property $schema $field)) {
      $issues += "$relativePath missing schema field: $field"
    }
  }
}

foreach ($relativePath in $requiredDocs) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing answer orchestration policy doc: $relativePath"
  }
}

foreach ($fileName in $requiredFixtures) {
  $relativePath = "$fixtureRoot/$fileName"
  $path = Join-Path $repoRoot $relativePath
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    $issues += "Missing answer orchestration fixture: $relativePath"
    continue
  }

  $fixture = Read-Json $relativePath
  foreach ($field in @('schema_version', 'plan_id', 'answer_mode', 'intent', 'evidence_cards', 'web_research', 'hold_reasons', 'response_requirements')) {
    Assert-Property $fixture $field $relativePath ([ref]$issues)
  }

  if ((Test-Property $fixture 'schema_version') -and $fixture.schema_version -ne 'answer-plan/v1') {
    $issues += "$relativePath must use schema_version answer-plan/v1"
  }

  if (Test-Property $fixture 'answer_mode') {
    Assert-ValueIn $fixture.answer_mode $answerModes "$relativePath answer_mode" ([ref]$issues)
  }

  if (Test-Property $fixture 'intent') {
    foreach ($field in @('schema_version', 'question_text', 'intent_kind', 'answer_mode', 'entities')) {
      Assert-Property $fixture.intent $field "$relativePath intent" ([ref]$issues)
    }
    if ((Test-Property $fixture.intent 'schema_version') -and $fixture.intent.schema_version -ne 'answer-intent/v1') {
      $issues += "$relativePath intent must use schema_version answer-intent/v1"
    }
    if (Test-Property $fixture.intent 'intent_kind') {
      Assert-ValueIn $fixture.intent.intent_kind $answerModes "$relativePath intent_kind" ([ref]$issues)
    }
    if (Test-Property $fixture.intent 'answer_mode') {
      Assert-ValueIn $fixture.intent.answer_mode $answerModes "$relativePath intent answer_mode" ([ref]$issues)
    }
  }

  if (Test-Property $fixture 'evidence_cards') {
    $evidenceCards = @($fixture.evidence_cards)
    if ($evidenceCards.Count -eq 0) {
      $issues += "$relativePath must include at least one evidence card"
    }

    foreach ($card in $evidenceCards) {
      foreach ($field in @('id', 'evidence_family', 'authority_role', 'canonicality', 'source_ref', 'supports_exact_current_fact', 'may_override_official_raw', 'limitations')) {
        Assert-Property $card $field "$relativePath evidence card" ([ref]$issues)
      }

      $family = if (Test-Property $card 'evidence_family') { [string]$card.evidence_family } else { '' }
      if ($family) {
        Assert-ValueIn $family $evidenceFamilies "$relativePath evidence_family" ([ref]$issues)
      }

      if (Test-Property $card 'authority_role') {
        Assert-ValueIn $card.authority_role $authorityRoles "$relativePath authority_role" ([ref]$issues)
      }

      $canonicality = if (Test-Property $card 'canonicality') { [string]$card.canonicality } else { '' }
      if ($canonicality) {
        Assert-ValueIn $canonicality $canonicalityValues "$relativePath canonicality" ([ref]$issues)
      }

      $supportsExact = (Test-Property $card 'supports_exact_current_fact') -and [bool]$card.supports_exact_current_fact
      $mayOverride = (Test-Property $card 'may_override_official_raw') -and [bool]$card.may_override_official_raw

      if ($family -eq 'hermes_memory_session_profile_state') {
        if ($canonicality -notin @('non_canonical', 'forbidden')) {
          $issues += "$relativePath treats Hermes state as canonical evidence"
        }
        if ($supportsExact) {
          $issues += "$relativePath allows Hermes state to support exact current facts"
        }
      }

      if ($family -in @('official_web', 'third_party_community_web')) {
        if ($supportsExact) {
          $issues += "$relativePath allows web evidence to support exact current facts"
        }
        if ($mayOverride) {
          $issues += "$relativePath allows web evidence to override packaged official_raw"
        }
      }

      if ($mayOverride) {
        $issues += "$relativePath contains evidence that may override official_raw"
      }
    }
  }

  if (Test-Property $fixture 'web_research') {
    foreach ($field in @('web_required', 'web_allowed', 'web_used', 'web_forbidden_for_current_fact_override', 'conflict_requires_hold')) {
      Assert-Property $fixture.web_research $field "$relativePath web_research" ([ref]$issues)
    }

    if (Test-Property $fixture.web_research 'required_source_authority') {
      Assert-ValueIn $fixture.web_research.required_source_authority $sourceAuthorityValues "$relativePath required_source_authority" ([ref]$issues)
    }

    if ((Test-Property $fixture.web_research 'web_forbidden_for_current_fact_override') -and -not [bool]$fixture.web_research.web_forbidden_for_current_fact_override) {
      $issues += "$relativePath must forbid web current-fact override"
    }

    if ((Test-Property $fixture.web_research 'conflict_requires_hold') -and -not [bool]$fixture.web_research.conflict_requires_hold) {
      $issues += "$relativePath must hold on web/current-fact conflict"
    }
  }

  if (Test-Property $fixture 'response_requirements') {
    foreach ($field in @('cite_evidence', 'state_authority_boundary', 'state_confidence', 'boundary_notes')) {
      Assert-Property $fixture.response_requirements $field "$relativePath response_requirements" ([ref]$issues)
    }
  }

  if ($fileName -eq 'current-fact.json') {
    $officialRawCards = @($fixture.evidence_cards | Where-Object {
      $sourcePath = if (Test-Property $_.source_ref 'path') { [string]$_.source_ref.path } else { '' }
      $_.evidence_family -eq 'frame_current_official_raw' -and
      $_.supports_exact_current_fact -eq $true -and
      $sourcePath -match '^skills/sf6-agent/assets/frame-current/published/.+/official_raw\.json$' -and
      (Test-Path -LiteralPath (Join-Path $repoRoot $sourcePath) -PathType Leaf)
    })
    if ($officialRawCards.Count -eq 0) {
      $issues += 'current-fact fixture must contain existing packaged frame-current official_raw evidence'
    }
  }

  if ($fileName -eq 'hold.json') {
    if (-not (Test-Property $fixture 'hold_reasons') -or @($fixture.hold_reasons).Count -eq 0) {
      $issues += 'hold fixture must include hold reasons'
    }
  }

  if ($fileName -eq 'web-needed.json') {
    $webRequired = (Test-Property $fixture.web_research 'web_required') -and [bool]$fixture.web_research.web_required
    $webAllowed = (Test-Property $fixture.web_research 'web_allowed') -and [bool]$fixture.web_research.web_allowed
    if (-not ($webRequired -or $webAllowed)) {
      $issues += 'web-needed fixture must mark web required or web allowed'
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Answer orchestration contracts OK'
