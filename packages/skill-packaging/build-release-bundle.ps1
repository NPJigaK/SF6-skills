Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$agentRoot = Join-Path $repoRoot 'skills\sf6-agent'
$distRoot = Join-Path $repoRoot '.dist'
$stagingRoot = Join-Path $distRoot 'bundle-root'
$bundlePath = Join-Path $distRoot 'sf6-agent-bundle.zip'
$knowledgeGenerator = Join-Path $repoRoot 'packages/knowledge-generation/build-sf6-agent-knowledge.ps1'
$frameAssetBuilder = Join-Path $repoRoot 'packages/skill-packaging/build-frame-current-runtime-assets.ps1'
$generatedValidator = Join-Path $repoRoot 'tests/validation/validate-generated-knowledge.ps1'
$frameAssetValidator = Join-Path $repoRoot 'tests/validation/validate-frame-current-assets.ps1'
$derivedOutputPaths = @(
  'skills/sf6-agent/references/generated-knowledge-index.md',
  'skills/sf6-agent/references/generated-concepts.md',
  'skills/sf6-agent/assets/frame-current'
)

function Assert-NoDerivedOutputStatus {
  param([Parameter(Mandatory = $true)][string]$Context)

  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "WARNING: git is unavailable; skipping derived output status check after $Context"
    return
  }

  $status = @(& git -C $repoRoot status --porcelain -- $derivedOutputPaths)
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to inspect derived output status during $Context"
  }
  if ($status.Count -gt 0) {
    throw "Tracked or untracked derived outputs changed during $Context. Commit regenerated generated-* references and frame-current assets before building a release bundle."
  }
}

if (-not (Test-Path -LiteralPath $agentRoot -PathType Container)) {
  throw 'Missing agent source: skills/sf6-agent'
}

foreach ($requiredScript in @($knowledgeGenerator, $frameAssetBuilder, $generatedValidator, $frameAssetValidator)) {
  if (-not (Test-Path -LiteralPath $requiredScript -PathType Leaf)) {
    throw "Missing release preflight script: $requiredScript"
  }
}

& $knowledgeGenerator
Assert-NoDerivedOutputStatus 'knowledge generation'
& $frameAssetBuilder
Assert-NoDerivedOutputStatus 'frame-current asset generation'
& $generatedValidator
& $frameAssetValidator
Assert-NoDerivedOutputStatus 'release preflight validation'

if (Test-Path -LiteralPath $bundlePath) {
  Remove-Item -LiteralPath $bundlePath -Force
}

if (Test-Path -LiteralPath $stagingRoot) {
  Remove-Item -LiteralPath $stagingRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $distRoot -Force | Out-Null
New-Item -ItemType Directory -Path $stagingRoot -Force | Out-Null

try {
  Copy-Item -LiteralPath $agentRoot -Destination $stagingRoot -Recurse -Force
  $bundleStream = [System.IO.File]::Open($bundlePath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
  try {
    $archive = New-Object System.IO.Compression.ZipArchive($bundleStream, [System.IO.Compression.ZipArchiveMode]::Create, $false)
    try {
      Get-ChildItem -LiteralPath $stagingRoot -Recurse -File | ForEach-Object {
        $relativePath = $_.FullName.Substring($stagingRoot.Length + 1).Replace('\', '/')
        $entry = $archive.CreateEntry($relativePath, [System.IO.Compression.CompressionLevel]::Optimal)
        $entryStream = $entry.Open()
        try {
          $fileStream = [System.IO.File]::OpenRead($_.FullName)
          try {
            $fileStream.CopyTo($entryStream)
          }
          finally {
            $fileStream.Dispose()
          }
        }
        finally {
          $entryStream.Dispose()
        }
      }
    }
    finally {
      $archive.Dispose()
    }
  }
  finally {
    $bundleStream.Dispose()
  }
}
finally {
  if (Test-Path -LiteralPath $stagingRoot) {
    Remove-Item -LiteralPath $stagingRoot -Recurse -Force
  }
}

Write-Host "Release bundle built: $bundlePath"
