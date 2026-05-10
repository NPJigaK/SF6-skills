# Codex-To-Hermes Delegation Workflow

## Purpose

Use this workflow when Codex delegates a bounded knowledge-growth or
maintainer-growth subtask to Hermes.

Codex remains the entrypoint and normal repo implementation executor. Hermes
may act as a repo-local growth workflow delegate when a configured maintainer
profile is available.

Hermes outputs are drafts until converted into reviewed repository artifacts.
Hermes memory, sessions, and local skills are not canonical evidence.
Completion is based on repository artifacts, validators, and review, not
Hermes confidence.

This workflow does not replace `workflows/maintainer-agent-session.md`.
Delegated work must still follow the maintainer session workflow, including
scope restatement, verification, warnings, unresolved items, and handoff.

## Suitable Delegation Tasks

Codex may delegate these bounded draft or review tasks to Hermes when the
target issue allows the work:

- source summary draft
- candidate claims draft
- observation draft
- review note draft
- smoke report draft
- workflow improvement proposal
- validator-pattern proposal
- alias maintenance proposal
- artifact boundary review

Delegation is most useful when Hermes can inspect source material, identify
candidate artifacts, summarize uncertainty, or propose maintainer workflow
improvements without changing canonical surfaces directly.

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

## Delegation Request Template

Use this request shape when handing a subtask to Hermes:

```yaml
task_id:
tracking_issue:
target_issue:
target_scope_summary:
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

## Hermes Response Template

Hermes responses should use this shape:

```yaml
summary:
proposed_artifacts:
source_refs:
evidence_candidate_notes:
uncertainty_or_hold_reasons:
boundary_notes:
follow_up_recommendations:
```

Do not use `evidence_refs` as a response field name. `source_refs` and
`evidence_candidate_notes` are not canonical evidence. They are review inputs
that Codex and the maintainer must evaluate before creating or modifying repo
artifacts.

Hermes response text is not itself canonical evidence. It becomes useful only
when converted into an in-scope repo artifact, validated, reviewed, and merged.

## Post-Delegation Checks Before Commit

Before committing work that used Hermes output:

1. Confirm the proposed artifact destination.
2. Confirm the output remains within the target issue scope.
3. Confirm no current-fact authority is changed unless the target issue
   explicitly allows it.
4. Confirm Hermes memory, session, and local skill state are not committed.
5. Run relevant validators for the changed surfaces.
6. Run `tests/validation/run-all.ps1` when practical.
7. Run `git diff --check`.
8. Verify generated or derived surfaces have no residual diff unless
   intentionally in scope.
9. Record warnings, unresolved items, and intentionally not done items.

If Windows PowerShell reports git-unavailable warnings during generated-surface
checks, follow `workflows/maintainer-agent-session.md` and separately verify
from a git-visible environment that generated references, `.dist`,
frame-current assets, and normalization assets have no residual diff.

## Review Checklist

Before opening a PR, check:

- The delegation request included the target issue and target scope summary.
- The target issue explicitly allows the delegated artifact type.
- The PR body identifies that Hermes output was draft input, if relevant.
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
