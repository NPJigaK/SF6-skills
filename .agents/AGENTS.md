# Compatibility Layer

Repo-wide guidance is defined in the root `AGENTS.md`.

`.agents/skills/` is generated compatibility output for repo-local dogfooding.
Do not treat `.agents/skills/` as the canonical source for distributed skills.

Some compatibility skills may still remain here until they are migrated into `skills/` or `maintainer-skills/` as appropriate.

Refresh it from `skills/` with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

The sync refreshes mirrored public skills and leaves non-public compatibility skills in place until their own migration tasks run.
