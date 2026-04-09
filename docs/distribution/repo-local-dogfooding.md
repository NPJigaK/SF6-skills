# Repo-Local Dogfooding

`skills/` is the canonical public source.

For repo-local Codex discovery, mirror the public skills into `.agents/skills/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

The sync refreshes mirrored public skills and leaves non-public compatibility skills in place until their own migration tasks run.
