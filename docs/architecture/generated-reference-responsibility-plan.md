---
title: Generated Reference Responsibility Plan
status: accepted
last_reviewed: 2026-05-19
tracking_issue: "#244"
---

# Generated Reference Responsibility Plan

この文書は、generated knowledge references と旧 hand-written public adapter
references の責務を分けた Phase 2 設計方針を記録する。

Phase A は design-only だった。Phase B/C では generator output path を
`runtime/generated-knowledge/` に移した。public adapter was removed after runtime
relocation, so the old compatibility copy and adapter policy references are no
longer active repository surfaces.

## Current State

`skills/sf6-agent/references/` に同居していた旧 references は削除済み。

| Surface | 現在の path | 責務 |
|---|---|---|
| generated knowledge references | `runtime/generated-knowledge/` | `knowledge/curated/` から生成された stable concept runtime payload |

generated knowledge references の現在値:

| 項目 | 現在値 |
|---|---|
| source authority | `knowledge/curated/` |
| generated output | `runtime/generated-knowledge/` |
| generator | `packages/knowledge-generation/build-sf6-agent-knowledge.ps1` |
| validator | `tests/validation/validate-generated-knowledge.ps1` |
| registry ID | `generated_knowledge_references` |

解消した問題は、generated stable concept payload と hand-written adapter behavior
policy が同じ `references/` directory に置かれていたことだった。

## Responsibility Split

責務は次のように固定する。

| Responsibility | Owner surface | Notes |
|---|---|---|
| stable concept authoring | `knowledge/curated/` | canonical knowledge source。exact current values は入れない。 |
| generated stable concept runtime payload | `generated_knowledge_references` | derived output。手で正本化しない。 |

`generated_knowledge_references` は `knowledge/curated/` から再生成できる derived
surface であり、canonical authoring location ではない。

旧 adapter policy references は canonical SF6 knowledge へ昇格せず、adapter removal
とともに削除した。

## Target Direction

preferred target for generated stable concept runtime payload は
`runtime/generated-knowledge/` とする。

理由:

- `knowledge/curated/` を stable concept authoring authority として維持できる。
- generated concept payload を deferred public adapter path から切り離せる。
- `skills/sf6-agent/` の remove / relocate / reactivate 判断を、generated concept
  payload の primary runtime location から独立させられる。
- frame-current runtime separation の target である `runtime/frame-current/` と同じ
  runtime surface family にできる。

target state:

```text
knowledge/curated/
  -> packages/knowledge-generation/build-sf6-agent-knowledge.ps1
  -> runtime/generated-knowledge/
```

必要な期間だけ、deferred public adapter compatibility copy を残してよい。

```text
runtime/generated-knowledge/
  -> skills/sf6-agent/references/generated-*
```

compatibility copy は authority ではない。`runtime/generated-knowledge/` を primary
derived generated knowledge runtime surface とし、`skills/sf6-agent/references/generated-*`
は legacy adapter copy または bridge として扱う。

## Transition Phases

### Phase A: Design And Registry Split

この文書を追加し、registry に `sf6_agent_adapter_policy_references` を追加する。

この phase では次をしない。

- `skills/sf6-agent/references/generated-*` の移動。
- `packages/knowledge-generation/build-sf6-agent-knowledge.ps1` の output path 変更。
- generated references の rebuild / commit。
- public `sf6-agent` behavior の変更。

### Phase B: Runtime Generated Knowledge Surface

`runtime/generated-knowledge/` を追加し、registry に primary derived generated
knowledge runtime surface として登録する。

必要な更新候補:

- `data/repository-surfaces.json`
- `packages/knowledge-generation/build-sf6-agent-knowledge.ps1`
- `tests/validation/validate-generated-knowledge.ps1`
- `tests/validation/run-all.ps1`
- README / architecture docs

### Phase C: Compatibility Bridge

public adapter compatibility が必要な間だけ、`runtime/generated-knowledge/` から
`skills/sf6-agent/references/generated-*` へ copy する bridge を置く。

この bridge は deferred legacy surface であり、private operation の primary runtime
surface ではない。bridge が必要かどうかは、`skills/sf6-agent/` の remove / relocate /
reactivate ADR と合わせて判断する。

### Phase D: Public Adapter ADR

`skills/sf6-agent/` を remove / relocate / reactivate する ADR では、少なくとも次を
同時に決める。

- `sf6_agent_adapter_policy_references` を残すか、別 adapter path へ移すか、削除するか。
- generated stable concept runtime payload の primary path を
  `runtime/generated-knowledge/` にするか。
- compatibility copy をどの validation lane で確認するか。

## Validator Expectations

移行時には、validator は次を区別する。

- source authority: `knowledge/curated/`
- primary derived generated knowledge runtime output: `runtime/generated-knowledge/`
- deferred public adapter compatibility copy: `skills/sf6-agent/references/generated-*`
- hand-written public adapter behavior policy: `skills/sf6-agent/references/*-policy.md`

`validate-generated-knowledge.ps1` は primary generated knowledge runtime output を
検証する。compatibility copy を検証する場合は、primary output と content が一致する
ことを確認する。

## Non-goals

- この design step では files を移動しない。
- この design step では generated references を rebuild / commit しない。
- この design step では public `sf6-agent` behavior を変更しない。
- `knowledge/curated/`、`data/exports/`、`data/roster/`、current facts を変更しない。
- frame-current runtime assets、normalization runtime assets、`.dist` を変更しない。
- `skills/sf6-agent/` の remove / relocate / reactivate はこの文書では決めない。
- Hermes local state、raw transcripts、memory、sessions、logs、caches、credentials は
  repo に入れない。

## Acceptance For Later Implementation

実移行 PR は、少なくとも次を満たす必要がある。

- `runtime/generated-knowledge/` の registry entry が追加される。
- generated stable concept runtime output が `knowledge/curated/` から再現できる。
- old adapter path が残る場合は compatibility copy / bridge として明記される。
- `sf6_agent_adapter_policy_references` は adapter behavior only として残す、移す、
  または削除する判断が ADR で明記される。
- `derived-build` lane が primary output と compatibility copy の残差分を検出できる。
- public `sf6-agent` behavior 変更がある場合は、別 issue / ADR で明示される。
