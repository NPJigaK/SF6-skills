# LLM Wiki エージェント指示

## コアモデル

このリポジトリは Karpathy-style の LLM-maintained knowledge base です。

人間はソースを選び、質問し、重要な変更をレビューし、方向性を決めます。
LLM は wiki を書き、リンクし、保守します。

ドメイン非依存の基礎方針は [ROADMAP.md](ROADMAP.md) に従ってください。

## Domain Phase Status

この repo は、`raw/` / `wiki/` / schema の base pattern 初期実装を完了済みとみなし、
現在は SF6 domain-enabled LLM Wiki として運用します。

ただし、Karpathy-style の境界は維持します。

- `raw/` は原文、元データ、取得物、manifest、metadata、validation の層です。
- `wiki/` は LLM が保守する compiled knowledge の層です。
- domain-specific tools は `tools/` 配下に置きます。
- tools は source of truth ではなく、raw capture、validation、derived output 生成の補助です。
- 新しい domain pipeline を追加する時は、raw manifest、metadata、validation、source page、review note、index/log 更新を必須にします。

## レイヤー

- `raw/`: 原則として不変の、原文・元データを保つソース素材。例外として、manifest の `storage_policy` で最新ミラーまたは更新可能な取得一式と示されている raw 一式（例: `raw/frame-data/`, `raw/battle-change/`, `raw/web-pages/`）は、再取得、取得物の差し替え、manifest / metadata / validation / hash 更新を許す。
- `wiki/`: LLM が生成・保守する Markdown wiki。
- `wiki/index.md`: 内容指向のカタログであり、最初のナビゲーション面。
- `wiki/log.md`: 時系列の追記専用アクティビティログ。
- `AGENTS.md` / `CLAUDE.md`: LLM エージェント向けの schema とワークフロー指示。

## Raw Manifest / Storage Policy

manifest がない通常の raw source は immutable とみなします。raw package manifest があり、
その `storage_policy` が更新可能な取得一式を示す場合だけ、限定された raw 更新を許可します。

現在許可される raw package `storage_policy` は次の通りです。

- `immutable`
- `latest_frame_data_mirror`
- `latest_battle_change_mirror`
- `updateable_web_page_capture`

更新可能な操作:

- 再取得
- 原文・元データを保つ取得物の差し替え
- manifest / metadata / validation / hash / review status の更新
- 表示証拠としての screenshot 再取得
- 対応する derived output の再生成

禁止される操作:

- 翻訳版を `raw/` に置く
- 要約版を `raw/` に置く
- 正規化済み置き換え版を `raw/` に置く
- LLM による説明文を `raw/` に置く
- source にない値を `raw/` へ補完する

`assets/manifest.json` のような補助 manifest は raw package の更新可否を決める正本ではありません。
補助 manifest は、親 raw package manifest の `storage_policy` と scope に従います。
新しい `storage_policy` を追加する場合は、先に `AGENTS.md`、`wiki/index.md`、
`wiki/log.md` で方針と入口を明記してください。

## ページ種別

- `wiki/sources/`: raw source ごとに 1 つの要約ページ。
- `wiki/concepts/`: 概念や再利用される考え方。
- `wiki/entities/`: 人物、企業、プロジェクト、ツール、論文、データセット、その他のエンティティ。
- `wiki/syntheses/`: 複数ページまたは複数ソースを横断する高次の分析。
- `wiki/questions/`: チャットから file back された、再利用しやすい回答済み質問。
- `wiki/outputs/`: 永続化するレポート、スライド、チャート、キャンバス、lint report、その他の成果物。
- `wiki/reviews/`: 個別の review finding、矛盾、古い主張、capture review、人間レビュー notes。
- `wiki/templates/`: 再利用するページテンプレート。

## Workflow Skill Dispatch

長い workflow 詳細は repo-local skill に置き、`AGENTS.md` には dispatch と境界ルールだけを置きます。
次の作業では該当 skill を使ってください。

- source ingest / re-ingest / wiki recompile after raw package update: `$sf6-source-ingest`
  (`.agents/skills/sf6-source-ingest/SKILL.md`)
