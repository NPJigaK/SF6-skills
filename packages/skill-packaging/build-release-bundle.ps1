Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$skillsRoot = Join-Path $repoRoot 'skills'
$distRoot = Join-Path $repoRoot '.dist'
$stagingRoot = Join-Path $distRoot 'bundle-root'
$stagedRepoRoot = Join-Path $stagingRoot 'sf6-skills'
$bundlePath = Join-Path $distRoot 'sf6-skills-bundle.zip'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
  throw 'Missing skills source: skills/'
}

if (Test-Path -LiteralPath $bundlePath) {
  Remove-Item -LiteralPath $bundlePath -Force
}

if (Test-Path -LiteralPath $stagingRoot) {
  Remove-Item -LiteralPath $stagingRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $distRoot -Force | Out-Null
New-Item -ItemType Directory -Path $stagedRepoRoot -Force | Out-Null

try {
  Copy-Item -LiteralPath $skillsRoot -Destination (Join-Path $stagedRepoRoot 'skills') -Recurse -Force
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

Write-Host 'Release bundle built'
