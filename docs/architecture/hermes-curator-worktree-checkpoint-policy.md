# Hermes Curator / Worktree / Checkpoint Policy

この文書は、private `sf6ingest` Hermes maintainer profile で使う Curator、
git worktree、checkpoints / `/rollback` の運用ライフサイクルを定義します。

対象は maintainer-local operation だけです。Curator output、local skills、
checkpoint store、Kanban state、session exports、logs、caches、profile state
は repo authority ではありません。

## Decision

v2.6 では以下を既定方針にします。

- Curator は local skill hygiene のために使ってよい。ただし初回と通常運用
  の前に `hermes curator run --dry-run` を確認する。
- 重要な hand-authored / workflow-critical skill は real Curator run の前に
  `hermes curator pin <skill>` で保護する。
- Real Curator run の前に `hermes curator backup --reason "<reason>"` を
  取り、必要なら `hermes curator rollback` または
  `hermes curator restore <skill>` で戻す。
- substantial Hermes editing は専用 git worktree または `hermes -w` を使う。
- Checkpoints は Hermes tool-driven edits の local safety feature として
  有効にしてよい。Git commit、validator、PR review の代替にはしない。
- Gateway、cron、Kanban は v2.6 既定では有効化しない。

## Curator Lifecycle

Curator may be used only for local `sf6ingest` skill hygiene.

Before a real Curator run:

1. Verify repo baseline with `git status --short --branch`.
2. Confirm `HERMES_HOME` is outside the repository.
3. Run `hermes curator status`.
4. Run `hermes curator run --dry-run`.
5. Review the proposed changes locally.
6. Pin important skills with `hermes curator pin <skill>`.
7. Take a manual backup with `hermes curator backup --reason "<reason>"`.

During or after a real Curator run:

- Do not let Curator mutate checked-in repo surfaces.
- Review `~/.hermes/logs/curator/.../REPORT.md` locally.
- If a change is wrong, use `hermes curator rollback` or
  `hermes curator restore <skill>`.
- If a lesson is durable, promote a summary through issue / PR / reviewed repo
  artifact. Do not commit the raw Curator report.

Curator promotion path:

```text
local Curator finding
  -> maintainer summary
  -> GitHub issue or PR note
  -> reviewed repo artifact under AGENTS.md / workflows / docs / tests
  -> validator coverage when the rule must be enforced
```

## Worktree Lifecycle

Use a dedicated git worktree, or Hermes automatic worktree mode with
`hermes -w`, when any of the following is true:

- multiple agents may work in parallel
- the change is a broad refactor or multi-directory edit
- the task is experimental and may be discarded
- generated surfaces or packaging outputs may be rebuilt
- the task may run destructive commands or large automated edits
- the work may conflict with active maintainer edits in the main checkout

Small docs-only edits in a clean checkout may stay in the main checkout, but
the maintainer must still verify `git status --short --branch` before editing.

Worktree rules:

- Use one branch/worktree per substantial Hermes experiment.
- Keep branch names issue-scoped.
- Commit reviewed milestones with Git; checkpoints are only between-commit
  safety nets.
- Remove worktrees only after deciding whether to keep or discard the work.
- Do not force-remove a worktree with unreviewed changes.
- Do not commit `.worktrees/` contents or Hermes-generated local state.

## Checkpoint Lifecycle

Checkpoints may be enabled for Hermes sessions that edit files, run generated
surface builds, or perform substantial tool-driven changes.

Checkpoint state lives under `~/.hermes/checkpoints/` and must remain local.
It is not a repo artifact.

Use checkpoints this way:

1. Enable checkpoints for the local Hermes session or profile when the task may
   edit files.
2. Keep normal Git commits as the reviewed history.
3. Use `/rollback diff <N>` before restoring.
4. Use `/rollback <N>` for agent-driven mistakes that should be undone in the
   working tree.
5. Re-run `git status --short --branch` and relevant validators after a
   rollback.
6. Periodically inspect and prune local checkpoint storage with Hermes
   checkpoint commands.

Do not use checkpoints to:

- hide or skip Git review
- replace PR review
- restore across unrelated tasks without inspecting the diff
- preserve raw media, datasets, credentials, or generated caches in repo
  artifacts
- claim validation passed after rollback without re-running validators

## Deferred Operations

Gateway, cron, durable Kanban, and background multi-agent workers remain
deferred by default for v2.6 `sf6ingest` operation.

If later enabled, they need a separate policy covering:

- profile isolation
- authorization and allowed users
- worktree isolation
- checkpoint behavior
- local state cleanup
- failure recovery
- no raw transcript / local state commit

## Not Committed

Do not commit:

- `~/.hermes/skills/` local managed skill directories
- `~/.hermes/skills/.archive/`
- `~/.hermes/skills/.curator_backups/`
- `~/.hermes/logs/curator/`
- Curator `run.json` or raw `REPORT.md`
- `~/.hermes/checkpoints/`
- Kanban state
- checkpoint store
- session exports
- logs, caches, browser state, cron state
- `.env`, `auth.json`, credentials, tokens, secrets
- raw Hermes transcripts or local command output

## References

- https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
- https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees
- https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback
