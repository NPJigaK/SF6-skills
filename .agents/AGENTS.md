# Compatibility Layer

Repo-wide guidance is defined in the root `AGENTS.md`.

`.agents/skills/` is generated compatibility output for repo-local dogfooding.
Do not treat `.agents/skills/` as the canonical source for distributed skills.

Refresh it from `skills/` with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

Some compatibility skills may still remain here until they are migrated into `skills/` or `maintainer-skills/` as appropriate.
