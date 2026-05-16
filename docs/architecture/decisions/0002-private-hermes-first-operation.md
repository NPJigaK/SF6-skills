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
public_skill_status: deferred_legacy_distribution_surface
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

deferred_distribution_surfaces:
  - skills/sf6-agent
  - skills/sf6-agent/references/generated-*
  - skills/sf6-agent/assets/frame-current
  - .dist

markers:
  - sf6.operation.private_hermes_first_priority
  - sf6.boundary.public_skill_deferred_legacy_distribution_surface
  - sf6.boundary.public_skill_removal_allowed_after_surface_mapping
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

`skills/sf6-agent/` remains in the repository for now, but it is no longer an
active public product surface. There are no known external public-skill users,
so the repository does not need to preserve it as an external compatibility
contract while private operation is still stabilizing.

The public skill and derived distribution surfaces are deferred legacy
distribution surfaces until a later scoped decision either reactivates,
relocates, or removes them.

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

`skills/sf6-agent/` is deferred. It should not receive new public feature work
while private Hermes-first operation is being stabilized.

Allowed short-term changes are limited to:

- fixes required to keep validators passing
- generated output updates when canonical sources require them
- boundary wording needed to point readers at this decision
- scoped cleanup needed before a later removal or relocation PR

Do not add maintainer workflows, Hermes profile procedures, Codex-Hermes
delegation playbooks, local tool state, or private operating assumptions to
`skills/sf6-agent/`.

Because there are no known external public-skill users, later scoped work may
remove or relocate `skills/sf6-agent/` after mapping its remaining canonical
and derived responsibilities.

## Deferred Distribution Surfaces

The following surfaces are not active design authorities:

- `skills/sf6-agent/`
- `skills/sf6-agent/references/generated-*`
- `skills/sf6-agent/assets/frame-current/`
- `.dist/`
- release-bundle docs and installers

They remain derived or legacy distribution surfaces until later scoped work
decides whether to reactivate, relocate, or remove them.

## Follow-Up Sequence

Recommended follow-ups:

1. Map remaining responsibilities of `skills/sf6-agent/`, generated references,
   frame-current assets, `.dist`, and release/install docs.
2. Decide whether to remove, relocate, or keep each public distribution
   surface.
3. Consolidate maintainer procedures under `workflows/` and keep Hermes packs
   as thin pointers.
4. Run private Hermes-first source/knowledge smoke tasks through reviewed repo
   artifacts.
5. Define reactivation criteria before any future public skill distribution
   work resumes.

## Non-Goals

- This decision does not delete `skills/sf6-agent/`.
- This decision does not move directories.
- This decision does not change current facts, `official_raw`, generated
  references, frame-current assets, normalization assets, or `.dist`.
- This decision does not make Hermes a canonical memory.
- This decision does not make private Hermes local state a repo artifact.
- This decision does not require public users to use Hermes or Codex.
