Set-StrictMode -Version Latest
$env:MISE_PWSH_CHPWD_WARNING = '0'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$bundlePath = Join-Path $repoRoot '.dist/sf6-skills-bundle.zip'
$resolverPath = Join-Path $repoRoot 'packages/skill-installers/resolve-install-target.ps1'
$installerPath = Join-Path $repoRoot 'packages/skill-installers/install-sf6-skills.ps1'
$readmePath = Join-Path $repoRoot 'packages/skill-installers/README.md'
$fixtureRoot = Join-Path $repoRoot '.dist/installer-fixtures'

foreach ($requiredPath in @($bundlePath, $resolverPath, $installerPath, $readmePath)) {
  if (-not (Test-Path -LiteralPath $requiredPath)) {
    throw "Missing required path: $requiredPath"
  }
}

if (Test-Path -LiteralPath $fixtureRoot) {
  Remove-Item -LiteralPath $fixtureRoot -Recurse -Force
}

$expectedSuffixes = @{
  codex = '.agents/skills/sf6-skills'
  opencode = '.config/opencode/skills/sf6-skills'
  claude = '.claude/skills/sf6-skills'
  cursor = '.cursor/skills/sf6-skills'
}

foreach ($agent in @('codex', 'opencode', 'claude', 'cursor')) {
  $dryRunJson = & powershell -ExecutionPolicy Bypass -File $installerPath -Agent $agent -DryRun
  $dryRun = $dryRunJson | ConvertFrom-Json
  if ($dryRun.agent -ne $agent) {
    throw "Dry-run agent mismatch for ${agent}: $($dryRun.agent)"
  }

  if (-not $dryRun.source.EndsWith('sf6-skills-bundle.zip')) {
    throw "Dry-run source mismatch for ${agent}: $($dryRun.source)"
  }

  $normalizedTargetPath = $dryRun.target_path.Replace('\', '/')
  if (-not $normalizedTargetPath.EndsWith($expectedSuffixes[$agent])) {
    throw "Dry-run target mismatch for ${agent}: $normalizedTargetPath"
  }

  $agentFixtureRoot = Join-Path $fixtureRoot $agent
  $installOutput = & powershell -ExecutionPolicy Bypass -File $installerPath -Agent $agent -Source $bundlePath -TargetRoot $agentFixtureRoot
  $installedRoot = Join-Path $agentFixtureRoot 'sf6-skills'
  $expectedMessage = "Installed sf6-skills for $agent to $installedRoot (source:"
  if ($installOutput -notmatch [regex]::Escape($expectedMessage)) {
    throw "Install output mismatch for ${agent}: $installOutput"
  }

  if (-not (Test-Path -LiteralPath $installedRoot)) {
    throw "Missing installed target for ${agent}: $installedRoot"
  }

  $installedItem = Get-Item -LiteralPath $installedRoot
  if ($installedItem.LinkType -notin @('Junction', 'SymbolicLink')) {
    throw "Installed target is not a link for ${agent}: $($installedItem.LinkType)"
  }

  $resolvedRoot = (Resolve-Path -LiteralPath $installedRoot).Path
  foreach ($relativePath in @('kb-sf6-core/SKILL.md', 'kb-sf6-frame-current/SKILL.md')) {
    $installedPath = Join-Path $resolvedRoot $relativePath
    if (-not (Test-Path -LiteralPath $installedPath -PathType Leaf)) {
      throw "Missing installed file for ${agent}: $installedPath"
    }
  }
}

Write-Output 'Installer contract OK'
