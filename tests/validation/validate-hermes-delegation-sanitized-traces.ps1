Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$contractDocPath = Join-Path $repoRoot 'contracts/hermes-delegation-sanitized-trace.md'
$schemaPath = Join-Path $repoRoot 'contracts/hermes-delegation-sanitized-trace.schema.json'
$fixtureRoot = Join-Path $repoRoot 'tests/fixtures/hermes-delegation-sanitized-trace'
$validFixtureRoot = Join-Path $fixtureRoot 'valid'
$invalidFixtureRoot = Join-Path $fixtureRoot 'invalid'

function Add-Issue {
  param(
    [Parameter(Mandatory = $true)][ref]$Issues,
    [Parameter(Mandatory = $true)][string]$Message
  )
  $Issues.Value += $Message
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
    Add-Issue $Issues "$Context missing property: $Name"
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
    Add-Issue $Issues "$Context missing property: $Name"
    return
  }

  $value = $Object.$Name
  if ($value -isnot [bool]) {
    Add-Issue $Issues "$Context.$Name must be a boolean"
    return
  }

  if ($value -ne $Expected) {
    Add-Issue $Issues "$Context.$Name must be $Expected"
  }
}

function Test-ArrayContains {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string]$Expected
  )

  if (-not (Test-Property $Object $Name)) {
    return $false
  }
  return @($Object.$Name) -contains $Expected
}

