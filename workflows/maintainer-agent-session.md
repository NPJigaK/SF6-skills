# Maintainer Agent Session Workflow

## Purpose

Use this workflow to standardize maintainer agent sessions for
Codex/Hermes-assisted repo work.

This workflow preserves the v2.2 operating lanes:

- Codex remains the normal repo implementation executor.
- Hermes is the repo-local growth engine when a configured maintainer profile
  is available.
- For in-scope analysis, review, and growth tasks, Codex should operate Hermes
  instead of performing primary object-level analysis itself.
- GitHub issues and pull requests are the primary progress state.
- Private memory is not repo state.
- Completion is based on verification results, not agent confidence.

## Start-Of-Session Checks

Before implementation starts:

1. Read `AGENTS.md`.
2. Read the target GitHub issue or pull request.
3. Read tracking issue #94 when working on v2.2.
4. Restate the target issue scope, non-goals, and acceptance before editing.
5. Confirm the branch and base branch.
6. Confirm the worktree is clean before editing.
7. Pull or fetch latest `main` when appropriate.
8. Inspect validators relevant to the changed surfaces.
9. Confirm dependencies are complete, or explicitly report the missing
   dependency before proceeding.
10. For analysis, review, or growth tasks, confirm whether Hermes-first
    delegation applies and record any Codex fallback reason before primary
    analysis starts.

For issue-scoped implementation PRs, do not begin editing until the target
scope, non-goals, and acceptance are clear enough to test.

## During-Session State Rules

- GitHub issues and pull requests are the primary progress state.
- PR bodies, issue comments, smoke reports, and reviewed docs are visible
  handoff surfaces.
- Do not rely on private model memory, Hermes memory, local sessions, local
  skills, Curator output, Kanban workers, or checkpoints as repo state.
- Do not add always-changing root progress files without a later architecture
  decision.
- Keep work issue-scoped.
- Do not hide unfinished work by rewriting task scope.
- If scope pressure appears, report it instead of silently expanding scope.
- If the task needs another issue's work, stop and report the dependency.

## Verification Requirements

Before opening a PR, run focused validators for the changed surfaces.

For normal private Hermes-first docs, contracts, workflow, registry, or
boundary-only changes, run the read-only lane:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane read-only
```

Use `-Lane derived-build` when generated references, frame-current assets, or
normalization assets are intentionally in scope. Use `-Lane
legacy-distribution` only when deferred public distribution bundle or installer
surfaces are intentionally in scope.

When practical, also run the full validation suite. Omitting `-Lane` is
equivalent to `-Lane all`:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

Always check whitespace and patch formatting:

```bash
git diff --check
```

For PR branches, check the full branch diff when practical:

```bash
git diff --check origin/main...HEAD
```

If Windows PowerShell cannot see `git` during generated-surface checks, report
the warning and separately verify from WSL or another git-visible environment
that these generated or derived surfaces have no residual diff:

- `skills/sf6-agent/references/`
- `runtime/generated-knowledge/`
- `.dist`
- `runtime/frame-current/`
- `skills/sf6-agent/assets/frame-current/`
- `runtime/normalization/`
- `skills/sf6-agent/assets/normalization/`

See `docs/architecture/powershell-compatibility-policy.md` for the canonical
`pwsh` / Windows PowerShell fallback policy.

Completion is determined by validation results, not agent confidence.

## End-Of-Session Handoff

Use this handoff shape in PR bodies, final implementation summaries, or issue
comments when a task is not fully merged:

```text
Task / issue:
Branch:
Commit or head SHA:
Files changed:
Validators run:
Validation results:
Warnings:
Unresolved items:
Intentionally not done:
Generated surfaces checked:
Clean worktree status:
Next action:
```

For merged PRs, also report:

- PR state
- issue state
- merge commit or squash commit SHA
- whether the tracking issue remains open

## Stop Conditions

Stop and ask for review when any of these apply:

- Scope creep risk appears.
- A required dependency is missing.
- A validator fails for a reason that is not obviously in scope.
- Generated-output residual diff might be present.
- Canonical authority is unclear.
- The requested work would cross into another issue.
- The work would require secrets, credentials, private local state, or
  unreviewed local memory.
- The implementation would change public `sf6-agent` behavior without issue
  scope explicitly allowing it.
