# Codex-Hermes Plugin And Gateway Plan

## Purpose

This document plans whether Codex needs a plugin, gateway, MCP, or other
remote access path for Hermes delegation in v2.3.

It is planning documentation only.

Local Hermes CLI remains the default path for Hermes growth workflows. Codex
remains the repo implementation entrypoint. Hermes is optional repo-local
growth support for maintainers, and public `sf6-agent` users do not need
Hermes.

If Hermes is unavailable, Hermes growth workflows may be skipped, blocked, or
deferred. This is acceptable for the current maintainer model.

This document does not implement plugin access, gateway access, MCP, cron,
Kanban, remote Hermes access, production config, credentials, network config,
or public `sf6-agent` behavior.

## Current Operating Assumption

The current maintainer setup is single-maintainer.

Maintainer-local Hermes availability is an acceptable prerequisite for
Codex-to-Hermes growth workflows. The repo does not need to guarantee
Hermes-free growth maintenance.

Codex may still implement normal repo work when Hermes is unavailable. Issue
scoping, docs, validators, contracts, packaging, GitHub operations, and public
adapter work remain Codex-first. However, Codex-to-Hermes growth workflows
themselves require Hermes availability. If Hermes is unavailable, those
workflows should be recorded as unavailable, skipped, blocked, or deferred
instead of silently replacing Hermes review with a weaker unscoped substitute.

#129 showed that maintainer-local Hermes bridge smoke is possible with the
merged `packs/codex-hermes-sf6/` pack. That smoke remains non-canonical and
does not make live Hermes execution a CI requirement.

## Distinguish Skill/Playbook Vs Plugin/Gateway

### Codex-Hermes Pack / Playbook

The Codex-Hermes pack lives under `packs/codex-hermes-sf6/`.

It teaches Codex how to prepare and review Hermes delegation. It is repo-local
maintainer support only. It does not connect to external services by itself,
does not store local Hermes state, and does not define public answer behavior.

The pack points to reviewed repo surfaces instead of duplicating canonical
policy or Hermes CLI command tables.

### Local Hermes CLI

Local Hermes CLI is the default maintainer-local execution path.

It may be used only when configured and safe. Hermes output remains draft
input until converted into reviewed repo artifacts through issue scope,
validators, PR review, and merge.

Local Hermes memory, sessions, profiles, skills, Curator output, cron state,
Kanban state, checkpoints, logs, caches, credentials, and secrets remain
non-canonical local state and must not be committed.

### Plugin

A plugin is a Codex-side connector to an external or remote tool or service.

A plugin is not needed while local Hermes CLI is sufficient for the current
single-maintainer workflow. Any future plugin path requires explicit security,
credential, state, audit, and operational planning before implementation.

### Gateway

A gateway is a Hermes server or gateway-style access path.

Gateway access is not needed for the current single-maintainer setup. It would
require authentication, allowlists, network exposure decisions, credential
handling, log and state boundaries, operational ownership, and validators
before implementation.

### MCP

MCP is a tool integration path.

MCP is not enabled by this issue. Future MCP work requires a scoped security
and credential policy, explicit config boundaries, and validators that ensure
repo artifacts, public `sf6-agent` behavior, and local Hermes state remain
separate.

## Decision Matrix

| Option | When To Use | Benefits | Risks | Required Future Safeguards | Current v2.3 Status |
| --- | --- | --- | --- | --- | --- |
| Local CLI only | Current single-maintainer Hermes growth workflows when Hermes is configured locally. | Simple operating path; keeps credentials and state local; aligns with #129 smoke. | Local environment availability can block Hermes-specific workflows. | Keep state out of repo; record unavailable/skipped status; keep live Hermes out of CI. | Default. |
| Codex skill/playbook only | Preparing and reviewing delegation requests without adding new execution access. | Gives Codex safe procedure and review boundaries; no network or credentials. | Does not execute Hermes by itself. | Keep under `packs/`; avoid policy table duplication; validate pack boundaries. | Implemented by #120. |
| Plugin | Only if Codex needs a connector because local CLI access is insufficient. | Could support remote execution from constrained environments. | Credentials, remote trust, logs, state leakage, and unclear operational ownership. | Explicit future issue, credential policy, allowlist, audit/log policy, state boundary, validators. | Deferred. |
| Gateway | Only if shared or remote Hermes access is explicitly approved. | Could support multi-maintainer or remote workflows. | Network exposure, auth failures, token leakage, server state, logs, abuse surface. | Authentication, authorization, allowlist, network exposure review, operational owner, no repo state leakage, validators. | Deferred. |
| MCP | Only if a future scoped integration needs MCP tools. | Standardized tool integration path. | Config and credential leakage, accidental public or CI dependency, unclear authority. | Scoped config policy, secret handling, local-state boundary, no public adapter dependency, validators. | Deferred. |
| Deferred / unavailable | When Hermes is not configured or local CLI access is not available. | Preserves safety and avoids unreviewed substitute workflows. | Hermes-specific growth work may wait. | Record unavailable/skipped/deferred status and map follow-up to a future issue if needed. | Allowed. |

