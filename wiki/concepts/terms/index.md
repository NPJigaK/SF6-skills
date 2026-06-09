---
type: concept
concept_type: term_index
title: "SF6 Terms"
created: 2026-06-10
updated: 2026-06-10
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Street Fighter 6 terms"
  - "SF6 用語"
  - "スト6 用語"
tags:
  - sf6
  - terms
  - glossary
---

# SF6 Terms

## 要約

Street Fighter 6 の用語を、source ごとの説明を残しながら統合するための index。個別 term page は `wiki/concepts/terms/` 配下に置き、公式 source、community source、質問回答、派生 output からの追加根拠を同じ用語へ集約する。

## 方針

- 用語ごとに 1 page を作り、source ごとの claim を追記する。
- source 間で意味や条件が違う場合は、片方を消さずに `意味差分` として明示する。
- 個別技の frame value や patch-specific な数値は、公式 frame-data / Battle Change source を優先し、用語 page では根拠 source への入口に留める。
- Slug は English / ASCII を使う。英語へ置き換えると意味がずれやすい用語は romaji を使う。

## Capcom eSports BASE 由来の用語

| 重要度 | Term page | 日本語 | 読み | 主な関連 |
|---:|---|---|---|---|
| 3 | [[concepts/terms/chip-damage]] | 削り | けずり | [[concepts/drive-system]] |
| 3 | [[concepts/terms/stun]] | スタン | すたん | [[concepts/drive-system]], [[concepts/terms/corner]] |
| 3 | [[concepts/terms/anti-air]] | 対空 | たいくう | [[concepts/drive-system]] |
| 3 | [[concepts/terms/corner]] | 画面端 | がめんはし | [[concepts/terms/stun]], [[concepts/terms/oki]] |
| 3 | [[concepts/terms/cross-up]] | めくり | めくり | [[concepts/terms/anti-air]] |
| 3 | [[concepts/terms/command-throw]] | コマ投げ | こまなげ | [[concepts/terms/shimmy]] |
| 3 | [[concepts/terms/raw-drive-rush]] | 生ラッシュ | なまらっしゅ | [[concepts/drive-system]], [[concepts/terms/frame-advantage]] |
| 3 | [[concepts/terms/drive-impact-counter]] | インパクト返し | いんぱくとがえし | [[concepts/drive-system]], [[concepts/terms/corner]] |
| 3 | [[concepts/terms/perfect-parry]] | ジャストパリィ | じゃすとぱりぃ | [[concepts/drive-system]], [[concepts/terms/scaling-reset]] |
| 2 | [[concepts/terms/oki]] | 起き攻め | おきぜめ | [[concepts/terms/meaty]], [[concepts/terms/setplay]] |
| 2 | [[concepts/terms/punish-counter]] | パニッシュカウンター | ぱにっしゅかうんたー | [[concepts/terms/frame-advantage]], [[concepts/terms/whiff-punish]] |
| 2 | [[concepts/terms/whiff-punish]] | 差し返し | さしかえし | [[concepts/terms/punish-counter]] |
| 2 | [[concepts/terms/invincible-move]] | 無敵技 | むてきわざ | [[concepts/terms/abare]] |
| 2 | [[concepts/terms/frame-advantage]] | 有利フレーム | ゆうりふれーむ | [[concepts/frame-data]], [[concepts/terms/guaranteed-punish]] |
| 2 | [[concepts/terms/meaty]] | 重ね | かさね | [[concepts/terms/oki]], [[concepts/terms/frame-advantage]] |
| 2 | [[concepts/terms/lethal]] | リーサル | りーさる | [[concepts/drive-system]] |
| 1 | [[concepts/terms/shikomi]] | 仕込み | しこみ | [[concepts/terms/hit-confirm]], [[concepts/terms/whiff-punish]] |
| 1 | [[concepts/terms/guaranteed-punish]] | 確定反撃 | かくていはんげき | [[concepts/terms/frame-advantage]] |
| 1 | [[concepts/terms/hit-confirm]] | ヒット確認 | ひっとかくにん | [[concepts/frame-data]], [[concepts/terms/shikomi]] |
| 1 | [[concepts/terms/shimmy]] | シミー | しみー | [[concepts/terms/punish-counter]], [[concepts/terms/corner]] |
| 1 | [[concepts/terms/setplay]] | セットプレイ | せっとぷれい | [[concepts/terms/oki]], [[concepts/terms/meaty]] |
| 1 | [[concepts/terms/abare]] | 暴れ | あばれ | [[concepts/terms/invincible-move]], [[concepts/terms/meaty]] |
| 1 | [[concepts/terms/scaling-reset]] | 補正切り | ほせいぎり | [[concepts/frame-data]], [[concepts/terms/hit-confirm]] |

## 未解決の質問

- SuperCombo glossary など community source を追加した時、どの用語で意味差分が出るか。
- Term page から個別の frame-data row や question page へ、どの粒度で backlink を張るか。