- wiki-based question answering / source-only query / contamination-sensitive answer: `$sf6-wiki-query`
  (`.agents/skills/sf6-wiki-query/SKILL.md`)
- durable output / report / file-back to `wiki/questions/`, `wiki/syntheses/`, or `wiki/outputs/`: `$sf6-durable-output`
  (`.agents/skills/sf6-durable-output/SKILL.md`)
- wiki lint / health check / contradiction or stale-claim review: `$sf6-wiki-health-check`
  (`.agents/skills/sf6-wiki-health-check/SKILL.md`)
- wiki structure refactor / recompile / merge / split / rename / deprecate / hub creation / index redesign:
  `$sf6-wiki-refactor` (`.agents/skills/sf6-wiki-refactor/SKILL.md`)

skill はこのファイルの正本ルールを上書きしません。`raw/` 境界、source traceability、
`wiki/index.md` / `wiki/log.md` 更新、言語ポリシー、page type、Git diff review は
常にこのファイルを優先します。

## Lint Report Placement

wiki 全体の health check report や lint report は `wiki/outputs/lint/` に置いてよいです。
この report は reader-facing output として扱い、frontmatter は `type: output`、
`output_type: lint_report` にします。

人間レビューが必要な個別 finding、矛盾、stale claim、capture review は
`wiki/reviews/` に review note として置きます。`wiki/reviews/` の page は
frontmatter で `type: review` を使います。

## Lint Severity / Fix Policy

Lint / health check では、LLM が安全に直せる構造問題と、人間レビューが必要な事実問題を分けます。

### P0: Integrity

LLM が自動修正してよい項目です。

- broken wikilinks
- missing frontmatter
- missing index entry
- log 追記漏れ
- obvious Markdown formatting issue

### P1: Evidence

LLM は勝手に結論や値を変えず、`wiki/reviews/` に review note を作ります。

- 出典なしの重要主張
- source 間の矛盾
- stale claim
- row count mismatch
- validation failure
- raw manifest / source page / derived output の不一致

### P2: Structure

小規模で局所的なら LLM が修正してよい項目です。大規模な統合や意味判断が必要なら人間レビューに回します。
source claim を変更しない structural merge、backlink repair、index rebuild、deprecated marker 追加は
wiki maintenance として実行または具体的な refactor plan にしてよいです。

- orphan page
- duplicate concept
- missing backlinks
- concept / entity 不足

### P3: Quality

LLM が改善してよい項目です。

- weak summary
- aliases / tags 不足
- 読みにくい構成

## Citation / Evidence ルール

重要な主張、数値、日付、比較、評価、判断には、近くに根拠を置きます。
特に frame 値、row count、patch / update の説明、source freshness、validation status、
source confidence は、source page、raw、または derived output へ辿れる形にします。

根拠の優先順位:

1. `wiki/sources/` の source page
2. source page 内の `raw_path`
3. raw manifest / metadata / validation
4. derived JSON output
5. review note

主張は次の種別を意識して書き分けます。

- `source fact`: source に明示されている事実
- `derived fact`: raw または derived JSON から機械的に導いた事実
- `synthesis`: 複数 source を統合した判断
- `inference`: 根拠からの推論
- `hypothesis`: 仮説

`inference` と `hypothesis` は断定しないでください。derived output 由来の数値や比較は、
可能な限り source page または JSON path / manifest / validation へ戻れるようにします。

## Wiki Refactor / Recompile Policy

`wiki/` は LLM-maintained compiled knowledge であり、source ingest、query、lint、
output file-back によって継続的に再コンパイルされる層です。

LLM は、既存構成を保守的に温存するだけでなく、wiki の再利用性、検索性、根拠追跡、
一貫性、将来の query quality が上がる場合は `wiki/` の再編を積極的に提案し、
低リスクなものは実行してください。

### やってよい wiki refactor

