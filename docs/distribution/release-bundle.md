# Release Bundle

The public distribution bundle is a GitHub Release artifact named `sf6-agent-bundle.zip`.

## Build

```powershell
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-release-bundle.ps1
```

## Output

- Local build path: `.dist/sf6-agent-bundle.zip`
- Release asset name: `sf6-agent-bundle.zip`

## Bundle Layout

```text
sf6-agent/
  SKILL.md
  references/
  assets/
```

## Excluded Content

The release bundle includes only `skills/sf6-agent/**`. It excludes:

- `maintainer-skills/`
- `.agents/`
- `data/`
- `docs/`
- `ingest/`
- `packages/`
- `scripts/`
- `shared/`
- `tests/`
- legacy public skill directories such as `kb-sf6-core/`, `kb-sf6-frame-current/`, and `video-analysis-core/`
