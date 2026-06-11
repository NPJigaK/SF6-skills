---
type: concept
concept_type: term_index
title: "SF6 Terms"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/defense]]"
  - "[[concepts/offense]]"
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

Street Fighter 6 の用語を、source ごとの説明を残しながら統合するための index。個別 term page は `wiki/concepts/terms/` 配下に置き、公式 source、community source、HUD 表示 cue、質問回答、派生 output からの追加根拠を同じ用語へ集約する。SuperCombo Gauges page 由来の Drive / Super Gauge 数値は、source page と `wiki/outputs/data/gauges/supercombo/numeric-tables.json` に戻れる形で該当 term page へ接続する。SuperCombo Offense page 由来の throw / safe jump / blockstring 系用語は community tactical source として扱い、公式 source と重なる一般 mechanics では公式 source を優先する。SuperCombo Defense page 由来の blocking / throw escape / wake-up / reversal / armor 系用語は defensive timing source として扱い、公式 source と重なる Drive / invincibility mechanics では公式 source を優先する。Query ではまずこの index から該当 term page を探し、用語ページの source claim から source page へ戻る。

## 方針

- 用語ごとに 1 page を作り、source ごとの claim を追記する。
- source 間で意味や条件が違う場合は、片方を消さずに `意味差分` として明示する。
- 個別技の frame value や patch-specific な数値は、公式 frame-data / Battle Change source を優先し、用語 page では根拠 source への入口に留める。
- HUD icon 由来の用語は display cue として記録し、mechanics / damage / frame value の正本にしない。公式 source と重なる場合は公式 source を優先し、HUD source は visual/community evidence として使う。
- SuperCombo Gauges 由来の数値は community numeric source として扱う。公式 source または実機検証と重なる cost / frame / damage / range 値では公式・検証済み data を優先し、Gauges 値は補助根拠として残す。
- Drive / Super Gauge 系 term page の `数値データ` section は query 用の索引であり、巨大表の正本ではない。30 character range / distance table や機械計算に使う全値は [[sources/supercombo-street-fighter-6-gauges]] と `wiki/outputs/data/gauges/supercombo/numeric-tables.json` に戻る。
- SuperCombo Offense 由来の throw range、safe jump、empty jump、throw loop、blockstring claim は community tactical source として扱う。公式 source または実機検証と重なる場合はそちらを優先し、character-specific throw loop notes は stale risk を明示する。
- SuperCombo Defense 由来の throw escape window、wake-up forced standing、reversal buffer、armor damage、punish route claim は community tactical source として扱う。公式 source または実機検証と重なる場合はそちらを優先し、dash buffer bug note のような lab claim は未検証として読む。
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
| 2 | [[concepts/terms/punish-counter]] | パニッシュカウンター | ぱにっしゅかうんたー | [[concepts/terms/frame-advantage]], [[concepts/terms/whiff-punish]], [[concepts/terms/counter-hit]] |
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
| [[concepts/terms/burnout]] | バーンアウト | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/drive-system]], [[concepts/terms/chip-damage]], [[concepts/terms/stun]] |
| [[concepts/terms/drive-impact]] | ドライブインパクト / Drive Impact | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/drive-system]], [[concepts/terms/drive-impact-counter]], [[concepts/terms/wall-bounce]], [[concepts/terms/armor-break]], [[concepts/terms/crush]], [[concepts/terms/lock]] |
| [[concepts/terms/armor]] | Armor / アーマー | [[sources/supercombo-street-fighter-6-defense]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/defense]], [[concepts/drive-system]], [[concepts/terms/drive-impact]], [[concepts/terms/armor-break]] |
| [[concepts/terms/drive-parry]] | ドライブパリィ / Drive Parry | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/drive-system]], [[concepts/defense]], [[concepts/terms/perfect-parry]], [[concepts/terms/raw-drive-rush]] |
| [[concepts/terms/drive-reversal]] | ドライブリバーサル / Drive Reversal | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/drive-system]], [[concepts/terms/invincible-move]] |
| [[concepts/terms/drive-rush-cancel]] | キャンセルドライブラッシュ / DRC | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/terms/raw-drive-rush]], [[concepts/terms/cancel]], [[concepts/terms/frame-advantage]] |
| [[concepts/terms/overdrive]] | オーバードライブ / OD | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/drive-system]], [[concepts/terms/burnout]] |
| [[concepts/terms/super-art]] | スーパーアーツ / SA | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/frame-data]], [[concepts/terms/critical-art]], [[concepts/terms/cancel]] |
| [[concepts/terms/critical-art]] | クリティカルアーツ / CA | [[sources/supercombo-street-fighter-6-gauges]], [[sources/capcom-official-zangief-frame-data]], [[sources/supercombo-zangief-frame-data]] | [[concepts/terms/super-art]], [[concepts/frame-data]] |
| [[concepts/terms/damage-scaling]] | ダメージ補正 / damage scaling | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/frame-data]], [[concepts/terms/scaling-reset]] |
| [[concepts/terms/wall-bounce]] | 壁バウンド / 壁やられ | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-glossary]], [[sources/capcom-official-zangief-frame-data]] | [[concepts/terms/drive-impact]], [[concepts/terms/corner]], [[concepts/juggle-system]], [[concepts/terms/crush]], [[concepts/terms/lock]] |
| [[concepts/terms/air-reset]] | Air Reset / 空中リセット | [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/juggle-system]], [[concepts/terms/wall-bounce]], [[concepts/terms/forced-knockdown]] |
| [[concepts/terms/chain]] | Chain / Chn | [[sources/supercombo-street-fighter-6-glossary]] | [[concepts/fighting-game-notation]], [[concepts/terms/cancel]] |
| [[concepts/terms/cancel]] | Cancel / キャンセル | [[sources/supercombo-street-fighter-6-glossary]], [[sources/capcom-official-fightingground-battle-system]] | [[concepts/fighting-game-notation]], [[concepts/terms/drive-rush-cancel]], [[concepts/terms/chain]] |

