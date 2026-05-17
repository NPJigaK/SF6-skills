# Hermes Maintainer Profile Policy

## Purpose

This document defines repo-managed expectations for Hermes maintainer profiles.
It is maintainer governance only. It is not SF6 gameplay knowledge, not public
`sf6-agent` behavior, and not local Hermes profile state.

Hermes profiles remain local runtime state. The repo may define expected model,
reasoning, freshness, and boundary rules, but it must not commit exported
profile config, memory, sessions, logs, caches, credentials, raw transcripts,
or command output.

## Managed Expectations

For repo-local maintainer workflows, Hermes profiles should use:

- model expectation: `gpt-5.5`
- accepted model alias: `codex 5.5`
- reasoning expectation: `xhigh`
- accepted reasoning aliases: `extra-high`, `extra_high`

The reasoning expectation is `required_when_supported`. If a Hermes provider
or CLI surface does not expose reasoning effort in a profile listing,
maintainers must verify it manually without committing the observed local
configuration or command output.

`data/toolchain/maintainer-agent-toolchain.json` is the canonical policy data
for these expectations. It records expected maintainer profile shape, not the
state of any maintainer machine.

## Skill Selection Policy

Hermes profiles should use narrow, repo-task-specific skill sets. The Hermes
Skills Hub advertised 689 total skills and 87 built-in skills on 2026-05-17,
so exposing every skill by default creates unnecessary tool temptation and
context noise for SF6 maintainer work.

`data/toolchain/maintainer-agent-toolchain.json` records the repo-managed skill
selection policy for `sf6ingest`, the single repo-local Hermes maintainer
profile. This is policy metadata only: it is not an exported Hermes profile,
not installed skill state, and not proof that any maintainer machine has those
skills enabled or disabled.

The default posture is:

- `sf6ingest` may use repo maintenance, GitHub, planning, debugging, review,
  provider-Codex, and codebase inspection skills by default.
- `sf6ingest` may use external source helpers such as `youtube-content`,
  `ocr-and-documents`, and `blogwatcher` only when the task scope requires
  them and copyright/source-boundary rules are followed.
- Validation and smoke work also use `sf6ingest`; do not create a separate
  smoke profile unless a later reviewed policy reintroduces one.
- For validation-only tasks, avoid conditional source-ingestion, transcript/OCR,
  or monitoring helpers unless the issue explicitly needs them.
- Side-effectful, personal, unrelated creative/media, red-team, smart-home,
  social-media, unrelated finance/health, and unrelated ML training/serving
  skill categories are forbidden unless a later reviewed architecture decision
  creates a narrow exception.

Local skill review commands remain non-canonical review signals only:

```bash
hermes skills list
hermes skills inspect hermes-agent
```

Do not copy local skill list output, enabled/disabled state, local skill paths,
or profile-specific skill configuration into canonical policy data.

## Safe Config Policy

This section defines the repo-managed safe config expectation for the local
`sf6ingest` Hermes profile. It is not an exported profile config and must not
be copied from a maintainer machine.

Recommended:

- `terminal.backend: docker` for untrusted repositories, broad source ingest,
  experimental refactors, or any task that may execute unfamiliar code.
- `approvals.mode: smart` for normal trusted repo-local maintainer work.
- `approvals.mode: manual` for credential-adjacent work, destructive file
  operations, gateway/bot operation, or high-risk external source handling.
- `skills.guard_agent_created: true` to scan agent-created or agent-mutated
  skills before they become reusable local procedure.
- `security.redact_secrets: true` so tool output and logs get a redaction
  safety net before they are displayed or stored.
- `security.tirith_fail_open: false` when Tirith is enabled, so a failed guard
  stops instead of silently allowing the action.
- `security.allow_private_urls: false` unless a task explicitly requires a
  reviewed private/local URL.
- `security.website_blocklist.enabled: true` with private/admin/local domains
  blocked for URL-capable web and browser tools.
- `compression.enabled: true` with `auxiliary.compression` using the main
  model/provider, or another summarizer whose context window is verified to be
  at least as large as the main model.
- `agent.tool_use_enforcement: auto` unless a later profile review shows a
  model-specific reason to change it.
- Empty or minimal `terminal.env_passthrough` and `terminal.docker_forward_env`.
  Forward only the credential needed for the active task, and remove it after
  the task when possible.

Allowed with explicit review:

- `terminal.backend: local` for trusted repo work on a maintainer-owned
  checkout. This is convenient but not a sandbox; commands run with the
  maintainer user's filesystem access.