function Get-TraceIssues {
  param(
    [Parameter(Mandatory = $true)][System.IO.FileInfo]$File
  )

  $issues = @()
  $relativePath = $File.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8

  foreach ($marker in @(
    'RAW TRANSCRIPT',
    'assistant:',
    'user:',
    'tool_call',
    'tool_result',
    'BEGIN LOG',
    'END LOG',
    'memory snapshot',
    'provider raw output'
  )) {
    if ($raw -match [regex]::Escape($marker)) {
      $issues += "$relativePath contains unsafe marker: $marker"
    }
  }

  foreach ($pattern in @(
    '"live_hermes_required"\s*:\s*true',
    '"requires_live_hermes"\s*:\s*true',
    '"requires_live_provider_execution"\s*:\s*true',
    '"requires_live_web_research"\s*:\s*true',
    '"requires_live_video_analysis"\s*:\s*true',
    '(?i)live Hermes execution is required'
  )) {
    if ($raw -match $pattern) {
      $issues += "$relativePath requires live execution outside CI-safe scope: $pattern"
    }
  }

  foreach ($pattern in @(
    '(?i)(^|[\\/])\.env($|[\\/])',
    '(?i)\.hermes[\\/](sessions|memories|skills|logs|checkpoints|state\.db)',
    '(?i)(^|[\\/])sessions[\\/]',
    '(?i)(^|[\\/])memory[\\/]',
    '(?i)(^|[\\/])checkpoints[\\/]',
    '(?i)(^|[\\/])logs[\\/]',
    '(?i)(^|[\\/])caches[\\/]',
    '(?i)\bcurator\b',
    '(?i)\bkanban\b',
    '(?i)[A-Za-z0-9_\-./\\]*(secret|token|credential)[A-Za-z0-9_\-./\\]*[\\/]'
  )) {
    if ($raw -match $pattern) {
      $issues += "$relativePath contains local state or secret path-like pattern: $pattern"
    }
  }

  foreach ($pattern in @(
    '(?i)\.(png|jpg|jpeg|gif|webp|mp4|mov|avi|mkv)\b'
  )) {
    if ($raw -match $pattern) {
      $issues += "$relativePath contains binary/media path-like text: $pattern"
    }
  }

  $activeStoragePattern = '(?im)^\s*(?:[-*+]\s+|\d+[.)]\s+)?(commit|store|save|persist|include|write|add)\b.*\b(sessions?|memory|local skills?|curator|checkpoints?|kanban state|logs?|caches?|credentials?|secrets?|tokens?|provider raw output|tool logs?)\b'
  foreach ($line in ($raw -split "`r?`n")) {
    if ($line -match $activeStoragePattern -and $line -notmatch '(?i)\b(do not|must not|forbid|forbidden|not|no|reject|rejection|without)\b') {
      $issues += "Potential active local-state storage instruction in ${relativePath}: $line"
    }
  }

  try {
    $trace = $raw | ConvertFrom-Json
  } catch {
    $issues += "$relativePath is not valid JSON"
    return $issues
  }

  foreach ($field in @(
    'schema_version',
    'trace_id',
    'trace_kind',
    'tracking_issue',
    'target_issue',
    'analysis_mode',
    'created_at',
    'created_from',
    'delegation_summary',
    'role_summary',
    'sanitized_inputs',
    'sanitized_hermes_result',
    'provider_codex_summary',
    'fallback',
    'post_delegation_review',
    'artifact_conversion',
    'validators',
    'expected_boundary_outcome',
    'sanitization_assertions'
  )) {
    Assert-Property $trace $field $relativePath ([ref]$issues)
  }

  if ((Test-Property $trace 'schema_version') -and [string]$trace.schema_version -ne 'hermes-delegation-sanitized-trace/v1') {
    $issues += "$relativePath must use schema_version hermes-delegation-sanitized-trace/v1"
  }
  if ((Test-Property $trace 'trace_id') -and [string]$trace.trace_id -notmatch '^[a-z0-9][a-z0-9-]*$') {
    $issues += "$relativePath trace_id must be kebab-case"
  }
  if ((Test-Property $trace 'analysis_mode') -and @('hermes_primary', 'codex_fallback') -notcontains [string]$trace.analysis_mode) {
    $issues += "$relativePath has invalid analysis_mode: $($trace.analysis_mode)"
  }

  if (Test-Property $trace 'role_summary') {
    foreach ($role in @('hermes_operator', 'boundary_auditor', 'artifact_converter', 'validator_executor')) {
      if (-not (Test-ArrayContains $trace.role_summary 'codex_app_role' $role)) {
        $issues += "$relativePath role_summary.codex_app_role missing: $role"
      }
    }

    if ((Test-Property $trace 'analysis_mode') -and [string]$trace.analysis_mode -eq 'hermes_primary') {
      foreach ($role in @('primary_analyst', 'orchestrator')) {
        if (-not (Test-ArrayContains $trace.role_summary 'hermes_role' $role)) {
          $issues += "$relativePath hermes_primary trace missing Hermes role: $role"
        }
      }
    }
  }

  if (Test-Property $trace 'provider_codex_summary') {
    if ((Test-Property $trace.provider_codex_summary 'used') -and $trace.provider_codex_summary.used -eq $true) {
      Assert-BooleanValue $trace.provider_codex_summary 'remained_executor' $true "$relativePath provider_codex_summary" ([ref]$issues)
      if ((Test-Property $trace 'post_delegation_review') -and (Test-Property $trace.post_delegation_review 'provider_codex_final_authority') -and $trace.post_delegation_review.provider_codex_final_authority -ne $false) {
        $issues += "$relativePath provider Codex must not become final authority"
      }
    }
  }

  if (Test-Property $trace 'fallback') {
    if ((Test-Property $trace 'analysis_mode') -and [string]$trace.analysis_mode -eq 'codex_fallback') {
      Assert-BooleanValue $trace.fallback 'occurred' $true "$relativePath fallback" ([ref]$issues)
      if (-not (Test-Property $trace.fallback 'reason') -or [string]::IsNullOrWhiteSpace([string]$trace.fallback.reason)) {
        $issues += "$relativePath codex_fallback must record a non-empty fallback reason"
      }
      if ((Test-Property $trace 'sanitized_hermes_result') -and (Test-Property $trace.sanitized_hermes_result 'result_status') -and [string]$trace.sanitized_hermes_result.result_status -ne 'fallback_required') {
        $issues += "$relativePath codex_fallback must not claim Hermes-first completion"
      }
    } elseif ((Test-Property $trace.fallback 'occurred') -and $trace.fallback.occurred -eq $true) {
      $issues += "$relativePath fallback.occurred true requires analysis_mode codex_fallback"
    }
  }

  if (Test-Property $trace 'post_delegation_review') {
    Assert-BooleanValue $trace.post_delegation_review 'hermes_output_is_draft_input' $true "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'canonical_promotion_allowed' $false "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'requires_codex_review' $true "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'requires_validators' $true "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'provider_codex_final_authority' $false "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'local_state_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'raw_transcript_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'credentials_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
    Assert-BooleanValue $trace.post_delegation_review 'provider_raw_output_committed' $false "$relativePath post_delegation_review" ([ref]$issues)
  }

  if (Test-Property $trace 'validators') {
    Assert-BooleanValue $trace.validators 'live_hermes_required' $false "$relativePath validators" ([ref]$issues)
  }

  if (Test-Property $trace 'sanitization_assertions') {
    foreach ($field in @(
      'contains_raw_transcript',
      'contains_local_state',
      'contains_credentials',
      'contains_provider_raw_output',
      'contains_tool_raw_log',
      'contains_binary_asset_path',
      'requires_live_hermes',
      'requires_live_provider_execution'
    )) {
      Assert-BooleanValue $trace.sanitization_assertions $field $false "$relativePath sanitization_assertions" ([ref]$issues)
    }
  }

  return $issues
}

