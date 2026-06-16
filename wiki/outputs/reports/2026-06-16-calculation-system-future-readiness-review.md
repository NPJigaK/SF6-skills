---
type: output
output_type: report
title: "Calculation system future readiness review"
created: 2026-06-16
updated: 2026-06-16
status: active
confidence: medium
sources:
  - "[[concepts/combo-damage-ledger-protocol]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/juggle-system]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap]]"
  - "[[reviews/2026-06-15-jp-combo-damage-ledger-regression]]"
  - "[[reviews/2026-06-15-mai-combo-damage-ledger-regression]]"
related:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]]"
tags:
  - sf6
  - calculation
  - combo-damage
  - evaluation
---

# Calculation system future readiness review

## 要約

今回の計算系で今やるべき準備は、route parser や frame simulator を急いで作ることではない。先に prediction / postmortem / fixture / evidence / authority の contract を固定し、将来の combo damage、gauge、juggle、distance、timing proof が同じ evidence model を使えるようにするべき。

既存の `tools/calculations/combo_damage/calculate.py` は、source-backed hit ledger を受け取り、hit ごとに `floor(base_damage * condition_multiplier * effective_scaling)` を合計する deterministic calculator として妥当な境界にある。現在の contract では top-level `source_paths`、共通 `authority` field、hit ごとの `condition_multiplier` / `effective_scaling` / `source_paths` を必須にし、candidate authority を deterministic output から拒否する。[[concepts/combo-damage-ledger-protocol]] も、route text から delayed hit、状態遷移、距離条件、juggle state を推測しない方針を明確にしている。

一方で、将来の評価ループを入れる前に残る gap がある。特に、外部動画 / screenshot を durable validation source として扱う policy、prediction record を正解開示後に改ざんできないようにする hash gate、`schema.json` が formal JSON Schema ではなく repo-local contract descriptor であることは、後続の accuracy report や rule promotion を曖昧にしないために固定が必要である。

## 調査した範囲

