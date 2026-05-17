Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$workflowPath = Join-Path $repoRoot 'workflows/calculation-backend-handoff.md'
$schemaPath = Join-Path $repoRoot 'contracts/calculation-backend-handoff.schema.json'
$fixtureRoot = Join-Path $repoRoot 'tests/fixtures/calculation-backend-handoff'

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

if (-not (Test-Path -LiteralPath $workflowPath -PathType Leaf)) {
  throw 'Missing calculation backend handoff workflow'
}
if (-not (Test-Path -LiteralPath $schemaPath -PathType Leaf)) {
  throw 'Missing calculation backend handoff schema'
}
if (-not (Test-Path -LiteralPath $fixtureRoot -PathType Container)) {
  throw 'Missing calculation backend handoff fixtures'
}

$workflowText = Get-Content -LiteralPath $workflowPath -Raw -Encoding UTF8
foreach ($needle in @(
  'operator instruction dependency',
  'operator_instruction_only',
  'not_formula_authority',
  'not_rounding_authority',
  'not_current_fact_authority',
  'not_public_answer_behavior',
  'must_not_feed_generated_references',
  'contracts/calculation-executor-trace.md',
  'Do not include real combo damage numbers',
  'Do not commit Hermes memory'
)) {
  if ($workflowText -notmatch [regex]::Escape($needle)) {
    Add-Issue ([ref]$issues) "workflows/calculation-backend-handoff.md missing boundary text: $needle"
  }
}

$schemaText = Get-Content -LiteralPath $schemaPath -Raw -Encoding UTF8
$schema = $schemaText | ConvertFrom-Json
foreach ($field in @('$schema', '$id', 'title', 'required', 'properties')) {
  Assert-Property $schema $field 'contracts/calculation-backend-handoff.schema.json' ([ref]$issues)
}
foreach ($needle in @(
  'sf6-calculation-backend-handoff/v1',
  'operator_instruction_only',
  '"public_answer_allowed"',
  '"const": false',
  'blocked_missing_calculation_instruction',
  'blocked_missing_rounding_instruction'
)) {
  if ($schemaText -notmatch [regex]::Escape($needle)) {
    Add-Issue ([ref]$issues) "contracts/calculation-backend-handoff.schema.json missing required text: $needle"
  }
}

$fixtureFiles = @(Get-ChildItem -LiteralPath $fixtureRoot -File -Filter '*.json' | Sort-Object Name)
if ($fixtureFiles.Count -lt 3) {
  Add-Issue ([ref]$issues) 'Expected at least three calculation backend handoff fixtures'
}

$requiredForbiddenUses = @(
  'not_formula_authority',
  'not_rounding_authority',
  'not_current_fact_authority',
  'not_public_answer_behavior',
  'must_not_feed_generated_references'
)
$forbiddenText = @(
  'accepted_formula',
  'official_formula',
  '"formula_authority": true',
  '"rounding_authority": true',
  '"current_fact_authority": true',
  '"authority_status": "formula_authority"',
  '"authority_status": "rounding_authority"',
  '"authority_status": "current_fact_authority"',
  '"public_answer_allowed": true',
  '"generated_reference_allowed": true',
  '"accepted_current_fact_authority": true',
  'Hermes memory',
  'raw transcript',
  'credential',
  'secret',
  'token',
  'provider output',
  'local skill path'
)

foreach ($fixtureFile in $fixtureFiles) {
  $relativePath = $fixtureFile.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $rawText = Get-Content -LiteralPath $fixtureFile.FullName -Raw -Encoding UTF8

  foreach ($forbidden in $forbiddenText) {
    if ($rawText -match [regex]::Escape($forbidden)) {
      Add-Issue ([ref]$issues) "$relativePath contains forbidden authority or local-state text: $forbidden"
    }
  }

  try {
    $fixture = $rawText | ConvertFrom-Json
  } catch {
    Add-Issue ([ref]$issues) "$relativePath is not valid JSON"
    continue
  }

  foreach ($field in @(
    'handoff_id',
    'handoff_schema_version',
    'tracking_issue',
    'backend_ref',
    'backend_role',
    'selected_dependency_ref',
    'authority_status',
    'public_answer_allowed',
    'generated_reference_allowed',
    'accepted_current_fact_authority',
    'request_scope',
    'calculation_intent',
    'input_values',
    'input_reference_refs',
    'input_status',
    'calculation_instruction',
    'calculation_instruction_status',
    'rounding_instruction',
    'rounding_instruction_status',
    'expected_trace_contract_ref',
    'blocked_status_if_missing',
    'uncertainty_or_hold_reasons',
    'forbidden_uses',
    'created_by',
    'created_at'
  )) {
    Assert-Property $fixture $field $relativePath ([ref]$issues)
  }

  if ($fixture.handoff_schema_version -ne 'sf6-calculation-backend-handoff/v1') {
    Add-Issue ([ref]$issues) "$relativePath has wrong handoff_schema_version"
  }
  if ($fixture.authority_status -ne 'operator_instruction_only') {
    Add-Issue ([ref]$issues) "$relativePath must use authority_status operator_instruction_only"
  }
  if ($fixture.public_answer_allowed -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath must not allow public answers"
  }
  if ($fixture.generated_reference_allowed -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath must not feed generated references"
  }
  if ($fixture.accepted_current_fact_authority -ne $false) {
    Add-Issue ([ref]$issues) "$relativePath must not be accepted current-fact authority"
  }
  if ($fixture.expected_trace_contract_ref -ne 'contracts/calculation-executor-trace.md') {
    Add-Issue ([ref]$issues) "$relativePath must point to calculation executor trace contract"
  }

  foreach ($requiredUse in $requiredForbiddenUses) {
    if (@($fixture.forbidden_uses) -notcontains $requiredUse) {
      Add-Issue ([ref]$issues) "$relativePath missing forbidden_uses entry: $requiredUse"
    }
  }

  if ($fixture.calculation_instruction_status -eq 'hold' -and @($fixture.blocked_status_if_missing) -notcontains 'blocked_missing_calculation_instruction') {
    Add-Issue ([ref]$issues) "$relativePath hold calculation instruction must block missing calculation instruction"
  }
  if ($fixture.rounding_instruction_status -eq 'hold' -and $null -eq $fixture.rounding_instruction -and @($fixture.blocked_status_if_missing) -notcontains 'blocked_missing_rounding_instruction') {
    Add-Issue ([ref]$issues) "$relativePath hold rounding instruction must block missing rounding instruction"
  }
  if ($fixture.calculation_instruction_status -eq 'not_applicable' -and $null -ne $fixture.calculation_instruction) {
    Add-Issue ([ref]$issues) "$relativePath not_applicable calculation instruction must be null"
  }
  if ($fixture.rounding_instruction_status -eq 'not_applicable' -and $null -ne $fixture.rounding_instruction) {
    Add-Issue ([ref]$issues) "$relativePath not_applicable rounding instruction must be null"
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Calculation backend handoff OK'