## Hermes Unavailable Policy

Hermes unavailable is not a public user failure.

Hermes unavailable does not block public `sf6-agent` usage. End users do not
need Hermes, and this repo must not make the public answer adapter depend on
Hermes, a plugin, a gateway, MCP, cron, Kanban, or local maintainer state.

Hermes unavailable may block or defer Hermes growth workflows. Do not create a
degraded Hermes-free substitute in this issue. Do not silently replace Hermes
review with weaker unscoped behavior. If a task requires Hermes and Hermes is
unavailable, record the workflow as unavailable, skipped, blocked, or deferred.

Distinguish feature-level unavailability from workflow-level unavailability:

- `video_analyze` unavailable:
  - feature-level fallback or hold is allowed under
    `docs/architecture/sf6-video-analysis-protocol.md`
  - the workflow may still use manual review, frame sampling, vision analysis,
    or hold when the target issue permits those options
- Hermes CLI unavailable:
  - the Codex-to-Hermes workflow itself is unavailable or deferred
  - Codex may continue normal repo work, but it should not pretend Hermes
    delegation happened

## Security And State Boundaries

Future plugin, gateway, MCP, or remote access work must preserve these
boundaries:

- no credentials in the repo
- no gateway tokens in the repo
- no provider keys, profile exports, local configs, or `.env` files in the repo
- no local Hermes sessions, memory, skills, Curator output, checkpoints,
  Kanban state, logs, caches, or browser state in the repo
- no raw Hermes transcripts in repo artifacts by default
- no public network exposure without a future scoped issue and security review
- no production cron, MCP, gateway, or Kanban runtime config in v2.3
- no public `sf6-agent` dependency on Hermes or remote access
- no exact current-fact promotion from remote outputs
- no `official_raw` override by Hermes, web, video, external visual atlas,
  plugin, gateway, MCP, or remote outputs

Remote outputs remain draft input. They become useful only after Codex converts
them into in-scope repo artifacts, runs validators, preserves authority
boundaries, and receives PR review.

## Future Trigger Conditions

Plugin, gateway, or MCP paths may be reconsidered only if one or more of these
conditions are true:

- multiple maintainers need shared Hermes access
- the Codex environment cannot access local Hermes CLI but Hermes delegation
  remains necessary
- local CLI workflow repeatedly blocks accepted maintenance work
- a secure remote execution environment is explicitly approved
- credentials, allowlists, audit behavior, logging, state handling, and
  artifact boundaries are defined
- a future issue scopes implementation, validators, and review requirements

Even when one trigger is present, implementation is not automatic. A future
issue must decide the access path, credentials, state boundary, validator
coverage, and public adapter isolation before any runtime config or connector
is added.

## Relationship To Existing v2.3 Work

This plan depends on the reviewed v2.3 bridge surfaces:

- #116: `docs/architecture/codex-hermes-bridge-policy.md`
- #121: `docs/architecture/hermes-cli-capability-reference.md`
- #123: `docs/architecture/sf6-video-analysis-protocol.md`
- #124: `docs/architecture/external-frame-atlas-policy.md`
- #120: `packs/codex-hermes-sf6/`
- #129: `docs/testing/smoke-runs/hermes-bridge-smoke-gap-report.md`
- #115: `tests/fixtures/codex-hermes-delegation/`

The bridge policy keeps Codex as the repo implementation entrypoint. The
capability reference marks gateway, MCP, cron, and Kanban as deferred. The
video and external atlas policies keep observations and visual references as
draft or review inputs, not current-fact authority. The pack and dry-run
fixtures define how Codex should prepare, review, and validate delegation
without requiring live Hermes in CI.

#129 confirms that a maintainer-local Hermes smoke can work, while also
recording that provider, model, toolset, `video_analyze`, gateway, Kanban, and
browser/web behavior were not validated. This plan keeps those unvalidated
surfaces deferred.

## Recommendation

Keep v2.3 local-CLI-first.

Keep plugin, gateway, and MCP deferred. Treat Hermes-unavailable growth
workflows as unavailable, skipped, blocked, or deferred. Do not implement
remote access until a later milestone or explicit issue defines the security,
credential, network, state, operational, and validator boundaries.

Do not make Hermes, plugin access, gateway access, MCP, cron, or Kanban a
public `sf6-agent` requirement.

## Non-Goals

This document does not add or modify Codex-to-Hermes dry-run fixtures and does
not close the v2.3 tracking issue. It does not implement a plugin, gateway,
MCP, cron, Kanban workflow, remote Hermes access, production config,
credentials, network config, allowlist config, live Hermes execution, live web
research, live video analysis, `video_analyze` testing, external asset
scraping, external asset download or cache creation, GIF/image/video binaries,
public `sf6-agent` behavior changes, frame-current changes, normalization
changes, generated output changes, `.dist` changes, historical smoke report
rewrites, raw transcript storage, sessions, memory, local skills, Curator
output, logs, caches, credentials, or secrets.