- `tools/calculations/combo_damage/calculate.py`
- `tests/calculations/combo_damage/test_calculate.py`
- `tests/calculations/combo_damage/fixtures/**/*.ledger.json`
- `wiki/outputs/data/calculations/combo-damage/schema.json`
- `docs/superpowers/specs/2026-06-16-combo-prediction-evaluation-loop-design.md`
- [[concepts/combo-damage-ledger-protocol]]
- [[concepts/terms/damage-scaling]]
- [[concepts/juggle-system]]
- [[reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap]]
- [[reviews/2026-06-15-jp-combo-damage-ledger-regression]]
- [[reviews/2026-06-15-mai-combo-damage-ledger-regression]]
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/mai/classic-supercombo.json`
- `wiki/outputs/data/gauges/supercombo/numeric-tables.json`

## 現状

計算 tool は現在 1 系統だけで、`combo_damage/v1` として hit / segment ledger 算術に閉じている。入力 ledger は `input_type: combo_damage_ledger`、`schema_version: 1`、`rounding_policy: floor_each_hit_after_condition_multiplier_and_effective_scaling`、非空 `source_paths`、共通 `authority` object、明示された hit scaling factor を要求する。出力は calculator version、SymPy version、input hash、source authority、per-hit / segment rows、total damage を持つ。

fixture は 7 件あり、`tests/calculations/combo_damage/fixtures/<character>/<control>/` に JP Year1 legacy ODアムネジア 5790、JP Classic 3178、JP SA2 delayed-hit 3660、Mai Classic 4 件の regression を保持する。これらは `authority_type: regression_fixture` として扱い、`human_training_validation` は route-specific な observation / regression の根拠に留める。1 つの route で正解に合った補正を、そのまま `validated_rule` として calculator default へ入れない。JP Year1 ODアムネジア 5790 は、SA3 を `damage_granularity: "move_total"` / `segment_type: "super_art_full_move_total"` として表し、内部 hit split を modeled と誤読させない legacy fixture として保持する。fixture filename の日付は基本的に evidence date だが、過去 ruleset 再現動画では gameplay ruleset を代表する日付を使い、動画投稿日は metadata に残す。日付後の slug は `YYYY-MM-DD-<starter>[-condition]-<total_damage>.ledger.json` を基本にし、character / control type はディレクトリ構造で表す。

frame-data derived output 側には、将来の timing / hit-order proof に使える素材がある。JP / Mai の enriched rows は official fields に加えて `supercombo_startup`、`supercombo_active`、`supercombo_hitstop`、`supercombo_damage_scaling`、`supercombo_juggle_start`、`supercombo_juggle_increase`、`supercombo_juggle_limit`、`supercombo_notes` を持つ。JP `SA2 ラヴーシュカ` には 4 projectile の sequence timing、JP `弱ヴィーハト` には automatic spike timing、Mai `214HP (No Flame)` には extra scaling を示す source-backed note がある。[[concepts/terms/damage-scaling]]

ただし、これらの情報はまだ route parser や simulator 用に正規化されていない。`supercombo_notes` には重要情報が多いが自然文であり、cancel anchor、hitstop、距離、juggle height、相手 hurtbox などが揃わない route では、[[concepts/combo-damage-ledger-protocol]] の fail-closed 方針を維持する必要がある。

## Findings

### 1. `authority` は共通語彙に寄せたが、future record でも同じ gate が必要

combo damage ledger では `authority_type`、`confidence`、`source_paths`、`validation_status`、`review_status` を共通 field として要求する。既存 fixture の route-specific な説明は `authority.notes` に閉じ、集計や promotion gate は共通 field を読む。

残る risk は、future prediction / postmortem 側がこの vocabulary を再利用せず、別の authority 形を増やすこと。`combo-evaluation` の validator は、human-only observation を `validated_rule` に昇格させず、candidate authority を deterministic calculator に渡さないことを fail closed で検証する必要がある。

### 2. `schema.json` は formal JSON Schema ではなく contract descriptor

既存の `wiki/outputs/data/calculations/combo-damage/schema.json` は `required_input_fields` や `required_output_fields` を列挙する repo-local contract descriptor であり、JSON Schema Draft として validation できる形式ではない。`tests/calculations/combo_damage/test_calculate.py` も schema file の key presence を確認するだけで、ledger payload 全体を schema validation していない。

将来 `prediction.schema.json` / `postmortem.schema.json` を足す時に formal JSON Schema と誤解すると、dependency、validator、既存 schema との互換性が曖昧になる。初期実装では repo-local contract descriptor と explicit Python validator に寄せるのが安全。formal JSON Schema を採用するなら `pyproject.toml` / lockfile / validator CLI / 既存 schema migration を同時に行う。

### 3. 外部動画 / screenshot evidence policy が未解決

JP / Mai regression review は、YouTube metadata とユーザー提供 training-mode 表示を validation として使っているが、動画や screenshot は raw package として保存していない。各 review はこの gap を明記している。[[reviews/2026-06-15-jp-combo-damage-ledger-regression]] [[reviews/2026-06-15-mai-combo-damage-ledger-regression]]

この扱いは regression fixture には実用的だが、validated rule への昇格条件としては弱い。prediction / postmortem では `human_training_validation` と `video_metadata` を source fact ではなく validation metadata として分けるべき。外部動画を raw に保存するなら、manifest、clip範囲、metadata、screenshot、保存しない large media の方針を先に決める。

### 4. Hit-order proof 用の素材はあるが、入力 ledger がまだない

enriched frame data には startup、active、hitstop、juggle、damage scaling、notes があるため、将来の timing ledger の入力候補にはなる。特に JP `SA2 ラヴーシュカ`、`弱ヴィーハト`、Mai `214HP` のような delayed / route-state case では有用。

ただし、現時点で automatic hit order を確定するには不足がある。cancel anchor、hitstop の適用点、接触距離、projectile travel、juggle height、character hurtbox が route ごとに必要になる。したがって今すぐ simulator を作るより、`timing_proof` record の schema を先に作り、source-backed な event と unknown を分ける方がよい。[[concepts/combo-damage-ledger-protocol]]

### 5. Fixture promotion と rule promotion は分離して扱う必要がある

既存 fixture は regression として有用だが、`expected_total_damage` があることと validated rule に昇格できることは別。たとえば user-provided training-mode total がある route は regression fixture として扱えても、move-specific scaling rule を汎用 tool に入れるには official source、derived output、または accepted review が必要になる。

prediction / postmortem では `fixture_decision` を `not_fixture`、`candidate_fixture`、`regression_fixture`、`validated_fixture` に分ける。同時に `rule_promotion_decision` を `not_rule`、`working_hypothesis`、`rejected_hypothesis`、`validated_rule` に分ける。これにより「答えに合った fixture」と「tool rule にしてよい一般 rule」を混同しない。

### 6. Tests は fixture discovery まで入り、future evaluation validator は未実装

`tests/calculations/combo_damage/test_calculate.py` は全 `*.ledger.json` の discovery test を持ち、各 fixture の expected total、`matches_expected`、共通 authority contract を確認する。重要 route の per-hit / segment damage list は明示テストとして残している。

ただし、prediction / postmortem / report / promotion gate の validator はまだ存在しない。次の実装では、prediction hash、postmortem の 1:1 対応、taxonomy enum、human-only validation の rule promotion 拒否を検証対象にする。

### 7. 計算 family を早く共通 engine 化しない

将来の scope には damage、gauge、juggle、distance、timing があるが、同じ calculator class にまとめるのは早い。共有すべきなのは arithmetic engine ではなく、evidence / authority / input hash / calculator version / confidence / fail-closed policy である。

各 family は別 tool として始める。たとえば combo damage は hit ledger、gauge は gauge event ledger、juggle は juggle-state ledger、distance は movement / spacing ledger、timing は event ledger を持つ。共通化は、lifecycle と semantics が一致した field だけに限定する。

## 今のうちにできること

| Priority | Action | 理由 |
|---:|---|---|
| P0 | prediction record を immutable にし、postmortem に `prediction_sha256` を持たせる | 「答えを見る前の予測」を機械的に保証する |
| P0 | `schema_format` を明示し、repo-local contract descriptor か formal JSON Schema かを決める | validator 実装と dependency 方針が変わる |
| P0 | `combo-evaluation` validator で `fixture_decision` と `rule_promotion_decision` を検証する | regression fixture と validated rule の混同を防ぐ |
| P1 | `combo-evaluation` の Phase 1 を schema / examples / validate のみで始める | route parser なしで予測ループの記録を始められる |
| P1 | `human_training_validation` と `video_metadata` を rule source から分離する | 外部動画未保存でも regression として使えるが、source fact に昇格しない |
| P1 | important postmortem だけ Markdown review にし、通常は JSON record にする | wiki が review note だらけになるのを防ぐ |
| P2 | `timing_proof` record を設計する | `最速入力` や delayed hit を次に検証する足場になる |
| P2 | external video raw package policy を決める | 大きな動画保存、clip、screenshot、metadata の境界が必要 |

## 今やらない方がよいこと

- route text から damaging hit order を自動確定する parser。
- JP SA2 / portal / bomb / install の自然文 notes を直接 simulator rule にすること。
- 「動画で一度合った」ことを理由に move-specific rule を calculator default に入れること。
- gauge、juggle、distance、damage を 1 つの汎用 calculator engine にまとめること。
- formal JSON Schema dependency を入れずに `.schema.json` という名前だけを増やすこと。

## 推奨される次の小さな実装順

1. `combo-evaluation` の prediction / postmortem contract descriptor と examples を作る。
2. prediction payload hash と postmortem 参照を検証する `validate` CLI だけを追加する。
3. `validate` に human-only validation が `validated_rule` へ昇格しない gate を入れる。
4. 次のユーザー提示 combo から、答えを見る前に immutable prediction JSON を作る。
5. 正解開示後に postmortem JSON を作り、accuracy report を生成する。

この順なら、将来の route parser や timing ledger を入れる前に、失敗から学ぶ仕組みだけを先に安定化できる。