$issues = @()

foreach ($requiredPath in @($contractDocPath, $schemaPath, $validFixtureRoot, $invalidFixtureRoot)) {
  if (-not (Test-Path -LiteralPath $requiredPath)) {
    $issues += "Missing required path: $requiredPath"
  }
}

if ($issues.Count -eq 0) {
  $contractText = Get-Content -LiteralPath $contractDocPath -Raw -Encoding UTF8
  foreach ($needle in @(
    'Hermes Delegation Sanitized Trace Contract',
    'orchestration metadata only',
    'Hermes output',
    'primary draft input',
    'provider Codex',
    'raw Hermes transcript',
    'Sanitized traces must not record'
  )) {
    if ($contractText -notmatch [regex]::Escape($needle)) {
      $issues += "contracts/hermes-delegation-sanitized-trace.md missing required text: $needle"
    }
  }

  $schemaText = Get-Content -LiteralPath $schemaPath -Raw -Encoding UTF8
  foreach ($needle in @(
    'hermes-delegation-sanitized-trace/v1',
    'hermes_primary_delegation',
    'provider_executor_summary',
    'codex_fallback',
    'post_delegation_review',
    'live_hermes_required',
    'sanitization_assertions'
  )) {
    if ($schemaText -notmatch [regex]::Escape($needle)) {
      $issues += "contracts/hermes-delegation-sanitized-trace.schema.json missing required text: $needle"
    }
  }

  $schemaObject = $schemaText | ConvertFrom-Json
  foreach ($field in @('$schema', '$id', 'title', 'required', 'properties')) {
    Assert-Property $schemaObject $field 'contracts/hermes-delegation-sanitized-trace.schema.json' ([ref]$issues)
  }

  $validFiles = @(Get-ChildItem -LiteralPath $validFixtureRoot -File -Filter '*.json' | Sort-Object Name)
  $invalidFiles = @(Get-ChildItem -LiteralPath $invalidFixtureRoot -File -Filter '*.json' | Sort-Object Name)

  foreach ($fileName in @('hermes-primary-delegation.json', 'provider-executor-summary.json', 'codex-fallback-recorded.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $validFixtureRoot $fileName) -PathType Leaf)) {
      $issues += "Missing valid sanitized trace fixture: $fileName"
    }
  }
  foreach ($fileName in @('raw-transcript-marker.json', 'local-state-path.json', 'provider-raw-output.json', 'live-hermes-required.json', 'binary-media-path.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $invalidFixtureRoot $fileName) -PathType Leaf)) {
      $issues += "Missing invalid sanitized trace fixture: $fileName"
    }
  }

  foreach ($file in $validFiles) {
    $traceIssues = @(Get-TraceIssues -File $file)
    if ($traceIssues.Count -gt 0) {
      $issues += $traceIssues
    }
  }

  foreach ($file in $invalidFiles) {
    $traceIssues = @(Get-TraceIssues -File $file)
    if ($traceIssues.Count -eq 0) {
      $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
      $issues += "$relativePath was expected to be rejected but produced no validation issues"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Hermes delegation sanitized traces OK'