## SuperCombo Offense 由来の追加用語

Offense page 由来の用語は、攻めの timing / pressure / tactical context として source claim を保持する。公式 source と重なる Counter / Punish Counter / Drive / Stun mechanics は公式 source または既存 source を優先し、Offense source は throw-specific / setup-specific な補助根拠として使う。

| Term page | 表記 | 主な source | 主な関連 |
|---|---|---|---|
| [[concepts/terms/throw]] | Throw / 投げ | [[sources/supercombo-street-fighter-6-offense]] | [[concepts/offense]], [[concepts/terms/throw-loop]], [[concepts/terms/command-throw]], [[concepts/terms/throw-escape]] |
| [[concepts/terms/throw-loop]] | Throw Loop / 投げループ | [[sources/supercombo-street-fighter-6-offense]] | [[concepts/offense]], [[concepts/terms/throw]], [[concepts/terms/oki]], [[concepts/terms/meaty]] |
| [[concepts/terms/safe-jump]] | Safe Jump / 安全飛び | [[sources/supercombo-street-fighter-6-offense]] | [[concepts/offense]], [[concepts/terms/oki]], [[concepts/terms/reversal]], [[concepts/terms/perfect-parry]] |
| [[concepts/terms/empty-jump-mixup]] | Empty Jump Mixup / 空ジャンプ択 | [[sources/supercombo-street-fighter-6-offense]] | [[concepts/offense]], [[concepts/terms/safe-jump]], [[concepts/terms/throw]], [[concepts/terms/oki]] |
| [[concepts/terms/blockstring]] | Blockstring / 固め | [[sources/supercombo-street-fighter-6-offense]] | [[concepts/offense]], [[concepts/frame-data]], [[concepts/terms/chain]], [[concepts/terms/cancel]] |

## SuperCombo Defense 由来の追加用語

Defense page 由来の用語は、守りの timing / defensive option / tactical context として source claim を保持する。公式 source と重なる Drive / invincibility / anti-air mechanics は公式 source または既存 source を優先し、Defense source は input window、wake-up state、armor / punish route の補助根拠として使う。

