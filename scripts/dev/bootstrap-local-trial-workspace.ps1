Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
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

    Remove-Item -LiteralPath $targetPath -Force
}

if ($IsWindows) {
    cmd /c mklink /J "$targetPath" "$sourcePath" | Out-Null
} else {
    New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath | Out-Null
}

Write-Host "Bootstrapped local trial discovery at $targetPath"
