---
type: entity
entity_type: other
created: 2026-05-26
updated: 2026-06-11
status: active
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-controls]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[syntheses/frame-data-raw-layout]]"
aliases:
  - "SuperCombo Wiki"
tags:
  - source
  - community-wiki
---

# SuperCombo Wiki

## 要約

SuperCombo Wiki は、この wiki が最初に ingest した Street Fighter 6 glossary source、controls source、HUD source、30 キャラ分の frame-data community source の掲載元。glossary は Drive System、notation、juggle、frame-data terms の補助 source として [[concepts/terms/index]] に統合され、controls は numpad notation、Classic / Modern control type、button notation の補助 source として [[concepts/fighting-game-notation]] に統合されている。HUD は Battle HUD、HUD icon、Health Bar Reference の community / visual source として保持し、HUD Icons section は term pages の display cue claim として集約している。公式 Classic data を正とする SuperCombo 補助列付き output も 30 キャラ分作成済み。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-06-11 | Street Fighter 6 HUD page の HUD Icons section を term pages に集約した。新規9件を作成し、既存3件に HUD display cue claim を追記した。 | [[concepts/terms/index]], [[sources/supercombo-street-fighter-6-hud]] |
| 2026-06-11 | Street Fighter 6 HUD page を web-page capture として保存した。Battle HUD、HUD icon、Health Bar Reference を含む community / visual source として扱う。 | [[sources/supercombo-street-fighter-6-hud]], [[reviews/2026-06-11-supercombo-hud-web-page-capture-review]] |
| 2026-06-11 | Street Fighter 6 controls page を web-page capture として保存した。Classic / Modern control type、numpad notation、button nickname を含む community source として扱う。 | [[sources/supercombo-street-fighter-6-controls]], [[reviews/2026-06-11-supercombo-controls-web-page-capture-review]] |
| 2026-06-09 | Street Fighter 6 glossary page を web-page capture として保存し、Notation Glossary の `ComboLegend-SF6` template 依存も記録した。旧 clipping は削除した。 | [[sources/supercombo-street-fighter-6-glossary]], [[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]] |
| 2026-05-31 | JP frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-jp-frame-data]] |
| 2026-05-31 | Ryu frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-ryu-frame-data]] |
| 2026-06-02 | Zangief frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-zangief-frame-data]] |
| 2026-06-02 | Ingrid frame-data page を raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像参照情報として保存した。 | [[sources/supercombo-ingrid-frame-data]] |
| 2026-06-02 | Ingrid の SuperCombo raw と公式 Classic data を照合し、補助列付き output のレビュー対象 26 行を accepted にした。 | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]], [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] |
| 2026-06-05 | SuperCombo frame-data 30 キャラ分の raw capture、validation、公式 Classic crosswalk、補助列付き output をそろえた。 | [[sources/supercombo-street-fighter-6-frame-data-batch]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] |

## 関連する主張

- 現在の wiki には SuperCombo Wiki 由来の glossary source、個別 frame-data source pages、30キャラ batch source summary がある。
- SuperCombo Wiki は community wiki source として扱い、公式 Capcom source より低い confidence で使う。
- SuperCombo glossary は [[concepts/terms/air-reset]]、[[concepts/terms/cancel]]、[[concepts/terms/chain]]、[[concepts/terms/damage-scaling]]、[[concepts/terms/wall-bounce]] などの term page に community source claim を提供する。
- SuperCombo controls は [[concepts/fighting-game-notation]] に、numpad notation、Classic notation、button nickname、Classic / Modern control type の community source claim を提供する。
- SuperCombo HUD は [[concepts/drive-system]]、[[concepts/frame-data]]、[[concepts/terms/index]] に、Battle HUD の表示要素と HUD icon の community / visual source claim を提供する。ただし character navigation icon は source content ではなく、raw media download から除外した。
- 30キャラ分の SuperCombo frame-data 取得データは official data と重なる基本フレーム値の正とはせず、公式にない notes、range、juggle、hitbox image refs などの補助 source として保持する。公式 + SuperCombo 補助 output では公式列を正とし、SuperCombo は `supercombo_*` 列に入れる。
- SuperCombo frame-data raw は latest mirror 固定パスに保存し、source revision は各 manifest の `source_revision` で追う。
- JP / Ryu / Zangief / Ingrid には既存の人間レビュー済み補助行がある。2026-06-06 の fail-closed policy 以降は accepted 69 行を保持し、複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ未レビュー補助行 1295 行を review queue に残している。
- Ingrid は imageinfo で face / portrait の 2 件しか解決できていないため、move / hitbox 画像の利用には追加確認が必要。

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[syntheses/frame-data-raw-layout]]
- [[concepts/fighting-game-notation]]
- [[concepts/juggle-system]]

## 未解決の質問

- 追加 source ingest 後、community wiki source の標準 confidence policy を定義するべきか。
- Capcom 公式 controls / control type source を追加 ingest して、SuperCombo controls の Modern Controls claim を照合するべきか。
- Capcom 公式 HUD / game screen source を追加 ingest して、SuperCombo HUD の visual claim と照合するべきか。
- Zangief / Ingrid の SuperCombo name override と review flags を標準 policy として採用できるか。
- imageinfo missing 599 件を、source 側の欠損として扱うか、filename 正規化で再解決するか。
- 未レビュー補助行 1295 行をどの順序で人間レビューするか。
