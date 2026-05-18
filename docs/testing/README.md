# Testing Docs

The v2 validation suite protects schemas, boundaries, generated markers, distribution contents, and legacy cleanup.

Manual adapter behavior checks:

- `docs/testing/sf6-agent-smoke.md`
- `docs/testing/smoke-runs/`

Run the full local verification sequence with:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

Maintainer validation uses `pwsh` as the supported command. Windows
PowerShell / `powershell.exe` fallback and git visibility warnings are covered
by [docs/architecture/powershell-compatibility-policy.md](../architecture/powershell-compatibility-policy.md).

GitHub Actions uses the same entrypoint in `.github/workflows/v2-validation.yml` for pull requests targeting `main` and pushes to `main`.

`run-all.ps1` supports validation lanes:

| Lane | Command | Purpose |
|---|---|---|
| `read-only` | `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane read-only` | Validate tracked repo artifacts, schemas, fixtures, docs, and boundaries without building generated outputs or `.dist`. |
| `derived-build` | `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane derived-build` | Rebuild generated knowledge refs, frame-current assets, and normalization assets, then validate the derived surfaces. |
| `legacy-distribution` | `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane legacy-distribution` | Build and validate the deferred public distribution bundle under `.dist`. |
| `all` | `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1` | CI-compatible full suite. This is the default when `-Lane` is omitted. |

The `all` lane intentionally builds derived payloads and the deferred distribution bundle before validation. The `derived-build` lane uses the first three commands only, while `legacy-distribution` uses the release-bundle command:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File packages/knowledge-generation/build-sf6-agent-knowledge.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File packages/skill-packaging/build-normalization-runtime-assets.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

After each generation step, the suite fails if tracked derived outputs changed. Regenerated `skills/sf6-agent/references/generated-*`, `runtime/frame-current/`, `skills/sf6-agent/assets/frame-current/`, or normalization runtime files must be reviewed and committed before validation or release packaging is treated as reliable.

Manual validator set:

- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-v2-surfaces.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-v2-contracts.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-schema.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-ingest-artifacts.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-artifacts.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-combo-damage-fixtures.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-evals.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-eval-score-reports.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-roster-source.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-frame-current-assets.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-generated-knowledge.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-current-fact-boundaries.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-distribution.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-doc-links.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-legacy-cleanup.ps1`

Old prose-locking validators were removed. New validators should check contracts and source boundaries, not subjective strategic correctness.
