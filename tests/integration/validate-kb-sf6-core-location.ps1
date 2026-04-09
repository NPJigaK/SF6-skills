Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$legacyRoot = Join-Path $repoRoot '.agents\skills\kb-sf6-core'
$publicRoot = Join-Path $repoRoot 'skills\kb-sf6-core'

function Get-RelativeFileInventory {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Root
  )

  $resolvedRoot = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar

  Get-ChildItem -LiteralPath $Root -Recurse -File |
    Sort-Object FullName |
    ForEach-Object {
      $relativePath = $_.FullName.Substring($resolvedRoot.Length).Replace('\', '/')
      $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
      [PSCustomObject]@{
        RelativePath = $relativePath
        Hash = $hash
      }
    }
}

$required = @(
  'skills/kb-sf6-core/SKILL.md',
  'skills/kb-sf6-core/references/CORE_QUESTIONS.md',
  'skills/kb-sf6-core/references/KNOWLEDGE.md',
  'skills/kb-sf6-core/references/REVIEW_QUEUE.md',
  'skills/kb-sf6-core/references/SOURCE_POLICY.md'
)

$missing = $required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $repoRoot $_)) }
if (@($missing).Count -gt 0) {
  throw "Missing kb-sf6-core public files: $($missing -join ', ')"
}

$legacyInventory = Get-RelativeFileInventory -Root $legacyRoot
$publicInventory = Get-RelativeFileInventory -Root $publicRoot

if (@($legacyInventory).Count -ne @($publicInventory).Count) {
  throw 'Public kb-sf6-core file count does not match legacy source'
}

$legacyEntries = $legacyInventory | ForEach-Object { "$($_.RelativePath)|$($_.Hash)" }
$publicEntries = $publicInventory | ForEach-Object { "$($_.RelativePath)|$($_.Hash)" }

if ((@($legacyEntries) -join '|') -ne (@($publicEntries) -join '|')) {
  throw 'Public kb-sf6-core file inventory does not match legacy source'
}

Write-Host 'kb-sf6-core public copy OK'
