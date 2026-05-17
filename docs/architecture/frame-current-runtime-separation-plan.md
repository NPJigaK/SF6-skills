---
title: Frame-current Runtime Separation Plan
status: accepted
last_reviewed: 2026-05-17
tracking_issue: "#242"
---

# Frame-current Runtime Separation Plan

この文書は、frame-current runtime assets を deferred public adapter surface から
切り離すための設計方針を定義する。

この PR は design-only であり、generated assets、generator output path、
`runtime_manifest.json` format、public `sf6-agent` behavior は変更しない。
In this design step, do not move generated frame-current assets.

## Current State

現在の exact current-fact runtime assets は次の構造になっている。

| 項目 | 現在値 |
|---|---|
| source authority | `data/exports/`, `data/roster/` |
| generated runtime output | `skills/sf6-agent/assets/frame-current/` |
| generator | `packages/skill-packaging/build-frame-current-runtime-assets.ps1` |
| validator | `tests/validation/validate-frame-current-assets.ps1` |
| contract | `contracts/frame-current-runtime-assets.md` |
| registry ID | `frame_current_runtime_assets` |

`data/exports/` と `data/roster/` は exact current-fact authority である。
`skills/sf6-agent/assets/frame-current/` は derived runtime payload であり、正本ではない。

問題は、derived runtime payload が `skills/sf6-agent/` 配下にあることだ。
`skills/sf6-agent/` は現在 deferred legacy public adapter surface であり、private
Hermes-first operation の active product focus ではない。これにより、current-fact
runtime payload と deferred public adapter が構造的に結合している。

## Target Direction

preferred target runtime surface は `runtime/frame-current/` とする。

理由:

- `data/exports/` と `data/roster/` を authority として維持し、derived runtime output を
  `data/` 配下に戻さない。
- `skills/sf6-agent/` から current-fact runtime payload を分離し、public adapter の
  remove / relocate / reactivate 判断を独立させる。
- `runtime/` 配下を generated runtime output surface として扱える。
- 将来、normalization runtime や他の private runtime payload も public adapter から
  独立して扱える。

target state:

```text
data/exports/
data/roster/
  -> packages/skill-packaging/build-frame-current-runtime-assets.ps1
  -> runtime/frame-current/
```

必要な期間だけ、deferred public adapter compatibility copy を残してよい。

```text
runtime/frame-current/
  -> skills/sf6-agent/assets/frame-current/
```

ただし compatibility copy は authority ではない。`runtime/frame-current/` を primary
derived runtime surface とし、`skills/sf6-agent/assets/frame-current/` は legacy adapter
copy または bridge として扱う。

## Transition Phases

### Phase A: Design Only

この文書を追加し、移行方針を review 可能にする。

この phase では次をしない。

- `skills/sf6-agent/assets/frame-current/` の移動。
- `packages/skill-packaging/build-frame-current-runtime-assets.ps1` の output path 変更。
- `runtime_manifest.json` の `asset_root` 変更。
- `tests/validation/validate-frame-current-assets.ps1` の expected path 変更。
- answer fixtures や public adapter behavior の変更。

### Phase B: New Runtime Surface

`runtime/frame-current/` を追加し、registry に new derived generated surface として
登録する。

この phase では generator を `runtime/frame-current/` に出力できるようにする。
旧 path はまだ削除しない。

必要な更新候補:

- `data/repository-surfaces.json`
- `contracts/frame-current-runtime-assets.md`
- `packages/skill-packaging/build-frame-current-runtime-assets.ps1`
- `tests/validation/validate-frame-current-assets.ps1`
- `tests/validation/run-all.ps1`
- README / workflow docs

### Phase C: Compatibility Bridge

public adapter compatibility が必要な間だけ、`runtime/frame-current/` から
`skills/sf6-agent/assets/frame-current/` へ copy する bridge を置く。

この bridge は deferred legacy surface であり、private operation の primary runtime
surface ではない。bridge が必要かどうかは、`skills/sf6-agent/` の remove / relocate /
reactivate ADR と合わせて判断する。

### Phase D: Answer Fixtures And Validators

answer fixtures、evidence-card examples、validator regex、doc examples が
`skills/sf6-agent/assets/frame-current/` を primary runtime authority として扱わないように
更新する。

この phase では、current-fact authority は引き続き `data/exports/` と `data/roster/` に
残す。`runtime/frame-current/` は generated exact current-fact runtime payload であり、
source authority ではない。

### Phase E: Legacy Path Retirement

`skills/sf6-agent/assets/frame-current/` を残す、compatibility copy にする、または削除する
判断は、`skills/sf6-agent/` 全体の remove / relocate / reactivate ADR と同期する。

legacy path の削除は、この design issue の scope ではない。

## Validator Expectations

移行時には、validator は次を区別する。

- source authority: `data/exports/`, `data/roster/`
- primary derived runtime output: `runtime/frame-current/`
- deferred public adapter compatibility copy: `skills/sf6-agent/assets/frame-current/`
- generated release bundle: `.dist/sf6-agent-bundle.zip`

`validate-frame-current-assets.ps1` は、最終的に primary runtime output を検証する。
compatibility copy を検証する場合は、primary runtime output と hash / manifest が一致する
ことを確認する bridge validator に分ける。

## Non-goals

- この design step では files を移動しない。
- この design step では generated assets を rebuild / commit しない。
- この design step では public `sf6-agent` behavior を変更しない。
- `data/exports/`、`data/roster/`、`official_raw`、current facts を変更しない。
- normalization runtime assets や generated knowledge references の relocation はこの文書では決めない。
- Hermes local state、raw transcripts、memory、sessions、logs、caches、credentials は repo に入れない。

## Acceptance For Later Implementation

実移行 PR は、少なくとも次を満たす必要がある。

- `runtime/frame-current/` の registry entry が追加される。
- `frame_current_runtime_assets` の role と source authority が更新される。
- generated runtime output が `data/exports/` と `data/roster/` から再現できる。
- old adapter path が残る場合は compatibility copy / bridge として明記される。
- `derived-build` lane が primary runtime output と compatibility copy の残差分を検出できる。
- public `sf6-agent` behavior 変更がある場合は、別 issue / ADR で明示される。
