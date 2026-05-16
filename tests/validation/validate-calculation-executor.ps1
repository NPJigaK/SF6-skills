Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$scriptPath = Join-Path $repoRoot 'packages/calculation-executor/sf6_calculation_executor.py'
$fixtureRoot = Join-Path $repoRoot 'tests/fixtures/calculation-executor'

$allowedExecutorRoles = @('calculation_executor', 'trace_generator', 'arithmetic_consistency_checker')
$allowedStatuses = @(
  'not_run',
  'trace_generated',
  'hypothetical_arithmetic_only',
  'accepted_formula_execution',
  'blocked_missing_input_authority',
  'blocked_missing_formula_policy',
  'blocked_missing_rounding_policy',
  'blocked_ambiguous_route',
  'blocked_public_answer_boundary',
  'invalid_input',
  'executor_error',
  'out_of_scope'
)
$blockedOrNonPublicStatuses = @(
  'not_run',
  'trace_generated',
  'hypothetical_arithmetic_only',
  'blocked_missing_input_authority',
  'blocked_missing_formula_policy',
  'blocked_missing_rounding_policy',
  'blocked_ambiguous_route',
  'blocked_public_answer_boundary',
  'invalid_input',
  'executor_error',
  'out_of_scope'
)

function Add-Issue {
  param(
    [Parameter(Mandatory = $true)][ref]$Issues,
    [Parameter(Mandatory = $true)][string]$Message
  )
  $Issues.Value += $Message
}

function Assert-Property {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not ($Object.PSObject.Properties.Name -contains $Name)) {
    Add-Issue $Issues "$Context missing field: $Name"
  }
}

$issues = @()

if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
  throw 'Missing calculation executor script'
}
if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  throw 'Missing calculation executor fixture directory'
}

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
  throw 'Python executable not found on PATH'
}

$fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.json' | Sort-Object Name)
if ($fixtureFiles.Count -eq 0) {
  throw 'No calculation executor fixtures found'
}

foreach ($fixtureFile in $fixtureFiles) {
  $relativePath = $fixtureFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $fixture = Get-Content -LiteralPath $fixtureFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  $outputText = & $pythonCommand.Source $scriptPath --input $fixtureFile.FullName
  if ($LASTEXITCODE -ne 0) {
    Add-Issue ([ref]$issues) "$relativePath executor exited with code $LASTEXITCODE"
    continue
  }

  try {
    $trace = $outputText | ConvertFrom-Json
  }
  catch {
    Add-Issue ([ref]$issues) "$relativePath executor output is not JSON"
    continue
  }

  foreach ($field in @(
    'trace_id',
    'trace_schema_version',
    'executor_id',
    'executor_role',
    'executor_authority_status',
    'calculation_intent',
    'question_scope',
    'input_values',
    'input_authority_refs',
    'input_status',
    'formula_policy_ref',
    'formula_status',
    'rounding_policy_ref',
    'rounding_status',
    'operation_steps',
    'output_values',
    'status',
    'public_answer_allowed',
    'generated_reference_allowed',
    'accepted_current_fact_authority',
    'uncertainty_or_hold_reasons',
    'created_by',
    'created_at',
    'repo_revision',
    'limitations'
  )) {
    Assert-Property $trace $field $relativePath ([ref]$issues)
  }

  if ($trace.trace_schema_version -ne 'sf6-calculation-trace/v1') {
    Add-Issue ([ref]$issues) "$relativePath output has unexpected trace_schema_version"
  }
  if ($trace.executor_role -notin $allowedExecutorRoles) {
    Add-Issue ([ref]$issues) "$relativePath output has invalid executor_role: $($trace.executor_role)"
  }
  if ($trace.status -notin $allowedStatuses) {
    Add-Issue ([ref]$issues) "$relativePath output has invalid status: $($trace.status)"
  }
  if ($trace.accepted_current_fact_authority -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath output must not be accepted current-fact authority"
  }
  if ($trace.generated_reference_allowed -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath output must not feed generated references"
  }
  if ($trace.status -in $blockedOrNonPublicStatuses -and $trace.public_answer_allowed -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath non-public status must not allow public answers"
  }

  foreach ($authorityFlag in @('not_sf6_authority', 'not_formula_authority', 'not_current_fact_authority')) {
    if (@($trace.executor_authority_status) -notcontains $authorityFlag) {
      Add-Issue ([ref]$issues) "$relativePath missing executor authority flag: $authorityFlag"
    }
  }

  foreach ($step in @($trace.operation_steps)) {
    foreach ($field in @('step_id', 'operation_kind', 'inputs_used', 'output', 'rounding_applied', 'policy_ref', 'notes')) {
      Assert-Property $step $field "$relativePath operation step" ([ref]$issues)
    }
  }

  $expected = $fixture.expected
  if ($expected) {
    if ($trace.status -ne $expected.status) {
      Add-Issue ([ref]$issues) "$relativePath expected status $($expected.status), got $($trace.status)"
    }
    if ($trace.public_answer_allowed -ne $expected.public_answer_allowed) {
      Add-Issue ([ref]$issues) "$relativePath public_answer_allowed mismatch"
    }
    if ($expected.PSObject.Properties.Name -contains 'operation_step_count') {
      if (@($trace.operation_steps).Count -ne $expected.operation_step_count) {
        Add-Issue ([ref]$issues) "$relativePath expected $($expected.operation_step_count) operation step(s), got $(@($trace.operation_steps).Count)"
      }
    }
    if ($expected.output_values) {
      foreach ($property in $expected.output_values.PSObject.Properties) {
        $actualProperty = $trace.output_values.PSObject.Properties[$property.Name]
        if (-not $actualProperty) {
          Add-Issue ([ref]$issues) "$relativePath missing output value: $($property.Name)"
          continue
        }
        if ($actualProperty.Value -ne $property.Value) {
          Add-Issue ([ref]$issues) "$relativePath expected output $($property.Name)=$($property.Value), got $($actualProperty.Value)"
        }
      }
    }
  }

  $rawFixtureText = Get-Content -LiteralPath $fixtureFile.FullName -Raw -Encoding UTF8
  foreach ($forbidden in @('Hermes memory', 'raw transcript', 'credential', 'secret', 'token', 'official_raw override')) {
    if ($rawFixtureText -match [regex]::Escape($forbidden)) {
      Add-Issue ([ref]$issues) "$relativePath contains forbidden local-state or authority text: $forbidden"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Calculation executor OK'
