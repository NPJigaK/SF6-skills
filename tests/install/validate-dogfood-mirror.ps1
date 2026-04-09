$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$sourceRoot = Join-Path $repoRoot 'skills'
$targetRoot = Join-Path $repoRoot '.agents/skills'
$syncScript = Join-Path $repoRoot 'scripts/dev/sync-dogfood-skills.ps1'

if (-not (Test-Path -LiteralPath $syncScript)) {
  throw "Missing sync script: $syncScript"
}

if (-not (Test-Path -LiteralPath $sourceRoot)) {
  throw "Missing public skills root: $sourceRoot"
}

$publicSkills = Get-ChildItem -LiteralPath $sourceRoot -Directory

if (-not (Test-Path -LiteralPath $targetRoot)) {
  throw "Missing dogfood mirror root: $targetRoot"
}

function Get-RelativeInventoryPath {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RootPath,

    [Parameter(Mandatory = $true)]
    [string]$FullPath
  )

  $relativePath = $FullPath.Substring($RootPath.Length).TrimStart('\', '/')
  return ($relativePath -replace '\\', '/')
}

function Get-SkillInventory {
  param(
    [Parameter(Mandatory = $true)]
    [string]$SkillRoot
  )

  $inventory = Get-ChildItem -LiteralPath $SkillRoot -Recurse -File | ForEach-Object {
    $relativePath = Get-RelativeInventoryPath -RootPath $SkillRoot -FullPath $_.FullName
    $fileHash = (Get-FileHash -LiteralPath $_.FullName).Hash
    "$relativePath`t$fileHash"
  }

  return @($inventory | Sort-Object)
}

foreach ($skill in $publicSkills) {
  $sourceSkillRoot = $skill.FullName
  $targetSkillRoot = Join-Path $targetRoot $skill.Name

  if (-not (Test-Path -LiteralPath $targetSkillRoot)) {
    throw "Missing dogfood mirror target for public skill '$($skill.Name)': $targetSkillRoot"
  }

  $sourceSkillMd = Join-Path $sourceSkillRoot 'SKILL.md'
  $targetSkillMd = Join-Path $targetSkillRoot 'SKILL.md'

  if (-not (Test-Path -LiteralPath $sourceSkillMd)) {
    throw "Missing public skill file for '$($skill.Name)': $sourceSkillMd"
  }

  if (-not (Test-Path -LiteralPath $targetSkillMd)) {
    throw "Missing mirrored skill file for '$($skill.Name)': $targetSkillMd"
  }

  $sourceInventory = Get-SkillInventory -SkillRoot $sourceSkillRoot
  $targetInventory = Get-SkillInventory -SkillRoot $targetSkillRoot

  if ($sourceInventory.Count -ne $targetInventory.Count) {
    throw "Dogfood mirror inventory count mismatch for public skill '$($skill.Name)': source=$($sourceInventory.Count) target=$($targetInventory.Count)"
  }

  for ($i = 0; $i -lt $sourceInventory.Count; $i++) {
    if ($sourceInventory[$i] -ne $targetInventory[$i]) {
      throw "Dogfood mirror inventory mismatch for public skill '$($skill.Name)' at entry $($i + 1): source='$($sourceInventory[$i])' target='$($targetInventory[$i])'"
    }
  }
}

Write-Host 'Dogfood mirror OK'
