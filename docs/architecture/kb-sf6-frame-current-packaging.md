# kb-sf6-frame-current Packaging Boundary

## Current Runtime Inputs
- `snapshot_manifest.json`
- published `official_raw.*`
- published `derived_metrics.*`
- published `supercombo_enrichment.*`
- supported characters: `jp`, `luke`

## Packaging Options
1. Bundle skill-local published snapshots under `skills/kb-sf6-frame-current/assets/`
2. Generate a reduced runtime asset set during packaging
3. Keep the skill repo-local only until asset packaging is solved

## Recommended Decision
For phase 1, do not migrate this skill into the public surface until a generated runtime asset subset is defined.

The follow-up plan should compare bundled full exports versus generated reduced assets and choose one explicit packaging contract.

## Next Plan Trigger
Write the follow-up plan only after the runtime asset contract is explicit enough to answer:
- which files ship with the skill
- how those files are regenerated
- how published exports remain the final source of truth