- `terminal.docker_mount_cwd_to_workspace: true` for deliberate repo editing
  inside Docker, after confirming the mounted path is the intended checkout.
- `terminal.docker_forward_env` entries such as `GITHUB_TOKEN` only when the
  active task requires them. Anything forwarded is visible to commands inside
  the container.
- `skills.external_dirs` only for reviewed maintainer dependency directories
  defined by #231 or a later policy. Do not point it at the whole repo
  `skills/` directory as the default.

Deferred:

- Gateway, messaging bot, cron, Kanban, MCP, external Memory Providers, and
  cloud memory integrations are not enabled by default for `sf6ingest`.
- APM / Agent Skill dependency installation is deferred to #231. Until then,
  do not install broad third-party skill collections as repo-managed profile
  state.

Forbidden:

- `approvals.mode: off` for normal repo work.
- Committing actual `config.yaml`, `.env`, `auth.json`, profile exports,
  memory, sessions, state DB, logs, caches, browser state, cron state, local
  managed skills, or raw transcripts.
- Forwarding broad host environment or credential sets into Docker or cloud
  sandboxes.
- Treating a local safe-config check as proof of canonical repo state.

The official Hermes configuration docs state that the local backend has no
isolation and runs with the user's filesystem access, while Docker provides a
containerized backend. They also document `skills.guard_agent_created`,
`security.redact_secrets`, Tirith, URL blocklists, and compression context
requirements. See:

- https://hermes-agent.nousresearch.com/docs/user-guide/configuration/
- https://hermes-agent.nousresearch.com/docs/user-guide/security

## Profile Distribution Boundary

Profile Distribution may be useful later for sharing the shape of a private
maintainer profile, but it is not active public `sf6-agent` distribution.

May be Git-managed if reviewed and scrubbed:

- `SOUL.md`
- safe `config.yaml` templates with no secrets, tokens, local paths, or
  machine-specific provider state
- reviewed `skills/` or APM-managed skill dependency manifests
- `cron/` templates only if cron operation is later enabled
- `mcp.json` templates only if MCP operation is later enabled
- `distribution.yaml`
- README / setup docs
- `.env.EXAMPLE`

Must remain local user-owned data and must not be committed:

- `memories/`
- `sessions/`
- `state.db`, `state.db-shm`, `state.db-wal`
- `.env`
- `auth.json`
- `logs/`
- `workspace/`
- `plans/`
- `home/`
- `*_cache/`
- `local/`
- raw transcripts, browser state, cron state, profile-specific managed skills,
  local command output, and credentials

Hermes Profile Distribution hard-excludes sensitive user-owned paths such as
`auth.json`, `.env`, `memories/`, `sessions/`, `state.db*`, `logs/`,
`workspace/`, `plans/`, `home/`, `*_cache/`, and `local/`. This repo mirrors
that boundary and treats local memory/session/provider state as non-canonical.
See https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions

## Version Pin And Freshness Review

Hermes CLI version management uses the repo Nix flake as the primary
path. The root `flake.nix` declares the `hermes-agent` input from
`github:NousResearch/hermes-agent`. `flake.lock` is the reviewed pin for the
Hermes Agent input.

Renovate should update the Nix flake input and lockfile through dependency
update PRs. Maintainers review those PRs as Hermes toolchain updates instead of
copying local `hermes --version` output into policy data.

Maintainers with Nix may update and inspect the pin manually:

```bash
nix flake update hermes-agent
nix run .#hermes -- --version
nix flake metadata
```

This environment may not always have Nix installed. If Nix is unavailable,
Hermes may still be checked as a fallback local installation:

```bash
hermes --version
hermes doctor
```

If the fallback installation needs updating, use the Hermes updater only as a
local operator action:

```bash
hermes update
hermes --version
hermes doctor
```

Fallback output is not the canonical version pin. Do not copy the exact
version, commit-behind count, local paths, Python version, SDK version, profile
list output, or logs into canonical policy data.

## Profile Review

Profile checks remain local review signals only:

```bash
hermes profile list
hermes profile show sf6ingest
```

These commands may help confirm local model and reasoning setup, but they do
not produce canonical repo data.

## Boundaries

- Do not require Hermes for public `sf6-agent` users.
- Do not change public adapter behavior from maintainer profile policy.
- Do not commit Hermes profile config, memory, sessions, logs, caches,
  credentials, raw transcripts, cron state, browser state, or local managed
  skills.
- Do not canonize local installed versions, update output, profile-list output,
  Nix command output, or command transcripts.
- CI validators must remain offline and must not call the internet to discover
  latest Hermes versions.
