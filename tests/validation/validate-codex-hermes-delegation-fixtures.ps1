Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixtureRootRelative = 'tests/fixtures/codex-hermes-delegation'
$fixtureRoot = Join-Path $repoRoot $fixtureRootRelative

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

function Assert-BooleanValue {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][bool]$Expected,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
    return
  }

  if ([bool]$Object.$Name -ne $Expected) {
    $Issues.Value += "$Context.$Name must be $Expected"
  }
}

function Assert-ArrayNotEmpty {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
    return
  }

  if (@($Object.$Name).Count -eq 0) {
    $Issues.Value += "$Context.$Name must not be empty"
  }
}

function Read-Fixture {
  param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8
  $json = $raw | ConvertFrom-Json
  return @{
    Raw = $raw
    Json = $json
    RelativePath = $File.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  }
}

$expectedFixtures = [ordered]@{
  'source-analysis-valid.json' = 'source_analysis'
  'validator-pattern-proposal.json' = 'validator_pattern'
  'video-analyze-unavailable-fallback.json' = 'video_fallback'
  'video-current-fact-forbidden.json' = 'video_current_fact_forbidden'
  'external-atlas-binary-import-forbidden.json' = 'external_atlas_binary_forbidden'
  'external-atlas-metadata-only-guidance.json' = 'external_atlas_metadata_only'
  'stale-pr-active-source-rejection.json' = 'stale_pr_rejection'
  'video-observed-damage-label-boundary.json' = 'observed_damage_label_boundary'
  'move-frequency-review-only.json' = 'move_frequency_review_only'
}

$allowedScenarioKinds = @(
  'source_analysis',
  'validator_pattern',
  'video_fallback',
  'video_current_fact_forbidden',
  'external_atlas_binary_forbidden',
  'external_atlas_metadata_only',
  'stale_pr_rejection',
  'observed_damage_label_boundary',
  'move_frequency_review_only'
)

$allowedOutcomeStatuses = @(
  'accept_draft',
  'reject',
  'hold',
  'metadata_only_guidance'
)

$issues = @()

if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  $issues += "Missing Codex-Hermes delegation fixture directory: $fixtureRootRelative"
}

foreach ($fileName in $expectedFixtures.Keys) {
  $path = Join-Path $fixtureRoot $fileName
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    $issues += "Missing Codex-Hermes delegation fixture: $fixtureRootRelative/$fileName"
  }
}

