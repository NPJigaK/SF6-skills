# Hermes Maintainer Harness Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-01 |
| Timezone | Asia/Tokyo |
| OS | WSL2 on Linux 6.6.87.2-microsoft-standard-WSL2 |
| Hermes version | Hermes Agent v0.12.0 (2026.4.30) |
| Python | 3.11.15 |
| OpenAI SDK | 2.32.0 |
| Profile | `sf6smoke` |
| Hermes profile path | `/home/devkey/.hermes/profiles/sf6smoke` |
| Repo commit | `2d8e93561e43b40681e6bc69c1d21d2b2c961597` |
| Issue | #30 |

## Setup

- Hermes was installed in WSL2, not native Windows.
- Smoke used `HERMES_HOME=/home/devkey/.hermes/profiles/sf6smoke`.
- The `sf6smoke` profile was cloned from default config but uses separate profile state.
- Profile memory was disabled for the smoke run:
  - `memory.memory_enabled: false`
  - `memory.user_profile_enabled: false`
- Curator was disabled for the smoke run:
  - `curator.enabled: false`
- `skills.external_dirs` pointed at the repo skills parent directory:
  - `/mnt/e/github/SF6-skills/skills`
- `workflows/` was not configured as a skill directory. It remained a repo maintainer playbook surface.
- Secrets were not recorded in this report.

## Doctor Summary

`hermes doctor` completed successfully enough for this smoke:

- Python environment: pass
- Required packages: pass
- Hermes command installation: pass
- `openai-codex` auth in `sf6smoke`: pass
- `codex CLI`: pass
- Optional integrations such as Nous Portal, OpenRouter, Discord, browser CDP, and web search were not configured and were not required for this smoke.

## Skill Discovery

`hermes skills list` showed `sf6-agent` as:

| Skill | Source | Trust | Status |
|---|---|---|---|
| `sf6-agent` | local | local | enabled |

## Cases

| Case | Expected | Result | Notes |
|---|---|---|---|
| `sf6-agent` discoverable | Hermes can see/use `skills/sf6-agent` through external skill discovery. | Pass | Hermes loaded `sf6-agent` with `--skills sf6-agent` and identified it as the runtime adapter for SF6 Knowledge Agent Kit. |
| Canonical/derived boundary | Hermes states `knowledge/`, `data/exports/`, and `data/roster/` are source-of-truth surfaces, while generated references and frame-current assets are derived. | Pass | Hermes described `knowledge/` as canonical stable knowledge, `data/exports/` and `data/roster/` as current fact authority, `generated-*` as derived, and `assets/frame-current/` as derived runtime assets. |
| Workflow boundary | Hermes identifies `workflows/` as canonical maintainer procedures, not public skills or gameplay knowledge. | Pass | Hermes described `workflows/` as canonical procedures for update/ingest/review tasks and not canonical SF6 gameplay knowledge. |
| Hermes pack boundary | Hermes treats `packs/hermes-sf6/` as optional harness guidance, not canonical knowledge. | Pass | Hermes described `packs/hermes-sf6/` as optional Hermes maintainer harness guidance and not required public distribution. |
| Memory boundary | Hermes does not treat Hermes memory as canonical SF6 knowledge. | Pass | Hermes explicitly stated that Hermes memory is not source-of-truth SF6 knowledge and should not preserve current frame data or curated facts. |
| Repo cleanliness | No repo-local Hermes memory, cron, secrets, sessions, profile state, or local state files are created. | Pass | `git status --porcelain` was clean after smoke before writing this report. A repo scan found no `.hermes`, memory, cron, session, state, or `.env` artifacts under the repo. |

## Commands

The smoke used non-interactive Hermes CLI prompts with the dedicated profile:

```bash
HERMES_HOME=/home/devkey/.hermes/profiles/sf6smoke hermes chat -Q --max-turns 8 --skills sf6-agent -q "<smoke prompt>"
```

Session IDs were created in the Hermes profile outside the repo:

- `20260501_103332_0cd352`
- `20260501_103406_5e3098`
- `20260501_103439_89e65a`
- `20260501_103533_2707eb`

These session records are Hermes operational state and are not repository knowledge or evidence.

## Findings

- Hermes can discover `sf6-agent` through the repo `skills/` directory.
- Hermes can state the v2 canonical/derived boundaries accurately.
- Hermes can distinguish `workflows/` from public skills and from canonical gameplay knowledge.
- Hermes can keep `packs/hermes-sf6/` in the optional maintainer harness role.
- Hermes profile/session state stayed outside the repository.

## Follow-ups

- No blocking follow-up from this smoke.
- Future Hermes smoke runs may test a fuller interactive workflow, but should keep dedicated profile isolation and repo cleanliness checks.
