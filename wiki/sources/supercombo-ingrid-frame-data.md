---
type: source
source_type: community_frame_data
title: "SuperCombo Ingrid フレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/frame-data/supercombo/ingrid/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Ingrid/Frame_data"
created: 2026-06-02
updated: 2026-06-02
captured_at_utc: "2026-06-02T01:58:06Z"
status: active
confidence: medium
tags:
  - sf6
  - supercombo
  - frame-data
  - community
aliases:
  - "Ingrid SuperCombo frame data"
  - "イングリッド SuperCombo フレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
related_entities:
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/ingrid]]"
---

# ソース: SuperCombo Ingrid フレームデータ

## 1行要約

SuperCombo Wiki の Ingrid フレームデータを、`Data?action=raw` の生 wikitext、Cargo API、表示ページ DOM、5種類のタブ別スクリーンショット、画像参照情報として保存した community source ページ。

## 重要ポイント

1. raw snapshot（原本スナップショット）は `raw/frame-data/supercombo/ingrid/` 配下の latest mirror 固定パスに保存されている。source revision は path ではなく manifest の `capture_label` と `source_revision` で追う。
2. 生データの中心は `Street_Fighter_6/Ingrid/Data?action=raw` で、`CharacterData-SF6` が 1 件、`FrameData-SF6` が 83 件ある。
3. 表示ページ `Street_Fighter_6/Ingrid/Frame_data?action=raw` は、Character Data と 4 section の表示テーブルを Cargo query で組み立てている。保存した表示 Cargo query は 21 件。
4. `Normals and Target Combos`、`Drive and Throw`、`Specials`、`Supers` は、それぞれ `General`、`Details`、`Meter`、`Properties`、`Notes` のタブを持つ。DOM 取得と validator は 4 section x 5 tab = 20 表を照合している。
5. Cargo API から取得した `SF6_FrameData` は 83 行、`SF6_CharacterData` は 1 行で、raw template の件数と一致する。
6. 画像参照は 164 refs、MediaWiki `imageinfo` の distinct title は 158 件。解決できた title は face / portrait の 2 件のみで、156 title は missing。取得できた画像も `SF6_Ingrid_Face.png` と `SF6_Ingrid_Portrait.png` の 2 件に限られる。
7. `6HPHK` と `236236P` は同じ input を持つ複数 row があるため、SuperCombo raw の行識別には `moveId` を使う。input は表示・検索用であり、主キーにはしない。
8. `moveType` には `Special` / `Super` の大文字表記が混じるため、後続の派生処理や section 照合では小文字正規化が必要になる可能性がある。
9. この source は community data なので、公式 Capcom data と重なる基本フレーム値では公式を正とする。SuperCombo は公式にない range、juggle、hitbox image、notes などを後で追加統合する候補として扱う。
10. 2026-06-02 に SuperCombo 派生 frame-data CSV/JSON、公式 Classic との crosswalk、補助列付き output を作成した。公式値は Capcom 公式 Classic CSV を正とし、SuperCombo は `supercombo_*` 補助列として扱う。
11. SuperCombo-only 9 行（Big Laser?、Burnout Attack?、Sun Octopus?、Monoid 関連）は特殊隠しコマンド / Monoid 操作に関係する通常利用外の row なので、通常の Ingrid frame-data 回答には混ぜず、hidden / Dark / Shin Ingrid / Monoid / taunt-summon / SuperCombo-only が明示された質問でだけ参照する。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| Ingrid の SuperCombo raw data は 1 件の character template と 83 件の frame template を含む。 | `raw/frame-data/supercombo/ingrid/data.raw.wikitext`; `raw/frame-data/supercombo/ingrid/data.templates.json`; `raw/frame-data/supercombo/ingrid/validation.json` | high | validator で raw template count と Cargo row count を照合済み。 |
| raw path は latest mirror 固定パスで、source revision は manifest の `capture_label` / `source_revision` で追う。 | `raw/frame-data/supercombo/ingrid/manifest.json` | high | `storage_policy` は `latest_frame_data_mirror`。`capture_label` は `2026-06-02`。 |
| 表示ページは 21 件の Cargo query で Character Data と frame table を作っている。 | `raw/frame-data/supercombo/ingrid/frame-data.raw.wikitext`; `raw/frame-data/supercombo/ingrid/frame-data.cargo-queries.json` | high | Character Data 1 件、section/tab 用 query 20 件。 |
| 4 section x 5 tab の表示 table は raw/Cargo から期待される header、row count、input order、cell values と照合済み。 | `raw/frame-data/supercombo/ingrid/rendered/tables.dom.json`; `raw/frame-data/supercombo/ingrid/validation.json` | high | Notes も含め、20 table comparisons を実行。 |
| `SF6_FrameData` は move type として ground_normal 19、air_normal 7、drive 6、throw 2、special 36、super 9、taunt 4 を含む。 | `raw/frame-data/supercombo/ingrid/validation.json` | high | validator の集計では `Special` / `Super` を小文字化して数えている。 |
| duplicate input は `6HPHK` と `236236P` の 2 種類。 | `raw/frame-data/supercombo/ingrid/validation.json`; `raw/frame-data/supercombo/ingrid/data.templates.json` | high | `6HPHK` は block/recovery、`236236P` は SA3/CA の variant。 |
| Data page の最新 revision は 2026-06-02T01:44:56Z、Frame data 表示ページの revision は 2026-04-22T23:42:21Z。 | `raw/frame-data/supercombo/ingrid/api/page-metadata.json`; `raw/frame-data/supercombo/ingrid/manifest.json` | high | Data page は pageid 97720 / revid 365281、Frame data page は pageid 97724 / revid 362024。 |
| image refs は 164 件、imageinfo の distinct title は 158 件で、face / portrait の 2 title しか解決できず、156 title が missing だった。 | `raw/frame-data/supercombo/ingrid/image-manifest.json`; `raw/frame-data/supercombo/ingrid/imageinfo.json`; `raw/frame-data/supercombo/ingrid/validation.json` | high | duplicate refs があるため refs 数と resolved + missing title 数は一致しない。downloaded images は 2 件、failed downloads は 0 件。 |
| 公式 Classic 75 rows との crosswalk は、自動一致 47、name override 一致 26、公式側未照合 2 になった。 | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]; `wiki/outputs/data/frame-data/supercombo/ingrid/crosswalk-summary.json` | high | 公式側未照合は `前方ステップ` / `後方ステップ`。 |
| 補助列付き output は `enriched` 47、`enriched_reviewed` 26、`official_only` 2 で、レビュー対象 26 行はすべて accepted。 | [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]; `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/summary.json` | high | 公式列は保持し、SuperCombo 値は `supercombo_*` 補助列に入れる。 |

