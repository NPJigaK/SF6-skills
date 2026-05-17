# Codex-To-Hermes Delegation Workflow

## Purpose

Use this workflow when Codex delegates a bounded knowledge-growth or
maintainer-growth subtask to Hermes.

Codex remains the entrypoint and normal repo implementation executor. For
in-scope analysis, review, and growth tasks, Codex acts as Hermes operator and
boundary auditor rather than primary analyst when a configured maintainer
profile is available.

Hermes is the primary draft analyst and orchestrator for delegated analysis
tasks. Hermes outputs are drafts until converted into reviewed repository
artifacts. Hermes memory, sessions, and local skills are not canonical
evidence. Completion is based on repository artifacts, validators, and review,
not Hermes confidence.

This workflow does not replace `workflows/maintainer-agent-session.md`.
Delegated work must still follow the maintainer session workflow, including
scope restatement, verification, warnings, unresolved items, and handoff.

## Suitable Delegation Tasks

Codex should delegate primary object-level analysis for these bounded draft or
review tasks to Hermes when the target issue allows the work and Hermes is
configured:

- source summary draft
- candidate claims draft
- observation draft
- review note draft
- architecture review draft
- directory or source-surface audit draft
- smoke report draft
- workflow improvement proposal
- validator-pattern proposal
- alias maintenance proposal
- artifact boundary review

Delegation is most useful when Hermes can inspect source material, identify
candidate artifacts, summarize uncertainty, or propose maintainer workflow
improvements without changing canonical surfaces directly.

Codex-only analysis for these tasks is fallback behavior. Record the fallback
reason when Hermes delegation is not attempted or cannot complete.

## Forbidden Delegation Tasks

Do not delegate tasks that would allow Hermes to bypass repo authority or issue
scope:

- direct promotion of current facts
- direct modification of packaged `official_raw`
- direct public `sf6-agent` behavior changes
- direct generated output, frame-current, or runtime asset changes
- storing full copyrighted article, video, or transcript content
- committing Hermes memory, session, or local skill state
- bypassing validators or review
- implementing another issue's scope without explicit approval

Hermes may propose changes to repo artifacts, but Codex must decide whether
those proposals belong in the target issue and must run the required checks
before commit.

## Role Model

Use this loop for Hermes-first analysis:

```text
maintainer
  -> Windows Codex app as human proxy and Hermes operator
  -> Hermes as primary analyst and orchestrator
  -> provider Codex as Hermes-controlled executor when needed
  -> Hermes integrated draft response
  -> Windows Codex app boundary audit, artifact conversion, validation, PR
```

Codex may read repo files to prepare scope, delegation requests, boundary
rules, and validators. Codex must not replace Hermes by producing the primary
object-level analysis when Hermes-first conditions apply.

Provider Codex may do bounded executor work under Hermes direction, such as
file reading, diff drafting, validator execution, report skeleton drafting, or
command-output collection. Provider Codex must not become the final analyst,
promote review-only evidence, override current-fact authority, or expand scope.

## Delegation Request Template

Use this request shape when handing a subtask to Hermes:

```yaml
analysis_mode: hermes_primary
task_id:
tracking_issue:
target_issue:
target_scope_summary:
codex_app_role:
  - hermes_operator
  - boundary_auditor
  - artifact_converter
  - validator_executor
hermes_role:
  - primary_analyst
  - orchestrator
provider_codex_role:
  - executor
source_material:
requested_artifact_type:
allowed_outputs:
forbidden_outputs:
authority_boundaries:
validators_to_run:
review_checklist:
```

`target_issue` is required for issue-scoped work. It identifies the child
issue whose scope, non-goals, acceptance, and dependencies control the
delegation.

`target_scope_summary` should restate the relevant scope, non-goals, and
acceptance before Hermes begins work.

`source_material` is input for analysis. It is not automatically canonical
evidence. The request should identify whether the source material is an
official source, repo artifact, draft, issue comment, PR discussion, article,
video, or other non-canonical input.

`authority_boundaries` must say which repo surfaces may become authoritative
after review and which sources remain non-canonical. For SF6 current facts,
exact authority remains grounded in `data/exports/`, `data/roster/`, and
derived frame-current assets; delegation alone cannot change that authority.

