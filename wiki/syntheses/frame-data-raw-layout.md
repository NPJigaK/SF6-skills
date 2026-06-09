---
type: synthesis
created: 2026-06-01
updated: 2026-06-09
status: active
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
  - "[[outputs/reports/2026-05-30-official-frame-data-coverage]]"
  - "[[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]]"
  - "[[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]]"
  - "[[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]"
  - "[[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]"
  - "[[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]"
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/jp]]"
  - "[[entities/ryu]]"
  - "[[entities/zangief]]"
  - "[[entities/ingrid]]"
aliases:
  - "frame-data raw layout"
  - "フレームデータ raw 配置"
tags:
  - frame-data
  - raw-layout
  - provenance
---

# Frame-data raw 配置

## 要約

frame-data raw は、capture date をディレクトリ名に入れる方式ではなく、`raw/frame-data/official/<character>/` と `raw/frame-data/supercombo/<character>/` の latest mirror 固定パスで保持する。由来の時点は path ではなく、各 `manifest.json` の `capture_label`、`created_at_utc` / `captured_at_utc`、SuperCombo の `source_updated_at` / `source_revision` で追う。2026-06-06 以降、SuperCombo の `validation.json` は現在の raw metadata と実ファイル artifact hash に対応する `raw_fingerprint` も持ち、extract は fingerprint 不一致の validation を拒否する。2026-06-07 以降、派生 output は `wiki/outputs/data/frame-data/official/`、`wiki/outputs/data/frame-data/supercombo/`、`wiki/outputs/data/frame-data/official-supercombo-enriched/` の data-family first layout で置く。2026-06-05 時点で、official は 30 character data slugs、SuperCombo は 30 character slugs の raw capture と派生 output がそろっている。

この方針により、読者は常に同じ raw path から最新 mirror を辿り、再現性や履歴判断が必要な場合だけ manifest の provenance fields を見る。`raw/` は原本保存層なので、翻訳、要約、正規化、統合分析は `wiki/` に置く。

## 鮮度日付の扱い

wiki 化の際、source の鮮度は取得日ではなく、raw に明示された source 側の日付を優先して判断する。SuperCombo frame-data では `source_updated_at` がある場合はこれを優先し、ない場合だけ `source_revision.latest_revision_timestamp`、さらに粗い表示が必要な場合は revision timestamp 由来の `capture_label` を参照する。`captured_at_utc` は raw を取得した時刻であり、source 本文が更新された時刻としては扱わない。

`source_published_at` は source の初版日や公開日が raw に明示されている場合だけ使う。現在の SuperCombo frame-data manifests は `source_updated_at` を持つが、`source_published_at` は持たないため、初版日を推測して wiki に入れない。

## 現在の固定パス

| Source family | Manifest | 主要 raw artifacts | Derived outputs |
|---|---|---|---|
| Capcom official | `raw/frame-data/official/<data-slug>/manifest.json` | `classic/page.html`, `classic/table.dom.json`, `classic/screenshot.png`, `classic/metadata.json`, `modern/...` | `wiki/outputs/data/frame-data/official/<data-slug>/` |
| SuperCombo | `raw/frame-data/supercombo/<character>/manifest.json` | `data.raw.wikitext`, `data.templates.json`, `cargo/`, `rendered/tables.dom.json`, `screenshots/`, `images/files/`, `validation.json` | `wiki/outputs/data/frame-data/supercombo/<character>/`, `wiki/outputs/data/frame-data/official-supercombo-enriched/<character>/` |

## 代表 character の入口

| Character | Official raw | SuperCombo raw | 主な成果物 |
|---|---|---|---|
| JP | `raw/frame-data/official/jp/manifest.json`; `classic/`; `modern/` | `raw/frame-data/supercombo/jp/manifest.json`; `data.raw.wikitext`; `cargo/frame-data.json`; `rendered/tables.dom.json` | [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]], [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]] |
| Ryu | `raw/frame-data/official/ryu/manifest.json`; `classic/`; `modern/` | `raw/frame-data/supercombo/ryu/manifest.json`; `data.raw.wikitext`; `cargo/frame-data.json`; `rendered/tables.dom.json` | [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]], [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] |
| Zangief | `raw/frame-data/official/zangief/manifest.json`; `classic/`; `modern/` | `raw/frame-data/supercombo/zangief/manifest.json`; `data.raw.wikitext`; `cargo/frame-data.json`; `rendered/tables.dom.json` | [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]], [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] |
| Ingrid | `raw/frame-data/official/ingrid/manifest.json`; `classic/`; `modern/` | `raw/frame-data/supercombo/ingrid/manifest.json`; `data.raw.wikitext`; `cargo/frame-data.json`; `rendered/tables.dom.json` | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]], [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] |

30 キャラ分の一覧と未レビュー補助行は [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] に集約する。raw entrypoint はすべて `raw/frame-data/supercombo/<character_slug>/manifest.json`。

## Provenance fields

