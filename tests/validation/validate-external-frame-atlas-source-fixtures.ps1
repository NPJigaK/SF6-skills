Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$schemaRelativePath = 'contracts/external-frame-atlas-source.schema.json'
$fixtureRootRelative = 'tests/fixtures/external-frame-atlas'
$evaluationMatrixRelativePath = 'data/external-frame-atlas/evaluation/source-evaluation-matrix.json'
$rosterRelativePath = 'data/roster/current-character-roster.json'
$runAllRelativePath = 'tests/validation/run-all.ps1'

$schemaPath = Join-Path $repoRoot $schemaRelativePath
$fixtureRoot = Join-Path $repoRoot $fixtureRootRelative
$evaluationMatrixPath = Join-Path $repoRoot $evaluationMatrixRelativePath
$rosterPath = Join-Path $repoRoot $rosterRelativePath
$runAllPath = Join-Path $repoRoot $runAllRelativePath

$expectedFixtures = @(
  'sf6frames-hitbox-overlay-candidate.json',
  'ultimate-frame-data-hitbox-image-candidate.json',
  'maintainer-local-captured-reference-placeholder.json',
  'unsupported-forbidden-source-example.json'
)

$requiredManifestFields = @(
  'schema_version',
  'manifest_id',
  'manifest_kind',
  'source_id',
  'source_name',
  'source_url',
  'source_evaluation_ref',
  'source_evaluation_status',
  'character_slug',
  'character_display_name',
  'move_id',
  'move_name',
  'move_input',
  'variant_type',
  'asset_type',
  'candidate_asset_type',
  'permission_status',
  'license_status',
  'redistribution_status',
  'cache_policy',
  'binary_storage_allowed',
  'numeric_frame_data_ingestion_allowed',
  'not_current_fact_authority',
  'may_override_official_raw',
  'public_bundle_allowed',
  'official_raw_consistency_check_status',
  'official_raw_consistency_notes',
  'move_mapping_status',
  'analysis_use',
  'forbidden_use',
  'binary_derived_fields',
  'future_acquisition',
  'review_status',
  'notes'
)

$cachePolicyFields = @(
  'cache_sync_status',
  'repo_external_cache_only',
  'local_cache_path_recorded',
  'cache_path_policy',
  'ci_cache_allowed',
  'public_bundle_cache_allowed'
)

$binaryDerivedFields = @(
  'asset_sha256',
  'perceptual_hash',
  'frame_count',
  'fps_assumption',
  'dimensions',
  'retrieved_at',
  'source_asset_url',
  'local_cache_path'
)

$futureAcquisitionFields = @(
  'existing_fetch_tooling_alignment',
  'future_acquisition_tooling',
  'new_fetch_dependency_required',
  'future_cache_sync_scope',
  'checked_in_raw_snapshot_allowed'
)

$allowedSourceEvaluationStatuses = @(
  'candidate_metadata_only',
  'hold_terms_or_permission',
  'hold_rate_limit_or_robots',
  'hold_unstable_assets',
  'reference_context_only',
  'not_recommended',
  'comparison_boundary'
)
$allowedVariantTypes = @('hitbox_overlay', 'hurtbox_overlay', 'hitbox_image', 'clean_visual', 'unknown', 'not_applicable', 'unsupported')
$allowedAssetTypes = @('metadata_only', 'gif', 'png_sequence', 'webp', 'sprite_sheet', 'frame_sequence', 'hitbox_image', 'unknown')
$allowedCandidateAssetTypes = @('gif', 'png_sequence', 'webp', 'sprite_sheet', 'frame_sequence', 'hitbox_image', 'unknown', 'not_applicable', 'unsupported')
$allowedPermissionStatuses = @('not_reviewed', 'reviewed_no_explicit_permission', 'permission_required', 'permission_granted', 'unknown', 'not_applicable')
$allowedLicenseStatuses = @('not_reviewed', 'unknown', 'explicit_license_found', 'no_explicit_license_found', 'permission_required', 'not_applicable')
$allowedRedistributionStatuses = @('not_allowed_by_default', 'unknown', 'permission_required', 'metadata_only_allowed', 'binary_redistribution_not_allowed', 'not_applicable')
$allowedConsistencyStatuses = @('not_checked', 'consistent', 'inconsistent', 'inconclusive', 'not_applicable')
$allowedMoveMappingStatuses = @('mapped', 'ambiguous', 'unmapped', 'not_applicable')
$allowedReviewStatuses = @('candidate', 'needs_review', 'unsupported', 'rejected')
$allowedCacheSyncStatuses = @('not_in_scope', 'later_explicit_issue_required')
$allowedFetchAlignment = @('align_with_ingest_frame_data_scrapling_stack_if_later_approved', 'not_applicable')
$allowedFutureAcquisitionTooling = @('scrapling_candidate_not_implemented', 'manual_review_only', 'not_in_scope', 'not_recommended')
$allowedFutureCacheScope = @('later_explicit_maintainer_local_repo_external_cache_issue_required', 'not_in_scope', 'not_recommended')

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