Use this shape when Codex fallback analysis is necessary:

```yaml
analysis_mode: codex_fallback
hermes_delegation:
  attempted: false
  reason:
debt: hermes_first_analysis_not_validated_for_this_workflow
```

## Hermes Response Template

Hermes responses should use this shape:

```yaml
analysis_executor: hermes_primary
summary:
proposed_artifacts:
source_refs:
evidence_candidate_notes:
uncertainty_or_hold_reasons:
boundary_notes:
follow_up_recommendations:
self_improvement_notes:
provider_codex_tasks:
provider_codex_outputs_used:
provider_codex_outputs_rejected:
next_hermes_instruction_suggestions:
```

Do not use `evidence_refs` as a response field name. `source_refs` and
`evidence_candidate_notes` are not canonical evidence. They are review inputs
that Codex and the maintainer must evaluate before creating or modifying repo
artifacts.

Hermes response text is not itself canonical evidence. It becomes useful only
when converted into an in-scope repo artifact, validated, reviewed, and merged.

`provider_codex_outputs_used` and `provider_codex_outputs_rejected` record how
Hermes treated provider work. They do not make provider output canonical.

## Post-Delegation Checks Before Commit

Before committing work that used Hermes output:

1. Confirm the proposed artifact destination.
2. Confirm the output remains within the target issue scope.
3. Confirm no current-fact authority is changed unless the target issue
   explicitly allows it.
4. Confirm Hermes performed primary analysis, or record the Codex fallback
   reason.
5. Confirm provider Codex did not become the final analyst or decision
   authority.
6. Confirm Hermes memory, session, and local skill state are not committed.
7. Run relevant validators for the changed surfaces. For normal Hermes-first
   docs, contracts, workflow, registry, or boundary-only changes, prefer
   `tests/validation/run-all.ps1 -Lane read-only`.
8. Run `tests/validation/run-all.ps1` when practical for merge readiness.
   Use `-Lane derived-build` only when generated references, frame-current
   assets, or normalization assets are intentionally in scope. Use
   `-Lane legacy-distribution` only when deferred public distribution bundle or
   installer surfaces are intentionally in scope.
9. Run `git diff --check`.
10. Verify generated or derived surfaces have no residual diff unless
   intentionally in scope.
11. Record warnings, unresolved items, and intentionally not done items.

If Windows PowerShell reports git-unavailable warnings during generated-surface
checks, follow `workflows/maintainer-agent-session.md` and separately verify
from a git-visible environment that generated references, `.dist`,
frame-current assets, and normalization assets have no residual diff.

## Review Checklist

Before opening a PR, check:

- The delegation request included the target issue and target scope summary.
- The request identifies `analysis_mode` as `hermes_primary` or records
  `codex_fallback` with a reason.
- The target issue explicitly allows the delegated artifact type.
- The PR body identifies that Hermes output was primary draft input, if
  relevant.
- The PR body identifies whether provider Codex was used by Hermes.
- `source_refs` and `evidence_candidate_notes` are not presented as canonical
  evidence.
- Current facts, `official_raw`, and public `sf6-agent` behavior did not
  change unless explicitly in scope.
- Validators and diff checks are reported.
- Any skipped checks have a reason and a narrower check list.
- Follow-up recommendations are either in scope, recorded as not done, or left
  for a later issue.

## Handoff Relationship

Codex-to-Hermes delegation is a sub-step inside a maintainer agent session. It
does not create a separate state system.

Use GitHub issues and PRs as primary progress state. Use PR bodies, issue
comments, smoke reports, and reviewed docs as visible handoff surfaces. Do not
rely on private model memory, Hermes memory, local sessions, local skills,
Curator output, Kanban workers, or checkpoints as repo state.

When a reusable record of a Hermes-first delegation is needed, use
`contracts/hermes-delegation-sanitized-trace.md`. The sanitized trace may
record orchestration and handoff metadata only. It must not include raw Hermes
transcripts, local Hermes state, provider raw output, raw command output,
credentials, binary media, or current-fact authority.
