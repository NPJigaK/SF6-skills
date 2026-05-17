Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$toolchainRootRelative = 'data/toolchain'
$toolchainRoot = Join-Path $repoRoot $toolchainRootRelative
$schemaPath = 'contracts/agent-toolchain.schema.json'
$manifestPath = 'data/toolchain/maintainer-agent-toolchain.json'

function Read-Json {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
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

function Get-ManifestItemIds {
  param(
    [AllowNull()][object]$Items,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $ids = @()
  if ($null -eq $Items) {
    return $ids
  }

  foreach ($item in @($Items)) {
    if ($null -eq $item) {
      $Issues.Value += "$Context contains null item"
      continue
    }
    Assert-Property $item 'id' $Context $Issues
    if (Test-Property $item 'id') {
      $id = [string]$item.id
      if ([string]::IsNullOrWhiteSpace($id)) {
        $Issues.Value += "$Context contains empty id"
      } else {
        $ids += $id
      }
    }
  }

  $uniqueIds = @($ids | Select-Object -Unique)
  if ($ids.Count -ne $uniqueIds.Count) {
    $Issues.Value += "$Context contains duplicate ids"
  }

  return $ids
}

function Assert-SetEquals {
  param(
    [Parameter(Mandatory = $true)][string[]]$Actual,
    [Parameter(Mandatory = $true)][string[]]$Expected,
    [Parameter(Mandatory = $true)][string]$Context,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  foreach ($expectedItem in $Expected) {
    if ($Actual -notcontains $expectedItem) {
      $Issues.Value += "$Context missing item: $expectedItem"
    }
  }
  foreach ($actualItem in $Actual) {
    if ($Expected -notcontains $actualItem) {
      $Issues.Value += "$Context has unexpected item: $actualItem"
    }
  }
}

function Get-ToolchainRelativePath {
  param([Parameter(Mandatory = $true)][string]$FullPath)

  $root = (Resolve-Path $toolchainRoot).Path.TrimEnd([char[]]@('\', '/'))
  $relative = $FullPath.Substring($root.Length)
  $relative = $relative -replace '^[\\/]+', ''
  return "$toolchainRootRelative/$($relative -replace '\\', '/')"
}

function Get-JsonPropertyNames {
  param([AllowNull()][object]$Object)

  if ($null -eq $Object) {
    return
  }

  if ($Object -is [pscustomobject]) {
    foreach ($property in $Object.PSObject.Properties) {
      $property.Name
      if ($null -ne $property.Value) {
        Get-JsonPropertyNames $property.Value
      }
    }
    return
  }

  if ($Object -is [System.Collections.IEnumerable] -and -not ($Object -is [string])) {
    foreach ($item in $Object) {
      if ($null -ne $item) {
        Get-JsonPropertyNames $item
      }
    }
  }
}

function Get-JsonStringValues {
  param([AllowNull()][object]$Object)

  if ($null -eq $Object) {
    return
  }

  if ($Object -is [string]) {
    $Object
    return
  }

  if ($Object -is [pscustomobject]) {
    foreach ($property in $Object.PSObject.Properties) {
      if ($null -ne $property.Value) {
        Get-JsonStringValues $property.Value
      }
    }
    return
  }

  if ($Object -is [System.Collections.IEnumerable]) {
    foreach ($item in $Object) {
      if ($null -ne $item) {
        Get-JsonStringValues $item
      }
    }
  }
}

$issues = @()
$requiredFiles = @(
  '.gitignore',
  '.github/renovate.json',
  'docs/architecture/agent-toolchain-freshness.md',
  'docs/architecture/agent-skill-dependency-policy.md',
  'docs/architecture/calculation-backend-policy.md',
  'docs/architecture/hermes-curator-worktree-checkpoint-policy.md',
  'docs/architecture/hermes-memory-policy.md',
  'docs/architecture/hermes-maintainer-profile-policy.md',
  'flake.lock',
  'flake.nix',
  $schemaPath,
  'contracts/hermes-maintainer-skill-allowlist.schema.json',
  'data/toolchain/README.md',
  'data/toolchain/hermes-maintainer-skill-allowlist.json',
  $manifestPath,
  'tools/agent-skills/.gitignore',
  'tools/agent-skills/apm.lock.yaml',
  'tools/agent-skills/apm.yml',
  'workflows/check-agent-toolchain-freshness.md'
)
$allowedRootProperties = @(
  'schema_version',
  'last_reviewed',
  'tools',
  'boundaries'
)
$allowedToolProperties = @(
  'id',
  'role',
  'recommended_channel',
  'known_good_version',
  'required_capabilities',
  'planned_capabilities',
  'version_command',
  'version_command_review_note',
  'update_guidance',
  'freshness_review_cadence',
  'version_management',
  'maintainer_profile_policy'
)
$allowedToolIds = @('codex-cli', 'hermes-cli')
$allowedRoles = @('repo_implementation_executor', 'repo_local_growth_engine')
$allowedRecommendedChannels = @('latest_stable', 'known_good', 'manual_review_required')
$forbiddenManifestFields = @(
  'secret',
  'token',
  'credential',
  'session',
  'cache',
  'log',
  'config',
  'local_state',
  'local_path',
  'local_installed_version',
  'installed_version',
  'current_version',
  'local_version',
  'detected_version',
  'home_path',
  'config_path',
  'cache_path',
  'session_path',
  'log_path'
)

foreach ($relativePath in $requiredFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing agent toolchain file: $relativePath"
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot '.gitignore') -PathType Leaf) {
  $rootGitignore = Read-Text '.gitignore'
  foreach ($needle in @(
    '.hermes/',
    '.env',
    '.env.*',
    '!.env.EXAMPLE',
    '*.transcript',
    '*-transcript.txt',
    '*-doctor-output.txt',
    '*-profile-output.txt',
    '*-command-output.txt'
  )) {
    if ($rootGitignore -notmatch [regex]::Escape($needle)) {
      $issues += ".gitignore missing Hermes local-state/output ignore: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $schemaPath) -PathType Leaf) {
  $schema = Read-Json $schemaPath
  foreach ($field in @('$schema', '$id', 'title')) {
    Assert-Property $schema $field $schemaPath ([ref]$issues)
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'contracts/hermes-maintainer-skill-allowlist.schema.json') -PathType Leaf) {
  $allowlistSchema = Read-Json 'contracts/hermes-maintainer-skill-allowlist.schema.json'
  foreach ($field in @('$schema', '$id', 'title', 'additionalProperties')) {
    Assert-Property $allowlistSchema $field 'contracts/hermes-maintainer-skill-allowlist.schema.json' ([ref]$issues)
  }
  if ((Test-Property $allowlistSchema 'additionalProperties') -and $allowlistSchema.additionalProperties -ne $false) {
    $issues += 'Hermes maintainer skill allowlist schema must set additionalProperties to false'
  }
  $allowlistSchemaText = Read-Text 'contracts/hermes-maintainer-skill-allowlist.schema.json'
  foreach ($needle in @(
    'hermes-maintainer-skill-allowlist/v1',
    'sf6ingest',
    'repo_maintainer_profiles_only',
    'policy_expectation_not_runtime_state',
    'public_sf6_agent_distribution_deferred',
    'do_not_commit_local_hermes_profile_state',
    'external_apm',
    'reviewed_tag_or_immutable_sha_required'
  )) {
    if ($allowlistSchemaText -notmatch [regex]::Escape($needle)) {
      $issues += "contracts/hermes-maintainer-skill-allowlist.schema.json missing required text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'data/toolchain/README.md') -PathType Leaf) {
  $readme = Read-Text 'data/toolchain/README.md'
  foreach ($needle in @(
    'not SF6 gameplay knowledge',
    'not exact current-fact authority',
    'local installed versions',
    'credentials',
    'secrets',
    'local configs',
    'sessions',
    'caches',
    'logs',
    'hermes-maintainer-skill-allowlist.json',
    'built-in default',
    'external APM-managed'
  )) {
    if ($readme -notmatch [regex]::Escape($needle)) {
      $issues += "data/toolchain/README.md missing boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'flake.nix') -PathType Leaf) {
  $flakeText = Read-Text 'flake.nix'
  foreach ($needle in @(
    'hermes-agent.url = "github:NousResearch/hermes-agent"',
    'program = "${hermes-agent.packages.${system}.default}/bin/hermes"',
    'hermes-agent.packages.${system}.default'
  )) {
    if ($flakeText -notmatch [regex]::Escape($needle)) {
      $issues += "flake.nix missing Hermes Nix input text: $needle"
    }
  }
  foreach ($forbidden in @(
    '~/.hermes',
    'HERMES_HOME',
    '.env',
    'credential',
    'secret',
    'token',
    'session',
    'memory',
    'profile-state',
    'cache',
    'log'
  )) {
    if ($flakeText -match [regex]::Escape($forbidden)) {
      $issues += "flake.nix contains forbidden local-state or secret-like text: $forbidden"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'flake.lock') -PathType Leaf) {
  $flakeLock = Read-Json 'flake.lock'
  Assert-Property $flakeLock 'nodes' 'flake.lock' ([ref]$issues)
  Assert-Property $flakeLock 'root' 'flake.lock' ([ref]$issues)

  if (Test-Property $flakeLock 'nodes') {
    if (-not (Test-Property $flakeLock.nodes 'hermes-agent')) {
      $issues += 'flake.lock must contain hermes-agent node'
    } else {
      $hermesLock = $flakeLock.nodes.'hermes-agent'
      foreach ($field in @('locked', 'original')) {
        Assert-Property $hermesLock $field 'flake.lock hermes-agent node' ([ref]$issues)
      }
      if (Test-Property $hermesLock 'locked') {
        foreach ($field in @('owner', 'repo', 'rev', 'narHash', 'type')) {
          Assert-Property $hermesLock.locked $field 'flake.lock hermes-agent locked' ([ref]$issues)
        }
        if ((Test-Property $hermesLock.locked 'owner') -and $hermesLock.locked.owner -ne 'NousResearch') {
          $issues += 'flake.lock hermes-agent owner must be NousResearch'
        }
        if ((Test-Property $hermesLock.locked 'repo') -and $hermesLock.locked.repo -ne 'hermes-agent') {
          $issues += 'flake.lock hermes-agent repo must be hermes-agent'
        }
        if ((Test-Property $hermesLock.locked 'type') -and $hermesLock.locked.type -ne 'github') {
          $issues += 'flake.lock hermes-agent type must be github'
        }
      }
      if (Test-Property $hermesLock 'original') {
        if ((Test-Property $hermesLock.original 'owner') -and $hermesLock.original.owner -ne 'NousResearch') {
          $issues += 'flake.lock hermes-agent original owner must be NousResearch'
        }
        if ((Test-Property $hermesLock.original 'repo') -and $hermesLock.original.repo -ne 'hermes-agent') {
          $issues += 'flake.lock hermes-agent original repo must be hermes-agent'
        }
      }
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot '.github/renovate.json') -PathType Leaf) {
  $renovateRaw = Get-Content -LiteralPath (Join-Path $repoRoot '.github/renovate.json') -Raw -Encoding UTF8
  $renovate = $renovateRaw | ConvertFrom-Json

  if (-not (Test-Property $renovate 'nix') -or -not (Test-Property $renovate.nix 'enabled') -or $renovate.nix.enabled -ne $true) {
    $issues += '.github/renovate.json must enable the Nix manager'
  }
  if (-not (Test-Property $renovate 'lockFileMaintenance') -or -not (Test-Property $renovate.lockFileMaintenance 'enabled') -or $renovate.lockFileMaintenance.enabled -ne $true) {
    $issues += '.github/renovate.json must enable lockFileMaintenance'
  }

  $renovateText = $renovateRaw.ToLowerInvariant()
  foreach ($needle in @('nix', 'hermes agent nix flake input')) {
    if ($renovateText -notmatch [regex]::Escape($needle)) {
      $issues += ".github/renovate.json missing Nix/Hermes update text: $needle"
    }
  }
  foreach ($needle in @(
    'tools/agent-skills/apm.yml',
    'agent skill apm dependencies',
    'git-tags',
    'git-refs'
  )) {
    if ($renovateText -notmatch [regex]::Escape($needle)) {
      $issues += ".github/renovate.json missing Agent Skill dependency update text: $needle"
    }
  }
  foreach ($forbidden in @('secret', 'token', 'credential', '.env')) {
    if ($renovateText -match [regex]::Escape($forbidden)) {
      $issues += ".github/renovate.json contains forbidden secret-like text: $forbidden"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/agent-skills/apm.yml') -PathType Leaf) {
  $apmText = Read-Text 'tools/agent-skills/apm.yml'
  foreach ($needle in @(
    'name: sf6-maintainer-agent-skills',
    'targets:',
    '- agent-skills',
    'dependencies:',
    'renovate: datasource=git-tags depName=K-Dense-AI/scientific-agent-skills',
    'K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0',
    'devDependencies:'
  )) {
    if ($apmText -notmatch [regex]::Escape($needle)) {
      $issues += "tools/agent-skills/apm.yml missing required text: $needle"
    }
  }
  foreach ($forbiddenDependency in @(
    'K-Dense-AI/scientific-agent-skills#',
    'K-Dense-AI/scientific-agent-skills/main',
    'scientific-skills/statistics',
    'sagemath',
    'mcp'
  )) {
    if ($apmText.ToLowerInvariant() -match [regex]::Escape($forbiddenDependency.ToLowerInvariant())) {
      $issues += "tools/agent-skills/apm.yml contains deferred or broad dependency text: $forbiddenDependency"
    }
  }
  foreach ($forbidden in @(
    '~/.hermes',
    'HERMES_HOME',
    '.env',
    'auth.json',
    'credential',
    'secret',
    'token',
    'memories/',
    'sessions/',
    'state.db',
    'logs/',
    'cache',
    '/home/',
    'C:\'
  )) {
    if ($apmText -match [regex]::Escape($forbidden)) {
      $issues += "tools/agent-skills/apm.yml contains forbidden local-state or secret-like text: $forbidden"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/agent-skills/.gitignore') -PathType Leaf) {
  $apmGitignore = Read-Text 'tools/agent-skills/.gitignore'
  foreach ($needle in @(
    '.agents/',
    'apm_modules/'
  )) {
    if ($apmGitignore -notmatch [regex]::Escape($needle)) {
      $issues += "tools/agent-skills/.gitignore missing ignored APM output text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/agent-skills/apm.lock.yaml') -PathType Leaf) {
  $apmLockText = Read-Text 'tools/agent-skills/apm.lock.yaml'
  foreach ($needle in @(
    "lockfile_version: '1'",
    'apm_version:',
    'repo_url: K-Dense-AI/scientific-agent-skills',
    'resolved_ref: v2.38.0',
    'virtual_path: scientific-skills/sympy',
    'is_virtual: true',
    'package_type: claude_skill',
    'deployed_files:',
    '- .agents/skills/sympy',
    'content_hash: sha256:'
  )) {
    if ($apmLockText -notmatch [regex]::Escape($needle)) {
      $issues += "tools/agent-skills/apm.lock.yaml missing required lock text: $needle"
    }
  }
  foreach ($forbiddenLockText in @(
    'scientific-skills/statistical-analysis',
    'scientific-skills/statsmodels',
    'scientific-skills/simpy',
    'sagemath',
    'mcp',
    'secret',
    'token',
    'credential',
    'memories/',
    'sessions/',
    'state.db',
    'logs/'
  )) {
    if ($apmLockText.ToLowerInvariant() -match [regex]::Escape($forbiddenLockText.ToLowerInvariant())) {
      $issues += "tools/agent-skills/apm.lock.yaml contains deferred or forbidden text: $forbiddenLockText"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'data/toolchain/hermes-maintainer-skill-allowlist.json') -PathType Leaf) {
  $skillAllowlist = Read-Json 'data/toolchain/hermes-maintainer-skill-allowlist.json'
  foreach ($field in @(
    'schema_version',
    'last_reviewed',
    'tracking_issue',
    'profile',
    'scope',
    'status',
    'public_distribution_boundary',
    'local_state_boundary',
    'default_activation_rule',
    'builtin_default_skills',
    'builtin_conditional_skills',
    'external_apm_skills',
    'deferred_candidates',
    'forbidden_categories',
    'review_commands',
    'source_refs'
  )) {
    Assert-Property $skillAllowlist $field 'data/toolchain/hermes-maintainer-skill-allowlist.json' ([ref]$issues)
  }

  $expectedAllowlistValues = @{
    'schema_version' = 'hermes-maintainer-skill-allowlist/v1'
    'tracking_issue' = '#279'
    'profile' = 'sf6ingest'
    'scope' = 'repo_maintainer_profiles_only'
    'status' = 'policy_expectation_not_runtime_state'
    'public_distribution_boundary' = 'public_sf6_agent_distribution_deferred'
    'local_state_boundary' = 'do_not_commit_local_hermes_profile_state'
  }
  foreach ($field in $expectedAllowlistValues.Keys) {
    if ((Test-Property $skillAllowlist $field) -and [string]$skillAllowlist.$field -ne $expectedAllowlistValues[$field]) {
      $issues += "Hermes skill allowlist $field must be $($expectedAllowlistValues[$field])"
    }
  }

  $defaultAllowlistIds = Get-ManifestItemIds $skillAllowlist.builtin_default_skills 'Hermes skill allowlist builtin_default_skills' ([ref]$issues)
  $conditionalAllowlistIds = Get-ManifestItemIds $skillAllowlist.builtin_conditional_skills 'Hermes skill allowlist builtin_conditional_skills' ([ref]$issues)
  $externalAllowlistIds = Get-ManifestItemIds $skillAllowlist.external_apm_skills 'Hermes skill allowlist external_apm_skills' ([ref]$issues)
  $deferredAllowlistIds = Get-ManifestItemIds $skillAllowlist.deferred_candidates 'Hermes skill allowlist deferred_candidates' ([ref]$issues)
  $forbiddenAllowlistIds = Get-ManifestItemIds $skillAllowlist.forbidden_categories 'Hermes skill allowlist forbidden_categories' ([ref]$issues)

  foreach ($id in $defaultAllowlistIds) {
    if ($conditionalAllowlistIds -contains $id) {
      $issues += "Hermes skill allowlist must not list $id as both default and conditional"
    }
    if ($externalAllowlistIds -contains $id) {
      $issues += "Hermes skill allowlist must not list $id as both built-in default and external APM"
    }
  }
  foreach ($id in $conditionalAllowlistIds) {
    if ($externalAllowlistIds -contains $id) {
      $issues += "Hermes skill allowlist must not list $id as both built-in conditional and external APM"
    }
  }

  foreach ($requiredDefaultSkill in @(
    'hermes-agent',
    'codex',
    'codebase-inspection',
    'github-issues',
    'github-pr-workflow',
    'github-code-review',
    'github-repo-management',
    'writing-plans',
    'systematic-debugging',
    'test-driven-development',
    'requesting-code-review',
    'spike',
    'subagent-driven-development'
  )) {
    if ($defaultAllowlistIds -notcontains $requiredDefaultSkill) {
      $issues += "Hermes skill allowlist default set missing: $requiredDefaultSkill"
    }
  }

  foreach ($requiredConditionalSkill in @(
    'youtube-content',
    'ocr-and-documents',
    'blogwatcher',
    'dspy',
    'kanban-orchestrator',
    'kanban-worker',
    'jupyter-live-kernel'
  )) {
    if ($conditionalAllowlistIds -notcontains $requiredConditionalSkill) {
      $issues += "Hermes skill allowlist conditional set missing: $requiredConditionalSkill"
    }
    if ($defaultAllowlistIds -contains $requiredConditionalSkill) {
      $issues += "Hermes skill allowlist must not default-enable conditional skill: $requiredConditionalSkill"
    }
  }

  if ($externalAllowlistIds -notcontains 'sympy') {
    $issues += 'Hermes skill allowlist external_apm_skills must include sympy'
  }
  if ($defaultAllowlistIds -contains 'sympy' -or $conditionalAllowlistIds -contains 'sympy') {
    $issues += 'Hermes skill allowlist must not classify sympy as a built-in skill'
  }

  if (Test-Property $skillAllowlist 'external_apm_skills') {
    foreach ($externalSkill in @($skillAllowlist.external_apm_skills)) {
      if ((Test-Property $externalSkill 'id') -and [string]$externalSkill.id -eq 'sympy') {
        $expectedExternalValues = @{
          'source_kind' = 'external_apm'
          'source_manifest' = 'tools/agent-skills/apm.yml'
          'lockfile' = 'tools/agent-skills/apm.lock.yaml'
          'dependency' = 'K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0'
          'virtual_path' = 'scientific-skills/sympy'
          'pin_policy' = 'reviewed_tag_or_immutable_sha_required'
          'authority_boundary' = 'not_sf6_formula_or_current_fact_authority'
          'public_answer_boundary' = 'not_public_adapter_dependency'
        }
        foreach ($field in $expectedExternalValues.Keys) {
          Assert-Property $externalSkill $field 'Hermes skill allowlist sympy external_apm skill' ([ref]$issues)
          if ((Test-Property $externalSkill $field) -and [string]$externalSkill.$field -ne $expectedExternalValues[$field]) {
            $issues += "Hermes skill allowlist sympy $field must be $($expectedExternalValues[$field])"
          }
        }
      }
    }
  }

  foreach ($requiredDeferred in @(
    'sagemath-skills',
    'statistics-skills',
    'mcp-servers',
    'gateway-bot-skills',
    'cron-kanban-defaults',
    'external-memory-providers',
    'public-sf6-agent-distribution'
  )) {
    if ($deferredAllowlistIds -notcontains $requiredDeferred) {
      $issues += "Hermes skill allowlist deferred candidate missing: $requiredDeferred"
    }
  }

  foreach ($requiredForbidden in @(
    'red_teaming',
    'smart_home',
    'social_media_posting',
    'unrelated_ml_training_or_serving',
    'secrets_or_profile_state',
    'raw_transcripts_or_runtime_state'
  )) {
    if ($forbiddenAllowlistIds -notcontains $requiredForbidden) {
      $issues += "Hermes skill allowlist forbidden category missing: $requiredForbidden"
    }
  }

  $reviewCommands = if (Test-Property $skillAllowlist 'review_commands') { @($skillAllowlist.review_commands | ForEach-Object { [string]$_ }) } else { @() }
  foreach ($reviewCommand in @('hermes skills list', 'hermes skills inspect hermes-agent')) {
    if ($reviewCommands -notcontains $reviewCommand) {
      $issues += "Hermes skill allowlist missing review command: $reviewCommand"
    }
  }

  $sourceRefs = if (Test-Property $skillAllowlist 'source_refs') { @($skillAllowlist.source_refs | ForEach-Object { [string]$_ }) } else { @() }
  foreach ($sourceRef in @(
    'docs/architecture/hermes-maintainer-profile-policy.md',
    'docs/architecture/agent-skill-dependency-policy.md',
    'tools/agent-skills/apm.yml',
    'tools/agent-skills/apm.lock.yaml',
    'workflows/hermes-ingest-profile-setup.md'
  )) {
    if ($sourceRefs -notcontains $sourceRef) {
      $issues += "Hermes skill allowlist missing source ref: $sourceRef"
    }
  }

  $apmTextForAllowlist = if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/agent-skills/apm.yml') -PathType Leaf) { Read-Text 'tools/agent-skills/apm.yml' } else { '' }
  $apmLockTextForAllowlist = if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/agent-skills/apm.lock.yaml') -PathType Leaf) { Read-Text 'tools/agent-skills/apm.lock.yaml' } else { '' }
  if ($apmTextForAllowlist -notmatch [regex]::Escape('K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0')) {
    $issues += 'Hermes skill allowlist expects SymPy dependency, but tools/agent-skills/apm.yml does not contain the pinned dependency'
  }
  if ($apmLockTextForAllowlist -notmatch [regex]::Escape('virtual_path: scientific-skills/sympy')) {
    $issues += 'Hermes skill allowlist expects SymPy virtual_path, but tools/agent-skills/apm.lock.yaml does not contain it'
  }
  if ($apmTextForAllowlist -match [regex]::Escape('K-Dense-AI/scientific-agent-skills#')) {
    $issues += 'Hermes skill allowlist forbids broad K-Dense-AI scientific-agent-skills root bundle dependency'
  }

  $allowlistStringValues = @(Get-JsonStringValues $skillAllowlist)
  foreach ($stringValue in $allowlistStringValues) {
    foreach ($forbiddenText in @(
      '~/.hermes',
      'HERMES_HOME',
      '.env',
      'auth.json',
      'memories/',
      'sessions/',
      'state.db',
      'logs/',
      '/home/',
      'C:\'
    )) {
      if ($stringValue -match [regex]::Escape($forbiddenText)) {
        $issues += "Hermes skill allowlist contains forbidden local-state text: $forbiddenText"
      }
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/agent-skill-dependency-policy.md') -PathType Leaf) {
  $agentSkillPolicy = Read-Text 'docs/architecture/agent-skill-dependency-policy.md'
  foreach ($needle in @(
    'tools/agent-skills/apm.yml',
    'tools/agent-skills/apm.lock.yaml',
    'data/toolchain/hermes-maintainer-skill-allowlist.json',
    'docs/architecture/calculation-backend-policy.md',
    'executor / operator instruction dependency',
    'reviewed tag or immutable SHA',
    'Renovate',
    'git-tags',
    'git-refs',
    'SymPy',
    'external_apm_skills',
    'SageMath',
    'K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0',
    'must not become repo-owned SF6 formula authority'
  )) {
    if ($agentSkillPolicy -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/agent-skill-dependency-policy.md missing policy text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/hermes-maintainer-profile-policy.md') -PathType Leaf) {
  $profilePolicyText = Read-Text 'docs/architecture/hermes-maintainer-profile-policy.md'
  foreach ($needle in @(
    'data/toolchain/hermes-maintainer-skill-allowlist.json',
    'contracts/hermes-maintainer-skill-allowlist.schema.json',
    'built-in default skills',
    'built-in conditional skills',
    'external APM-managed skills',
    'deferred candidates',
    'forbidden skill categories',
    'External Agent Skills are not built-in Hermes skills',
    'public answer authority'
  )) {
    if ($profilePolicyText -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/hermes-maintainer-profile-policy.md missing skill allowlist policy text: $needle"
    }
  }

  foreach ($needle in @(
    'Freshness Review Is Not Profile Export',
    'policy expectations',
    'not local proof',
    'profile listings',
    'hermes doctor',
    'device codes'
  )) {
    if ($profilePolicyText -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/hermes-maintainer-profile-policy.md missing freshness boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'workflows/hermes-ingest-profile-setup.md') -PathType Leaf) {
  $ingestProfileSetupText = Read-Text 'workflows/hermes-ingest-profile-setup.md'
  foreach ($needle in @(
    'data/toolchain/hermes-maintainer-skill-allowlist.json',
    'built-in default skills',
    'Built-in conditional skills',
    'external APM skills',
    'hermes skills list',
    'tools/agent-skills/',
    'external_apm_skills',
    'Broad third-party skill bundles'
  )) {
    if ($ingestProfileSetupText -notmatch [regex]::Escape($needle)) {
      $issues += "workflows/hermes-ingest-profile-setup.md missing skill allowlist setup text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/calculation-backend-policy.md') -PathType Leaf) {
  $calculationBackendPolicy = Read-Text 'docs/architecture/calculation-backend-policy.md'
  foreach ($needle in @(
    'SymPy is the initial default maintainer-local calculation backend',
    'sympy==1.14.0',
    'K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0',
    'tools/agent-skills/apm.lock.yaml',
    'SageMath is deferred',
    'MCP servers are deferred',
    'statistics are catalogued candidates only',
    'not SF6 formula authority',
    'not accepted repo formula authority'
  )) {
    if ($calculationBackendPolicy -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/calculation-backend-policy.md missing policy text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/hermes-memory-policy.md') -PathType Leaf) {
  $memoryPolicy = Read-Text 'docs/architecture/hermes-memory-policy.md'
  foreach ($needle in @(
    'built-in memory',
    'session_search',
    'local non-canonical context',
    'external Memory Provider',
    'defer',
    'Holographic',
    'Honcho',
    'Mem0',
    'Hindsight',
    'Memory and session search may improve operator efficiency, but they must not override current git, disk, issue, PR, validator, or checked-in artifact evidence',
    'Do not commit:',
    'state.db',
    'provider output remains non-canonical'
  )) {
    if ($memoryPolicy -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/hermes-memory-policy.md missing policy text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/hermes-curator-worktree-checkpoint-policy.md') -PathType Leaf) {
  $lifecyclePolicy = Read-Text 'docs/architecture/hermes-curator-worktree-checkpoint-policy.md'
  foreach ($needle in @(
    'Curator / Worktree / Checkpoint Policy',
    'hermes curator run --dry-run',
    'hermes curator pin <skill>',
    'hermes curator backup --reason',
    'hermes curator rollback',
    'hermes curator restore <skill>',
    'hermes -w',
    'dedicated git worktree',
    '/rollback diff <N>',
    '~/.hermes/checkpoints/',
    'Git commit、validator、PR review の代替にはしない',
    'Gateway、cron、Kanban は v2.6 既定では有効化しない',
    'Do not commit:',
    '~/.hermes/logs/curator/',
    'checkpoint store'
  )) {
    if ($lifecyclePolicy -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/hermes-curator-worktree-checkpoint-policy.md missing policy text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'docs/architecture/agent-toolchain-freshness.md') -PathType Leaf) {
  $freshnessPolicy = Read-Text 'docs/architecture/agent-toolchain-freshness.md'
  foreach ($needle in @(
    'Freshness Continuation',
    'flake.lock',
    'Renovate Nix flake PRs',
    'policy expectations',
    'not local proof',
    'gpt-5.5',
    'xhigh',
    'command transcripts',
    'doctor transcripts',
    'commit-behind counts'
  )) {
    if ($freshnessPolicy -notmatch [regex]::Escape($needle)) {
      $issues += "docs/architecture/agent-toolchain-freshness.md missing freshness boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'workflows/check-agent-toolchain-freshness.md') -PathType Leaf) {
  $freshnessWorkflow = Read-Text 'workflows/check-agent-toolchain-freshness.md'
  foreach ($needle in @(
    'Canonical Hermes CLI Freshness Route',
    'Renovate Nix flake PRs',
    'operator diagnostics',
    'local profile state',
    'policy expectations',
    'not copied local profile state',
    'gpt-5.5',
    'xhigh',
    'command transcripts',
    'doctor transcripts',
    'profile listings',
    'device codes'
  )) {
    if ($freshnessWorkflow -notmatch [regex]::Escape($needle)) {
      $issues += "workflows/check-agent-toolchain-freshness.md missing freshness boundary text: $needle"
    }
  }
}

if (Test-Path -LiteralPath (Join-Path $repoRoot $manifestPath) -PathType Leaf) {
  $manifestRaw = Get-Content -LiteralPath (Join-Path $repoRoot $manifestPath) -Raw -Encoding UTF8
  $manifest = $manifestRaw | ConvertFrom-Json

  foreach ($propertyName in @($manifest.PSObject.Properties.Name)) {
    if ($allowedRootProperties -notcontains $propertyName) {
      $issues += "$manifestPath contains unsupported root property: $propertyName"
    }
  }

  foreach ($field in @('schema_version', 'last_reviewed', 'tools', 'boundaries')) {
    Assert-Property $manifest $field $manifestPath ([ref]$issues)
  }

  if ((Test-Property $manifest 'schema_version') -and $manifest.schema_version -ne 'agent-toolchain/v1') {
    $issues += "$manifestPath must use schema_version agent-toolchain/v1"
  }

  foreach ($propertyName in @(Get-JsonPropertyNames $manifest)) {
    $propertyNameLower = $propertyName.ToLowerInvariant()
    foreach ($field in $forbiddenManifestFields) {
      if ($propertyNameLower.Contains($field)) {
        $issues += "$manifestPath contains forbidden local-state or secret-like property: $propertyName"
        break
      }
    }
  }

  foreach ($stringValue in @(Get-JsonStringValues $manifest)) {
    foreach ($localOutputPattern in @(
      'Hermes Agent v\d+\.\d+\.\d+',
      '\d+ commits behind',
      'Project: /',
      'Project: [A-Za-z]:\\',
      'Python: \d+\.\d+',
      'OpenAI SDK: \d+\.\d+',
      'Update available:',
      'Active profile:',
      'Profile path:',
      'Config path:',
      'HERMES_HOME=',
      'auth\.json',
      'state\.db',
      'device code',
      'Doctor report:'
    )) {
      if ([string]$stringValue -match $localOutputPattern) {
        $issues += "$manifestPath contains local command output or installed-version-like value: $stringValue"
        break
      }
    }
  }

  if (Test-Property $manifest 'tools') {
    $tools = @($manifest.tools)
    $toolsById = @{}
    foreach ($tool in $tools) {
      if (Test-Property $tool 'id') {
        $toolsById[[string]$tool.id] = $tool
      }
    }

    foreach ($toolId in @('codex-cli', 'hermes-cli')) {
      if (-not $toolsById.ContainsKey($toolId)) {
        $issues += "$manifestPath missing tool entry: $toolId"
      }
    }

    if ($toolsById.ContainsKey('codex-cli')) {
      $codex = $toolsById['codex-cli']
      if ((Test-Property $codex 'role') -and $codex.role -ne 'repo_implementation_executor') {
        $issues += 'codex-cli must use role repo_implementation_executor'
      }
    }

    if ($toolsById.ContainsKey('hermes-cli')) {
      $hermes = $toolsById['hermes-cli']
      if ((Test-Property $hermes 'role') -and $hermes.role -ne 'repo_local_growth_engine') {
        $issues += 'hermes-cli must use role repo_local_growth_engine'
      }
      if ((Test-Property $hermes 'version_command') -and $hermes.version_command -ne 'nix run .#hermes -- --version') {
        $issues += 'hermes-cli version_command must use the repo Nix flake'
      }
    }

    foreach ($tool in $tools) {
      $toolId = if (Test-Property $tool 'id') { [string]$tool.id } else { '<missing-id>' }
      foreach ($propertyName in @($tool.PSObject.Properties.Name)) {
        if ($allowedToolProperties -notcontains $propertyName) {
          $issues += "$manifestPath tool $toolId contains unsupported property: $propertyName"
        }
      }
      foreach ($field in @(
        'recommended_channel',
        'known_good_version',
        'required_capabilities',
        'planned_capabilities',
        'version_command',
        'version_command_review_note',
        'update_guidance',
        'freshness_review_cadence'
      )) {
        Assert-Property $tool $field "$manifestPath tool $toolId" ([ref]$issues)
      }

      if ((Test-Property $tool 'id') -and $allowedToolIds -notcontains [string]$tool.id) {
        $issues += "$manifestPath tool $toolId has unsupported id: $($tool.id)"
      }
      if ((Test-Property $tool 'role') -and $allowedRoles -notcontains [string]$tool.role) {
        $issues += "$manifestPath tool $toolId has unsupported role: $($tool.role)"
      }
      if ((Test-Property $tool 'recommended_channel') -and $allowedRecommendedChannels -notcontains [string]$tool.recommended_channel) {
        $issues += "$manifestPath tool $toolId has unsupported recommended_channel: $($tool.recommended_channel)"
      }
      if ((Test-Property $tool 'required_capabilities') -and @($tool.required_capabilities).Count -eq 0) {
        $issues += "$manifestPath tool $toolId must include required_capabilities"
      }
      if ((Test-Property $tool 'version_command') -and $null -ne $tool.version_command) {
        if (-not (Test-Property $tool 'version_command_review_note') -or [string]::IsNullOrWhiteSpace([string]$tool.version_command_review_note)) {
          $issues += "$manifestPath tool $toolId with version_command must include version_command_review_note"
        }
      }
    }

    if ($toolsById.ContainsKey('hermes-cli')) {
      $hermes = $toolsById['hermes-cli']
      $capabilities = @()
      if (Test-Property $hermes 'required_capabilities') {
        $capabilities += @($hermes.required_capabilities)
      }
      if (Test-Property $hermes 'planned_capabilities') {
        $capabilities += @($hermes.planned_capabilities)
      }
      $capabilityText = (($capabilities | ForEach-Object { [string]$_ }) -join ' ').ToLowerInvariant()

      $capabilityChecks = @{
        'subagents or delegation' = @('subagent', 'delegation')
        'local skills' = @('skill')
        'Curator' = @('curator')
        'session search' = @('session_search', 'session search')
        '/goal or checkpoints' = @('goal', 'checkpoint')
        'cron or freshness audits' = @('cron', 'freshness')
      }

      foreach ($label in $capabilityChecks.Keys) {
        $found = $false
        foreach ($needle in $capabilityChecks[$label]) {
          if ($capabilityText.Contains($needle)) {
            $found = $true
          }
        }
        if (-not $found) {
          $issues += "hermes-cli capabilities must include $label"
        }
      }

      if (-not (Test-Property $hermes 'maintainer_profile_policy')) {
        $issues += 'hermes-cli must include maintainer_profile_policy'
      } else {
        $profilePolicy = $hermes.maintainer_profile_policy
        foreach ($field in @(
          'profile_expectation_scope',
          'profile_names',
          'required_model',
          'accepted_model_aliases',
          'required_reasoning_effort',
          'accepted_reasoning_effort_aliases',
          'reasoning_effort_requirement_mode',
          'profile_check_commands',
          'profile_check_output_policy',
          'skill_selection_policy'
        )) {
          Assert-Property $profilePolicy $field 'hermes-cli maintainer_profile_policy' ([ref]$issues)
        }

        if ((Test-Property $profilePolicy 'profile_expectation_scope') -and $profilePolicy.profile_expectation_scope -ne 'repo_maintainer_profiles_only') {
          $issues += 'Hermes profile policy must be repo_maintainer_profiles_only'
        }
        if ((Test-Property $profilePolicy 'required_model') -and $profilePolicy.required_model -ne 'gpt-5.5') {
          $issues += 'Hermes profile policy required_model must be gpt-5.5'
        }
        if ((Test-Property $profilePolicy 'required_reasoning_effort') -and $profilePolicy.required_reasoning_effort -ne 'xhigh') {
          $issues += 'Hermes profile policy required_reasoning_effort must be xhigh'
        }
        if ((Test-Property $profilePolicy 'reasoning_effort_requirement_mode') -and $profilePolicy.reasoning_effort_requirement_mode -ne 'required_when_supported') {
          $issues += 'Hermes profile policy reasoning_effort_requirement_mode must be required_when_supported'
        }
        if ((Test-Property $profilePolicy 'profile_check_output_policy') -and $profilePolicy.profile_check_output_policy -ne 'local_profile_output_is_noncanonical_review_signal') {
          $issues += 'Hermes profile policy must keep local profile output noncanonical'
        }

        $profileNames = if (Test-Property $profilePolicy 'profile_names') { @($profilePolicy.profile_names) } else { @() }
        if ($profileNames -notcontains 'sf6ingest') {
          $issues += 'Hermes profile policy missing expected profile: sf6ingest'
        }
        foreach ($profileName in $profileNames) {
          if ([string]$profileName -ne 'sf6ingest') {
            $issues += "Hermes profile policy has unsupported profile: $profileName"
          }
        }

        $modelAliases = if (Test-Property $profilePolicy 'accepted_model_aliases') { @($profilePolicy.accepted_model_aliases) } else { @() }
        foreach ($modelAlias in @('gpt-5.5', 'codex 5.5')) {
          if ($modelAliases -notcontains $modelAlias) {
            $issues += "Hermes profile policy missing model alias: $modelAlias"
          }
        }

        $reasoningAliases = if (Test-Property $profilePolicy 'accepted_reasoning_effort_aliases') { @($profilePolicy.accepted_reasoning_effort_aliases) } else { @() }
        foreach ($reasoningAlias in @('xhigh', 'extra-high', 'extra_high')) {
          if ($reasoningAliases -notcontains $reasoningAlias) {
            $issues += "Hermes profile policy missing reasoning alias: $reasoningAlias"
          }
        }

        $profileCheckCommands = if (Test-Property $profilePolicy 'profile_check_commands') { @($profilePolicy.profile_check_commands) } else { @() }
        foreach ($profileCheckCommand in @('hermes profile list', 'hermes profile show sf6ingest')) {
          if ($profileCheckCommands -notcontains $profileCheckCommand) {
            $issues += "Hermes profile policy missing profile check command: $profileCheckCommand"
          }
        }
        foreach ($profileCheckCommand in $profileCheckCommands) {
          if ($profileCheckCommand -notmatch '^hermes profile (list|show sf6ingest)$') {
            $issues += "Hermes profile policy has unsupported profile check command: $profileCheckCommand"
          }
        }

        if (-not (Test-Property $profilePolicy 'skill_selection_policy')) {
          $issues += 'Hermes profile policy must include skill_selection_policy'
        } else {
          $skillPolicy = $profilePolicy.skill_selection_policy
          $expectedSkillPolicyValues = @{
            'selection_scope' = 'repo_maintainer_profiles_only'
            'selection_status' = 'policy_expectation_not_runtime_state'
            'skill_review_output_policy' = 'local_skill_output_is_noncanonical_review_signal'
          }

          foreach ($field in $expectedSkillPolicyValues.Keys) {
            Assert-Property $skillPolicy $field 'hermes-cli skill_selection_policy' ([ref]$issues)
            if ((Test-Property $skillPolicy $field) -and [string]$skillPolicy.$field -ne $expectedSkillPolicyValues[$field]) {
              $issues += "Hermes skill_selection_policy $field must be $($expectedSkillPolicyValues[$field])"
            }
          }

          foreach ($field in @(
            'applies_to_profile',
            'hub_context',
            'allowlist_manifest',
            'allowlist_schema',
            'purpose',
            'default_builtin_skills',
            'conditional_builtin_skills',
            'forbidden_skill_categories',
            'skill_review_commands'
          )) {
            Assert-Property $skillPolicy $field 'hermes-cli skill_selection_policy' ([ref]$issues)
          }
          if ((Test-Property $skillPolicy 'applies_to_profile') -and [string]$skillPolicy.applies_to_profile -ne 'sf6ingest') {
            $issues += 'Hermes skill_selection_policy applies_to_profile must be sf6ingest'
          }
          if ((Test-Property $skillPolicy 'allowlist_manifest') -and [string]$skillPolicy.allowlist_manifest -ne 'data/toolchain/hermes-maintainer-skill-allowlist.json') {
            $issues += 'Hermes skill_selection_policy allowlist_manifest must be data/toolchain/hermes-maintainer-skill-allowlist.json'
          }
          if ((Test-Property $skillPolicy 'allowlist_schema') -and [string]$skillPolicy.allowlist_schema -ne 'contracts/hermes-maintainer-skill-allowlist.schema.json') {
            $issues += 'Hermes skill_selection_policy allowlist_schema must be contracts/hermes-maintainer-skill-allowlist.schema.json'
          }

          if (Test-Property $skillPolicy 'hub_context') {
            $hubContext = $skillPolicy.hub_context
            foreach ($field in @('source', 'last_reviewed', 'advertised_total_skills', 'advertised_builtin_skills', 'narrowing_reason')) {
              Assert-Property $hubContext $field 'hermes-cli skill_selection_policy hub_context' ([ref]$issues)
            }
            if ((Test-Property $hubContext 'source') -and [string]$hubContext.source -ne 'Hermes Skills Hub') {
              $issues += 'Hermes skill_selection_policy hub_context source must be Hermes Skills Hub'
            }
            if ((Test-Property $hubContext 'advertised_total_skills') -and [int]$hubContext.advertised_total_skills -lt 1) {
              $issues += 'Hermes skill_selection_policy advertised_total_skills must be positive'
            }
            if ((Test-Property $hubContext 'advertised_builtin_skills') -and [int]$hubContext.advertised_builtin_skills -lt 1) {
              $issues += 'Hermes skill_selection_policy advertised_builtin_skills must be positive'
            }
          }

          $skillReviewCommands = if (Test-Property $skillPolicy 'skill_review_commands') { @($skillPolicy.skill_review_commands) } else { @() }
          foreach ($skillReviewCommand in @('hermes skills list', 'hermes skills inspect hermes-agent')) {
            if ($skillReviewCommands -notcontains $skillReviewCommand) {
              $issues += "Hermes skill_selection_policy missing skill review command: $skillReviewCommand"
            }
          }
          foreach ($skillReviewCommand in $skillReviewCommands) {
            if ($skillReviewCommand -notmatch '^hermes skills (list|inspect hermes-agent)$') {
              $issues += "Hermes skill_selection_policy has unsupported skill review command: $skillReviewCommand"
            }
          }

          foreach ($arrayField in @('default_builtin_skills', 'conditional_builtin_skills', 'forbidden_skill_categories')) {
            if (Test-Property $skillPolicy $arrayField) {
              $values = @($skillPolicy.$arrayField | ForEach-Object { [string]$_ })
              $uniqueValues = @($values | Select-Object -Unique)
              if ($values.Count -ne $uniqueValues.Count) {
                $issues += "Hermes skill_selection_policy $arrayField contains duplicates"
              }
              foreach ($value in $values) {
                if ([string]::IsNullOrWhiteSpace($value)) {
                  $issues += "Hermes skill_selection_policy $arrayField contains an empty value"
                }
              }
            }
          }

          $defaultSkills = if (Test-Property $skillPolicy 'default_builtin_skills') { @($skillPolicy.default_builtin_skills | ForEach-Object { [string]$_ }) } else { @() }
          $conditionalSkills = if (Test-Property $skillPolicy 'conditional_builtin_skills') { @($skillPolicy.conditional_builtin_skills | ForEach-Object { [string]$_ }) } else { @() }
          $forbiddenCategories = if (Test-Property $skillPolicy 'forbidden_skill_categories') { @($skillPolicy.forbidden_skill_categories | ForEach-Object { [string]$_ }) } else { @() }

          if (Test-Path -LiteralPath (Join-Path $repoRoot 'data/toolchain/hermes-maintainer-skill-allowlist.json') -PathType Leaf) {
            $allowlistForToolchain = Read-Json 'data/toolchain/hermes-maintainer-skill-allowlist.json'
            $allowlistDefaultIds = @($allowlistForToolchain.builtin_default_skills | ForEach-Object { [string]$_.id })
            $allowlistConditionalIds = @($allowlistForToolchain.builtin_conditional_skills | ForEach-Object { [string]$_.id })
            $allowlistForbiddenIds = @($allowlistForToolchain.forbidden_categories | ForEach-Object { [string]$_.id })

            Assert-SetEquals $defaultSkills $allowlistDefaultIds 'Hermes skill_selection_policy default_builtin_skills must match allowlist builtin_default_skills' ([ref]$issues)
            Assert-SetEquals $conditionalSkills $allowlistConditionalIds 'Hermes skill_selection_policy conditional_builtin_skills must match allowlist builtin_conditional_skills' ([ref]$issues)
            Assert-SetEquals $forbiddenCategories $allowlistForbiddenIds 'Hermes skill_selection_policy forbidden_skill_categories must match allowlist forbidden_categories' ([ref]$issues)
          }

          foreach ($requiredSkill in @(
            'hermes-agent',
            'codex',
            'codebase-inspection',
            'github-issues',
            'github-pr-workflow',
            'github-code-review',
            'writing-plans',
            'systematic-debugging',
            'test-driven-development',
            'requesting-code-review',
            'subagent-driven-development'
          )) {
            if ($defaultSkills -notcontains $requiredSkill) {
              $issues += "sf6ingest default skill set missing: $requiredSkill"
            }
          }

          foreach ($conditionalSkill in @('youtube-content', 'ocr-and-documents', 'blogwatcher', 'dspy')) {
            if ($conditionalSkills -notcontains $conditionalSkill) {
              $issues += "sf6ingest conditional skill set missing: $conditionalSkill"
            }
            if ($defaultSkills -contains $conditionalSkill) {
              $issues += "sf6ingest must not default-enable external/source helper skill: $conditionalSkill"
            }
          }

          foreach ($requiredForbiddenCategory in @('red_teaming', 'smart_home', 'social_media_posting', 'unrelated_ml_training_or_serving')) {
            if ($forbiddenCategories -notcontains $requiredForbiddenCategory) {
              $issues += "sf6ingest forbidden categories missing: $requiredForbiddenCategory"
            }
          }
        }
      }

      if (-not (Test-Property $hermes 'version_management')) {
        $issues += 'hermes-cli must include version_management'
      } else {
        $versionManagement = $hermes.version_management
        foreach ($field in @(
          'primary_pin_surface',
          'primary_update_surface',
          'flake_input',
          'flake_input_url',
          'manual_update_command',
          'fallback_local_check_commands',
          'fallback_local_update_command',
          'local_output_policy'
        )) {
          Assert-Property $versionManagement $field 'hermes-cli version_management' ([ref]$issues)
        }

        $expectedVersionValues = @{
          'primary_pin_surface' = 'nix_flake_lock'
          'primary_update_surface' = 'renovate_nix_flake_pr'
          'flake_input' = 'hermes-agent'
          'flake_input_url' = 'github:NousResearch/hermes-agent'
          'manual_update_command' = 'nix flake update hermes-agent'
          'fallback_local_update_command' = 'hermes update'
          'local_output_policy' = 'local_command_output_is_noncanonical_review_signal'
        }

        foreach ($field in $expectedVersionValues.Keys) {
          if ((Test-Property $versionManagement $field) -and [string]$versionManagement.$field -ne $expectedVersionValues[$field]) {
            $issues += "Hermes version_management $field must be $($expectedVersionValues[$field])"
          }
        }

        $fallbackCommands = if (Test-Property $versionManagement 'fallback_local_check_commands') { @($versionManagement.fallback_local_check_commands) } else { @() }
        foreach ($fallbackCommand in @('hermes --version', 'hermes doctor')) {
          if ($fallbackCommands -notcontains $fallbackCommand) {
            $issues += "Hermes version_management missing fallback command: $fallbackCommand"
          }
        }
        foreach ($fallbackCommand in $fallbackCommands) {
          if ($fallbackCommand -notmatch '^hermes (--version|doctor)$') {
            $issues += "Hermes version_management has unsupported fallback command: $fallbackCommand"
          }
        }
      }
    }
  }

  if (Test-Property $manifest 'boundaries') {
    $boundaryText = (@($manifest.boundaries) -join ' ')
    foreach ($needle in @(
      'toolchain policy is not SF6 gameplay knowledge',
      'local tool state is non-canonical',
      'CI must not call the internet for latest-version checks'
    )) {
      if ($boundaryText -notmatch [regex]::Escape($needle)) {
        $issues += "$manifestPath missing boundary: $needle"
      }
    }
  }
}

if (-not (Test-Path -LiteralPath $toolchainRoot -PathType Container)) {
  $issues += "Missing toolchain root: $toolchainRootRelative"
} else {
  foreach ($item in Get-ChildItem -LiteralPath $toolchainRoot -Force -Recurse -File) {
    $name = $item.Name.ToLowerInvariant()
    $relativePath = Get-ToolchainRelativePath $item.FullName
    $relativePathLower = $relativePath.ToLowerInvariant()

    if (
      $name -eq '.env' -or
      $name -like '.env.*' -or
      $name -eq '.envrc' -or
      $name -like '*secret*' -or
      $name -like '*token*' -or
      $name -like '*credential*' -or
      $name -like '*session*' -or
      $name -like '*cache*' -or
      $name -like '*log*' -or
      $name -like '*transcript*' -or
      $name -like '*profile-output*' -or
      $name -like '*doctor-output*' -or
      $name -like '*command-output*' -or
      $relativePathLower -like '*/.env' -or
      $relativePathLower -like '*/.env.*' -or
      $relativePathLower -like '*/.envrc' -or
      $relativePathLower -like '*secret*' -or
      $relativePathLower -like '*token*' -or
      $relativePathLower -like '*credential*' -or
      $relativePathLower -like '*session*' -or
      $relativePathLower -like '*cache*' -or
      $relativePathLower -like '*log*' -or
      $relativePathLower -like '*transcript*' -or
      $relativePathLower -like '*profile-output*' -or
      $relativePathLower -like '*doctor-output*' -or
      $relativePathLower -like '*command-output*'
    ) {
      $issues += "Forbidden toolchain local-state or secret-like file: $relativePath"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Agent toolchain OK'