function Assert-NoUnexpectedProperties {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string[]]$AllowedFields,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($property in $Object.PSObject.Properties.Name) {
    if ($AllowedFields -notcontains $property) {
      $Issues.Value += "$Context has unexpected property: $property"
    }
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

  if ($null -eq $Object.$Name) {
    $Issues.Value += "$Context.$Name must not be null"
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

  if ($Object.$Name -isnot [System.Array]) {
    $Issues.Value += "$Context.$Name must be an array"
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

function Assert-NullField {
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

  if ($null -ne $Object.$Name) {
    $Issues.Value += "$Context.$Name must be null in #139 metadata-only fixtures"
  }
}

function Assert-NoForbiddenRawContent {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $binaryPathPattern = '(?i)(^|["''\s:/\\])([A-Za-z0-9_.-]+[\\/]+)+[A-Za-z0-9_.-]+\.(gif|png|jpg|jpeg|webp|mp4|mov|avi|mkv)(["''\s,)}\]]|$)'
  if ($Content -match $binaryPathPattern) {
    $Issues.Value += "$RelativePath contains a path-like binary asset reference"
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
    '(?i)(^|["''\s:/\\])data/raw([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])data/normalized([\\/]|["''\s,)}\]]|$)',
    '(?i)(^|["''\s:/\\])data/exports([\\/]|["''\s,)}\]]|$)'
  )) {
    if ($Content -match $cachePathPattern) {
      $Issues.Value += "$RelativePath contains a forbidden repo-local cache or authority-surface path"
    }
  }

  foreach ($line in ($Content -split "`r?`n")) {
    $lower = $line.ToLowerInvariant()
    if ($lower -match '\b(implements|implemented|adds|added|creates|created|enables|enabled|approves|approved)\b.*\b(scraper|downloader|local cache sync|cache-sync|binary storage|git lfs|move recognition|numeric frame-data ingestion|public `?sf6-agent`? runtime behavior)\b') {
      $Issues.Value += "$RelativePath appears to claim #139 implemented forbidden behavior: $line"
    }
    if ($lower -match '\bexternal visual (source|sources|reference|references)\b.*\b(current-fact authority|current fact authority|may override official_raw|override official_raw)\b' -and $lower -notmatch '\b(not|do not|does not|must not|cannot|never|forbidden|no)\b') {
      $Issues.Value += "$RelativePath appears to grant external visual current-fact authority: $line"
    }
    if ($lower -match '\bofficial_raw_consistency_check_status\b.*\b(authority|current-fact|current fact|promote)\b' -and $lower -notmatch '\b(not|do not|does not|must not|cannot|never|forbidden|review metadata only)\b') {
      $Issues.Value += "$RelativePath appears to promote consistency status into authority: $line"
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

Assert-FileExists $schemaPath $schemaRelativePath ([ref]$issues)
Assert-FileExists $evaluationMatrixPath $evaluationMatrixRelativePath ([ref]$issues)
Assert-FileExists $rosterPath $rosterRelativePath ([ref]$issues)
Assert-FileExists $runAllPath $runAllRelativePath ([ref]$issues)

if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  $issues += "Missing external frame-atlas fixture directory: $fixtureRootRelative"
}

foreach ($fileName in $expectedFixtures) {
  $path = Join-Path $fixtureRoot $fileName
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    $issues += "Missing external frame-atlas fixture: $fixtureRootRelative/$fileName"
  }
}

if ($issues.Count -eq 0) {
  $schemaRaw = Get-Content -LiteralPath $schemaPath -Raw -Encoding UTF8
  $evaluationMatrixRaw = Get-Content -LiteralPath $evaluationMatrixPath -Raw -Encoding UTF8
  $rosterRaw = Get-Content -LiteralPath $rosterPath -Raw -Encoding UTF8
  $runAllRaw = Get-Content -LiteralPath $runAllPath -Raw -Encoding UTF8
  $schema = $schemaRaw | ConvertFrom-Json
  $evaluationMatrix = $evaluationMatrixRaw | ConvertFrom-Json
  $roster = $rosterRaw | ConvertFrom-Json

  Assert-Contains $runAllRaw 'tests/validation/validate-external-frame-atlas-source-fixtures.ps1' 'run-all.ps1' ([ref]$issues)
  Assert-NoForbiddenRawContent $schemaRaw $schemaRelativePath ([ref]$issues)

  if ($schema.'$schema' -ne 'https://json-schema.org/draft/2020-12/schema') {
    $issues += "$schemaRelativePath must use JSON Schema draft 2020-12"
  }
  if ($schema.title -ne 'External Frame Atlas Source Manifest') {
    $issues += "$schemaRelativePath has unexpected title"
  }
  if ($schema.additionalProperties -ne $false) {
    $issues += "$schemaRelativePath must reject unexpected top-level properties"
  }

  $schemaRequired = @($schema.required)
  foreach ($field in $requiredManifestFields) {
    if ($schemaRequired -notcontains $field) {
      $issues += "$schemaRelativePath schema is missing required field: $field"
    }
  }

  $evaluationSourceIds = @($evaluationMatrix.records | ForEach-Object { [string]$_.source_id })
  $rosterSlugs = @($roster.characters | ForEach-Object { [string]$_.character_slug })
  if ($rosterSlugs.Count -eq 0) {
    $issues += "$rosterRelativePath must include current roster character slugs"
  }
  foreach ($expectedSourceId in @('sf6frames', 'ultimate_frame_data', 'maintainer_local_captured_references')) {
    if ($evaluationSourceIds -notcontains $expectedSourceId) {
      $issues += "$evaluationMatrixRelativePath missing expected source evaluation record: $expectedSourceId"
    }
  }

  $fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.json' | Sort-Object Name)
  foreach ($file in $fixtureFiles) {
    if ($expectedFixtures -notcontains $file.Name) {
      $issues += "Unexpected external frame-atlas fixture: $fixtureRootRelative/$($file.Name)"
    }
  }

  $fixtureRecords = @()
  foreach ($file in $fixtureFiles) {
    $fixtureRecords += Read-Fixture $file
  }

  $fixtures = @($fixtureRecords | ForEach-Object { $_.Json })
  foreach ($expectedSourceId in @('sf6frames', 'ultimate_frame_data', 'maintainer_local_captured_references', 'unsupported_forbidden_source_example')) {
    if (@($fixtures | Where-Object { $_.source_id -eq $expectedSourceId }).Count -ne 1) {
      $issues += "$fixtureRootRelative must include exactly one fixture for source_id: $expectedSourceId"
    }
  }

  foreach ($record in $fixtureRecords) {
    $raw = [string]$record.Raw
    $fixture = $record.Json
    $relativePath = [string]$record.RelativePath

    Assert-NoForbiddenRawContent $raw $relativePath ([ref]$issues)
    Assert-NoUnexpectedProperties $fixture $requiredManifestFields $relativePath ([ref]$issues)

    foreach ($field in $requiredManifestFields) {
      Assert-Property $fixture $field $relativePath ([ref]$issues)
    }

    foreach ($field in @('schema_version', 'manifest_id', 'manifest_kind', 'source_id', 'source_name', 'source_url', 'source_evaluation_ref', 'official_raw_consistency_notes')) {
      Assert-NonEmptyString $fixture $field $relativePath ([ref]$issues)
    }

    if ((Test-Property $fixture 'schema_version') -and [string]$fixture.schema_version -ne 'external-frame-atlas-source/v1') {
      $issues += "$relativePath must use schema_version external-frame-atlas-source/v1"
    }
    if ((Test-Property $fixture 'manifest_kind') -and [string]$fixture.manifest_kind -ne 'metadata_only_external_frame_atlas_source') {
      $issues += "$relativePath has invalid manifest_kind"
    }
    if ((Test-Property $fixture 'manifest_id')) {
      $expectedManifestId = [System.IO.Path]::GetFileNameWithoutExtension($relativePath)
      if ([string]$fixture.manifest_id -ne $expectedManifestId) {
        $issues += "$relativePath manifest_id must be $expectedManifestId"
      }
    }
    if ((Test-Property $fixture 'source_evaluation_ref') -and [string]$fixture.source_evaluation_ref -notmatch '^data/external-frame-atlas/evaluation/source-evaluation-matrix\.json#(source_id=[a-z0-9_=-]+|boundary=[a-z0-9_-]+)$') {
      $issues += "$relativePath source_evaluation_ref must point to the #138 evaluation matrix"
    }

    if (Test-Property $fixture 'character_slug') {
      if ($null -eq $fixture.character_slug) {
        if ((Test-Property $fixture 'move_mapping_status') -and [string]$fixture.move_mapping_status -notin @('not_applicable', 'unmapped')) {
          $issues += "$relativePath move_mapping_status must be not_applicable or unmapped when character_slug is null"
        }
        if ((Test-Property $fixture 'source_id') -and [string]$fixture.source_id -in @('sf6frames', 'ultimate_frame_data')) {
          $issues += "$relativePath external visual candidates must use a current roster character_slug"
        }
        if ((Test-Property $fixture 'variant_type') -and [string]$fixture.variant_type -notin @('unknown', 'not_applicable', 'unsupported')) {
          $issues += "$relativePath null character_slug must be limited to placeholder, unsupported, or not-applicable context"
        }
        if ((Test-Property $fixture 'review_status') -and [string]$fixture.review_status -notin @('candidate', 'unsupported', 'rejected')) {
          $issues += "$relativePath null character_slug must use placeholder, unsupported, or rejected review status"
        }
      }
      else {
        $characterSlug = [string]$fixture.character_slug
        if ($characterSlug -eq 'unknown') {
          $issues += "$relativePath must not use unknown as a character_slug; use null for placeholder or unsupported records"
        }
        if ($characterSlug -notmatch '^[a-z0-9][a-z0-9_]*$') {
          $issues += "$relativePath character_slug is not roster-style: $characterSlug"
        }
        if ($rosterSlugs -notcontains $characterSlug) {
          $issues += "$relativePath character_slug is not in $rosterRelativePath`: $characterSlug"
        }
      }
    }

    Assert-StringInSet $fixture 'source_evaluation_status' $allowedSourceEvaluationStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'variant_type' $allowedVariantTypes $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'asset_type' $allowedAssetTypes $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'candidate_asset_type' $allowedCandidateAssetTypes $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'permission_status' $allowedPermissionStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'license_status' $allowedLicenseStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'redistribution_status' $allowedRedistributionStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'official_raw_consistency_check_status' $allowedConsistencyStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'move_mapping_status' $allowedMoveMappingStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'review_status' $allowedReviewStatuses $relativePath ([ref]$issues)
    Assert-StringInSet $fixture 'asset_type' @('metadata_only') $relativePath ([ref]$issues)

    foreach ($field in @('analysis_use', 'forbidden_use', 'notes')) {
      Assert-StringArray $fixture $field $relativePath ([ref]$issues)
    }

    Assert-BooleanValue $fixture 'not_current_fact_authority' $true $relativePath ([ref]$issues)
    Assert-BooleanValue $fixture 'may_override_official_raw' $false $relativePath ([ref]$issues)
    Assert-BooleanValue $fixture 'numeric_frame_data_ingestion_allowed' $false $relativePath ([ref]$issues)
    Assert-BooleanValue $fixture 'public_bundle_allowed' $false $relativePath ([ref]$issues)
    Assert-BooleanValue $fixture 'binary_storage_allowed' $false $relativePath ([ref]$issues)

    if (Test-Property $fixture 'cache_policy') {
      $cachePolicy = $fixture.cache_policy
      Assert-NoUnexpectedProperties $cachePolicy $cachePolicyFields "$relativePath cache_policy" ([ref]$issues)
      foreach ($field in $cachePolicyFields) {
        Assert-Property $cachePolicy $field "$relativePath cache_policy" ([ref]$issues)
      }
      Assert-StringInSet $cachePolicy 'cache_sync_status' $allowedCacheSyncStatuses "$relativePath cache_policy" ([ref]$issues)
      Assert-StringInSet $cachePolicy 'cache_path_policy' @('not_recorded') "$relativePath cache_policy" ([ref]$issues)
      Assert-BooleanValue $cachePolicy 'local_cache_path_recorded' $false "$relativePath cache_policy" ([ref]$issues)
      Assert-BooleanValue $cachePolicy 'ci_cache_allowed' $false "$relativePath cache_policy" ([ref]$issues)
      Assert-BooleanValue $cachePolicy 'public_bundle_cache_allowed' $false "$relativePath cache_policy" ([ref]$issues)
      if ((Test-Property $cachePolicy 'repo_external_cache_only') -and $cachePolicy.repo_external_cache_only -isnot [bool]) {
        $issues += "$relativePath cache_policy.repo_external_cache_only must be a boolean"
      }
    }

    if (Test-Property $fixture 'binary_derived_fields') {
      $binaryDerived = $fixture.binary_derived_fields
      Assert-NoUnexpectedProperties $binaryDerived $binaryDerivedFields "$relativePath binary_derived_fields" ([ref]$issues)
      foreach ($field in $binaryDerivedFields) {
        Assert-NullField $binaryDerived $field "$relativePath binary_derived_fields" ([ref]$issues)
      }
    }

    if (Test-Property $fixture 'future_acquisition') {
      $futureAcquisition = $fixture.future_acquisition
      Assert-NoUnexpectedProperties $futureAcquisition $futureAcquisitionFields "$relativePath future_acquisition" ([ref]$issues)
      foreach ($field in $futureAcquisitionFields) {
        Assert-Property $futureAcquisition $field "$relativePath future_acquisition" ([ref]$issues)
      }
      Assert-StringInSet $futureAcquisition 'existing_fetch_tooling_alignment' $allowedFetchAlignment "$relativePath future_acquisition" ([ref]$issues)
      Assert-StringInSet $futureAcquisition 'future_acquisition_tooling' $allowedFutureAcquisitionTooling "$relativePath future_acquisition" ([ref]$issues)
      Assert-StringInSet $futureAcquisition 'future_cache_sync_scope' $allowedFutureCacheScope "$relativePath future_acquisition" ([ref]$issues)
      Assert-BooleanValue $futureAcquisition 'new_fetch_dependency_required' $false "$relativePath future_acquisition" ([ref]$issues)
      Assert-BooleanValue $futureAcquisition 'checked_in_raw_snapshot_allowed' $false "$relativePath future_acquisition" ([ref]$issues)

      if ([string]$futureAcquisition.future_acquisition_tooling -in @('implemented', 'approved', 'active', 'approved_for_cache_sync')) {
        $issues += "$relativePath future_acquisition.future_acquisition_tooling must not be active or approved in #139"
      }
    }

    if ([string]$fixture.source_id -in @('sf6frames', 'ultimate_frame_data')) {
      Assert-StringInSet $fixture 'source_evaluation_status' @('hold_terms_or_permission', 'hold_rate_limit_or_robots', 'hold_unstable_assets', 'candidate_metadata_only') $relativePath ([ref]$issues)
      if ([string]$fixture.candidate_asset_type -eq 'unknown') {
        $issues += "$relativePath should record a conceptual candidate asset type for external visual sources"
      }
    }

    if ([string]$fixture.source_id -eq 'sf6frames') {
      Assert-StringInSet $fixture 'variant_type' @('hitbox_overlay', 'hurtbox_overlay') $relativePath ([ref]$issues)
    }
    if ([string]$fixture.source_id -eq 'ultimate_frame_data') {
      Assert-StringInSet $fixture 'variant_type' @('hitbox_image') $relativePath ([ref]$issues)
    }
    if ([string]$fixture.source_id -eq 'unsupported_forbidden_source_example') {
      Assert-StringInSet $fixture 'review_status' @('unsupported', 'rejected') $relativePath ([ref]$issues)
      Assert-StringInSet $fixture 'source_evaluation_status' @('not_recommended') $relativePath ([ref]$issues)
      if (Test-Property $fixture 'cache_policy') {
        Assert-StringInSet $fixture.cache_policy 'cache_sync_status' @('not_in_scope') "$relativePath cache_policy" ([ref]$issues)
      }
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'External frame-atlas source fixtures OK'
