---
type: concept
title: "Frame Data"
created: 2026-05-26
updated: 2026-06-02
status: active
confidence: high
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/capcom-official-luke-frame-data]]"
  - "[[sources/capcom-official-jamie-frame-data]]"
  - "[[sources/capcom-official-chun-li-frame-data]]"
  - "[[sources/capcom-official-guile-frame-data]]"
  - "[[sources/capcom-official-kimberly-frame-data]]"
  - "[[sources/capcom-official-juri-frame-data]]"
  - "[[sources/capcom-official-ken-frame-data]]"
  - "[[sources/capcom-official-blanka-frame-data]]"
  - "[[sources/capcom-official-dhalsim-frame-data]]"
  - "[[sources/capcom-official-e-honda-frame-data]]"
  - "[[sources/capcom-official-dee-jay-frame-data]]"
  - "[[sources/capcom-official-manon-frame-data]]"
  - "[[sources/capcom-official-marisa-frame-data]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/capcom-official-lily-frame-data]]"
  - "[[sources/capcom-official-cammy-frame-data]]"
  - "[[sources/capcom-official-rashid-frame-data]]"
  - "[[sources/capcom-official-aki-frame-data]]"
  - "[[sources/capcom-official-ed-frame-data]]"
  - "[[sources/capcom-official-gouki-akuma-frame-data]]"
  - "[[sources/capcom-official-vega-m-bison-frame-data]]"
  - "[[sources/capcom-official-terry-frame-data]]"
  - "[[sources/capcom-official-mai-frame-data]]"
  - "[[sources/capcom-official-elena-frame-data]]"
  - "[[sources/capcom-official-sagat-frame-data]]"
  - "[[sources/capcom-official-c-viper-frame-data]]"
  - "[[sources/capcom-official-alex-frame-data]]"
  - "[[sources/capcom-official-ingrid-frame-data]]"
  - "[[outputs/reports/2026-05-30-official-frame-data-coverage]]"
  - "[[syntheses/frame-data-raw-layout]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[entities/street-fighter-6]]"
  - "[[syntheses/frame-data-raw-layout]]"
  - "[[entities/ryu]]"
  - "[[entities/luke]]"
  - "[[entities/jamie]]"
  - "[[entities/chun-li]]"
  - "[[entities/guile]]"
  - "[[entities/kimberly]]"
  - "[[entities/juri]]"
  - "[[entities/ken]]"
  - "[[entities/blanka]]"
  - "[[entities/dhalsim]]"
  - "[[entities/e-honda]]"
  - "[[entities/dee-jay]]"
  - "[[entities/manon]]"
  - "[[entities/marisa]]"
  - "[[entities/jp]]"
  - "[[entities/zangief]]"
  - "[[entities/lily]]"
  - "[[entities/cammy]]"
  - "[[entities/rashid]]"
  - "[[entities/aki]]"
  - "[[entities/ed]]"
  - "[[entities/gouki-akuma]]"
  - "[[entities/vega-m-bison]]"
  - "[[entities/terry]]"
  - "[[entities/mai]]"
  - "[[entities/elena]]"
  - "[[entities/sagat]]"
  - "[[entities/c-viper]]"
  - "[[entities/alex]]"
  - "[[entities/ingrid]]"
aliases:
  - "フレームデータ"
  - "Frame Data"
tags:
  - mechanics
  - glossary
---

# Frame Data（フレームデータ）

## 要約

Frame data は、技の発生、持続、硬直、有利不利、ダメージ、補正、キャンセル可否、Drive gauge 変動などを説明するための timing / property vocabulary と structured move data。現在この wiki には、30 character data slugs 分の Capcom 公式 Classic / Modern frame-data outputs と、SuperCombo Wiki の JP / Ryu / Zangief community raw frame-data 取得データがある。raw frame-data の現在の入口は latest mirror 固定パスで、由来は manifest の `capture_label` / `source_revision` から確認する。

## 定義

SuperCombo glossary は active frames、startup、recovery、cancel options、hit/block advantage、guard direction、damage、damage scaling、hitconfirm windows、Drive Rush Cancel advantage、actionable recovery などの用語を説明している。

Capcom 公式 capture は、Classic / Modern controls の per-move data を raw HTML、raw DOM、screenshot、metadata、派生 CSV / field-meaning JSON として保持する。raw path は `raw/frame-data/official/<data-slug>/`。JP、Ryu、Chun-Li、Zangief は人間レビュー済み accepted。2026-05-30 の 26 captures は自動検証済みで、人間レビューは未完了。

