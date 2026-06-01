---
type: source
source_type: community_frame_data
title: "SuperCombo JP フレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/frame-data/supercombo/jp/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/JP/Frame_data"
created: 2026-05-31
updated: 2026-06-01
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

1. raw snapshot は `raw/frame-data/supercombo/jp/` 配下の latest mirror 固定パスに保存されている。source revision は path ではなく manifest の `capture_label` と `source_revision` で追う。
2. 生データの中心は `Street_Fighter_6/JP/Data?action=raw` で、`CharacterData-SF6` が 1 件、`FrameData-SF6` が 64 件ある。
3. 表示ページ `Street_Fighter_6/JP/Frame_data?action=raw` は、Character Data と 4 section の表示テーブルを Cargo query で組み立てている。保存した表示 Cargo query は 21 件。
4. `Normals and Target Combos`、`Drive and Throw`、`Specials`、`Supers` は、それぞれ `General`、`Details`、`Meter`、`Properties`、`Notes` のタブを持つ。DOM capture と validator は 4 section x 5 tab = 20 表を照合している。
5. Cargo API から取得した `SF6_FrameData` は 64 行、`SF6_CharacterData` は 1 行で、raw template の件数と一致する。
6. 画像参照は 143 件、distinct filename は 134 件。MediaWiki `imageinfo` で 123 件を解決し、123 件を `raw/frame-data/supercombo/jp/images/files/` に保存した。
7. `6HPHK` と `236236K` は同じ input を持つ複数 row があるため、SuperCombo raw の行識別には `moveId` を使う。input は表示・検索用であり、主キーにはしない。
8. この source は community data なので、公式 Capcom data と重なる基本フレーム値では公式を正とする。SuperCombo は公式にない range、juggle、hitbox image、notes などを後で追加統合する候補として扱う。
9. Review 用の派生 CSV/JSON と公式 JP Classic との候補 crosswalk は `wiki/outputs/data/supercombo/frame-data/jp/` と [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]] に保存している。
10. 公式列を保持した enriched output は `wiki/outputs/data/enriched/frame-data/jp/` と [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]] に保存している。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| JP の SuperCombo raw data は 1 件の character template と 64 件の frame template を含む。 | `raw/frame-data/supercombo/jp/data.raw.wikitext`; `raw/frame-data/supercombo/jp/data.templates.json`; `raw/frame-data/supercombo/jp/validation.json` | high | validator で raw template count と Cargo row count を照合済み。 |
| raw path は latest mirror 固定パスで、source revision は manifest の `capture_label` / `source_revision` で追う。 | `raw/frame-data/supercombo/jp/manifest.json` | high | `storage_policy` は `latest_frame_data_mirror`。`capture_label` は `2026-05-30`。 |
| 表示ページは 21 件の Cargo query で Character Data と frame table を作っている。 | `raw/frame-data/supercombo/jp/frame-data.raw.wikitext`; `raw/frame-data/supercombo/jp/frame-data.cargo-queries.json` | high | Character Data 1 件、section/tab 用 query 20 件。 |
| 4 section x 5 tab の表示 table は raw/Cargo から期待される header、row count、input order、cell values と照合済み。 | `raw/frame-data/supercombo/jp/rendered/tables.dom.json`; `raw/frame-data/supercombo/jp/validation.json` | high | Notes も含め、20 table comparisons を実行。 |
| タブ別スクリーンショットはページ上部、Character Data、各 tab の table、下部ナビゲーション、footer を含む。 | `raw/frame-data/supercombo/jp/screenshots/general.png`; `details.png`; `meter.png`; `properties.png`; `notes.png` | high | 5枚を目視確認済み。ad/iframe/sticky UI は screenshot から除去。 |
| `SF6_FrameData` は move type として ground_normal 20、air_normal 6、drive 6、throw 3、special 22、super 4、taunt 3 を含む。 | `raw/frame-data/supercombo/jp/validation.json` | high | taunt は表示ページの 4 section には含まれないが、raw/Cargo row として保存されている。 |
| `6HPHK` と `236236K` は duplicate input を持つ。 | `raw/frame-data/supercombo/jp/validation.json`; `raw/frame-data/supercombo/jp/data.templates.json` | high | `6HPHK` は `jp_6hphk` / `jp_6hphk_recovery`、`236236K` は `jp_236236k` / `jp_236236k(ca)`。 |
| Data page の最新 revision は 2026-05-30T01:25:44Z、Frame data 表示ページの revision は 2024-10-19T05:16:43Z。 | `raw/frame-data/supercombo/jp/api/page-metadata.json` | high | Data page は pageid 67945 / revid 364994、Frame data page は pageid 68384 / revid 310371。 |

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
- 2026-05-31 の人間レビューで、`ヴィーハト・アクノ`、`パリィドライブラッシュ`、`キャンセルドライブラッシュ` は `supplemental_link`、`ヴィーハト・チェーニ` は `non_additive_supplemental_damage`、`SA2 ラヴーシュカ` は `conflict_supplemental_only` として扱うことになった。

## 未解決の質問

- 人間レビュー済みの5件を正式 merge policy として他 character に一般化できるか。多対一対応 rows と SuperCombo-only rows の扱いをどう確定するか。
- `imageinfo` で missing になった 11 件の画像参照を、SuperCombo 側の削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
- SuperCombo の HTML 装飾付き frame advantage を、公式 CSV と比較可能な値へ正規化する schema をいつ作るか。

## ソースメモ

- Raw manifest: `raw/frame-data/supercombo/jp/manifest.json`
- Raw metadata: `raw/frame-data/supercombo/jp/metadata.json`
- Raw wikitext:
  - `raw/frame-data/supercombo/jp/data.raw.wikitext`
  - `raw/frame-data/supercombo/jp/frame-data.raw.wikitext`
- Cargo API:
  - `raw/frame-data/supercombo/jp/cargo/frame-data.json`
  - `raw/frame-data/supercombo/jp/cargo/character-data.json`
- Rendered DOM: `raw/frame-data/supercombo/jp/rendered/tables.dom.json`
- Screenshots: `raw/frame-data/supercombo/jp/screenshots/`
- Images: `raw/frame-data/supercombo/jp/images/files/`
- Validation: `raw/frame-data/supercombo/jp/validation.json`
- Derived outputs: `wiki/outputs/data/supercombo/frame-data/jp/`
- Crosswalk report: [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]]
- Enriched outputs: `wiki/outputs/data/enriched/frame-data/jp/`
- Enriched report: [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]]
