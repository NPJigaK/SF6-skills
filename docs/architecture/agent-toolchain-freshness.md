# Agent Toolchain Freshness

## Purpose

This document defines how the SF6 repo tracks maintainer agent toolchain
freshness for v2.2 Hermes Growth Operations.

Toolchain freshness tracking is for maintainer operations only. It records
reviewed expectations, required capabilities, planned capabilities, and review
cadence for local maintainer tools. It does not record local installed
versions or local machine inventory.

## Roles

Codex CLI is the normal repo implementation executor. It is used for
issue-scoped edits, validators, contracts, docs, packaging changes, GitHub
workflow operations, commits, pushes, and draft PR creation.

Hermes CLI is the repo-local growth engine when a configured maintainer profile
is available. Hermes may support knowledge-growth and maintainer-growth work
such as subagent review, local procedural skill operations, session recall,
Curator review, goal/checkpoint handling, and future freshness audits.

End users do not need Codex CLI or Hermes CLI to use `skills/sf6-agent/`.

## Authority Boundary

Toolchain policy is not SF6 gameplay knowledge. It is not exact current-fact
authority. Exact current facts remain grounded in `data/exports/` and
`data/roster/`.

Local tool state is non-canonical. Do not store local installed versions,
local config, local sessions, caches, logs, credentials, tokens, or secrets in
the repo.

The canonical maintainer-toolchain policy data lives under `data/toolchain/`.
That data records reviewed expectations and required/planned capabilities, not
the state of any maintainer machine.

## Freshness Policy

The repo tracks reviewed freshness, not newest-at-any-cost freshness.

Use these concepts:

- `recommended_channel`: the review target, such as `latest_stable`.
- `known_good_version`: a reviewed version when pinned; otherwise `null`.
- `required_capabilities`: capabilities expected for current v2.2 workflows.
- `planned_capabilities`: capabilities expected to matter for later v2.2 work.
- `last_reviewed`: when the policy was last reviewed.
- `freshness_review_cadence`: when maintainers should revisit the tool entry.

Newest versions should be reviewed before being treated as known-good. Version
and update commands should be recorded only when verified from official docs or
release sources. If a command is not verified, leave it nullable and include a
review note.

CI validators must not perform online latest-version checks. Online checks are
manual workflow steps or future reporting tasks only.

## Verification

`tests/validation/validate-agent-toolchain.ps1` verifies the contract, policy
manifest, documentation boundaries, and forbidden local-state paths. It does
not call the internet.

Future Hermes cron may report tool freshness, but it must not auto-update
tools and must not mutate canonical repo surfaces.
