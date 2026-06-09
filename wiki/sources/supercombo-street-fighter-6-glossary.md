---
type: source
source_type: wiki_page
title: "Street Fighter 6/Glossary"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/glossary/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary"
created: 2026-05-26
updated: 2026-06-10
source_updated_at: 2026-01-31T11:22:26Z
captured_at_utc: 2026-06-09T13:47:52Z
status: active
confidence: medium
tags:
  - sf6
  - glossary
  - community-wiki
  - web-page-capture
aliases:
  - "SF6 glossary"
  - "ストリートファイター6 用語集"
related_concepts:
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Glossary

## 1行要約

SuperCombo Wiki の Street Fighter 6 glossary を MediaWiki wikitext、HTML、rendered DOM として保存した raw source。Drive System、frame data、juggle、notation の用語説明を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Drive System では Burnout、Drive Impact、Drive Parry、Drive Reversal、Drive Rush、Overdrive などの用語を説明している。
3. Frame Data では startup、active、recovery、cancel、damage、damage scaling、hit/block advantage、guard などの読み方を説明している。
4. Juggles では Free Juggle、Limited Juggle、Juggle Count、Juggle Start、Juggle Increase、Juggle Limit の関係を説明している。
5. Notation Glossary は wikitext では `{{ComboLegend-SF6}}` テンプレート呼び出しとして現れる。展開後の link、cancel、hold/release、chain、counter hit、jump、delay、tiger knee などの表記は `rendered/tables.dom.json` に保存し、template 本文と revision は `templates/combo-legend-sf6.raw.wikitext` と `api/template-combo-legend-sf6.json` に保存している。
6. 旧 Obsidian Web Clipper clipping は web-page capture で置き換えたため削除した。
7. この取得一式は `storage_policy: updateable_web_page_capture` を持つ更新可能な raw 一式なので、再取得、manifest 補正、validation 更新が可能。ただし翻訳・要約・正規化した raw 上の置き換え版は置かない。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| Drive System は Street Fighter 6 の移動・攻め・守りに関わる共通 meter system として説明されている。 | `raw/web-pages/wiki.supercombo.gg/glossary/page.raw.wikitext` | medium | community wiki source。 |
| frame data 用語は、startup、active、recovery、cancel、damage、guard、hit/block advantage などを含む。 | `raw/web-pages/wiki.supercombo.gg/glossary/page.raw.wikitext` | medium | 公式用語とは異なる可能性がある。 |
| juggle 用語は community-designated terms として説明され、公式 Capcom 用語との差異にも触れている。 | `raw/web-pages/wiki.supercombo.gg/glossary/page.raw.wikitext` | medium | 後続の公式資料で対応関係を確認する必要がある。 |
| notation 用語は `ComboLegend-SF6` の rendered table として展開され、link / cancel / hold / release などの表記を含む。 | `raw/web-pages/wiki.supercombo.gg/glossary/rendered/tables.dom.json`, `raw/web-pages/wiki.supercombo.gg/glossary/templates/combo-legend-sf6.raw.wikitext`, `raw/web-pages/wiki.supercombo.gg/glossary/api/template-combo-legend-sf6.json` | medium | 直接の page wikitext には template invocation がある。template revision は revid `283225`、timestamp `2023-12-11T18:45:25Z`。 |
| 2026-06-09 capture は page 本体の MediaWiki revid 351898、revision timestamp 2026-01-31T11:22:26Z を source freshness として記録している。 | `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json` | high | `captured_at_utc` は raw 取得時刻であり、source 更新日ではない。Notation table の本文は別途 `Template:ComboLegend-SF6` の revision に依存する。 |
| SuperCombo glossary の `storage_policy` は `updateable_web_page_capture`。 | `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json` | high | Web page 取得一式の補正・再取得・manifest 更新を許す。 |

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/juggle-system]]
- [[concepts/fighting-game-notation]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- raw source は英語のまま保存し、日本語説明はこの source page と concept pages に置く。
- 2026-06-09 に `raw/web-pages/` 配下で wikitext / HTML / DOM capture を追加した。旧 Obsidian clipping は削除し、現在の source page は web-page capture を raw entrypoint とする。
- `raw/` は原則不変だが、この取得一式は manifest の `storage_policy` により更新可能な Web capture として扱う。

## 未解決の質問

- 公式 Capcom のシステム用語資料を追加 ingest して、community terms と official terms の対応を確認するべきか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/glossary/page.raw.wikitext`
- Rendered table DOM: `raw/web-pages/wiki.supercombo.gg/glossary/rendered/tables.dom.json`
- Template 依存一覧: `raw/web-pages/wiki.supercombo.gg/glossary/api/templates.json`
- ComboLegend raw wikitext: `raw/web-pages/wiki.supercombo.gg/glossary/templates/combo-legend-sf6.raw.wikitext`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary
