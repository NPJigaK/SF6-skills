Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$decisionPath = 'docs/architecture/decisions/0001-hermes-primary-orchestration.md'

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Read-FrontMatter {
  param([Parameter(Mandatory = $true)][string]$RelativePath)

  $content = Read-Text $RelativePath
  $match = [regex]::Match($content, "(?s)\A---\s*\r?\n(.*?)\r?\n---")
  $parseIssues = @()
  $metadata = @{}

  if (-not $match.Success) {
    $parseIssues += "$RelativePath missing YAML front matter"
    return [pscustomobject]@{
      Metadata = $metadata
      Issues = $parseIssues
    }
  }

  $currentListKey = $null
  foreach ($rawLine in ($match.Groups[1].Value -split "\r?\n")) {
    $line = $rawLine.TrimEnd()
    if ([string]::IsNullOrWhiteSpace($line)) {
      continue
    }

    if ($line -match '^\s*-\s*(.+?)\s*$') {
      if (-not $currentListKey) {
        $parseIssues += "$RelativePath front matter list item without a parent key: $line"
        continue
      }
      $metadata[$currentListKey] = @($metadata[$currentListKey]) + $matches[1]
      continue
    }

    if ($line -match '^([A-Za-z0-9_]+):\s*(.*?)\s*$') {
      $key = $matches[1]
      $value = $matches[2]
      if ([string]::IsNullOrWhiteSpace($value)) {
        $metadata[$key] = @()
        $currentListKey = $key
      } else {
        $metadata[$key] = $value
        $currentListKey = $null
      }
      continue
    }

    $parseIssues += "$RelativePath front matter uses unsupported YAML syntax: $line"
  }

  return [pscustomobject]@{
    Metadata = $metadata
    Issues = $parseIssues
  }
}

function Assert-FieldEquals {
  param(
    [Parameter(Mandatory = $true)][hashtable]$Metadata,
    [Parameter(Mandatory = $true)][string]$Field,
    [Parameter(Mandatory = $true)][string]$Expected,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not $Metadata.ContainsKey($Field)) {
    $Issues.Value += "$decisionPath missing front matter field: $Field"
    return
  }

  $actual = [string]$Metadata[$Field]
  if ($actual -ne $Expected) {
    $Issues.Value += "$decisionPath front matter field $Field expected '$Expected' but found '$actual'"
  }
}

function Assert-ListContains {
  param(
    [Parameter(Mandatory = $true)][hashtable]$Metadata,
    [Parameter(Mandatory = $true)][string]$Field,
    [Parameter(Mandatory = $true)][string[]]$ExpectedValues,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not $Metadata.ContainsKey($Field)) {
    $Issues.Value += "$decisionPath missing front matter list: $Field"
    return
  }

  $actual = @($Metadata[$Field])
  foreach ($expected in $ExpectedValues) {
    if ($actual -notcontains $expected) {
      $Issues.Value += "$decisionPath front matter list $Field missing value: $expected"
    }
  }
}

$issues = @()

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $decisionPath) -PathType Leaf)) {
  $issues += "Missing architecture decision: $decisionPath"
} else {
  $frontMatter = Read-FrontMatter $decisionPath
  $issues += @($frontMatter.Issues)
  $metadata = [hashtable]$frontMatter.Metadata

  Assert-FieldEquals $metadata 'id' 'adr-0001' ([ref]$issues)
  Assert-FieldEquals $metadata 'status' 'accepted' ([ref]$issues)
  Assert-FieldEquals $metadata 'decision_type' 'architecture_decision' ([ref]$issues)
  Assert-FieldEquals $metadata 'scope' 'repo_local_maintainer_orchestration' ([ref]$issues)
  Assert-FieldEquals $metadata 'public_answer_adapter' 'skills/sf6-agent' ([ref]$issues)
  Assert-FieldEquals $metadata 'hermes_role' 'primary_repo_local_orchestration_when_configured' ([ref]$issues)
  Assert-FieldEquals $metadata 'hermes_distribution' 'repo_local_only' ([ref]$issues)
  Assert-FieldEquals $metadata 'hermes_state' 'non_canonical' ([ref]$issues)

  Assert-ListContains $metadata 'canonical_sources' @(
    'knowledge',
    'data/exports',
    'data/roster',
    'contracts',
    'workflows',
    'evals'
  ) ([ref]$issues)

  Assert-ListContains $metadata 'repo_artifact_outputs' @(
    'knowledge/sources',
    'knowledge/evidence/claims',
    'knowledge/evidence/video-observations',
    'knowledge/review',
    'knowledge/curated',
    'docs/testing/smoke-runs'
  ) ([ref]$issues)

  Assert-ListContains $metadata 'fallback_executors' @(
    'codex',
    'human',
    'other_agents'
  ) ([ref]$issues)

  Assert-ListContains $metadata 'markers' @(
    'sf6.harness.hermes.primary_repo_local_orchestration_when_configured',
    'sf6.boundary.hermes_state_non_canonical',
    'sf6.boundary.public_adapter_remains_sf6_agent',
    'sf6.boundary.repo_artifacts_are_source_of_truth'
  ) ([ref]$issues)
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Architecture markers OK'
