---
title: Generic Schema Validation Runner
status: accepted
last_reviewed: 2026-05-18
tracking_issue: "#252"
---

# Generic Schema Validation Runner

この文書は、JSON Schema backed artifacts を共通 runner で検証する
Phase 3 方針を定義する。

## Decision

JSON Schema と JSON artifact の対応は
`tests/validation/schema-validation-manifest.json` に集約する。

`tests/validation/validate-json-schema-manifest.ps1` は manifest を読み、
各 schema と artifact を PowerShell `Test-Json` で検証する。

この runner は structural schema validation 専用であり、既存の semantic
validators を置き換えない。

## Initial Coverage

初期 coverage は、network access や external dependency なしで安定して検証できる
JSON artifact に限定する。

| Schema | Documents |
|---|---|
| `contracts/repository-surface.schema.json` | `data/repository-surfaces.json` |
| `contracts/agent-toolchain.schema.json` | `data/toolchain/maintainer-agent-toolchain.json` |
| `contracts/normalization-aliases.schema.json` | `data/aliases/ja-query-fixtures.json` |
| `contracts/external-frame-atlas-source-evaluation.schema.json` | `data/external-frame-atlas/evaluation/source-evaluation-matrix.json` |
| `contracts/external-frame-atlas-source.schema.json` | `tests/fixtures/external-frame-atlas/*.json` |

Schemas with external relative `$ref` files, markdown front matter contracts,
or command-generated traces stay under dedicated validators until a later PR
adds safe bundling or extraction support.

## Boundary

- Generic schema runner checks shape, required fields, enums, constants,
  additional properties, and other JSON Schema structural constraints supported
  by the local PowerShell runtime.
- Dedicated validators continue to check semantic boundaries, cross-file
  consistency, generated-output reproducibility, current-fact rules, copyright
  boundaries, and repo policy wording.
- Adding a schema/document pair requires updating the manifest and keeping any
  necessary semantic validator in place.

## Non-Goals

- Do not replace semantic validators in this issue.
- Do not validate markdown front matter through this runner in this issue.
- Do not change artifact schemas, current facts, generated runtime assets,
  `official_raw`, public `sf6-agent` behavior, or package executable behavior.
- Do not add external schema validation dependencies.
- Do not commit Hermes local state, raw transcripts, memory, sessions, logs,
  caches, credentials, or secrets.
