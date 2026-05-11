# Hermes CLI Capability Reference

## Purpose

This document records the reviewed Hermes CLI and tool capabilities that Codex
may consider for repo-local growth delegation.

It is a maintainer reference only. It does not require Hermes for public
`sf6-agent` users, does not change public answer behavior, and does not make
Hermes output canonical.

This issue implements the reference as documentation only. It does not add a
machine-readable `data/toolchain/hermes-cli-capabilities.json` file. A future
issue may add policy data if the repo needs validator-readable capability
metadata.

## Source And Verification Policy

Capability entries in this document are based on official Hermes Agent docs or
official NousResearch/hermes-agent release notes reviewed on 2026-05-11.

Official sources used:

- Hermes Agent CLI Commands Reference:
  <https://hermes-agent.nousresearch.com/docs/reference/cli-commands/>
- Hermes Agent Toolsets Reference:
  <https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference>
- Hermes Agent Sessions:
  <https://hermes-agent.nousresearch.com/docs/user-guide/sessions>
- Hermes Agent Profiles:
  <https://hermes-agent.nousresearch.com/docs/user-guide/profiles/>
- Hermes Agent Curator:
  <https://hermes-agent.nousresearch.com/docs/user-guide/features/curator>
- Hermes Agent Scheduled Tasks:
  <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/>
- Hermes Agent Checkpoints and Rollback:
  <https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback>
- Hermes Agent skills guide:
  <https://hermes-agent.nousresearch.com/docs/guides/work-with-skills>
- NousResearch/hermes-agent release notes:
  <https://github.com/NousResearch/hermes-agent/releases>

Unverified commands must not be encoded as required repo behavior. If a
capability is not verified, not present in a maintainer environment, or depends
on unavailable provider/model/toolset support, Codex must record the limitation
and use a documented fallback or hold.

CI must not require live Hermes execution and must not perform online
latest-version checks.

## Status Model

Use these status values when future repo surfaces refer to Hermes capabilities:

- `allowed_manual`: verified capability that a maintainer may use locally when
  configured and in scope.
- `planned`: verified or expected capability that needs a later issue's policy,
  fixtures, or validator boundaries before normal SF6 repo use.
- `deferred`: capability intentionally not enabled by v2.3 unless later
  planning approves it.
- `nullable`: command or invocation details are not verified or not guaranteed
  in the maintainer environment.

The status describes repo policy, not whether a local machine currently has
Hermes installed or configured.

## Capability Reference

