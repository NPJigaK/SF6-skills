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
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
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
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[outputs/reports/2026-05-30-official-frame-data-coverage]]"
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
  - "[[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]]"
  - "[[syntheses/frame-data-raw-layout]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/offense]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/system-data]]"
  - "[[concepts/range-comparisons]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/terms/throw]]"
  - "[[concepts/terms/throw-escape]]"
  - "[[concepts/terms/wake-up]]"
  - "[[concepts/terms/reversal]]"
  - "[[concepts/terms/guaranteed-punish]]"
  - "[[concepts/terms/safe-jump]]"
  - "[[concepts/terms/blockstring]]"
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

Frame data は、技の発生、持続、硬直、有利不利、ダメージ、[[concepts/terms/damage-scaling|補正]]、[[concepts/terms/cancel|キャンセル]]可否、Drive gauge 変動などを説明するための timing / property vocabulary と structured move data。現在この wiki には、30 character data slugs 分の Capcom 公式 Classic / Modern frame-data outputs、Capcom 公式 eSports BASE の観戦用語説明、Capcom 公式 Battle Change List、SuperCombo Patch Notes、SuperCombo Wiki の 30 キャラ分 community frame-data source がある。SuperCombo HUD page は [[concepts/terms/combo-counter|Combo Counter]]、[[concepts/terms/counter-hit|Counter-hit]]、[[concepts/terms/punish-counter|Punish Counter]]、knockdown、[[concepts/terms/reversal|Reversal]]、[[concepts/terms/throw-escape|Throw Escape]] などの HUD icon を display cue として補う。SuperCombo Gauges page は Drive Impact、Drive Reversal、Drive Parry、Drive Rush などの system frame / cost / distance table を community numeric source として補う。SuperCombo Offense page は [[concepts/terms/throw|throw]]、[[concepts/terms/throw-loop|throw loop]]、[[concepts/terms/safe-jump|safe jump]]、[[concepts/terms/empty-jump-mixup|empty jump mixup]]、[[concepts/terms/blockstring|blockstring]] の common timing / tactical context を補う。SuperCombo Defense page は [[concepts/terms/wake-up|wake-up]] forced standing frames、[[concepts/terms/reversal|reversal]] buffer、[[concepts/terms/throw-escape|throw escape]] window、[[concepts/terms/guaranteed-punish|punish route]] の timing を補う。Patch / Battle Change sources は時系列の変更説明に使うが、個別技の現在値は frame-data output を優先する。Battle Change の `change-events.json` / `move-change-index.json` は「昔は繋がったが今は繋がらない」系の原因候補を探す入口であり、数値計算では公式本文の明示 before/after と現在 frame-data output に戻る。これらの fighter index は source-local key を残しつつ `character_slug` を持つため、過去変更を現在 frame-data output に結びつける時は `character_slug` を使う。SuperCombo Patch Notes の `change-events.json` / `move-change-index.json` は community 側の詳細説明、combo / juggle / blockstring への影響、内部的な意図説明を拾う補助 index として使う。取得物の配置と freshness の扱いは [[syntheses/frame-data-raw-layout]] と各 source page にまとめる。

SuperCombo Game Data page は、damage scaling progression、system data、range comparisons、Longest Punish `≤4F` table を含む community numeric source。Tabber 付き table は raw validation で 4 tabber groups / 46 tabs / 39 content tables として照合済みで、table text は `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` に保持する。Reader-facing な詳細表は [[concepts/terms/damage-scaling]]、[[concepts/system-data]]、[[concepts/range-comparisons]]、[[concepts/terms/guaranteed-punish]] に昇格している。

## 定義

Capcom 公式 eSports BASE は観戦者向けに、1 frame = 1/60 秒、[[concepts/terms/frame-advantage|有利 frame / 不利 frame]]、Counter / [[concepts/terms/punish-counter|Punish Counter]] の advantage 増加、Drive Rush 通常技の advantage 増加、[[concepts/terms/hit-confirm|hit confirm]]、frame kill を含む [[concepts/terms/setplay|setplay]] などを説明している。SuperCombo glossary は active frames、startup、recovery、cancel options、hit/block advantage、guard direction、damage、[[concepts/terms/damage-scaling|damage scaling]]、hitconfirm windows、[[concepts/terms/drive-rush-cancel|Drive Rush Cancel]] advantage、actionable recovery などの用語を説明している。SuperCombo HUD page は、[[concepts/terms/combo-counter|Combo Counter]]、[[concepts/terms/counter-hit|Counter-hit]]、[[concepts/terms/punish-counter|Punish Counter]] などを画面上の表示 cue として説明する community visual source として扱う。SuperCombo Gauges page は、Drive Impact、Drive Reversal、Drive Parry、Drive Rush の startup / active / recovery / block advantage / distance などを community numeric source として扱う。SuperCombo Offense page は、通常投げの startup / active / whiff、throw invincibility、Counter / Punish Counter timing、input buffer、safe jump / empty jump advantage 目安を community source として扱う。SuperCombo Defense page は、throw escape window、wake-up forced standing frames、reversal buffer、dash buffer note、armor damage、punish route advantage を community source として扱う。