if ($issues.Count -eq 0) {
  $fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -Filter '*.json' -File | Sort-Object Name)

  foreach ($file in $fixtureFiles) {
    $fixtureRecord = Read-Fixture $file
    $raw = [string]$fixtureRecord.Raw
    $fixture = $fixtureRecord.Json
    $relativePath = [string]$fixtureRecord.RelativePath
    $rawLower = $raw.ToLowerInvariant()

    foreach ($field in @(
      'schema_version',
      'scenario_id',
      'scenario_kind',
      'codex_request',
      'hermes_draft_response',
      'post_delegation_review',
      'expected_boundary_outcome'
    )) {
      Assert-Property $fixture $field $relativePath ([ref]$issues)
    }

    if ((Test-Property $fixture 'schema_version') -and [string]$fixture.schema_version -ne 'codex-hermes-delegation-fixture/v1') {
      $issues += "$relativePath must use schema_version codex-hermes-delegation-fixture/v1"
    }

    if (Test-Property $fixture 'scenario_kind') {
      $kind = [string]$fixture.scenario_kind
      if ($allowedScenarioKinds -notcontains $kind) {
        $issues += "$relativePath has invalid scenario_kind: $kind"
      }

      $expectedName = $file.Name
      if ($expectedFixtures.Contains($expectedName) -and $expectedFixtures[$expectedName] -ne $kind) {
        $issues += "$relativePath expected scenario_kind $($expectedFixtures[$expectedName]) but found $kind"
      }
    }

    if (Test-Property $fixture 'codex_request') {
      foreach ($field in @(
        'target_issue',
        'target_scope_summary',
        'source_material',
        'requested_artifact_type',
        'allowed_outputs',
        'forbidden_outputs',
        'authority_boundaries',
        'validators_to_run',
        'review_checklist'
      )) {
        Assert-Property $fixture.codex_request $field "$relativePath codex_request" ([ref]$issues)
      }
    }

    if (Test-Property $fixture 'hermes_draft_response') {
      foreach ($field in @(
        'summary',
        'proposed_artifacts',
        'source_refs',
        'evidence_candidate_notes',
        'uncertainty_or_hold_reasons',
        'boundary_notes',
        'follow_up_recommendations'
      )) {
        Assert-Property $fixture.hermes_draft_response $field "$relativePath hermes_draft_response" ([ref]$issues)
      }
    }

    if (Test-Property $fixture 'post_delegation_review') {
      Assert-BooleanValue $fixture.post_delegation_review 'hermes_output_is_draft_input' $true "$relativePath post_delegation_review" ([ref]$issues)
      Assert-BooleanValue $fixture.post_delegation_review 'canonical_promotion_allowed' $false "$relativePath post_delegation_review" ([ref]$issues)
      Assert-BooleanValue $fixture.post_delegation_review 'requires_codex_review' $true "$relativePath post_delegation_review" ([ref]$issues)
      Assert-BooleanValue $fixture.post_delegation_review 'requires_validators' $true "$relativePath post_delegation_review" ([ref]$issues)
      Assert-BooleanValue $fixture.post_delegation_review 'local_state_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
      Assert-BooleanValue $fixture.post_delegation_review 'raw_transcript_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
    }

    if (Test-Property $fixture 'expected_boundary_outcome') {
      Assert-Property $fixture.expected_boundary_outcome 'status' "$relativePath expected_boundary_outcome" ([ref]$issues)
      Assert-Property $fixture.expected_boundary_outcome 'reason' "$relativePath expected_boundary_outcome" ([ref]$issues)

      if ((Test-Property $fixture.expected_boundary_outcome 'status') -and $allowedOutcomeStatuses -notcontains [string]$fixture.expected_boundary_outcome.status) {
        $issues += "$relativePath has invalid expected_boundary_outcome.status: $($fixture.expected_boundary_outcome.status)"
      }
    }

    foreach ($marker in @('RAW TRANSCRIPT', 'assistant:', 'user:', 'tool_call')) {
      if ($raw -match [regex]::Escape($marker)) {
        $issues += "$relativePath contains raw transcript marker: $marker"
      }
    }

    foreach ($pattern in @(
      '"requires_live_hermes"\s*:\s*true',
      '"requires_live_web_research"\s*:\s*true',
      '"requires_live_video_analysis"\s*:\s*true',
      '"video_analyze_tested"\s*:\s*true',
      '(?i)live hermes execution is required',
      '(?i)live web research is required',
      '(?i)live video analysis is required'
    )) {
      if ($raw -match $pattern) {
        $issues += "$relativePath requires live execution outside dry-run scope: $pattern"
      }
    }

    foreach ($pattern in @(
      '(^|[\\/])\.env($|[\\/])',
      '\.sqlite\b',
      '\.db\b',
      '(?i)\b[A-Za-z0-9_\-./\\]*(secret|token|credential)[A-Za-z0-9_\-./\\]*[\\/]'
    )) {
      if ($raw -match $pattern) {
        $issues += "$relativePath contains local secret/state path-like pattern: $pattern"
      }
    }

    $activeStoragePattern = '(?im)^\s*(?:[-*+]\s+|\d+[.)]\s+)?(commit|store|save|persist|include|write|add)\b.*\b(sessions?|memory|local skills?|curator|checkpoints?|kanban state|logs?|caches?|credentials?|secrets?|tokens?)\b'
    foreach ($line in ($raw -split "`r?`n")) {
      if ($line -match $activeStoragePattern -and $line -notmatch '(?i)\b(do not|must not|forbid|forbidden|not|no|reject|rejection)\b') {
        $issues += "Potential active local-state storage instruction in ${relativePath}: $line"
      }
    }

    if ($raw -match '(?i)[A-Za-z0-9_\-./\\]+\.(gif|png|jpg|jpeg|webp|mp4|mov|avi|mkv)\b') {
      $issues += "$relativePath contains a binary asset path"
    }

    switch ([string]$fixture.scenario_kind) {
      'source_analysis' {
        Assert-ArrayNotEmpty $fixture.hermes_draft_response 'source_refs' "$relativePath hermes_draft_response" ([ref]$issues)
        Assert-ArrayNotEmpty $fixture.hermes_draft_response 'evidence_candidate_notes' "$relativePath hermes_draft_response" ([ref]$issues)
        Assert-ArrayNotEmpty $fixture.hermes_draft_response 'boundary_notes' "$relativePath hermes_draft_response" ([ref]$issues)
        if ($raw -match '"raw_excerpt"' -or $raw -match '"full_article_text"') {
          $issues += "$relativePath must not contain raw_excerpt or full_article_text"
        }
      }
      'validator_pattern' {
        if ($rawLower -notmatch 'review input') {
          $issues += "$relativePath must describe validator proposals as review input"
        }
        if ($raw -match '"requires_live_command_execution"\s*:\s*true') {
          $issues += "$relativePath must not require live command execution"
        }
        if ([string]$fixture.expected_boundary_outcome.status -ne 'accept_draft') {
          $issues += "$relativePath expected outcome must be accept_draft"
        }
      }
      'video_fallback' {
        foreach ($requiredText in @('video_analyze', 'not_inferred', 'official_raw')) {
          if ($raw -notmatch [regex]::Escape($requiredText)) {
            $issues += "$relativePath must include $requiredText"
          }
        }
        if ($rawLower -notmatch 'tool_unavailable|unavailable') {
          $issues += "$relativePath must record tool_unavailable or unavailable"
        }
        if ([string]$fixture.expected_boundary_outcome.status -ne 'hold') {
          $issues += "$relativePath expected status must be hold"
        }
      }
      'video_current_fact_forbidden' {
        if ($raw -notmatch 'official_raw') {
          $issues += "$relativePath must include official_raw"
        }
        if ($rawLower -notmatch 'video alone') {
          $issues += "$relativePath must reject exact current facts from video alone"
        }
        foreach ($pattern in @(
          '(?i)\baccept\b.*exact startup',
          '(?i)\baccept\b.*exact active',
          '(?i)\baccept\b.*exact recovery',
          '(?i)\baccept\b.*exact block advantage'
        )) {
          if ($raw -match $pattern) {
            $issues += "$relativePath appears to accept exact video-derived frame facts: $pattern"
          }
        }
      }
      'external_atlas_binary_forbidden' {
        foreach ($requiredText in @('GIF', 'image', 'frame-atlas')) {
          if ($raw -notmatch [regex]::Escape($requiredText)) {
            $issues += "$relativePath must include binary import request text for $requiredText"
          }
        }
        if ([string]$fixture.expected_boundary_outcome.status -ne 'reject') {
          $issues += "$relativePath expected status must be reject"
        }
        foreach ($forbiddenPath in @('.external-cache', '.external-assets', '.local-media', '.video-cache', '.frame-atlas-cache')) {
          if ($raw -match [regex]::Escape($forbiddenPath)) {
            $issues += "$relativePath must not include repo cache path: $forbiddenPath"
          }
        }
      }
      'external_atlas_metadata_only' {
        if ([string]$fixture.expected_boundary_outcome.status -ne 'metadata_only_guidance') {
          $issues += "$relativePath expected status must be metadata_only_guidance"
        }
        if ($rawLower -notmatch 'source evaluation|acquisition feasibility') {
          $issues += "$relativePath must include source evaluation or acquisition feasibility"
        }
        foreach ($requiredText in @('scraping', 'download', 'cache', 'binary storage', 'official_raw')) {
          if ($rawLower -notmatch [regex]::Escape($requiredText.ToLowerInvariant())) {
            $issues += "$relativePath must include $requiredText"
          }
        }
      }
      'stale_pr_rejection' {
        if ($raw -notmatch 'PR #71|PR #83') {
          $issues += "$relativePath must include PR #71 or PR #83"
        }
        if ($rawLower -notmatch 'reject') {
          $issues += "$relativePath must reject active-source use"
        }
        if ($rawLower -notmatch 'fresh scoped issue') {
          $issues += "$relativePath must require fresh scoped issue recreation"
        }
      }
      'observed_damage_label_boundary' {
        foreach ($requiredText in @('observed damage label', 'review context', 'current-system authority', 'official_raw')) {
          if ($rawLower -notmatch [regex]::Escape($requiredText.ToLowerInvariant())) {
            $issues += "$relativePath must include $requiredText"
          }
        }
      }
      'move_frequency_review_only' {
        foreach ($requiredText in @('candidate', 'confidence', 'review-only', 'official_raw')) {
          if ($rawLower -notmatch [regex]::Escape($requiredText.ToLowerInvariant())) {
            $issues += "$relativePath must include $requiredText"
          }
        }
      }
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Codex-Hermes delegation fixtures OK'
