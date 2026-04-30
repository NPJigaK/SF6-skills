param(
  [string]$RepoRoot = (Join-Path $PSScriptRoot '..\..')
)

Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$skillsRoot = Join-Path $repoRoot 'skills'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
  throw "Missing public skills root: $skillsRoot"
}

$skillDirs = @(
  Get-ChildItem -LiteralPath $skillsRoot -Directory |
    Sort-Object Name
)

$skillNames = @($skillDirs | ForEach-Object { $_.Name })

function Assert-SkillManifest {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [Parameter(Mandatory = $true)]
    [string]$SkillRoot
  )

  $skillManifest = Join-Path $SkillRoot 'SKILL.md'
  if (-not (Test-Path -LiteralPath $skillManifest -PathType Leaf)) {
    throw "Public skill missing SKILL.md: skills/$SkillName"
  }

  return $skillManifest
}

function Assert-NoCrossSkillDirectoryDependency {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [Parameter(Mandatory = $true)]
    [string]$SkillManifest,

    [Parameter(Mandatory = $true)]
    [string[]]$AllSkillNames
  )

  $content = (Get-Content -LiteralPath $SkillManifest -Raw) -replace '\\', '/'
  $otherSkillNames = @($AllSkillNames | Where-Object { $_ -ne $SkillName })

  foreach ($otherSkillName in $otherSkillNames) {
    $checks = @(
      @{
        Label = 'public skill directory'
        Needle = "skills/$otherSkillName/"
        Example = "skills/$otherSkillName/"
      }
      @{
        Label = 'repo-local dogfood skill directory'
        Needle = ".agents/skills/$otherSkillName/"
        Example = ".agents/skills/$otherSkillName/"
      }
      @{
        Label = 'sibling skill directory traversal'
        Needle = "../$otherSkillName/"
        Example = "../$otherSkillName/"
      }
    )

    foreach ($check in $checks) {
      $searchStart = 0
      while ($true) {
        $matchIndex = $content.IndexOf($check.Needle, $searchStart, [System.StringComparison]::OrdinalIgnoreCase)
        if ($matchIndex -lt 0) {
          break
        }

        if ($check.Label -eq 'public skill directory') {
          $prefixStart = $matchIndex - 8
          $prefix = if ($prefixStart -ge 0) { $content.Substring($prefixStart, 8) } else { '' }
          if ($prefix -ne '.agents/') {
            throw "Public skill boundary violation: skills/$SkillName/SKILL.md references $($check.Label) $($check.Example)"
          }
        } else {
          throw "Public skill boundary violation: skills/$SkillName/SKILL.md references $($check.Label) $($check.Example)"
        }

        $searchStart = $matchIndex + 1
      }
    }
  }
}

foreach ($skillDir in $skillDirs) {
  $skillManifest = Assert-SkillManifest -SkillName $skillDir.Name -SkillRoot $skillDir.FullName
  Assert-NoCrossSkillDirectoryDependency -SkillName $skillDir.Name -SkillManifest $skillManifest -AllSkillNames $skillNames
}

Write-Host 'Public skill boundaries OK'
