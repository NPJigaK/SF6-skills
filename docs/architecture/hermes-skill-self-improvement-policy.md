# Hermes Skill Self-Improvement Policy

## Purpose

Hermes may learn local procedural repo-maintenance skills when a configured
maintainer profile is available.

Hermes local skill learning is for improving maintainer workflows. It is not
for storing canonical SF6 knowledge, exact current facts, or final evidence.
Hermes self-improvement output is non-canonical until promoted through
reviewed repository artifacts.

Curator may manage local agent-created procedural skills, but it must not
mutate canonical repo surfaces directly.

## Allowed Local Procedural Skill Learning

Hermes may learn or refine local procedural skills for recurring maintainer
work such as:

- validator pattern learning
- PR review scope guard patterns
- article ingest procedure improvements
- video observation boundary reminders
- alias maintenance patterns
- smoke report drafting patterns
- Codex-to-Hermes delegation request/response patterns
- handoff and reporting pattern improvements

These skills may help future maintainer sessions become more consistent. They
do not become repo behavior unless promoted through the repo review path.

## Forbidden Local Skill Content

Local Hermes skills must not store or present these as authority:

- exact current facts
- frame values
- matchup conclusions
- strategy conclusions as authority
- unreviewed article claims
- unreviewed video observations as final knowledge
- credentials
- secrets
- local config
- local state
- private sessions or logs
- copyrighted source text beyond allowed summaries or references

If a local skill needs an example, use a procedural placeholder or a reviewed
repo artifact reference. Do not embed SF6 current facts or private maintainer
state as reusable skill content.

## Promotion Path

Local procedural learning becomes repo behavior only through this path:

```text
local Hermes skill
-> proposal summary
-> repo artifact draft
-> validator
-> PR
-> review
-> merge
```

A local Hermes skill does not become repo behavior automatically. Promotion
must target an appropriate repo surface, such as:

- `workflows/*`
- `docs/architecture/*`
- `contracts/*`
- `tests/validation/*`
- `packs/hermes-sf6/*`
- `docs/testing/*`

Promotion must not bypass issue scope, validators, or review. If a proposed
improvement crosses issue scope, record it as a follow-up instead of expanding
the current PR.

Do not promote by committing raw local Hermes skill files, local skill
directories, Curator archives, memory snapshots, session logs, or local state
into the repo. Promotion means distilling the reusable procedure into an
in-scope reviewed repo artifact.

## Curator Boundaries

Curator may prune, patch, consolidate, or archive local agent-created
procedural skills.

Hand-authored or relied-upon local skills should be protected, for example by
pinning, before Curator or agent-managed skill updates are allowed to touch
them. Repo promotion still requires distilling any reusable procedure into a
reviewed repository artifact.

Curator output is local procedural maintenance input. It is not canonical SF6
knowledge and is not repo behavior. Curator must not mutate canonical repo
surfaces directly.

Curator output must be converted into reviewed repo artifacts before becoming
canonical. The same promotion path applies: proposal summary, repo artifact
draft, validators, PR, review, and merge.

## Review Checklist

Before promoting any self-improvement output into the repo, check:

- Is the proposed improvement procedural rather than SF6 factual authority?
- Does it avoid exact current facts and unreviewed claims?
- Is the target repo surface appropriate?
- Are validators required and listed?
- Is any local state or secret excluded?
- Is the target issue scope respected?
- Is the proposed improvement distilled into a repo artifact instead of
  committing raw local Hermes skill files, Curator output, memory snapshots,
  session logs, or local state?
- Does the PR make clear that local Hermes skill output was draft input, not
  canonical evidence?
