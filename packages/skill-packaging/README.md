# skill-packaging

Package classification: `shared_infra`.

Shared packaging scripts live here.

`build-release-bundle.ps1` is deferred public distribution tooling. ADR-0004
keeps it only as interim `legacy-distribution` lane coverage until the public
`skills/sf6-agent/` adapter is removed after runtime payload relocation. Policy
reference:
`docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md`.

Current entrypoints:

- `build-frame-current-runtime-assets.ps1`: `active_repo_local`
- `build-normalization-runtime-assets.ps1`: `active_repo_local`
- `build-release-bundle.ps1`: `deferred_distribution`

`build-release-bundle.ps1` packages only `skills/sf6-agent/**` under the archive root `sf6-agent/` and writes `.dist/sf6-agent-bundle.zip`.
