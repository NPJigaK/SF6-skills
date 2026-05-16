---
name: codex-hermes-sf6
description: Repo-local Codex playbook for safe Hermes delegation in the SF6 Knowledge Agent Kit.
---

# Codex-Hermes SF6 Playbook

This is repo-local Codex skill/playbook source. It is maintainer support only,
not public `sf6-agent` distribution, and it does not define public answer
behavior.

## When To Use

Use this playbook when issue scope allows Hermes-first analysis or when Codex
needs to delegate bounded draft or review work to Hermes, such as:

- source analysis drafts
- claim or observation draft shaping
- architecture review or directory audit drafts
- validator-pattern proposals
- review checklist drafting
- maintainer workflow improvement proposals

Codex remains the repo implementation entrypoint. When Hermes is configured
and the task is in scope for Hermes-first analysis, Codex is the Hermes
operator, boundary auditor, artifact converter, validator runner, and PR
executor. Codex must not replace Hermes as the primary object-level analyst.

## When Not To Use

Do not use this playbook to:

- answer public SF6 user questions directly
- change `skills/sf6-agent/`
- promote exact current facts from Hermes output
- override packaged `official_raw`
- run live Hermes in CI
- run live video analysis in CI
- scrape, download, cache, or store external visual assets
- rely on closed PR #71 or PR #83

## Required Procedure

1. Read the target issue and restate scope, non-goals, and acceptance.
2. Follow `workflows/maintainer-agent-session.md`.
3. Use `workflows/codex-to-hermes-delegation.md` for request and response
   shape when Hermes-first analysis or delegation is appropriate.
4. Check `docs/architecture/codex-hermes-bridge-policy.md` to confirm
   Hermes-first delegation applies or to record a documented fallback reason.
5. Check `docs/architecture/hermes-cli-capability-reference.md` for reviewed
   Hermes capability status. Do not invent command requirements.
6. For video work, check
   `docs/architecture/sf6-video-analysis-protocol.md`.
7. For external visual atlas work, check
   `docs/architecture/external-frame-atlas-policy.md`.
8. Convert useful Hermes output into reviewed repo artifacts only when the
   target issue scope allows it.
9. If Codex fallback analysis is used, record why Hermes-first delegation was
   not attempted or could not complete.
10. Run the relevant validators and record results before commit.

## Review Checklist

- Hermes output remains draft input.
- For Hermes-first analysis, Hermes output is the primary draft input.
- Codex did not perform primary object-level analysis unless a fallback reason
  is recorded.
- Provider Codex, when used by Hermes, remained an executor and did not become
  the final analyst.
- Source references are review inputs, not canonical evidence by themselves.
- Exact current facts remain grounded in current-fact authority surfaces.
- Web, article, video, and external visual atlas inputs do not override
  `official_raw`.
- Hermes memory, sessions, local skills, Curator output, browser state, cron
  state, Kanban state, and checkpoints are non-canonical.
- Stale PR #71 and PR #83 are closed historical debt, not active sources.
- Validators and PR review remain required.

## Verification

For pack changes, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-codex-hermes-pack.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

Also run:

```bash
git diff --check
git diff --check origin/main...HEAD
```

If PowerShell cannot see `git` during generated-surface checks, verify from a
git-visible environment that generated references, `.dist`, frame-current
assets, and normalization assets have no residual unintended diff.

## Pitfalls

- Do not copy the Hermes CLI command table into this pack.
- Do not make Hermes local state into repo state.
- Do not confuse video observations with current-fact authority.
- Do not treat external GIF, image, or frame atlas assets as source-of-truth
  data.
- Do not add public adapter behavior to a maintainer playbook.