| Capability | Reviewed command or surface | Status | SF6 repo policy |
| --- | --- | --- | --- |
| One-shot chat | `hermes chat --query "..."` / `hermes chat -q "..."` | `allowed_manual` | May support bounded local delegation. Output is draft input and must be reviewed before becoming repo artifacts. |
| Scripted one-shot mode | `hermes -z "..."` | `planned` | May be useful for future local scripting, but #121 does not wire it into validators, CI, repo automation, or public answer behavior. |
| Provider/model override | `hermes chat --provider <provider> --model <model>` and `hermes -z ... --provider ... --model ...` | `allowed_manual` | Local maintainer choice only. Do not commit credentials, provider config, or local model inventory. |
| Toolsets | `hermes chat --toolsets <csv>` and `hermes tools` | `allowed_manual` | Tool availability is environment and toolset dependent. Future pack guidance should request only issue-appropriate toolsets. |
| Skill preload | `hermes chat --skills <name>` / `hermes chat -s <name>` | `allowed_manual` | Local Hermes skills remain procedural local state. Do not commit raw local skills or treat them as canonical. |
| Worktree mode | `hermes chat --worktree` | `allowed_manual` | May isolate local Hermes work. Resulting files still require Codex review, validators, and PR scope before merge. |
| Checkpoints | `hermes chat --checkpoints` | `allowed_manual` | Local safety feature only. Checkpoint storage is non-canonical and must not be committed. |
| Resume / continue | global `--resume <session>` / `--continue [name]`, and `hermes chat --resume` / `--continue` | `allowed_manual` | Session recall can aid local continuity, but sessions are non-canonical and cannot replace repo artifacts or issue comments. |
| Profiles | `hermes --profile <name> ...`, `hermes profile list`, `hermes profile use`, `hermes profile show` | `allowed_manual` | Profiles isolate local Hermes config/state. Do not commit profile exports, `.env`, local memory, sessions, skills, cron jobs, or state databases. |
| Profile cloning/import/export | `hermes profile create --clone`, `--clone-all`, `export`, `import` | `deferred` | Useful for local administration, but not part of SF6 repo workflow. Treat as local-state operations outside repo artifacts. |
| Sessions | `hermes sessions` plus list/browse/export/prune/rename/delete style operations documented by Hermes | `allowed_manual` | Session management is local maintenance. Exported sessions/logs must not be committed or used as canonical evidence. |
| Curator review | `hermes curator status`, `hermes curator run --dry-run` | `allowed_manual` | Curator output is local procedural maintenance input only. It may suggest skill cleanup but cannot mutate repo canonical surfaces. |
| Curator protection | `hermes curator pin <skill>`, `hermes curator unpin <skill>` | `allowed_manual` | Protect relied-upon local skills before Curator or agent-managed updates. Pinned/local skill state remains outside repo authority. |
| Curator restore | `hermes curator restore <name>` | `allowed_manual` | Local recovery only. Restored skills are not repo artifacts unless distilled through issue scope, validators, PR review, and merge. |
| Vision analysis | `vision_analyze` tool through appropriate toolsets | `planned` | Candidate support for future observation workflows. Output remains draft input and cannot become exact current-fact authority. |
| Video analysis | `video_analyze` tool, with exact toolset and invocation details to remain verified against official docs and the maintainer environment | `planned` | Official release notes mention native video understanding on Gemini and compatible multimodal models. Provider, model, and toolset availability is environment-dependent. #123 must define SF6-specific protocol before normal use. |
| Cron | `hermes cron create ...` and cronjob tool operations | `deferred` | #121 does not enable scheduled Hermes operation. Cron output and `~/.hermes/cron/*` are local state and must not enter the repo. |
| Gateway | `hermes gateway <subcommand>` | `deferred` | Messaging gateway is not enabled by this issue. #119 owns plugin/gateway planning if local CLI access is insufficient. |
| MCP | `hermes mcp` | `deferred` | MCP config is not enabled by this issue. Do not add production MCP config, credentials, or gateway state. |
| ACP server | `hermes acp` | `deferred` | Editor integration is outside #121 scope and must not become a CI or public `sf6-agent` requirement. |
| Kanban | official Hermes Kanban CLI surface | `deferred` | Official docs describe Kanban, but #121 does not enable Kanban workflows. Kanban board state is local and non-canonical unless a later scoped issue verifies and approves details. |
| Update | `hermes update`, `hermes update --check`, `hermes update --backup` | `deferred` | Do not auto-update Hermes from repo workflows. Tool freshness remains reviewed policy, not newest-at-any-cost automation. |

## Video Capability Boundary

`video_analyze` is not a source of truth.

For SF6 work, `video_analyze` must be treated as a provider/model/toolset
dependent tool candidate. It may be referenced as planned for future local
analysis only after #123 defines the SF6 video-analysis protocol.

Video tool output must remain observation draft input. It must not:

- infer exact current facts from video alone
- override packaged frame-current `official_raw`
- become exact startup, active, recovery, damage, route, matchup, or coaching
  authority
- bypass issue scope, validators, or review

If `video_analyze` is unavailable or unverified in a maintainer environment,
Codex must use the fallback/hold behavior defined by #123.

External frame-atlas/cache policy is handled by #124 and is not a Hermes CLI
capability by itself. #121 documents Hermes CLI/tool capabilities and should
cross-reference #124 when video-analysis workflows rely on external visual
references.

## Curator And Local Skill Boundary

Curator capabilities are local procedural skill maintenance tools. They may be
used to inspect, dry-run, pin, unpin, or restore local agent-created procedural
skills.

Curator output is not canonical evidence and does not mutate repo canonical
surfaces. Any reusable procedure must be distilled into an in-scope reviewed
repo artifact before promotion.

Do not commit raw Hermes skill files, local skill directories, Curator
archives, memory snapshots, sessions, logs, caches, credentials, or local
state.

## Deferred Integration Boundary

The following are explicitly not enabled by #121:

- production cron
- gateway
- MCP
- ACP
- Kanban workflows
- plugin/gateway remote access
- live Hermes CI execution
- online latest-version checks
- automatic Hermes update workflows

Future work may plan or enable these only through scoped issues that preserve
the Codex-Hermes bridge policy, public `sf6-agent` boundary, local-state
boundary, and validator/review requirements.

## Public Adapter Boundary

End users do not need Hermes.

This reference does not modify `skills/sf6-agent/`, public answer behavior,
release bundle behavior, generated outputs, frame-current assets, or
normalization assets.
