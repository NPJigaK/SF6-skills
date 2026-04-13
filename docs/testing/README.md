# Testing Docs

How to verify layout, packaging, installation, and public-skill boundaries.

`tests/integration/validate-public-skill-boundaries.ps1` checks explicit cross-skill path references in public `SKILL.md` files.

Core local verification set:

- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-video-analysis-core-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`

Maintainer smoke workflows:

- Real-video smoke stays outside the core local verification set because it depends on maintainer-provided local fixtures and generated outputs.
- For `video-analysis-core`, use `pwsh -File scripts/dev/run-video-analysis-smoke.ps1 -CaseId combo-short -InputVideoPath local/smoke-inputs/video-analysis/combo-short.mp4 -OutputDir local/smoke-out/video-analysis/combo-short -WhatIf` to stage a case without writing outputs.
- Save canonical JSON under the chosen output directory, then re-run the same script without `-WhatIf` or with `-AnalysisJsonPath <path>` to validate schema and case invariants.