- 古い summary の更新
- concept / entity / synthesis page の統合、分割、rename
- duplicate concept の merge
- overloaded page の split
- orphan page の hub 接続
- hub page / overview page / synthesis page の作成
- stale claim の `review-needed` 化
- contradiction の明示
- backlinks、aliases、tags、related links の再構成
- `wiki/index.md` の section 再編、entry 移動、summary 更新
- 有用な query result の `wiki/questions/`、`wiki/syntheses/`、`wiki/outputs/` への file-back
- question / output に溜まった再利用可能な知見の synthesis 昇格
- page status の `deprecated`、`contradicted`、`review-needed` 化
- `wiki/reviews/` に refactor plan または review note を作ること

### 禁止

- `raw/` source の翻訳、要約、正規化置換
- source にない値を raw / derived output に補完すること
- validation failure の値を正本扱いすること
- 根拠なしの重要 claim 追加
- source fact と inference / hypothesis を混ぜること
- official evidence と community evidence を黙って同格扱いすること
- 矛盾や stale claim を黙って消すこと
- `wiki/index.md` / `wiki/log.md` 更新なしの大きな wiki refactor
- 人間レビューが必要な factual judgment を勝手に確定すること

### Refactor trigger

次のいずれかを見つけたら、単なる報告で終わらせず、refactor plan または
実行可能な safe refactor を検討してください。

- 同じ概念を扱う page が複数ある
- source summary はあるが concept / entity / synthesis に統合されていない
- query が毎回同じ複数ページを読む必要がある
- index.md が navigation surface として長すぎる、または入口が分かりにくい
- orphan page がある
- important concept が何度も出るが独立 page がない
- old source に基づく summary が新しい source で古くなっている
- official / community / derived evidence が混ざっていて authority が分かりにくい
- question page に一般化できる知見がある
- output が孤立しており core wiki へ統合されていない
- lint report が同じ structural issue を繰り返している

### 大規模 refactor の扱い

大規模な merge / split / rename / directory restructure は、いきなり実行せず、
まず `wiki/reviews/` に refactor plan を作ってください。

refactor plan には次を含めます。

- 現在の問題
- 根拠となる source / wiki pages
- 変更対象 page
- 変更後の構成案
- 期待される利点
- 失う情報またはリスク
- 人間レビューが必要な点

低リスクな P0/P2 structural fix は実行してよいですが、source authority、値、結論、
page lifecycle に関わる判断は review note に残してください。

## Calculation Tool Gate

SF6 の frame、damage、gauge、juggle、distance などの計算 tool は、
厳密に確定した source fact または検証済み derived fact から再現できる計算式だけを実装対象にします。

tool 化してよいもの:

- source page、raw、derived JSON、または review accepted な根拠へ戻れる式
- 入力 ledger、適用条件、丸め / floor、minimum、version adjustment の順序が明文化できる式
- fixture で再計算でき、失敗時に fail closed できる式
- output に source path、source revision または input hash、calculator version、dependency version、
  authority / confidence を保持できる計算
- character-specific scaling、move-specific extra hit scaling、condition-specific multiplier は、
  route text から推測せず、source-backed ledger に `effective_scaling` と trace note として明示する計算
- combo damage ledger の `hits[]` は、1 damaging hit、source-backed に明示された 1 damage segment、
  または `damage_granularity: "move_total"` と `segment_type` で明示した full move total だけを表す。
  `hit_span: "10-16"` のような multi-hit subtotal row は deterministic `combo_damage` tool に入れない。
  Super Art などを full move total として扱う場合は、内部 hit split を modeled と誤読しない trace note を残す。

tool 化してはいけないもの:

- LLM が推測した式
- source にない内部仕様の補完
- 実機検証、公式 source、または accepted review がない仮説
- route text だけから非明示 hit、状態遷移、patch rollback、juggle condition、距離条件を推測する処理
- community numeric source を公式値または lab-verified value のように昇格する処理

