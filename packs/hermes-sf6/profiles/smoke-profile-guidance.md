# Smoke Profile Guidance

This file is repo-local orchestration support for future Hermes smoke profile guidance.

It is not public answer behavior and does not replace skills/sf6-agent. Public SF6 answer behavior remains in the single `skills/sf6-agent/` adapter.

Hermes smoke guidance must follow canonical workflows and canonical contracts, especially validator and smoke-run procedures under `workflows/` and `tests/validation/`.

Reusable output must be committed as repo artifacts, not stored in Hermes state. Smoke reports are workflow execution evidence, not SF6 gameplay knowledge authority.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

This is markdown guidance only, not executable profile config. Operational prompt bodies belong to later work after answer contracts and evidence gate policy.

## Model And Reasoning Expectation

The `sf6smoke` profile should follow the repo maintainer profile policy in
`data/toolchain/maintainer-agent-toolchain.json`.

Expected setup:

- model: `gpt-5.5`
- accepted model alias: `codex 5.5`
- reasoning effort: `xhigh` / extra-high where supported

If Hermes does not expose reasoning effort in `hermes profile list`, verify the
setting manually outside the repo. Do not commit Hermes profile config, profile
state, command output, memory, sessions, logs, caches, credentials, or raw
transcripts.
