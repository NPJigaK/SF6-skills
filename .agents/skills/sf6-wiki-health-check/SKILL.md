---
name: sf6-wiki-health-check
description: Use when SF6 wiki health を確認する時。broken wikilinks、missing index/log entries、orphan pages、uncited important claims、stale claims、contradictions、validation mismatches、review-note candidates を含む。
---

# SF6 Wiki Health Check

## 中核ルール

安全な structural repair と factual judgment を分ける。`raw/` / `wiki/` / schema 境界、lint report placement、page type、index/log 更新、最終報告は `AGENTS.md` を正本にする。

## 開始手順

1. `AGENTS.md` を読む。
2. `wiki/index.md` を読む。
3. `wiki/log.md` の最近の entry を読む。
4. 新しい tool を足す前に、`rg` と単純な file tools を使う。

## Severity

- P0 Integrity: broken wikilinks、missing frontmatter、missing index entry、log omission、obvious Markdown formatting。安全なら修正する。
- P1 Evidence: uncited important claims、source conflicts、stale claims、row count mismatch、validation failure、raw/source/derived mismatch。事実を書き換えず、`wiki/reviews/` を作成または更新する。
- P2 Structure: orphan pages、duplicate concepts、missing backlinks、missing concept/entity pages。小さな局所修正なら直し、大きな semantic merge は review に回す。
- P3 Quality: weak summaries、missing aliases/tags、readability issues。低リスクなら改善する。

## Workflow

1. structural issue と evidence issue を分けて確認する。
2. safe P0 fix を適用する。
3. P1 issue では disputed claim を消さず、evidence path と human review が必要な点を review note に残す。
4. wiki 全体 report は `wiki/outputs/lint/` に `type: output`、`output_type: lint_report` として置く。
5. 新規 report / review または主要 status 変更があれば `wiki/index.md` を更新する。
6. `wiki/log.md` に追記する。
7. 変更ファイルと human-review items を報告する。

## Subagent Use

subagent が許可されており、wiki が大きい、または factual risk が高い場合は independent read-only audits を使ってよい。

- 1 pass は structural issues を地図化する。
- 別 pass は evidence risks、conflicts、stale claims、validation mismatches を確認する。
- 親 agent が修正可否を判断し、review note を書き、diff を検証する。

## Tool Gate

judgment を encode するためだけに `kb_lint.py`、path guard、その他 generic tool を作らない。同じ deterministic check が十分に繰り返され、prompt discipline より automation の方が明らかに信頼できる時だけ tool を追加する。
