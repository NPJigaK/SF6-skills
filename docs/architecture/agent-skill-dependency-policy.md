# Agent Skill Dependency Policy

この文書は、private `sf6ingest` Hermes maintainer profile で使う外部
Agent Skill 依存を GitHub-reviewable に管理するための方針です。

対象は maintainer operation だけです。外部 Agent Skill は SF6 公式値、
式、丸め規則、current facts、public answer authority を提供しません。
外部 Agent Skill は executor / operator instruction dependency であり、
repo authority は `AGENTS.md`、`workflows/`、`contracts/`、validator、
reviewed repo artifact に残します。

## Decision

v2.6 では APM を依存 manifest / lockfile の標準候補として採用します。

ただし、public `sf6-agent` distribution は ADR-0002 により deferred の
ままです。APM は public skill distribution を再開するためではなく、
private maintainer profile の外部 skill 依存を review するために使います。

管理場所:

- manifest: `tools/agent-skills/apm.yml`
- lockfile: `tools/agent-skills/apm.lock.yaml`
- allowlist: `data/toolchain/hermes-maintainer-skill-allowlist.json`

`apm.lock.yaml` は、外部依存を初めて追加して `apm install` を実行した
時点で commit します。依存が空の間は lockfile は不要です。

## Manifest Rules

`tools/agent-skills/apm.yml` は maintainer-only manifest です。

依存を追加する場合は、以下を必須にします。

- GitHub / Git host dependency は reviewed tag または immutable SHA に pin
  する。
- In English validator terms: every external Agent Skill dependency must use a
  reviewed tag or immutable SHA.
- Floating `main`、default branch、moving branch は原則禁止。使う場合は
  temporary exception として issue / PR に理由と review deadline を書く。
- multi-skill repository は必要な skill subset だけを選ぶ。広い bundle を
  丸ごと入れない。
- Renovate が拾える metadata comment を依存行の直前に置く。
- private local path、absolute path、secrets、tokens、profile state、
  local Hermes state を manifest に入れない。
- dependency の採用理由、source review、security/trust review、expected
  maintainer task を PR に書く。

Dependency example:

```yaml
dependencies:
  apm:
    # renovate: datasource=git-tags depName=K-Dense-AI/scientific-agent-skills
    - K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0
```

The example uses a virtual subdirectory plus a pinned tag. APM records selected
skill subsets in `apm.yml` / `apm.lock.yaml` when `--skill` is used, so broad
skill collections must preserve the selected subset in reviewed files.

## Lockfile Rules

When dependencies exist:

- Commit `tools/agent-skills/apm.lock.yaml`.
- Do not hand-edit the lockfile.
- Review resolved commit SHA, content hash, deployed file list, and any security
  scan findings.
- Use frozen / audit style checks before treating a dependency update as ready.
- Do not commit deployed local Hermes profile state, local installed skill
  directories, memories, sessions, logs, caches, raw transcripts, `.env`, or
  `auth.json`.

If APM output paths would collide with public `skills/sf6-agent/`, generated
adapter references, `.dist`, or runtime assets, hold the PR until the output
boundary is redesigned.

## Renovate Rules

Renovate tracks `tools/agent-skills/apm.yml` with a regex custom manager.

The custom manager uses the metadata comment immediately before a dependency
line and supports `git-tags` / `git-refs` style datasources. For normal
dependencies, prefer `git-tags` so Renovate proposes reviewed release/tag
updates.

Renovate PRs for Agent Skill dependencies are dependency PRs, not automatic
authority promotions. A maintainer must still review:

- upstream skill diff
- pinned ref / resolved commit
- selected skill subset
- APM lockfile changes
- security/audit output
- whether the skill remains executor-only for SF6 work

`data/toolchain/hermes-maintainer-skill-allowlist.json` must list every
reviewed external APM skill under `external_apm_skills`. The allowlist entry
must match the manifest dependency, lockfile, selected virtual path, pin policy,
and authority boundary. Built-in Hermes skills and external APM skills must not
be mixed: for example, `sympy` is external APM-managed, not a built-in default
or conditional Hermes skill.

## Current Math Skill Decision

v2.6 selects only the K-Dense-AI `scientific-agent-skills` SymPy skill as the
initial external Agent Skill dependency for maintainer-local calculation work.

```yaml
dependencies:
  apm:
    # renovate: datasource=git-tags depName=K-Dense-AI/scientific-agent-skills
    - K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0
```

This is a selected subset, not adoption of the whole scientific skill bundle.
SageMath skills, statistics skills, MCP servers, and broad math/science bundles
remain deferred until a later issue defines a task-scoped adoption policy.
The lockfile must preserve `virtual_path: scientific-skills/sympy` so reviewers
can verify that the selected subset, not the broad bundle, is installed.

See `docs/architecture/calculation-backend-policy.md`.

## Math Skill Boundary

Math-related skills such as SymPy / SageMath operator instructions are managed
through this same dependency mechanism if adopted.

They may help produce calculation traces or prompts for a selected CAS /
symbolic math backend. They must not become repo-owned SF6 formula authority.
SF6-specific calculation behavior belongs in maintainer instructions for the
selected backend, not in accepted repo facts.

## Not Managed Here

Do not use this manifest for:

- Hermes memory
- session search state
- external Memory Provider state
- Curator output
- profile exports
- local installed skill directories
- gateway / bot config
- MCP server defaults
- public `sf6-agent` distribution

Gateway, MCP, external Memory Providers, and broad third-party skill bundles
remain deferred unless a later issue adds a reviewed adoption policy.

## References

- https://microsoft.github.io/apm/consumer/manage-dependencies/
- https://microsoft.github.io/apm/reference/cli/install/
- https://docs.renovatebot.com/modules/manager/regex/
- https://docs.renovatebot.com/modules/datasource/git-tags/
- https://docs.renovatebot.com/modules/datasource/git-refs/
