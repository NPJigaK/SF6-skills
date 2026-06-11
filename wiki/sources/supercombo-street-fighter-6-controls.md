---
type: source
source_type: wiki_page
title: "Street Fighter 6/Controls"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/controls/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Controls"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-06-03T09:40:46Z
captured_at_utc: 2026-06-11T00:01:49Z
status: active
confidence: medium
tags:
  - sf6
  - controls
  - notation
  - community-wiki
  - web-page-capture
aliases:
  - "SF6 controls"
  - "ストリートファイター6 操作"
  - "Street Fighter 6 Controls"
related_concepts:
  - "[[concepts/fighting-game-notation]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Controls

## 1行要約

SuperCombo Wiki の Street Fighter 6 controls page を MediaWiki wikitext、HTML、rendered DOM として保存した raw source。Classic / Modern control type、numpad notation、旧 Street Fighter notation、button nickname を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/controls/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Classic Controls は 6 button control を前提に、movement、block、throw、Drive Parry、Drive Impact、taunt などの基本操作を説明している。
3. Modern Controls は L / M / H、Special Move、Assist、simple input、Assist Combo、Overdrive Art、Super Art、Modern 固有の damage penalty claim を説明している。
4. Notation は、この wiki で使う standard として numpad notation を説明し、direction grid、5 neutral、6 がキャラクターの向きと同じ方向であること、`2LK` / `236HP` などの例を含む。
5. Classic Notation は `cr.`、`st.`、QCF / QCB / DP / RDP / HCF / HCB / SPD / 360 / 720 など、旧来の英語 abbreviations と numpad notation の対応を説明している。
6. Button nickname table は Light Punch = Jab = LP、Medium Punch = Strong = MP、Heavy Punch = Fierce = HP、Light Kick = Short = LK、Medium Kick = Forward = MK、Heavy Kick = Roundhouse = HK の対応を保持する。
7. `api/templates.json` は `Template:Clr` と `Template:Navbox-SF6` 系の直接 template 依存だけを記録する。主要本文は `page.raw.wikitext` に保存されているため、template 本文は保存していない。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| SuperCombo controls page は Classic と Modern の 2 control type を説明し、この wiki の表記は主に Classic notation を想定すると述べている。 | `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext` | medium | community wiki source。 |
| Classic Controls は 8方向移動、後ろ / 下後ろ block、LP / MP / HP、LK / MK / HK、throw、Drive Parry、Drive Impact などの基本操作を説明している。 | `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext` | medium | 公式操作説明ではない。 |
| Modern Controls は L / M / H、Special Move、Assist、simple input Special Move / Super Art、Assist Combo、Overdrive Art を説明し、simple input move の damage penalty claim を含む。 | `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext` | medium | damage penalty は source fact として記録し、公式確認は未実施。 |
| Numpad notation は digital direction を数字に対応させ、5 を neutral、6 をキャラクターが向いている方向として扱う。 | `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/controls/rendered/tables.dom.json` | medium | rendered table 0 / 1 に direction grid と numpad grid がある。 |
| Classic notation は QCF = 236、QCB = 214、DP / SRK = 623、RDP = 421、HCF = 41236、HCB = 63214 などの対応を説明している。 | `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext` | medium | 旧来表記との対応表として扱う。 |
| 2026-06-11 capture は page 本体の MediaWiki revid 365425、revision timestamp 2026-06-03T09:40:46Z を source freshness として記録している。 | `raw/web-pages/wiki.supercombo.gg/controls/manifest.json` | high | `captured_at_utc` は raw 取得時刻であり、source 更新日ではない。 |

## 関連概念

- [[concepts/fighting-game-notation]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- Controls page は [[concepts/fighting-game-notation]] の directional input / button notation の補助 source として追加する。
- Modern Controls の damage penalty や simple input の実戦的評価は source fact として記録し、公式 data または公式説明で上書き確認するまでは断定的な wiki synthesis にしない。

## 未解決の質問

- Capcom 公式の controls / control type 説明 source を ingest して、Modern Controls、simple input damage penalty、button mapping の official evidence を追加するべきか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/controls/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/controls/page.raw.wikitext`
- Rendered table DOM: `raw/web-pages/wiki.supercombo.gg/controls/rendered/tables.dom.json`
- Template 依存一覧: `raw/web-pages/wiki.supercombo.gg/controls/api/templates.json`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/Controls
