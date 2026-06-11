---
type: concept
title: "Frame Data"
created: 2026-05-26
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
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
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
  - "[[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]]"
  - "[[syntheses/frame-data-raw-layout]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/chain]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/super-art]]"
  - "[[concepts/terms/critical-art]]"
  - "[[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]]"
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

Frame data は、技の発生、持続、硬直、有利不利、ダメージ、[[concepts/terms/damage-scaling|補正]]、[[concepts/terms/cancel|キャンセル]]可否、Drive gauge 変動などを説明するための timing / property vocabulary と structured move data。現在この wiki には、30 character data slugs 分の Capcom 公式 Classic / Modern frame-data outputs、Capcom 公式 eSports BASE の観戦用語説明、SuperCombo Wiki の 30 キャラ分 community frame-data source がある。SuperCombo HUD page は [[concepts/terms/combo-counter|Combo Counter]]、[[concepts/terms/counter-hit|Counter-hit]]、[[concepts/terms/punish-counter|Punish Counter]]、knockdown、[[concepts/terms/reversal|Reversal]]、[[concepts/terms/throw-escape|Throw Escape]] などの HUD icon を display cue として補う。取得物の配置と freshness の扱いは [[syntheses/frame-data-raw-layout]] と各 source page にまとめる。

## 定義

Capcom 公式 eSports BASE は観戦者向けに、1 frame = 1/60 秒、[[concepts/terms/frame-advantage|有利 frame / 不利 frame]]、Counter / [[concepts/terms/punish-counter|Punish Counter]] の advantage 増加、Drive Rush 通常技の advantage 増加、[[concepts/terms/hit-confirm|hit confirm]]、frame kill を含む [[concepts/terms/setplay|setplay]] などを説明している。SuperCombo glossary は active frames、startup、recovery、cancel options、hit/block advantage、guard direction、damage、[[concepts/terms/damage-scaling|damage scaling]]、hitconfirm windows、[[concepts/terms/drive-rush-cancel|Drive Rush Cancel]] advantage、actionable recovery などの用語を説明している。SuperCombo HUD page は、[[concepts/terms/combo-counter|Combo Counter]]、[[concepts/terms/counter-hit|Counter-hit]]、[[concepts/terms/punish-counter|Punish Counter]] などを画面上の表示 cue として説明する community visual source として扱う。

Capcom 公式 frame-data source は、Classic / Modern controls の per-move data と派生 JSON output を保持する。現在の派生 output は `wiki/outputs/data/frame-data/official/<data-slug>/<control-scheme>.json` に置く。30 character coverage は [[outputs/reports/2026-05-30-official-frame-data-coverage]] にまとまっている。JP、Ryu、Chun-Li、Zangief は人間レビュー済み accepted。2026-05-30 の 26 captures は自動検証済みで、人間レビューは未完了。

SuperCombo frame-data source は、community wiki の Data page、Cargo API、表示 DOM、5タブ別スクリーンショット、参照画像を保持する。SuperCombo 派生 output は `wiki/outputs/data/frame-data/supercombo/<character>/`、公式 + SuperCombo 補助列付き output は `wiki/outputs/data/frame-data/official-supercombo-enriched/<character>/` に置く。30 キャラ分の coverage は [[sources/supercombo-street-fighter-6-frame-data-batch]] と [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] にまとまっている。公式 source と重なる基本フレーム値では Capcom 公式 data を優先し、SuperCombo は公式にない range、juggle、notes、hitbox image refs などを補助 source として扱う。公式 Classic rows を保持した SuperCombo 補助列付き output は 30 キャラ分あり、JP / Ryu / Zangief / Ingrid 以外には人間レビュー待ちの補助行が残る。

## なぜ重要か

