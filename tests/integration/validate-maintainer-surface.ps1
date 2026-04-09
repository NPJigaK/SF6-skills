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

if (Test-Path '.agents/skills/sync-knowledge') {
  throw 'Legacy maintainer skill still present in .agents/skills'
}

if (Test-Path '.agents/automation-prompts/triage-new-notes.md') {
  throw 'Legacy automation prompt still present under .agents'
}

Write-Host 'Maintainer surface OK'