SuperCombo Game Data page は、FAF を含む move stage 説明、hitstun / blockstun / hitstop、screen freeze buffer、priority、damage scaling、system data、range comparison、punish option table をまとめる community source として扱う。Tabbed table の検証結果は [[sources/supercombo-street-fighter-6-game-data]] と `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` に戻る。

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
| SuperCombo Offense page は、通常投げを startup `5f`、active `3f`、whiff animation `30f` total とし、strike と throw が同 frame に当たる場合は strike が勝つと説明する。 | [[sources/supercombo-street-fighter-6-offense]] | medium |
| SuperCombo Offense page は、Counter-hit を startup / active への strike、Punish Counter を recovery への attack とし、Counter-hit `+2` / `20%`、Punish Counter `+4` / `20%` を説明する。 | [[sources/supercombo-street-fighter-6-offense]] | medium |
| SuperCombo Offense page は、SF6 の input buffer を一般に `4f`、tightest possible links を `5f` input timing と説明する。 | [[sources/supercombo-street-fighter-6-offense]] | medium |
| SuperCombo Defense page は、Throw Escape window を thrown state の `9th` frame までとし、success 時に `5000` Drive / `1/2` bar を得ると説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |
| SuperCombo Defense page は、wake-up crouch animation の最初 `4f` を forced standing、hurtbox shrink を frame `5`、air reset landing 後を `2` forced standing frames と説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |
| SuperCombo Defense page は、wake-up reversal buffer を `10f`、hitstun / blockstun / air reset 後を `4f` とし、true reversal frame を含めて total `11f` / `5f` window と説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |
| SuperCombo Defense page は、punish combo の first attack は `4` extra frames of hit advantage を持つと説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |
| SuperCombo Game Data page は、Damage Scaling / System Data / Range Comparisons / Longest Punish の tabbed tables を含み、capture validation は 4 tabber groups、46 tabs、39 content tables を確認している。 | [[sources/supercombo-street-fighter-6-game-data]], [[reviews/2026-06-11-supercombo-game-data-web-page-capture-review]] | medium |
| SuperCombo Game Data page は Longest Punish `≤4F` table を持つが、`≤5F` から `≤12F` までは source 上で `(to-do)` として table がない。 | [[sources/supercombo-street-fighter-6-game-data]] | medium |
| Drive Rush からの通常技は有利 frame が増えるため強力と説明される。 | [[sources/capcom-esports-base-terms]] | high |
| SuperCombo Gauges page は、Drive Impact の frame data を startup `26(27)`、active `2`、recovery `35`、block `-3`、damage `800` とする。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
| SuperCombo Gauges page は、Drive Reversal の frame data を startup `20(18)`、active `3`、recovery `26(31)*`、hit KD `+23*`、block `-6`、damage `500` とする。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
| SuperCombo Gauges page は、Drive Parry の frame data を startup `1`、active `12~ [2]`、recovery `33 [1]` とする。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
| SuperCombo Gauges page は、Drive Rush の frame table を Parry~DR `3+8 / 15 / 22 / 37`、DRC `9 / 15 / 22 / 37` とし、10f freeze と通常技 +4 advantage を説明する。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
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
| SuperCombo Patch Notes の 17 detail pages は community `change-events.json` 1374 events、`move-change-index.json` 1118 targets として派生済みで、556 events は明示的な before/after 数値変更を含む。 | [[sources/supercombo-street-fighter-6-patch-notes]]; `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json` | medium |
| Battle Change / Patch Notes の fighter event は `character_slug` を持ち、公式 frame-data output の character slug と join できる。 | [[sources/capcom-official-battle-change-list]], [[sources/supercombo-street-fighter-6-patch-notes]]; `wiki/outputs/data/battle-change/official/move-change-index.json`; `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json` | medium |
| Classic / Modern 比較は、公式の技名完全一致を default にする。 | [[reviews/2026-05-27-health-check]] | high |
| 読者向け command notation は display-only transform であり、raw input tokens が source-preserving data。 | [[reviews/2026-05-27-health-check]] | high |

