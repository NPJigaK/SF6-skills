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
  @{ Label = 'source_tier'; Pattern = [regex]::Escape('source_tier') },
  @{ Label = 'legacy answer label metadata'; Pattern = '\u56de\u7b54\u30e9\u30d9\u30eb' },
  @{ Label = 'legacy evidence tier metadata'; Pattern = '\u6839\u62e0\u968e\u5c64' },
  @{ Label = 'core-community-label'; Pattern = [regex]::Escape('core-community-label') },
  @{ Label = 'concept-stable'; Pattern = [regex]::Escape('concept-stable') },
  @{ Label = 'community-labeled'; Pattern = [regex]::Escape('community-labeled') }
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
      if ($content -match $pattern.Pattern) {
        $violations += "$relativePath contains legacy canonical metadata: $($pattern.Label)"
      }
    }
  }
}

if ($violations.Count -gt 0) {
  throw ($violations -join '; ')
}

Write-Host 'Legacy cleanup OK'
