Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$docPath = Join-Path $repoRoot 'docs/distribution/release-bundle.md'
if (-not (Test-Path -LiteralPath $docPath -PathType Leaf)) {
  throw 'Missing release bundle doc: docs/distribution/release-bundle.md'
}

$docContent = Get-Content -LiteralPath $docPath -Raw
$requiredDocStrings = @(
  '# Release Bundle',
  'sf6-skills-bundle.zip',
  'powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1',
  '.dist/sf6-skills-bundle.zip',
  'Release asset name: `sf6-skills-bundle.zip`',
  'sf6-skills/',
  '- `maintainer-skills/`',
  '- `.agents/`',
  '- `data/`',
  '- `docs/`',
  '- `ingest/`',
  '- `packages/`',
  '- `scripts/`',
  '- `shared/`',
  '- `tests/`'
)

foreach ($requiredDocString in $requiredDocStrings) {
  if ($docContent -notmatch [regex]::Escape($requiredDocString)) {
    throw "Missing release bundle doc content: $requiredDocString"
  }
}

$buildScriptPath = Join-Path $repoRoot 'packages/skill-packaging/build-release-bundle.ps1'
if (-not (Test-Path -LiteralPath $buildScriptPath -PathType Leaf)) {
  throw 'Missing release bundle build script: packages/skill-packaging/build-release-bundle.ps1'
}

$bundlePath = Join-Path $repoRoot '.dist/sf6-skills-bundle.zip'
if (-not (Test-Path -LiteralPath $bundlePath -PathType Leaf)) {
  throw 'Missing release bundle archive: .dist/sf6-skills-bundle.zip'
}

$requiredEntries = @(
  'sf6-skills/skills/kb-sf6-core/SKILL.md',
  'sf6-skills/skills/kb-sf6-frame-current/SKILL.md'
)

$forbiddenPrefixes = @(
  'sf6-skills/.agents/',
  'sf6-skills/data/',
  'sf6-skills/docs/',
  'sf6-skills/ingest/',
  'sf6-skills/maintainer-skills/',
  'sf6-skills/packages/',
  'sf6-skills/scripts/',
  'sf6-skills/shared/',
  'sf6-skills/tests/'
)

function Test-SafeZipEntryName {
  param(
    [Parameter(Mandatory = $true)]
    [string] $EntryName
  )

  if ([string]::IsNullOrWhiteSpace($EntryName)) {
    return $null
  }

  if ($EntryName.Contains('\') -or $EntryName.Contains(':')) {
    return $null
  }

  if ($EntryName.StartsWith('/') -or $EntryName.StartsWith('\')) {
    return $null
  }

  if ($EntryName -match '(^|/)\.\.(/|$)' -or $EntryName -match '(^|/)\.(/|$)' -or $EntryName -match '//') {
    return $null
  }

  return $EntryName.Replace('\', '/')
}

$archive = [System.IO.Compression.ZipFile]::OpenRead($bundlePath)
try {
  $entries = @(
    $archive.Entries |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_.Name) } |
    ForEach-Object {
      $safeEntry = Test-SafeZipEntryName -EntryName $_.FullName
      if ($null -eq $safeEntry) {
        throw "Unsafe bundle entry name: $($_.FullName)"
      }

      $safeEntry
    }
  )

  $bundleRootPrefix = 'sf6-skills/'
  $skillRootPrefix = 'sf6-skills/skills/'

  foreach ($entry in $entries) {
    if (-not $entry.StartsWith($bundleRootPrefix)) {
      throw "Bundle entry outside sf6-skills root: $entry"
    }

    if (-not $entry.StartsWith($skillRootPrefix)) {
      throw "Bundle entry outside sf6-skills/skills/: $entry"
    }
  }

  foreach ($requiredEntry in $requiredEntries) {
    if ($entries -notcontains $requiredEntry) {
      throw "Missing required bundle entry: $requiredEntry"
    }
  }

  foreach ($forbiddenPrefix in $forbiddenPrefixes) {
    $violations = @($entries | Where-Object { $_.StartsWith($forbiddenPrefix) })
    if ($violations.Count -gt 0) {
      throw "Forbidden bundle entries found under ${forbiddenPrefix}: $($violations -join ', ')"
    }
  }
}
finally {
  $archive.Dispose()
}

Write-Host 'Release bundle OK'
