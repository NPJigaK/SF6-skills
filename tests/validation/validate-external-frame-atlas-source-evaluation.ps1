Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$schemaRelativePath = 'contracts/external-frame-atlas-source-evaluation.schema.json'
$matrixRelativePath = 'data/external-frame-atlas/evaluation/source-evaluation-matrix.json'
$readmeRelativePath = 'data/external-frame-atlas/evaluation/README.md'
$runAllRelativePath = 'tests/validation/run-all.ps1'

$schemaPath = Join-Path $repoRoot $schemaRelativePath
$matrixPath = Join-Path $repoRoot $matrixRelativePath
$readmePath = Join-Path $repoRoot $readmeRelativePath
$runAllPath = Join-Path $repoRoot $runAllRelativePath

$requiredRecordFields = @(
  'source_id',
  'source_name',
  'source_kind',
  'source_url',
  'candidate_role',
  'coverage_notes',
  'move_category_coverage',
  'hitbox_overlay_available',
  'clean_visual_available',
  'frame_numbers_visible',
  'update_cadence_notes',
  'machine_readability_notes',
  'asset_url_stability_notes',
  'robots_or_terms_reviewed',
  'rate_limit_policy',
  'attribution_required',
  'permission_status',
  'license_status',
  'redistribution_status',
  'risk_level',
  'recommended_status',
  'not_current_fact_authority',
  'may_override_official_raw',
  'numeric_frame_data_ingestion_allowed',
  'public_bundle_allowed',
  'binary_asset_storage_allowed',
  'repo_external_cache_candidate',
  'future_cache_sync_status',
  'analysis_use',
  'forbidden_use',
  'existing_fetch_tooling_alignment',
  'future_acquisition_tooling',
  'new_fetch_dependency_required',
  'future_cache_sync_scope',
  'checked_in_raw_snapshot_allowed'
)

$allowedSourceKinds = @(
  'external_visual_atlas',
  'maintainer_local_placeholder',
  'current_fact_authority_boundary',
  'text_reference_context'
)
$allowedAvailability = @('yes', 'partial', 'no', 'unknown', 'not_applicable')
$allowedRobotsOrTerms = @('not_reviewed', 'limited_manual_review', 'reviewed_no_explicit_cache_permission', 'unknown', 'not_applicable')
$allowedRateLimitPolicy = @('not_reviewed', 'unknown', 'not_applicable', 'requires_later_review')
$allowedAttribution = @('not_reviewed', 'unknown', 'yes', 'no', 'not_applicable')
$allowedPermission = @('not_reviewed', 'reviewed_no_explicit_permission', 'permission_required', 'permission_granted', 'unknown', 'not_applicable')
$allowedLicense = @('not_reviewed', 'unknown', 'explicit_license_found', 'no_explicit_license_found', 'permission_required', 'not_applicable')
$allowedRedistribution = @('not_allowed_by_default', 'unknown', 'permission_required', 'metadata_only_allowed', 'binary_redistribution_not_allowed', 'not_applicable')
$allowedRisk = @('low', 'medium', 'high', 'unknown')
$allowedRecommended = @('candidate_metadata_only', 'hold_terms_or_permission', 'hold_rate_limit_or_robots', 'hold_unstable_assets', 'reference_context_only', 'not_recommended', 'comparison_boundary')
$allowedFutureCacheSync = @('not_in_scope', 'candidate_requires_terms_review', 'candidate_requires_permission', 'candidate_metadata_only_until_approved', 'not_recommended')
$allowedFetchAlignment = @('align_with_ingest_frame_data_scrapling_stack_if_later_approved', 'not_applicable', 'unknown')
$allowedFutureAcquisition = @('not_in_scope', 'scrapling_candidate_not_implemented', 'manual_review_only', 'not_recommended')
$allowedFutureCacheScope = @('not_in_scope', 'later_explicit_maintainer_local_repo_external_cache_issue_required', 'not_recommended')

function Test-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name
  )

  return $null -ne $Object.PSObject.Properties[$Name]
}

function Assert-FileExists {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    $Issues.Value += "Missing file: $RelativePath"
  }
}

