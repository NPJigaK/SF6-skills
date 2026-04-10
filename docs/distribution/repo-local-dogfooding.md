# Repo-Local Dogfooding

`skills/` is the canonical public source.

For repo-local Codex discovery, mirror the public skills into `.agents/skills/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.
The sync refresh removes stale extra directories.
