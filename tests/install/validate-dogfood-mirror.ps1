$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sourceRoot = Join-Path $repoRoot 'skills/kb-sf6-core'
$targetRoot = Join-Path $repoRoot '.agents/skills/kb-sf6-core'
$syncScript = Join-Path $repoRoot 'scripts/dev/sync-dogfood-skills.ps1'

if (-not (Test-Path $syncScript)) {
  throw 'Missing sync script'
}

if (-not (Test-Path $sourceRoot)) {
  throw 'Missing public source skill'
}

if (-not (Test-Path $targetRoot)) {
  throw 'Missing dogfood mirror target'
}

$sourceHash = Get-FileHash (Join-Path $sourceRoot 'SKILL.md')
$targetHash = Get-FileHash (Join-Path $targetRoot 'SKILL.md')

if ($sourceHash.Hash -ne $targetHash.Hash) {
  throw 'Dogfood mirror is out of sync with public source'
}

Write-Host 'Dogfood mirror OK'
