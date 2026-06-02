---
type: output
output_type: report
created: 2026-06-02
updated: 2026-06-02
status: active
sources:
  - "[[sources/supercombo-ingrid-frame-data]]"
  - "[[sources/capcom-official-ingrid-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/ingrid]]"
  - "[[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]]"
  - "[[syntheses/frame-data-raw-layout]]"
aliases:
  - "SuperCombo Ingrid official crosswalk"
  - "Ingrid SuperCombo 公式照合"
---

# SuperCombo Ingrid / 公式 Ingrid フレームデータ照合 - 2026-06-02

## 要約

SuperCombo Ingrid raw 取得データからレビュー用の派生 CSV/JSON を作成し、Capcom 公式 Ingrid Classic CSV との候補照合を生成した。これは最終マージではなく、公式 data を正としたまま SuperCombo の `move_id`、range、juggle、notes、画像、hitbox をどの公式 row に紐づけられるか確認するためのレビュー面。

Sun Crest stock level、OD Sun Shot の共有 row、SA1 / SA2 の stock level、Drive Rush など 26 行は人間レビューし、公式値を正とした補助リンクとして accepted にした。この照合を使った補助列付き output は [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] に保存している。

## 生成ファイル

- `wiki/outputs/data/supercombo/frame-data/ingrid/frames.csv`
- `wiki/outputs/data/supercombo/frame-data/ingrid/frames.json`
- `wiki/outputs/data/supercombo/frame-data/ingrid/character.csv`
- `wiki/outputs/data/supercombo/frame-data/ingrid/schema.json`
- `wiki/outputs/data/supercombo/frame-data/ingrid/crosswalk-official-classic.csv`
- `wiki/outputs/data/supercombo/frame-data/ingrid/crosswalk-summary.json`
- `wiki/outputs/data/supercombo/frame-data/ingrid/supercombo-unmatched.csv`

## 方針

| 項目 | 方針 |
|---|---|
| 正とする source | 公式に存在する基本フレーム値は Capcom 公式 Ingrid data を正とする。 |
| SuperCombo の扱い | SuperCombo raw は削らず保持し、公式にない補助情報の候補 source として使う。 |
| SuperCombo row key | input ではなく `move_id` を使う。Ingrid には同じ input を持つ variant row があるため。 |
| 照合の意味 | 自動候補に、Ingrid の Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush override を反映したレビュー面。 |
| 比較対象 | startup、active duration、recovery、damage は単純数値化できる場合だけ比較する。 |

## 照合サマリー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 75 |
| SuperCombo frame rows | 83 |
| 自動一致 | 47 |
| Ingrid / 汎用 name override による一致 | 26 |
| 公式側未照合 | 2 |
| 一致した distinct SuperCombo row | 70 |
| SuperCombo 側未照合 | 13 |

公式側で未照合の 2 件は `前方ステップ` と `後方ステップ`。SuperCombo 取得データでは dash speed/distance が `SF6_CharacterData` にあり、`SF6_FrameData` row ではないため、frame-row 照合では未対応になる。

## name override 行

| 分類 | 件数 | 例 |
|---|---:|---|
| command normal | 1 | `ingrid_jhk_jhk` |
| OD Sun Shot strength variant | 3 | `ingrid_236lpmp`, `ingrid_236mphp` |
| Sun Flare / Solar Burst stock row | 14 | `ingrid_214lp`, `ingrid_214hp_2stock`, `ingrid_j214pp_2stock` |
| SA1 / SA2 stock level | 6 | `ingrid_236236k_hold_2stock`, `ingrid_214214p_hold_2stock` |
| Drive Rush variant | 2 | `ingrid_mpmk_66_pdr`, `ingrid_mpmk_66_drc` |

これら 26 件の name override match は、人間レビューで補助リンクとして accepted。公式列は上書きせず、SuperCombo の range、notes、juggle、hitbox などを補助列として扱う。

## SuperCombo row 再利用

| SuperCombo move_id | 理由 |
|---|---|
| `ingrid_236lpmp` | 公式側の `OD 弱 サンシュート` / `OD 中 サンシュート` が SuperCombo の同一 shared row に対応する候補。 |
| `ingrid_mpmk` | ドライブパリィ / ジャストパリィ rows と Drive Rush 系の候補集合に同じ base row が現れる。Drive Rush は専用 `move_id` を補助リンクとして使う。 |

## SuperCombo 側未照合行

| 分類 | 件数 | 内容 |
|---|---:|---|
| taunt | 4 | `ingrid_5pppkkk`, `ingrid_6pppkkk`, `ingrid_4pppkkk`, `ingrid_2pppkkk` |
| SuperCombo-only extra / hidden row | 9 | `ingrid_22ppp`, `ingrid_214214k`, `ingrid_360kk`, `ingrid_monoid_l`, `ingrid_monoid_m`, `ingrid_monoid_h`, `ingrid_monoid_hphk`, `ingrid_monoid_jx`, `ingrid_monoid_super` |

## 注意点

- この report はレビュー用であり、`wiki/outputs/data/frame-data/ingrid/` の公式 CSV を置き換えない。
- Ingrid は imageinfo で face / portrait の 2 件しか解決できていない。SuperCombo の `supercombo_images` / `supercombo_hitboxes` は参照名として保持するが、画像ファイル自体を根拠に使うには追加確認が必要。
- SuperCombo-only 9 行は公式 frame row と直接照合していない。これらを extra / hidden / community-only data として schema に入れるかは別途判断する。

## 根拠

- SuperCombo source（根拠）: [[sources/supercombo-ingrid-frame-data]]
- 公式 source（根拠）: [[sources/capcom-official-ingrid-frame-data]]
- SuperCombo 検証: [[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]]
- SuperCombo 原本 manifest: `raw/frame-data/supercombo/ingrid/manifest.json`
- 照合 summary: `wiki/outputs/data/supercombo/frame-data/ingrid/crosswalk-summary.json`
- 補助列付き output report: [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]
