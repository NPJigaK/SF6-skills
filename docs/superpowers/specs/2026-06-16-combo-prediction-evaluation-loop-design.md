# Combo Prediction Evaluation Loop Design

## Goal

SF6 のコンボダメージ計算について、ユーザーがコンボを提示し、LLM が答えを見る前に予測し、ユーザーが正解を開示し、誤差を分析して knowledge / fixture / rule を更新するループを安定運用できるようにする。

目標は、LLM の一回ごとの推論精度を信じることではない。予測、答え合わせ、反省、再発防止、検証済み fixture 化を機械的に残し、正答率を測定しながら改善することである。

## Non-Goals

- route text から hit order、juggle、距離、設置、delayed hit を自動で確定する parser は初期実装しない。
- source-backed でない仮説を `tools.calculations.combo_damage` の確定計算式へ入れない。
- YouTube 動画の自動解析、OCR、frame-by-frame capture pipeline は初期実装しない。
- 正解が開示されていない予測を validation fixture として扱わない。
- 仮説を source fact / derived fact / review accepted fact と同じ権威に昇格しない。

## Recommended Approach

既存 calculator の前後に、評価用の薄い JSON ledger 層を追加する。

`tools.calculations.combo_damage` はこれまで通り、確定済み hit ledger の算術だけを担当する。新しい評価ループは、予測時点の入力、使った知識、未知点、仮説、予測値、正解開示後の差分、原因分類、更新判断を記録する。これにより、予測には仮説を使えるが、calculator と validated fixture には未検証仮説が混入しない。

この方式は、最初から大きな simulation engine を作るよりも安全である。誤答ごとの原因が残るため、どのルールを source-backed tool に昇格すべきか、どの領域は人間検証待ちにすべきかを後から判断できる。

## Phase 0 Contract Stabilization

prediction / postmortem CLI を作る前に、既存 combo damage ledger と future evaluation record が共有する contract を固定する。

- `evidence` object: official source、community source、human-provided training-mode observation、video metadata、screenshot path、review note、fixture path を同じ形で参照する。
- `authority` object: `authority_type`, `confidence`, `source_paths`, `validation_status`, `review_status` を最低限の共通 field にする。
- `fixture_promotion` field: `not_fixture`, `candidate_fixture`, `regression_fixture`, `validated_fixture` を分ける。
- `rule_promotion` field: `not_rule`, `working_hypothesis`, `rejected_hypothesis`, `validated_rule` を分ける。`validated_rule` は一般化を明示承認した根拠がある場合だけ使う。
- `schema_format` field: 既存 `schema.json` が formal JSON Schema ではなく repo-local contract descriptor であることを明示する。formal JSON Schema に移行する場合は dependency と validator を同時に追加する。
- fixture tests: fixture を test code に個別列挙するだけでなく、directory discovery で全 ledger を最低限検証する。

この Phase 0 は計算式を増やさない。将来の route parser、timing ledger、gauge calculator、juggle checker が同じ evidence / authority model を使えるようにする準備である。

## Data Layout

```text
wiki/outputs/data/calculations/combo-evaluation/
  schema/
    prediction.schema.json
    postmortem.schema.json
    accuracy-report.schema.json
  predictions/
    <prediction-id>.prediction.json
  postmortems/
    <prediction-id>.postmortem.json
  reports/
    <date>-accuracy-report.json
```

Reader-facing なまとめが必要な場合だけ、`wiki/outputs/reports/` または `wiki/reviews/` に日本語 Markdown を置く。通常のループは machine-readable JSON を正本にする。

validated fixture は引き続き `tests/calculations/combo_damage/fixtures/**/*.ledger.json` に置く。prediction / postmortem は fixture 候補を記録するが、正解開示と原因分析だけでは fixture 昇格の十分条件にしない。

`schema/*.schema.json` は初期実装では repo-local contract descriptor とする。`jsonschema` package に依存する formal JSON Schema を採用する場合は、`pyproject.toml` / lockfile、validator CLI、既存 output schema との互換方針を同時に整備する。

## Prediction Record

予測時点で、答えを見る前に次を保存する。

