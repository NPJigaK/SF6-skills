Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$policyRelativePath = 'workflows/media-scratch-cache-policy.md'
$runAllRelativePath = 'tests/validation/run-all.ps1'

$policyPath = Join-Path $repoRoot $policyRelativePath
$runAllPath = Join-Path $repoRoot $runAllRelativePath

$mediaExtensions = @('.gif', '.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mov', '.avi', '.mkv')
$scratchOnlyExtensions = @('.vtt', '.srt', '.ass')
$repoLocalCacheRoots = @(
  'tmp',
  '.cache',
  'downloads',
  'assets/raw',
  '.external-cache',
  '.external-assets',
  '.local-media',
  '.video-cache',
  '.frame-atlas-cache'
)
$forbiddenBinarySurfaces = @(
  '.dist',
  'skills/sf6-agent',
  'skills/sf6-agent/assets/frame-current',
  'runtime/normalization',
  'skills/sf6-agent/assets/normalization',
  'data/raw',
  'data/normalized',
  'data/exports',
  'tests/fixtures',
  'knowledge',
  'docs/testing/smoke-runs'
) + $repoLocalCacheRoots
$suspiciousDirectoryNames = @(
  'frames',
  'frame-dump',
  'frame_dump',
  'frame-dumps',
  'frame_dumps',
  'contact-sheet',
  'contact_sheet',
  'contact-sheets',
  'contact_sheets',
  'screenshots',
  'image-dump',
  'image_dump',
  'video-cache',
  'frame-atlas-cache'
)

function ConvertTo-RepoRelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $fullPath = (Resolve-Path -LiteralPath $Path).Path
  $rootPrefix = $repoRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
  $rootPrefix = $rootPrefix + [System.IO.Path]::DirectorySeparatorChar
  if ($fullPath.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    return ($fullPath.Substring($rootPrefix.Length) -replace '\\', '/')
  }

  return ($fullPath -replace '\\', '/')
}

