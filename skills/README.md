# Public Adapter

`skills/sf6-agent/` is the single public adapter for SF6 Knowledge Agent Kit.

The adapter contains:

- `SKILL.md` for runtime behavior.
- `references/*-policy.md` for hand-written answer policy.
- `references/generated-*` as derived concept payload from `knowledge/curated`.
- `assets/frame-current/` as derived exact current-fact payload from `data/exports` and `data/roster`.

Do not add separate public `kb-*` skills or agent-specific front doors here. Environment-specific wrappers belong under `packs/`, and human install docs belong under `docs/distribution/agents/`.
