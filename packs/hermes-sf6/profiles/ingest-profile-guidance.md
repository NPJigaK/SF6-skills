# Ingest Profile Guidance

This file is repo-local orchestration support for future Hermes ingest profile guidance.

It is not public answer behavior and does not replace skills/sf6-agent. Public SF6 answer behavior remains in the single `skills/sf6-agent/` adapter.

Hermes ingest guidance must follow canonical workflows and canonical contracts, including the relevant article, video, and source review workflows under `workflows/`.

Reusable output must be committed as repo artifacts, not stored in Hermes state. Source metadata, claims, observations, review notes, and smoke evidence belong in their canonical repository surfaces.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

This is markdown guidance only, not executable profile config. Operational prompt bodies belong to later work after answer contracts and evidence gate policy.

## Model And Reasoning Expectation

The `sf6ingest` profile should follow the repo maintainer profile policy in
`data/toolchain/maintainer-agent-toolchain.json`.

Expected setup:

- model: `gpt-5.5`
- accepted model alias: `codex 5.5`
- reasoning effort: `xhigh` / extra-high where supported

If Hermes does not expose reasoning effort in `hermes profile list`, verify the
setting manually outside the repo. Do not commit Hermes profile config, profile
state, command output, memory, sessions, logs, caches, credentials, or raw
transcripts.

## Skill Selection Expectation

The `sf6ingest` profile should use the repo-managed skill selection policy in
`data/toolchain/maintainer-agent-toolchain.json`.

Default built-in skills should stay focused on Hermes orchestration,
provider-Codex execution, codebase inspection, GitHub issue/PR work, planning,
debugging, test-driven changes, review preparation, spikes, and subagent-driven
development.

External source helpers such as `youtube-content`, `ocr-and-documents`, and
`blogwatcher` are conditional. Use them only when the target issue explicitly
needs source extraction or monitoring, and do not commit full copyrighted
transcripts, OCR dumps, Hermes skill output, or local skill state.
