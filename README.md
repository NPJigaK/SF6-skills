# SF6-skills

Clean-slate Karpathy-style LLM Wiki scaffold.

See [ROADMAP.md](ROADMAP.md).

## 人間がやること

このリポジトリは Karpathy-style LLM Wiki です。

人間は一次資料を `raw/` に追加し、LLM は `raw/` を読んで `wiki/` を保守します。
`raw/` は source of truth なので、LLM には編集させません。

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

## source を置いた後にLLMへ依頼すること

source を `raw/` に置いたら、次のように依頼します。

```text
Ingest this source:

raw/<path>

Follow AGENTS.md exactly.

Requirements:
- Do not edit raw/.
- Read wiki/index.md first.
- Read recent entries in wiki/log.md.
- Create a source summary in wiki/sources/.
- Update related concept/entity/synthesis pages.
- Prefer updating existing pages over creating duplicates.
- Add backlinks.
- Flag contradictions, stale claims, and uncertainty.
- Update wiki/index.md.
- Append to wiki/log.md.
- Report changed files and open questions.
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
- 不確実な点が Open questions や review note として残っている

問題なければ commit します。

```bash
git add raw/ wiki/
git commit -m "Ingest <source title>"
```

## 質問する時の流れ

質問する時は、LLM に wiki を使って回答するよう依頼します。

```text
Answer this question using the wiki:

<Question>

Workflow:
1. Read wiki/index.md first.
2. Search the wiki if needed.
3. Read relevant source, concept, entity, and synthesis pages.
4. Produce an answer with citations.
5. If the answer is durable, save it to wiki/questions/ or wiki/syntheses/.
6. Update wiki/index.md and wiki/log.md.
7. Report changed files.
```

良い回答をチャット履歴だけに残さず、`wiki/questions/` や
`wiki/syntheses/` に file back するのがこの方式の重要な運用です。
