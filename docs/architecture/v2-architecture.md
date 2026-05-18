# V2 Architecture

## Product

SF6 Knowledge Agent Kit is a reviewable knowledge repo for AI agents answering Street Fighter 6 questions.

The former public adapter was removed after runtime payload relocation. The repo now keeps canonical source surfaces and repo-local runtime payloads.

## Canonical Surfaces

- `knowledge/`: curated concepts, glossary, strategy notes, and reviewable claims.
- `data/exports/`: exact published current-fact exports.
- `data/roster/`: exact current roster source.
- `contracts/`: schemas and structured artifact contracts.
- `workflows/`: maintainer procedures for growing and refreshing the repo.
- `evals/`: answer-quality questions and rubrics.

## Runtime Surface

- `runtime/generated-knowledge/`: derived stable concept runtime payload.
- `runtime/frame-current/`: derived exact current-fact runtime payload.
- `runtime/normalization/`: derived query-normalization runtime payload.

## Derived Surface Rules

Generated references and frame-current assets are outputs. They must carry provenance and must point back to canonical source paths.

Generated knowledge runtime assets come from `knowledge/curated/` only. They must not contain exact current frame values. The runtime path is `runtime/generated-knowledge/`.

Frame-current assets come from `data/exports/` plus `data/roster/` only. They must not include manual-review rows, raw snapshots, normalized intermediate files, or CSV sidecars. The runtime path is `runtime/frame-current/`.

## Evidence Model

V2 uses generic evidence metadata. Canonical artifacts should describe source kind, source role, evidence basis, verification state, confidence, volatility, patch sensitivity, review status, source references, and review timing.

These fields are the metadata vocabulary used by current contracts, evals, and validators.

## Answer Modes

Public answers should communicate the mode and evidence boundary naturally:

- `stable_concept`
- `verified_current_fact`
- `strategy_or_matchup_knowledge`
- `observation`
- `unresolved_or_hold`

Evals check whether the answer mode and boundary behavior are correct.

## Hermes

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available.

Hermes is not canonical memory and is not a public answer adapter. No Hermes memory, sessions, profile state, browser state, cron state, secrets, local managed skills, local config, or chat transcripts should be shipped.

public adapter was removed. Canonical maintainer procedures remain under `workflows/*`, and reusable Hermes-assisted output must be committed as repo artifacts.

See [decisions/0001-hermes-primary-orchestration.md](./decisions/0001-hermes-primary-orchestration.md).
