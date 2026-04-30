# Testing Docs

The v2 validation suite protects schemas, boundaries, generated markers, distribution contents, and legacy cleanup.

Run the full local verification sequence with:

```powershell
powershell -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

The sequence intentionally builds derived payloads before validation:

```powershell
powershell -ExecutionPolicy Bypass -File packages/knowledge-generation/build-sf6-agent-knowledge.ps1
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

After each generation step, the suite fails if tracked derived outputs changed. Regenerated `skills/sf6-agent/references/generated-*` or `skills/sf6-agent/assets/frame-current/` files must be reviewed and committed before validation or release packaging is treated as reliable.

Manual validator set:

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
