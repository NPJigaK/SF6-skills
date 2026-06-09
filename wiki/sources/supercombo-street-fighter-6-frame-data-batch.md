---
type: source
source_type: community_frame_data
title: "SuperCombo Street Fighter 6 全キャラフレームデータ"
author: "SuperCombo Wiki contributors"
publisher: "SuperCombo Wiki"
raw_path: "raw/frame-data/supercombo/<character_slug>/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/<Character>/Frame_data"
created: 2026-06-05
updated: 2026-06-09
status: active
confidence: medium
tags:
  - sf6
  - supercombo
  - frame-data
  - community
  - batch-capture
aliases:
  - "SuperCombo SF6 all frame data"
  - "SuperCombo SF6 全キャラフレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
related_entities:
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
related_outputs:
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
related_reviews:
  - "[[reviews/2026-06-05-supercombo-all-frame-data-capture-review]]"
---

# ソース: SuperCombo Street Fighter 6 全キャラフレームデータ

## 1行要約

SuperCombo Wiki の Street Fighter 6 frame-data pages 30 キャラ分を、`Data?action=raw` の生 wikitext、Cargo API、表示ページ DOM、5種類のタブ別スクリーンショット、画像参照情報として保存した batch source summary。

## 重要ポイント

1. raw snapshot（原本スナップショット）は `raw/frame-data/supercombo/<character_slug>/` 配下の latest mirror 固定パスに保存されている。source freshness は path や取得時刻ではなく、各 `manifest.json` の `source_updated_at` と `source_revision` で追う。
2. 対象は A.K.I.、Akuma、Alex、Blanka、C.Viper、Cammy、Chun-Li、Dee Jay、Dhalsim、E.Honda、Ed、Elena、Guile、Ingrid、Jamie、JP、Juri、Ken、Kimberly、Lily、Luke、M.Bison、Mai、Manon、Marisa、Rashid、Ryu、Sagat、Terry、Zangief の 30 ページ。
3. 30 キャラすべてで `validation.json` の status は `passed`。2026-06-06 以降の validation は現在 raw の `raw_fingerprint` を持ち、再取得後の古い validation では extract できない。SuperCombo raw/Cargo 由来の frame rows は合計 2306 行。
4. 公式 Classic との crosswalk と、公式列を正として SuperCombo を `supercombo_*` 補助列に入れる enriched output を 30 キャラ分生成した。
5. JP / Ryu / Zangief / Ingrid には既存の個別 source summary と人間レビュー済み補助行がある。2026-06-06 の fail-closed policy 以降も accepted 69 行は保持しているが、それ以外の複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field は `enriched_review_required` として扱う。
6. 新規 26 キャラの capture は `--no-download-images` で実行した。画像ファイル本体は保存していないが、raw image refs、`imageinfo.json`、`image-manifest.json`、DOM 内の画像参照は保存している。
7. SuperCombo は community data なので、Capcom 公式 data と重なる基本フレーム値では公式を正とする。SuperCombo は range、juggle、notes、hitbox image refs などの補助 source として扱う。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| SuperCombo frame-data raw capture は 30 キャラ分そろっている。 | `raw/frame-data/supercombo/<character_slug>/manifest.json`; [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high | 30/30 で manifest と validation がある。 |
| 30 キャラの source freshness は `source_updated_at` で追える。 | `raw/frame-data/supercombo/<character_slug>/manifest.json` | high | 範囲は 2026-05-30T01:24:06Z から 2026-06-02T03:14:40Z。これは取得日ではなく source revision 由来の日付。 |
| 現在の SuperCombo frame-data manifests には `source_published_at` はない。 | `raw/frame-data/supercombo/<character_slug>/manifest.json` | high | 初版日や公開日は推測しない。 |
| 30 キャラすべてで自動検証 status は `passed`。 | `raw/frame-data/supercombo/<character_slug>/validation.json`; [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | high | raw template、Cargo row、表示 DOM table を照合し、2026-06-06 以降は現在 raw の `raw_fingerprint` も保存する。 |
| SuperCombo raw/Cargo の frame rows は合計 2306 行、公式 Classic rows は合計 2361 行。 | [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]; `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/summary.json` | high | 集計は生成済み JSON から作成。 |
| enriched output の `enriched_review_required` は合計 1295 行残っている。 | `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/summary.json`; [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | high | 既存 accepted 69 行とは別。勝手に accept していない。 |
| SuperCombo-only rows は合計 620 行ある。 | `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/supercombo-only.json`; [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high | taunt、派生 variant、公式 row に直接照合しない行を含む。 |
| 新規 26 キャラは画像ファイルをダウンロードしていない。 | `raw/frame-data/supercombo/<character_slug>/image-manifest.json`; [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | high | 画像 refs と imageinfo は保存済み。既存 JP/Ryu/Zangief/Ingrid の画像取得状態は保持。 |

## データ構造メモ

- `data.raw.wikitext` は SuperCombo の raw template source。値の翻訳・要約・正規化はしていない。
- `data.templates.json` は `CharacterData-SF6` / `FrameData-SF6` template を機械的に抽出した raw-adjacent JSON。
- `cargo/frame-data.json` と `cargo/character-data.json` は SuperCombo の Cargo API から取得した表データ。
- `rendered/tables.dom.json` は実際に表示された table の DOM text / HTML / tab state を保存する。
- `screenshots/*.png` は `General`、`Details`、`Meter`、`Properties`、`Notes` の各タブをページ全体で保存する。
- `imageinfo.json` と `image-manifest.json` は画像参照、MediaWiki imageinfo、ダウンロード結果を保存する。
- `manifest.json` の `source_updated_at` は source 側の最新 revision timestamp。`captured_at_utc` は raw 取得時刻なので、鮮度判断では混同しない。
- `validation.json` は検証 status に加え、現在 raw metadata と実ファイル artifact hash に対応する `raw_fingerprint` を保存する。capture 時は古い validation を削除し、extract 時は fingerprint 不一致を拒否する。
- `wiki/outputs/data/frame-data/supercombo/<character_slug>/` は SuperCombo raw から作った派生 frame-data と公式 Classic crosswalk。
- `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/` は公式 Classic rows を保持したまま SuperCombo 補助列を付与した output。

## 既存 wiki との矛盾または更新

- 以前は SuperCombo source summary が JP / Ryu / Zangief / Ingrid に限られていた。2026-06-05 時点では raw capture と派生 output は 30 キャラ分ある。
- 公式列を SuperCombo 値で上書きする方針にはしていない。公式 data がある行は Capcom 公式 Classic JSON を正とし、SuperCombo は補助列に入れる。
- `enriched_review_required` は未レビューであり、推測で accepted にしていない。2026-06-06 の fail-closed policy 以降は、新規 26 キャラだけでなく既存 4 キャラの未レビュー補助行も review queue に戻している。括弧付き damage / startup / recovery は条件付き SuperCombo field として review queue に残す。`着地後N` と `N land` の landing recovery 表記差、括弧・注記なしの多段 damage 合計は機械正規化したが、多段 damage は候補選択 score には使わない。
- SuperCombo-only rows は通常回答へ自動混入させない前提で、公式 rows とは別 JSON に分離している。ただし Ingrid の特殊隠しコマンド / Monoid rows 以外の全キャラ分の細分類はまだ未レビュー。

## 未解決の質問

- `enriched_review_required` 1295 行を、queue と character のどちらを優先して人間レビューするか。
- SuperCombo-only 620 行のうち、taunt、条件付き variant、hidden / non-standard row、公式未掲載 row をどう細分化するか。
- imageinfo missing 599 件が source 側の欠損なのか、filename 正規化や API title 変換で再解決可能なのか。
- C.Viper の `moveType=air_normal8` row を、SuperCombo 表示 query に出ない非標準 moveType として保持するだけでよいか、将来の派生 section に含めるべきか。

## ソースメモ

- batch coverage report: [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]
- batch capture review: [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]]
- raw entrypoint: `raw/frame-data/supercombo/<character_slug>/manifest.json`
- SuperCombo 派生 output: `wiki/outputs/data/frame-data/supercombo/<character_slug>/`
- 公式 + SuperCombo 補助 output: `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/`
