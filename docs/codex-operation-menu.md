# Codex Operation Menu

このファイルは、SF6 LLM Wiki の日常作業を短い依頼文で安定して回すためのメニューです。

詳細な workflow は `AGENTS.md` と `.agents/skills/*/SKILL.md` を正本にします。このメニューは呼び出し文の例であり、source fact、validation status、review status の正本ではありません。

## 使い方

各メニューは短い呼び出し文です。迷う場合は、次の mode を明示してください。

- `read-only plan`: 編集せず計画だけ出す。
- `one safe fix`: 低リスクな1件だけ実行する。
- `apply approved plan`: 既にreview済みのplanだけ実行する。
- `capture-only`: raw package化まで。wiki化しない。
- `capture-then-ingest`: `ready-for-ingest` ならwiki化まで進める。

## URLをraw化する

```text
$sf6-url-source-capture を使って、このURLをraw source package化してください。

URL:
<URL>

条件:
- raw/ に要約・翻訳・正規化版を置かない
- 既存repo toolがあれば優先する
- scope / storage_policy / manifest / metadata / validation を残す
- wiki/reviews/ にcapture reviewを作る
- まだwiki化はしない
- 最後に ingest してよいか判断してください
```

## URLをraw化してwiki化まで進める

```text
まず $sf6-url-source-capture でこのURLをraw化してください。
capture reviewで ready-for-ingest と判断できたら、続けて $sf6-source-ingest でwiki化してください。

URL:
<URL>

条件:
- raw/ はsource artifactsだけ
- wiki化ではsource summaryだけで終わらせず、関連concept/entity/synthesis/index/logまで確認
- 大きな再編はplan-first
- 不確実な点はreview noteに残す
```

重要 source では、capture と ingest を別ターンに分ける方が安全です。

## raw capture済みsourceをreviewする

```text
$sf6-raw-capture-review を使って、このraw packageがingest可能か確認してください。

対象:
<raw/package/manifest.json>

条件:
- raw artifactsは編集しない
- storage_policy / scope / metadata / validation / freshness を確認
- wiki/reviews/ にcapture reviewを作るか更新する
- ready-for-ingest / needs-human-review / needs-recapture を判定してください
```

## raw済みsourceをwiki化する

```text
$sf6-source-ingest を使って、このraw sourceをwiki化してください。

対象:
<raw path or manifest>

条件:
- raw/ は編集しない
- source summaryだけで終わらせない
- related concept / entity / synthesis / review / output を確認
- Topology Passを行う
- 大きな再編はrefactor planにする
- index/logを更新する
```

## wiki evidenceだけで質問に答える

```text
$sf6-wiki-query を使って答えてください。

質問:
<question>

条件:
- wiki/index.md から読み始める
- source fact / derived fact / inference を分ける
- 根拠と不確実性を明示する
- 編集はしない
```

## calculation grounding dry-runを回す

```text
$sf6-calculation-grounding を使って、以下のcombo damage fixture / candidate routeをread-onlyで検証してください。

対象:
<fixture path or candidate route>

条件:
- route textだけからexact deterministic outputを出さない
- hit order proof / accepted validationがなければcandidate / unknowns / required evidenceで止める
- historical fixtureをcurrent answerに使わない
- human training validationをvalidated_ruleに昇格しない
- 実行が必要な場合はrepo-managed environmentの `uv run` を使う

推奨コマンド:
- `uv run python -m tools.calculations.combo_damage.calculate <ledger>`
- `uv run pytest tests/calculations/combo_damage`
```

## 回答をwikiへ保存する

```text
$sf6-durable-output を使って、直前回答をfile-backしてください。

条件:
- reader-facing な形式にする
- wiki/questions/、wiki/syntheses/、wiki/outputs/ のどれに置くべきか判断する
- Compound Back Into Wikiまで行う
- index/logを更新する
```

## wikiを整理する

```text
$sf6-wiki-refactor を使って、この範囲を整理してください。

対象:
<wiki page, source family, or review item>

条件:
- raw/ は編集しない
- evidence と provenance は残す
- 大きな merge / split / rename は plan-first
- index/logを更新する
```

## health checkを回す

```text
$sf6-wiki-health-check を使って、scope-limitedに確認してください。

対象:
<scope>

条件:
- P0/P1/P2/P3 を分ける
- safe fixだけ実行する
- 人間レビューが必要な事実問題は wiki/reviews/ に残す
- refactor candidatesも出す
```

## URLを入れるべきかだけ判断する

```text
$sf6-url-source-capture の観点で、このURLをraw化すべきかread-onlyで判断してください。

URL:
<URL>

条件:
- ファイル編集しない
- source authority / copyright / scope / existing coverage / expected value を確認
- raw化するなら保存先候補とstorage_policyを提案
- wiki化する価値があるか判断
```
