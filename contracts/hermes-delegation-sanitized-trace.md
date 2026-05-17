# Hermes Delegation Sanitized Trace Contract

この contract は、Codex app -> Hermes -> optional provider Codex の
delegation / handoff を、repo に残せる sanitized metadata として記録する
ための境界を定義します。

Sanitized trace は orchestration metadata only として扱う。

Sanitized trace は、Hermes-first orchestration がどの issue scope で行われ、
どの role boundary と validator boundary で repo artifact に変換されたかを
示す review artifact です。Hermes output、provider output、local state、
raw command output、または SF6 gameplay fact の証拠ではありません。

## Authority Boundary

Sanitized traces may record:

- `analysis_mode` が `hermes_primary` か `codex_fallback` か。
- Codex app が `hermes_operator` / `boundary_auditor` /
  `artifact_converter` / `validator_executor` として動いたこと。
- Hermes が primary draft input を返したこと、または fallback reason が
  記録されたこと。
- provider Codex を使った場合に、executor-only の task/output summary が
  used / rejected として整理されたこと。
- どの repo artifact に変換されたか、どの validator が必要だったか。
- raw/local/private state を commit していないという sanitization assertion。

Sanitized traces must not record:

- raw Hermes transcript
- raw provider output
- raw command output or tool logs
- Hermes memory, sessions, local skills, Curator output, Kanban state,
  checkpoints, logs, caches, profile state, `.env`, or `auth.json`
- credentials, secrets, tokens, API keys, OAuth material, or private URLs
- screenshots, videos, audio, binary media, or local browser/cache artifacts
- SF6 current facts, official values, formulas, rounding rules, or analysis
  correctness claims

## Required Behavior

- `schema_version` must be `hermes-delegation-sanitized-trace/v1`.
- `analysis_mode: hermes_primary` requires Hermes primary analyst role and
  Codex app operator/auditor role.
- `analysis_mode: codex_fallback` requires `fallback.occurred: true` and a
  non-empty fallback reason.
- provider Codex, when used, must remain a bounded executor and must not be
  recorded as final authority.
- `post_delegation_review.hermes_output_is_draft_input` must be true.
- `post_delegation_review.canonical_promotion_allowed` must be false.
- `validators.live_hermes_required` must be false.
- All `sanitization_assertions` must remain false for unsafe content.

## Relationship To Delegation Workflow

`workflows/codex-to-hermes-delegation.md` defines request and response shape.
This contract defines the sanitized trace that may be committed after that
workflow is used. A trace is acceptable only after Codex has reviewed Hermes
draft output against issue scope, converted supported material into repo
artifacts, and run the relevant validators.

## Validation

- JSON shape: `contracts/hermes-delegation-sanitized-trace.schema.json`
- Fixtures: `tests/fixtures/hermes-delegation-sanitized-trace/`
- Semantic validator:
  `tests/validation/validate-hermes-delegation-sanitized-traces.ps1`
