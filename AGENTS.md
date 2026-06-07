# LLM Wiki エージェント指示

## コアモデル

このリポジトリは Karpathy-style の LLM-maintained knowledge base です。

人間はソースを選び、質問し、重要な変更をレビューし、方向性を決めます。
LLM は wiki を書き、リンクし、保守します。

ドメイン非依存の実装計画は [ROADMAP.md](ROADMAP.md) に従ってください。
基礎となる `raw/` / `wiki/` / schema パターンが実装されレビューされるまでは、
ドメイン固有のアーキテクチャを導入しないでください。

## レイヤー

- `raw/`: 不変のソース素材。`raw/` 配下のファイルは絶対に編集しない。
- `wiki/`: LLM が生成・保守する Markdown wiki。
- `wiki/index.md`: 内容指向のカタログであり、最初のナビゲーション面。
- `wiki/log.md`: 時系列の追記専用アクティビティログ。
- `AGENTS.md` / `CLAUDE.md`: LLM エージェント向けの schema とワークフロー指示。

## ページ種別

- `wiki/sources/`: raw source ごとに 1 つの要約ページ。
- `wiki/concepts/`: 概念や再利用される考え方。
- `wiki/entities/`: 人物、企業、プロジェクト、ツール、論文、データセット、その他のエンティティ。
- `wiki/syntheses/`: 複数ページまたは複数ソースを横断する高次の分析。
- `wiki/questions/`: チャットから file back された、再利用しやすい回答済み質問。
- `wiki/outputs/`: 永続化するレポート、スライド、チャート、キャンバス、その他の成果物。
- `wiki/reviews/`: lint 結果、矛盾、古い主張、レビュー notes。
- `wiki/templates/`: 再利用するページテンプレート。

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
- 既存ページを続けて編集する場合は、そのページの既存言語に従う。ただし読者の使いやすさが
  明確に上がる場合は、日本語へ寄せてよい。

## 絶対ルール

1. `raw/` 配下のファイルは絶対に変更しない。翻訳・要約・正規化した派生物も `raw/` に置かない。
2. 重複ページを作るより、既存 wiki ページの更新を優先する。
3. 重要な主張はすべて raw source または wiki source page へ辿れるようにする。
4. 不確実性は明示する。
5. 矛盾や古い主張は隠さず記録する。
6. 意味のある ingest、新規ページ、主要なページ更新の後は `wiki/index.md` を更新する。
7. ingest、query、output、lint pass、schema 変更の後は `wiki/log.md` に追記する。
8. 有用な query 結果は `wiki/questions/`、`wiki/syntheses/`、または `wiki/outputs/` に file back する。
9. 各タスクの最後に変更ファイルと未解決の質問を報告する。
10. 後の明示的な domain design step までは、base pattern をドメイン非依存に保つ。

## Ingest ワークフロー

ソースの ingest を依頼されたら:

1. このファイルを読む。
2. `wiki/index.md` を読む。
3. `wiki/log.md` の最近のエントリを読む。
4. 指定された raw source を読む。
5. `raw/` は編集しない。翻訳・要約・正規化もしない。
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
8. `wiki/index.md` を更新する。
9. `wiki/log.md` に追記する。
10. 変更ファイルと人間レビューが必要な項目を報告する。

## Obsidian Markdown

`wiki/` や Obsidian で閲覧する Markdown を作成・編集する場合は、repo-local
skill として `.agents/skills/obsidian-markdown/SKILL.md` に配置した
`$obsidian-markdown` skill を使ってよいです。Codex の skill は、明示的には
`$obsidian-markdown` として呼び出し、暗黙的には task が skill の `description` に
合う場合に選択されます。

ただし、このリポジトリの正本ルールはこのファイルに従います。`raw/` 不変、
source traceability、`wiki/index.md` / `wiki/log.md` 更新、言語ポリシー、
page type、workflow は skill ではなく `AGENTS.md` / `CLAUDE.md` を優先します。

## Git とツール

- LLM が保守した wiki 変更のレビュー面として Git diff を使う。
- ローカルテキスト検索には `rg` を使う。
- 既存の単純な file-based CLI tools だけを使う。
- base implementation では Obsidian CLI、Obsidian APIs、vector databases、graph databases、
  hosted RAG systems、MCP-first architecture に依存しない。
