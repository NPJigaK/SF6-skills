Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$packRootRelative = 'packs/hermes-sf6'
$packRoot = Join-Path $repoRoot $packRootRelative

function Read-Text {
  param([Parameter(Mandatory = $true)][string]$RelativePath)
  return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw -Encoding UTF8
}

function Assert-TextContains {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string[]]$Phrases,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $text = Read-Text $RelativePath
  foreach ($phrase in $Phrases) {
    if ($text -notmatch [regex]::Escape($phrase)) {
      $Issues.Value += "$RelativePath missing boundary phrase: $phrase"
    }
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
  'packs/hermes-sf6/README.md',
  'packs/hermes-sf6/prompts/README.md',
  'packs/hermes-sf6/profiles/README.md',
  'packs/hermes-sf6/profiles/ingest-profile-guidance.md',
  'packs/hermes-sf6/profiles/smoke-profile-guidance.md',
  'packs/hermes-sf6/guards/README.md',
  'packs/hermes-sf6/reports/README.md'
)

$commonBoundaryPhrases = @(
  'repo-local orchestration support',
  'not public answer behavior',
  'does not replace skills/sf6-agent',
  'canonical workflows',
  'canonical contracts',
  'non-canonical',
  'repo artifacts'
)

$issues = @()

foreach ($relativePath in $requiredFiles) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath) -PathType Leaf)) {
    $issues += "Missing Hermes pack skeleton file: $relativePath"
  }
}

if ($issues.Count -eq 0) {
  foreach ($relativePath in $requiredFiles) {
    Assert-TextContains $relativePath $commonBoundaryPhrases ([ref]$issues)
  }

  foreach ($relativePath in @(
    'packs/hermes-sf6/profiles/README.md',
    'packs/hermes-sf6/profiles/ingest-profile-guidance.md',
    'packs/hermes-sf6/profiles/smoke-profile-guidance.md'
  )) {
    Assert-TextContains $relativePath @('not executable profile config') ([ref]$issues)
  }

  foreach ($relativePath in @(
    'packs/hermes-sf6/profiles/README.md',
    'packs/hermes-sf6/profiles/ingest-profile-guidance.md',
    'packs/hermes-sf6/profiles/smoke-profile-guidance.md'
  )) {
    Assert-TextContains $relativePath @(
      'gpt-5.5',
      'codex 5.5',
      'xhigh',
      'extra-high',
      'do not commit'
    ) ([ref]$issues)
  }

  Assert-TextContains 'packs/hermes-sf6/profiles/README.md' @(
    'flake.nix',
    'flake.lock',
    'Renovate Nix flake PRs',
    'hermes --version',
    'hermes doctor',
    'hermes profile list',
    'local installed versions'
  ) ([ref]$issues)

  foreach ($relativePath in @(
    'packs/hermes-sf6/README.md',
    'packs/hermes-sf6/prompts/README.md',
    'packs/hermes-sf6/profiles/ingest-profile-guidance.md',
    'packs/hermes-sf6/profiles/smoke-profile-guidance.md',
    'packs/hermes-sf6/guards/README.md',
    'packs/hermes-sf6/reports/README.md'
  )) {
    Assert-TextContains $relativePath @('operational prompt bodies belong to later work') ([ref]$issues)
  }
}

if (-not (Test-Path -LiteralPath $packRoot -PathType Container)) {
  $issues += "Missing Hermes pack root: $packRootRelative"
} else {
  $forbiddenOperationalPromptNames = @(
    'answer-intent-router.md',
    'evidence-gate.md',
    'answer-composer.md',
    'ingest-router.md',
    'article-ingest.md',
    'video-observation.md',
    'review-promotion.md'
  )

  foreach ($item in Get-ChildItem -LiteralPath $packRoot -Force -Recurse -File) {
    $name = $item.Name.ToLowerInvariant()
    $relativePath = Get-PackRelativePath $item.FullName
    $relativePathLower = $relativePath.ToLowerInvariant()

    if (
      $name -eq '.env' -or
      $name -like '.env.*' -or
      $name -eq '.envrc' -or
      $name -like '*secret*' -or
      $name -like '*token*' -or
      $name -like '*credential*' -or
      $name -like '*session*' -or
      $name -like '*sessions*' -or
      $name -like '*memory*' -or
      $name -like '*cron*' -or
      $name -like 'browser-state*' -or
      $name -like 'profile-state*' -or
      $name -like '*.sqlite' -or
      $name -like '*.db' -or
      $relativePathLower -like '*/.env' -or
      $relativePathLower -like '*/.env.*' -or
      $relativePathLower -like '*/.envrc' -or
      $relativePathLower -like '*secret*' -or
      $relativePathLower -like '*token*' -or
      $relativePathLower -like '*credential*' -or
      $relativePathLower -like '*session*' -or
      $relativePathLower -like '*sessions*' -or
      $relativePathLower -like '*memory*' -or
      $relativePathLower -like '*cron*' -or
      $relativePathLower -like '*browser-state*' -or
      $relativePathLower -like '*profile-state*' -or
      $relativePathLower -like '*.sqlite' -or
      $relativePathLower -like '*.db'
    ) {
      $issues += "Forbidden Hermes local-state or secret-like file under pack: $relativePath"
    }

    if ($forbiddenOperationalPromptNames -contains $name) {
      $issues += "Operational Hermes prompt file belongs to later work: $relativePath"
    }
  }

  $profileRoot = Join-Path $packRoot 'profiles'
  if (Test-Path -LiteralPath $profileRoot -PathType Container) {
    foreach ($item in Get-ChildItem -LiteralPath $profileRoot -Force -Recurse -File -Filter '*.json') {
      $issues += "JSON Hermes profile config requires an explicit profile schema: $(Get-PackRelativePath $item.FullName)"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Hermes pack OK'
