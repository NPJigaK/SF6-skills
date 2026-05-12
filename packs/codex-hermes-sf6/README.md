# Codex-Hermes SF6 Pack

This pack is repo-local maintainer support only.

It is not public `sf6-agent` distribution, must not live under `skills/`,
and does not define public answer behavior. It teaches Codex how to prepare
and review Hermes delegation for maintainer work. It does not teach end users
how to answer SF6 questions directly.

Hermes output remains draft input until converted into reviewed repo
artifacts through issue scope, validators, PR review, and merge. Repo
artifacts, validators, workflows, contracts, issue scope, and PR review remain
authoritative.

## Contents

- `skill/SKILL.md`: repo-local Codex skill/playbook source.
- `resources/`: request templates, review checklists, and pointer notes.
- `guards/`: boundary notes for local state, current facts, article/video
  inputs, video observations, and external visual assets.

## Required References

This pack points to reviewed repo surfaces instead of duplicating them:

- `workflows/maintainer-agent-session.md`
- `workflows/codex-to-hermes-delegation.md`
- `docs/architecture/codex-hermes-bridge-policy.md`
- `docs/architecture/hermes-cli-capability-reference.md`
- `docs/architecture/sf6-video-analysis-protocol.md`
- `docs/architecture/external-frame-atlas-policy.md`

## Rules

- Keep this pack under `packs/codex-hermes-sf6/`.
- Do not move Codex-Hermes maintainer support under `skills/`.
- Do not modify `skills/sf6-agent/` from this pack.
- Do not add public answer behavior.
- Do not require live Hermes or live video analysis in CI.
- Do not commit Hermes memory, sessions, local skills, Curator output,
  browser state, cron state, Kanban state, checkpoints, local configs, logs,
  caches, credentials, secrets, or tokens.
- Do not treat stale PR #71 or PR #83 as active source material.
- Do not promote exact current facts from Hermes output.
- Do not override packaged `official_raw`.
- Do not copy the Hermes CLI capability table from
  `docs/architecture/hermes-cli-capability-reference.md`.
