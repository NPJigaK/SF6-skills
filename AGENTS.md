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

1. このファイルを読む。
2. `wiki/index.md` を読む。
3. `wiki/log.md` の最近のエントリを読む。
4. 指定された raw source を読む。
5. `raw/` は原則編集しない。例外として、指定 source が更新可能な raw 一式（例: frame-data 最新ミラー、battle-change 最新ミラー、web-page capture）に属する場合は、取得、再取得、manifest 補正として該当する raw 一式を更新してよい。翻訳・要約・正規化はしない。
6. `wiki/sources/` に 1 つのページを作るか更新する。
7. 関連する concept、entity、synthesis ページを更新する。
8. 新規ページは、有用で重複でない場合にだけ作る。
9. backlink と source reference を追加する。
10. 矛盾、古い主張、不確実性を明示する。
11. `wiki/index.md` を更新する。
12. `wiki/log.md` に追記する。
13. 変更ファイルと open questions を報告する。

## Query ワークフロー

質問への回答を依頼されたら:

1. 最初に `wiki/index.md` を読む。
2. index だけで不十分な場合のみ wiki を検索する。
3. 関連する source、concept、entity、synthesis、question、output ページを読む。
4. wiki page または source page への citation 付きで回答する。
5. 不確実性と不足している evidence を明確に述べる。
6. 回答が永続的に有用なら、`wiki/questions/`、`wiki/syntheses/`、または `wiki/outputs/` に保存する。
7. 保存する question page は再利用可能な回答に集中させる。file-back の詳細や changed files は
   question page ではなく `wiki/log.md` に置く。
8. ページを作成または大きく変更した場合は `wiki/index.md` を更新する。
9. `wiki/log.md` に追記する。
10. 変更ファイルと未解決の質問を報告する。

## Output ワークフロー

永続的な output の作成を依頼されたら:

1. `wiki/index.md` を読む。
2. 関連する wiki page と source page を読む。
3. 要求された output を `wiki/outputs/` 配下に作成する。
4. 関連する wiki/source page を citation する。
5. 可能な限り plain Markdown として読みやすく保つ。
6. `wiki/index.md` を更新する。
7. `wiki/log.md` に追記する。
8. 変更ファイルを報告する。

## Lint / Health Check ワークフロー

wiki health check を依頼されたら:

1. このファイルを読む。
2. `wiki/index.md` を読む。
3. `wiki/log.md` の最近のエントリを読む。
4. broken wikilinks、orphan pages、duplicate pages、missing index entries、
   missing frontmatter、missing backlinks、contradictions、stale claims、
   uncited important claims、weak summaries、missing concept/entity pages、
   data gaps、suggested next sources/questions を確認する。
5. 安全に直せる構造上の問題を修正する。
6. 事実を捏造しない。
7. 不確実な事実問題は `wiki/reviews/` に review note を作る。
8. 全体 report を保存する場合は `wiki/outputs/lint/` に `type: output`, `output_type: lint_report` として置く。
9. `wiki/index.md` を更新する。
10. `wiki/log.md` に追記する。
11. 変更ファイルと人間レビューが必要な項目を報告する。

## Obsidian Markdown

`wiki/` や Obsidian で閲覧する Markdown を作成・編集する場合は、repo-local
skill として `.agents/skills/obsidian-markdown/SKILL.md` に配置した
`$obsidian-markdown` skill を使ってよいです。Codex の skill は、明示的には
`$obsidian-markdown` として呼び出し、暗黙的には task が skill の `description` に
合う場合に選択されます。

ただし、このリポジトリの正本ルールはこのファイルに従います。`raw/` 原則不変と更新可能な raw 一式、
source traceability、`wiki/index.md` / `wiki/log.md` 更新、言語ポリシー、
page type、workflow は skill ではなく `AGENTS.md` / `CLAUDE.md` を優先します。

## Git とツール

- LLM が保守した wiki 変更のレビュー面として Git diff を使う。
- ローカルテキスト検索には `rg` を使う。
- 既存の単純な file-based CLI tools だけを使う。
- base implementation では Obsidian CLI、Obsidian APIs、vector databases、graph databases、
  hosted RAG systems、MCP-first architecture に依存しない。
