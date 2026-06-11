---
name: sf6-durable-output
description: Use when SF6 wiki の durable output や reusable answer の file-back を作る時。wiki/questions、wiki/syntheses、wiki/outputs reports、comparison tables、lint reports、reader-facing Markdown artifacts を含む。
---

# SF6 Durable Output

## 中核ルール

有用な回答を durable に残しつつ、作業履歴を reader-facing content に混ぜない。page type、言語ポリシー、evidence、index/log 更新、最終報告は `AGENTS.md` を正本にする。

## 保存先

- `wiki/questions/`: 再利用可能な answered question。answer、evidence、explanation、uncertainty に集中する。
- `wiki/syntheses/`: 1 つの質問を超える cross-source analysis や durable theory。
- `wiki/outputs/reports/`: reader-facing report や comparison table。
- `wiki/outputs/lint/`: wiki 全体の health / lint report。frontmatter は `type: output`、`output_type: lint_report`。
- `wiki/reviews/`: individual finding、contradiction、stale claim、capture review、人間レビュー note。

question page には changed files、implementation notes、file-back mechanics を入れない。workflow history は `wiki/log.md` に置く。

## Workflow

1. `AGENTS.md` と `wiki/index.md` を読む。
2. output を支える source/wiki pages を読む。
3. convenience ではなく page type に基づいて保存先を選ぶ。
4. 既存 template と local page style があれば従う。
5. 重要 claim の近くに citation を置く。derived value は source page、raw path、manifest/validation、derived JSON path へ戻す。
6. derived JSON 由来の数値、件数、比較を output に書く時は `$jq-cli` skill を使い、`jq` で取得・検証した値を使う。
7. source fidelity が必要な場合を除き、本文は日本語を優先する。
8. 新規 page または主要 output 更新があれば `wiki/index.md` を更新する。
9. `wiki/log.md` に task history を追記する。
10. 変更ファイルと unresolved evidence gaps を報告する。

## File-Back Decision

回答が再利用されそう、wiki knowledge を修正または明確化する、durable comparison を作る、source conflict を記録する場合は file back する。一回限りの chat control message、status-only reply、evidence 不足の回答は file back しない。ただし、durable artifact が evidence gap の review note である場合は例外。

## Subagent Use

subagent が許可されており、output が長い、または evidence-heavy な場合は read-only outline/evidence pass を使ってよい。

- candidate structure、supporting pages、unresolved evidence gaps を依頼する。
- 親 agent が output を書き、citation を確認し、index/log を更新する。
- subagent prose を検証なしに final text にしない。
