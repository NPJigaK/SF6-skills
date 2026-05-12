Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixtureRootRelative = 'tests/fixtures/video-observation-taxonomy'
$fixtureRoot = Join-Path $repoRoot $fixtureRootRelative

$expectedFixtures = @(
  'gameplay-only.json',
  'gameplay-with-commentary.json',
  'livestream-layout-webcam-overlay.json',
  'vertical-short.json',
  'subtitle-overlay.json',
  'clip-compilation.json',
  'training-mode.json',
  'commentary-only.json',
  'unknown-mixed.json'
)

$allowedVideoTypes = @(
  'gameplay_only',
  'commentary_only',
  'gameplay_with_commentary',
  'livestream_layout',
  'webcam_overlay',
  'subtitle_overlay',
  'vertical_short',
  'clip_compilation',
  'replay_review',
  'training_mode',
  'tournament_broadcast',
  'coaching_review',
  'social_short',
  'unknown_or_mixed'
)

$allowedRelationshipModes = @('metadata_layer', 'fixture_only_mapping')
$allowedSourceRefTypes = @('placeholder', 'existing_repo_source', 'none')
$allowedVisibility = @('full', 'partial', 'intermittent', 'none', 'unknown')
$allowedHudVisibility = @('full', 'partial', 'blocked', 'cropped', 'none', 'unknown')
$allowedInputVisibility = @('visible', 'partial', 'blocked', 'not_present', 'unknown')
$allowedDamageVisibility = @('visible', 'partial', 'blocked', 'not_present', 'unknown')
$allowedSubtitles = @('none', 'present_non_obstructing', 'present_obstructing', 'unknown')
$allowedOverlayPresence = @('none', 'present_non_obstructing', 'present_obstructing', 'unknown')
$allowedSeverity = @('none', 'minor', 'major', 'critical', 'unknown')
$allowedReplayUncertainty = @('none', 'possible', 'likely', 'unknown')
$allowedAudioTypes = @('no_audio', 'game_audio_only', 'commentary_only', 'gameplay_plus_commentary', 'mixed_voice_chat', 'music_ambient', 'unknown')
$allowedCapabilities = @('likely', 'limited', 'not_safe', 'unknown')

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

  $value = $Object.$Name
  if ($value -isnot [bool]) {
    $Issues.Value += "$Context.$Name must be a boolean"
    return
  }

  if ($value -ne $Expected) {
    $Issues.Value += "$Context.$Name must be $Expected"
  }
}

function Assert-StringInSet {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string[]]$AllowedValues,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
    return
  }

  $value = [string]$Object.$Name
  if ($AllowedValues -notcontains $value) {
    $Issues.Value += "$Context.$Name has invalid value: $value"
  }
}

function Assert-ArrayIncludes {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string[]]$RequiredValues,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
    return
  }

  $values = @($Object.$Name)
  foreach ($required in $RequiredValues) {
    if ($values -notcontains $required) {
      $Issues.Value += "$Context.$Name must include: $required"
    }
  }
}

function Assert-StringArrayValues {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string[]]$AllowedValues,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $Object $Name)) {
    $Issues.Value += "$Context missing property: $Name"
    return
  }

  $values = @($Object.$Name)
  if ($values.Count -eq 0) {
    $Issues.Value += "$Context.$Name must not be empty"
    return
  }

  foreach ($value in $values) {
    if ($value -isnot [string]) {
      $Issues.Value += "$Context.$Name entries must be strings"
      continue
    }
    if ($AllowedValues -notcontains $value) {
      $Issues.Value += "$Context.$Name has invalid entry: $value"
    }
  }
}

function Assert-StrictArray {
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

  if ($Object.$Name -isnot [System.Array]) {
    $Issues.Value += "$Context.$Name must be an array"
  }
}

function Assert-ObjectArray {
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

  $value = $Object.$Name
  if ($null -ne $value -and $value -isnot [System.Array]) {
    $Issues.Value += "$Context.$Name must be an array"
  }
}

function Assert-MultiMatchCompilation {
  param(
    [Parameter(Mandatory = $true)][object]$VisualLayout,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Property $VisualLayout 'multi_match_compilation')) {
    $Issues.Value += "$Context missing property: multi_match_compilation"
    return
  }

  $value = $VisualLayout.multi_match_compilation
  if ($value -is [bool]) {
    return
  }
  if ($value -is [string] -and $value -eq 'unknown') {
    return
  }

  $Issues.Value += "$Context.multi_match_compilation must be a boolean or unknown"
}