| Field | Applies to | 意味 |
|---|---|---|
| `storage_policy` | official / SuperCombo | `latest_frame_data_mirror` の場合、raw path は固定の最新 mirror で、capture date を path に含めない。 |
| `capture_label` | official / SuperCombo | snapshot の由来を表すラベル。具体的な日付は各 manifest で確認する。SuperCombo は 2026-06-05 時点で 30キャラ分の latest mirror を持つ。 |
| `created_at_utc` | official | 公式 raw 取得データの作成時刻。 |
| `captured_at_utc` | SuperCombo | SuperCombo raw 取得データの取得時刻。 |
| `source_updated_at` | SuperCombo | source 側の最新 revision timestamp。source freshness を見る時は、取得時刻ではなくこの field を優先する。 |
| `source_published_at` | source raw when available | source の初版日や公開日が取得できた場合の field。明示されていない source では推測しない。 |
| `source_revision` | SuperCombo | Data page と Frame data page の revision timestamp / revid。SuperCombo では path ではなくこれを見て source revision を判断する。 |
| `raw_fingerprint` | SuperCombo validation | `metadata.json` と raw artifact 実ファイルの現在状態に validation が対応していることを示す。capture 後に古い validation が残る状態を extract 前に拒否するために使う。 |

## 根拠

| 論点 | 根拠ソース | 信頼度 |
|---|---|---|
| official raw は `raw/frame-data/official/<data-slug>/` 配下に Classic / Modern capture を持つ。 | [[outputs/reports/2026-05-30-official-frame-data-coverage]], [[sources/capcom-official-jp-frame-data]], [[sources/capcom-official-ryu-frame-data]] | high |
| official manifest は `storage_policy: latest_frame_data_mirror` と `capture_label` を持つ。 | `raw/frame-data/official/jp/manifest.json`, `raw/frame-data/official/ryu/manifest.json` | high |
| SuperCombo raw は `raw/frame-data/supercombo/<character>/` 配下に raw wikitext、Cargo API、DOM、screenshots、images、validation を持つ。 | [[sources/supercombo-jp-frame-data]], [[sources/supercombo-ryu-frame-data]], [[sources/supercombo-zangief-frame-data]], [[sources/supercombo-ingrid-frame-data]] | high |
| SuperCombo raw capture と派生 output は 30 キャラ分そろっており、validation は 30/30 で `passed`。2026-06-06 以降は validation が現在 raw の `raw_fingerprint` を持つ。 | [[sources/supercombo-street-fighter-6-frame-data-batch]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]], `raw/frame-data/supercombo/<character>/validation.json` | high |
| SuperCombo manifest は `storage_policy: latest_frame_data_mirror`、`capture_label`、`source_updated_at`、`source_revision` を持つ。 | `raw/frame-data/supercombo/jp/manifest.json`, `raw/frame-data/supercombo/ryu/manifest.json`, `raw/frame-data/supercombo/zangief/manifest.json`, `raw/frame-data/supercombo/ingrid/manifest.json` | high |
| SuperCombo 30キャラの source freshness は `source_updated_at` で 2026-05-30T01:24:06Z から 2026-06-02T03:14:40Z の範囲に分布する。 | `raw/frame-data/supercombo/<character>/manifest.json`, [[sources/supercombo-street-fighter-6-frame-data-batch]] | high |
| official + SuperCombo の統合成果物は公式列を正として保持し、SuperCombo は `supercombo_*` 補助列として扱う。 | [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]], [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]], [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]], [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] | high |

## 含意

- 新しい ingest や query では、旧 `raw/official/frame-data/<date>/...` や `raw/supercombo/frame-data/<date>/...` を現在の入口として使わない。
- 日付を確認したい時は path ではなく manifest を読む。特に SuperCombo は `source_updated_at` を source freshness、`captured_at_utc` を取得時刻、`source_revision.latest_revision_timestamp` と各 page の `lastrevid` を revision 根拠として分けて確認する。
- SuperCombo の派生 output を再生成する前に、`validation.json` の `status: passed` だけでなく `raw_fingerprint` が現在 raw と一致していることを確認する。`tools.frame_data.supercombo.extract` はこの確認に失敗した場合、派生データを出さない。
- 派生 JSON は `wiki/outputs/data/...` に置き、raw source を正規化した置き換え版を `raw/` に置かない。
- 2026-06-07 以降、frame-data 派生 output は `wiki/outputs/data/frame-data/<variant>/<character>/` に置く。`variant` は `official`、`supercombo`、`official-supercombo-enriched`。
- 既存 raw manifest の `derived_outputs` に旧 output path が残っていても、`raw/` 不変ルールに従って書き換えない。現在の output contract は README、tools、`wiki/index.md`、この synthesis を入口に確認する。
- historical log や古い review note に旧 path が残っていても、それは当時の作業履歴として扱う。現在の読者向け入口は source page、coverage report、この synthesis、index に置く。
- SuperCombo 30キャラ分は派生 output / official crosswalk / 補助列付き output まで作成済み。既存レビュー済み 69 行は保持し、複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ 1295 行は `enriched_review_required` として accept していない。未レビュー理由は `enrichment_review_queues` で分離している。
- 画像を使う分析では `image-manifest.json` と review note を確認する。新規 26キャラは画像ファイル本体をダウンロードせず、image refs / imageinfo を保存している。

## 未解決の質問

- `latest_frame_data_mirror` の再取得時に旧 mirror をどこまで外部 artifact として保持するか。
- official manifest の `raw_review_status` と wiki review page の accepted / pending 状態を同期する運用ルールをどうするか。
- SuperCombo 30キャラ分の未レビュー補助行と SuperCombo-only rows をどの粒度で個別 source / entity page に反映するか。
