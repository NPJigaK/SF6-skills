Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$generatedRoot = Join-Path $repoRoot 'skills/sf6-agent/references'
$curatedRoot = Join-Path $repoRoot 'knowledge/curated'
$generatorPath = Join-Path $repoRoot 'packages/knowledge-generation/build-sf6-agent-knowledge.ps1'

$generatedFiles = @(
  'generated-knowledge-index.md',
  'generated-concepts.md'
)

function ConvertTo-RepoRelativePath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $resolved = (Resolve-Path -LiteralPath $Path).Path
  if (-not $resolved.StartsWith($repoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Path is outside repository root: $Path"
  }

  return $resolved.Substring($repoRoot.Length + 1).Replace('\', '/')
}

function ConvertFrom-ScalarValue {
  param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)

  $trimmed = $Value.Trim()
  if ($trimmed.Length -ge 2 -and $trimmed.StartsWith('"') -and $trimmed.EndsWith('"')) {
    return $trimmed.Substring(1, $trimmed.Length - 2)
  }

  return $trimmed
}

function Read-GeneratedFrontMatter {
  param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

  $relativePath = ConvertTo-RepoRelativePath $File.FullName
  $raw = Get-Content -LiteralPath $File.FullName -Raw -Encoding UTF8
  $normalized = $raw -replace "`r`n", "`n"

  if (-not $normalized.StartsWith("---`n")) {
    throw "$relativePath missing generated YAML front matter"
  }

  $frontMatterEnd = $normalized.IndexOf("`n---`n", 4)
  if ($frontMatterEnd -lt 0) {
    throw "$relativePath generated YAML front matter is not closed"
  }

  $frontMatter = $normalized.Substring(4, $frontMatterEnd - 4)
  $metadata = [ordered]@{}
  $currentKey = $null

  foreach ($line in ($frontMatter -split "`n")) {
    if ($line -match '^([A-Za-z0-9_]+):\s*(.*)$') {
      $currentKey = $Matches[1]
      $metadata[$currentKey] = ConvertFrom-ScalarValue $Matches[2]
      continue
    }

    if ($null -ne $currentKey -and $line -match '^\s+-\s+(.+)$') {
      if (-not ($metadata[$currentKey] -is [System.Collections.IList])) {
        $previous = $metadata[$currentKey]
        $metadata[$currentKey] = @()
        if ($null -ne $previous -and "$previous".Trim().Length -gt 0) {
          $metadata[$currentKey] += $previous
        }
      }
      $metadata[$currentKey] += ConvertFrom-ScalarValue $Matches[1]
    }
  }

  return $metadata
}

if (-not (Test-Path -LiteralPath $generatorPath -PathType Leaf)) {
  throw 'Missing generated knowledge generator'
}

$expectedSourcePaths = @(
  Get-ChildItem -LiteralPath $curatedRoot -Recurse -File -Filter '*.md' |
    Where-Object { $_.Name -ne 'README.md' } |
    Sort-Object FullName |
    ForEach-Object { ConvertTo-RepoRelativePath $_.FullName }
)

if ($expectedSourcePaths.Count -eq 0) {
  throw 'No curated knowledge source paths found'
}

foreach ($name in $generatedFiles) {
  $path = Join-Path $generatedRoot $name
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing generated knowledge file: skills/sf6-agent/references/$name"
  }

  $metadata = Read-GeneratedFrontMatter (Get-Item -LiteralPath $path)
  if ($metadata.generated -ne 'true') {
    throw "$name generated front matter must set generated: true"
  }
  if ($metadata.generator -ne 'packages/knowledge-generation/build-sf6-agent-knowledge.ps1') {
    throw "$name generated front matter has unexpected generator"
  }
  if ($metadata.target_path -ne "skills/sf6-agent/references/$name") {
    throw "$name generated front matter has unexpected target_path"
  }
  $actualSourcePaths = @($metadata.source_paths)
  if (Compare-Object ($expectedSourcePaths | Sort-Object) ($actualSourcePaths | Sort-Object)) {
    throw "$name generated front matter source_paths do not match knowledge/curated"
  }

  $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  foreach ($needle in @(
    'GENERATED FILE - DO NOT EDIT',
    'generator: packages/knowledge-generation/build-sf6-agent-knowledge.ps1',
    'source_root: knowledge/curated'
  )) {
    if ($content -notmatch [regex]::Escape($needle)) {
      throw "$name missing generated marker: $needle"
    }
  }
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
try {
  & $generatorPath -OutputRoot $tempRoot | Out-Null
  foreach ($name in $generatedFiles) {
    $expectedPath = Join-Path $tempRoot $name
    $actualPath = Join-Path $generatedRoot $name
    if (-not (Test-Path -LiteralPath $expectedPath -PathType Leaf)) {
      throw "Generator did not produce expected temp file: $name"
    }
    $expected = [System.IO.File]::ReadAllText($expectedPath)
    $actual = [System.IO.File]::ReadAllText($actualPath)
    if ($expected -ne $actual) {
      throw "$name is stale; rerun packages/knowledge-generation/build-sf6-agent-knowledge.ps1"
    }
  }
}
finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}

Write-Host 'Generated knowledge OK'
