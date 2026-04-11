# Release Bundle

Phase 1 distributes the public skill library as a GitHub Release artifact named `sf6-skills-bundle.zip`.

## Build

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

## Output

- Local build path: `.dist/sf6-skills-bundle.zip`
- Release asset name: `sf6-skills-bundle.zip`

## Bundle Layout

```text
sf6-skills/
  skills/
    kb-sf6-core/
    kb-sf6-frame-current/
```

## Excluded Content

The release bundle excludes:

- `maintainer-skills/`
- `.agents/`
- `data/`
- `docs/`
- `ingest/`
- `packages/`
- `scripts/`
- `shared/`
- `tests/`
