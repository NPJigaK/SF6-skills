Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$bundlePath = Join-Path $repoRoot '.dist/sf6-agent-bundle.zip'

foreach ($relativePath in @(
  'packages/skill-packaging/build-release-bundle.ps1',
  'packages/skill-installers/install-sf6-agent.ps1',
  'packages/skill-installers/resolve-install-target.ps1',
  'docs/distribution/agents/codex.md',
  'docs/distribution/agents/claude.md',
  'docs/distribution/agents/cursor.md',
  'docs/distribution/agents/opencode.md',
  'docs/distribution/agents/hermes.md',
  'docs/distribution/release-bundle.md'
)) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath))) {
    throw "Missing distribution path: $relativePath"
  }
}

if (-not (Test-Path -LiteralPath $bundlePath -PathType Leaf)) {
  throw 'Missing release bundle: .dist/sf6-agent-bundle.zip'
}

$archive = [System.IO.Compression.ZipFile]::OpenRead($bundlePath)
try {
  $entries = @($archive.Entries | Where-Object { $_.Name } | ForEach-Object { $_.FullName.Replace('\', '/') })
  foreach ($requiredEntry in @(
    'sf6-agent/SKILL.md',
    'sf6-agent/references/answer-policy.md',
    'sf6-agent/references/current-fact-policy.md',
    'sf6-agent/references/generated-knowledge-index.md',
    'sf6-agent/assets/frame-current/runtime_manifest.json',
    'sf6-agent/assets/normalization/runtime_manifest.json',
    'sf6-agent/assets/normalization/aliases.json'
  )) {
    if ($entries -notcontains $requiredEntry) {
      throw "Bundle missing required entry: $requiredEntry"
    }
  }

  foreach ($entry in $entries) {
    if (-not $entry.StartsWith('sf6-agent/')) {
      throw "Bundle entry outside sf6-agent root: $entry"
    }
    if ($entry -match '(^|/)(kb-sf6-core|kb-sf6-frame-current|video-analysis-core)(/|$)') {
      throw "Bundle contains legacy skill entry: $entry"
    }
  }
}
finally {
  $archive.Dispose()
}

Write-Host 'Distribution OK'
