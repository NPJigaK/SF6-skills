# Karpathy-style LLM Wiki ロードマップ

ステータス: draft roadmap
作成日: 2026-05-26
範囲: ドメイン非依存の LLM Knowledge Base / LLM Wiki 設計

## 目的

このロードマップは、Karpathy-style の LLM Knowledge Base / LLM Wiki を
ドメイン非依存で実装するための計画を定義します。

この文書には、意図的にドメイン固有のアーキテクチャ、schema、回答ルール、
データモデル、product behavior を含めません。ドメイン固有の設計は、この
base pattern が実装されレビューされた後にだけ行います。

目標は、一般的な app、database-backed RAG system、domain-specific runtime ではありません。
目標は plain-file knowledge repository です。

```text
Human curates sources and asks questions.
LLM compiles, writes, links, maintains, lints, searches, and outputs.
Obsidian is the frontend.
Markdown files are the durable memory.
CLI tools are the LLM's hands.
```

既存実装との互換性は、このロードマップの目的ではありません。
Git history を rollback mechanism として使います。

## 出典

このロードマップは、ユーザーの「Karpathy式 LLM Knowledge Base / LLM Wiki
設計実装まとめ」と、現在公開されている Karpathy `llm-wiki` gist に基づきます。

出典リンク:

- [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Farzapedia / file collection memory](https://x.com/karpathy/status/2040572272944324650)
- [LLM Knowledge Bases post](https://x.com/karpathy/status/2039805659525644595)
- [Manual incremental compilation reply](https://x.com/karpathy/status/2039812403962253744)
- [Obsidian CLI reply](https://x.com/karpathy/status/2039814066575917263)

## 設計境界

最初の実装は Karpathy-style の base pattern 内に留めます。

- 汎用の `raw/`
- 汎用の `wiki/`
- 汎用の schema files
- 汎用の `index.md`
- 汎用の `log.md`
- 汎用の ingest / query / output / lint workflows
- 任意の小さな file-based CLI tools
- 任意の Obsidian viewing workflow

最初の実装に含めてはいけないもの:

- ドメイン固有の page types
- ドメイン固有の answer policy
- ドメイン固有の validators
- ドメイン固有の structured databases
- ドメイン固有の runtime behavior
- ドメイン固有の UI
- ドメイン固有の retrieval architecture
- product-specific automation

## Karpathy が述べた中核

### 1. LLM Wiki は通常の RAG ではない

通常の RAG は query 時に raw documents から chunk を retrieve し、毎回回答を再構成します。

LLM Wiki pattern は違います。

- raw sources を curated collection に追加する
- LLM が新しい source を読む
- LLM が source を persistent Markdown wiki に compile する
- LLM が entity pages、concept pages、summaries、contradictions、cross-references を更新する
- 知識は質問ごとに再導出されるのではなく、wiki の中で蓄積される

wiki は persistent で compounding な artifact です。

### 2. 3 つのレイヤー

アーキテクチャは 3 レイヤーです。

```text
1. Raw sources
2. The wiki
3. The schema
```

`raw/` は immutable source of truth です。LLM は raw files を読みますが、変更しません。

`wiki/` は LLM-generated Markdown files のディレクトリです。LLM はこの layer を所有し、
ページ作成、ページ更新、cross-reference の保守、wiki の一貫性維持を行います。

schema は `AGENTS.md` や `CLAUDE.md` のようなファイルです。wiki がどう構造化され、
どの workflow に従うかを LLM に伝えます。

### 3. 役割分担

Human:

- sources を curate する
- 何が重要かを選ぶ
- 質問する
- 重要な変更をレビューする
- 分析の方向を決める
- Git diffs を確認する

LLM:

- sources を要約する
- pages を作る
- pages を更新する
- cross-references を保守する
- `index.md` を更新する
- `log.md` に追記する
- wiki から質問に答える
- 有用な回答を wiki に file back する
- health checks を実行する
- outputs を作る

### 4. Obsidian は IDE

Obsidian は、人間が file collection を閲覧するための frontend です。

- pages を読む
- wikilinks を辿る
- graph view を見る
- outputs を見る
- Marp や Dataview など任意 plugin を使う

Obsidian は knowledge base 本体ではありません。knowledge base 本体は plain files のディレクトリです。

### 5. 完全自動 ingest から始めない

初期 ingest は、人間を loop に入れて source-by-source で行います。

batch ingest やより強い automation は、schema、page shape、review expectation が安定してから検討します。

## 実装判断

以下は Karpathy が普遍要件として固定したものではありません。ただし pattern を保つための実践的判断です。

### 1. Plain Directory Structure

小さく明快なディレクトリツリーを使います。

```text
llm-wiki/
  AGENTS.md
  CLAUDE.md
  README.md

  raw/
    articles/
    papers/
    repos/
    datasets/
    images/
    assets/
    transcripts/
    notes/

  wiki/
    index.md
    log.md

    sources/
    concepts/
    entities/
    syntheses/
    questions/
    outputs/
      reports/
      slides/
      charts/
      canvases/
    reviews/
    templates/

  tools/
    kb_search.py
    kb_status.py
    kb_lint.py
    kb_render.py
    kb_ingest_status.py

  scripts/
    normalize_web_clip.py
    extract_pdf_notes.py
    download_assets.py
```

最小実用版は次の通りです。

```text
raw/
wiki/
AGENTS.md
CLAUDE.md
README.md
wiki/index.md
wiki/log.md
```

### 2. 有用な場所で frontmatter を使う

YAML frontmatter は、人間、LLM、任意の Obsidian Dataview query にとって有用です。
単純で編集しやすい形に保ちます。

### 3. Tools は小さく保つ

CLI tools は、LLM が file tree 上で作業するための補助です。source of truth にしてはいけません。

まずは単純な file-based tooling から始めます。base implementation では vector databases、
graph databases、hosted RAG systems、MCP-first architecture を導入しません。

### 4. Git を安全柵にする

wiki は単なる files なので、Git が次を提供します。

- history
- diffs
- branching
- rollback
- review

LLM-maintained wiki changes は Git diff でレビューします。

### 5. 言語方針

この repository は日本語のメンテナーが読むため、wiki 本文、永続回答、統合分析、レビュー、
source summary は日本語を優先します。

一方で、構造識別子は安定性と検索性のため English/ASCII を保ちます。

- directory names
- filenames
- slugs
- YAML frontmatter keys
- field names
- generated data paths
- commands

重要語は必要に応じて日本語と英語を併記し、`aliases` や `tags` にも入れます。

## Raw Layer 設計

`raw/` は人間が curate した source material を保存します。

例:

```text
raw/articles/
raw/papers/
raw/repos/
raw/datasets/
raw/images/
raw/assets/
raw/transcripts/
raw/notes/
```

ルール:

- LLM は `raw/` 配下のファイルを編集してはいけない。
- `raw/` は原本保存層なので、元ソースの言語と内容を維持する。
- 英語 source は英語のまま、日本語 source は日本語のまま保存する。
- 翻訳・要約・正規化した置き換え版を `raw/` に作らない。
- 日本語化、要約、説明、統合は `wiki/` layer で行い、raw source または source page に citation を戻す。
- raw filename は date、source、topic が十分に分かる形にする。
- 重要な画像はローカル保存する。
- source metadata は frontmatter または sidecar file に置いてよい。
- wiki pages は raw sources へ link back する。

raw source frontmatter 例:

```markdown
---
type: raw_source
source_type: article
title: ""
author: ""
original_url: ""
captured_at: YYYY-MM-DD
status: raw
aliases: []
---
```

## Wiki Layer 設計

`wiki/` は LLM-generated、LLM-maintained の compiled knowledge を保存します。

推奨ディレクトリ:

```text
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/syntheses/
wiki/questions/
wiki/outputs/
wiki/reviews/
wiki/templates/
```

ルール:

- 重複ページを作るより既存ページの更新を優先する。
- 重要な主張はすべて source へ traceable にする。
- 不確実性を明示する。
- 矛盾や古い主張を隠さず記録する。
- backlinks と cross-references を保守する。
- 有用な query results を wiki に戻す。
- 意味のある page changes の後は `wiki/index.md` を更新する。
- ingest、query、output、lint、schema work の後は `wiki/log.md` に追記する。

## Schema Layer 設計

`AGENTS.md` と `CLAUDE.md` は、agent-facing の operating constitution です。

定義すべき内容:

- core model
- raw/wiki/schema layer boundaries
- page types
- naming conventions
- wikilink conventions
- frontmatter conventions
- ingest workflow
- query workflow
- output workflow
- lint workflow
- index update rules
- log append rules
- citation/source handling
- uncertainty handling
- contradiction handling
- CLI tool usage
- Git diff reporting

最小 schema rules:

```markdown
# LLM Wiki エージェント指示

## コアモデル

このリポジトリは LLM-maintained knowledge base です。

人間は sources を curate し、質問し、重要な変更をレビューし、方向性を決めます。
LLM は wiki を書き、保守します。

## レイヤー

- `raw/`: 不変の source material。`raw/` 配下は絶対に編集しない。
- `wiki/`: LLM-generated、LLM-maintained の Markdown wiki。
- `wiki/index.md`: 内容指向の catalog。
- `wiki/log.md`: 時系列の追記専用 activity log。

## 絶対ルール

1. `raw/` を絶対に変更しない。
2. 重複ページより既存 wiki ページの更新を優先する。
3. 重要な主張はすべて source へ traceable にする。
4. 不確実性を明示する。
5. 意味のある ingest または new page の後は `wiki/index.md` を更新する。
6. ingest、query、output、lint pass の後は `wiki/log.md` に追記する。
7. 有用な query results は wiki に file back する。
8. 各タスクの最後に変更ファイルをすべて報告する。
```

## 特別なファイル

### `wiki/index.md`

`index.md` は content-oriented です。wiki pages を links、one-line summaries、optional metadata とともに catalog します。

LLM は質問に答える時、最初にこのファイルを読みます。

推奨形:

```markdown
# Wiki Index（内容カタログ）

## Sources（ソース）

| Page | Summary | Date | Source type | Status |
|---|---|---:|---|---|

## Concepts（概念）

| Page | Summary | Related |
|---|---|---|

## Entities（エンティティ）

| Page | Summary | Type |
|---|---|---|

## Syntheses（統合分析）

| Page | Summary | Updated |
|---|---|---:|

## Questions（質問）

| Page | Question | Summary | Updated |
|---|---|---|---:|

## Outputs（成果物）

| Page | Type | Summary | Updated |
|---|---|---|---:|

## Reviews（レビュー）

| Page | Review type | Summary | Status |
|---|---|---|---|
```

ルール:

- 新しい wiki pages を index に追加する。
- major page updates の後は summary を更新する。
- index を navigation に有用な状態に保つ。
- search tools は index だけで不十分な場合にだけ使う。

### `wiki/log.md`

`log.md` は chronological で append-only です。

推奨形:

```markdown
# Wiki Log（活動ログ）

## [YYYY-MM-DD] schema | LLM Wiki を初期化
- 作成:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - raw/wiki/schema structure を初期化した。

## [YYYY-MM-DD] ingest | <Source Title>
- Raw source（原資料）:
  - `raw/articles/<file>.md`
- 作成:
  - `wiki/sources/<source>.md`
- 更新:
  - `wiki/index.md`
- 未解決の質問:
  - ...
```

ルール:

- 追記専用にする。
- obvious formatting mistakes の修正を除き、古い entries を書き換えない。
- ingest、query、output、lint、schema updates を記録する。
- Unix tools で recent activity を parse しやすいよう、entry prefix を一貫させる。

## ページテンプレート

### ソース要約ページ

```markdown
---
type: source
source_type: article
title: ""
author: ""
raw_path: ""
original_url: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: high
tags: []
aliases: []
related_concepts: []
related_entities: []
---

# ソース: <タイトル>

## 1行要約

...

## 重要ポイント

1. ...
2. ...
3. ...

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| ... | ... | high | ... |

## 関連概念

- [[concepts/...]]

## 関連エンティティ

- [[entities/...]]

## 既存 wiki との矛盾または更新

- ...

## 未解決の質問

- ...

## ソースメモ

- Raw file: `raw/...`
- Original URL: ...
```

### 概念ページ

```markdown
---
type: concept
title: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: medium
sources: []
related: []
aliases: []
tags: []
---

# <概念>

## 要約

...

## 定義

...

## なぜ重要か

...

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| ... | ... | ... |

## 関連

- [[concepts/...]]
- [[entities/...]]

## 矛盾 / 注意点

...

## 未解決の質問

...
```

### エンティティページ

```markdown
---
type: entity
entity_type: person | company | project | tool | paper | dataset | other
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
sources: []
related: []
aliases: []
tags: []
---

# <エンティティ>

## 要約

...

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| ... | ... | ... |

## 関連する主張

...

## 関連概念

...

## 未解決の質問

...
```

### 統合分析ページ

```markdown
---
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
sources: []
related: []
aliases: []
tags: []
---

# <統合分析タイトル>

## 要約

...

## 中心論点

...

## 根拠

| 論点 | 根拠ソース | 信頼度 |
|---|---|---|
| ... | ... | ... |

## 比較

| 観点 | A | B | メモ |
|---|---|---|---|
| ... | ... | ... | ... |

## 含意

...

## 未解決の質問

...

## 更新候補ページ

- [[concepts/...]]
```

### 質問ページ

```markdown
---
type: question
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
question: ""
sources: []
related: []
aliases: []
---

# 質問: <質問>

## 短い答え

...

## 根拠

...

## 説明

...

## 注意 / 不確実性

...
```

### Lint レビュー

```markdown
---
type: review
review_type: lint
created: YYYY-MM-DD
status: open
aliases: []
---

# Wiki ヘルスチェック - YYYY-MM-DD

## 要約

...

## 構造上の問題

### 壊れたリンク

...

### 孤立ページ

...

### index 未掲載ページ

...

## 知識上の問題

### 矛盾

...

### 古い主張

...

### Citation のない主張

...

## 不足している概念

...

## 推奨される新規 sources

...

## 次に調べる質問の候補

...

## 実施した変更

...

## 人間レビューが必要な項目

...
```

## ワークフロー

### Ingest ワークフロー

目的: 新しい raw source を 1 つ wiki に統合する。

手順:

1. Human が `raw/` に source を 1 つ追加する。
2. LLM が `AGENTS.md` または `CLAUDE.md` を読む。
3. LLM が `wiki/index.md` を読む。
4. LLM が最近の `wiki/log.md` entries を読む。
5. LLM が新しい raw source を読む。
6. LLM が `wiki/sources/` に source summary を作る。
7. LLM が関連する concept、entity、synthesis pages を探す。
8. LLM が必要に応じて既存 pages を更新する。
9. LLM が有用な場合にだけ新しい concept または entity pages を作る。
10. LLM が contradictions、stale claims、uncertainty を記録する。
11. LLM が backlinks を追加する。
12. LLM が `wiki/index.md` を更新する。
13. LLM が `wiki/log.md` に追記する。
14. LLM が changed files と open questions を報告する。
15. Human が Git diff をレビューする。

初期 prompt:

```text
この source を LLM Wiki に ingest してください。

ソース:
raw/<path>

AGENTS.md に厳密に従ってください。

要件:
- raw/ を編集しない。
- 最初に wiki/index.md を読む。
- wiki/log.md の最近の entries を読む。
- wiki/sources/ に source summary を作る。
- 関連する concept/entity/synthesis pages を更新する。
- 重複ページを作るより既存ページの更新を優先する。
- backlinks を追加する。
- contradictions、stale claims、uncertainty を明示する。
- wiki/index.md を更新する。
- wiki/log.md に追記する。
- changed files と open questions を報告する。
```

バッチ方針:

```text
0-20 sources:
  human review 付きで 1 source ずつ

20-100 sources:
  patterns が安定した後に small batches のみ

100+ sources:
  index.md だけでは不足する場合、より強い search tooling を検討する
```

### Query ワークフロー

目的: compiled wiki から質問に答え、有用な結果を保存する。

手順:

1. LLM が `wiki/index.md` を読む。
2. 必要なら LLM が wiki を検索する。
3. LLM が関連する source、concept、entity、synthesis pages を読む。
4. LLM が wiki/source pages への citation 付きで answer を synthesis する。
5. 必要に応じて output form を選ぶ。
   - Markdown report
   - comparison table
   - Marp slide deck
   - matplotlib chart
   - canvas
6. LLM が durable answers を `wiki/questions/`、`wiki/syntheses/`、または `wiki/outputs/` に file back する。
7. LLM が `wiki/index.md` を更新する。
8. LLM が `wiki/log.md` に追記する。

初期 prompt:

```text
wiki を使って次の質問に答えてください。

質問:
<question>

ワークフロー:
1. 最初に wiki/index.md を読む。
2. 必要なら wiki を検索する。
3. 関連する source、concept、entity、synthesis pages を読む。
4. wiki/source pages への citation 付きで回答する。
5. 回答が有用なら次へ file back する:
   - Q&A は wiki/questions/
   - 永続分析は wiki/syntheses/
   - visual または presentation output は wiki/outputs/
6. wiki/index.md と wiki/log.md を更新する。
7. changed files と unresolved questions を報告する。
```

### Output ワークフロー

目的: 有用な結果を durable かつ viewable にする。

出力先:

```text
wiki/outputs/reports/
wiki/outputs/slides/
wiki/outputs/charts/
wiki/outputs/canvases/
```

初期 prompt:

```text
wiki から durable output を作成してください。

トピック:
<topic>

出力形式:
Markdown report / Marp slide deck / matplotlib chart / comparison table

出力 path:
wiki/outputs/<type>/<filename>

要件:
- 関連する wiki/source pages を citation する。
- Obsidian で有用に読むことができる形にする。
- wiki に file back する。
- index.md と log.md を更新する。
```

### Lint / Health Check ワークフロー

目的: wiki が成長しても健全に保つ。

Checks:

```text
Structural:
  - broken wikilinks
  - orphan pages
  - duplicate pages
  - pages missing from index.md
  - pages with missing frontmatter
  - pages with missing backlinks

Knowledge:
  - contradictions between pages
  - stale claims superseded by newer sources
  - uncited important claims
  - weak summaries
  - concepts mentioned repeatedly but lacking pages
  - entities without pages
  - missing cross-references

Research:
  - data gaps
  - web-searchable missing facts
  - new article candidates
  - further questions to investigate
```

初期 prompt:

```text
wiki health check を実行してください。

ワークフロー:
1. AGENTS.md / CLAUDE.md を読む。
2. wiki/index.md と最近の wiki/log.md entries を読む。
3. 次を確認する:
   - contradictions
   - stale claims
   - orphan pages
   - missing cross-references
   - important concepts without pages
   - missing source citations
   - data gaps
   - broken links
4. 安全な structural issues を修正する。
5. 不確実な factual issues は推測せず review note を作る。
6. findings を wiki/reviews/<date>-health-check.md に書く。
7. wiki/index.md と wiki/log.md を更新する。
8. next questions と next sources を提案する。
```

## CLI 設計

CLI tools は LLM の optional helpers です。knowledge base ではありません。

Initial commands:

```bash
kb search "query"
kb status
kb recent --n 5
kb lint
kb unprocessed
```

Decision status:

| Tool | Status | Basis |
|---|---|---|
| search CLI | recommended | LLM helper として最も明確に有用 |
| status CLI | implementation judgment | maintenance に有用 |
| recent CLI | implementation judgment | parseable な `log.md` を読む |
| lint CLI | implementation judgment | health checks をまとめる |
| render CLI | optional | output generation をまとめる |
| qmd | later option | Markdown search needs が増えたら有用 |
| MCP | deferred | 選んだ tool が cleanly expose する場合のみ有用 |

最初から導入しないもの:

- Obsidian CLI
- vector DB
- graph DB
- hosted RAG
- MCP-first architecture
- fine-tuning

## Obsidian 設計

Obsidian は viewer 兼 IDE-like frontend として推奨します。

推奨 settings:

```text
Attachment folder path:
  raw/assets/

Useful core feature:
  Graph view

Useful plugins:
  Web Clipper
  Marp
  Dataview
```

ルール:

- correctness を Obsidian に依存させない。
- Obsidian CLI を必須にしない。
- Obsidian APIs を必須にしない。
- ordinary file tools で repository を読める状態に保つ。

## Git 設計

Git の用途:

- version history
- rollback
- branch-based experiments
- collaboration
- LLM edits の review

推奨 operations:

```bash
git status
git diff
git add raw/ wiki/ AGENTS.md CLAUDE.md README.md
git commit -m "Initialize LLM Wiki"
```

ingest 後:

```bash
git status
git diff
git add raw/ wiki/
git commit -m "Ingest <source title>"
```

lint 後:

```bash
git status
git diff
git add wiki/
git commit -m "Run wiki health check"
```

## スケール計画

### 小規模

使うもの:

- `index.md`
- `log.md`
- source summaries
- `rg`
- simple search CLI

避けるもの:

- vector DB
- graph DB
- MCP-first design
- complex RAG pipelines

### 中規模

検討するもの:

- qmd または別の local Markdown search tool
- BM25/vector hybrid search
- より強い frontmatter conventions
- periodic lint
- より強い index conventions

### 大規模

検討するもの:

- dedicated search layer
- page-level metadata discipline
- source confidence tracking
- batch ingest queues
- review workflows
- branch / PR process
- possible vector search
- possible MCP
- possible evaluation set

core は変わりません。raw sources を persistent wiki に compile します。

## Fine-Tuning / Synthetic Data

fine-tuning と synthetic data は将来の探索であり、MVP requirements ではありません。

推奨順序:

1. `raw/` と `wiki/` を作る。
2. ingest / query / lint を手動で回す。
3. `index.md` と `log.md` を安定させる。
4. 必要なら simple search CLI を追加する。
5. 有用なら evaluation questions を作る。
6. synthetic data を検討する。
7. wiki が育った後にだけ fine-tuning を検討する。

## セキュリティとプライバシー

汎用 LLM Wiki でも source sensitivity は明示すべきです。

Optional frontmatter:

```markdown
---
sensitivity: public | internal | private
share_with_cloud_llm: true
contains_personal_data: false
---
```

ルール:

- sensitive raw sources に label を付ける。
- sensitive wiki pages に label を付ける。
- 許可されていない sources を cloud LLMs に送らない。
- local-only material を public remotes に入れない。
- screenshots、transcripts、personal notes は慎重にレビューする。

## 明示的な Non-Goals

- base layer に domain-specific architecture を入れること。
- day one から complete automation を行うこと。
- Obsidian CLI dependency。
- Obsidian API dependency。
- app-first design。
- database-first design。
- day one から vector DB を使うこと。
- day one から graph DB を使うこと。
- MCP-first design。
- day one から fine-tuning を行うこと。
- 人間が traditional notes として wiki を手動保守すること。
- 有用な回答を chat history にだけ残すこと。

## MVP ロードマップ

### Phase 0: Pure Pattern Lock

目的: 特定ドメインへ適用する前に、domain-independent Karpathy-style design を受け入れる。

タスク:

- この roadmap をレビューする。
- base pattern に domain-specific logic が入らないことを確認する。
- この roadmap が現在の実装計画を supersede するか決める。

受け入れ条件:

- `raw/`、`wiki/`、schema だけが architectural layers である。
- `index.md` と `log.md` は mandatory。
- ingest、query、output、lint だけが workflows。
- CLI tools は optional helpers。
- domain-specific page types または answer policies が存在しない。

検証:

```bash
git diff --check
```

### Phase 1: Base Repository Scaffold

目的: plain-file LLM Wiki structure を作る。

タスク:

- `raw/` を作る。
- `wiki/` を作る。
- `wiki/index.md` を作る。
- `wiki/log.md` を作る。
- `wiki/templates/` を作る。
- generic templates を追加する。
- `README.md` を追加する。

受け入れ条件:

- repo は Obsidian なしで読める。
- repo は Obsidian で有用に使える。
- domain-specific files が導入されていない。
- app runtime が導入されていない。

検証:

```bash
git diff --check
find raw wiki -maxdepth 3 -type f | sort
```

### Phase 2: Schema Files

目的: LLM agent behavior を明示する。

タスク:

- `AGENTS.md` を書く。
- `CLAUDE.md` を書く。
- layer boundaries を定義する。
- page types を定義する。
- workflows を定義する。
- index and log rules を定義する。
- uncertainty and citation rules を定義する。
- Git diff reporting を定義する。

受け入れ条件:

- schema files は `raw/` 編集を禁止する。
- schema files は query 時に最初に `wiki/index.md` を読むことを要求する。
- schema files は meaningful work 後に `wiki/log.md` へ追記することを要求する。
- schema files は useful answers を wiki へ file back することを要求する。

検証:

```bash
git diff --check
rg "raw/" AGENTS.md CLAUDE.md
rg "wiki/index.md" AGENTS.md CLAUDE.md
rg "wiki/log.md" AGENTS.md CLAUDE.md
```

### Phase 3: First Manual Ingest

目的: single-source compilation を証明する。

タスク:

- Human が generic source を 1 つ `raw/` に追加する。
- LLM が source summary を 1 つ作る。
- LLM が関連する concept/entity/synthesis pages を作るか更新する。
- LLM が index を更新する。
- LLM が log に追記する。
- Human が diff をレビューする。

受け入れ条件:

- raw source は変更されていない。
- source summary は raw source に link している。
- compiled wiki page が少なくとも 1 つ存在する。
- index と log が更新されている。

検証:

```bash
git diff --check
rg "raw/" wiki/sources wiki/index.md wiki/log.md
```

### Phase 4: First Query And File-Back

目的: 質問が durable knowledge として compounding することを証明する。

タスク:

- wiki から答えられる質問を 1 つする。
- LLM が citations 付きで答える。
- LLM が有用な回答を `wiki/questions/` または `wiki/syntheses/` に保存する。
- LLM が index と log を更新する。

受け入れ条件:

- 回答が wiki/source pages を cite している。
- filed-back page は chat history の外でも有用。
- index と log が更新されている。

検証:

```bash
git diff --check
rg "type: question|type: synthesis" wiki/questions wiki/syntheses
rg "questions/|syntheses/" wiki/index.md wiki/log.md
```

### Phase 5: First Health Check

目的: maintenance workflow を証明する。

タスク:

- wiki health check を実行する。
- 安全な structural issues を修正する。
- 不確実な factual issues を `wiki/reviews/` に書く。
- next sources と next questions を提案する。
- index と log を更新する。

受け入れ条件:

- review page が存在する。
- broken links と missing index entries がチェックされている。
- uncertain claims を推測していない。
- index と log が更新されている。

検証:

```bash
git diff --check
rg "type: review" wiki/reviews
rg "health" wiki/log.md
```

### Phase 6: Small CLI

目的: optional file-based helper tools を追加する。

タスク:

- simple search を追加する。
- status を追加する。
- recent log reader を追加する。
- basic lint を追加する。
- unprocessed raw source report を追加する。

受け入れ条件:

- tools は plain files 上で動く。
- tools は source of truth にならない。
- tools は Obsidian を要求しない。
- tools は vector DB や hosted services を要求しない。

検証:

```bash
python tools/kb_status.py
python tools/kb_search.py "query"
python tools/kb_lint.py
```

### Phase 7: Scale Review

目的: simple files と index がまだ十分か判断する。

トリガー:

- sources が約 100
- wiki pages が数百
- search failures が繰り返される
- lint friction が繰り返される

タスク:

- search quality をレビューする。
- index usefulness をレビューする。
- log usefulness をレビューする。
- qmd または別の local Markdown search layer を追加するか決める。
- decision を `wiki/reviews/` に記録する。

受け入れ条件:

- search escalation が evidence-based。
- new tools が raw/wiki/schema boundaries を保つ。
- domain-specific assumptions が追加されていない。

## 意思決定表

| Item | Decision | Basis |
|---|---:|---|
| `raw/` | required | immutable source layer |
| `wiki/` | required | LLM-generated compiled Markdown wiki |
| `AGENTS.md` | required | Codex schema |
| `CLAUDE.md` | recommended | Claude Code schema |
| `wiki/index.md` | required | content-oriented catalog |
| `wiki/log.md` | required | chronological append-only log |
| Obsidian app | recommended | human IDE frontend |
| Obsidian CLI | rejected | simple-file core の一部ではない |
| Git | strongly recommended | version history and review |
| search CLI | recommended | LLM helper |
| lint CLI | optional | health check packaged as tool |
| render CLI | optional | output generation packaged as tool |
| qmd | later option | 必要になった時の local Markdown search |
| MCP | deferred | 選んだ tool が useful にする場合だけ |
| vector DB | deferred | small scale では不要 |
| fine-tuning | future exploration | MVP ではない |
| full automation | rejected for MVP | early human-in-loop ingest |

## Base Pattern の完了定義

base pattern は次を満たした時に complete です。

- `raw/` が存在し、immutable として扱われている。
- `wiki/` が存在し、LLM-maintained である。
- `AGENTS.md` が存在する。
- `CLAUDE.md` が存在する、または明示的に deferred されている。
- `wiki/index.md` が存在し、保守されている。
- `wiki/log.md` が存在し、append-only である。
- source が 1 つ manually ingested されている。
- 有用な query が 1 つ wiki に file back されている。
- health check が 1 つ記録されている。
- optional CLI tools が存在する場合、plain files のみに作用する。
- domain-specific architecture が導入されていない。