- `prediction_id`: 安定した slug。例: `2026-06-16-jp-sa2-vihkhat-route`.
- `created_at`: 予測を出した日時。
- `character`, `control_type`, `version_context`: character、Classic / Modern、動画日付や patch context。
- `route_text`: ユーザーが提示した入力そのもの。
- `source_context`: 参照した wiki / raw / source page / fixture。
- `knowledge_snapshot`: 予測時点で重要だった rule、concept、review note の path。
- `preflight`: move resolution、non-linear hit gate、hit order proof、scaling-state gate の結果。
- `candidate_ledger`: 算術に使った hit list。確定ではなく candidate と明示する。
- `predicted_total_damage`: 予測値。
- `confidence`: `low`, `medium`, `high` のいずれか。
- `unknowns`: 未確定の cancel anchor、hitstop、距離、juggle height、multi-hit partial hit など。
- `hypotheses_used`: source-backed でない仮説の一覧。
- `record_status`: `predicted` または `candidate_only`。作成後は変更しない。

予測値を出せない場合も prediction record を作る。その場合は `predicted_total_damage` を省略し、`record_status` は `candidate_only` とする。

prediction record は正解開示後に書き換えない。`revealed` や `reviewed` は prediction file の status 更新ではなく、対応する postmortem / review event の存在から導出する。validator は prediction payload の SHA-256 を計算し、postmortem 側の `prediction_sha256` と照合する。

## Postmortem Record

正解開示後に、prediction と 1:1 で次を保存する。

- `prediction_id`: 対応する prediction。
- `prediction_sha256`: 正解開示前に作成された prediction payload の hash。
- `revealed_at`: 正解開示日時。
- `actual_total_damage`: ユーザーまたは source が開示した正解。
- `actual_evidence`: 動画 URL、スクリーンショット path、training-mode 表示、人間検証メモ。
- `delta`: `predicted_total_damage - actual_total_damage`。予測値がない場合は省略する。
- `correct`: exact match なら true。
- `error_taxonomy`: 複数選択可能な原因分類。
- `root_cause`: なぜ最初に見抜けなかったか。
- `would_have_caught_if`: 何をしていれば事前に防げたか。
- `rule_updates`: concept / review note / protocol に反映すべき変更。
- `fixture_decision`: `not_fixture`, `candidate_fixture`, `regression_fixture`, `validated_fixture`。
- `rule_promotion_decision`: `not_rule`, `working_hypothesis`, `rejected_hypothesis`, `validated_rule`。

postmortem は「今回だけ正解に合わせる」ためのメモではなく、次の未知コンボで同じ失敗を減らすための record にする。

## Evidence And Authority Model

prediction、postmortem、validated fixture は、同じ evidence / authority vocabulary を使う。

- `official_source`: Capcom official frame data、Battle Change、公式 mechanics page など。
- `community_source`: SuperCombo frame data、Game Data、Gauges、Patch Notes など。
- `human_training_validation`: ユーザーが提示した training-mode total、per-hit damage、scaling display、screenshot。
- `video_metadata`: URL、title、published/upload date、time range。動画自体を raw capture していない場合は source fact ではなく validation metadata として扱う。
- `review_accepted`: `wiki/reviews/` の accepted / active review note。
- `derived_output`: `wiki/outputs/data/` の JSON output と input hash。

fixture 昇格は `human_training_validation` だけでも regression fixture にはできるが、validated rule への昇格には official source、derived output、または review accepted な根拠が必要である。

`human_training_validation` と `video_metadata` は observation / validation metadata であり、それだけでは calculator に入れる一般 rule の source ではない。1 つの route で正解に合った補正は、その route の regression fixture には使えるが、同じ補正を別 route へ自動適用する rule にはしない。

## Initial Error Taxonomy

- `hit_order_unproven`: route text の順序を damaging hit 順として扱った。
- `delayed_hit_omitted`: 設置、portal、projectile、SA projectile などの delayed hit を落とした。
- `partial_multihit_wrong`: multi-hit 技の一部だけが当たる条件を誤った。
- `attack_step_wrong`: `hit_index` と `attack_step` を混同した。
- `immediate_scaling_scope_wrong`: immediate scaling の適用範囲を誤った。
- `starter_scaling_wrong`: starter、Counter、Punish Counter、Drive Rush starter の扱いを誤った。
- `drive_rush_penalty_wrong`: Drive Rush の one-time penalty や scaling interaction を誤った。
- `minimum_scaling_wrong`: minimum scaling、Super Art minimum、character-specific minimum を誤った。
- `condition_multiplier_wrong`: Counter / Punish Counter / punish-only multiplier の適用を誤った。
- `move_resolution_wrong`: 表記から source move への対応を誤った。
- `version_context_wrong`: 動画日付、patch、current-only 前提を誤った。
- `source_gap_unhandled`: source 不足を unknown とせず、推測を確定扱いした。
- `arithmetic_error`: ledger は正しいが floor / 合計 / multiplier 計算を誤った。

taxonomy は追加可能にするが、既存 label の意味は後方互換のため変えない。

## Rule And Hypothesis Boundary

観測、fixture、rule、仮説を分ける。

`validated_observation` は、training-mode 表示、スクリーンショット、動画 timestamp、ユーザー開示値など、個別 route の結果として trace できる事実である。これは postmortem evidence や regression fixture の根拠にはなるが、一般 rule ではない。

`regression_fixture` は、個別 route の再計算を守るための fixture である。route-specific な補正や hit ledger を含めてよいが、別 route へ適用する calculator rule ではない。

`validated_rule` は、official source、raw / derived output、または一般化を明示的に承認した review accepted note へ辿れる。calculator の default behavior や複数 route へ適用する rule に使ってよい。

`working_hypothesis` は、複数の observation から有力だが source-backed ではない。prediction には使えるが、output に明示し、calculator の default behavior には入れない。

`rejected_hypothesis` は、反例が出た仮説。再利用しないために残す。

prediction record は `hypotheses_used` を必須にし、仮説を使った予測と使っていない予測を accuracy report で分けられるようにする。

## Workflow

1. ユーザーが combo route と context を提示する。
2. agent は preflight を行い、prediction record を作る。
3. agent は予測値、confidence、unknowns、使った仮説を回答する。
4. ユーザーが正解を開示する。
5. agent は prediction file を書き換えず、`prediction_sha256` を持つ postmortem record を作り、原因分類と `would_have_caught_if` を書く。
6. source-backed に昇格できるものだけ concept / fixture / tool test に反映する。
7. accuracy report を再生成し、正答率、誤差、原因分類、character / route feature 別の傾向を見る。

## Tooling Scope

初期 CLI は小さくする。

- `new-prediction`: prediction JSON の雛形を作る。算術は既存 combo damage calculator を呼び出せる。
- `reveal`: prediction を変更せず、prediction hash と正解を持つ postmortem JSON の雛形を作る。
- `report`: predictions / postmortems を集計して accuracy report JSON を作る。
- `validate`: schema、prediction / postmortem の 1:1 対応、taxonomy label、fixture reference を検証する。

CLI は route parser ではない。hit ledger は人間または agent が preflight 後に書く。

validator は formal JSON Schema に依存しなくてよい。初期は Python の explicit checks で、required field、enum、path existence、prediction / postmortem relation、fixture promotion boundary を fail closed する。

## Accuracy Report

report は最低限、次を出す。

- 全体件数、exact match 件数、exact match rate。
- predicted-only、candidate-only、revealed、reviewed の derived state 件数。
- character、control type、version context、route feature 別の正答率。
- `hypotheses_used` 有無別の正答率。
- error taxonomy 別の件数。
- average absolute error、median absolute error、max absolute error。
- fixture 昇格済み件数と保留件数。

これにより「何となく良くなっている」ではなく、どの失敗が減ったかを確認できる。

## Verification

実装時は次を満たす。

- prediction / postmortem / report の contract validation test が通る。
- すべての postmortem が既存 prediction を参照する。
- `report` の出力が deterministic である。
- postmortem の `prediction_sha256` が対応する prediction payload と一致する。
- `reveal` は prediction payload を変更しない。
- taxonomy に未登録 label がある場合は fail closed する。
- `candidate_only` prediction が fixture として扱われない。
- `human_training_validation` だけの record は regression fixture にできても、validated rule として扱われない。
- 既存の `tests/calculations` は引き続き通る。

## Phased Implementation

Phase 1 は schema、JSON examples、`validate`、手書き prediction / postmortem の最小運用に絞る。

Phase 2 で `new-prediction`、`reveal`、`report` CLI を追加する。

Phase 3 で hypothesis registry と promotion / rejection gate を追加する。

Phase 4 で hit order proof 用の timing ledger を追加する。ここでも source-backed な startup、cancel anchor、scheduled hit timing、distance / juggle assumptions が揃う範囲だけを扱う。

## Design Decisions

予測レコードは machine-readable JSON を正本にする。日本語 Markdown の review note は、重要な誤答や reusable な反省だけに限定する。

ユーザーが開示した正解は postmortem evidence として使える。ただし validated fixture へ昇格するには、動画、スクリーンショット、training-mode 表示、既存 source のいずれかに trace できることを条件にする。validated rule へ昇格するには、個別 route の結果だけでなく、official source、derived output、または一般化を明示承認した review accepted note が必要である。

仮説は prediction には使う。ただし回答時に `hypotheses_used` と `unknowns` を明示し、確定 calculator の rule とは分ける。