frame-data 用語、structured capture、Classic / Modern comparison policy がないと、技データ、比較、timing-sensitive claims を安定して解釈できない。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| active は、技が相手に当たり得る状態で残る frames を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| recovery は、active frames 終了後に技が終わるまでの frames を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| startup は、技が active になるまでの frames を説明し、last startup frame と first active frame は同じ frame として扱われる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| hit/block values は、攻撃が当たった時またはガードされた時の frame advantage を説明する。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| 1 frame は 1/60 秒で、[[concepts/terms/frame-advantage|有利 frame]] は hit / guard させた後に自分が先に動き出せる時間、不利 frame は相手が先に動ける時間として説明される。 | [[sources/capcom-esports-base-terms]] | high |
| Counter は +2、[[concepts/terms/punish-counter|Punish Counter]] は +4 の advantage 増加を伴い、通常 hit より damage が 1.2 倍になると説明される。 | [[sources/capcom-esports-base-terms]] | high |
| SuperCombo HUD page は [[concepts/terms/combo-counter|Combo Counter]] を現在の combo hit 数の表示として説明し、true combo かどうかの判断補助になると述べる。 | [[sources/supercombo-street-fighter-6-hud]] | medium |
| SuperCombo HUD page は [[concepts/terms/counter-hit|Counter-hit]] icon を相手攻撃の startup / active への割り込み、[[concepts/terms/punish-counter|Punish Counter]] icon を相手の recovery への punish として説明する。 | [[sources/supercombo-street-fighter-6-hud]] | medium |
| Drive Rush からの通常技は有利 frame が増えるため強力と説明される。 | [[sources/capcom-esports-base-terms]] | high |
| [[concepts/terms/hit-confirm|hit confirm]] は通常技の hit を確認し、hit 時だけ cancel special などへ繋いで combo にする technique と説明される。 | [[sources/capcom-esports-base-terms]] | high |
| [[concepts/terms/setplay|setplay]] は相手の行動不能時間を利用した pattern 化された起き攻めで、空振りによる frame kill で timing を調整することがある。 | [[sources/capcom-esports-base-terms]] | high |
| この wiki には 30 character data slugs 分の Classic / Modern 公式 frame-data outputs がある。 | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
| frame-data raw は latest mirror 固定パスで保存し、source freshness / 取得時刻 / source revision は manifest の `source_updated_at` / `captured_at_utc` / `source_revision` で分けて追う。 | [[syntheses/frame-data-raw-layout]] | high |
| JP、Ryu、Chun-Li、Zangief captures は人間レビュー済み accepted。 | [[reviews/2026-05-26-official-jp-frame-data-capture-review]], [[reviews/2026-05-27-official-ryu-frame-data-capture-review]], [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]], [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | high |
| 2026-05-30 の 26 official captures は自動検証済みで、人間レビューは未完了。 | [[reviews/2026-05-30-official-frame-data-roster-capture-review]] | high |
| official captures は field explanations を各 control scheme JSON の `field_meanings.records` に保存している。 | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
| SuperCombo JP capture は raw template 64 件、Cargo frame rows 64 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-jp-frame-data]], [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]] | high |
| SuperCombo Ryu capture は raw template 77 件、Cargo frame rows 77 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-ryu-frame-data]], [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]] | high |
| SuperCombo Zangief 取得データは raw template 68 件、Cargo frame rows 68 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-zangief-frame-data]], [[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]] | high |
| SuperCombo Ingrid 取得データは raw template 83 件、Cargo frame rows 83 件、5タブ x 4 section の DOM table comparisons 20 件を含む。 | [[sources/supercombo-ingrid-frame-data]], [[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]] | high |
| SuperCombo frame-data raw capture と派生 output は 30 キャラ分そろっており、validation は 30/30 で `passed`。 | [[sources/supercombo-street-fighter-6-frame-data-batch]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high |
| 30 キャラ分の SuperCombo enriched output には `enriched_review_required` 1295 行、`enriched_reviewed` 69 行、SuperCombo-only 620 行が残る。 | [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high |
| 2026-06-06 の fail-closed policy 以降、複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ行は人間レビューなしでは `enriched` にしない。`着地後N` と `N land` の landing recovery 表記差、括弧・注記なしの多段 damage 合計は機械正規化済み。 | [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high |
| `enrichment_review_queues` は未レビュー補助行の理由を `uncomparable_notation`、`structural_ambiguity`、`condition_dependent_field`、`field_conflict`、`manual_or_ambiguous_match` に分けるための field。 | [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | high |
| SuperCombo 補助列の人間レビュー順は、source disagreement になり得る `field_conflict` を最優先し、次に `manual_or_ambiguous_match`、最後に query demand が高い character batch を進める。 | [[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]], [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | medium |
| SuperCombo raw では同じ input を持つ複数 row があるため、input ではなく `moveId` を行識別子として扱う。 | [[sources/supercombo-jp-frame-data]], [[sources/supercombo-ryu-frame-data]], [[sources/supercombo-zangief-frame-data]], [[sources/supercombo-ingrid-frame-data]] | high |
| Classic / Modern 比較は、公式の技名完全一致を default にする。 | [[reviews/2026-05-27-health-check]] | high |
| 読者向け command notation は display-only transform であり、raw input tokens が source-preserving data。 | [[reviews/2026-05-27-health-check]] | high |

## 比較方針

Classic / Modern frame-data comparison では、公式表の技名完全一致を default にする。`しゃがみ強K（ビッグスタンプ）` と `ビッグスタンプ` のように実質対応しそうでも名前が違う場合は、勝手に merge せず、対応候補として注記する。

読者向け回答では `↓↘→ + 強P` のような読みやすい command notation を使ってよい。ただしこれは説明用の表示変換であり、source-preserving data は公式 capture outputs の raw token data。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/index]]
- [[concepts/terms/cancel]]
- [[concepts/terms/chain]]
- [[concepts/terms/damage-scaling]]
- [[concepts/terms/drive-rush-cancel]]
- [[concepts/terms/super-art]]
- [[concepts/terms/critical-art]]
- [[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]]
- [[concepts/juggle-system]]
- [[concepts/fighting-game-notation]]
- [[entities/street-fighter-6]]

## 矛盾 / 注意点

- この page は個別技の値を網羅しない。個別値は source page と `wiki/outputs/data/...` の派生 JSON output に残し、再利用可能な question / synthesis が必要になった時だけ昇格する。
- Capcom eSports BASE source は観戦用語の説明であり、個別技の frame value source ではない。
- `input_raw_display` は raw DOM-token display であり、normalized command notation ではない。
- 30-character coverage は単一日付 snapshot ではない。JP は 2026-05-26、Ryu / Chun-Li / Zangief は 2026-05-27、残り 26 characters は 2026-05-30。
- frame-data 取得物は latest mirror 固定パスで管理する。配置と source freshness の詳細は [[syntheses/frame-data-raw-layout]] と各 source page で確認する。
- SuperCombo は community data なので、公式 Capcom data と同じ項目については公式を優先する。SuperCombo raw 取得データは削らず保持し、補助列付き output でも公式列を上書きしない。
- SuperCombo HUD page は HUD icon の display cue source として使う。[[concepts/terms/counter-hit|Counter-hit]] / [[concepts/terms/punish-counter|Punish Counter]] の advantage や damage、個別技の frame value は公式 term source や frame-data output を優先する。
- Ryu capture では `Special` / `Super` のような moveType の大文字表記が混じるため、派生処理では小文字正規化して section と照合する。
- Zangief の照合では `key-circle` を `360+`、2回転を `720+` として扱い、hold / 近距離・中距離・遠距離 / CA variant は Zangief 専用 name override で `moveId` に対応させている。
- SuperCombo 30キャラ batch では、Chun-Li の `serenity_stream`、Dee Jay の Cargo key `Dee_Jay`、C.Viper の `cancel=*SA3` 表示正規化、Jamie Specials の pagination を source に従って扱った。これらは raw を変更せず、抽出・検証の解釈を合わせるための補正。
- Ingrid capture でも `Special` / `Super` の大文字表記が混じる。Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush は Ingrid 専用 / 汎用 name override で `moveId` に対応させ、人間レビュー済み accepted にした。さらに imageinfo は face / portrait の 2 件しか解決できていないため、move / hitbox 画像の根拠利用には追加確認が必要。

## 未解決の質問

- display-only command notation を formal wiki notation schema にする条件は何か。
- 公式 patch notes / Battle Change List を ingest して、frame-data changes を時系列で扱うべきか。
- SuperCombo 30キャラ分の `enriched_review_required` 1295 行をどの順序で人間レビューするか。
- SuperCombo-only 620 行を taunt、条件付き variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。
- 補助列レビューは、source disagreement になり得る `field_conflict` を最優先し、次に `manual_or_ambiguous_match`、最後に character demand が高い Juri / Jamie / Mai などの query-driven batch を進める。
