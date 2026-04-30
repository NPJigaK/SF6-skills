param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'opencode', 'claude', 'cursor')]
  [string]$Agent,

  [string]$Version = 'latest',

  [string]$Source = $null,

  [string]$TargetRoot = $null,

  [switch]$DryRun = $false
)

Set-StrictMode -Version Latest

$repoOwner = 'NPJigaK'
$repoName = 'SF6-skills'
$libraryName = 'sf6-agent'
$bundleName = 'sf6-agent-bundle.zip'
$resolverPath = Join-Path $PSScriptRoot 'resolve-install-target.ps1'

if (-not (Test-Path -LiteralPath $resolverPath -PathType Leaf)) {
  throw "Missing resolver script: $resolverPath"
}

if (-not $Source) {
  if ($Version -eq 'latest') {
    $Source = "https://github.com/$repoOwner/$repoName/releases/latest/download/$bundleName"
  }
  else {
    $Source = "https://github.com/$repoOwner/$repoName/releases/download/$Version/$bundleName"
  }
}

$resolverArgs = @{
  Agent = $Agent
  LibraryName = $libraryName
}
if ($PSBoundParameters.ContainsKey('TargetRoot')) {
  $resolverArgs.TargetRoot = $TargetRoot
}
$targetPath = & $resolverPath @resolverArgs
if ((Split-Path -Path $targetPath -Leaf) -ne $libraryName) {
  throw "Resolved target leaf must be ${libraryName}: $targetPath"
}

$privateInstallRoot = if ($PSBoundParameters.ContainsKey('TargetRoot')) {
  Join-Path $TargetRoot '_install-root'
}
else {
  Join-Path $HOME '.sf6-agent'
}
$checkoutRoot = Join-Path $privateInstallRoot $Agent

if ($DryRun) {
  [pscustomobject]@{
    agent = $Agent
    source = $Source
    target_path = $targetPath
  } | ConvertTo-Json -Compress
  return
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
$bundlePath = Join-Path $tempRoot $bundleName
$extractRoot = Join-Path $tempRoot 'extract'
$bundledAgentRoot = Join-Path $extractRoot $libraryName

try {
  New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
  if ($Source -match '^(https?)://') {
    Invoke-WebRequest -Uri $Source -OutFile $bundlePath
  }
  else {
    Copy-Item -LiteralPath $Source -Destination $bundlePath -Force
  }

  Expand-Archive -LiteralPath $bundlePath -DestinationPath $extractRoot -Force

  if (-not (Test-Path -LiteralPath $bundledAgentRoot -PathType Container)) {
    throw "Missing bundled agent root: $bundledAgentRoot"
  }

  $skillEntryPath = Join-Path $bundledAgentRoot 'SKILL.md'
  if (-not (Test-Path -LiteralPath $skillEntryPath -PathType Leaf)) {
    throw "Missing bundled skill entrypoint: $skillEntryPath"
  }

  if (Test-Path -LiteralPath $checkoutRoot) {
    Remove-Item -LiteralPath $checkoutRoot -Recurse -Force
  }
  New-Item -ItemType Directory -Path $checkoutRoot -Force | Out-Null

  Get-ChildItem -LiteralPath $bundledAgentRoot -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $checkoutRoot -Recurse -Force
  }

  $targetParent = Split-Path -Path $targetPath -Parent
  New-Item -ItemType Directory -Path $targetParent -Force | Out-Null

  if (Test-Path -LiteralPath $targetPath) {
    Remove-Item -LiteralPath $targetPath -Recurse -Force
  }

  $linkItemType = if ($env:OS -eq 'Windows_NT') { 'Junction' } else { 'SymbolicLink' }
  New-Item -ItemType $linkItemType -Path $targetPath -Target $checkoutRoot | Out-Null
}
finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}

Write-Output "Installed sf6-agent for $Agent to $targetPath (source: $checkoutRoot)"
