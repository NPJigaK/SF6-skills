# Codex-Hermes Bridge Policy

## Purpose

This document defines the repo-local Codex-Hermes bridge policy for v2.3.

Codex remains the repo implementation entrypoint for issue-scoped PRs,
validators, contracts, docs, packaging changes, and GitHub workflow
operations.

Hermes is the primary repo-local analyst and growth orchestrator for in-scope
analysis, review, and maintainer-growth tasks when a configured maintainer
profile is available. Hermes output remains draft input until converted into
reviewed repo artifacts.

Codex needs repo-local skill and playbook guidance to use Hermes safely. That
guidance is maintainer-only support. It is not public answer distribution and
it does not change public `sf6-agent` behavior.

## Hermes-First Analysis Loop

When Hermes is configured, available, and the task is in scope for analysis,
review, or growth delegation, Codex must not perform the primary object-level
analysis itself. Codex acts as the maintainer proxy and Hermes operator.

In-scope Hermes-first work includes:

- architecture review drafts
- directory or source-surface audit drafts
- source analysis and source summary drafts
- claim decomposition and observation draft shaping
- review note and review checklist drafting
- workflow improvement proposals
- validator-pattern proposals
- knowledge-growth and maintainer-growth planning
- procedural skill self-improvement review

Codex's role in this loop is:

- scope controller
- Hermes delegation request author
- Hermes operator on behalf of the maintainer
- boundary auditor
- artifact converter
- validator, diff, GitHub, and PR executor
- user handoff surface

Hermes's role is:

- primary analyst
- repo-local orchestrator
- self-improvement reviewer
- provider task planner
- integrator of provider outputs and uncertainty

Hermes may use provider Codex as an executor for file reading, diff drafting,
validator execution, report skeletons, and other bounded implementation tasks.
Provider Codex output remains under Hermes orchestration and must not replace
Hermes as the analysis or decision authority.

Hermes output is non-canonical, but for delegated analysis tasks it is the
primary draft input. Codex must review that draft against repo boundaries and
convert only in-scope, supported material into repo artifacts.

Codex-only analysis for Hermes-first work is fallback behavior. It is allowed
only when Hermes is unavailable or unconfigured, the required Hermes capability
is unavailable or unverified, the target issue explicitly requests Codex-only
analysis, the task contains material that must not be passed to Hermes, or the
task is a narrow implementation/validation step rather than object-level
analysis. The fallback reason must be recorded in the PR body, issue comment,
or review artifact.

## Surface Decision

The preferred future support surface is `packs/codex-hermes-sf6/`.

Codex-Hermes maintainer support must not live under `skills/`. The `skills/`
tree is reserved for public skill distribution surfaces such as
`skills/sf6-agent/`.

`skills/sf6-agent/` remains the public answer adapter. It is end-user facing
and must not absorb repo-local maintainer workflows, local Hermes procedures,
or Codex delegation playbooks.

`packs/codex-hermes-sf6/` is repo-local maintainer support only. It may later
hold a Codex-oriented playbook, guardrails, request templates, and pointers to
reviewed capability references, but it is not canonical SF6 knowledge and is
not a public answer adapter.

## Distinctions

### Codex Skill / Playbook

A Codex skill or playbook teaches Codex repo-specific maintainer procedures.

It may help Codex:

- decide whether Hermes delegation is appropriate
- prepare a bounded Hermes delegation request
- review Hermes output against repo authority boundaries
- preserve issue scope, validators, PR review, and handoff requirements

A Codex skill or playbook does not become canonical evidence. It is procedural
maintainer guidance and must defer to reviewed repo artifacts, validators,
contracts, workflows, and PR review.

### Codex Plugin

A Codex plugin is an external tool or service access path.

A plugin is not needed unless local Hermes CLI access is insufficient. Plugin,
gateway, MCP, or other external integration work requires separate planning
and security review. It is not implemented by this policy.

### Hermes Skill

A Hermes skill is local procedural skill content for Hermes.

Hermes skills are local maintainer workflow aids. They are non-canonical until
distilled into reviewed repository artifacts through issue scope, validators,
PR review, and merge. Raw Hermes skill files, Curator output, memory snapshots,
session logs, and local state must not be committed as promotion artifacts.

### Public `sf6-agent` Skill

The public `sf6-agent` skill is the end-user answer adapter under
`skills/sf6-agent/`.