## 数値データ

この section は system move frame 値への索引。個別キャラの per-move frame data は `wiki/outputs/data/frame-data/official/` と `wiki/outputs/data/frame-data/official-supercombo-enriched/` を正とし、ここには複製しない。

| 対象 | 主要 frame / value | 根拠 |
|---|---|---|
| Drive Impact | startup `26(27)`, active `2`, recovery `35`, block `-3`, damage `800` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_frame_data` |
| Drive Reversal | startup `20(18)`, active `3`, recovery `26(31)*`, on hit KD `+23*`, block `-6`, damage `500` | [[sources/supercombo-street-fighter-6-gauges#Drive Reversal]]; `drive_reversal_frame_data` |
| Drive Parry | startup `1`, active `12~ [2]`, recovery `33 [1]`; `[]` は Perfect Parry | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_frame_data` |
| Parry~Drive Rush | startup `3+8`, attack-cancelable recovery `15`, fully-cancelable recovery `22`, total recovery `37` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data[type=Parry~DR]` |
| Drive Rush Cancel | startup `9`, attack-cancelable recovery `15`, fully-cancelable recovery `22`, total recovery `37` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data[type=DR Cancel]` |
| Drive Rush common | screen freeze `10f`, normal / command normal advantage `+4`, directional movement transition extra recovery `2f` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values` |
| Character-specific system distances | Drive Impact range と Drive Rush distance は 30 characters 分を source page / JSON に保持 | [[sources/supercombo-street-fighter-6-gauges#Drive Impact range table]], [[sources/supercombo-street-fighter-6-gauges#Drive Rush distance table]]; `drive_impact_range_by_character`, `drive_rush_distance_by_character` |
| Normal throw | startup `5f`, active `3f`, whiff animation `30f`; PC throw `+70%` damage / Hard Knockdown / Drive drain `1` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Throw invincibility | grounded wakeup `1f`; after hitstun / blockstun `2f`; air reset landing recovery `2f`; backdash first `15f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Throw Escape | input `LP+LK`; success gain `5000` Drive / `1/2` bar; window は thrown state `9th` frame まで | [[sources/supercombo-street-fighter-6-defense#Throw Escape]] |
| Wake-up / forced standing | wake-up crouch animation: `4f` forced standing, hurtbox shrink frame `5`; air reset landing: `2f` forced standing | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Reversal buffer | wake-up `10f` / total `11f`; hitstun / blockstun / air reset 後 `4f` / total `5f`; dash buffer intended `7f` | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Punish route | punish combo first attack gets `4` extra frames of hit advantage | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |
| Safe jump / empty jump | standard `45f` jump safe jump: `+42` vs 5f anti-air, `+41` vs 6f reversal; empty jump mixup: `+45` or slightly better | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] |
| Game Data tabbed tables | 39 content tables: damage scaling progression, 30 character-specific scaling tabs, 3 system data tabs, 4 range comparison tabs, Longest Punish `≤4F` | [[sources/supercombo-street-fighter-6-game-data]]; `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` |
| Frame unit | `1f = 1/60` second; `60f = 60` frames | [[sources/supercombo-street-fighter-6-game-data]] |
| FAF / First Active Frame startup | total attack frames are `Startup + Active + Recovery - 1`; `+5` advantage combos into 5f startup, `-7` disadvantage can be punished by 7f startup | [[sources/supercombo-street-fighter-6-game-data]] |
| General input buffer | most moves can be buffered up to `4f` early, giving a `5f` earliest-timing input window | [[sources/supercombo-street-fighter-6-game-data]] |
| Dash / wake-up reversal buffer | dash and wake-up reversals have `7f` buffer, `8f` total input window; source notes Ryu `5MP` block dash buffer exception as `4f` | [[sources/supercombo-street-fighter-6-game-data]] |
| Crouch hurtbox / Parry from crouch | standing-to-crouching hurtbox fully shifts on frame `5`; Parry from crouch keeps crouching hurtbox for first `2f` and stands on frame `3` | [[sources/supercombo-street-fighter-6-game-data]] |
| Recoverable HP | cooldown `120f`, restores `2HP/f`; `500` damage Drive Reversal example takes `370f` / `6.17s` total to recover | [[sources/supercombo-street-fighter-6-game-data]] |
| System Data tables | HP, throw range, walk speed, dash speed / distance, jump speed / distance / apex | [[concepts/system-data]]; `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` tables `31..33` |
| Range Comparison tables | Cancelable 2MK range, 4f normal range / hitstun / pushback, 5f punish options, sweep ranges | [[concepts/range-comparisons]]; `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` tables `34..37` |

## 比較方針

Classic / Modern frame-data comparison では、公式表の技名完全一致を default にする。`しゃがみ強K（ビッグスタンプ）` と `ビッグスタンプ` のように実質対応しそうでも名前が違う場合は、勝手に merge せず、対応候補として注記する。

読者向け回答では `↓↘→ + 強P` のような読みやすい command notation を使ってよい。ただしこれは説明用の表示変換であり、source-preserving data は公式 capture outputs の raw token data。

## 関連

- [[concepts/defense]]
- [[concepts/drive-system]]
- [[concepts/offense]]
- [[concepts/system-data]]
- [[concepts/range-comparisons]]
- [[concepts/terms/index]]
- [[concepts/terms/throw]]
- [[concepts/terms/throw-escape]]
- [[concepts/terms/wake-up]]
- [[concepts/terms/reversal]]
- [[concepts/terms/guaranteed-punish]]
- [[concepts/terms/safe-jump]]
- [[concepts/terms/blockstring]]
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
- SuperCombo Gauges page は Drive system の community numeric source として使う。system move の frame / distance / Drive damage 値は有用だが、公式 source や実機検証がある場合はそちらを優先する。
- SuperCombo Offense page は attack timing / tactical setup の community source として使う。throw range、safe jump、empty jump、throw loop の値や character-specific notes は公式値として扱わない。
- SuperCombo Defense page は defensive timing / tactical setup の community source として使う。throw escape window、wake-up forced standing、reversal buffer、armor damage、punish route values は公式値として扱わない。
- SuperCombo Game Data page は damage scaling、system data、range comparison、punish option table の community numeric source として使う。Tabbed table は capture completeness を検証済みだが、各 gameplay value は公式値として扱わない。
- Capcom 公式 Battle Change List と SuperCombo Patch Notes は version/update の変更説明 source として raw capture 済み。現在値の回答では frame-data output を優先し、過去 update の説明では official source と community source を分ける。`wiki/outputs/data/battle-change/official/change-events.json` は公式 change rows に `change_types`、明示的な before/after、`confidence` を付けた検索補助で、非数値 bugfix / hitbox / behavior 変更は数値計算ではなく原因候補として扱う。`wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json` は SuperCombo detail page の top-level bullet、nested explanation、wikitext table text を community event として保持し、combo / juggle / blockstring の背景説明を探す補助 source として扱う。どちらも `fighter_tool_name` / `fighter_key` は source-local key、`character_slug` は frame-data join key として読む。
- Ryu capture では `Special` / `Super` のような moveType の大文字表記が混じるため、派生処理では小文字正規化して section と照合する。
- Zangief の照合では `key-circle` を `360+`、2回転を `720+` として扱い、hold / 近距離・中距離・遠距離 / CA variant は Zangief 専用 name override で `moveId` に対応させている。
- SuperCombo 30キャラ batch では、Chun-Li の `serenity_stream`、Dee Jay の Cargo key `Dee_Jay`、C.Viper の `cancel=*SA3` 表示正規化、Jamie Specials の pagination を source に従って扱った。これらは raw を変更せず、抽出・検証の解釈を合わせるための補正。
- Ingrid capture でも `Special` / `Super` の大文字表記が混じる。Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush は Ingrid 専用 / 汎用 name override で `moveId` に対応させ、人間レビュー済み accepted にした。さらに imageinfo は face / portrait の 2 件しか解決できていないため、move / hitbox 画像の根拠利用には追加確認が必要。

## 未解決の質問

- display-only command notation を formal wiki notation schema にする条件は何か。
- Battle Change List / SuperCombo Patch Notes の version detail を、character 別または version 別の時系列 synthesis へ昇格する条件は何か。`move-change-index.json` の query 実績を見て、よく使う character / move から昇格する。
- SuperCombo 30キャラ分の `enriched_review_required` 1295 行をどの順序で人間レビューするか。
- SuperCombo-only 620 行を taunt、条件付き variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。
- 補助列レビューは、source disagreement になり得る `field_conflict` を最優先し、次に `manual_or_ambiguous_match`、最後に character demand が高い Juri / Jamie / Mai などの query-driven batch を進める。
- SuperCombo Gauges の `numeric-tables.json` schema を、character-specific numeric query 用の標準 output として固定するか。