SymPy などの数式 library は、LLM の暗算置き換えではなく repo 内の deterministic CLI / tool の実装依存として使います。
`Sympy-Skill` の一時的な利用だけに依存する計算結果は、CI、review、再実行、rollback ができないため
正本の derived output にしません。SymPy を導入する場合は `pyproject.toml` / lockfile、schema、fixture、
rounding policy、source hash gate を同時に整備します。
combo damage ledger では `attack_step` や `scaling_note` のような trace field を使い、
Mai `214HP (No Flame)` の extra scaling step など、見落としやすい source-backed 補正を結果に残します。

### Combo Damage Ledger Preflight

Exact combo damage を回答または fixture 化する前に、`wiki/concepts/combo-damage-ledger-protocol.md`
の preflight を通します。特に次の条件では route text の順番を damaging hit ledger として扱わず、
hit order proof を作るか、確定値として答えず fail closed します。

- `最速入力`、`微遅らせ`、`ディレイ` など timing-dependent な route。
- delayed projectile、設置、bomb、portal、SA projectile、install follow-up、multi-hit、juggle、距離依存、
  corner / height 依存を含む route。
- target combo follow-up、派生、manual / auto activation、入力強度、Modern / Classic が曖昧な route。
- starter / immediate / multiplier scaling、Super Art minimum、Drive Rush one-time penalty、
  character-specific extra scaling、condition multiplier が絡む route。

`最速入力` は hit order proof ではありません。startup、active、cancel window、scheduled projectile timing、
auto-hit timing から relative event table を作れる場合だけ derived fact として扱います。cancel anchor、
hitstop、距離、juggle height などが source から足りない場合は、training-mode 表示、動画 frame、
accepted review fixture などの validation がない限り、candidate ledger と不確実点までに留めます。

## Index / Log Update ルール

`wiki/index.md` は LLM が最初に読む navigation surface です。

新規 page を作成したら:

- 対応する section に 1 行追加する。
- 読者が用途を判断できる 1 行 summary を書く。
- status / source type / updated など、既存 section の列に合わせて metadata を更新する。

主要 page を大きく更新したら:

- index の summary や status が古くなっていないか確認する。
- related links や入口 page が変わった場合は index も更新する。

`wiki/log.md` は append-only の activity log です。明らかな typo や formatting mistake の修正を除き、
古い entry は履歴として残します。

各 entry は必要に応じて次の形にします。

```markdown
## [YYYY-MM-DD] <kind> | <title>
- 原本:
  - `raw/...`
- 作成:
  - `wiki/...`
- 更新:
  - `wiki/...`
- 検証:
  - ...
- メモ:
  - ...
- 未解決事項:
  - ...
```

質問ページは、読者向けの永続的な回答です。`wiki/questions/` には
`Filed-back updates`、変更ファイル、タスク要約、実装メモのような作業履歴セクションを
入れないでください。運用履歴は `wiki/log.md` に、レビュー findings は `wiki/reviews/`
に置いてください。

## 言語ポリシー

この wiki は日本語のメンテナーが読むことを前提にします。ユーザーが別言語を明示した場合、
またはソース忠実性のために英語が必要な場合を除き、`wiki/` ページ、永続回答、統合分析、
outputs、reviews、source summary の本文は日本語を優先してください。

`wiki/log.md` も読者向けの wiki 本文として扱い、見出し、作業分類、メモ、未解決事項は
日本語を優先してください。英語の workflow label を使う場合も日本語説明を併記し、
ファイル名、path、コマンド、field 名、status 値、公式用語は English/ASCII のまま維持してよいです。

構造識別子は安定してツールで扱いやすい形に保ちます。

- ディレクトリ名、ファイル名、slug、YAML frontmatter の key、field 名、tool 名、
  生成データ path は English/ASCII を使う。
- 元ソースの用語、公式名称、コマンド、入力表記、コード、引用文は元の言語を維持する。
- 検索上重要な語は、必要に応じて title、summary、`aliases`、`tags` に日本語と英語の両方を入れる。
  例: `Drive Rush` と `ドライブラッシュ`。
- `raw/` は原本保存層なので、元ソースの言語と内容を維持する。英語 source は英語のまま、
  日本語 source は日本語のまま保存する。
