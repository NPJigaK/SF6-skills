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

  $sourceHash = Get-FileHash -LiteralPath $sourceSkillMd
  $targetHash = Get-FileHash -LiteralPath $targetSkillMd

  if ($sourceHash.Hash -ne $targetHash.Hash) {
    throw "Dogfood mirror is out of sync for public skill '$($skill.Name)'"
  }
}

Write-Host 'Dogfood mirror OK'
