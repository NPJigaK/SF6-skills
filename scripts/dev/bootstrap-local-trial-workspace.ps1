Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
$runningOnWindows = [System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT
$localRoot = Join-Path $repoRoot 'local'
$adapterRoot = Join-Path (Join-Path $localRoot '.agents') 'skills'
$targetPath = Join-Path $adapterRoot 'sf6-skills'
$sourcePath = Join-Path $repoRoot 'skills'

New-Item -ItemType Directory -Path $adapterRoot -Force | Out-Null

if (Test-Path -LiteralPath $targetPath) {
    $targetItem = Get-Item -LiteralPath $targetPath -Force
    if ($targetItem.LinkType -notin @('Junction', 'SymbolicLink')) {
        throw "Refusing to remove existing non-link path: $targetPath"
    }

    $resolvedTargetPath = @($targetItem.Target | ForEach-Object { $_.ToString() }) | Select-Object -First 1
    if (-not $resolvedTargetPath) {
        throw "Unable to resolve existing discovery link target: $targetPath"
    }
    $matchesSource = if ($runningOnWindows) {
        [System.StringComparer]::OrdinalIgnoreCase.Equals($resolvedTargetPath, $sourcePath)
    }
    else {
        $resolvedTargetPath -eq $sourcePath
    }

    if ($matchesSource) {
        Write-Host "Bootstrapped local trial discovery at $targetPath"
        return
    }

    throw "Existing discovery link points elsewhere. Remove it manually and rerun: $targetPath -> $resolvedTargetPath"
}

if ($runningOnWindows) {
    cmd /c mklink /J "$targetPath" "$sourcePath" | Out-Null
} else {
    New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath | Out-Null
}

Write-Host "Bootstrapped local trial discovery at $targetPath"
