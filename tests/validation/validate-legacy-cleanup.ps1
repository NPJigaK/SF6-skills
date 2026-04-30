Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$legacyPaths = @(
  'skills/kb-sf6-core',
  'skills/kb-sf6-frame-current',
  'skills/video-analysis-core',
  'maintainer-skills',
  'shared',
  'shared/roster',
  'local',
  '.codex',
  '.claude-plugin',
  '.cursor-plugin',
  '.opencode'
)

$violations = @()
foreach ($relativePath in $legacyPaths) {
  if (Test-Path -LiteralPath (Join-Path $repoRoot $relativePath)) {
    $violations += "Legacy path still exists: $relativePath"
  }
}

$canonicalRoots = @(
  'AGENTS.md',
  'README.md',
  'knowledge',
  'contracts',
  'evals',
  'workflows',
  'skills/sf6-agent'
)

$legacyMetadataPatterns = @(
  'source_tier',
  '回答ラベル',
  '根拠階層',
  'core-community-label',
  'concept-stable',
  'community-labeled'
)

foreach ($relativeRoot in $canonicalRoots) {
  $path = Join-Path $repoRoot $relativeRoot
  if (-not (Test-Path -LiteralPath $path)) {
    continue
  }
  $files = if (Test-Path -LiteralPath $path -PathType Leaf) {
    @(Get-Item -LiteralPath $path)
  } else {
    @(Get-ChildItem -LiteralPath $path -Recurse -File)
  }
  foreach ($file in $files) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    foreach ($pattern in $legacyMetadataPatterns) {
      if ($content -match [regex]::Escape($pattern)) {
        $violations += "$relativePath contains legacy canonical metadata: $pattern"
      }
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Legacy cleanup OK'
