---
name: codex-hermes-sf6
description: Repo-local Codex pointer pack for safe Hermes delegation in the SF6 Knowledge Agent Kit.
---

# Codex-Hermes SF6 Pack Pointer

This is repo-local maintainer support only. It is a thin pointer, template,
and checklist surface for Codex-operated Hermes work. It is not canonical
procedure authority, not public `sf6-agent` distribution, and it does not
define public answer behavior.

Validator anchor: this pack is not canonical procedure authority.

## Canonical Procedure References

Use the reviewed repo surfaces as authority:

- `AGENTS.md`
- `workflows/maintainer-agent-session.md`
- `workflows/codex-to-hermes-delegation.md`
- `docs/architecture/codex-hermes-bridge-policy.md`
- `docs/architecture/hermes-cli-capability-reference.md`
- `docs/architecture/sf6-video-analysis-protocol.md`
- `docs/architecture/external-frame-atlas-policy.md`
- `contracts/hermes-delegation-sanitized-trace.md`
- `contracts/calculation-executor-trace.md`
- `workflows/calculation-backend-handoff.md`

If this pack conflicts with those sources, the canonical workflow, contract,
validator, issue scope, and merged repo artifact win.

## Use This Pack For

- Finding the Codex-to-Hermes request template.
- Finding the Hermes response review checklist.
- Finding short guard reminders for local state, current facts, article/video
  material, visual assets, stale PRs, and calculation executors.
- Remembering that Hermes output remains draft input and, for Hermes-first
  analysis, the primary draft input.

## Do Not Use This Pack For

- Public SF6 answers.
- Public `skills/sf6-agent/` behavior changes.
- Exact current-fact promotion from Hermes output.
- `official_raw` overrides.
- Hermes CLI command truth.
- Live Hermes or live video analysis in CI.
- Committing Hermes memory, sessions, local skills, Curator output, browser
  state, cron state, Kanban state, checkpoints, local configs, logs, caches,
  credentials, secrets, tokens, raw transcripts, or provider raw output.
- Treating stale PR #71 and PR #83 as active source material.

## Pack Helpers

- `resources/codex-to-hermes-request-template.md`: fill-in template only.
- `resources/hermes-response-review-checklist.md`: pre-conversion checklist.
- `resources/*`: pointer notes to reviewed policies and contracts.
- `guards/*`: short boundary reminders only.

## Verification

For pack changes, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-codex-hermes-pack.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane read-only
```

Also run:

```bash
git diff --check
git diff --check origin/main...HEAD
```
