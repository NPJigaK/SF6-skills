param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'opencode', 'claude', 'cursor')]
  [string]$Agent,

  [string]$LibraryName = 'sf6-agent',

  [string]$TargetRoot = $null
)

Set-StrictMode -Version Latest

if ($PSBoundParameters.ContainsKey('TargetRoot')) {
  return (Join-Path $TargetRoot $LibraryName)
}

switch ($Agent) {
  'codex' {
    return (Join-Path $HOME ".agents\skills\$LibraryName")
  }
  'opencode' {
    return (Join-Path $HOME ".config\opencode\skills\$LibraryName")
  }
  'claude' {
    return (Join-Path $HOME ".claude\skills\$LibraryName")
  }
  'cursor' {
    return (Join-Path $HOME ".cursor\skills\$LibraryName")
  }
}
