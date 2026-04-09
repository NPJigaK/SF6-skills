$required = @(
  'maintainer-skills/sync-knowledge/SKILL.md',
  'maintainer-skills/sync-knowledge/references/SYNC_POLICY.md',
  'maintainer-skills/sync-knowledge/templates/ENTRY_TEMPLATE.md',
  'maintainer-skills/sync-knowledge/templates/REVIEW_TEMPLATE.md',
  'docs/authoring/automation-prompts/triage-new-notes.md'
)

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing maintainer assets: $($missing -join ', ')"
}

$skillPath = 'maintainer-skills/sync-knowledge/SKILL.md'
$canonicalReferences = @(
  '../../skills/kb-sf6-core/references/SOURCE_POLICY.md',
  '../../skills/kb-sf6-core/references/KNOWLEDGE.md',
  '../../skills/kb-sf6-core/references/REVIEW_QUEUE.md'
)

$skillContents = Get-Content $skillPath -Raw
$missingReferences = $canonicalReferences | Where-Object { $skillContents -notmatch [regex]::Escape($_) }
if ($missingReferences.Count -gt 0) {
  throw "Missing canonical references in ${skillPath}: $($missingReferences -join ', ')"
}

if (Test-Path '.agents/skills/sync-knowledge') {
  throw 'Legacy maintainer skill still present in .agents/skills'
}

if (Test-Path '.agents/automation-prompts/triage-new-notes.md') {
  throw 'Legacy automation prompt still present under .agents'
}

Write-Host 'Maintainer surface OK'
