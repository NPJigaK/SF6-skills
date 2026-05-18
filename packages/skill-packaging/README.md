# skill-packaging

Package classification: `active_repo_local`.

Repo-local runtime asset builders live here. deferred distribution surfaces were removed with issue #295; see
`docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md`.

Current entrypoints:

- `build-frame-current-runtime-assets.ps1`: `active_repo_local`
- `build-normalization-runtime-assets.ps1`: `active_repo_local`; writes runtime output to `runtime/normalization/`.
