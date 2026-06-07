# SF6-skills

クリーンスレートの Karpathy-style LLM Wiki scaffold。

See [ROADMAP.md](ROADMAP.md).

## 人間がやること

このリポジトリは Karpathy-style LLM Wiki です。

人間は一次資料を `raw/` に追加し、LLM は `raw/` を読んで `wiki/` を保守します。
`raw/` は source of truth なので、LLM には編集させません。
`raw/` は原本保存層です。英語 source は英語のまま、日本語 source は日本語のまま保存し、
翻訳・要約・正規化した置き換え版は `raw/` に置きません。日本語化や説明は `wiki/` 側で行います。

## Karpathy本人発言として確認済みの道具

この節は、Karpathy 本人の [llm-wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
で確認できる運用だけをまとめます。

| 道具 | 何に使うか | このrepoでの使い方 |
|---|---|---|
| Obsidian app | 人間が raw、wiki、outputs を見るための IDE frontend | このrepoをObsidian vaultとして開く |
| Obsidian Web Clipper | Web記事をMarkdown化する | Web記事を `.md` として `raw/articles/` に保存する |
| Download attachments for current file | Web記事内の画像をローカル保存する | Obsidianの添付保存先を `raw/assets/` にして実行する |
| Obsidian Graph view | wikiのリンク構造を見る | hub、orphan、つながりを確認する |
| Marp | Markdown slide deck を作る | LLMが作った slide output をObsidianで見る |
| Dataview | frontmatterをqueryする | wiki pageのmetadata確認に使う |
| Git | Markdown repoの履歴、差分、branch管理 | ingest後に `git diff` を確認する |
| qmd | wikiが育った後のMarkdown検索 | small scaleでは不要。必要になったら検討する |

Karpathy式の中心は、Obsidianそのものではなく普通のファイルです。
Obsidianは見るためのfrontendで、知識ベース本体は `raw/` と `wiki/` のMarkdown repoです。

## Obsidian Web ClipperでWeb記事を追加する手順

Web記事を最初の source にする場合は、この方法が最も Karpathy式に近いです。

1. Obsidianでこのrepoをvaultとして開く。
2. Obsidian Web Clipperをブラウザに入れる。
3. Web記事を開く。
4. Web Clipperで記事をMarkdownとして保存する。
5. 保存先を `raw/articles/` にする。
6. ファイル名を日付・source名・topicが分かる形にする。

例:

```text
raw/articles/2026-05-26-example-topic.md
```

画像が重要な記事なら、続けて画像もローカル保存します。

1. Obsidian Settings -> Files and links を開く。
2. Attachment folder path を `raw/assets/` にする。
3. Obsidian Settings -> Hotkeys で `Download attachments for current file` を探す。
4. 任意のhotkeyを割り当てる。
5. Web Clipperで保存した記事を開いた状態で、そのhotkeyを実行する。

これにより、記事本文は `raw/articles/`、記事画像は `raw/assets/` に残ります。
URL切れに依存せず、LLMが必要に応じて画像を参照しやすくなります。

注意:

- LLMはMarkdown内のinline画像を一度に自然に読むとは限りません。
- 画像が重要な場合は、まずMarkdown本文を読ませ、必要な画像を別途参照させます。
- `raw/` はimmutable sourceなので、保存後にLLMへ編集させません。
- `raw/` には翻訳・要約・正規化した置き換え版を置きません。派生した日本語説明は `wiki/` に置きます。

## Obsidianで人間が確認すること

LLMが `wiki/` を更新したら、Obsidianで以下を確認します。

- `wiki/index.md` から関係ページを辿れるか
- wikilinkが自然につながっているか
- Graph viewで孤立ページやhubが見えるか
- source summaryが `raw/` のsourceへ戻れるか
- 出力されたMarkdown、Marp、chartなどが読めるか

この確認は、人間がwikiを手書きで保守するという意味ではありません。
wikiの作成と保守はLLMの担当で、人間はレビューと方向づけをします。

## Gitで人間が確認すること

Karpathy式では、wikiはMarkdown filesのGit repoとして扱います。
LLMが作業した後は、必ず差分を見ます。

```bash
git status
git diff
```

見るべき点:

- `raw/` がLLMに変更されていない
- `wiki/index.md` が更新されている
- `wiki/log.md` に追記されている
- 新しいwiki pageが必要以上に増えていない
- 既存pageを更新すべき場面で重複pageを作っていない
- 重要なclaimがsourceへ辿れる
- 不確実な点が明示されている

問題なければ commit します。

```bash
git add raw/ wiki/
git commit -m "Ingest <source title>"
```

## まだ最初から使わないもの

Karpathy本人のGistでも、これらは初期必須ではありません。

- vector DB
- graph DB
- MCP中心設計
- fine-tuning
- batch ingest
- 完全自動ingest

まずは `raw/`、`wiki/`、`AGENTS.md` / `CLAUDE.md`、`wiki/index.md`、
`wiki/log.md`、Obsidian、Git、1 sourceずつのmanual ingestを優先します。

## source の置き方

1つずつ追加してください。初期段階では batch ingest しません。

置き場所の目安:

```text
raw/articles/      Web記事、ブログ、ニュース
raw/papers/        論文、PDF由来Markdown
raw/repos/         GitHub repo のREADME、docs、重要ファイルのsnapshot
raw/datasets/      CSV、JSON、metadata
raw/images/        スクリーンショット、図
raw/assets/        記事画像などの添付ファイル
raw/transcripts/   transcript
raw/notes/         自分の調査メモ、読書メモ
raw/official/      公式一次資料のHTML、DOM、スクリーンショットなど
```

ファイル名は、日付・source名・topic が分かる形にします。

例:

```text
raw/articles/2026-05-26-example-topic.md
raw/papers/2026-05-26-example-paper.md
raw/datasets/2026-05-26-example-dataset.json
raw/images/2026-05-26-example-screenshot.png
```

Markdown source には、可能なら frontmatter を付けます。

```markdown
---
type: raw_source
source_type: article
title: ""
author: ""
original_url: ""
captured_at: YYYY-MM-DD
status: raw
---

# <Title>

...
```

画像や添付ファイルが重要な場合は、URL参照だけにせず `raw/images/` または
`raw/assets/` にローカル保存します。

## 公式フレームデータの置き方

公式フレームデータは記事ではなく、公式リファレンス / dataset-like source として扱います。
Web Clipper Markdownではなく、再現できるツールでHTML、DOM、スクリーンショットを保存します。

この frame-data capture pipeline は、`raw/` の中でも履歴用 snapshot ではなく
`storage_policy: latest_frame_data_mirror` の固定 mirror として保存します。
由来の時点は path ではなく、各 `manifest.json` / `metadata.json` の provenance field と
Git 履歴で確認します。

```text
raw/frame-data/official/<character>/<control-scheme>/
  page.html
  table.dom.json
  screenshot.png
  metadata.json
raw/frame-data/official/<character>/manifest.json
```

派生CSVも安定したpathに出します。

```text
wiki/outputs/data/frame-data/official/<character>/<control-scheme>.csv
wiki/outputs/data/frame-data/official/<character>/<control-scheme>.field-meanings.json
```

CSVは技1項目ごとのデータに絞り、publisher、game、locale、source URL、
character、control scheme、raw pathなどのsource-level metadataは
`raw/frame-data/official/.../manifest.json`、各 `metadata.json`、wiki source page に残します。
`*.field-meanings.json` には、表ヘッダの補足説明やtooltip相当の説明を保存します。

ツールは `uv` で実行します。

```bash
uv sync
uv run python -m tools.frame_data.official.capture --character-slug jp
uv run python -m tools.frame_data.official.extract --character-slug jp
uv run python -m tools.frame_data.official.validate --character-slug jp
```

`tools.frame_data.official.validate` は全行について `page.html` 内の表、`table.dom.json`、
派生CSV、`*.field-meanings.json` の一致を確認します。スクリーンショットは値の正本として
OCRするのではなく、表の横幅と高さを覆っていること、Cookieやnavigation overlayが
残っていないことを確認します。値の正確性は、画像ではなく raw HTML / DOM / CSV の
全行照合で確認します。

Capcom 公式 capture は Classic / Modern tab の identity と active state も保存・検証します。
表 body に category row でも通常データ row でもない未知の cell 数が出た場合は、
その row を黙って捨てず、capture / extract / validate を失敗させます。

## 公式Battle Change Listの置き方

公式 Battle Change List は、公式の更新履歴 / battle balance source として扱います。
frame-data と同じく履歴用 snapshot ではなく、`storage_policy: latest_battle_change_mirror`
の固定 mirror として保存します。由来の時点は path ではなく `manifest.json` の
`capture_label` / `created_at_utc` と Git 履歴で確認します。

```text
raw/battle-change/official/
  manifest.json
  discovery/
    page.html
    data.json
    metadata.json
  versions/<version>/
    page.html
    data.json
    metadata.json
```

派生CSV / JSONは安定したpathに出します。

```text
wiki/outputs/data/battle-change/official/versions.csv
wiki/outputs/data/battle-change/official/changes.csv
wiki/outputs/data/battle-change/official/changes.json
wiki/outputs/data/battle-change/official/schema.json
```

ツールは次の順で実行します。

```bash
uv run python -m tools.battle_change.official.capture --dry-run
uv run python -m tools.battle_change.official.capture
uv run python -m tools.battle_change.official.validate
uv run python -m tools.battle_change.official.extract
```

`tools.battle_change.official.capture` は discovery page の `adjust.versions` から
全 version を列挙し、各 version の HTML と Next.js `_next/data` JSON を保存します。
`tools.battle_change.official.validate` は artifact hash、HTML `__NEXT_DATA__` と
`data.json` の payload 一致、version ID 一致を確認します。`changes.csv` の
`text_html` は公式 HTML fragment を保持し、翻訳・要約・正規化した raw replacement ではありません。
version title は各 version page 由来の `version_title` と discovery selector 由来の
`version_selector_title` を別列で保持し、公式 source 内の表記差は `version_title_mismatch`
で明示します。

## SuperComboフレームデータの置き方

SuperCombo も fixed latest mirror として保存します。source revision は path ではなく、
`manifest.json` の `source_revision` と `validation.json` の `raw_fingerprint` で確認します。

```text
raw/frame-data/supercombo/<character>/
  data.raw.wikitext
  frame-data.raw.wikitext
  data.templates.json
  frame-data.cargo-queries.json
  cargo/
  rendered/
  screenshots/
  imageinfo.json
  image-manifest.json
  metadata.json
  manifest.json
  validation.json
```

派生データは次に出します。

```text
wiki/outputs/data/frame-data/supercombo/<character>/
wiki/outputs/data/frame-data/official-supercombo-enriched/<character>/
```

実行順序は capture、validate、extract、必要に応じて enriched build です。

```bash
uv run python -m tools.frame_data.supercombo.capture --character JP --character-slug jp
uv run python -m tools.frame_data.supercombo.validate --character-slug jp
uv run python -m tools.frame_data.supercombo.extract --character-slug jp
uv run python -m tools.frame_data.enriched.build --character-slug jp
```

`tools.frame_data.supercombo.capture` は古い `validation.json` を削除します。
`tools.frame_data.supercombo.validate` は現在の raw metadata と実ファイル artifact hash から `raw_fingerprint` を作り、
`validation.json` に保存します。`tools.frame_data.supercombo.extract` は `status: passed` だけでなく
`raw_fingerprint` が現在の raw と一致することを要求するため、再取得後に古い validation だけが
残っている状態では派生データを生成しません。

## source を置いた後にLLMへ依頼すること

source を `raw/` に置いたら、次のように依頼します。

```text
この source を ingest してください:

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

## ingest 後に人間が確認すること

LLM が ingest した後、人間は Git diff を確認します。

```bash
git status
git diff
```

確認する点:

- `raw/` が変更されていない
- `wiki/sources/` に source summary が作られている
- 必要な `wiki/concepts/`、`wiki/entities/`、`wiki/syntheses/` が更新されている
- `wiki/index.md` が更新されている
- `wiki/log.md` に追記されている
- 重要な claim が source に辿れる
- 不確実な点が open questions や review note として残っている

問題なければ commit します。

```bash
git add raw/ wiki/
git commit -m "Ingest <source title>"
```

## 質問する時の流れ

質問する時は、LLM に wiki を使って回答するよう依頼します。

```text
wiki を使って次の質問に答えてください:

<Question>

ワークフロー:
1. 最初に wiki/index.md を読む。
2. 必要なら wiki を検索する。
3. 関連する source、concept、entity、synthesis pages を読む。
4. citations 付きで回答する。
5. 回答が durable なら wiki/questions/ または wiki/syntheses/ に保存する。
6. wiki/index.md と wiki/log.md を更新する。
7. changed files を報告する。
```

良い回答をチャット履歴だけに残さず、`wiki/questions/` や
`wiki/syntheses/` に file back するのがこの方式の重要な運用です。
