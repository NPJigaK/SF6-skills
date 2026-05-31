---
type: entity
entity_type: other
created: 2026-05-26
updated: 2026-05-31
status: active
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
aliases:
  - "SuperCombo Wiki"
tags:
  - source
  - community-wiki
---

# SuperCombo Wiki

## 要約

SuperCombo Wiki は、この wiki が最初に ingest した Street Fighter 6 glossary source と、JP / Ryu frame-data raw community capture の掲載元。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-26 | Street Fighter 6 glossary page を Obsidian Web Clipper で `raw/articles/` に保存した。 | [[sources/supercombo-street-fighter-6-glossary]] |
| 2026-05-31 | JP frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、tab screenshots、画像として保存した。 | [[sources/supercombo-jp-frame-data]] |
| 2026-05-31 | Ryu frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、tab screenshots、画像として保存した。 | [[sources/supercombo-ryu-frame-data]] |

## 関連する主張

- 現在の wiki には SuperCombo Wiki 由来の source page が 3 つある。
- SuperCombo Wiki は community wiki source として扱い、公式 Capcom source より低い confidence で使う。
- JP / Ryu frame-data capture は official data と重なる基本フレーム値の正とはせず、公式にない notes、range、juggle、hitbox image などの候補 source として保持する。

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/juggle-system]]

## 未解決の質問

- 追加 source ingest 後、community wiki source の標準 confidence policy を定義するべきか。
- JP / Ryu 以外の SuperCombo frame-data pages も同じ raw/Cargo/DOM/screenshot/image capture schema で取得するべきか。
