$required = @(
  'skills/kb-sf6-core/SKILL.md',
  'skills/kb-sf6-core/references/CORE_QUESTIONS.md',
  'skills/kb-sf6-core/references/KNOWLEDGE.md',
  'skills/kb-sf6-core/references/REVIEW_QUEUE.md',
  'skills/kb-sf6-core/references/SOURCE_POLICY.md'
)

$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) {
  throw "Missing kb-sf6-core public files: $($missing -join ', ')"
}

$oldFiles = Get-ChildItem '.agents/skills/kb-sf6-core' -Recurse -File | ForEach-Object { $_.Name } | Sort-Object
$newFiles = Get-ChildItem 'skills/kb-sf6-core' -Recurse -File | ForEach-Object { $_.Name } | Sort-Object

if ((@($oldFiles) -join '|') -ne (@($newFiles) -join '|')) {
  throw 'Public kb-sf6-core file set does not match legacy source'
}

Write-Host 'kb-sf6-core public copy OK'
