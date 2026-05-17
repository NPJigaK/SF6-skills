# Hermes Local State Boundary

This guard is a repo-local reminder only. Canonical authority remains in
`AGENTS.md`, `workflows/`, `docs/architecture/`, `contracts/`,
`tests/validation/`, and reviewed repo artifacts.

Do not commit Hermes or Codex local state.

Forbidden repo content includes:

- Hermes memory
- sessions
- local skills
- Curator archives or output
- browser state
- cron state
- Kanban state
- checkpoints
- local configs
- logs
- caches
- credentials
- secrets
- tokens

If local state produces a useful idea, recreate the idea as an in-scope repo
artifact through GitHub issue scope, validators, PR review, and merge.
