Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$required = @(
  'skills/kb-sf6-core/SKILL.md',
  'skills/kb-sf6-core/references/CORE_QUESTIONS.md',
  'skills/kb-sf6-core/references/KNOWLEDGE.md',
  'skills/kb-sf6-core/references/REVIEW_QUEUE.md',
  'skills/kb-sf6-core/references/SOURCE_POLICY.md'
)

$missing = $required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $repoRoot $_)) }
if (@($missing).Count -gt 0) {
  throw "Missing kb-sf6-core public files: $($missing -join ', ')"
}

$legacyRoot = Join-Path $repoRoot '.agents'
if (Test-Path -LiteralPath $legacyRoot -PathType Container) {
  throw 'Repo-root .agents must not exist'
}

Write-Host 'kb-sf6-core public shell OK'