function Test-RelativePathUnder {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string]$Prefix
  )

  $normalizedPath = ($RelativePath -replace '\\', '/').TrimStart('./').TrimEnd('/')
  $normalizedPrefix = ($Prefix -replace '\\', '/').TrimStart('./').TrimEnd('/')
  return $normalizedPath -eq $normalizedPrefix -or $normalizedPath.StartsWith("$normalizedPrefix/", [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-RelativePathUnderAny {
  param(
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][string[]]$Prefixes
  )

  foreach ($prefix in $Prefixes) {
    if (Test-RelativePathUnder $RelativePath $prefix) {
      return $true
    }
  }
  return $false
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

function Assert-NoActiveAcquisitionClaims {
  param(
    [Parameter(Mandatory = $true)][string]$Content,
    [Parameter(Mandatory = $true)][string]$RelativePath,
    [Parameter(Mandatory = $true)][ref]$Issues
  )

  $activeVerbPattern = '\b(adds?|added|creates?|created|implements?|implemented|enables?|enabled|approves?|approved|authorizes?|authorized|permits?|permitted)\b'
  $objectPattern = '\b(scraper|downloader|download|scrape|cache sync|local cache sync|binary storage|git lfs|move recognition|public `?sf6-agent`? runtime lookup|runtime lookup|external numeric frame-data ingestion|official_raw override)\b'
  $safeLanguagePattern = '\b(no|not|does not|do not|must not|cannot|never|forbidden|exclude|excluded|without|later|future|deferred|not implemented|not approved|does not authorize|not authorize|repo-external by default|only if later|if a later|requires later|after #[0-9]+|blocked)\b'

  foreach ($line in ($Content -split "`r?`n")) {
    $lower = $line.ToLowerInvariant()
    if ($lower -match $activeVerbPattern -and $lower -match $objectPattern -and $lower -notmatch $safeLanguagePattern) {
      $Issues.Value += "$RelativePath appears to actively implement or approve forbidden media/cache behavior: $line"
    }
    if ($lower -match '\bexternal (visual|frame-atlas|atlas).*\b(current-fact authority|override `?official_raw`?|numeric frame-data ingestion)\b' -and $lower -notmatch '\b(not|no|do not|does not|must not|cannot|never|forbidden|unable to|do not override)\b') {
      $Issues.Value += "$RelativePath appears to grant authority to external visual atlas assets: $line"
    }
  }
}

$issues = @()

Assert-FileExists $policyPath $policyRelativePath ([ref]$issues)
Assert-FileExists $runAllPath $runAllRelativePath ([ref]$issues)

if ($issues.Count -eq 0) {
  $policyRaw = Get-Content -LiteralPath $policyPath -Raw -Encoding UTF8
  $runAllRaw = Get-Content -LiteralPath $runAllPath -Raw -Encoding UTF8

  Assert-Contains $runAllRaw 'tests/validation/validate-no-video-binary-assets.ps1' $runAllRelativePath ([ref]$issues)

  foreach ($requiredText in @(
    'repo-external scratch/cache root',
    'external frame-atlas cache sync',
    'later explicit issue only',
    'repo-external by default',
    'disabled from CI',
    'public `sf6-agent` behavior',
    'does not authorize #140 to scrape, download, cache, or sync',
    'External frame-atlas local cache sync smoke',
    'External frame-atlas video usability smoke',
    '`official_raw` remains the current-fact authority',
    'not numeric frame-data ingestion sources',
    'Forbidden Repo Locations',
    'tests/fixtures/` unless metadata-only'
  )) {
    Assert-Contains $policyRaw $requiredText $policyRelativePath ([ref]$issues)
  }

  Assert-NoActiveAcquisitionClaims $policyRaw $policyRelativePath ([ref]$issues)

  $textFilesToInspect = @(
    $policyRelativePath,
    'data/external-frame-atlas/evaluation/README.md',
    'data/external-frame-atlas/evaluation/source-evaluation-matrix.json',
    'contracts/external-frame-atlas-source.schema.json',
    'docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md'
  )

  $fixtureRoot = Join-Path $repoRoot 'tests/fixtures/external-frame-atlas'
  if (Test-Path -LiteralPath $fixtureRoot -PathType Container) {
    $textFilesToInspect += @(
      Get-ChildItem -LiteralPath $fixtureRoot -Filter '*.json' -File |
        ForEach-Object { ConvertTo-RepoRelativePath $_.FullName }
    )
  }

  foreach ($relativePath in $textFilesToInspect) {
    $path = Join-Path $repoRoot $relativePath
    if (Test-Path -LiteralPath $path -PathType Leaf) {
      $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
      Assert-NoActiveAcquisitionClaims $raw $relativePath ([ref]$issues)
    }
  }

  $allItems = Get-ChildItem -LiteralPath $repoRoot -Force -Recurse -ErrorAction SilentlyContinue
  foreach ($item in $allItems) {
    $relativePath = ConvertTo-RepoRelativePath $item.FullName

    if (Test-RelativePathUnder $relativePath '.git') {
      continue
    }

    if ($item.PSIsContainer) {
      $directoryName = $item.Name.ToLowerInvariant()
      if ($suspiciousDirectoryNames -contains $directoryName) {
        $issues += "Forbidden media/cache directory found: $relativePath"
      }
      if ($repoLocalCacheRoots | Where-Object { Test-RelativePathUnder $relativePath $_ }) {
        $issues += "Repo-local media/cache directory found: $relativePath"
      }
      continue
    }

    $extension = [System.IO.Path]::GetExtension($item.Name).ToLowerInvariant()
    $underForbiddenSurface = Test-RelativePathUnderAny $relativePath $forbiddenBinarySurfaces
    $underScratchSurface = Test-RelativePathUnderAny $relativePath $repoLocalCacheRoots

    if ($underForbiddenSurface -and $mediaExtensions -contains $extension) {
      $issues += "Forbidden media asset in repo/public/cache surface: $relativePath"
    }

    if ($underScratchSurface -and ($scratchOnlyExtensions -contains $extension)) {
      $issues += "Subtitle/caption file in repo-local media scratch surface: $relativePath"
    }

    if ($underScratchSurface -and $item.Name.ToLowerInvariant().EndsWith('.info.json')) {
      $issues += "yt-dlp metadata JSON in repo-local media scratch surface: $relativePath"
    }

    if ($underForbiddenSurface -and $item.Name -match '(?i)^contact[-_]sheet.*\.(png|jpg|jpeg|webp)$') {
      $issues += "Contact sheet media file in forbidden surface: $relativePath"
    }
    if ($underForbiddenSurface -and $item.Name -match '(?i)^frame[-_][0-9]{4,}\.(png|jpg|jpeg|webp)$') {
      $issues += "Frame dump media file in forbidden surface: $relativePath"
    }
    if ($underForbiddenSurface -and $item.Name -match '(?i)(thumb|thumbnail).*\.(png|jpg|jpeg|webp)$') {
      $issues += "Thumbnail media file in forbidden surface: $relativePath"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'No video binary assets OK'
