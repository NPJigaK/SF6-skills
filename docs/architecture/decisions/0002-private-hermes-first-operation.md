---
id: adr-0002
title: Private Hermes-First Operation Before Public Skill Distribution
status: accepted
date: 2026-05-17
decision_type: architecture_decision
scope: private_hermes_first_operation

primary_operation_loop: windows_codex_app_to_hermes_to_repo_artifacts
codex_role: hermes_operator_boundary_auditor_artifact_pr_executor
hermes_role: primary_private_analyst_and_repo_local_orchestrator
public_skill_status: removed_after_runtime_relocation
public_skill_external_users: none_known
public_skill_removal_path: allowed_after_scoped_surface_mapping
hermes_state: non_canonical

canonical_sources:
  - knowledge
  - data/exports
  - data/roster
  - contracts
  - workflows
  - evals

retired_distribution_surfaces:
  - skills/sf6-agent
  - skills/sf6-agent/references/generated-*
  - skills/sf6-agent/assets/frame-current
  - skills/sf6-agent/assets/normalization
  - .dist
  - docs/distribution
  - packages/skill-installers

markers:
  - sf6.operation.private_hermes_first_priority
  - sf6.boundary.public_skill_removed_after_runtime_relocation
  - sf6.boundary.deferred_distribution_surfaces_removed
  - sf6.boundary.hermes_state_non_canonical
  - sf6.boundary.repo_artifacts_are_source_of_truth
---

# Private Hermes-First Operation Before Public Skill Distribution

## Decision

This repository will prioritize private, maintainer-facing Hermes-first
operation before continuing public `sf6-agent` skill distribution work.

The target operating loop is:

```text
maintainer
  -> Windows Codex app
  -> Hermes primary draft analysis / orchestration
  -> Codex boundary audit, artifact conversion, validation, and PR execution
  -> reviewed repo artifacts
```

The former `skills/sf6-agent/` public adapter has been removed after runtime
payload relocation. There were no known external public-skill users, so the
repository did not need to preserve it as an external compatibility contract
while private operation was still stabilizing.

The public skill and derived distribution surfaces were retired by ADR-0003,
ADR-0004, and issue #295. Future public distribution work requires a new scoped
architecture decision.

This decision supersedes ADR-0001 only for public adapter priority and
distribution planning. ADR-0001 remains accepted for the Hermes repo-local
orchestration role, canonical repo artifact boundaries, and non-canonical
Hermes state boundary.

## Rationale

The current repository has too many simultaneously active operating surfaces:

- public `skills/sf6-agent/` adapter behavior
- generated public references
- frame-current runtime assets
- release bundles
- repo-local Hermes packs
- Codex-Hermes bridge guidance
- maintainer workflows
- contracts and validators
- local Hermes profiles, skills, memory, and sessions

Trying to grow a public skill while the private knowledge-management process is
still moving creates duplicated management and bug risk. The more important
near-term goal is to make knowledge collection, review, validation, and
promotion stable as GitHub-reviewable repo artifacts.

## Target Architecture

Windows Codex app is the maintainer-facing operating console. It prepares
Hermes requests, waits for Hermes output, audits boundaries, converts supported
drafts into repo artifacts, runs validators, and opens PRs.

Hermes is the primary analyst and repo-local orchestrator for source analysis,
claim decomposition, observation drafting, architecture review, workflow
learning, and maintainer-growth tasks.

Codex remains the repo implementation and GitHub execution entrypoint. Codex
must not replace Hermes as the primary object-level analyst for in-scope
Hermes-first analysis unless a documented fallback condition applies.

Hermes output is primary draft input only. It becomes reusable only when
converted into reviewed repo artifacts and validated through repo workflows.

## Canonical Boundaries

Canonical repository surfaces remain:

- `knowledge/`
- `data/exports/`
- `data/roster/`
- `contracts/`
- `workflows/`
- `evals/`
- `tests/validation/`
- reviewed architecture docs and ADRs

Hermes memory, sessions, local profiles, local skill state, raw transcripts,
logs, caches, credentials, and local command output are non-canonical and must
not be committed as source of truth.

## Public Skill Status

`skills/sf6-agent/` was removed after reusable runtime payloads moved to
`runtime/generated-knowledge/`, `runtime/frame-current/`, and
`runtime/normalization/`.

Do not recreate the public adapter, add public adapter features, or place
maintainer workflows, Hermes profile procedures, Codex-Hermes delegation
playbooks, local tool state, or private operating assumptions in a replacement
public skill path without a new ADR.

## Deferred Distribution Surfaces

The following surfaces are retired and are not active design authorities:

- `skills/sf6-agent/`
- `skills/sf6-agent/references/generated-*`
- `skills/sf6-agent/assets/frame-current/`
- `skills/sf6-agent/assets/normalization/`
- `.dist/`
- release-bundle docs and installers

They must not be used by private Hermes-first operation.

## Follow-Up Sequence

Recommended follow-ups:

1. Keep runtime payloads under `runtime/generated-knowledge/`,
   `runtime/frame-current/`, and `runtime/normalization/`.
2. Keep maintainer procedures under `workflows/` and keep Hermes packs
   as thin pointers.
3. Run private Hermes-first source/knowledge smoke tasks through reviewed repo
   artifacts.
4. Define reactivation criteria before any future public skill distribution
   work resumes.

## Non-Goals

- This decision does not define a replacement public skill.
- This decision does not change current facts, `official_raw`, generated
  references, frame-current assets, normalization assets, or `.dist`.
- This decision does not make Hermes a canonical memory.
- This decision does not make private Hermes local state a repo artifact.
- This decision does not require public users to use Hermes or Codex.
