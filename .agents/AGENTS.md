# Compatibility Layer

Repo-wide guidance is defined in the root `AGENTS.md`.

`skills/` is the canonical public source.
`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.
The sync refresh removes stale extra directories.

Refresh it from `skills/` with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

The sync refreshes the mirror from `skills/`.
