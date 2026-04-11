param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('codex', 'opencode', 'claude', 'cursor')]
  [string]$Agent,

  [string]$LibraryName = 'sf6-skills',

  [string]$TargetRoot = $null
)

Set-StrictMode -Version Latest

if ($PSBoundParameters.ContainsKey('TargetRoot')) {
  return (Join-Path $TargetRoot $LibraryName)
}

switch ($Agent) {
  'codex' {
    return (Join-Path $HOME '.agents\skills\sf6-skills')
  }
  'opencode' {
    return (Join-Path $HOME '.config\opencode\skills\sf6-skills')
  }
  'claude' {
    return (Join-Path $HOME '.claude\skills\sf6-skills')
  }
  'cursor' {
    return (Join-Path $HOME '.cursor\skills\sf6-skills')
  }
}
