Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$buildScriptPath = Join-Path $repoRoot 'packages/skill-packaging/build-release-bundle.ps1'
if (-not (Test-Path -LiteralPath $buildScriptPath -PathType Leaf)) {
  throw 'Missing release bundle build script: packages/skill-packaging/build-release-bundle.ps1'
}

$docPath = Join-Path $repoRoot 'docs/distribution/release-bundle.md'
if (-not (Test-Path -LiteralPath $docPath -PathType Leaf)) {
  throw 'Missing release bundle doc: docs/distribution/release-bundle.md'
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

$archive = [System.IO.Compression.ZipFile]::OpenRead($bundlePath)
try {
  $entries = @(
    $archive.Entries |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_.Name) } |
    ForEach-Object { $_.FullName.Replace('\', '/') }
  )

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