## データ構造メモ

- `data.raw.wikitext` は SuperCombo の raw template source。値の正規化や翻訳はしていない。
- `data.templates.json` は `CharacterData-SF6` / `FrameData-SF6` template を機械的に抽出した raw-adjacent JSON。
- `cargo/frame-data.json` と `cargo/character-data.json` は SuperCombo の Cargo API から取得した表データ。
- `rendered/tables.dom.json` は実際に表示された table の DOM text / HTML / image refs / tab state を保存する。
- `screenshots/*.png` は `General`、`Details`、`Meter`、`Properties`、`Notes` の各タブをページ全体で保存する。
- `imageinfo.json` と `image-manifest.json` は画像参照、MediaWiki imageinfo、ダウンロード結果を保存する。ただし Ingrid では move / hitbox 画像の大半が missing になっている。
- `wiki/outputs/data/frame-data/supercombo/ingrid/` は SuperCombo raw から作った派生 frame-data と公式 Classic crosswalk。
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/` は公式 Classic rows を保持したまま SuperCombo 補助列を付与した output。

## 既存 wiki との矛盾または更新

- SuperCombo は community source なので、公式 Capcom source と同じ項目がある場合は Capcom 公式 data を優先する。今回の取得は、SuperCombo 側を削らず完全 raw source として保持し、後続の照合 / merge policy で official と照合するための基礎データ。
- input が同じでも `moveId`、挙動、条件、notes が異なる row がある。したがって SuperCombo raw の主キーは `moveId` とし、input は主キーにしない。
- `taunt` move type は raw/Cargo に含まれるが、表示ページの 4 section x 5 tab validation 対象には入っていない。
- Ingrid では face / portrait 以外の move / hitbox 画像がほぼ解決できていないため、画像付き hitbox analysis の根拠としては現時点で使えない。
- 公式 Classic との照合では Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush など 26 行を人間レビューし、公式値を正とする補助リンクとして accepted にした。
- 公式 row に直接照合しなかった SuperCombo-only 9 行は、特殊隠しコマンド / Monoid 操作に関係する通常利用外の row として `supercombo-only.csv` に隔離する。通常の frame-data 質問では公式 row と公式 row に紐づく補助列付き output を優先する。

## 未解決の質問

- `imageinfo` で missing になった 156 title が source 側の未作成/削除済みファイルなのか、filename 正規化や API title 変換で再解決可能なのか。
- 公式 row に直接照合しなかった SuperCombo-only 9 行（Big Laser?、Burnout Attack?、Sun Octopus?、Monoid 関連）について、既存の `suggested_handling` を将来 `supercombo_only_hidden_command` や `supercombo_only_taunt_summon` のように細分化する必要があるか。

## ソースメモ

- 原本 manifest: `raw/frame-data/supercombo/ingrid/manifest.json`
- 原本 metadata: `raw/frame-data/supercombo/ingrid/metadata.json`
- 原本 wikitext:
  - `raw/frame-data/supercombo/ingrid/data.raw.wikitext`
  - `raw/frame-data/supercombo/ingrid/frame-data.raw.wikitext`
- Cargo API データ:
  - `raw/frame-data/supercombo/ingrid/cargo/frame-data.json`
  - `raw/frame-data/supercombo/ingrid/cargo/character-data.json`
- 表示 DOM: `raw/frame-data/supercombo/ingrid/rendered/tables.dom.json`
- スクリーンショット: `raw/frame-data/supercombo/ingrid/screenshots/`
- 画像: `raw/frame-data/supercombo/ingrid/images/files/`
- 検証結果: `raw/frame-data/supercombo/ingrid/validation.json`
- SuperCombo 派生 output: `wiki/outputs/data/frame-data/supercombo/ingrid/`
- 公式 + SuperCombo 補助 output: `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/`
- crosswalk report: [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]
- enriched report: [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]
