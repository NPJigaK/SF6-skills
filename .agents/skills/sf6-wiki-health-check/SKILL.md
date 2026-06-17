---
name: sf6-wiki-health-check
description: Use for SF6 wiki health check, lint, structural refactor planning, stale-claim review, duplicate/orphan detection, calculation evidence drift, missing backlinks, index/log repair, and evidence validation. Produces safe fixes, review notes, or refactor plans.
---

# SF6 Wiki Health Check

## 中核ルール

安全な structural repair と factual judgment を分ける。`raw/` / `wiki/` / schema 境界、lint report placement、page type、index/log 更新、最終報告は `AGENTS.md` を正本にする。

## 開始手順

1. `AGENTS.md` を読む。
2. `wiki/index.md` を読む。
3. `wiki/log.md` の最近の entry を読む。
4. JSON / JSONL の値、件数、schema-like 条件、validation status を確認する時は repo-local `$jq-cli` skill を使い、`jq` / `jq -e` を第一選択にする。
5. 新しい tool を足す前に、`rg`、`jq`、単純な file tools を使う。

## Severity

- P0 Integrity: broken wikilinks、missing frontmatter、missing index entry、log omission、obvious Markdown formatting。安全なら修正する。
- P1 Evidence: uncited important claims、source conflicts、stale claims、row count mismatch、validation failure、raw/source/derived mismatch。事実を書き換えず、`wiki/reviews/` を作成または更新する。
- P2 Structure: orphan pages、duplicate concepts、missing backlinks、missing concept/entity pages。小さな局所修正なら直し、大きな semantic merge は review に回す。
  source claim を変更しない backlink repair、index rebuild、deprecated marker 追加、明らかな duplicate entry 整理は wiki maintenance として実行してよい。
  page merge / split / rename / directory move は semantic 判断を含みやすいため、明らかな placeholder や完全重複を除き、まず `wiki/reviews/` に refactor plan を作る。
- P3 Quality: weak summaries、missing aliases/tags、readability issues。低リスクなら改善する。

## Workflow

1. structural issue と evidence issue を分けて確認する。
2. safe P0 fix を適用する。
3. P1 issue では disputed claim を消さず、evidence path と human review が必要な点を review note に残す。
4. row count mismatch、validation failure、raw/source/derived mismatch の JSON 側検証は、可能な限り `jq -e` で exit status を使って確認する。
5. wiki 全体 report は `wiki/outputs/lint/` に `type: output`、`output_type: lint_report` として置く。
6. 新規 report / review または主要 status 変更があれば `wiki/index.md` を更新する。
7. `wiki/log.md` に追記する。
8. 変更ファイルと human-review items を報告する。

## Calculation Evidence Health Check

Calculation-related health check では、次を `$sf6-calculation-grounding` の対象として扱う。

- candidate ledger / candidate fixture が deterministic output に混入している
- human-only validation が general rule / validated_rule に昇格している
- source-backed でない rule promotion がある
- community-only numeric source が official / lab-verified value として扱われている
- validation failure output が source of truth として引用されている
- calculator output に source path、authority、validation status、review status、calculator version、input hash がない
- schema / contract descriptor、fixtures、tests、protocol page、reports の間で drift がある
- route-specific regression fixture が general formula の証拠として使われている

これらは原則 P1 Evidence として扱い、値や結論を黙って修正しない。
安全な修正は metadata / backlink / index / status の補正までに留め、事実判断は review note または refactor plan に残す。

## Refactor-Oriented Health Check

health check は report 作成だけではなく、wiki を再利用しやすく保つための refactor trigger です。

### Required structural review

- duplicate concept を merge できるか
- concept / entity / synthesis の責務が曖昧でないか
- source summary が concept / entity / synthesis へ統合されているか
- repeated query pattern から新しい synthesis / hub page が必要でないか
- index.md が入口として機能しているか
- term pages、frame-data pages、battle-change pages のディレクトリ構成が読者と LLM の両方に使いやすいか
- question/output pages が孤立していないか
- old lint findings が繰り返し出ているのに構造改善されていない箇所がないか

### Output

health check は scope に応じて次のどちらかを出す。

1. `No structural refactor needed` と根拠
2. `Refactor candidates` table

| Candidate | Type | Evidence | Suggested action | Risk | Can auto-fix? |
|---|---|---|---|---|---|

### Auto-fix

低リスクなものは実行してよい。

- missing backlink
- aliases / tags 追加
- index summary 更新
- orphan page に明らかな backlink を追加
- status / frontmatter 補正
- duplicate entry の整理
- obvious related link 追加

大きな意味変更、page merge、rename、directory restructure は `wiki/reviews/` に refactor plan を作る。

## Subagent Use

subagent が許可されており、wiki が大きい、または factual risk が高い場合は independent read-only audits を使ってよい。

- 1 pass は structural issues を地図化する。
- 別 pass は evidence risks、conflicts、stale claims、validation mismatches を確認する。
- 親 agent が修正可否を判断し、review note を書き、diff を検証する。

## Tool Gate

judgment を encode するためだけに `kb_lint.py`、path guard、その他 generic tool を作らない。同じ deterministic check が十分に繰り返され、prompt discipline より automation の方が明らかに信頼できる時だけ tool を追加する。
