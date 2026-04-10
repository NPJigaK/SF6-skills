# Compatibility Layer

Repo-wide guidance is defined in the root `AGENTS.md`.

`.agents/skills/` is the exact top-level mirror of `skills/` for repo-local dogfooding.
Do not treat `.agents/skills/` as a separate compatibility layer or canonical source.

Refresh it from `skills/` with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

The sync refreshes the mirror from `skills/`.
