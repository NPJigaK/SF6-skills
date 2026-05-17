# Hermes Memory And Provider Policy

この文書は、private `sf6ingest` Hermes maintainer profile で使う memory、
session search、external Memory Providers の採用判断を定義します。

## Decision

v2.6 では、built-in memory と `session_search` を local non-canonical
context として許可します。

Validator anchor: built-in memory and `session_search` are local non-canonical context.

v2.6 では、external Memory Provider の既定採用は defer します。
Honcho、OpenViking、Mem0、Hindsight、RetainDB、ByteRover、Supermemory の
ような cloud / account / API-key backed provider は、データ保持、削除、
cost、profile 分離、Windows/WSL 運用、offline fallback、Hermes version
compatibility を確認する別 issue なしに有効化しません。

local-only candidate として Holographic は後続評価してよい候補です。
ただし、それもこの issue では有効化しません。

## What Goes Where

| Surface | 用途 | Repo authority |
| --- | --- | --- |
| `AGENTS.md` | project-wide mandatory behavior, guardrails, status protocol | yes |
| `workflows/` | maintainer procedures and repeatable repo operations | yes |
| reviewed repo artifacts | source, evidence, review, smoke, policy, validation output summaries | yes |
| skills / APM deps | reusable procedures and executor instructions | executor / procedure only |
| built-in memory | compact personal/project hints for next sessions | no |
| `session_search` | past-session recall for "前に話したか" search | no |
| external Memory Provider | optional semantic/user modeling layer after review | no |

Memory and session search may improve operator efficiency, but they must not
override current git, disk, issue, PR, validator, or checked-in artifact
evidence.

Validator anchor: Memory and session search may improve operator efficiency, but they must not override current git, disk, issue, PR, validator, or checked-in artifact evidence.

## Built-in Memory Rules

Allowed memory content:

- stable user preferences that affect interaction style
- stable local environment facts useful across sessions
- durable repo workflow reminders that are not already in `AGENTS.md`
- short pointers that a reviewed repo artifact exists
- durable lessons learned after they are verified as non-transient

Forbidden memory content:

- secrets, tokens, credentials, API keys, private URLs, or auth material
- exact SF6 current facts, formulas, rounding rules, or current answer data
- raw source excerpts, full transcripts, copyrighted material, screenshots, or
  media-derived raw data
- temporary file paths, one-off debugging state, CI run logs, or command dumps
- rules already present in `AGENTS.md`, canonical workflows, or reviewed docs
- tool avoidance conclusions caused only by transient failures

If a memory entry becomes important project policy, promote it to `AGENTS.md`,
`workflows/`, `docs/architecture/`, or another reviewed repo artifact and then
remove or shorten the private memory.

## Session Search Rules

`session_search` is allowed for recall, but only as secondary evidence.

Use it for:

- finding prior discussions or handoff context
- locating the name of a prior issue, PR, or report
- recalling a previous failed path that needs re-verification

Do not use it for:

- claiming current issue / PR / merge / validation status
- deciding current repo architecture without reading disk
- restoring old instructions that conflict with `AGENTS.md`
- promoting unreviewed prior chat as policy

For status, resume, or file-editing work, always apply the Project Status
Protocol in `AGENTS.md`: current date, cwd, git root, `git status`, current
issue/PR/docs, and validator evidence beat memory/session recall.

## External Memory Provider Evaluation Matrix

| Provider family | Current v2.6 decision | Reason |
| --- | --- | --- |
| built-in `MEMORY.md` / `USER.md` | allowed local-only | small, profile-local, already part of Hermes memory model |
| `session_search` / `state.db` | allowed local-only | useful recall, but non-canonical |
| Holographic | candidate for later local-only smoke | local SQLite store, no external account required |
| ByteRover local mode | candidate after CLI/storage review | local-first, but adds a separate CLI and tree state |
| Honcho self-hosted | deferred | richer modeling, but setup, storage, and deletion policy needed |
| Honcho Cloud | deferred | cloud user modeling requires privacy/data-retention review |
| OpenViking | deferred | provider-specific storage and deletion review needed |
| Mem0 | deferred | semantic memory can help, but storage/deletion/cost review needed |
| Hindsight | deferred | session-derived memory needs retention and provenance review |
| RetainDB | deferred | cloud service and cost boundary need review |
| Supermemory | deferred | cloud graph/profile capture needs privacy and deletion review |

## Adoption Requirements For A Later Issue

Before enabling an external Memory Provider, create a scoped issue and require:

- provider name and exact Hermes version tested
- local/self-host/cloud storage mode
- what data leaves the machine
- profile isolation behavior for `sf6ingest`
- data deletion / disable / rollback procedure
- cost and account requirements
- offline fallback behavior
- smoke test that no provider state, memory DB, logs, credentials, or raw
  transcript are committed
- clear statement that provider output remains non-canonical

For cloud providers, require explicit user approval before setup.

## Not Committed

Do not commit:

- `memories/`
- `MEMORY.md`
- `USER.md`
- `sessions/`
- `state.db`, `state.db-shm`, `state.db-wal`
- provider databases, exports, or profile stores
- raw transcripts
- logs, caches, browser state, cron state, checkpoints, local skills
- `.env`, `auth.json`, provider API keys, credentials, tokens

## References

- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
