# Public Adapter

`skills/sf6-agent/` is the existing public adapter for SF6 Knowledge Agent Kit.
It is currently a deferred legacy distribution surface while private
Hermes-first operation is stabilized.

The adapter contains:

- `SKILL.md` for runtime behavior.
- `references/*-policy.md` for hand-written public adapter behavior policy.
- `references/generated-*` as compatibility copy of generated concept payload from `runtime/generated-knowledge/`.
- `assets/frame-current/` as compatibility copy of exact current-fact payload from `runtime/frame-current/`.

Do not add separate public `kb-*` skills or agent-specific front doors here. Environment-specific wrappers belong under `packs/`, and human install docs belong under `docs/distribution/agents/`.

Generated knowledge references and hand-written adapter policy references are
separate responsibility surfaces. The Phase 2 plan is in
`docs/architecture/generated-reference-responsibility-plan.md`.
