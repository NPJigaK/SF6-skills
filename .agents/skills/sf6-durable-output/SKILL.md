---
name: sf6-durable-output
description: Use for durable file-back of SF6 answers, syntheses, reports, comparison tables, calculation reports, fixtures/postmortems, lint reports, and wiki-compounding outputs. Saves reader-facing artifacts and integrates reusable findings back into related wiki pages.
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
6. derived JSON 由来の数値、件数、比較を output に書く時は repo-local `$jq-cli` skill を使い、`jq` / `jq -e` で取得・検証した値を使う。
7. source fidelity が必要な場合を除き、本文は日本語を優先する。
8. 新規 page または主要 output 更新があれば `wiki/index.md` を更新する。
9. `wiki/log.md` に task history を追記する。
10. 変更ファイルと unresolved evidence gaps を報告する。

## Compound Back Into Wiki

durable output を保存した後、次の compound pass を行う。

1. output の知見は既存 concept / entity / synthesis を更新するべきか。
2. question answer に一般化可能な知見がある場合、`wiki/syntheses/` に昇格または既存 synthesis に統合するべきか。
3. output が repeated query pattern を示す場合、新しい hub page / overview page が必要か。
4. output から related links / backlinks / aliases / tags を追加するべきか。
5. index.md に entry を追加するだけでなく、既存 summary や入口構造を更新するべきか。
6. 古い output / question / synthesis が supersede された場合、`deprecated`、`review-needed`、または相互 link を追加すべきか。

保存だけでなく、wiki 全体への統合を検討する。

## File-Back Decision

回答が再利用されそう、wiki knowledge を修正または明確化する、durable comparison を作る、source conflict を記録する場合は file back する。一回限りの chat control message、status-only reply、evidence 不足の回答は file back しない。ただし、durable artifact が evidence gap の review note である場合は例外。

## Calculation Output Gate

Calculation report、fixture、postmortem、prediction、rule promotion、calculator output を保存する場合は、
`$sf6-calculation-grounding` の authority / validation / fixture decision / rule promotion decision を確認する。

File-back してよいもの:

- source-backed または validation-backed な exact result
- candidate ledger と unknowns を明示した review note
- route-specific regression fixture の根拠と限界
- prediction / postmortem が protocol、fixture、schema、tool contract へ戻すべき学び
- rule promotion を拒否した理由と必要 evidence

File-back してはいけないもの:

- route text だけから作った exact value
- candidate fixture を deterministic output のように見せる report
- human-only observation を general rule / validated_rule に昇格した claim
- validation failure を source of truth として扱う output

計算系 output を保存した後は、`wiki/concepts/combo-damage-ledger-protocol.md`、
関連 review、schema、tests、index/log へ戻す必要があるかを確認する。

## Subagent Use

subagent が許可されており、output が長い、または evidence-heavy な場合は read-only outline/evidence pass を使ってよい。

- candidate structure、supporting pages、unresolved evidence gaps を依頼する。
- 親 agent が output を書き、citation を確認し、index/log を更新する。
- subagent prose を検証なしに final text にしない。
