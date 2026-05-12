Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$packRootRelative = 'packs/codex-hermes-sf6'
$packRoot = Join-Path $repoRoot $packRootRelative

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Add-Issue {
  param(
    [Parameter(Mandatory = $true)][ref]$Issues,
    [Parameter(Mandatory = $true)][string]$Message
  )
  $Issues.Value += $Message
}

function Assert-File {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $RelativePath) -PathType Leaf)) {
    $Issues.Value += "Missing Codex-Hermes pack file: $RelativePath"
  }
}

function Get-PackRelativePath {
  param([Parameter(Mandatory = $true)][string]$FullPath)

  $root = (Resolve-Path $packRoot).Path.TrimEnd([char[]]@('\', '/'))
  $relative = $FullPath.Substring($root.Length)
  $relative = $relative -replace '^[\\/]+', ''
  return "$packRootRelative/$($relative -replace '\\', '/')"
}

$requiredFiles = @(
  'packs/codex-hermes-sf6/README.md',
  'packs/codex-hermes-sf6/skill/SKILL.md',
  'packs/codex-hermes-sf6/resources/codex-to-hermes-request-template.md',
  'packs/codex-hermes-sf6/resources/hermes-response-review-checklist.md',
  'packs/codex-hermes-sf6/resources/stale-debt-boundary.md',
  'packs/codex-hermes-sf6/resources/hermes-cli-capability-reference.md',
  'packs/codex-hermes-sf6/resources/sf6-video-analysis-protocol.md',
  'packs/codex-hermes-sf6/resources/external-frame-atlas-policy.md',
  'packs/codex-hermes-sf6/guards/hermes-local-state-boundary.md',
  'packs/codex-hermes-sf6/guards/current-fact-boundary.md',
  'packs/codex-hermes-sf6/guards/article-video-boundary.md',
  'packs/codex-hermes-sf6/guards/video-observation-boundary.md',
  'packs/codex-hermes-sf6/guards/external-visual-asset-boundary.md'
)

$issues = @()

if (-not (Test-Path -LiteralPath $packRoot -PathType Container)) {
  $issues += "Missing Codex-Hermes pack root: $packRootRelative"
}

foreach ($relativePath in $requiredFiles) {
  Assert-File $relativePath ([ref]$issues)
}

if (Test-Path -LiteralPath (Join-Path $repoRoot 'skills/codex-hermes-sf6')) {
  $issues += 'Codex-Hermes maintainer support must not be placed under skills/.'
}

if ($issues.Count -eq 0) {
  $combinedText = ($requiredFiles | ForEach-Object { Read-Text $_ }) -join "`n"

  $requiredPhrases = @(
    'repo-local maintainer support only',
    'does not define public answer behavior',
    'workflows/maintainer-agent-session.md',
    'workflows/codex-to-hermes-delegation.md',
    'docs/architecture/codex-hermes-bridge-policy.md',
    'docs/architecture/hermes-cli-capability-reference.md',
    'docs/architecture/sf6-video-analysis-protocol.md',
    'docs/architecture/external-frame-atlas-policy.md',
    'Hermes output remains draft input',
    'Stale PR #71 and PR #83 are closed historical debt',
    'official_raw'
  )

  foreach ($phrase in $requiredPhrases) {
    if ($combinedText -notmatch [regex]::Escape($phrase)) {
      $issues += "Codex-Hermes pack missing required phrase: $phrase"
    }
  }

  $cliPointer = Read-Text 'packs/codex-hermes-sf6/resources/hermes-cli-capability-reference.md'
  if ($cliPointer -match '\|\s*Capability\s*\|') {
    $issues += 'Codex-Hermes pack must not duplicate the #121 Hermes CLI capability command table.'
  }

  $activePublicAnswerPatterns = @(
    '(?im)^\s*(this pack|the pack)\s+defines\s+public answer behavior',
    '(?im)^\s*define\s+public answer behavior'
  )
  foreach ($pattern in $activePublicAnswerPatterns) {
    if ($combinedText -match $pattern) {
      $issues += 'Codex-Hermes pack appears to define public answer behavior.'
    }
  }

  $activeStoragePattern = '(?im)^\s*(commit|store|save|persist|include|write|add)\b.*\b(memory|sessions?|local skills?|curator|browser state|cron state|kanban state|checkpoints?|local configs?|logs?|caches?|credentials?|secrets?|tokens?)\b'
  $activeStalePattern = '(?i)\b(use|treat|list|include)\b.*\b(PR #71|PR #83)\b.*\bactive source\b'
  foreach ($relativePath in $requiredFiles) {
    $lineNumber = 0
    foreach ($line in (Read-Text $relativePath) -split "`r?`n") {
      $lineNumber += 1
      if (
        $line -match $activeStalePattern -and
        $line -notmatch '(?i)\b(do not|must not|not active|closed historical debt)\b'
      ) {
        $issues += "Codex-Hermes pack treats stale PR #71 or #83 as active source material in $relativePath line ${lineNumber}: $line"
      }

      if (
        $line -match $activeStoragePattern -and
        $line -notmatch '(?i)\b(do not|must not|forbid|forbidden|not)\b'
      ) {
        $issues += "Potential active local-state storage instruction in $relativePath line ${lineNumber}: $line"
      }
    }
  }
}

if (Test-Path -LiteralPath $packRoot -PathType Container) {
  $forbiddenPathPatterns = @(
    '(^|[\\/])\.env($|[\\.\\/])',
    'secret',
    'token',
    'credential',
    'session',
    'memory',
    'cache',
    'log',
    'browser-state',
    'profile-state',
    'cron',
    'kanban',
    'checkpoint',
    '\.sqlite$',
    '\.db$'
  )

  $binaryExtensions = @('.gif', '.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mov', '.avi', '.mkv')

  foreach ($item in Get-ChildItem -LiteralPath $packRoot -Force -Recurse -File) {
    $relativePath = Get-PackRelativePath $item.FullName
    $relativeLower = $relativePath.ToLowerInvariant()

    foreach ($pattern in $forbiddenPathPatterns) {
      if ($relativeLower -match $pattern) {
        $issues += "Forbidden local-state or secret-like path under Codex-Hermes pack: $relativePath"
      }
    }

    if ($binaryExtensions -contains $item.Extension.ToLowerInvariant()) {
      $issues += "Forbidden binary asset under Codex-Hermes pack: $relativePath"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Codex-Hermes pack OK'
