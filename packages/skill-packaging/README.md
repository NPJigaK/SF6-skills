# skill-packaging

Shared packaging scripts live here.

Current entrypoints:

- `build-frame-current-runtime-assets.ps1`
- `build-release-bundle.ps1`

`build-release-bundle.ps1` packages only `skills/sf6-agent/**` under the archive root `sf6-agent/` and writes `.dist/sf6-agent-bundle.zip`.
