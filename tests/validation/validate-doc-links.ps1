Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$markdownFiles = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Include '*.md' |
  Where-Object {
    $relative = $_.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
    $relative -notmatch '^(\.git|\.dist|\.worktrees)/'
  }

$issues = @()
foreach ($file in $markdownFiles) {
  $relativePath = $file.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
  $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
  $matches = [regex]::Matches($content, '\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)')
  foreach ($match in $matches) {
    $target = $match.Groups[1].Value
    if ($target.StartsWith('<') -and $target.EndsWith('>')) {
      $target = $target.Substring(1, $target.Length - 2)
    }
    $target = ($target -split '#')[0]
    if ([string]::IsNullOrWhiteSpace($target)) {
      continue
    }
    $resolved = Join-Path (Split-Path -Parent $file.FullName) $target
    if (-not (Test-Path -LiteralPath $resolved)) {
      $issues += "$relativePath has broken link: $($match.Groups[1].Value)"
    }
  }
}

if ($issues.Count -gt 0) {
  throw ($issues -join '; ')
}

Write-Host 'Doc links OK'