SuperCombo JP / Ryu / Zangief 取得データは、community wiki の `Data?action=raw`、Cargo API、表示 DOM、5タブ別スクリーンショット、参照画像を保持する。raw path は `raw/frame-data/supercombo/<character>/`。公式 source と重なる基本フレーム値では Capcom 公式 data を優先し、SuperCombo は公式にない range、juggle、notes、hitbox image などを後で統合する候補として扱う。

## なぜ重要か

frame-data 用語、structured capture、Classic / Modern comparison policy がないと、技データ、比較、timing-sensitive claims を安定して解釈できない。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| active は、技が相手に当たり得る状態で残る frames を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| recovery は、active frames 終了後に技が終わるまでの frames を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| startup は、技が active になるまでの frames を説明し、last startup frame と first active frame は同じ frame として扱われる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| hit/block values は、攻撃が当たった時またはガードされた時の frame advantage を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| この wiki には 30 character data slugs 分の Classic / Modern 公式 frame-data outputs がある。 | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
| frame-data raw は latest mirror 固定パスで保存し、capture date / source revision は manifest の `capture_label` / `source_revision` で追う。 | [[syntheses/frame-data-raw-layout]] | high |
| JP、Ryu、Chun-Li、Zangief captures は人間レビュー済み accepted。 | [[reviews/2026-05-26-official-jp-frame-data-capture-review]], [[reviews/2026-05-27-official-ryu-frame-data-capture-review]], [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]], [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | high |
| 2026-05-30 の 26 official captures は自動検証済みで、人間レビューは未完了。 | [[reviews/2026-05-30-official-frame-data-roster-capture-review]] | high |
| official captures は field explanations を per-move CSV rows から分離して保存している。 | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
| SuperCombo JP capture は raw template 64 件、Cargo frame rows 64 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-jp-frame-data]], [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]] | high |
| SuperCombo Ryu capture は raw template 77 件、Cargo frame rows 77 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-ryu-frame-data]], [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]] | high |
| SuperCombo Zangief 取得データは raw template 68 件、Cargo frame rows 68 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-zangief-frame-data]], [[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]] | high |
| SuperCombo raw では同じ input を持つ複数 row があるため、input ではなく `moveId` を行識別子として扱う。 | [[sources/supercombo-jp-frame-data]], [[sources/supercombo-ryu-frame-data]], [[sources/supercombo-zangief-frame-data]] | high |
| Classic / Modern 比較は、公式の技名完全一致を default にする。 | [[reviews/2026-05-27-health-check]] | high |
| 読者向け command notation は display-only transform であり、raw input tokens が source-preserving data。 | [[reviews/2026-05-27-health-check]] | high |

## 比較方針

Classic / Modern frame-data comparison では、公式表の技名完全一致を default にする。`しゃがみ強K（ビッグスタンプ）` と `ビッグスタンプ` のように実質対応しそうでも名前が違う場合は、勝手に merge せず、対応候補として注記する。

読者向け回答では `↓↘→ + 強P` のような読みやすい command notation を使ってよい。ただしこれは説明用の表示変換であり、source-preserving data は公式 capture outputs の raw token data。

## 関連

- [[concepts/drive-system]]
- [[concepts/juggle-system]]
- [[concepts/fighting-game-notation]]
- [[entities/street-fighter-6]]

## 矛盾 / 注意点

- この page は個別技の値を網羅しない。個別値は raw DOM と派生 CSV に残し、再利用可能な question / synthesis が必要になった時だけ昇格する。
- `input_raw_display` は raw DOM-token display であり、normalized command notation ではない。
- 30-character coverage は単一日付 snapshot ではない。JP は 2026-05-26、Ryu / Chun-Li / Zangief は 2026-05-27、残り 26 characters は 2026-05-30。
- raw path は現在 `raw/frame-data/...` の latest mirror 固定パス。古い log / review に残る date-based path は当時の履歴として読む。
- SuperCombo は community data なので、公式 Capcom data と同じ項目については公式を優先する。SuperCombo raw 取得データは削らず保持し、後続の照合で統合する。
- Ryu capture では `Special` / `Super` のような moveType の大文字表記が混じるため、派生処理では小文字正規化して section と照合する。
- Zangief の照合では `key-circle` を `360+`、2回転を `720+` として扱い、hold / 近距離・中距離・遠距離 / CA variant は Zangief 専用 name override で `moveId` に対応させている。

## 未解決の質問

- display-only command notation を formal wiki notation schema にする条件は何か。
- 公式 patch notes / Battle Change List を ingest して、frame-data changes を時系列で扱うべきか。
- SuperCombo JP / Ryu / Zangief の range、juggle、hitbox image、notes を公式 data にどの schema で追加統合するか。
