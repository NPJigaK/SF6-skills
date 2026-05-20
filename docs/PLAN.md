# SF6 Knowledge Coach Redesign And Governance Plan

## Summary

目的は、現在はJPを主対象にした、キャラ非依存の個人用SF6コーチAIを作ること。

JP専用AIにはしない。JPは最初の `active_character_package` として扱い、将来ほかの自キャラを追加できる構造にする。

このPLANは実装指示書ではなく、全体アーキテクチャ契約にする。実装は必ず小さな `ExecPlan` に分割して行う。

確認済み根拠:

- Codex公式は、複雑な作業では先にPlanを作る運用を推奨している。参考: [Codex Best Practices](https://developers.openai.com/codex/learn/best-practices)
- Codex公式は、`AGENTS.md` をプロジェクト規約として読み込む仕組みを説明している。参考: [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md)
- Codex公式は、ExecPlan形式の長時間作業計画を `AGENTS.md` で規定する例を示している。参考: [Using PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans)
- ローカル `codex review --help` では、`--uncommitted`、`--base`、`--commit`、prompt引数が表示された。ただし、実装時確認では `codex review --uncommitted "<prompt>"` と `codex review --uncommitted -` は拒否されたため、`--uncommitted` ではpromptなしで使う。
- Codex CLIの `/review` は作業ツリーのレビューに使える。参考: [Codex CLI Slash Commands](https://developers.openai.com/codex/cli/slash-commands)

## Governance

### 1. `docs/PLAN.md`

最新の全体設計を `docs/PLAN.md` に置く。

`docs/PLAN.md` はアーキテクチャ契約であり、一括実装対象ではない。

`docs/PLAN.md` の末尾には必ず英語と日本語のアーキテクチャ契約注記を置く。

### 2. ExecPlan

複数ファイル変更、schema変更、runtime変更、validator変更、data pipeline変更、private/public境界変更は、実装前に個別の `ExecPlan` を作る。

ExecPlanは `docs/execplans/` に置く。

各ExecPlanは少なくとも次を持つ。

- Purpose
- Scope
- Acceptance Criteria
- Files / Interfaces
- Validation Commands
- Progress
- Decision Log
- Deviations
- Risks
- Completion Review Table

実装者はExecPlanに書かれていない機能、依存、schema、public API、runtime挙動を追加しない。

計画が誤っている、または不足している場合は、`Decision Log` に記録して確認待ちにする。

### 3. `AGENTS.md`

`AGENTS.md` は、Codexや他の保守エージェントが最初に読む恒久ルールの入口にする。

`AGENTS.md` には次を含める。

- Project Goal
- Plan Conformance
- Hard Rules
- Validation
- Done

### 4. Mandatory Review

各ExecPlan実装完了時に、必ずレビューを行う。

使用方法は次のいずれかにする。

- Codex CLI: `/review`
- Codex CLI: `codex review --uncommitted`
- Codex CLI: `codex review --base <branch>`
- Codex CLI: `codex review --commit <sha>`
- 別セッションでの独立レビュー

このローカルCLI版では `codex review --uncommitted` とprompt引数を併用できない。custom review instructions が必要な場合は、`/review`、対応するreview mode、または別セッションレビューを使う。

レビューでは必ず次の照合表を出す。

```text
| PLAN項目 | 実装内容 | 変更ファイル | 検証コマンド | 結果 | 逸脱 | 未完了 | リスク |
```

レビューの目的は、実装がExecPlanと一致しているか、余計な変更がないか、検証が足りているかを確認すること。

## Architecture Decisions

### 1. 知識レイヤー

知識は次の5層に分ける。

- `universal_mechanics`: 全キャラ共通の仕組み、用語、原則
- `opponent_character_profile`: 相手キャラが何で勝つか、何が危険か
- `active_character_package`: 現在使っている自キャラの技、立ち回り、実行手段
- `matchup_overlay`: 自キャラ x 相手キャラでだけ成立する確反、例外、相互作用
- `personal_layer`: ユーザー本人の癖、負けパターン、練習課題

JPは `active_character_package` の最初の実装対象にする。

### 2. データ配置

公開Git repoに置くもの。

- 知識本文
- スキーマ
- 生成手順
- 検査ルール
- 評価ケース
- synthetic example
- 個人情報漏れ検査
- public DB生成元

Git外private vaultに置くもの。

- 実ユーザープロファイル
- 実練習ログ
- 実回答ログ
- 現在の練習課題
- 個人レビュー済み知識
- private overlay DB
- 元動画、切り出しクリップ、ローカル解析結果

### 3. 回答runtime

初期runtimeは次にする。

```text
Codex CLI
  -> sf6 CLI
    -> Python tools
      -> public Git knowledge
      -> generated public DB
      -> private vault
      -> private overlay DB
```

日常回答ではWeb検索を初期defaultにしない。Webはupdate/research modeだけで使う。

API fallbackは初期defaultにしない。Codex Pro/Codex CLI枠を優先する。

Discord botは後段で追加する薄い入口にする。Discord側に知識判断を持たせない。

## Interfaces And Contracts

### 1. Knowledge Item

```yaml
knowledge_item:
  id: string
  layer: universal_mechanics | opponent_character_profile | active_character_package | matchup_overlay | personal_layer
  status: candidate | observed | review_ready | reviewed | personal_reviewed | deprecated | rejected
  title: string
  summary: string
  evidence:
    source_refs: []
    evidence_basis: official | verified_by_user | video_observation | community | inferred
    confidence: low | medium | high
    patch_sensitivity: low | medium | high
    review_status: unreviewed | reviewed
  payload: object
```

通常回答で使える状態は原則として `reviewed`、`personal_reviewed`、公式・現在値として検証済みの数値データに限定する。

`candidate`、`observed`、`deprecated` は断定根拠にしない。

### 2. 数値・確反・フレーム

次の話題では、自然文知識だけで答えない。

- フレーム
- 有利不利
- 確反
- ダメージ
- 補正
- コンボダメージ
- パッチ差分
- 技の現在値

### 3. Initial Search / Retrieval Contract

初期検索・取得基盤は次の組み合わせにする。

- SQLite + FTS: prose/search 用。概念説明、レビュー済み知識、用語、戦術メモの検索に使う。
- Structured numeric tables: frame、damage、scaling、punish、combo damage、patch delta、current move facts の正確値に使う。
- Alias dictionary from `data/aliases/`: 日本語・英語・略称・表記揺れのquery normalizationに使う。
- Metadata filters: evidence boundary、status、review state、patch sensitivity、source role、personal/public boundary の絞り込みに使う。

数値回答は、prose FTSやLLM memoryではなく、deterministic tools/tables の結果を必須根拠にする。

ベクトル検索は初期実装に入れない。

### 4. Video / VLM Pipeline

動画分析は次の流れにする。

```text
許可された動画
  -> Git外 Media Vault
  -> FFmpegで音声・フレーム抽出
  -> ASR
  -> 低fps粗解析
  -> CV/OCR/ルールでHUD・ゲージ・表示文字・イベント抽出
  -> 重要区間を切り出し
  -> VLMで説明補助
  -> vlm_observation / video_observation を作成
  -> candidate claim化
  -> 人間レビュー
  -> reviewed knowledgeへ昇格
```

VLMは重要区間の説明補助に限定する。

VLMに任せるもの。

- 重要区間の場面説明
- 行動候補の説明
- 判断ミス候補の説明
- 不明点の列挙
- 人間レビュー用メモ

VLMに任せないもの。

- フレーム値の確定
- 確反あり/なしの確定
- ダメージ、補正、コンボ成否の確定
- 入力や押したボタンの断定
- 正式知識への自動昇格

初期defaultは次にする。

```yaml
vlm_default:
  provider_profile: llama_cpp_server
  model_profile: qwen3_vl_8b_instruct_gguf_q4_k_m
  model: Qwen3-VL-8B-Instruct-GGUF Q4_K_M
  role: important_segment_explanation
```

`vlm_observation` は常に `observation_candidate` から始める。

## Implementation Phases

### Phase 0: Governance Baseline

- `docs/PLAN.md` を作成する
- `docs/execplans/` とExecPlan templateを作成する
- `AGENTS.md` にProject Goal、Plan Conformance、Hard Rules、Validation、Doneを追加する
- 以後の複数ファイル変更はExecPlan単位に分割する

### Phase 1: Local QA Vertical Slice

- `sf6 ask` はPhase 1の必須要件にしない。optional/deferred とする
- Codex-generated answer prose を使い、deterministic `sf6` CLI subcommands/tools で回答根拠を組み立てる
- Phase 1の `sf6` CLI subcommands/tools は、context resolve、search、frame/current-fact lookup、answer prepare、answer verify、append-only Git-outside answer logging を対象にする
- public knowledge + generated public DB + private vault overlayを読む
- JPを初期 `active_character_package` として扱う
- 回答時に内部 `resolved_context` を作り、Git外に記録する
- 個人情報がpublic repoに混入したら検査で失敗させる

### Phase 2: One Video To Reviewed Knowledge

- 1本の許可済み動画をMedia Vaultに入れる
- FFmpeg、ASR、CV/OCR、イベント抽出を通す
- 重要区間だけVLMへ渡す
- `vlm_observation` と `video_observation` を作る
- そこから `candidate` を作り、人間レビューで `reviewed` へ昇格する

### Phase 3: Private Overlay

- 実ユーザーの練習ログ、負けパターン、現在の練習課題をGit外に保存する
- `personal_reviewed` はprivate overlay DBだけに置く
- 回答時に個人情報を使った場合は、必要に応じてそのことを明示する

### Phase 4: Review Workflow

- 知識追加はPRレビュー可能な単位にする
- `candidate`、`observed`、`review_ready`、`reviewed` の昇格条件を検査する
- 古いパッチ情報や不確かな情報は `deprecated` または `rejected` に落とす
- ExecPlan完了ごとに必須レビューと照合表を出す

### Phase 5: Discord Thin Adapter

- Discord botは薄い入口として追加する
- Discord側に知識判断を持たせない
- 同じ `sf6` CLIまたはローカルruntimeを呼ぶ
- コスト回避のため、初期defaultではAPI回答runtimeにしない

## Test Plan

必須テスト。

- 数値・確反・フレーム質問で専用データを使わない回答を失敗させる
- `candidate` や `observed` を通常回答で断定利用したら失敗させる
- `deprecated` を回答に使ったら失敗させる
- 未実装キャラの自キャラ固有回答を断定したら失敗させる
- private vaultの実個人情報がpublic repoに入ったら失敗させる
- 回答ごとに `resolved_context` がGit外へ記録されることを確認する
- 動画観察から直接 `reviewed` に昇格できないことを確認する
- VLMがフレーム、確反、入力、コンボ成否を断定したら失敗させる
- `vlm_observation` がschemaに合わない場合は失敗させる
- ExecPlan対象の実装完了時に必須レビュー照合表が作られていることを確認する

VLM評価は段階式にする。

```text
Step 0: 5短尺クリップ
Step 1: 16短尺クリップ
Step 2: 30+短尺クリップ
```

評価観点。

- 場面説明が大きく外れていないか
- HUDや状況を無理に断定しないか
- イベントログと矛盾しないか
- 不明な点を不明と言えるか
- フレーム、確反、入力、コンボ成否を勝手に断定しないか
- JSON/schemaを守れるか
- 人間レビューに役立つメモになっているか

## Assumptions

- 初期対象ユーザーは個人利用のSF6プレイヤー
- 初期の自キャラはJP
- 将来の自キャラ追加を前提にするが、初期実装で全キャラ分の空構造は作らない
- 公開repoに実個人情報は置かない
- 日常回答runtimeはCodex CLI中心
- API課金前提の回答runtimeにはしない
- 初期検索・取得はSQLite + FTS、structured numeric tables、`data/aliases/` alias dictionary、metadata filtersを組み合わせる
- 数値回答はdeterministic tools/tablesを必須根拠にし、prose FTSやLLM memoryから答えない
- ベクトル検索は後続判断
- 動画の元データと解析中間物はGit外
- VLM初期defaultはQwen3-VL-8B-Instruct-GGUF Q4_K_M
- VLM runnerは初期defaultを `llama_cpp_server` とするが、実装時に導入確認が必要
- VLMモデルは固定せず、設定で差し替え可能にする
- `docs/PLAN.md` は全体契約であり、実装は必ず個別ExecPlanに分割する

This PLAN is the architecture contract.
Implementation must be performed through smaller ExecPlans.
Do not implement broad changes directly from this PLAN.

このPLANは全体アーキテクチャ契約である。
実装は、個別のExecPlanに分割して行う。
このPLAN全体を一括実装対象にしない。
