---
type: source
source_type: community_frame_data
title: "SuperCombo Zangief フレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/frame-data/supercombo/zangief/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Zangief/Frame_data"
created: 2026-06-02
updated: 2026-06-02
captured_at_utc: "2026-06-01T21:41:34Z"
status: active
confidence: medium
tags:
  - sf6
  - supercombo
  - frame-data
  - community
aliases:
  - "Zangief SuperCombo frame data"
  - "ザンギエフ SuperCombo フレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
related_entities:
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/zangief]]"
---

# ソース: SuperCombo Zangief フレームデータ

## 1行要約

SuperCombo Wiki の Zangief フレームデータを、`Data?action=raw` の生 wikitext、Cargo API、表示ページ DOM、5種類のタブ別スクリーンショット、参照画像として保存した community source ページ。

## 重要ポイント

1. raw snapshot（原本スナップショット）は `raw/frame-data/supercombo/zangief/` 配下の latest mirror 固定パスに保存されている。source revision は path ではなく manifest の `capture_label` と `source_revision` で追う。
2. 生データの中心は `Street_Fighter_6/Zangief/Data?action=raw` で、`CharacterData-SF6` が 1 件、`FrameData-SF6` が 68 件ある。
3. 表示ページ `Street_Fighter_6/Zangief/Frame_data?action=raw` は、Character Data と 4 section の表示テーブルを Cargo query で組み立てている。保存した表示 Cargo query は 21 件。
4. `Normals and Target Combos`、`Drive and Throw`、`Specials`、`Supers` は、それぞれ `General`、`Details`、`Meter`、`Properties`、`Notes` のタブを持つ。DOM 取得と validator は 4 section x 5 tab = 20 表を照合している。
5. Cargo API から取得した `SF6_FrameData` は 68 行、`SF6_CharacterData` は 1 行で、raw template の件数と一致する。
6. 画像参照は 185 件、distinct filename は 169 件。MediaWiki `imageinfo` で 165 件を解決し、165 件を `raw/frame-data/supercombo/zangief/images/files/` に保存した。
7. `6HPHK` と `720+P` は同じ input を持つ複数 row があるため、SuperCombo raw の行識別には `moveId` を使う。input は表示・検索用であり、主キーにはしない。
8. Zangief は 360 / 720 motion、近距離/中距離/遠距離版、hold 版、CA 版の対応があるため、公式 Classic との照合では Zangief 専用の name override を使って `move_id` に対応させている。
9. この source は community data なので、公式 Capcom data と重なる基本フレーム値では公式を正とする。SuperCombo は公式にない range、juggle、hitbox image、notes などを後で追加統合する候補として扱う。
10. レビュー用の派生 CSV/JSON と公式 Zangief Classic との照合結果は `wiki/outputs/data/supercombo/frame-data/zangief/` と [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]] に保存している。
11. 公式列を保持した補助列付き output は `wiki/outputs/data/enriched/frame-data/zangief/` と [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] に保存している。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| Zangief の SuperCombo raw data は 1 件の character template と 68 件の frame template を含む。 | `raw/frame-data/supercombo/zangief/data.raw.wikitext`; `raw/frame-data/supercombo/zangief/data.templates.json`; `raw/frame-data/supercombo/zangief/validation.json` | high | validator で raw template count と Cargo row count を照合済み。 |
| raw path は latest mirror 固定パスで、source revision は manifest の `capture_label` / `source_revision` で追う。 | `raw/frame-data/supercombo/zangief/manifest.json` | high | `storage_policy` は `latest_frame_data_mirror`。`capture_label` は `2026-06-01`。 |
| 表示ページは 21 件の Cargo query で Character Data と frame table を作っている。 | `raw/frame-data/supercombo/zangief/frame-data.raw.wikitext`; `raw/frame-data/supercombo/zangief/frame-data.cargo-queries.json` | high | Character Data 1 件、section/tab 用 query 20 件。 |
| 4 section x 5 tab の表示 table は raw/Cargo から期待される header、row count、input order、cell values と照合済み。 | `raw/frame-data/supercombo/zangief/rendered/tables.dom.json`; `raw/frame-data/supercombo/zangief/validation.json` | high | Notes も含め、20 table comparisons を実行。 |
| `SF6_FrameData` は move type として ground_normal 23、air_normal 9、drive 6、throw 6、special 15、super 5、taunt 4 を含む。 | `raw/frame-data/supercombo/zangief/validation.json` | high | taunt は表示ページの 4 section には含まれないが、raw/Cargo row として保存されている。 |
| duplicate input は `6HPHK` と `720+P` の 2 種類。 | `raw/frame-data/supercombo/zangief/validation.json`; `raw/frame-data/supercombo/zangief/data.templates.json` | high | `6HPHK` は block/recovery、`720+P` は SA3/CA の variant。 |
| Data page の最新 revision は 2026-06-01T07:31:24Z、Frame data 表示ページの revision は 2024-10-19T05:08:24Z。 | `raw/frame-data/supercombo/zangief/api/page-metadata.json` | high | Data page は pageid 69264 / revid 365204、Frame data page は pageid 69274 / revid 310361。 |
| 公式 Zangief Classic との照合は 46 件の自動一致、24 件の Zangief / 汎用 name override による一致、2 件の公式側未照合を含む。 | `wiki/outputs/data/supercombo/frame-data/zangief/crosswalk-summary.json` | high | 公式側未照合は前方ステップ / 後方ステップ。 |
| 補助列付き output は 45 件の `enriched`、25 件の `enriched_reviewed`、2 件の `official_only` を含む。 | `wiki/outputs/data/enriched/frame-data/zangief/summary.json` | high | 25 件のレビュー対象行は `accepted` 済み。SuperCombo-only rows は taunt 4 件。 |

