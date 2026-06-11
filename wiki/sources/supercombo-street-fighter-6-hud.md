---
type: source
source_type: wiki_page
title: "Street Fighter 6/HUD"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/hud/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/HUD"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-01-03T12:40:35Z
captured_at_utc: 2026-06-11T01:00:31Z
status: active
confidence: medium
tags:
  - sf6
  - hud
  - ui
  - community-wiki
  - web-page-capture
  - visual-source
aliases:
  - "SF6 HUD"
  - "Street Fighter 6 HUD"
  - "ストリートファイター6 HUD"
related_concepts:
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 HUD

## 1行要約

SuperCombo Wiki の Street Fighter 6 HUD page を MediaWiki wikitext、HTML、rendered DOM、HUD 関連画像、scoped screenshots として保存した raw source。Battle HUD の表示要素、HUD icon の意味、Health Bar Reference を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/hud/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Battle HUD section は Vitality Gauge、Drive Gauge、Timer、Round Count、Attribute Icon、Character Icon、Super Art Gauge の表示要素を説明する。
3. HUD Icons section は Combo Counter、Counter-hit、Punish Counter、Forced Knockdown、Cross-up、Hard Knockdown、Reversal、Throw Escape、Stun/Dizzy、Armor Break、Crush、Lock の icon と説明を含む。
4. Health Bar Reference section は `SF6_Health_Bars_SA3_Scaling.png` を参照し、標準 10,000 HP opponent に対する SA3 / CA minimum scaling の目安を説明する。
5. この page は画像情報が重要なので、本文に明示された HUD semantic content media と rendered content media を保存した。`images/files/` には Battle HUD、Health Bar Reference、HUD icon 12 件の計 14 original files を置く。
6. MediaWiki API の `prop=images` は template transclusion 後の画像を 44 件返すが、HUD 本文外の navigation / character icon 30 件は raw media download の対象外にした。除外一覧は `metadata.json` の `excluded_api_image_titles` で provenance として保持する。
7. Source freshness は MediaWiki revid `345794`、revision timestamp `2026-01-03T12:40:35Z`。Raw 取得時刻は `2026-06-11T01:00:31Z`。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| HUD page は Battle HUD の表示要素として Vitality Gauge、Drive Gauge、Timer、Round Count、Attribute Icon、Character Icon、Super Art Gauge を説明している。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/SF6_Battle_HUD.jpg` | medium | community wiki source。画像は表示位置の確認に使う。 |
| Drive Gauge は Drive actions の resource として説明され、空になると Burnout になり、完全回復まで Drive-related techniques が使えないとされる。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext` | medium | 公式 source と重なる mechanics claim は公式 source を優先する。 |
| Super Art Gauge は attack が hit すると増え、最大 3 stocks まで保持し、round 間で carry over すると説明される。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext` | medium | 公式 source と照合可能な補助 claim。 |
| Combo Counter は現在の combo hit 数を示し、sequence が true combo かを判断する補助になると説明される。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/SF6_icon_combocount.png` | medium | HUD icon の display cue として扱う。 |
| Counter-hit と Punish Counter icon は、それぞれ相手攻撃の startup / active への割り込み、相手の recovery への punish として説明される。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/SF6_icon_counterhit.png`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/SF6_icon_punishcounter.png` | medium | advantage / damage 数値はこの page ではなく公式 term source を優先する。 |
| Forced Knockdown、Hard Knockdown、Reversal、Throw Escape などの icon は、match 中の状態表示として説明される。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/` | medium | 個別 mechanics の詳細 source ではなく HUD 表示 source。 |
| Stun/Dizzy、Armor Break、Crush、Lock icon は Drive Impact、Burnout、corner、armor、true blockstring と関係する表示として説明される。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/` | medium | 公式 Drive / Burnout source と衝突する場合は公式 source を優先する。 |
| Health Bar Reference は標準 10,000 HP opponent に対する minimum scaling の目安として SA3 / CA damage を画像で示す。 | `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/hud/images/files/SF6_Health_Bars_SA3_Scaling.png` | medium | 近似的な visual reference であり、公式 damage data ではない。 |
| 2026-06-11 capture は MediaWiki `prop=images` 44 件のうち、HUD semantic content media 14 件だけを imageinfo / original download 対象にし、navigation / template image 30 件を除外した。 | `raw/web-pages/wiki.supercombo.gg/hud/manifest.json`, `raw/web-pages/wiki.supercombo.gg/hud/metadata.json`, `raw/web-pages/wiki.supercombo.gg/hud/validation.json` | high | character icon 画像は HUD source の本文 media として扱わない。 |

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- Drive Gauge、Burnout、Super Art Gauge、Drive Impact など、公式 source と重なる mechanics claim は公式 source を優先する。
- この source は HUD 表示と visual evidence の source として使う。個別 frame value、damage value、advantage、system rule の正本にはしない。
- Character navigation icon は HUD page 本文の source content ではないため、raw media としては保存せず、除外した provenance としてのみ記録する。

## 未解決の質問

- Capcom 公式の HUD / game screen 説明 source を追加 ingest して、HUD 表示要素と icon 表示の official evidence を補うか。
- HUD icon ごとに個別 term page へ source claim を追加するか、それとも HUD source page と [[concepts/frame-data]] の補助 claim に留めるか。
- 将来の動画・画像質問向けに、scoped screenshots、original media、large video capture の保存基準をどこまで細分化するか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/hud/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`
- Image manifest: `raw/web-pages/wiki.supercombo.gg/hud/images/manifest.json`
- Original HUD media: `raw/web-pages/wiki.supercombo.gg/hud/images/files/`
- Rendered HUD media: `raw/web-pages/wiki.supercombo.gg/hud/images/rendered/`
- Scoped screenshots: `raw/web-pages/wiki.supercombo.gg/hud/screenshots/`
- Validation: `raw/web-pages/wiki.supercombo.gg/hud/validation.json`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/HUD
