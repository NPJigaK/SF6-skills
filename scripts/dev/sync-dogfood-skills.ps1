$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sourceRoot = Join-Path $repoRoot 'skills'
$targetRoot = Join-Path $repoRoot '.agents/skills'

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$publicSkills = Get-ChildItem $sourceRoot -Directory
$publicNames = $publicSkills.Name

foreach ($skill in $publicSkills) {
  $destination = Join-Path $targetRoot $skill.Name
  if (Test-Path $destination) {
    Remove-Item -LiteralPath $destination -Recurse -Force
  }
  Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse
}

Get-ChildItem $targetRoot -Directory |
  Where-Object { $_.Name -notin $publicNames } |
  ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

Write-Host "Synced $($publicSkills.Count) public skills to .agents/skills"
