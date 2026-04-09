---
name: sync-knowledge
description: 新しいメモ、記事、動画要約、調査結果、ユーザーの補足を読み、SF6 knowledge を整理して更新するときに使う。core に昇格できるものと review に送るものを分ける。
---

あなたは SF6 knowledge を **安全に更新する** skill です。

## 目的
- 新しい素材を読み、core knowledge に昇格できるものだけを統合する。
- mixed / current fact / ソース不足は review queue へ送る。
- knowledge を冗長化させず、概念中心で育てる。

## 参照順
1. `../../skills/kb-sf6-core/references/SOURCE_POLICY.md`
2. `../../skills/kb-sf6-core/references/KNOWLEDGE.md`
3. `../../skills/kb-sf6-core/references/REVIEW_QUEUE.md`
4. `templates/ENTRY_TEMPLATE.md`
5. `templates/REVIEW_TEMPLATE.md`

## 手順
1. 入力素材を読む。
2. 各候補を次のどれかに分類する:
   - core
   - mixed
   - current-fact
   - community-term
   - insufficient-evidence
3. 根拠階層を判定する:
   - T1 / T2 / T3 / T4 / none
4. core として長く保てるものだけ `KNOWLEDGE.md` に統合する。
5. mixed / current-fact / ソース不足 / 衝突ありは `REVIEW_QUEUE.md` に追記する。
6. 既存の core と重複する場合は、新規節を増やさず既存節に統合する。
7. current fact を core knowledge に混ぜ込まない。

## 昇格ルール
- 概念として安定している
- 特定キャラ・特定パッチ・特定条件への依存が薄い
- 定義と実戦的意味が長く保てる
- ソースが弱くても一般概念として安定している場合は「コミュニティラベル」付きで採用可

## review 行きの条件
- exact 数値を含む
- current 仕様やコストを含む
- パッチ差分を含む
- 距離や状況が無いと成立が決まらない
- 公式と他ソースが衝突する

## 出力
- 何を knowledge に統合したか
- 何を review queue に送ったか
- 理由
- 追加で必要な確認があれば列挙
