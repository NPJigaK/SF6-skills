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
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/juggle-system]]"
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

Street Fighter 6 の用語を、source ごとの説明を残しながら統合するための index。個別 term page は `wiki/concepts/terms/` 配下に置き、公式 source、community source、質問回答、派生 output からの追加根拠を同じ用語へ集約する。Query ではまずこの index から該当 term page を探し、用語ページの source claim から raw/source page へ戻る。

## 方針

- 用語ごとに 1 page を作り、source ごとの claim を追記する。
- source 間で意味や条件が違う場合は、片方を消さずに `意味差分` として明示する。
- 個別技の frame value や patch-specific な数値は、公式 frame-data / Battle Change source を優先し、用語 page では根拠 source への入口に留める。
- Slug は English / ASCII を使う。英語へ置き換えると意味がずれやすい用語は romaji を使う。
- `wiki/index.md` は個別 term page の direct catalog を持ち、用語の詳細な集約はこの page が担う。
- Question pages から term pages への backlink は、本文に自然に出る重要語だけを本文リンクし、補助的な発見性は frontmatter `related:` に集約する。

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

## Drive / Super Art / frame-data / notation 由来の追加用語

| Term page | 日本語 / 表記 | 主な source | 主な関連 |
|---|---|---|---|
| [[concepts/terms/burnout]] | バーンアウト | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/drive-system]], [[concepts/terms/chip-damage]], [[concepts/terms/stun]] |
| [[concepts/terms/drive-impact]] | ドライブインパクト / Drive Impact | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/drive-system]], [[concepts/terms/drive-impact-counter]], [[concepts/terms/wall-bounce]] |
| [[concepts/terms/drive-parry]] | ドライブパリィ / Drive Parry | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/drive-system]], [[concepts/terms/perfect-parry]], [[concepts/terms/raw-drive-rush]] |
| [[concepts/terms/drive-reversal]] | ドライブリバーサル / Drive Reversal | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/drive-system]], [[concepts/terms/invincible-move]] |
| [[concepts/terms/drive-rush-cancel]] | キャンセルドライブラッシュ / DRC | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/terms/raw-drive-rush]], [[concepts/terms/cancel]], [[concepts/terms/frame-advantage]] |
| [[concepts/terms/overdrive]] | オーバードライブ / OD | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/drive-system]], [[concepts/terms/burnout]] |
| [[concepts/terms/super-art]] | スーパーアーツ / SA | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/frame-data]], [[concepts/terms/critical-art]], [[concepts/terms/cancel]] |
| [[concepts/terms/critical-art]] | クリティカルアーツ / CA | [[sources/capcom-official-zangief-frame-data]], [[sources/supercombo-zangief-frame-data]] | [[concepts/terms/super-art]], [[concepts/frame-data]] |
| [[concepts/terms/damage-scaling]] | ダメージ補正 / damage scaling | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/frame-data]], [[concepts/terms/scaling-reset]] |
| [[concepts/terms/wall-bounce]] | 壁バウンド / 壁やられ | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/capcom-official-zangief-frame-data]] | [[concepts/terms/drive-impact]], [[concepts/terms/corner]], [[concepts/juggle-system]] |
| [[concepts/terms/air-reset]] | Air Reset / 空中リセット | [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/juggle-system]], [[concepts/terms/wall-bounce]] |
| [[concepts/terms/chain]] | Chain / Chn | [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/fighting-game-notation]], [[concepts/terms/cancel]] |
| [[concepts/terms/cancel]] | Cancel / キャンセル | [[sources/supercombo-street-fighter-6-glossary]], [[sources/capcom-official-fightingground-battle-system]] | [[concepts/fighting-game-notation]], [[concepts/terms/drive-rush-cancel]], [[concepts/terms/chain]] |

## 未解決の質問

- SuperCombo glossary など community source を追加した時、どの用語で意味差分が出るか。
- Term page から個別の frame-data row や question page へ、どの粒度で backlink を張るか。
