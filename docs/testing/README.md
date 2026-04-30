# Testing Docs

The v2 validation suite protects schemas, boundaries, generated markers, distribution contents, and legacy cleanup.

Core local verification set:

- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-v2-surfaces.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-v2-contracts.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-schema.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-evals.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-roster-source.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-frame-current-assets.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-generated-knowledge.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-current-fact-boundaries.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-distribution.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-doc-links.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/validation/validate-legacy-cleanup.ps1`

Old prose-locking validators were removed. New validators should check contracts and source boundaries, not subjective strategic correctness.
