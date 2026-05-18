# Skills

The former `skills/sf6-agent/` public adapter was removed after runtime payload
relocation. This directory remains only as a placeholder for future reviewed
decisions.

Do not create a public skill, agent-specific front door, or replacement adapter
here without a new architecture decision. Repo-local runtime payloads live under:

- `runtime/generated-knowledge/`
- `runtime/frame-current/`
- `runtime/normalization/`

Historical public adapter disposition is recorded in
`docs/architecture/decisions/0003-retire-public-sf6-agent-adapter.md`. The
generated knowledge responsibility plan is in
`docs/architecture/generated-reference-responsibility-plan.md`.
