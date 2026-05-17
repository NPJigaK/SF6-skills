# Agent Toolchain Freshness

## Purpose

This document defines how the SF6 repo tracks maintainer agent toolchain
freshness for Hermes Growth Operations.

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
- `required_capabilities`: capabilities expected for current maintainer workflows.
- `planned_capabilities`: capabilities expected to matter for later maintainer work.
- `last_reviewed`: when the policy was last reviewed.
- `freshness_review_cadence`: when maintainers should revisit the tool entry.
- `version_management`: repo-managed Hermes CLI pin and update policy, with
  the Nix flake/lockfile path as primary and local Hermes commands as fallback.
- `maintainer_profile_policy`: repo-managed expectations for local maintainer
  profiles, such as required model, reasoning effort, profile-check commands,
  and repo-local scope.

Newest versions should be reviewed before being treated as known-good. Version
and update commands should be recorded only when verified from official docs,
release sources, or the tool's own reviewed CLI help. If a command is not
verified, leave it nullable and include a review note.

CI validators must not perform online latest-version checks. Online checks are
manual workflow steps or future reporting tasks only.

Hermes maintainer profile expectations are defined in
`docs/architecture/hermes-maintainer-profile-policy.md`. These expectations are
policy only. They do not commit local Hermes profile config or prove that a
local profile currently matches the policy.

Hermes CLI freshness is managed through the root `flake.nix` and the reviewed
`flake.lock` pin. Renovate Nix flake PRs are the normal update signal. Local
`hermes --version` and `hermes update` output is fallback operator evidence
only.

## Freshness Continuation

The v2.6 freshness loop continues through reviewed policy and reviewed pins:

- `flake.nix` declares the Hermes Agent input.
- `flake.lock` records the reviewed pin.
- Renovate Nix flake PRs are the normal update surface.
- `nix run .#hermes -- --version` is the preferred local inspection command
  because it uses the reviewed flake input.
- fallback local `hermes --version`, `hermes doctor`, and `hermes update`
  output remains operator diagnostic output only.

Do not promote local Hermes CLI output to canonical data. In particular, do not
commit exact local installed versions, commit-behind counts, local paths,
doctor transcripts, provider diagnostics, Python/OpenAI SDK versions, update
output, logs, caches, credentials, auth output, or command transcripts.

## Model And Reasoning Expectations

`gpt-5.5` / `codex 5.5` and `xhigh` / extra-high reasoning are maintainer
profile policy expectations recorded in `data/toolchain/maintainer-agent-toolchain.json`.
They are not copied local profile output, not local proof, and are not proof
that any maintainer machine currently matches the policy.

If a local Hermes CLI or provider surface does not expose reasoning effort in a
profile listing, treat the missing display as a local manual-review gap. Do not
paste the profile listing into repo artifacts. Fix local profile state locally,
or open a reviewed policy PR if the repo expectation itself needs to change.

## Verification

`tests/validation/validate-agent-toolchain.ps1` verifies the contract, policy
manifest, documentation boundaries, and forbidden local-state paths. It does
not call the internet.

Future Hermes cron may report tool freshness, but it must not auto-update
tools and must not mutate canonical repo surfaces.