## データ構造メモ

- `data.raw.wikitext` は SuperCombo の raw template source。値の正規化や翻訳はしていない。
- `data.templates.json` は `CharacterData-SF6` / `FrameData-SF6` template を機械的に抽出した raw-adjacent JSON。
- `cargo/frame-data.json` と `cargo/character-data.json` は SuperCombo の Cargo API から取得した表データ。
- `rendered/tables.dom.json` は実際に表示された table の DOM text / HTML / image refs / tab state を保存する。
- `screenshots/*.png` は `General`、`Details`、`Meter`、`Properties`、`Notes` の各タブをページ全体で保存する。
- `imageinfo.json` と `image-manifest.json` は画像参照、MediaWiki imageinfo、ダウンロード結果を保存する。

## 既存 wiki との矛盾または更新

- SuperCombo は community source なので、公式 Capcom source と同じ項目がある場合は Capcom 公式 data を優先する。今回の取得は、SuperCombo 側を削らず完全 raw source として保持し、後続の照合 / merge policy で official と照合するための基礎データ。
- input が同じでも `moveId`、挙動、条件、notes が異なる row がある。したがって SuperCombo raw の主キーは `moveId` とし、input は主キーにしない。
- `taunt` move type は raw/Cargo に含まれるが、表示ページの 4 section x 5 tab validation 対象には入っていない。
- Zangief では公式 input token の `key-circle` を `360+`、2回転を `720+` として扱う必要があり、汎用 input-only matching だけでは SuperCombo row を十分に対応できない。

## 未解決の質問

- `imageinfo` で missing になった 4 件の画像参照を、SuperCombo 側の削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。

## ソースメモ

- 原本 manifest: `raw/frame-data/supercombo/zangief/manifest.json`
- 原本 metadata: `raw/frame-data/supercombo/zangief/metadata.json`
- 原本 wikitext:
  - `raw/frame-data/supercombo/zangief/data.raw.wikitext`
  - `raw/frame-data/supercombo/zangief/frame-data.raw.wikitext`
- Cargo API データ:
  - `raw/frame-data/supercombo/zangief/cargo/frame-data.json`
  - `raw/frame-data/supercombo/zangief/cargo/character-data.json`
- 表示 DOM: `raw/frame-data/supercombo/zangief/rendered/tables.dom.json`
- スクリーンショット: `raw/frame-data/supercombo/zangief/screenshots/`
- 画像: `raw/frame-data/supercombo/zangief/images/files/`
- 検証結果: `raw/frame-data/supercombo/zangief/validation.json`
- 派生 output: `wiki/outputs/data/supercombo/frame-data/zangief/`
- 照合レポート: [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]]
- 補助列付き output: `wiki/outputs/data/enriched/frame-data/zangief/`
- 補助列付きレポート: [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]