It must not include repo-local maintainer workflows, Hermes delegation
procedures, Codex playbooks, local tool state, or operational bridge guidance.
End users do not need Codex or Hermes to use the public adapter.

## AGENTS.md Pointer Strategy

Future `AGENTS.md` updates should stay minimal.

`AGENTS.md` should preserve high-level invariants:

- Codex remains the repo implementation entrypoint.
- Hermes-first analysis applies to in-scope analysis, review, and growth tasks
  when configured.
- Codex is the Hermes operator and boundary auditor for those tasks.
- Codex-only analysis for Hermes-first tasks is recorded fallback behavior.
- `skills/sf6-agent/` remains the public answer adapter.
- Hermes local state is non-canonical.
- Repo artifacts and validators remain authoritative.

Once `packs/codex-hermes-sf6/` exists, `AGENTS.md` may link to this policy and
the pack as maintainer support. It should not become a long Hermes CLI manual.

This issue documents the pointer strategy only. It does not update
`AGENTS.md`.

## Command Reference Policy

Codex and Hermes CLI command references must be official-source verified or
left nullable with review notes. Unverified commands must not be encoded as
required repo behavior.

The Hermes CLI capability reference should have one reviewed owner surface.
Future pack resources should point to that reviewed capability surface instead
of duplicating command tables across multiple paths.

CI must not require live Hermes execution. CI must not perform online
latest-version checks. Local Hermes availability can be a maintainer
capability, but it is not a public `sf6-agent` requirement.

## Tool Selection Policy

Codex-Hermes bridge work must not select a tool only because it is built into
Hermes. Hermes-first analysis is about analysis ownership and orchestration,
not about making every Hermes-native tool authoritative.

For article, video, validation, and review workflows, Codex should choose the
method that best fits the target issue, expected evidence quality,
reproducibility, safety boundary, and validator or review path.

Hermes-native tools, external tools, manual review, frame sampling, vision
analysis, video analysis, and repo validators may all be candidates depending
on the task. A Hermes capability such as `video_analyze` should be treated as
an available or planned capability only after official-source verification,
not as the default source of truth.

Tool availability depends on the maintainer environment, provider, model,
credentials, and enabled toolsets. If a capability is unavailable or
unverified, Codex must use a documented fallback such as manual review, frame
sampling, vision analysis, or hold, and must record the limitation instead of
treating the missing tool as a blocker or inventing results.

For SF6 video work, tool output remains observation draft input. It must not
become exact current-fact authority, must not override packaged
`official_raw`, and must be converted into reviewed repo artifacts before
promotion.

## Stale Input Policy

Stale PRs, old branches, old observations, and closed legacy issues are not
active implementation input.

Future work may reference old ideas only by recreating them as fresh issues
under current boundaries. Any useful idea from an old branch must be distilled
into a new scoped issue and reviewed repo artifact. The old branch or draft PR
itself remains non-canonical.

PR #71 and PR #83 must not be used as active source material. They were closed
without merge and are reference-only historical debt unless a fresh issue
explicitly re-reviews a narrow idea under current contracts and validators.

## Canonical Boundary

Hermes output is draft input. For Hermes-first delegated analysis, it is the
primary draft input, not a canonical artifact and not a source of truth by
itself.

Hermes memory, sessions, local skills, Curator output, browser state, cron
state, Kanban state, checkpoints, local configs, logs, caches, credentials,
tokens, and secrets are non-canonical.

Repo artifacts, validators, reviewed docs, workflows, contracts, GitHub issue
scope, PR review, and merged repository state remain authoritative for repo
behavior. Exact current facts remain grounded in `data/exports/`,
`data/roster/`, and derived frame-current runtime assets.

Codex-Hermes bridge support must not bypass validators, issue scope, or PR
review. It can improve maintainer procedure only after its procedures are
reviewed and merged into the appropriate repo-local surfaces.

## Non-Goals For This Policy

This policy does not add the `packs/codex-hermes-sf6/` skeleton, Codex skill
files, Hermes CLI capability reference, dry-run delegation fixtures, plugin or
gateway planning, live Hermes execution, runtime config, Hermes operational
prompts, public `sf6-agent` behavior changes, generated outputs,
frame-current assets, normalization assets, historical smoke report rewrites,
or stale PR imports.