function Assert-NoForbiddenRawContent {
  param(
    [Parameter(Mandatory = $true)][string]$Raw,
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($marker in @('RAW TRANSCRIPT', 'assistant:', 'user:', 'tool_call')) {
    if ($Raw -match [regex]::Escape($marker)) {
      $Issues.Value += "$RelativePath contains raw transcript marker: $marker"
    }
  }

  $binaryPathPattern = '(?i)(^|["''\s:/\\])([A-Za-z0-9_.-]+[\\/])*[A-Za-z0-9_.-]+\.(gif|png|jpg|jpeg|webp|mp4|mov|avi|mkv)(["''\s,}\]]|$)'
  if ($Raw -match $binaryPathPattern) {
    $Issues.Value += "$RelativePath contains a binary asset path"
  }

  foreach ($urlPattern in @(
    '(?i)https?://',
    '(?i)\byoutube\.com\b',
    '(?i)\byoutu\.be\b',
    '(?i)\btwitch\.tv\b'
  )) {
    if ($Raw -match $urlPattern) {
      $Issues.Value += "$RelativePath contains a live or fetchable URL; taxonomy fixtures must use non-fetching placeholders or existing repo source references"
    }
  }

  foreach ($cachePathPattern in @(
    '(?i)(^|["''\s:/\\])\.cache([\\/]|["''\s,}\]]|$)',
    '(?i)(^|["''\s:/\\])downloads([\\/]|["''\s,}\]]|$)',
    '(?i)(^|["''\s:/\\])tmp([\\/]|["''\s,}\]]|$)',
    '(?i)(^|["''\s:/\\])\.external-cache([\\/]|["''\s,}\]]|$)',
    '(?i)(^|["''\s:/\\])\.video-cache([\\/]|["''\s,}\]]|$)',
    '(?i)(^|["''\s:/\\])\.frame-atlas-cache([\\/]|["''\s,}\]]|$)'
  )) {
    if ($Raw -match $cachePathPattern) {
      $Issues.Value += "$RelativePath contains a repo-local cache path"
    }
  }

  foreach ($statePathPattern in @(
    '(?i)(^|[\\/])\.env($|[\\/])',
    '(?i)(^|["''\s:/\\])([A-Za-z0-9_.-]+[\\/])*[A-Za-z0-9_.-]*(secret|token|credential|session|memory|cache|log)[A-Za-z0-9_.-]*([\\/][A-Za-z0-9_.-]+)*(["''\s,}\]]|$)',
    '(?i)\.sqlite\b',
    '(?i)\.db\b'
  )) {
    if ($Raw -match $statePathPattern) {
      $Issues.Value += "$RelativePath contains a local state or secret path-like pattern"
    }
  }

  $activeStoragePattern = '(?im)^\s*"[^"]*"\s*:\s*".*\b(commit|store|save|persist|include|write|add)\b.*\b(sessions?|memory|local skills?|curator|checkpoints?|kanban state|logs?|caches?|credentials?|secrets?|tokens?)\b'
  foreach ($line in ($Raw -split "`r?`n")) {
    if ($line -match $activeStoragePattern -and $line -notmatch '(?i)\b(do not|must not|forbid|forbidden|not|no|reject|rejection)\b') {
      $Issues.Value += "Potential active local-state storage instruction in ${RelativePath}: $line"
    }
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

$issues = @()

if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  $issues += "Missing video observation taxonomy fixture directory: $fixtureRootRelative"
}

foreach ($fileName in $expectedFixtures) {
  $path = Join-Path $fixtureRoot $fileName
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    $issues += "Missing video observation taxonomy fixture: $fixtureRootRelative/$fileName"
  }
}

if ($issues.Count -eq 0) {
  $fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.json' | Sort-Object Name)

  foreach ($file in $fixtureFiles) {
    if ($expectedFixtures -notcontains $file.Name) {
      $issues += "Unexpected video observation taxonomy fixture: $fixtureRootRelative/$($file.Name)"
    }
  }

  foreach ($file in $fixtureFiles) {
    $record = Read-Fixture $file
    $raw = [string]$record.Raw
    $fixture = $record.Json
    $relativePath = [string]$record.RelativePath

    Assert-NoForbiddenRawContent $raw $relativePath ([ref]$issues)

    foreach ($field in @(
      'schema_version',
      'fixture_id',
      'video_type',
      'relationship_to_video_observation_schema',
      'source_reference_policy',
      'visual_layout',
      'audio_context',
      'analysis_capability',
      'unsafe_inferences',
      'gap_notes',
      'follow_up_candidate'
    )) {
      Assert-Property $fixture $field $relativePath ([ref]$issues)
    }

    if ((Test-Property $fixture 'schema_version') -and [string]$fixture.schema_version -ne 'video-observation-taxonomy-fixture/v1') {
      $issues += "$relativePath must use schema_version video-observation-taxonomy-fixture/v1"
    }

    if (Test-Property $fixture 'fixture_id') {
      $expectedId = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
      if ([string]$fixture.fixture_id -ne $expectedId) {
        $issues += "$relativePath fixture_id must be $expectedId"
      }
    }

    Assert-StrictArray $fixture 'video_type' $relativePath ([ref]$issues)
    Assert-StringArrayValues $fixture 'video_type' $allowedVideoTypes $relativePath ([ref]$issues)
    if ($file.Name -eq 'unknown-mixed.json') {
      Assert-ArrayIncludes $fixture 'video_type' @('unknown_or_mixed') $relativePath ([ref]$issues)
    }

    if (Test-Property $fixture 'relationship_to_video_observation_schema') {
      $relationship = $fixture.relationship_to_video_observation_schema
      Assert-StringInSet $relationship 'mode' $allowedRelationshipModes "$relativePath relationship_to_video_observation_schema" ([ref]$issues)
      Assert-BooleanValue $relationship 'replaces_video_observation_schema' $false "$relativePath relationship_to_video_observation_schema" ([ref]$issues)
      Assert-BooleanValue $relationship 'maps_to_existing_fields' $true "$relativePath relationship_to_video_observation_schema" ([ref]$issues)
      Assert-ObjectArray $relationship 'mapping_notes' "$relativePath relationship_to_video_observation_schema" ([ref]$issues)
    }

    if (Test-Property $fixture 'source_reference_policy') {
      $sourcePolicy = $fixture.source_reference_policy
      Assert-StringInSet $sourcePolicy 'source_ref_type' $allowedSourceRefTypes "$relativePath source_reference_policy" ([ref]$issues)
      Assert-Property $sourcePolicy 'source_ref' "$relativePath source_reference_policy" ([ref]$issues)
      Assert-BooleanValue $sourcePolicy 'non_fetching_reference' $true "$relativePath source_reference_policy" ([ref]$issues)

      if ((Test-Property $sourcePolicy 'source_ref_type') -and [string]$sourcePolicy.source_ref_type -eq 'none' -and $null -ne $sourcePolicy.source_ref) {
        $issues += "$relativePath source_reference_policy.source_ref must be null when source_ref_type is none"
      }

      if ((Test-Property $sourcePolicy 'source_ref_type') -and [string]$sourcePolicy.source_ref_type -eq 'existing_repo_source') {
        $sourceRef = [string]$sourcePolicy.source_ref
        if ($sourceRef.Length -eq 0) {
          $issues += "$relativePath existing_repo_source must include source_ref"
        } elseif ($sourceRef -notmatch '^knowledge/sources/videos/[^/]+\.md$') {
          $issues += "$relativePath existing_repo_source must point under knowledge/sources/videos/*.md"
        } elseif (-not (Test-Path -LiteralPath (Join-Path $repoRoot $sourceRef) -PathType Leaf)) {
          $issues += "$relativePath references missing existing repo source: $sourceRef"
        }
      }
    }

    if (Test-Property $fixture 'visual_layout') {
      $layout = $fixture.visual_layout
      Assert-StringInSet $layout 'gameplay_visibility' $allowedVisibility "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'hud_visibility' $allowedHudVisibility "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'input_display_visibility' $allowedInputVisibility "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'damage_label_visibility' $allowedDamageVisibility "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'subtitles' $allowedSubtitles "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'webcam_or_wipe_overlay' $allowedOverlayPresence "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'overlay_obstruction' $allowedSeverity "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'vertical_crop' $allowedSeverity "$relativePath visual_layout" ([ref]$issues)
      Assert-MultiMatchCompilation $layout "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'replay_speed_uncertainty' $allowedReplayUncertainty "$relativePath visual_layout" ([ref]$issues)
      Assert-StringInSet $layout 'compression_resolution_limitation' $allowedSeverity "$relativePath visual_layout" ([ref]$issues)
    }

    if (Test-Property $fixture 'audio_context') {
      $audio = $fixture.audio_context
      Assert-StringInSet $audio 'audio_type' $allowedAudioTypes "$relativePath audio_context" ([ref]$issues)
      Assert-BooleanValue $audio 'commentary_claims_are_source_local' $true "$relativePath audio_context" ([ref]$issues)
    }

    if (Test-Property $fixture 'analysis_capability') {
      $capability = $fixture.analysis_capability
      foreach ($field in @(
        'candidate_move_identification',
        'hit_block_whiff_candidate_labeling',
        'timing_frame_window_observation',
        'matchup_strategy_summary',
        'input_hud_observation'
      )) {
        Assert-StringInSet $capability $field $allowedCapabilities "$relativePath analysis_capability" ([ref]$issues)
      }

      Assert-StringInSet $capability 'exact_current_fact' @('forbidden') "$relativePath analysis_capability" ([ref]$issues)
    }

    Assert-ArrayIncludes $fixture 'unsafe_inferences' @('exact_current_fact_from_video', 'official_raw_override') $relativePath ([ref]$issues)
    Assert-ObjectArray $fixture 'gap_notes' $relativePath ([ref]$issues)

    if (Test-Property $fixture 'follow_up_candidate') {
      $followUp = $fixture.follow_up_candidate
      foreach ($field in @('taxonomy_update_needed', 'report_template_update_needed', 'fixture_candidate', 'validator_update_needed')) {
        if (-not (Test-Property $followUp $field)) {
          $issues += "$relativePath follow_up_candidate missing property: $field"
        } elseif ($followUp.$field -isnot [bool]) {
          $issues += "$relativePath follow_up_candidate.$field must be a boolean"
        }
      }
      Assert-ObjectArray $followUp 'notes' "$relativePath follow_up_candidate" ([ref]$issues)
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Video observation taxonomy fixtures OK'
