# Repo-Local Dogfooding

`skills/` is the canonical public source.

For repo-local Codex discovery, mirror the public skills into `.agents/skills/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

Only distributed skills are mirrored. Maintainer-only skills stay outside `.agents/skills/`.
