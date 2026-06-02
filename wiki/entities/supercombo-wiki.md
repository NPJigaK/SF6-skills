---
type: entity
entity_type: other
created: 2026-05-26
updated: 2026-06-02
status: active
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
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

SuperCombo Wiki は、この wiki が最初に ingest した Street Fighter 6 glossary source と、JP / Ryu / Zangief / Ingrid frame-data community raw 取得データの掲載元。現在の SuperCombo frame-data raw entrypoint は `raw/frame-data/supercombo/<character>/`。JP / Ryu / Zangief / Ingrid では、公式 Classic data を正とする SuperCombo 補助列付き output も作成済み。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-26 | Street Fighter 6 glossary page を Obsidian Web Clipper で `raw/articles/` に保存した。 | [[sources/supercombo-street-fighter-6-glossary]] |
| 2026-05-31 | JP frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-jp-frame-data]] |
| 2026-05-31 | Ryu frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-ryu-frame-data]] |
| 2026-06-02 | Zangief frame-data page を Scrapling で raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像として保存した。 | [[sources/supercombo-zangief-frame-data]] |
| 2026-06-02 | Ingrid frame-data page を raw wikitext、Cargo API、表示 DOM、タブ別スクリーンショット、画像参照情報として保存した。 | [[sources/supercombo-ingrid-frame-data]] |
| 2026-06-02 | Ingrid の SuperCombo raw と公式 Classic data を照合し、補助列付き output のレビュー対象 26 行を accepted にした。 | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]], [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] |

## 関連する主張

- 現在の wiki には SuperCombo Wiki 由来の source page が 5 つある。
- SuperCombo Wiki は community wiki source として扱い、公式 Capcom source より低い confidence で使う。
- JP / Ryu / Zangief / Ingrid frame-data 取得データは official data と重なる基本フレーム値の正とはせず、公式にない notes、range、juggle、hitbox image などの候補 source として保持する。公式 + SuperCombo 補助 output では公式列を正とし、SuperCombo は `supercombo_*` 列に入れる。
- JP / Ryu / Zangief / Ingrid frame-data raw は latest mirror 固定パスに保存し、source revision は各 manifest の `source_revision` で追う。
- Ingrid は imageinfo で face / portrait の 2 件しか解決できていないため、move / hitbox 画像の利用には追加確認が必要。

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[syntheses/frame-data-raw-layout]]
- [[concepts/fighting-game-notation]]
- [[concepts/juggle-system]]

## 未解決の質問

- 追加 source ingest 後、community wiki source の標準 confidence policy を定義するべきか。
- Zangief / Ingrid の SuperCombo name override と review flags を標準 policy として採用できるか。
- Ingrid の imageinfo missing 156 件を、source 側の欠損として扱うか、filename 正規化で再解決するか。
- JP / Ryu / Zangief / Ingrid 以外の SuperCombo frame-data pages も同じ raw/Cargo/DOM/screenshot/image capture schema で取得するべきか。
