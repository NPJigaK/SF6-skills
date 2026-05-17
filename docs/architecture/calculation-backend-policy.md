# Calculation Backend Policy

この文書は、v2.6 で repo-local maintainer が計算を必要とする場合の
backend selection と dependency boundary を定義します。

## Decision

v2.6 では、maintainer-local calculation execution の初期既定 backend
として SymPy を採用します。

SymPy は symbolic math / exact arithmetic backend として使います。
これは SF6 公式値、式、丸め規則、system mechanics、current facts、
public answer authority を repo が所有するという意味ではありません。

Validator anchor: SymPy is the initial default maintainer-local calculation backend.

## Managed Dependencies

Python package dependency は `packages/calculation-executor/` の
package-local project で管理します。

- package file: `packages/calculation-executor/pyproject.toml`
- lockfile: `packages/calculation-executor/uv.lock`
- dependency: `sympy==1.14.0`

この dependency は calculation trace helper の実行環境を固定するための
ものです。`packages/calculation-executor/` を custom SF6 math engine に
拡張するためのものではありません。

External Agent Skill dependency は maintainer-only APM manifest で管理します。

- manifest: `tools/agent-skills/apm.yml`
- lockfile: `tools/agent-skills/apm.lock.yaml`
- selected dependency:
  `K-Dense-AI/scientific-agent-skills/scientific-skills/sympy#v2.38.0`

The K-Dense SymPy skill is an executor / operator instruction dependency only.
It is not SF6 formula authority, rounding authority, input truth authority,
current-fact authority, or public answer behavior.

## Deferred Choices

SageMath is deferred in v2.6.

Reasons:

- It is a heavier CAS and install/runtime surface than the first-tranche
  maintainer calculation workflow needs.
- It needs a separate install, lock, security, and update policy before adoption.
- SymPy is sufficient for the initial backend decision and smaller PR scope.

MCP servers are deferred in v2.6.

Reasons:

- MCP server defaults are outside the current Agent Skill dependency manifest.
- MCP adoption needs server allowlists, no-secret config handling, output
  boundary rules, and validator coverage.

Additional K-Dense skills such as statistics are catalogued candidates only.
Do not add them to `tools/agent-skills/apm.yml` until a later issue defines a
specific maintainer task, selected skill subset, security review, and validator
expectation.

Broad scientific skill bundles are not adopted. Add only reviewed, task-scoped
skill subsets.

## SF6 Calculation Boundary

Do not add repo-owned:

- combo damage formulas
- scaling tables
- minimum guarantees
- frame advantage interpretation rules
- punish-window logic
- meaty or oki timing formulas
- resource formulas
- SF6 rounding rules
- current-system exception tables

If SF6-specific calculation is needed, the reusable knowledge should be a
repo-reviewed operator instruction or handoff prompt for the selected backend,
not accepted repo formula authority.

Calculation outputs remain trace candidates. If an input, route mapping,
formula-like instruction, or rounding instruction is missing or uncertain, the
trace must remain hold / blocked rather than public answer authority.

## Not Committed

Do not commit:

- Hermes memory, sessions, raw transcripts, local skills, Curator output,
  checkpoints, logs, caches, credentials, or profile state
- local installed Agent Skill directories
- API keys, `.env`, `auth.json`, or provider output
- generated frame-current assets, generated references, `.dist`, or public
  `sf6-agent` behavior for this decision

## References

- `docs/architecture/agent-skill-dependency-policy.md`
- `contracts/calculation-executor-trace.md`
- `packages/calculation-executor/README.md`
- `tools/agent-skills/apm.yml`
- `tools/agent-skills/apm.lock.yaml`