function Assert-Contains {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$Needle,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if ($Content -notmatch [regex]::Escape($Needle)) {
    $Issues.Value += "$Context missing required text: $Needle"
  }
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

function Assert-NonEmptyString {
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

  $value = [string]$Object.$Name
  if ($value.Trim().Length -eq 0) {
    $Issues.Value += "$Context.$Name must not be empty"
  }
}

function Assert-StringArray {
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

  $values = @($Object.$Name)
  if ($values.Count -eq 0) {
    $Issues.Value += "$Context.$Name must not be empty"
    return
  }

  foreach ($value in $values) {
    if ($value -isnot [string]) {
      $Issues.Value += "$Context.$Name entries must be strings"
    } elseif ($value.Trim().Length -eq 0) {
      $Issues.Value += "$Context.$Name entries must not be empty"
    }
  }
}

function Assert-NoForbiddenRawContent {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $binaryPathPattern = '(?i)(^|["''\s:/\\])([A-Za-z0-9_.-]+[\\/]+)*[A-Za-z0-9_.-]+\.(gif|png|jpg|jpeg|webp|mp4|mov|avi|mkv)(["''\s,)}\]]|$)'
  if ($Content -match $binaryPathPattern) {
    $Issues.Value += "$RelativePath contains a path-like binary media reference"
  }

  foreach ($cachePathPattern in @(
    '(?i)(^|["''\s:/\\])\.external-cache([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.external-assets([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.local-media([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.video-cache([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.frame-atlas-cache([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])tmp([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.cache([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])downloads([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])assets/raw([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])skills/sf6-agent([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])\.dist([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])skills/sf6-agent/assets/frame-current([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])skills/sf6-agent/assets/normalization([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])data/normalized([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])data/exports([\\/]|["''\s,)}\]]|$)'
  )) {
    if ($Content -match $cachePathPattern) {
      $Issues.Value += "$RelativePath contains a forbidden repo-local cache or generated-surface path"
    }
  }

  if ($Content -match '(?i)approved_for_cache_sync') {
    $Issues.Value += "$RelativePath must not approve cache sync in #138"
  }

  foreach ($line in ($Content -split "`r?`n")) {
    $lower = $line.ToLowerInvariant()
    if ($lower -match '\b(added|adds|implements|implemented|created|creates)\b.*\b(scraper|downloader|cache-sync|cache sync|fetch workflow|package dependency)\b') {
      $Issues.Value += "$RelativePath appears to claim implemented acquisition tooling: $line"
    }
    if (
      $lower -match '\b(fetch|download|scrape|cache|store|hash|redistribute)\b.*\b(external visual assets|external atlas assets|sf6frames|ultimate frame data|binaries|binary assets)\b' -and
      $lower -notmatch '\b(no|not|does not|do not|must not|without|never|forbid|forbidden|future|later|if ever|if a later|does not authorize|require later)\b'
    ) {
      $Issues.Value += "$RelativePath appears to include active external asset acquisition instructions: $line"
    }
    if ($lower -match '\bexternal visual (source|sources|atlas sources)\b.*\b(current-fact authority|override official_raw|may override official_raw)\b' -and $lower -notmatch '\b(not|do not|does not|must not|cannot|forbid|forbidden)\b') {
      $Issues.Value += "$RelativePath appears to grant external visual authority: $line"
    }
    if ($lower -match '\b(sf6frames|ultimate frame data|ufd)\b.*\bnumeric frame-data ingestion\b' -and $lower -notmatch '\b(not|do not|does not|must not|cannot|forbid|forbidden)\b') {
      $Issues.Value += "$RelativePath appears to allow SF6Frames/UFD numeric frame-data ingestion: $line"
    }
    if ($lower -match '\bexternal visual atlas binaries\b.*\b(data/raw|raw snapshot)\b' -and $lower -notmatch '\b(not|do not|does not|must not|cannot|forbid|forbidden|does not make|remain outside)\b') {
      $Issues.Value += "$RelativePath appears to allow checked-in raw snapshot storage for atlas binaries: $line"
    }
  }
}

$issues = @()

Assert-FileExists $schemaPath $schemaRelativePath ([ref]$issues)
Assert-FileExists $matrixPath $matrixRelativePath ([ref]$issues)
Assert-FileExists $readmePath $readmeRelativePath ([ref]$issues)
Assert-FileExists $runAllPath $runAllRelativePath ([ref]$issues)

if ($issues.Count -eq 0) {
  $schemaRaw = Get-Content -LiteralPath $schemaPath -Raw -Encoding UTF8
  $matrixRaw = Get-Content -LiteralPath $matrixPath -Raw -Encoding UTF8
  $readmeRaw = Get-Content -LiteralPath $readmePath -Raw -Encoding UTF8
  $runAllRaw = Get-Content -LiteralPath $runAllPath -Raw -Encoding UTF8

  $schema = $schemaRaw | ConvertFrom-Json
  $matrix = $matrixRaw | ConvertFrom-Json

  Assert-Contains $runAllRaw 'tests/validation/validate-external-frame-atlas-source-evaluation.ps1' 'run-all.ps1' ([ref]$issues)

  Assert-NoForbiddenRawContent $schemaRaw $schemaRelativePath ([ref]$issues)
  Assert-NoForbiddenRawContent $matrixRaw $matrixRelativePath ([ref]$issues)
  Assert-NoForbiddenRawContent $readmeRaw $readmeRelativePath ([ref]$issues)

  Assert-Contains $readmeRaw 'metadata-only' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'No external assets are fetched or stored here' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'SF6Frames and Ultimate Frame Data are visual reference candidates' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'not numeric frame-data ingestion sources' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'do not override `official_raw`' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'Normal public user answer generation must not scrape or cache' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'Scrapling-based fetch stack' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'does not add a scraper, downloader, or cache-sync workflow' $readmeRelativePath ([ref]$issues)
  Assert-Contains $readmeRaw 'remain repo-external by default' $readmeRelativePath ([ref]$issues)

  if ($schema.'$schema' -ne 'https://json-schema.org/draft/2020-12/schema') {
    $issues += "$schemaRelativePath must use JSON Schema draft 2020-12"
  }
  if ($schema.title -ne 'External Frame Atlas Source Evaluation Matrix') {
    $issues += "$schemaRelativePath has unexpected title"
  }
  $schemaRequired = @($schema.'$defs'.source_evaluation_record.required)
  foreach ($field in $requiredRecordFields) {
    if ($schemaRequired -notcontains $field) {
      $issues += "$schemaRelativePath schema record is missing required field: $field"
    }
  }

  if ($matrix.schema_version -ne 'external-frame-atlas-source-evaluation/v1') {
    $issues += "$matrixRelativePath has invalid schema_version"
  }
  if ($matrix.matrix_kind -ne 'metadata_only_source_evaluation') {
    $issues += "$matrixRelativePath has invalid matrix_kind"
  }
  if ($matrix.issue -ne '#138') {
    $issues += "$matrixRelativePath must be scoped to #138"
  }

  $records = @($matrix.records)
  if ($records.Count -lt 5) {
    $issues += "$matrixRelativePath must include at least five source evaluation records"
  }

  foreach ($expectedSource in @(
    'sf6frames',
    'ultimate_frame_data',
    'maintainer_local_captured_references',
    'official_raw_comparison_boundary',
    'supercombo_text_reference_context'
  )) {
    if (@($records | Where-Object { $_.source_id -eq $expectedSource }).Count -ne 1) {
      $issues += "$matrixRelativePath must include exactly one record for: $expectedSource"
    }
  }

  foreach ($record in $records) {
    $context = "$matrixRelativePath record $($record.source_id)"

    foreach ($field in $requiredRecordFields) {
      Assert-Property $record $field $context ([ref]$issues)
    }

    foreach ($field in @('source_id', 'source_name', 'source_url', 'coverage_notes', 'move_category_coverage', 'update_cadence_notes', 'machine_readability_notes', 'asset_url_stability_notes')) {
      Assert-NonEmptyString $record $field $context ([ref]$issues)
    }

    foreach ($field in @('candidate_role', 'analysis_use', 'forbidden_use')) {
      Assert-StringArray $record $field $context ([ref]$issues)
    }

    Assert-StringInSet $record 'source_kind' $allowedSourceKinds $context ([ref]$issues)
    Assert-StringInSet $record 'hitbox_overlay_available' $allowedAvailability $context ([ref]$issues)
    Assert-StringInSet $record 'clean_visual_available' $allowedAvailability $context ([ref]$issues)
    Assert-StringInSet $record 'frame_numbers_visible' $allowedAvailability $context ([ref]$issues)
    Assert-StringInSet $record 'robots_or_terms_reviewed' $allowedRobotsOrTerms $context ([ref]$issues)
    Assert-StringInSet $record 'rate_limit_policy' $allowedRateLimitPolicy $context ([ref]$issues)
    Assert-StringInSet $record 'attribution_required' $allowedAttribution $context ([ref]$issues)
    Assert-StringInSet $record 'permission_status' $allowedPermission $context ([ref]$issues)
    Assert-StringInSet $record 'license_status' $allowedLicense $context ([ref]$issues)
    Assert-StringInSet $record 'redistribution_status' $allowedRedistribution $context ([ref]$issues)
    Assert-StringInSet $record 'risk_level' $allowedRisk $context ([ref]$issues)
    Assert-StringInSet $record 'recommended_status' $allowedRecommended $context ([ref]$issues)
    Assert-StringInSet $record 'future_cache_sync_status' $allowedFutureCacheSync $context ([ref]$issues)
    Assert-StringInSet $record 'existing_fetch_tooling_alignment' $allowedFetchAlignment $context ([ref]$issues)
    Assert-StringInSet $record 'future_acquisition_tooling' $allowedFutureAcquisition $context ([ref]$issues)
    Assert-StringInSet $record 'future_cache_sync_scope' $allowedFutureCacheScope $context ([ref]$issues)

    foreach ($field in @(
      'not_current_fact_authority',
      'may_override_official_raw',
      'numeric_frame_data_ingestion_allowed',
      'public_bundle_allowed',
      'binary_asset_storage_allowed',
      'repo_external_cache_candidate',
      'new_fetch_dependency_required',
      'checked_in_raw_snapshot_allowed'
    )) {
      if ((Test-Property $record $field) -and $record.$field -isnot [bool]) {
        $issues += "$context.$field must be a boolean"
      }
    }

    Assert-BooleanValue $record 'may_override_official_raw' $false $context ([ref]$issues)
    Assert-BooleanValue $record 'numeric_frame_data_ingestion_allowed' $false $context ([ref]$issues)
    Assert-BooleanValue $record 'public_bundle_allowed' $false $context ([ref]$issues)
    Assert-BooleanValue $record 'binary_asset_storage_allowed' $false $context ([ref]$issues)
    Assert-BooleanValue $record 'new_fetch_dependency_required' $false $context ([ref]$issues)
    Assert-BooleanValue $record 'checked_in_raw_snapshot_allowed' $false $context ([ref]$issues)

    if ([string]$record.future_acquisition_tooling -in @('implemented', 'approved', 'active', 'approved_for_cache_sync')) {
      $issues += "$context.future_acquisition_tooling must not be active or approved in #138"
    }
    if ([string]$record.recommended_status -eq 'approved_for_cache_sync') {
      $issues += "$context.recommended_status must not approve cache sync in #138"
    }

    if ($record.source_kind -eq 'external_visual_atlas') {
      Assert-BooleanValue $record 'not_current_fact_authority' $true $context ([ref]$issues)
      Assert-BooleanValue $record 'may_override_official_raw' $false $context ([ref]$issues)
      Assert-BooleanValue $record 'numeric_frame_data_ingestion_allowed' $false $context ([ref]$issues)
      Assert-BooleanValue $record 'public_bundle_allowed' $false $context ([ref]$issues)
      Assert-BooleanValue $record 'binary_asset_storage_allowed' $false $context ([ref]$issues)
      Assert-BooleanValue $record 'checked_in_raw_snapshot_allowed' $false $context ([ref]$issues)
      if ($record.recommended_status -notin @('candidate_metadata_only', 'hold_terms_or_permission', 'hold_rate_limit_or_robots', 'hold_unstable_assets', 'not_recommended')) {
        $issues += "$context external visual candidates must remain metadata-only, hold, or not recommended"
      }
      if ($record.future_cache_sync_status -notin @('candidate_requires_terms_review', 'candidate_requires_permission', 'candidate_metadata_only_until_approved', 'not_recommended')) {
        $issues += "$context external visual candidates must not mark cache sync as in-scope or approved"
      }
    }

    if ($record.source_id -in @('sf6frames', 'ultimate_frame_data')) {
      Assert-BooleanValue $record 'not_current_fact_authority' $true $context ([ref]$issues)
      Assert-BooleanValue $record 'numeric_frame_data_ingestion_allowed' $false $context ([ref]$issues)
      Assert-BooleanValue $record 'may_override_official_raw' $false $context ([ref]$issues)
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'External frame-atlas source evaluation OK'