- `raw/` に翻訳・要約・正規化した置き換え版を作らない。翻訳、要約、説明、統合は
  `wiki/` layer で行い、raw source または source page に citation を戻す。
- 更新可能な raw 一式でも、置けるのは原文・元データを保つ取得物
  （HTML、wikitext、DOM、API response、screenshots、metadata、manifest、validation など）に限る。
- 既存ページを続けて編集する場合は、そのページの既存言語に従う。ただし読者の使いやすさが
  明確に上がる場合は、日本語へ寄せてよい。

## 絶対ルール

1. `raw/` 配下のファイルは原則変更しない。ただし manifest の `storage_policy` で最新ミラーまたは更新可能な取得一式と示されている raw 一式は更新可能。翻訳・要約・正規化した派生物は更新可能な raw 一式も含めて `raw/` に置かない。
2. 重複ページを作るより、既存 wiki ページの更新を優先する。
3. 重要な主張はすべて raw source または wiki source page へ辿れるようにする。
4. 不確実性は明示する。
5. 矛盾や古い主張は隠さず記録する。
6. 意味のある ingest、新規ページ、主要なページ更新の後は `wiki/index.md` を更新する。
7. ingest、query、output、lint pass、schema 変更の後は `wiki/log.md` に追記する。
8. 有用な query 結果は `wiki/questions/`、`wiki/syntheses/`、または `wiki/outputs/` に file back する。
9. 各タスクの最後に変更ファイルと未解決の質問を報告する。
10. domain-specific な運用や tools を追加する場合も、`raw/` / `wiki/` / schema の base pattern 境界を維持する。

## Ingest ワークフロー

ソースの ingest を依頼されたら:

`$sf6-source-ingest` skill を使ってください。skill には raw package 確認、source summary、
関連 wiki 更新、index/log 更新、open questions 報告の詳細を置きます。

## Query ワークフロー

質問への回答を依頼されたら:

`$sf6-wiki-query` skill を使ってください。skill には source-only query、evidence authority、
contamination-sensitive query、file-back 判断の詳細を置きます。

## Output ワークフロー

永続的な output の作成を依頼されたら:

`$sf6-durable-output` skill を使ってください。skill には output path、reader-facing 形式、
citation、file-back、index/log 更新の詳細を置きます。

## Lint / Health Check ワークフロー

wiki health check を依頼されたら:

`$sf6-wiki-health-check` skill を使ってください。skill には lint severity、safe fix、
review note 作成、全体 report 配置、index/log 更新の詳細を置きます。

## Obsidian Markdown

`wiki/` や Obsidian で閲覧する Markdown を作成・編集する場合は、repo-local
または local 環境で `$obsidian-markdown` skill が利用可能な場合は使ってよいです。
ただし必須依存ではありません。

ただし、このリポジトリの正本ルールはこのファイルに従います。`raw/` 原則不変と更新可能な raw 一式、
source traceability、`wiki/index.md` / `wiki/log.md` 更新、言語ポリシー、
page type、workflow は skill ではなく `AGENTS.md`、page type、wiki templates、既存 page style を優先します。

## Git とツール

- LLM が保守した wiki 変更のレビュー面として Git diff を使う。
- ローカルテキスト検索には `rg` を使う。
- JSON / JSONL から値を取得、集計、検証する場合は `jq` / `jq -e` を第一選択にする。repo-local `$jq-cli` skill が利用可能な場合は使ってよいが、必須依存にはしない。特に `wiki/outputs/data/`、raw manifest / metadata / validation、frame-data JSON、numeric derived output の数値・row count・条件検証では、ad hoc な text grep や one-off Python より `jq -e` / `jq` filter を優先する。
- Python を使ってよいのは、既存 repo tool の実行、複数 file をまたぐ domain-specific 生成・検証、または `jq` だけでは不自然な構造処理の場合に限る。その場合も重要な数値 claim では可能な範囲で `jq` による spot check を併用する。
- 既存の単純な file-based CLI tools だけを使う。
- base implementation では Obsidian CLI、Obsidian APIs、vector databases、graph databases、
  hosted RAG systems、MCP-first architecture に依存しない。
