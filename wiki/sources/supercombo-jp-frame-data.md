---
type: source
source_type: community_frame_data
title: "SuperCombo JP フレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/supercombo/frame-data/2026-05-31/jp/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Frame_data"
created: 2026-05-31
updated: 2026-05-31
captured_at_utc: "2026-05-30T21:38:52Z"
status: active
confidence: medium
tags:
  - sf6
  - supercombo
  - frame-data
  - community
aliases:
  - "JP SuperCombo frame data"
  - "JP SuperCombo フレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
related_entities:
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/jp]]"
---

# ソース: SuperCombo JP フレームデータ

## 1行要約

SuperCombo Wiki の JP フレームデータを、`Data?action=raw` の生 wikitext、Cargo API、表示ページ DOM、5種類のタブ別スクリーンショット、参照画像として保存した community source page。

## 重要ポイント

1. 生データの中心は `Street_Fighter_6/JP/Data?action=raw` で、`CharacterData-SF6` が 1 件、`FrameData-SF6` が 64 件ある。
2. 表示ページ `Street_Fighter_6/JP/Frame_data?action=raw` は、Character Data と 4 section の表示テーブルを Cargo query で組み立てている。保存した表示 Cargo query は 21 件。
3. `Normals and Target Combos`、`Drive and Throw`、`Specials`、`Supers` は、それぞれ `General`、`Details`、`Meter`、`Properties`、`Notes` のタブを持つ。DOM capture と validator は 4 section x 5 tab = 20 表を照合している。
4. Cargo API から取得した `SF6_FrameData` は 64 行、`SF6_CharacterData` は 1 行で、raw template の件数と一致する。
5. 画像参照は 143 件、distinct filename は 134 件。MediaWiki `imageinfo` で 123 件を解決し、123 件を `raw/supercombo/frame-data/2026-05-31/jp/images/files/` に保存した。
6. `6HPHK` と `236236K` は同じ input を持つ複数 row があるため、SuperCombo raw の行識別には `moveId` を使う。input は表示・検索用であり、主キーにはしない。
7. この source は community data なので、公式 Capcom data と重なる基本フレーム値では公式を正とする。SuperCombo は公式にない range、juggle、hitbox image、notes などを後で追加統合する候補として扱う。
## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| JP の SuperCombo raw data は 1 件の character template と 64 件の frame template を含む。 | `raw/supercombo/frame-data/2026-05-31/jp/data.raw.wikitext`; `raw/supercombo/frame-data/2026-05-31/jp/data.templates.json`; `raw/supercombo/frame-data/2026-05-31/jp/validation.json` | high | validator で raw template count と Cargo row count を照合済み。 |
| 表示ページは 21 件の Cargo query で Character Data と frame table を作っている。 | `raw/supercombo/frame-data/2026-05-31/jp/frame-data.raw.wikitext`; `raw/supercombo/frame-data/2026-05-31/jp/frame-data.cargo-queries.json` | high | Character Data 1 件、section/tab 用 query 20 件。 |
| 4 section x 5 tab の表示 table は raw/Cargo から期待される header、row count、input order、cell values と照合済み。 | `raw/supercombo/frame-data/2026-05-31/jp/rendered/tables.dom.json`; `raw/supercombo/frame-data/2026-05-31/jp/validation.json` | high | Notes も含め、20 table comparisons を実行。 |
| タブ別スクリーンショットはページ上部、Character Data、各 tab の table、下部ナビゲーション、footer を含む。 | `raw/supercombo/frame-data/2026-05-31/jp/screenshots/general.png`; `details.png`; `meter.png`; `properties.png`; `notes.png` | high | 5枚を目視確認済み。ad/iframe/sticky UI は screenshot から除去。 |
| `SF6_FrameData` は move type として ground_normal 20、air_normal 6、drive 6、throw 3、special 22、super 4、taunt 3 を含む。 | `raw/supercombo/frame-data/2026-05-31/jp/validation.json` | high | taunt は表示ページの 4 section には含まれないが、raw/Cargo row として保存されている。 |
| `6HPHK` と `236236K` は duplicate input を持つ。 | `raw/supercombo/frame-data/2026-05-31/jp/validation.json`; `raw/supercombo/frame-data/2026-05-31/jp/data.templates.json` | high | `6HPHK` は `jp_6hphk` / `jp_6hphk_recovery`、`236236K` は `jp_236236k` / `jp_236236k(ca)`。 |
| Data page の最新 revision は 2026-05-30T01:25:44Z、Frame data 表示ページの revision は 2024-10-19T05:16:43Z。 | `raw/supercombo/frame-data/2026-05-31/jp/api/page-metadata.json` | high | Data page は pageid 67945 / revid 364994、Frame data page は pageid 68384 / revid 310371。 |

## データ構造メモ

- `data.raw.wikitext` は SuperCombo の raw template source。値の正規化や翻訳はしていない。
- `data.templates.json` は `CharacterData-SF6` / `FrameData-SF6` template を機械的に抽出した raw-adjacent JSON。
- `cargo/frame-data.json` と `cargo/character-data.json` は SuperCombo の Cargo API から取得した表データ。
- `rendered/tables.dom.json` は実際に表示された table の DOM text / HTML / image refs / tab state を保存する。
- `screenshots/*.png` は `General`、`Details`、`Meter`、`Properties`、`Notes` の各タブをページ全体で保存する。
- `imageinfo.json` と `image-manifest.json` は画像参照、MediaWiki imageinfo、download 結果を保存する。

## 既存 wiki との矛盾または更新

- SuperCombo は community source なので、公式 Capcom source と同じ項目がある場合は Capcom 公式 data を優先する。今回の capture は、SuperCombo 側を削らず完全 raw source として保持し、後続の crosswalk / merge policy で official と照合するための基礎データ。
- input が同じでも `moveId`、挙動、条件、notes が異なる row がある。したがって SuperCombo raw の主キーは `moveId` とし、input は主キーにしない。
- `taunt` move type は raw/Cargo に含まれるが、表示ページの 4 section x 5 tab validation 対象には入っていない。

## 未解決の質問

- 候補 crosswalk の `matched_manual` 4件、多対一対応 rows、SuperCombo-only rows を人間レビューし、正式な merge policy に昇格できるか。
- `imageinfo` で missing になった 11 件の画像参照を、SuperCombo 側の削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
- SuperCombo の HTML 装飾付き frame advantage を、公式 CSV と比較可能な値へ正規化する schema をいつ作るか。

## ソースメモ

- Raw manifest: `raw/supercombo/frame-data/2026-05-31/jp/manifest.json`
- Raw metadata: `raw/supercombo/frame-data/2026-05-31/jp/metadata.json`
- Raw wikitext:
  - `raw/supercombo/frame-data/2026-05-31/jp/data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/jp/frame-data.raw.wikitext`
- Cargo API:
  - `raw/supercombo/frame-data/2026-05-31/jp/cargo/frame-data.json`
  - `raw/supercombo/frame-data/2026-05-31/jp/cargo/character-data.json`
- Rendered DOM: `raw/supercombo/frame-data/2026-05-31/jp/rendered/tables.dom.json`
- Screenshots: `raw/supercombo/frame-data/2026-05-31/jp/screenshots/`
- Images: `raw/supercombo/frame-data/2026-05-31/jp/images/files/`
- Validation: `raw/supercombo/frame-data/2026-05-31/jp/validation.json`
