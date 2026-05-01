# GitHub Management Workflow

This repository uses GitHub CLI (`gh`) as the default interface for reproducible GitHub issue, pull request, review, status, label, milestone, and merge management.

Use the GitHub web UI when it is safer, clearer, or required by GitHub settings. Examples include repository settings, branch protection, GitHub App installation settings, visual PR diff review, and complex Actions UI investigation.

## Goals

- Keep GitHub operations reproducible and traceable.
- Prefer command-line operations that can be logged and repeated.
- Avoid browser-only changes when `gh` can perform the operation safely.
- Keep repo changes, issue updates, PR creation, validation, and merge decisions connected.
- Keep secrets out of commands, docs, issue comments, PR bodies, smoke reports, and logs.

## Tooling

Use `gh` for:

- issue creation, editing, commenting, and closing
- PR creation, editing, draft/ready transitions, status checks, and merges
- CI run and check inspection
- labels and milestones
- issue and PR metadata inspection
- issue closure and PR-to-issue mapping

Use local `git` for:

- branch creation and switching
- staging and committing
- checking local diffs and status
- pushing branches before opening PRs

## Authentication

Check authentication before GitHub operations:

```bash
gh auth status
```

If login is needed:

```bash
gh auth login
```

Do not paste tokens into repo files, issue comments, PR bodies, smoke reports, or logs. If command output includes token-like or secret-like content, redact it before recording it.

## Standard Issue Flow

Create an issue from a prepared body file:

```bash
gh issue create \
  --title "[v2.1] Example issue" \
  --body-file /tmp/issue-body.md \
  --label "type:validation" \
  --label "priority:p1"
```

View an issue:

```bash
gh issue view 24 --comments
```

Edit labels or milestone:

```bash
gh issue edit 24 \
  --add-label "area:knowledge" \
  --milestone "v2.1: CI, evals, and smoke tests"
```

Close an issue:

```bash
gh issue close 24 --comment "Completed by PR #XX."
```

Prefer issue bodies and comments that record the decision, validation, and follow-up state. Keep issue closure tied to PR evidence when possible.

## Standard PR Flow

Start from a clean branch state:

```bash
git status --short --branch
git switch main
git pull --ff-only
git switch -c v2.1/example-work
```

Create a PR from a prepared body file:

```bash
gh pr create \
  --title "Example PR" \
  --body-file /tmp/pr-body.md \
  --base main \
  --head v2.1/example-work \
  --draft
```

Check PR metadata and CI:

```bash
gh pr view 33 \
  --json state,isDraft,mergeable,headRefName,baseRefName,statusCheckRollup

gh pr checks 33
```

Mark a draft PR ready:

```bash
gh pr ready 33
```

Merge a PR after review and green checks:

```bash
gh pr merge 33 --merge
```

After merge, sync local `main`:

```bash
git fetch origin
git switch main
git pull --ff-only
```

## Validation Before PR Or Merge

Before opening or merging PRs, run the relevant local checks. For broad repo changes, use the full v2 validation suite:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

Also check:

```bash
git status --porcelain
git diff --check
```

If Windows PowerShell cannot see `git` while running `run-all.ps1`, verify derived output cleanliness from WSL or another shell immediately afterward:

```bash
git status --porcelain -- \
  skills/sf6-agent/references/generated-knowledge-index.md \
  skills/sf6-agent/references/generated-concepts.md \
  skills/sf6-agent/assets/frame-current
```

Do not ignore failing checks. If a failure is legacy-obsolete or out of scope, document that clearly in the PR and create a follow-up issue when needed.

## PR Body Requirements

Every PR should include:

- summary
- changed surfaces
- boundary notes when relevant
- validation results
- issue mapping
- risks or follow-ups

Use `Closes #NN` only when the PR fully completes the issue.

Use `Refs #NN`, `Advances #NN`, or prose references when the PR only moves an issue forward.

## Review And Merge Rules

- Prefer draft PRs when validation is incomplete or when the PR is still being shaped.
- Mark a PR ready only after validation passes and the intended scope is clear.
- Do not merge with failing required checks.
- Do not merge broad changes that mix unrelated implementation, validation, and cleanup unless the issue explicitly calls for it.
- After merge, confirm the linked issue state and main-branch CI.

## Safety Rules

Do not put secrets into:

- commands committed in docs
- issue bodies
- PR bodies
- issue or PR comments
- smoke reports
- logs
- workflow files

Use redaction when command output includes local private state, tokens, account identifiers that should not be public, or secret-like values.

Do not use `gh` commands that mutate labels, milestones, issues, PRs, or repository settings unless the intended target is clear.

When browser/manual GitHub changes are used, summarize what changed and why `gh` was not the best tool for that operation.
