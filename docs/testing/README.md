# Testing Docs

How to verify layout, packaging, installation, and public-skill boundaries.

Core local verification set:

- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`
