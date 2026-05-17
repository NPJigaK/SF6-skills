# Hermes Growth Harness Map

## Purpose

This document maps harness engineering concepts to SF6 repo maintainer
operations for v2.2.

External harness engineering material is reference input only. It is not
canonical SF6 repo authority. SF6 repo architecture decisions, contracts,
workflows, validators, and reviewed repository artifacts remain authoritative
for repository behavior and canonical surfaces. GitHub issues and pull
requests are authoritative for task scope, progress state, review, and handoff;
they are not canonical SF6 gameplay knowledge or exact current-fact authority.

v2.2 uses this map to keep Hermes Growth Operations concrete. Hermes is the
repo-local growth engine when a configured maintainer profile is available,
while Codex remains the normal repo implementation executor and
`skills/sf6-agent/` remains the public answer adapter.

## Boundary

The maintainer harness is repo-local. It coordinates implementation,
knowledge-growth, review, validation, and handoff work.

The public answer surface is still `skills/sf6-agent/`. End users do not need
Hermes, Codex, local Hermes memory, local skills, Curator output, Kanban
workers, or checkpoints to use the public adapter.

Hermes-generated drafts, local Hermes skills, session memory, Curator output,
and other local state are not canonical until promoted through reviewed
repository artifacts.

## Harness Subsystem Map

| Harness subsystem | Existing SF6 repo surfaces | Missing or weak surfaces | v2.2 issue mapping | Deferred items and reason |
|---|---|---|---|---|
| Instructions | `AGENTS.md`; `README.md`; `docs/architecture/*`; `docs/architecture/decisions/*`; `workflows/*`; issue bodies with scope and non-goals | A consolidated harness map for v2.2 growth operations | #95 maps current instructions and gaps | Operational Hermes prompt bodies remain deferred until contracts, boundaries, and smoke surfaces are ready |
| State | GitHub issues and milestones; PR bodies; PR comments; roadmap docs; reviewed repository artifacts; smoke reports when created by workflow | Explicit maintainer session state rules; clean handoff template; guidance against always-changing root progress files | #97 defines session lifecycle and handoff | A root `progress.md` or feature-list file is deferred because GitHub issues and PRs are the primary progress state and root churn should be avoided |
| Verification | `tests/validation/run-all.ps1`; focused validators under `tests/validation/`; JSON schemas in `contracts/*`; GitHub Actions; `git diff --check`; scope guard review | Toolchain freshness validator; answer smoke fixture validator; normalization runtime asset validator; planning prerequisites for article/video validators | #96, #100, and #101 add concrete validators; #102 and #103 plan future ingest validators | Online latest-version checks in CI remain deferred because CI should not depend on network freshness checks |
| Scope | Issue scope, non-goals, acceptance, dependencies, labels, and milestone; ADR invariants; contracts; `AGENTS.md` operating lanes | Explicit Codex-to-Hermes request/response boundaries; local skill promotion path; repeated restatement of target issue acceptance before implementation | #98 defines delegation scope; #99 defines skill promotion boundaries; #97 requires target issue scope restatement | Runtime answer behavior changes remain deferred until assets, smoke, and adapter changes are separately reviewed |
| Session lifecycle / handoff | The v2.1 issue-to-PR pattern; PR validation sections; final implementation summaries; clean worktree checks in practice | A canonical workflow for start-of-session checks, during-session state, end-of-session handoff, warnings, unresolved items, and next action | #97 defines `workflows/maintainer-agent-session.md` | Durable Kanban, cron reminders, and checkpoint policy remain deferred until local state and promotion boundaries are documented |

## Gap To Issue Mapping

| Gap | Why it matters | v2.2 issue |
|---|---|---|
| Harness map for Hermes Growth Operations | Prevents v2.2 from becoming a loose collection of Hermes usage ideas | #95 |
| Maintainer toolchain freshness policy | Tracks required/planned Codex and Hermes capabilities without storing local machine state | #96 |
| Session lifecycle and clean handoff | Makes multi-session agent work restartable and reviewable | #97 |
| Codex-to-Hermes delegation request/response shape | Turns Hermes Growth Lane delegation into a structured handoff instead of oral convention | #98 |
| Hermes local skill self-improvement promotion path | Allows procedural learning while preventing automatic canonicalization | #99 |
| Normalization runtime generation and packaging | Converts canonical alias data into derived runtime assets without changing answer behavior | #100 |
| Contract-level answer smoke skeleton | Adds fixture-level smoke coverage before operational prompt execution | #101 |
| Article ingest planning | Separates source metadata, candidate claims, review, copyright, and future wrapper work | #102 |
| Video observation planning | Separates observation-only media artifacts from exact current facts and coaching conclusions | #103 |

## Authority Model

The map keeps three lanes separate:

- Repo implementation lane: Codex implements issue-scoped PRs, validators,
  contracts, docs, packaging changes, and GitHub workflow operations.
- Hermes growth lane: Hermes may assist with source analysis, claim
  decomposition, observation drafting, review drafting, smoke drafting,
  workflow learning, validator-pattern learning, and procedural skill
  self-improvement when configured.
- Public user lane: users consume `skills/sf6-agent/`; Hermes is optional and
  not required for public answering.

Hermes output is draft material until reviewed. It may become a repository
artifact only through the same repo review path as other maintainer work:
issue scope, local edits, validators, PR, review, and merge.

## Verification Principle

Completion is based on verification results, not agent confidence.

For v2.2 work, the relevant verification surface is usually a combination of:

- targeted validators for the changed surface
- `tests/validation/run-all.ps1`
- `git diff --check`
- scope guard review against the issue non-goals
- clean worktree and handoff reporting

When Windows PowerShell cannot see Git during generated-surface checks, the
handoff should report that warning and separately verify from a git-visible
environment that generated references, `.dist`, frame-current assets, and
normalization runtime assets have no residual diff.
See `docs/architecture/powershell-compatibility-policy.md` for the canonical
`pwsh` / Windows PowerShell fallback policy.

## Deferred Harness Surfaces

| Deferred surface | Reason |
|---|---|
| Hermes operational prompt bodies | Contracts, smoke skeletons, and delegation/promotion policy should precede prompt bodies |
| Root progress file or always-changing feature list | GitHub issues and PRs are the primary progress state; root churn should require a later decision |
| Production cron jobs | Cron may report freshness later, but automatic canonical promotion is not allowed |
| MCP and gateway config | External tool bridges and notifications need separate authority and secret-handling policy |
| Automatic Curator-to-repo promotion | Curator may manage local agent-created skills, but repo promotion requires PR review |
| Runtime answer behavior changes for normalization assets | #100 may package assets for future use, but lookup, routing, and answer composition need separate review |
