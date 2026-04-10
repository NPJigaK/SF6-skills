$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sourceRoot = Join-Path $repoRoot 'skills'
$targetRoot = Join-Path $repoRoot '.agents/skills'

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$publicSkills = Get-ChildItem $sourceRoot -Directory
$publicNames = $publicSkills.Name
$staleSkills = Get-ChildItem -LiteralPath $targetRoot -Directory | Where-Object {
  $publicNames -notcontains $_.Name
}

foreach ($skill in $staleSkills) {
  Remove-Item -LiteralPath $skill.FullName -Recurse -Force
}

foreach ($skill in $publicSkills) {
  $destination = Join-Path $targetRoot $skill.Name
  if (Test-Path $destination) {
    Remove-Item -LiteralPath $destination -Recurse -Force
  }
  Copy-Item -LiteralPath $skill.FullName -Destination $destination -Recurse
}

Write-Host "Synced $($publicSkills.Count) public skills to .agents/skills"