| Term page | 表記 | 主な source | 主な関連 |
|---|---|---|---|
| [[concepts/terms/blocking]] | Blocking / ガード | [[sources/supercombo-street-fighter-6-defense]] | [[concepts/defense]], [[concepts/terms/blockstring]], [[concepts/terms/cross-up]], [[concepts/terms/drive-parry]] |
| [[concepts/terms/throw-escape]] | Throw Escape / Throw Tech | [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/defense]], [[concepts/terms/throw]], [[concepts/terms/shimmy]] |
| [[concepts/terms/drive-parry]] | Drive Parry / ドライブパリィ | [[sources/capcom-official-fightingground-battle-system]], [[sources/supercombo-street-fighter-6-gauges]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/drive-system]], [[concepts/defense]], [[concepts/terms/blocking]], [[concepts/terms/perfect-parry]] |
| [[concepts/terms/wake-up]] | Wake-up / 起き上がり | [[sources/supercombo-street-fighter-6-defense]], [[sources/supercombo-street-fighter-6-hud]] | [[concepts/defense]], [[concepts/offense]], [[concepts/terms/oki]], [[concepts/terms/reversal]] |
| [[concepts/terms/reversal]] | Reversal / リバーサル | [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/defense]], [[concepts/frame-data]], [[concepts/terms/wake-up]], [[concepts/terms/invincible-move]] |
| [[concepts/terms/armor]] | Armor / アーマー | [[sources/supercombo-street-fighter-6-defense]], [[sources/supercombo-street-fighter-6-gauges]] | [[concepts/defense]], [[concepts/drive-system]], [[concepts/terms/drive-impact]], [[concepts/terms/armor-break]] |
| [[concepts/terms/anti-air]] | 対空 / anti-air | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/defense]], [[concepts/terms/cross-up]], [[concepts/drive-system]] |
| [[concepts/terms/guaranteed-punish]] | 確定反撃 / punish route | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-defense]] | [[concepts/defense]], [[concepts/frame-data]], [[concepts/terms/punish-counter]] |

## SuperCombo HUD icon 由来の追加用語

HUD icon 由来の用語は、画面上の表示 cue として source claim を保持する。公式 source と重なる mechanics は公式 source を優先し、HUD source は visual/community evidence として扱う。

| Term page | HUD 表記 | 主な source | 主な関連 |
|---|---|---|---|
| [[concepts/terms/combo-counter]] | Combo Counter | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/frame-data]], [[concepts/terms/hit-confirm]], [[concepts/terms/damage-scaling]] |
| [[concepts/terms/counter-hit]] | Counter-hit | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-offense]] | [[concepts/frame-data]], [[concepts/offense]], [[concepts/terms/frame-advantage]], [[concepts/terms/punish-counter]] |
| [[concepts/terms/punish-counter]] | Punish Counter | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-offense]] | [[concepts/terms/counter-hit]], [[concepts/terms/frame-advantage]], [[concepts/terms/throw]] |
| [[concepts/terms/forced-knockdown]] | Forced Knockdown | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/juggle-system]], [[concepts/terms/air-reset]], [[concepts/terms/hard-knockdown]] |
| [[concepts/terms/cross-up]] | Cross-up | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/anti-air]], [[concepts/terms/oki]] |
| [[concepts/terms/hard-knockdown]] | Hard Knockdown / HKD | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/oki]], [[concepts/terms/punish-counter]] |
| [[concepts/terms/reversal]] | Reversal | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/frame-data]], [[concepts/terms/invincible-move]], [[concepts/terms/drive-reversal]] |
| [[concepts/terms/throw-escape]] | Throw Escape / Throw Tech | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/shimmy]], [[concepts/terms/punish-counter]] |
| [[concepts/terms/stun]] | Stun/Dizzy | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-hud]], [[sources/supercombo-street-fighter-6-gauges]], [[sources/supercombo-street-fighter-6-offense]] | [[concepts/drive-system]], [[concepts/offense]], [[concepts/terms/burnout]], [[concepts/terms/drive-impact]] |
| [[concepts/terms/armor-break]] | Armor Break | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/drive-impact]], [[concepts/terms/drive-reversal]], [[concepts/terms/chain]] |
| [[concepts/terms/crush]] | Crush | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/drive-impact]], [[concepts/terms/corner]], [[concepts/terms/wall-bounce]] |
| [[concepts/terms/lock]] | Lock | [[sources/supercombo-street-fighter-6-hud]] | [[concepts/terms/drive-impact]], [[concepts/terms/corner]], [[concepts/terms/crush]] |

## 未解決の質問

- SuperCombo glossary / HUD / Gauges / Offense / Defense など community source を追加した時、どの用語で意味差分が出るか。
- Term page から個別の frame-data row や question page へ、どの粒度で backlink を張るか。
- SuperCombo Gauges の `numeric-tables.json` schema を、他の gauge / system numeric source の標準 output にするか。
