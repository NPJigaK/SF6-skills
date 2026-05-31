---
type: source
source_type: community_frame_data
title: "SuperCombo Ryu フレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/supercombo/frame-data/2026-05-31/ryu/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Ryu/Frame_data"
created: 2026-05-31
updated: 2026-05-31
captured_at_utc: "2026-05-31T06:56:44Z"
status: active
confidence: medium
tags:
  - sf6
  - supercombo
  - frame-data
  - community
aliases:
  - "Ryu SuperCombo frame data"
  - "リュウ SuperCombo フレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
related_entities:
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/ryu]]"
---

# ソース: SuperCombo Ryu フレームデータ

## 1行要約

SuperCombo Wiki の Ryu フレームデータを、`Data?action=raw` の生 wikitext、Cargo API、表示ページ DOM、5種類のタブ別スクリーンショット、参照画像として保存した community source page。

## 重要ポイント

1. 生データの中心は `Street_Fighter_6/Ryu/Data?action=raw` で、`CharacterData-SF6` が 1 件、`FrameData-SF6` が 77 件ある。
2. 表示ページ `Street_Fighter_6/Ryu/Frame_data?action=raw` は、Character Data と 4 section の表示テーブルを Cargo query で組み立てている。保存した表示 Cargo query は 21 件。
3. `Normals and Target Combos`、`Drive and Throw`、`Specials`、`Supers` は、それぞれ `General`、`Details`、`Meter`、`Properties`、`Notes` のタブを持つ。DOM capture と validator は 4 section x 5 tab = 20 表を照合している。
4. Cargo API から取得した `SF6_FrameData` は 77 行、`SF6_CharacterData` は 1 行で、raw template の件数と一致する。
5. 画像参照は 173 件、distinct filename は 134 件。MediaWiki `imageinfo` で 133 件を解決し、133 件を `raw/supercombo/frame-data/2026-05-31/ryu/images/files/` に保存した。
6. `6HPHK`、`236HP`、`236PP`、`214HP`、`214PP`、`236236P`、`214214P`、`214214P (Hold Lv.2)`、`214214P (Hold Lv.3)`、`236236K` は duplicate input を持つため、SuperCombo raw の行識別には `moveId` を使う。
7. この source は community data なので、公式 Capcom data と重なる基本フレーム値では公式を正とする。SuperCombo は公式にない range、juggle、hitbox image、notes などを後で追加統合する候補として扱う。
8. Review 用の派生 CSV/JSON と公式 Ryu Classic との候補 crosswalk は `wiki/outputs/data/supercombo/frame-data/ryu/` と [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]] に保存している。
9. 公式列を保持した enriched output は `wiki/outputs/data/enriched/frame-data/ryu/` と [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] に保存している。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| Ryu の SuperCombo raw data は 1 件の character template と 77 件の frame template を含む。 | `raw/supercombo/frame-data/2026-05-31/ryu/data.raw.wikitext`; `raw/supercombo/frame-data/2026-05-31/ryu/data.templates.json`; `raw/supercombo/frame-data/2026-05-31/ryu/validation.json` | high | validator で raw template count と Cargo row count を照合済み。 |
| 表示ページは 21 件の Cargo query で Character Data と frame table を作っている。 | `raw/supercombo/frame-data/2026-05-31/ryu/frame-data.raw.wikitext`; `raw/supercombo/frame-data/2026-05-31/ryu/frame-data.cargo-queries.json` | high | Character Data 1 件、section/tab 用 query 20 件。 |
| 4 section x 5 tab の表示 table は raw/Cargo から期待される header、row count、input order、cell values と照合済み。 | `raw/supercombo/frame-data/2026-05-31/ryu/rendered/tables.dom.json`; `raw/supercombo/frame-data/2026-05-31/ryu/validation.json` | high | Notes も含め、20 table comparisons を実行。 |
| タブ別スクリーンショットはページ上部、Character Data、各 tab の table、下部ナビゲーション、footer を含む。 | `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/general.png`; `details.png`; `meter.png`; `properties.png`; `notes.png` | high | General と Notes を目視確認済み。ad/iframe/sticky UI は screenshot から除去。 |
| `SF6_FrameData` は move type として ground_normal 20、air_normal 6、drive 6、throw 2、special 29、super 10、taunt 4 を含む。 | `raw/supercombo/frame-data/2026-05-31/ryu/validation.json` | high | validator では `Special` / `Super` の表記ゆれを小文字正規化して集計する。 |
| duplicate input が 10 種類ある。 | `raw/supercombo/frame-data/2026-05-31/ryu/validation.json`; `raw/supercombo/frame-data/2026-05-31/ryu/data.templates.json` | high | Denjin / hold level / CA などの variant が同じ input を共有するため、input は主キーにしない。 |
| Data page の最新 revision は 2026-05-30T01:26:46Z、Frame data 表示ページの revision は 2024-10-19T05:06:40Z。 | `raw/supercombo/frame-data/2026-05-31/ryu/api/page-metadata.json` | high | Data page は pageid 65938 / revid 365005、Frame data page は pageid 68275 / revid 310359。 |

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
- Ryu capture では `Special` / `Super` のように moveType の大文字表記が混じるため、派生データでは小文字正規化して section と照合している。

## 未解決の質問

- Ryu の `enriched_review_required` 13件を人間レビューし、正式な merge policy に昇格できるか。
- `imageinfo` で missing になった `File:SF6 Ryu 236p hitbox.png` を、SuperCombo 側の削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
- Denjin / hold level / duplicate input rows を、公式 row の補助情報、variant row、または SuperCombo-only rows としてどう確定するか。

## ソースメモ

- Raw manifest: `raw/supercombo/frame-data/2026-05-31/ryu/manifest.json`
- Raw metadata: `raw/supercombo/frame-data/2026-05-31/ryu/metadata.json`
- Raw wikitext:
  - `raw/supercombo/frame-data/2026-05-31/ryu/data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/ryu/frame-data.raw.wikitext`
- Cargo API:
  - `raw/supercombo/frame-data/2026-05-31/ryu/cargo/frame-data.json`
  - `raw/supercombo/frame-data/2026-05-31/ryu/cargo/character-data.json`
- Rendered DOM: `raw/supercombo/frame-data/2026-05-31/ryu/rendered/tables.dom.json`
- Screenshots: `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/`
- Images: `raw/supercombo/frame-data/2026-05-31/ryu/images/files/`
- Validation: `raw/supercombo/frame-data/2026-05-31/ryu/validation.json`
- Derived outputs: `wiki/outputs/data/supercombo/frame-data/ryu/`
- Crosswalk report: [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]]
- Enriched outputs: `wiki/outputs/data/enriched/frame-data/ryu/`
- Enriched report: [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]]
