---
id: adr-0001
title: Hermes Primary Repo-Local Orchestration
status: accepted
date: 2026-05-09
decision_type: architecture_decision
scope: repo_local_maintainer_orchestration

public_answer_adapter: skills/sf6-agent
hermes_role: primary_repo_local_orchestration_when_configured
hermes_distribution: repo_local_only
hermes_state: non_canonical

canonical_sources:
  - knowledge
  - data/exports
  - data/roster
  - contracts
  - workflows
  - evals

repo_artifact_outputs:
  - knowledge/sources
  - knowledge/evidence/claims
  - knowledge/evidence/video-observations
  - knowledge/review
  - knowledge/curated
  - docs/testing/smoke-runs

fallback_executors:
  - codex
  - human
  - other_agents

markers:
  - sf6.harness.hermes.primary_repo_local_orchestration_when_configured
  - sf6.boundary.hermes_state_non_canonical
  - sf6.boundary.public_adapter_remains_sf6_agent
  - sf6.boundary.repo_artifacts_are_source_of_truth
---

# Hermes Primary Repo-Local Orchestration

## Decision

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available.

Hermes orchestrates repo-local answer, ingest, review, validation, and smoke workflows. It does not replace `skills/sf6-agent/` as the public answer adapter, and it is not a public distribution target.

Reusable knowledge and exact current facts remain canonical only as repo artifacts. Canonical sources include `knowledge/`, `data/exports/`, `data/roster/`, `contracts/`, `workflows/`, and `evals/`.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, and chat transcripts are non-canonical.

Codex, humans, or other agents may still execute the same canonical workflows as fallback executors when Hermes is unavailable or unconfigured.

## Repo Artifact Outputs

Hermes-assisted work must produce reusable output as repository artifacts, such as:

- `knowledge/sources/*`
- `knowledge/evidence/claims/*`
- `knowledge/evidence/video-observations/*`
- `knowledge/review/*`
- `knowledge/curated/*` after review and promotion
- `docs/testing/smoke-runs/*`

`docs/testing/smoke-runs/` is a canonical repo artifact surface for workflow execution evidence. It is not SF6 gameplay knowledge authority.

## Non-Goals

- Hermes is not canonical memory.
- Hermes is not a public answer adapter.
- Hermes does not replace `skills/sf6-agent/`.
- Hermes does not make unreviewed article, image, video, or web claims canonical.
- Hermes wrappers do not replace canonical maintainer procedures under `workflows/*`.

## Consequences

Guidance docs may change prose over time, but validators should check the machine-readable decision fields and markers in this ADR rather than requiring exact natural-language sentences.

Hermes-related implementation should remain repo-local. Public distribution continues to focus on the single `sf6-agent` adapter and its derived runtime payloads.
