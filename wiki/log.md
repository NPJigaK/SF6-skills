# Wiki Log

これは LLM-maintained wiki の時系列・追記専用アクティビティログです。

## [2026-06-16] synthesis | Battle Change read order quick reference
- 更新:
  - `wiki/syntheses/battle-change-version-timeline.md`
  - `wiki/log.md`
- 検証:
  - `$sf6-wiki-query` の query-only 検証で見つかった friction を受け、synthesis 冒頭に `Read order quick reference` を追加した。
  - 追加内容は既存の authority model / query recipes の短縮版に限定し、source authority、validation status、patch fact、frame value は変更していない。
  - `raw/`、`tools/`、derived output は変更していない。
- メモ:
  - `wiki/index.md` の summary は既に version timeline、authority model、freshness rules、derived output、current value / historical explanation の読み分けを含むため、今回は更新していない。

## [2026-06-16] synthesis | Battle Change version timeline draft
- 作成:
  - `wiki/syntheses/battle-change-version-timeline.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/reviews/2026-06-16-battle-change-version-timeline-refactor-plan.md`
- 検証:
  - `$sf6-durable-output` と `$sf6-wiki-refactor` の方針に従い、review plan を actual synthesis draft へ昇格した。
  - `jq` で official versions 20、official change events 1820、official move-index rows 1419、SuperCombo versions 17、SuperCombo events 1374、SuperCombo targets 1118、crosswalk 16 matched / 1 launch / 4 official-only を再確認した。
  - `raw/`、`tools/`、derived output は変更していない。
- メモ:
  - synthesis は `status: review-needed`、`confidence: medium` とし、official-only 4 update、launch row、SuperCombo detail 昇格粒度、community detail と official fact の境界を未解決項目として残した。
  - source authority、validation status、patch fact、frame value は変更していない。

## [2026-06-16] refactor-plan | Battle Change version timeline synthesis plan
- 作成:
  - `wiki/reviews/2026-06-16-battle-change-version-timeline-refactor-plan.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `$sf6-wiki-refactor` の read-only plan で選定した Battle Change / SuperCombo Patch Notes version timeline synthesis 候補を、actual synthesis 作成前の refactor plan として永続化した。
  - `jq` で official versions 20、official change events 1820、official move-index rows 1419、SuperCombo versions 17、SuperCombo events 1374、SuperCombo targets 1118、crosswalk 16 matched / 1 launch / 4 official-only を確認した。
  - `raw/` と `tools/` は変更していない。
- メモ:
  - 今回は actual synthesis page、derived output 再生成、page merge / split / rename / directory move、source authority / validation status / patch fact の変更は行っていない。
  - official-only 4 update、launch row、SuperCombo detail の昇格粒度、community detail を official fact と誤読しない表記は人間レビュー項目として残した。

## [2026-06-16] schema-review | jq and Obsidian skills made repo-local
- 作成:
  - `.agents/skills/jq-cli/`
  - `.agents/skills/obsidian-markdown/` の tracked repo-local skill 化
- 更新:
  - `AGENTS.md`
  - `.agents/skills/sf6-source-ingest/SKILL.md`
  - `.agents/skills/sf6-wiki-query/SKILL.md`
  - `.agents/skills/sf6-durable-output/SKILL.md`
  - `.agents/skills/sf6-wiki-health-check/SKILL.md`
  - `.gitignore`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - `jq-cli` を global skill から repo-local skill に取り込み、JSON / JSONL の値・件数・validation では `$jq-cli` skill と `jq` / `jq -e` を明示利用する方針にした。
  - 既存の `.agents/skills/obsidian-markdown/` を track 対象にし、Obsidian Flavored Markdown では `$obsidian-markdown` skill を明示利用する方針にした。
  - 直前 entry の `jq-cli` / `obsidian-markdown` optional local skill 扱いの未解決事項は、この方針で superseded とする。

## [2026-06-16] schema-review | Wiki refactor workflow boundary clarified
- 更新:
  - `AGENTS.md`
  - `.agents/skills/sf6-wiki-health-check/SKILL.md`
  - `wiki/log.md`
- メモ:
  - raw capture / raw update 専用 skill が未定義であることを明記し、`$sf6-source-ingest` は既存 raw source / raw package を wiki に compile する skill として境界を締めた。
  - P2 Structure の `structural merge` 表現を締め、page merge / split / rename / directory move は原則 refactor plan first とした。
  - `$sf6-wiki-refactor` 用の短い `Refactor ワークフロー` section を `AGENTS.md` に追加した。

## [2026-06-16] schema | Karpathy-style wiki refactor workflow added
- 作成:
  - `.agents/skills/sf6-wiki-refactor/SKILL.md`
  - `.agents/skills/sf6-wiki-refactor/agents/openai.yaml`
- 更新:
  - `AGENTS.md`
  - `.agents/skills/sf6-source-ingest/SKILL.md`
  - `.agents/skills/sf6-wiki-query/SKILL.md`
  - `.agents/skills/sf6-durable-output/SKILL.md`
  - `.agents/skills/sf6-wiki-health-check/SKILL.md`
  - `.gitignore`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Karpathy-style の `wiki/` refactor / recompile を一級 workflow として追加した。
  - `raw/` は source of truth として保護し、`wiki/` は LLM-maintained compiled knowledge として積極的に再編可能にした。
  - source ingest、query、durable output、health check から wiki improvement / refactor へ戻る feedback loop を追加した。
  - `sf6-source-ingest` は既存 raw source を wiki に compile する skill とし、raw capture / raw update は別 workflow 扱いに寄せた。
- 未解決事項:
  - Calculation Tool Gate / Combo Damage Ledger Preflight の詳細を、将来 `sf6-calculation-grounding` skill または wiki concept へ分離するか。
  - `jq-cli` / `obsidian-markdown` の optional local skill 扱いを長期的にどうするか。

## [2026-06-16] implementation | Source-backed combo damage calculator and evaluation groundwork
- 作成:
  - `tools/calculations/combo_damage/calculate.py`
  - `tests/calculations/combo_damage/test_calculate.py`
  - `tests/calculations/combo_damage/fixtures/**/*.ledger.json`
  - `wiki/outputs/data/calculations/combo-damage/schema.json`
  - `wiki/concepts/combo-damage-ledger-protocol.md`
  - `wiki/reviews/2026-06-15-jp-combo-damage-ledger-regression.md`
  - `wiki/reviews/2026-06-15-mai-combo-damage-ledger-regression.md`
  - `wiki/outputs/reports/2026-06-16-calculation-system-future-readiness-review.md`
  - `docs/superpowers/specs/2026-06-16-combo-prediction-evaluation-loop-design.md`
- 更新:
  - `AGENTS.md`
  - `README.md`
  - `pyproject.toml`
  - `uv.lock`
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/index.md`
  - `wiki/outputs/lint/2026-06-11-health-check.md`
  - `wiki/outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation.md`
  - `wiki/reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap.md`
- 検証:
  - `$env:PYTHONPATH = (Get-Location).Path; uvx --with sympy --with pytest pytest tests\calculations tests\test_output_data_json_only.py` (`30 passed`)
  - `jq empty` for `tests/calculations/combo_damage/fixtures/**/*.ledger.json` and `wiki/outputs/data/calculations/combo-damage/schema.json`
  - `jq` fixture count / numeric `hit_span` range rejection check
  - `$env:PYTHONPATH = (Get-Location).Path; uvx --with sympy python -m tools.calculations.combo_damage.calculate tests/calculations/combo_damage/fixtures/jp/classic/2025-10-25-5hp-pc-3178.ledger.json | jq -e '.total_damage == 3178 and .matches_expected == true'`
  - `git diff --check` and `git diff --cached --check`
- メモ:
  - `combo_damage` は SymPy `Rational` / `floor` による deterministic hit / segment ledger 算術に限定し、candidate authority、provenance 不足、暗黙 scaling、数値 range の aggregated `hit_span` を拒否する。
  - regression fixture は `tests/calculations/combo_damage/fixtures/<character>/<control>/` に配置し、filename は `YYYY-MM-DD-<starter>[-condition]-<total_damage>.ledger.json` を基本にした。
  - JP Year1 ODアムネジア 5790 は legacy regression fixture として保持する。fixture date は gameplay ruleset を代表する `2024-02-24`、動画投稿日は metadata、SA3 は `move_total` segment として扱い内部 hit split は modeled としない。
  - JP / Mai regression fixture は human/video validation に基づく個別 route の再計算防止であり、個別 route の成功を calculator の `validated_rule` へ自動昇格しない。
  - prediction / postmortem ループは、prediction hash、authority、fixture promotion、rule promotion を分け、route parser / frame simulator より先に評価記録を安定化する方針にした。
- 未解決事項:
  - `combo-evaluation` の prediction / postmortem validator と accuracy report generator はまだ未実装。
  - 外部動画 / screenshot の raw package policy は未決定。

## [2026-06-15] 修正 | PDR cost_bars field 契約の明確化
- 更新:
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
  - `wiki/concepts/terms/raw-drive-rush.md`
  - `wiki/sources/supercombo-street-fighter-6-gauges.md`
  - `wiki/outputs/lint/2026-06-11-health-check.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `Drive Rush from Parry` は `cost_bars` を単一 direct cost として使わず、`transition_component_cost_bars: 0.5` と `minimum_total_cost_bars: 1.0` を別 field に分ける方針にした。
  - `2026-06-11-health-check` の PDR cost 未解決扱いは、2026-06-15 の component / total 整理で superseded と明記した。
- メモ:
  - `cost_bars` だけを読む downstream が「PDR cost は 0.5」と誤答しないよう、PDR の `cost_bars` は `null` のまま維持する。

## [2026-06-15] review/update | PDR cost component 解釈の整理
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/gauges/page.raw.wikitext`
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
  - `wiki/outputs/data/battle-change/official/change-events.json`
  - `wiki/outputs/data/frame-data/official/luke/classic.json`
- 作成:
  - `wiki/reviews/2026-06-15-pdr-cost-component-video-observation.md`
- 更新:
  - `wiki/concepts/terms/raw-drive-rush.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/sources/supercombo-street-fighter-6-gauges.md`
  - `wiki/sources/capcom-official-battle-change-list.md`
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Capcom 公式の Drive Parry からの Drive Rush cost `1` は、SuperCombo の Drive Parry activation `0.5` と Drive Rush from Parry transition `0.5` の最小総消費として扱う。
  - SuperCombo の cost table `1/2` と section / caption `1 Drive Stock` は source conflict ではなく、component と total の粒度差として整理した。
  - `→, →+Parry` の入力推奨と training 1本設定後の前進回復は、今回の残す情報から外した。
- 未解決事項:
  - frame `4` の hold drain が特定入力で何 frame 分乗るか、入力履歴だけでどこまで判定できるかは未確定として残す。

## [2026-06-12] 修正 | Patch Notes freshness と batch raw path pattern の分離
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/validation.batch.json`
  - `raw/frame-data/supercombo/`
- 更新:
  - `wiki/sources/supercombo-street-fighter-6-patch-notes.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/outputs/lint/2026-06-11-health-check.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - Patch Notes root page の `source_updated_at` は raw manifest の `2023-09-27T14:23:05Z`、detail pages の最新 freshness は `latest_detail_source_updated_at: 2026-06-02T03:12:40Z` として分離した。
  - `detail_page_count: 17`、`detail_page_validation_status: passed`、`batch_validation_status: passed` を source page frontmatter に明記した。
  - SuperCombo 30キャラ batch source の `raw_path` を実在する `raw/frame-data/supercombo/` にし、character manifest の pattern は `raw_path_pattern` に分けた。
- メモ:
  - `Drive Rush from Parry` cost 表記揺れは内部数値だけでは検証できないため、単一値へ正規化せず unresolved のまま残す。
  - open review pages の dashboard 化は別 follow-up として扱う。

## [2026-06-11] lint | Wiki health check
- 作成:
  - `wiki/outputs/lint/2026-06-11-health-check.md`
- 更新:
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - Markdown frontmatter、wikilink、index 掲載、orphan-like page、duplicate title を確認した。
  - `jq empty` で `wiki/**/*.json` 371 件、`raw/**/*.json` 793 件に parse error がないことを確認した。
  - `raw/**/validation*.json` 59 件が pass 系 status であることを確認した。
  - official frame-data 30 source page の Classic / Modern row count と derived JSON `row_count` の一致を確認した。
  - Battle Change、SuperCombo Patch Notes、Game Data、Gauges の主要 derived count を `jq -e` で確認した。
- 修正:
  - SuperCombo JP / Ryu source page の `captured_at_utc` を raw manifest と同期した。
- 未解決事項:
  - Patch Notes の root page freshness と detail page 最新 freshness を frontmatter schema 上で分けるか。
  - `Drive Rush from Parry` cost 表記揺れを component 分解と見るか、source-internal conflict として残すか。

## [2026-06-11] 修正 | SuperCombo Game Data tabber pipeline の正式統合
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/game-data/manifest.json`
- raw-derived artifact:
  - `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`
- 更新:
  - `tools/web_pages/supercombo_page.py`
  - `raw/web-pages/wiki.supercombo.gg/game-data/metadata.json`
  - `raw/web-pages/wiki.supercombo.gg/game-data/validation.tabbers.json`
  - `raw/web-pages/wiki.supercombo.gg/game-data/rendered/tabbers.dom.json`
  - `wiki/sources/supercombo-street-fighter-6-game-data.md`
  - `wiki/reviews/2026-06-11-supercombo-game-data-web-page-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - temp repo root で `tools/web_pages/supercombo_page.py --page-title "Street Fighter 6/Game Data" --page-slug game-data` を実行し、`validation_status: passed`、`tabber_validation_status: passed` を確認した。
  - 実 repo でも同じ command を実行し、MediaWiki revision `365507`、`captured_at_utc` `2026-06-11T13:38:34Z`、tabber groups `4`、tabs `46`、content tables `39`、navigation table `1` を再生成した。
  - manifest / metadata に `game_data_tabber_pipeline` と `raw_derived_artifacts` を記録し、再取得時に `rendered/tabbers.dom.json`、`validation.tabbers.json`、`tabber-tables.json` が同じ capture pass で更新されるようにした。
- メモ:
  - `validation.tabbers.json` は stale cleanup 対象に追加した。`rendered/tabbers.dom.json` は `rendered/` cleanup、`tabber-tables.json` は Game Data 再取得開始時の raw-derived artifact cleanup と再生成で同期する。

## [2026-06-11] update | SuperCombo Game Data numeric tables promoted to concepts
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/game-data/manifest.json`
- raw-derived artifact:
  - `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`
- 作成:
  - `wiki/concepts/system-data.md`
  - `wiki/concepts/range-comparisons.md`
- 更新:
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/concepts/terms/guaranteed-punish.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/terms/index.md`
  - `wiki/sources/supercombo-street-fighter-6-game-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `tabber-tables.json` の tables `0..30` を [[concepts/terms/damage-scaling]] に昇格した。Character-Specific Scaling は 30 character tables / 323 rendered rows。
  - tables `31..33` を [[concepts/system-data]] に昇格した。
  - tables `34..37` を [[concepts/range-comparisons]] に昇格した。
  - table `38` を [[concepts/terms/guaranteed-punish]] に昇格した。
- メモ:
  - これらは community numeric source の reader-facing table であり、公式 source または実機検証と矛盾する場合はそちらを優先する。
  - [[concepts/frame-data]] には `1f = 1/60`、FAF、input buffer、crouch hurtbox、recoverable HP など Game Data の scalar numeric facts も索引化した。

## [2026-06-11] ingest | SuperCombo Game Data web-page raw capture
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/game-data/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/game-data/page.raw.wikitext`
- raw-derived artifact:
  - `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`
- 作成:
  - `wiki/sources/supercombo-street-fighter-6-game-data.md`
  - `wiki/reviews/2026-06-11-supercombo-game-data-web-page-capture-review.md`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/game-data/validation.json` は `passed`。
  - `raw/web-pages/wiki.supercombo.gg/game-data/validation.tabbers.json` は `passed`。
  - Tabber validation は 4 groups、46 tabs、source table / Cargo tabs `30 / 3 / 4 / 1`、content tables 39、navigation table 1、live revision `365507` を確認した。
  - `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` は rendered DOM の table text を保持し、SF6 Navigation table を `excluded_tables` に分離する。
- メモ:
  - SuperCombo Game Data は community numeric source として扱い、公式 source と重なる values では公式 source を優先する。
  - Longest Punish `≤5F` から `≤12F` は source 上で `(to-do)` のため、table 欠落ではなく source content として記録する。
- 未解決事項:
  - Character-specific scaling、system data、range comparison、Longest Punish `≤4F` values を公式 source または実機検証で照合するか。
  - Character-specific scaling tabs を moveId-linked schema に正規化するか。

## [2026-06-11] ingest | SuperCombo Defense web-page raw capture
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/defense/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/defense/page.raw.wikitext`
- 作成:
  - `wiki/sources/supercombo-street-fighter-6-defense.md`
  - `wiki/concepts/defense.md`
  - `wiki/concepts/terms/blocking.md`
  - `wiki/concepts/terms/wake-up.md`
  - `wiki/concepts/terms/armor.md`
  - `wiki/reviews/2026-06-11-supercombo-defense-web-page-capture-review.md`
- 更新:
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/throw-escape.md`
  - `wiki/concepts/terms/drive-parry.md`
  - `wiki/concepts/terms/reversal.md`
  - `wiki/concepts/terms/anti-air.md`
  - `wiki/concepts/terms/cross-up.md`
  - `wiki/concepts/terms/blockstring.md`
  - `wiki/concepts/terms/invincible-move.md`
  - `wiki/concepts/terms/guaranteed-punish.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/defense/validation.json` は `passed`。
  - MediaWiki page / raw wikitext / API / templates API / render fetch は取得済み。API revision wikitext と `action=raw` wikitext は一致。
  - Rendered DOM は heading 9 件、table 1 件。table は SF6 Navigation で、本文数値表ではない。
  - Rendered button / direction media は 14 件保存。navigation / character icon 30 件は excluded provenance として記録され、original media download 対象外。
- メモ:
  - SuperCombo Defense は community source として扱い、公式 source と重なる Drive / invincibility / anti-air mechanics では公式 source を優先する。
  - Blocking、throw escape、wake-up、reversal buffer、armor、anti-air、punish route は source page と term pages に戻れる形で集約した。
  - Defense page の table は navigation table のみなので、今回は `wiki/outputs/data/` に derived JSON を作らず source page の数値索引に保持した。
- 未解決事項:
  - Throw escape window、reversal buffer、wake-up forced standing frames、armor damage を公式 source または実機検証で照合するか。
  - Defense と Offense を横断して、strike / throw / shimmy / reversal / parry の defensive decision tree を synthesis にするか。
  - Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric facts を derived JSON にする基準をどうするか。

## [2026-06-11] ingest | SuperCombo Offense web-page raw capture
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/offense/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/offense/page.raw.wikitext`
- 作成:
  - `wiki/sources/supercombo-street-fighter-6-offense.md`
  - `wiki/concepts/offense.md`
  - `wiki/concepts/terms/throw.md`
  - `wiki/concepts/terms/throw-loop.md`
  - `wiki/concepts/terms/safe-jump.md`
  - `wiki/concepts/terms/empty-jump-mixup.md`
  - `wiki/concepts/terms/blockstring.md`
  - `wiki/reviews/2026-06-11-supercombo-offense-web-page-capture-review.md`
- 更新:
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/counter-hit.md`
  - `wiki/concepts/terms/punish-counter.md`
  - `wiki/concepts/terms/stun.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/offense/validation.json` は `passed`。
  - MediaWiki page / raw wikitext / API / templates API / render fetch は取得済み。API revision wikitext と `action=raw` wikitext は一致。
  - Rendered DOM は heading 17 件、table 2 件。本文 table は Throw Ranges 1 件、もう 1 件は SF6 Navigation。
  - Content media は 0 件。navigation / character icon 30 件は excluded provenance として記録され、download 対象外。
- メモ:
  - SuperCombo Offense は community source として扱い、公式 source と重なる Counter / Punish Counter / Drive / Stun mechanics では公式 source を優先する。
  - Throw range、throw invincibility、safe jump、empty jump、throw loop、blockstring は source page と term pages に戻れる形で集約した。
  - Throw range table は小規模なため、今回は `wiki/outputs/data/` に derived JSON を作らず source page の数値表に保持した。
- 未解決事項:
  - Throw range、throw loop、safe jump values を公式 source または実機検証で照合するか。
  - Character-specific throw loop notes を character entity / character source page へどの粒度で backlink するか。
  - Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric tables を derived JSON にする基準をどうするか。

## [2026-06-11] review | JP Year1 ODアムネジア 5790 combo calculation model gap
- 原本:
  - `https://www.youtube.com/shorts/g-m0AFGe4jY` (yt-dlp で metadata / video frame を一時取得して確認)
- 作成:
  - `wiki/reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap.md`
  - `wiki/outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation.md`
- 更新:
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `yt-dlp 2026.06.09` で YouTube Short metadata と 1080x1920/60fps video を一時取得した。
  - `ffmpeg` で 0.1s / 0.5s 刻みの gameplay crop を作り、`720/510/510/650/440/360/350/125/125/SA3 2000` の hit ledger と `16 HITS / 5790` を確認した。
  - `jq` で JP official / SuperCombo frame-data と 2024-02-27 Battle Change を確認し、`jq -n '[720,510,510,650,440,360,350,125,125,2000] | add'` が `5790` を返すことを確認した。
- メモ:
  - 前回の `evidence_gap` 見立ては不正確だった。このケースは source 不足ではなく、delayed OD Amnesia Bomb、2024-02-27 前の即時補正15%、Punish Counter、SA3 minimum scaling を統合する計算手順が不足していた。
  - exact combo damage query では、route text だけでなく damaging hit ledger を作ってから答える。
- 未解決事項:
  - 通常 combo hit scaling の基礎表を、どの source を正として wiki に取り込むか。
  - YouTube / community video evidence の raw capture policy と review 基準を定義するか。

## [2026-06-11] output-fix | Battle Change canonical character slugs and SuperCombo upstream regeneration
- 原本:
  - `raw/battle-change/official/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/rendered/main.dom.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/<version-slug>/manifest.json`
- 更新:
  - `tools/battle_change/characters.py`
  - `tools/battle_change/official/extract.py`
  - `tools/battle_change/supercombo/extract.py`
  - `tests/battle_change/test_official_extraction.py`
  - `tests/battle_change/test_supercombo_extraction.py`
  - `tests/test_output_data_json_only.py`
  - `wiki/outputs/data/battle-change/official/change-events.json`
  - `wiki/outputs/data/battle-change/official/move-change-index.json`
  - `wiki/outputs/data/battle-change/official/schema.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/schema.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/version-captures.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/validation.batch.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`
  - `wiki/sources/capcom-official-battle-change-list.md`
  - `wiki/sources/supercombo-street-fighter-6-patch-notes.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `python -m pytest tests/battle_change/test_official_extraction.py tests/battle_change/test_supercombo_extraction.py tests/test_output_data_json_only.py -q`
  - `python -m tools.battle_change.official.extract --repo-root .`
  - `python -m tools.battle_change.supercombo.extract --repo-root .`
- メモ:
  - `fighter_tool_name` / `fighter_key` は source-local key として保持し、frame-data output との join には `character_slug` を使う。`gouki` / `honda` / `vega` は `gouki_akuma` / `ehonda` / `vega_mbison` に対応させた。
  - SuperCombo upstream derived artifacts は `tools.battle_change.supercombo.extract` で root DOM table と detail manifests から再生成する。`versions.json` の `fields` も row keys と同期する。
- 未解決事項:
  - `target_title` の技名正規化はまだ source text ベースの機械抽出。よく使う character / move から人間レビューで補正する。

## [2026-06-11] output | SuperCombo Patch Notes community change-event index
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/<version-slug>/page.raw.wikitext`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`
- 作成:
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json`
  - `tools/battle_change/supercombo/__init__.py`
  - `tools/battle_change/supercombo/extract.py`
  - `tests/battle_change/test_supercombo_extraction.py`
- 更新:
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/schema.json`
  - `wiki/sources/supercombo-street-fighter-6-patch-notes.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `python -m pytest tests/battle_change/test_supercombo_extraction.py`
  - `python -m tools.battle_change.supercombo.extract --repo-root .`
  - `change-events.json` は 1374 community events、`move-change-index.json` は 1118 targets、明示 before/after 数値変更を持つ event は 556 件。
  - `source_authority` は `community`、`source_family` は `supercombo-patch-notes`、raw path は `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/` 配下に限定。
- メモ:
  - top-level bullet を 1 event とし、nested bullet と wikitext table text を同じ event に保持する。SuperCombo の説明は公式 source の置き換えではなく、combo / juggle / blockstring への影響や community terminology を探す補助 index として扱う。
  - 公式 Battle Change id は SuperCombo page の明示 link から来た `official_battle_change_id_from_link` として保持し、公式 event との同一性は仮定しない。
- 未解決事項:
  - `target_title` と `change_types` は機械抽出なので、よく使う character / move から人間レビューで refinement する。

## [2026-06-11] output | Battle Change change-event index
- 原本:
  - `raw/battle-change/official/manifest.json`
  - `wiki/outputs/data/battle-change/official/changes.json`
- 作成:
  - `wiki/outputs/data/battle-change/official/change-events.json`
  - `wiki/outputs/data/battle-change/official/move-change-index.json`
- 更新:
  - `tools/battle_change/official/extract.py`
  - `tests/battle_change/test_official_extraction.py`
  - `wiki/outputs/data/battle-change/official/schema.json`
  - `wiki/sources/capcom-official-battle-change-list.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `python -m pytest tests/battle_change/test_official_extraction.py`
  - `python -m tools.battle_change.official.extract --repo-root .`
  - `change-events.json` は 1820 events、`move-change-index.json` は 1419 targets。
- メモ:
  - `change-events.json` は公式 change rows の検索補助。`change_types`、明示的な before/after、`confidence` を付けるが、公式本文を置き換える正規化版ではない。
  - combo / frame-data query では、現在値は frame-data output、過去変更の原因候補は Battle Change index、最終根拠は公式 `text_html` と raw source に戻す。
- 未解決事項:
  - `change_types` の機械分類は query 実績に合わせて調整する。非数値 bugfix / hitbox / behavior 変更は数値計算ではなく原因候補として扱う。

## [2026-06-11] ingest | SuperCombo Patch Notes web-page raw capture
- 原本:
  - `https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`
- 作成:
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/`
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/<version-slug>/`
  - `wiki/sources/supercombo-street-fighter-6-patch-notes.md`
  - `wiki/reviews/2026-06-11-supercombo-patch-notes-web-page-capture-review.md`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`
  - `wiki/outputs/data/battle-change/supercombo-patch-notes/schema.json`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/patch-notes/validation.batch.json` は `passed`。
  - Patch Notes table は 17 version rows、detail page capture は 17/17、detail validation は 17/17 passed。
  - SuperCombo row から Capcom 公式 Battle Change id へ明示 link できるものは 16 rows。`1.00` は launch version で official battle_change id なし。
  - 公式 Battle Change 側の `20251113`、`20251022`、`20250901`、`20230808` は SuperCombo Patch Notes table から直接リンクされていない。
- メモ:
  - Patch Notes 本体の wikitext は Cargo query だけなので、version 一覧は rendered DOM と derived output を入口にする。
  - 各 version の詳細本文は `versions/<version-slug>/page.raw.wikitext` を正本にする。
  - Capcom 公式 Battle Change List と SuperCombo Patch Notes は authority を分け、公式 source と重なる変更説明では公式を優先する。
- 未解決事項:
  - SuperCombo detail page の character 変更を、version 別 synthesis、character 別 synthesis、または official Battle Change の補助列としてどの粒度で昇格するか。
  - Official-only update 4 件を SuperCombo timeline gap として扱うか、公式 hotfix-only update として分けるか。

## [2026-06-11] workflow | JSON data access uses jq
- 更新:
  - `AGENTS.md`
  - `.agents/skills/sf6-source-ingest/SKILL.md`
  - `.agents/skills/sf6-wiki-query/SKILL.md`
  - `.agents/skills/sf6-durable-output/SKILL.md`
  - `.agents/skills/sf6-wiki-health-check/SKILL.md`
  - `wiki/log.md`
- 検証:
  - `jq --version` は `jq-1.8.1`。
- メモ:
  - `wiki/outputs/data/`、raw manifest / metadata / validation、frame-data JSON、numeric derived output から値・件数・数値を読む時は `$jq-cli` skill と `jq` を第一選択にする。
  - 重要な数値 claim や row count / validation status は、可能な限り `jq -e` の exit status で確認する。
  - Python は既存 repo tool、複数 file をまたぐ domain-specific 生成・検証、または `jq` だけでは不自然な構造処理に限定する。

## [2026-06-11] wiki-update | SuperCombo Gauges numeric query surface
- 原本:
  - `wiki/sources/supercombo-street-fighter-6-gauges.md`
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
- 更新:
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/burnout.md`
  - `wiki/concepts/terms/chip-damage.md`
  - `wiki/concepts/terms/critical-art.md`
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/concepts/terms/drive-impact.md`
  - `wiki/concepts/terms/drive-parry.md`
  - `wiki/concepts/terms/drive-reversal.md`
  - `wiki/concepts/terms/drive-rush-cancel.md`
  - `wiki/concepts/terms/overdrive.md`
  - `wiki/concepts/terms/perfect-parry.md`
  - `wiki/concepts/terms/raw-drive-rush.md`
  - `wiki/concepts/terms/stun.md`
  - `wiki/concepts/terms/super-art.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - 主要 term に `## 数値データ`、`drive-system.md` に横断 `## 数値索引`、`frame-data.md` に system move frame の `## 数値データ` を追加した。
- メモ:
  - 30 character の Drive Impact range / Drive Rush distance table は term page に複製せず、source page と `numeric-tables.json` を正とする。
  - Term page の数値表は回答時の入口であり、公式 source または実機検証と重なる場合はそちらを優先する。
- 未解決事項:
  - `numeric-tables.json` の schema を他の gauge / system numeric source にも使う標準 schema として固定するか。

## [2026-06-11] ingest | SuperCombo Gauges web-page raw capture
- 原本:
  - `https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges`
  - `raw/web-pages/wiki.supercombo.gg/gauges/manifest.json`
- 作成:
  - `raw/web-pages/wiki.supercombo.gg/gauges/`
  - `wiki/sources/supercombo-street-fighter-6-gauges.md`
  - `wiki/reviews/2026-06-11-supercombo-gauges-web-page-capture-review.md`
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
- 更新:
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/burnout.md`
  - `wiki/concepts/terms/chip-damage.md`
  - `wiki/concepts/terms/critical-art.md`
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/concepts/terms/drive-impact.md`
  - `wiki/concepts/terms/drive-parry.md`
  - `wiki/concepts/terms/drive-reversal.md`
  - `wiki/concepts/terms/drive-rush-cancel.md`
  - `wiki/concepts/terms/overdrive.md`
  - `wiki/concepts/terms/perfect-parry.md`
  - `wiki/concepts/terms/raw-drive-rush.md`
  - `wiki/concepts/terms/stun.md`
  - `wiki/concepts/terms/super-art.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/gauges/validation.json` は `passed`。
  - API の revision wikitext と `action=raw` の wikitext が一致した。
  - MediaWiki revid は `365841`、source freshness は `2026-06-07T12:31:40Z`、raw 取得時刻は `2026-06-11T01:23:20Z`。
  - Rendered DOM は heading 18件、table 14件、image refs 64件を記録する。本文 table は 0-12、table 13 は SF6 Navigation。
  - Content media は 8 original files と 28 rendered image files。`numeric-tables.json` は content table 13件、Drive Impact range 30 rows、Drive Rush distance 30 rows を保持する。
- メモ:
  - Canonical raw は `page.raw.wikitext`。Drive / Super Gauge の数値が重要な source なので、source page と numeric JSON の両方に主要数値を保持した。
  - Drive Impact range と Drive Rush distance の 30 character table は省略せず source page と `numeric-tables.json` に残した。
  - SuperCombo Gauges は community numeric source として扱い、公式 Capcom source と重なる mechanics claim では公式 source を優先する。
- 未解決事項:
  - Drive regeneration、cooldown、Drive Impact range、Drive Rush distance values を公式 source または実機検証で照合するか。
  - `Drive Rush from Parry` の cost 表記を、cost table の `1/2` と section / caption text の `1 Drive Stock` の component 分解として扱うか、source-internal conflict として保持するか。
  - `wiki/outputs/data/gauges/supercombo/numeric-tables.json` の schema を、他の gauge / system numeric source にも使う標準 schema として固定するか。

## [2026-06-11] wiki-update | SuperCombo HUD Icons term pages
- 原本:
  - `raw/web-pages/wiki.supercombo.gg/hud/page.raw.wikitext`
  - `wiki/sources/supercombo-street-fighter-6-hud.md`
- 作成:
  - `wiki/concepts/terms/combo-counter.md`
  - `wiki/concepts/terms/counter-hit.md`
  - `wiki/concepts/terms/forced-knockdown.md`
  - `wiki/concepts/terms/hard-knockdown.md`
  - `wiki/concepts/terms/reversal.md`
  - `wiki/concepts/terms/throw-escape.md`
  - `wiki/concepts/terms/armor-break.md`
  - `wiki/concepts/terms/crush.md`
  - `wiki/concepts/terms/lock.md`
- 更新:
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/punish-counter.md`
  - `wiki/concepts/terms/cross-up.md`
  - `wiki/concepts/terms/stun.md`
  - `wiki/concepts/terms/air-reset.md`
  - `wiki/concepts/terms/drive-impact.md`
  - `wiki/concepts/terms/wall-bounce.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/sources/supercombo-street-fighter-6-hud.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - HUD Icons section の 12 項目を display cue として term 化した。新規9件を作成し、Punish Counter / Cross-up / Stun は既存 page に HUD source claim を追加した。
  - `Crush` と `Lock` は一般語として広げず、SuperCombo HUD の Drive Impact 関連 icon 名に scope を限定した。
  - HUD source は community visual evidence なので、Counter / Punish Counter の advantage / damage、Stun の system 条件、Drive Impact の mechanics では公式 source を優先する方針を維持した。
- 未解決事項:
  - Capcom 公式 HUD / game screen source または実機検証で、HUD icon 表示条件を公式・実測の根拠として補強するか。

## [2026-06-11] ingest | SuperCombo HUD web-page raw capture
- 原本:
  - `https://wiki.supercombo.gg/w/Street_Fighter_6/HUD`
  - `raw/web-pages/wiki.supercombo.gg/hud/manifest.json`
- 作成:
  - `raw/web-pages/wiki.supercombo.gg/hud/`
  - `wiki/sources/supercombo-street-fighter-6-hud.md`
  - `wiki/reviews/2026-06-11-supercombo-hud-web-page-capture-review.md`
- 更新:
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/hud/validation.json` は `passed`。
  - API の revision wikitext と `action=raw` の wikitext が一致した。
  - MediaWiki revid は `345794`、source freshness は `2026-01-03T12:40:35Z`、raw 取得時刻は `2026-06-11T01:00:31Z`。
  - MediaWiki API `prop=images` は 44件を返したが、HUD semantic content media 14件だけを `images/files/` と `images/rendered/` の対象にし、navigation / character icon 30件は除外 provenance として `metadata.json` に記録した。
- メモ:
  - Canonical raw は `page.raw.wikitext`。画像情報が重要な source なので、Battle HUD、HUD icon、Health Bar Reference の original media と rendered media、navigation 除去後の scoped screenshots を保存した。
  - Character navigation icon は HUD page 本文の根拠ではないため、raw media download から除外した。`api/query.json` は MediaWiki response の provenance として保持する。
  - HUD page は Battle HUD / HUD icon / Health Bar Reference の community visual source として扱い、Drive Gauge、Burnout、Super Art、Counter / Punish Counter など公式 source と重なる mechanics claim では公式 source を優先する。
- 未解決事項:
  - Capcom 公式 HUD / game screen source を追加 ingest して、SuperCombo HUD の community / visual claim と照合するか。
  - 将来の動画・画像質問向けに、scoped screenshots、original media、large video capture の保存基準をどこまで細分化するか。

## [2026-06-11] ingest | SuperCombo Controls web-page raw capture
- 原本:
  - `https://wiki.supercombo.gg/w/Street_Fighter_6/Controls`
  - `raw/web-pages/wiki.supercombo.gg/controls/manifest.json`
- 作成:
  - `raw/web-pages/wiki.supercombo.gg/controls/`
  - `wiki/sources/supercombo-street-fighter-6-controls.md`
  - `wiki/reviews/2026-06-11-supercombo-controls-web-page-capture-review.md`
- 更新:
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `raw/web-pages/wiki.supercombo.gg/controls/validation.json` は `passed`。
  - API の revision wikitext と `action=raw` の wikitext が一致した。
  - MediaWiki revid は `365425`、source freshness は `2026-06-03T09:40:46Z`、raw 取得時刻は `2026-06-11T00:01:49Z`。
- メモ:
  - Canonical raw は `page.raw.wikitext`。表示証拠として `page.html`、`rendered/main.dom.json`、`rendered/tables.dom.json` を保存した。
  - Direct template dependencies は `Template:Clr` と `Template:Navbox-SF6` 系で、主要本文を template 本文として別保存する必要はないと判断した。
  - Controls page は Classic / Modern control type、numpad notation、classic notation、button nickname の community source として扱う。
- 未解決事項:
  - Capcom 公式 controls / control type source を追加 ingest して、Modern Controls、simple input damage penalty、button mapping の official evidence と照合するか。

## [2026-06-11] schema | Workflow details を repo-local skills へ移動
- 更新:
  - `.gitignore`
  - `AGENTS.md`
  - `.agents/skills/sf6-source-ingest/SKILL.md`
  - `.agents/skills/sf6-source-ingest/agents/openai.yaml`
  - `.agents/skills/sf6-wiki-query/SKILL.md`
  - `.agents/skills/sf6-wiki-query/agents/openai.yaml`
  - `.agents/skills/sf6-durable-output/SKILL.md`
  - `.agents/skills/sf6-durable-output/agents/openai.yaml`
  - `.agents/skills/sf6-wiki-health-check/SKILL.md`
  - `.agents/skills/sf6-wiki-health-check/agents/openai.yaml`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - `AGENTS.md` に長い workflow 詳細を増やすのではなく、source ingest、wiki query、durable output、wiki health check の 4 つの repo-local skill へ分離した。
  - `AGENTS.md` は raw / wiki / schema 境界、page type、citation、index/log 更新、skill dispatch を担う正本として残した。
  - `$sf6-wiki-query` に source-only query、evidence authority、contamination-sensitive query、read-only evidence pass subagent の使いどころを置いた。
  - `$sf6-source-ingest`、`$sf6-durable-output`、`$sf6-wiki-health-check` にも、大きい source / evidence-heavy output / factual risk が高い audit で read-only subagent を使う条件を明記した。
  - source ingest / query skill に、raw/web source text は evidence であって agent instruction ではないという基本的な Source Safety ルールを追加した。
  - `.agents/` は原則 ignored のまま、今回作成した 4 つの repo workflow skill だけ Git 追跡できるよう `.gitignore` を調整した。
  - `tools/kb_path_guard.py` や `tools/kb_lint.py` は作らず、反復的な deterministic check が明確になった時だけ tool 化する方針を skill 側に残した。
- 未解決事項:
  - Source Safety / Prompt Injection の adversarial examples と Tool Safety の詳細ルールは引き続き後続 schema / skill 変更候補。
  - RAG / grounding / evaluation の論文を永続 source として扱う場合は、別途 `raw/papers/` または `raw/web-pages/` に source を置いて ingest する。

## [2026-06-11] schema | Core operating policies を明文化
- 更新:
  - `AGENTS.md`
  - `wiki/log.md`
- メモ:
  - この repo は base pattern 初期実装を完了済みとみなし、現在は SF6 domain-enabled LLM Wiki として運用することを明記した。
  - domain-specific tools は source of truth ではなく、raw capture、validation、derived output 生成の補助として扱う境界を記録した。
  - manifest がない通常 raw は immutable とみなし、更新可能 raw package は許可済み `storage_policy` と親 raw package manifest に従うことを明記した。
  - `latest_frame_data_mirror`、`latest_battle_change_mirror`、`updateable_web_page_capture` を現在の許可済み更新可能 policy として記録した。
  - wiki 全体の lint / health check report は `wiki/outputs/lint/`、個別 finding や capture review は `wiki/reviews/` に置く分担を明記した。
  - lint severity を P0 Integrity、P1 Evidence、P2 Structure、P3 Quality に分け、row count mismatch や validation failure は勝手に事実修正せず review note に回す方針を明記した。
  - 重要な主張、数値、日付、比較、評価、判断は近くに根拠を置き、`source fact` / `derived fact` / `synthesis` / `inference` / `hypothesis` を意識して書き分ける方針を明記した。
  - `wiki/index.md` は最初の navigation surface として新規 page / 主要更新時に更新し、`wiki/log.md` は append-only の activity log として entry 形式を揃える方針を明記した。
- 未解決事項:
  - Source Safety / Prompt Injection、Tool Safety の詳細ルールは後続 schema 変更で追加する。

## [2026-06-10] wiki-maintenance | Health check follow-up
- 更新:
  - `raw/frame-data/official/ryu/manifest.json`
  - `raw/frame-data/official/chunli/manifest.json`
  - `raw/frame-data/official/zangief/manifest.json`
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/entities/jp.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/chun-li.md`
  - `wiki/entities/zangief.md`
  - `wiki/questions/*.md` の関連 backlink 一部
  - `wiki/reviews/2026-05-26-official-jp-frame-data-capture-review.md`
  - `wiki/reviews/2026-05-27-official-ryu-frame-data-capture-review.md`
  - `wiki/reviews/2026-05-27-official-chun-li-frame-data-capture-review.md`
  - `wiki/reviews/2026-05-27-official-zangief-frame-data-capture-review.md`
  - `wiki/reviews/2026-05-30-official-frame-data-roster-capture-review.md`
  - `wiki/reviews/2026-05-31-supercombo-jp-frame-data-capture-review.md`
  - `wiki/reviews/2026-05-31-supercombo-ryu-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/outputs/lint/2026-06-10-health-check.md`
- 作成:
  - `wiki/concepts/terms/burnout.md`
  - `wiki/concepts/terms/drive-parry.md`
  - `wiki/concepts/terms/drive-reversal.md`
  - `wiki/concepts/terms/drive-impact.md`
  - `wiki/concepts/terms/drive-rush-cancel.md`
  - `wiki/concepts/terms/overdrive.md`
  - `wiki/concepts/terms/super-art.md`
  - `wiki/concepts/terms/critical-art.md`
  - `wiki/concepts/terms/damage-scaling.md`
  - `wiki/concepts/terms/wall-bounce.md`
  - `wiki/concepts/terms/air-reset.md`
  - `wiki/concepts/terms/chain.md`
  - `wiki/concepts/terms/cancel.md`
- メモ:
  - ユーザー確認済みに従い、Ryu / Chun-Li / Zangief の公式 raw manifest `raw_review_status` を既存 accepted review と同期した。
  - 個別 term pages は `wiki/index.md` に direct row を持たせ、詳細な claim 統合は [[concepts/terms/index]] に集約する運用にした。
  - 古い review pages の date-based raw path は履歴文書として保持し、現在の latest mirror entrypoint を注記した。
  - SuperCombo 補助列レビューは `field_conflict`、`manual_or_ambiguous_match`、query-demand character batch の順に進める方針を [[concepts/frame-data]] に記録した。
  - Question pages から term pages への backlink は、本文に自然に出る重要語は本文リンク、補助的な探索性は frontmatter `related:` に寄せる。
- 未解決事項:
  - `hitbox` / `hurtbox` は source confidence と imageinfo 欠損 policy を含むため、次の term page 化では追加 source 確認が必要。
  - SuperCombo-only 620 行を通常回答から分離すべき row と補助情報として使える row に分類する必要がある。

## [2026-06-10] lint | Wiki health check
- 作成:
  - `wiki/outputs/lint/2026-06-10-health-check.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 確認:
  - Markdown graph、frontmatter、direct index coverage、orphan-like pages、broken wikilinks。
  - `wiki/outputs/**/*.json` 363 files の JSON parse。
  - `raw/**/validation.json` 33 files の validation status。
  - 公式 frame-data 30 character source pages の row count と派生 JSON row count。
  - 公式 Battle Change List / update notice の quick web search による data-gap 確認。
- 所見:
  - Real page の broken wikilink と missing frontmatter は見つからなかった。
  - Ryu / Chun-Li / Zangief は wiki review/source 側で accepted とされるが、raw manifest の `raw_review_status` は `pending_human_review` のまま。review-needed として記録した。
  - 個別 term page 23 件は `concepts/terms/index` から到達可能だが、`wiki/index.md` direct entry はない。運用判断が必要。
  - Question pages 7 件と `2026-06-06-supercombo-field-conflict-queue-prereview` は index/log を除く inbound backlink が薄い。
- 未解決事項:
  - Ryu / Chun-Li / Zangief の manifest status を同期するか。
  - 古い review page に残る date-based raw path へ historical note を足すか。
  - Term page と question page の backlink 基準をどうするか。

## [2026-06-10] wiki-update | SF6 term pages for CAPCOM eSports BASE terms
- 作成:
  - `wiki/concepts/terms/index.md`
  - `wiki/concepts/terms/chip-damage.md`
  - `wiki/concepts/terms/stun.md`
  - `wiki/concepts/terms/anti-air.md`
  - `wiki/concepts/terms/corner.md`
  - `wiki/concepts/terms/cross-up.md`
  - `wiki/concepts/terms/command-throw.md`
  - `wiki/concepts/terms/raw-drive-rush.md`
  - `wiki/concepts/terms/drive-impact-counter.md`
  - `wiki/concepts/terms/perfect-parry.md`
  - `wiki/concepts/terms/oki.md`
  - `wiki/concepts/terms/punish-counter.md`
  - `wiki/concepts/terms/whiff-punish.md`
  - `wiki/concepts/terms/invincible-move.md`
  - `wiki/concepts/terms/frame-advantage.md`
  - `wiki/concepts/terms/meaty.md`
  - `wiki/concepts/terms/lethal.md`
  - `wiki/concepts/terms/shikomi.md`
  - `wiki/concepts/terms/guaranteed-punish.md`
  - `wiki/concepts/terms/hit-confirm.md`
  - `wiki/concepts/terms/shimmy.md`
  - `wiki/concepts/terms/setplay.md`
  - `wiki/concepts/terms/abare.md`
  - `wiki/concepts/terms/scaling-reset.md`
- 更新:
  - `wiki/sources/capcom-esports-base-terms.md`
  - `wiki/reviews/2026-06-10-capcom-esports-base-terms-capture-review.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Capcom eSports BASE 由来の 23 語を `wiki/concepts/terms/` 配下の個別 term page に昇格した。
  - `wiki/concepts/terms/index.md` を用語カタログとし、今後の公式 / community source claims を用語ごとに集約する方針を明記した。
  - 英語で意味が安定している用語は `punish-counter` などの English slug、英語に置き換えると意味がずれやすい用語は `shikomi` / `abare` のような romaji slug を使った。
  - `sources/capcom-esports-base-terms.md` の用語一覧を term page への入口に更新した。
- 未解決事項:
  - SuperCombo glossary などを term pages に追加統合する時、source page と term page の claim 粒度をどう分けるか。
  - 個別 frame-data row や question page から term pages へ backlink を張る基準をどうするか。

## [2026-06-10] ingest | CAPCOM eSports BASE terms scoped raw capture
- 原本:
  - `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json`
  - `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json`
- 作成:
  - `wiki/sources/capcom-esports-base-terms.md`
  - `wiki/reviews/2026-06-10-capcom-esports-base-terms-capture-review.md`
- 更新:
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Capcom 公式 `CAPCOM eSports BASE` の `実況ワード解説` セクションだけを scoped raw として wiki に ingest した。raw 本体は既存取得物を読み、今回の wiki ingest では変更していない。
  - Source は CPT / SFL 観戦向けの Street Fighter 6 用語 23 語を、重要度 3 段階で説明する。重要度 3 は削り、スタン、対空、画面端、めくり、コマ投げ、生ラッシュ、インパクト返し、ジャストパリィ。
  - Canonical raw は `source/word-section.raw.html`、`source/modal-open-close.raw.js`、`api/terms.raw.json`、`rendered/word-section.dom.json`、`rendered/modals/`。表示証拠として `screenshots/word-section.png` と `screenshots/modal-word-00.png` がある。
  - Full page HTML、full page JavaScript、movie list assets、consult / coaching assets、logos、page chrome、unrelated images は保存対象から外れている。
  - Page HTML / page JS の HTTP `Last-Modified` は `2025-11-11T06:17:24Z`、raw 取得時刻は `2026-06-09T17:48:14Z`。
- 検証:
  - `validation.json` は `passed`。23 terms、3 groups、47 downloaded assets、23 modal DOM、2 screenshots を確認している。
- 未解決事項:
  - HTTP `Last-Modified` を source freshness として表示し続けるか、artifact metadata としてのみ扱うか。
  - 23 語を個別 concept page に昇格する基準をどうするか。
  - SuperCombo glossary の community terms と対応表を作るか。

## [2026-06-10] ingest | Capcom Fighting Ground Battle System scoped raw capture
- 原本:
  - `https://www.streetfighter.com/6/ja-jp/mode/fightingground`
- 作成:
  - `raw/web-pages/www.streetfighter.com/fightingground-battle-system/`
  - `tools/web_pages/__init__.py`
  - `tools/web_pages/capcom_fightingground_battle_system.py`
  - `wiki/sources/capcom-official-fightingground-battle-system.md`
  - `wiki/reviews/2026-06-10-capcom-fightingground-battle-system-capture-review.md`
- 更新:
  - `wiki/concepts/drive-system.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/capcom.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Fighting Ground ページ全体ではなく、Battle System に関係する `BATTLE SYSTEM DESIGN`、`DRIVE GAUGE`、`COMMON SYSTEM`、`simpleOperationImage` modal だけを scoped raw として保存した。
  - `SOUND ACCESSIBILITY`、`CHARACTER DAMAGE`、`Real Time Commentary`、`CONTROL TYPE`、`BATTLE CONTENTS` は保存対象から外した。
  - full page HTML、full Next.js data JSON、page chunk JS は保存せず、`source-provenance.json` に response metadata と hash だけを残した。
  - Canonical raw は `api/source-text.scoped.json` と `rendered/*.dom.json`。表示証拠として `screenshots/*.png`、必要な画像 asset と `assets/manifest.json` を保存した。
  - Next.js build ID は `8PI3Oj_9ikUinAmp3j_yf`。source の公開更新日時は未取得なので、`captured_at_utc` と build ID を由来情報として扱う。
- 検証:
  - `python -m tools.web_pages.capcom_fightingground_battle_system --repo-root .`
  - `validation.json` は `passed`。期待 text key 34 件、4 件の scoped DOM、4 枚の screenshot、14 件の asset download を確認した。
  - modal screenshot を目視確認し、ゲーム画面画像と 6 件の UI 説明が表示されていることを確認した。
- 未解決事項:
  - Web page capture で scoped raw を作る場合、除外 section 名を manifest policy に残すだけで十分か。
  - `COMMON SYSTEM` の command icon refs を binary asset として保存しない運用でよいか。

## [2026-06-10] raw/schema | SuperCombo glossary Web page raw と更新可能 raw 方針
- 原本:
  - `https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary`
- 作成・削除:
  - `raw/web-pages/wiki.supercombo.gg/glossary/`
  - `wiki/reviews/2026-06-09-supercombo-glossary-web-page-capture-review.md`
  - 削除: `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md`
- 更新:
  - `.gitattributes`
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `ROADMAP.md`
  - `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json`
  - `raw/web-pages/wiki.supercombo.gg/glossary/validation.json`
  - `wiki/index.md`
  - `wiki/sources/supercombo-street-fighter-6-glossary.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo glossary は MediaWiki source なので、`page.raw.wikitext` を canonical raw 取得物とし、`page.html` と `rendered/*.dom.json` を表示構造の証拠として保存した。
  - MediaWiki revid `351898`、revision timestamp `2026-01-31T11:22:26Z`、`captured_at_utc` `2026-06-09T13:47:52Z` を manifest に記録した。
  - Notation Glossary の `{{ComboLegend-SF6}}` 依存を追加で保存した。template 一覧は `api/templates.json`、`ComboLegend-SF6` 本文は `templates/combo-legend-sf6.raw.wikitext`、revision は revid `283225` / timestamp `2023-12-11T18:45:25Z`。
  - `raw/` は通常は不変とし、manifest の `storage_policy` で最新ミラーまたは更新可能な取得一式と示されている raw 一式は更新可能とする方針に整理した。
  - README / ROADMAP の古い「raw を絶対に編集しない」文言を、通常 raw と更新可能 raw 一式を分ける説明に直した。
  - 古い Obsidian Web Clipper raw は削除し、新 raw から wiki を再点検した。Drive System、Frame Data、Juggles の意味内容は変わらず、Notation Glossary は `{{ComboLegend-SF6}}` 展開後の table を `rendered/tables.dom.json` へ辿る形に直した。
- 検証:
  - `validation.json` は `passed`。API の revision wikitext と `action=raw` の wikitext は一致した。
  - template 依存の validation は存在確認と API/raw wikitext 一致だけに留め、template 内容の意味検証や再帰的な展開は追加しなかった。
  - `raw/frame-data/` は `latest_frame_data_mirror`、`raw/battle-change/official/` は `latest_battle_change_mirror`、`raw/web-pages/` は `updateable_web_page_capture` として扱うことを確認した。
- 未解決事項:
  - Web page capture で screenshot を常時保存するか、必要時だけにするか。
  - 最新ミラーの再取得時に旧ミラーをどこまで外部保管物として保持するか。

## [2026-06-09] wiki-update | frame-data source freshness metadata
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `raw/frame-data/supercombo/<character_slug>/manifest.json`
- 更新:
  - `wiki/index.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- メモ:
  - SuperCombo frame-data の source freshness は `source_updated_at` を優先し、`captured_at_utc` は raw 取得時刻として分離する方針を明記した。
  - 30キャラ batch は単一の代表日ではなく、`source_updated_at` の範囲 2026-05-30T01:24:06Z から 2026-06-02T03:14:40Z として扱う。
  - 現在の SuperCombo frame-data manifests には `source_published_at` がないため、初版日や公開日は推測しない。
- 未解決事項:
  - Capcom official source の source freshness と取得時刻を wiki 上でどこまで分けて表現するか。

## [2026-06-08] query | JP しゃがみ中P＞キャンセルDR＞しゃがみ強P＞強ストリボーグ＞中トルバラン＞トリグラフの成立理論
- 質問:
  - `JPのコンボで、しゃがみ中P＞キャンセルラッシュ＞しゃがみ大P＞強ストリボーグ＞中トルバラン＞トリグラフ　が繋がる理論を具体的に解説してほしい。`
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/sources/capcom-official-battle-change-list.md`
  - `wiki/outputs/data/frame-data/official/jp/classic.json`
  - `wiki/outputs/data/frame-data/supercombo/jp/frames.json`
  - `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
  - `wiki/outputs/data/battle-change/official/changes.json`
- 作成:
  - `wiki/questions/jp-crouching-medium-p-drc-crouching-heavy-p-heavy-stribog-medium-torbalan-triglav-combo-theory.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - `しゃがみ中P`→`DRしゃがみ強P` は素リンクではなく、`C` からのキャンセルDRとDRC最速攻撃可能9Fで説明した。
  - `DRしゃがみ強P`→`強 ストリボーグ` は、DR通常技の `+4F` と `C` 必殺技キャンセルで成立する形として説明した。
  - `強 ストリボーグ` 以降は地上リンクではなく、limited juggle / wall bounce、`中 トルバラン` の空中拾い、`トリグラフ` の `juggle limit 26` で説明した。
- 未解決事項:
  - 中央 / 端、最後の `トリグラフ` 強度、先端距離ごとの実戦安定性は未検証。

## [2026-06-08] query | JP しゃがみ弱P＞立ち弱P＞弱ストリボーグの成立理論
- 質問:
  - `JPのコンボで、しゃがみ小P＞立ち小P＞弱ストリボーグが繋がる理論を具体的に解説してほしい。`
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/outputs/data/frame-data/official/jp/classic.json`
  - `wiki/outputs/data/frame-data/supercombo/jp/frames.json`
  - `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
- 作成:
  - `wiki/questions/jp-crouching-light-p-standing-light-p-light-stribog-combo-theory.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - `しゃがみ弱P`→`立ち弱P` は `+4F` から発生6Fをリンクしているのではなく、連打キャンセル / chain として説明した。
  - `立ち弱P`→`弱 ストリボーグ` は `C` の必殺技キャンセルであり、出し切り後のリンクではないと明記した。
- 未解決事項:
  - このルートの距離別安定性、先端ヒット時の可否、Modern入力での実戦差は未検証。

## [2026-06-08] review-fix | query-facing JSON-only references
- 変更:
  - `wiki/questions/` と `wiki/entities/` に残っていた削除済み CSV output path、`*.field-meanings.json`、旧 field 名 `input_token_json` の現在形参照を JSON-only contract に更新した。
  - 公式 frame-data 参照は `classic.json` / `modern.json` と `rows[]` / `field_meanings.records[]` を読む形に統一した。
  - enriched output を説明する entity page では `classic-supercombo.json` / `supercombo-only.json` を明示した。
  - `tests/test_output_data_json_only.py` に query-facing wiki pages の旧 output contract と missing `wiki/outputs/data/...` path を検出する回帰テストを追加した。
- 更新:
  - `wiki/entities/`
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
  - `wiki/questions/chun-li-standing-medium-p-into-crouching-medium-p-link.md`
  - `wiki/index.md`
  - `tests/test_output_data_json_only.py`
- メモ:
  - `wiki/log.md` と `raw/` 内の historical path は履歴・原本として扱い、query-facing contract の検査対象から外す。

## [2026-06-08] schema | wiki output data JSON-only migration
- 変更:
  - `wiki/outputs/data` 配下の canonical output を JSON-only に統一した。
  - 公式 frame-data は `<control-scheme>.json` に `rows`、`fields`、source metadata、`field_meanings.records` をまとめ、旧 CSV と `*.field-meanings.json` を削除した。
  - SuperCombo 派生 output は `frames.json`、`character.json`、`crosswalk-official-classic.json`、`supercombo-unmatched.json` を canonical JSON payload とした。
  - 公式 + SuperCombo enriched output は `classic-supercombo.json` と `supercombo-only.json` のみを canonical output とした。
  - Battle Change output は `versions.json` と `changes.json` を `fields` + `rows` payload に統一した。
- 更新:
  - `tools/frame_data/official/`
  - `tools/frame_data/supercombo/extract.py`
  - `tools/frame_data/enriched/`
  - `tools/battle_change/official/extract.py`
  - `tests/`
  - `README.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - current output/source/report/review references.
- メモ:
  - `raw/` は source-native のまま不変とし、CSV 廃止は wiki output layer に限定した。
  - 互換 CSV 出力や CSV reader fallback は残していない。必要な一時 export は canonical output とは別の one-off 作業として扱う。
  - LLM エージェントは `jq` で `rows[]`、`field_meanings.records[]`、`summary`、`schema.json` を直接参照する。
- 未解決事項:
  - 既存 raw manifest 内の historical `derived_outputs` path は `raw/` 不変ルールにより書き換えない。将来の raw manifest schema で historical field として明示するかは別途判断する。

## [2026-06-07] schema | tool layout migration
- 変更:
  - `tools/` の flat scripts を data family first の package layout に移動した。
  - frame-data tools は `tools/frame_data/official/`、`tools/frame_data/supercombo/`、`tools/frame_data/enriched/` に分けた。
  - Battle Change tools は `tools/battle_change/official/` に分けた。
  - tooling tests は CLI tools から分離し、`tests/frame_data/` と `tests/battle_change/` に移動した。
- メモ:
  - 個人用 repo のため旧 `tools/*.py` wrapper は残さず、実行入口は `python -m tools...` に切り替えた。
  - `raw/` は不変なので、既存 raw manifest 内の過去 tool path は書き換えない。
- 未解決事項:
  - 今後の新規 source family で、source 固有 helper を `tools/<data_family>/<source>/` と `tools/<data_family>/<variant>/` のどちらに置くかは個別に判断する。

## [2026-06-07] schema | output data layout migration
- 変更:
  - `wiki/outputs/data/frame-data/<character>/` を `wiki/outputs/data/frame-data/official/<character>/` に移動。
  - `wiki/outputs/data/supercombo/frame-data/<character>/` を `wiki/outputs/data/frame-data/supercombo/<character>/` に移動。
  - `wiki/outputs/data/enriched/frame-data/<character>/` を `wiki/outputs/data/frame-data/official-supercombo-enriched/<character>/` に移動。
- 更新:
  - `tools/capture_capcom_frame_data.py`
  - `tools/extract_capcom_frame_data.py`
  - `tools/validate_capcom_frame_data.py`
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `tools/audit_supercombo_enriched_review_status.py`
  - `tools/test_supercombo_enrichment_review.py`
  - `README.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - reader-facing wiki path references and generated output metadata.
- メモ:
  - `battle-change/official/` と同じく、第一階層を data family に揃える方針にした。
  - enriched audit は missing root または 0 rows scan を失敗として扱うようにし、移設後の空パス成功を防ぐ。
  - `raw/` 不変ルールにより、既存 raw manifest 内の旧 `derived_outputs` path は書き換えない。現在の output contract は README、tools、index、この synthesis を入口に確認する。
- 未解決事項:
  - 既存 raw manifest の `derived_outputs` を将来の manifest schema で historical field として明示するか。

## [2026-06-07] ingest | Capcom official Battle Change List
- 原本:
  - `raw/battle-change/official/manifest.json`
  - `raw/battle-change/official/discovery/`
  - `raw/battle-change/official/versions/<version>/`
- 派生 output:
  - `wiki/outputs/data/battle-change/official/versions.csv`
  - `wiki/outputs/data/battle-change/official/changes.csv`
  - `wiki/outputs/data/battle-change/official/changes.json`
  - `wiki/outputs/data/battle-change/official/schema.json`
- ツール:
  - Added `tools/capture_capcom_battle_change.py`.
  - Added `tools/validate_capcom_battle_change.py`.
  - Added `tools/extract_capcom_battle_change.py`.
  - Added focused tests for capture helpers, raw validation, and extraction flattening.
- 作成:
  - `wiki/sources/capcom-official-battle-change-list.md`
  - `wiki/reviews/2026-06-07-official-battle-change-capture-review.md`
- 更新:
  - `README.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `python tools/test_battle_change_capture.py`
  - `python tools/test_battle_change_validation.py`
  - `python tools/test_battle_change_extraction.py`
  - `python tools/capture_capcom_battle_change.py --dry-run`
  - `python tools/capture_capcom_battle_change.py --delay-seconds 0.25`
  - `python tools/validate_capcom_battle_change.py`
  - `python tools/extract_capcom_battle_change.py`
- メモ:
  - Discovery page の `adjust.versions` から 20 update version を列挙した。
  - `_next/data/<buildId>/ja-jp/battle_change/<version>.json` を version ごとの構造化 raw response として保存した。
  - 自動 validation は HTML 内 `__NEXT_DATA__` と `_next/data` JSON の `adjust` 一致、artifact hash、version ID 一致を確認した。
  - 派生 output は 20 version / 1820 change rows。内訳は policy 123、common 100、fighter 1597。
  - `version_title` と `version_selector_title` を別列化し、公式 source 内の表記差は `version_title_mismatch` で示す。`20231201` は page title `2023.12.1 update` と selector title `2023.12.01 update` が異なる。
- 未解決事項:
  - 20 version 分の本文を、version 別 source page、character 別 synthesis、時系列 synthesis のどれへ昇格するか。
  - `text_html` の HTML fragment を読者向け plain text / Markdown に派生する方針を決める。
  - 人間レビュー後に raw review status を accepted に更新するか。

## [2026-06-06] 修正 | frame-data capture validation guard
- 作成:
  - `tools/frame_data_integrity.py`
  - `tools/test_capcom_capture_guards.py`
  - `tools/test_supercombo_validation_integrity.py`
- 更新:
  - `tools/capture_capcom_frame_data.py`
  - `tools/validate_capcom_frame_data.py`
  - `tools/capture_supercombo_frame_data.py`
  - `tools/validate_supercombo_frame_data.py`
  - `tools/extract_supercombo_frame_data.py`
  - `raw/frame-data/supercombo/<character_slug>/validation.json`
  - `README.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo capture は古い `validation.json` を削除し、validation は現在 raw metadata と実ファイル artifact hash の `raw_fingerprint` を保存する。
  - SuperCombo extract は `status: passed` だけでなく `raw_fingerprint` 一致を要求するため、再取得後の古い validation で派生 output を生成しない。
  - Capcom official capture / validate は Classic / Modern tab identity と未知 row shape を fail-closed にした。
  - 30 キャラ分の SuperCombo validation を fingerprint 付き形式へ更新した。
- 検証:
  - `python tools\test_capcom_capture_guards.py`
  - `python tools\test_supercombo_validation_integrity.py`
  - `python tools\extract_supercombo_frame_data.py --repo-root . --character-slug jp`
  - `python tools\test_supercombo_frame_comparison.py`
  - `python tools\test_supercombo_enrichment_review.py`
  - `python tools\audit_supercombo_enriched_review_status.py --repo-root .`
  - `python tools\validate_capcom_frame_data.py --repo-root . --character-slug <all official slugs>`
- 未解決事項:
  - Capcom official manifest の `raw_review_status` と wiki review page の accepted / pending 状態を同期する運用ルールは別途決める。

## [2026-06-06] レビュー | SuperCombo field_conflict 単独キュー事前レビュー
- 作成:
  - `wiki/reviews/2026-06-06-supercombo-field-conflict-queue-prereview.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - `enrichment_review_queues == field_conflict` 単独の 11 行を抽出した。
  - 追加で自動 accept できる行は見つからなかった。
  - Jamie の 4 行は酔いLv damage scaling 由来の条件付き値として分離候補。
  - Terry の jump MP / jump MK 2 行は active と damage が相互に入れ替わっている疑いがあり、source 確認が必要。
  - Zangief Tundra Storm は既存レビュー済みなので、今回の未レビュー削減対象からは外す。
- 未解決事項:
  - Jamie の酔いLv damage scaling を `condition_dependent_field` 相当へ分類し直すか。
  - Terry jMP / jMK の source conflict をどう扱うか。

## [2026-06-06] 修正 | 多段 damage 正規化とレビューキュー分離
- 作成:
  - `tools/test_supercombo_enrichment_review.py`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `tools/test_supercombo_frame_comparison.py`
  - `wiki/outputs/data/supercombo/frame-data/`
  - `wiki/outputs/data/enriched/frame-data/`
  - `wiki/outputs/reports/2026-06-05-supercombo-all-frame-data-coverage.md`
  - `wiki/reviews/2026-06-05-supercombo-all-frame-data-capture-review.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
- メモ:
  - `$adversarial-review` の事前レビュー結果を踏まえ、`400x2` や `300,400` のような括弧・注記なしの多段 damage 合計だけを機械比較対象にした。
  - 多段 damage 合計は `multihit_damage_sum` として field 比較に使うが、候補選択 score には使わない。これにより SuperCombo-only 行の増減は発生していない。
  - `enrichment_review_queues` を追加し、`uncomparable_notation`、`structural_ambiguity`、`condition_dependent_field`、`field_conflict`、`manual_or_ambiguous_match` に review flags を束ねた。
  - 30 キャラ再生成後、`enriched` 592、`enriched_reviewed` 69、`enriched_review_required` 1295、`official_only` 405、SuperCombo-only 620 になった。
  - review queue 件数は `uncomparable_notation` 1138、`structural_ambiguity` 851、`condition_dependent_field` 554、`field_conflict` 199、`manual_or_ambiguous_match` 161。
- 検証:
  - `python tools\test_supercombo_frame_comparison.py`
  - `python tools\test_supercombo_enrichment_review.py`
  - `python tools\audit_supercombo_enriched_review_status.py --repo-root .`
- 未解決事項:
  - 次の review pass を queue 単位で進めるか、character 単位で進めるか。
  - SuperCombo-only 620 行を taunt、条件付き variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。

## [2026-06-06] 修正 | 条件付き SuperCombo field の fail-closed 化と landing recovery 正規化
- 作成:
  - `tools/test_supercombo_frame_comparison.py`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `tools/audit_supercombo_enriched_review_status.py`
  - `wiki/outputs/data/supercombo/frame-data/`
  - `wiki/outputs/data/enriched/frame-data/`
  - `wiki/outputs/reports/2026-06-05-supercombo-all-frame-data-coverage.md`
  - `wiki/reviews/2026-06-05-supercombo-all-frame-data-capture-review.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
- メモ:
  - `$adversarial-review` の `adversarial_reviewer` が、`800(700)` や `2800 (3220)` のような括弧付き damage が primary 値だけで `enriched` に通る no-ship finding を出した。
  - `damage` / `startup` / `recovery` の括弧付き SuperCombo 値は `condition_dependent_supercombo_field:<field>` として扱い、人間レビューなしでは `enriched` にしない。
  - `audit_supercombo_enriched_review_status.py` は条件付き括弧値が `enriched` に残る場合も失敗する。修正前は 102 件を検出した。
  - `着地後N` と `N land`、および `A+着地後B` と `A+B land` は landing recovery の表記差として機械正規化する。
  - 30 キャラ再生成後、`enriched` 591、`enriched_reviewed` 69、`enriched_review_required` 1296、`official_only` 405、SuperCombo-only 620 になった。
- 検証:
  - `python tools\test_supercombo_frame_comparison.py`
  - `python tools\audit_supercombo_enriched_review_status.py --repo-root .`
- 未解決事項:
  - `enriched_review_required` 1296 行のうち、条件付き field、構造的 ambiguity、基本 field conflict を別々の review queue としてどう処理するか。
  - 多段 damage (`400x2` など) は notes / source evidence を確認してから、別段階で安全な正規化候補にするか判断する。
  - SuperCombo-only 620 行を taunt、conditional variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。

## [2026-06-06] 修正 | SuperCombo enriched status の fail-closed 化
- 作成:
  - `tools/audit_supercombo_enriched_review_status.py`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/supercombo/frame-data/`
  - `wiki/outputs/data/enriched/frame-data/`
  - `wiki/outputs/reports/2026-06-05-supercombo-all-frame-data-coverage.md`
  - `wiki/reviews/2026-06-05-supercombo-all-frame-data-capture-review.md`
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
- メモ:
  - adversarial review で、複数候補・SuperCombo row 再利用・比較不能な基本 field を持つ補助リンクが `enriched` のまま公開される no-ship finding が出た。
  - 先に `tools/audit_supercombo_enriched_review_status.py` を追加し、現状で 663 件の risky `enriched` を検出することを確認した。
  - `damage` の `2500 (2875)` のような parenthetical value は primary damage として比較し、Alex の `パワードロップ` は `basic_field_conflict:damage` を持つ `enriched_review_required` になった。
  - 複数候補、SuperCombo row 再利用、manual/ambiguous match、基本 field conflict、比較不能 field は、人間レビュー済み decision がない限り `enriched_review_required` に落とす fail-closed policy にした。
  - 既存の `human_review_status: accepted` 69 行は `enriched_reviewed` として保持した。
  - 30 キャラ再生成後、`enriched` 524、`enriched_reviewed` 69、`enriched_review_required` 1363、`official_only` 405 になった。
- 未解決事項:
  - `enriched_review_required` 1363 行をどの順序で人間レビューするか。
  - SuperCombo-only 621 行を taunt、conditional variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。
  - 比較不能 field のうち、将来安全に自動比較できる notation を増やすか。

## [2026-06-05] 取り込み | SuperCombo 全キャラフレームデータ batch capture
- 作成:
  - `wiki/sources/supercombo-street-fighter-6-frame-data-batch.md`
  - `wiki/reviews/2026-06-05-supercombo-all-frame-data-capture-review.md`
  - `wiki/outputs/reports/2026-06-05-supercombo-all-frame-data-coverage.md`
  - `raw/frame-data/supercombo/<character_slug>/` の新規 26 キャラ分
  - `wiki/outputs/data/supercombo/frame-data/<character_slug>/` の新規 26 キャラ分
  - `wiki/outputs/data/enriched/frame-data/<character_slug>/` の新規 26 キャラ分
- 更新:
  - `tools/capture_supercombo_frame_data.py`
  - `tools/extract_supercombo_frame_data.py`
  - `tools/validate_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/outputs/data/supercombo/frame-data/`
  - `wiki/outputs/data/enriched/frame-data/`
- メモ:
  - SuperCombo Wiki の Street Fighter 6 frame-data は 30 キャラ分の raw capture と派生 output がそろった。
  - raw validation は 30/30 で `passed`。SuperCombo raw/Cargo の frame rows は合計 2306 行、公式 Classic rows は合計 2361 行。
  - 新規 26 キャラは `--no-download-images` で取得した。画像ファイル本体は保存していないが、image refs、`imageinfo.json`、`image-manifest.json`、DOM は保存している。
  - 公式 Classic との crosswalk と、公式列を正として SuperCombo を `supercombo_*` 補助列に入れる enriched output を 30 キャラ分生成した。
  - JP / Ryu / Zangief / Ingrid の既存人間レビュー済み行は保持し、新規 26 キャラの補助行は勝手に accept していない。
  - Chun-Li の `serenity_stream`、Dee Jay の Cargo key `Dee_Jay`、C.Viper の `cancel=*SA3` 表示正規化、Jamie Specials table の pagination を source に従って extractor / validator に反映した。
  - C.Viper の `moveType=air_normal8` は SuperCombo 表示 query に出ない非標準 row として保持し、推測で `air_normal` 扱いにはしていない。
- 未解決事項:
  - `enriched_review_required` 233 行をどの順序で人間レビューするか。
  - SuperCombo-only 621 行を taunt、conditional variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。
  - imageinfo missing 599 件を source 側の欠損として扱うか、filename 正規化で再解決を試すか。
  - 新規 26 キャラの個別 character entity page へ、batch coverage 以上の詳細をどこまで反映するか。

## [2026-06-02] 事前レビュー | SuperCombo Ingrid SuperCombo-only 9 行
- 作成:
  - `wiki/reviews/2026-06-02-supercombo-ingrid-supercombo-only-prereview.md`
- 更新:
  - `wiki/reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo Ingrid の公式 row に直接照合しない 9 行（Big Laser?、Burnout Attack?、Sun Octopus?、Monoid 関連）について、ネット検索と外部 page 確認を使って事前レビューした。
  - Capcom News / Steam official announcements / 公式 frame-data では通常掲載範囲に hidden 9 行を確認できず、公式 row への統合根拠にはしない。
  - Twisted Voxel、Reddit、Street Fighter Wiki の Dark Ingrid / Monoid pages は、Shin/Dark Ingrid 変身、Monoid 経由、`22PPP`、`214214K`、`360/412369+KK` の存在条件を補強する secondary / community evidence として扱う。
  - 今回は accept ではない。`human_review_status`、`human_review_decision`、公式 row への照合、補助列付き output は変更していない。
  - repo の現段階では domain-specific な answer policy field や新 schema は作らず、既存の `supercombo-only.csv` / `suggested_handling` と review note の tags / 説明で「通常回答には混ぜない」ことを表す。
- 未解決事項:
  - hidden / Dark / Shin Ingrid と Monoid 操作 row を reader-facing data として公開する場合、通常の Ingrid frame-data とどう分けて表示するか。
  - 既存の `suggested_handling` の `supercombo_only` を、将来 `supercombo_only_hidden_command` や `supercombo_only_taunt_summon` のように細分化する必要があるか。
  - accept 前に Capcom 公式動画、公式 command list、in-game training/frame meter で追加検証するか。

## [2026-06-02] レビュー | SuperCombo Ingrid 補助データのレビュー対象行
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/supercombo/frame-data/ingrid/`
  - `wiki/outputs/data/enriched/frame-data/ingrid/`
  - `wiki/outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk.md`
  - `wiki/outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data.md`
  - `wiki/sources/supercombo-ingrid-frame-data.md`
  - `wiki/reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review.md`
  - `wiki/entities/ingrid.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Ingrid の SuperCombo raw から派生 frame-data CSV/JSON を生成し、Capcom 公式 Ingrid Classic CSV との crosswalk を作成した。
  - crosswalk は公式 75 rows / SuperCombo 83 rows、自動一致 47、name override 一致 26、公式側未照合 2。
  - 補助列付き output は `enriched` 47、`enriched_reviewed` 26、`official_only` 2。`enriched_review_required` は 0。
  - レビュー対象 26 行は `human_review_status: accepted`。decision は `supplemental_link` 4、`shared_variant_supplemental_link` 2、`stock_build_supplemental_link` 2、`stock_level_supplemental_link` 18。
  - Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush を公式値を正とする補助リンクとして扱う。
  - 公式列と補助列付き output の公式由来列が一致することを検証した。
- 未解決事項:
  - `imageinfo` missing 156 件が source 側の欠損なのか、filename 正規化や API title 変換で再解決可能なのか。
  - 公式 row に直接照合しない SuperCombo-only 9 行（Big Laser?、Burnout Attack?、Sun Octopus?、Monoid 関連）を、特殊隠しコマンド / Monoid 操作に関係する通常利用外 row として通常回答から分離する方針を事前レビューした。

## [2026-06-02] 取り込み | SuperCombo Ingrid フレームデータ wiki ingest
- 原本:
  - `raw/frame-data/supercombo/ingrid/manifest.json`
  - `raw/frame-data/supercombo/ingrid/validation.json`
  - `raw/frame-data/supercombo/ingrid/data.raw.wikitext`
  - `raw/frame-data/supercombo/ingrid/frame-data.raw.wikitext`
  - `raw/frame-data/supercombo/ingrid/cargo/`
  - `raw/frame-data/supercombo/ingrid/rendered/`
  - `raw/frame-data/supercombo/ingrid/screenshots/`
  - `raw/frame-data/supercombo/ingrid/image-manifest.json`
- 作成:
  - `wiki/sources/supercombo-ingrid-frame-data.md`
  - `wiki/reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review.md`
- 更新:
  - `wiki/index.md`
  - `wiki/entities/ingrid.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo Ingrid raw 取得データを source summary と capture review note として wiki layer に取り込んだ。
  - `validation.json` の status は `passed`。83 件の frame template、1 件の character template、21 件の表示 Cargo query、20 件の DOM table comparison が通過している。
  - source revision label は `2026-06-02`。Data page revision は `2026-06-02T01:44:56Z`、Frame data page revision は `2026-04-22T23:42:21Z`。
  - 画像参照は 164 refs、`imageinfo` の distinct title は 158 件。解決できた title は face / portrait の 2 件のみで、156 title は missing。取得済み画像も 2 件。
  - 今回は wiki ingest が範囲なので、派生 frame-data CSV/JSON、公式 Classic との crosswalk、補助列付き output は作成していない。
- 未解決事項:
  - Ingrid の move / hitbox image refs の大半が SuperCombo API の `imageinfo` で missing になる理由を確認する。
  - Sun Crest、Monoid、Shin Ingrid 関連 rows を公式 Classic data とどの schema で照合するか。
  - 次 step で派生 frame-data output と公式 Classic との crosswalk を作るか。

## [2026-06-02] 取り込み | SuperCombo Ingrid フレームデータ raw 取得
- 原本:
  - `raw/frame-data/supercombo/ingrid/manifest.json`
  - `raw/frame-data/supercombo/ingrid/data.raw.wikitext`
  - `raw/frame-data/supercombo/ingrid/frame-data.raw.wikitext`
  - `raw/frame-data/supercombo/ingrid/cargo/`
  - `raw/frame-data/supercombo/ingrid/rendered/`
  - `raw/frame-data/supercombo/ingrid/screenshots/`
  - `raw/frame-data/supercombo/ingrid/images/files/`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo Ingrid を `https://wiki.supercombo.gg/w/Street_Fighter_6/Ingrid/Frame_data` と関連 Data page から取得した。
  - source revision label は `2026-06-02`。Data page revision は `2026-06-02T01:44:56Z`、Frame data page revision は `2026-04-22T23:42:21Z`。
  - 今回は raw 取得までに範囲を限定し、派生 data output、source summary、review note は作成していない。
  - 検証は 83 件の frame template、1 件の character template、21 件の表示 Cargo query、20 件の DOM table comparison で通過した。
  - 画像参照は 164 refs、`imageinfo` の distinct title は 158 件。2 title だけ解決され、156 title は missing だった。取得できた画像は face と portrait の 2 件。
- 未解決事項:
  - Ingrid の move / hitbox image refs の大半が SuperCombo API の `imageinfo` で missing になる理由を、次の source summary / review 作成時に確認する。
  - 次 step で派生 frame-data output と公式 Classic との crosswalk を作るか。

## [2026-06-02] レビュー | Zangief SuperCombo 補助データのレビュー対象行
- 更新:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/zangief/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/zangief/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/zangief/summary.json`
  - `wiki/outputs/data/enriched/frame-data/zangief/schema.json`
  - `wiki/outputs/data/enriched/frame-data/zangief/supercombo-only.csv`
  - `wiki/outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data.md`
  - `wiki/outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk.md`
  - `wiki/sources/supercombo-zangief-frame-data.md`
  - `wiki/reviews/2026-06-02-supercombo-zangief-frame-data-capture-review.md`
  - `wiki/entities/zangief.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Zangief の `enriched_review_required` 25 行を、JP/Ryu と同じ形式で `human_review_*` 列に反映した。
  - review decision の内訳は `supplemental_link` 19 件、`hold_supplemental_link` 3 件、`movement_variant_supplemental_link` 2 件、`conflict_supplemental_only` 1 件。
  - 公式列は正として保持し、SuperCombo の range、juggle、notes、hitbox、damage decomposition、startup decomposition は補助情報として扱う。
  - `ツンドラストーム` は startup / active duration conflict があるため、公式値を正とした `conflict_supplemental_only` として accepted にした。
- 未解決事項:
  - `imageinfo` で missing の 4 件を source 側の欠損として扱うか、filename 正規化で再解決するか。

## [2026-06-02] ルール更新 | wiki/log.md と Zangief 追記の日本語化
- 更新:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `wiki/log.md`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/sources/supercombo-zangief-frame-data.md`
  - `wiki/reviews/2026-06-02-supercombo-zangief-frame-data-capture-review.md`
  - `wiki/outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk.md`
  - `wiki/outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data.md`
- メモ:
  - `wiki/log.md` も読者向け wiki 本文として日本語優先にするルールを `AGENTS.md` と `CLAUDE.md` に明記した。
  - 直近の Zangief 追記と関連カタログ文の英語説明ラベルを、日本語の読者向け表現へ寄せた。
  - `wiki/log.md` の過去エントリに残っていた共通ラベルと未解決事項の英語文も、意味を変えない範囲で日本語へ置き換えた。
  - `raw/` 配下の原本は変更していない。
- 未解決事項:
  - 既存 wiki 全体に残る English/ASCII technical terms を、構造識別子・公式用語として許容する範囲と追加 lint 対象にする範囲に分けるか。

## [2026-06-02] ingest | SuperCombo Zangief フレームデータ
- 原本:
  - `raw/frame-data/supercombo/zangief/manifest.json`
  - `raw/frame-data/supercombo/zangief/data.raw.wikitext`
  - `raw/frame-data/supercombo/zangief/frame-data.raw.wikitext`
- 作成:
  - `wiki/sources/supercombo-zangief-frame-data.md`
  - `wiki/reviews/2026-06-02-supercombo-zangief-frame-data-capture-review.md`
  - `wiki/outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk.md`
  - `wiki/outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data.md`
  - `wiki/outputs/data/supercombo/frame-data/zangief/`
  - `wiki/outputs/data/enriched/frame-data/zangief/`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/syntheses/frame-data-raw-layout.md`
  - `wiki/log.md`
- メモ:
  - SuperCombo Zangief を Scrapling で `https://wiki.supercombo.gg/w/Street_Fighter_6/Zangief/Frame_data` から取得した。
  - source revision label は `2026-06-01`。Data page revision は `2026-06-01T07:31:24Z`、Frame data page revision は `2024-10-19T05:08:24Z`。
  - 検証は 68 件の frame template、1 件の character template、21 件の表示 Cargo query、20 件の DOM table comparison、165 件の画像ダウンロードで通過した。
  - Zangief 専用の照合処理として、`key-circle` / 360 / 720 input、hold row、近距離/中距離/遠距離 row、CA variant を追加した。
  - 照合サマリーは 46 件の自動一致、24 件の `matched_manual`、2 件の公式側未照合、4 件の SuperCombo-only taunt row。
  - 補助列付きデータのサマリーは 45 件の `enriched`、25 件の `enriched_review_required`、2 件の `official_only`。公式列を正とする方針は維持している。
- 未解決事項:
  - Zangief の name override による 24 件の一致を、レビュー済み補助リンクとして採用できるか。
  - `imageinfo` で missing になった 4 件が、source 側の欠損なのか filename 正規化で解決できる問題なのか。
  - `ツンドラストーム` の startup / active duration 差分を別の review note に切り出すべきか。

## [2026-06-01] Wiki 更新 | frame-data raw latest mirror 配置の反映
- 追加:
  - `wiki/syntheses/frame-data-raw-layout.md`
- 更新:
  - `wiki/index.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/jp.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/outputs/reports/2026-05-30-official-frame-data-coverage.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/outputs/data/supercombo/frame-data/jp/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
  - `wiki/sources/capcom-official-*-frame-data.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
- 決定:
  - frame-data raw の現在の入口は `raw/frame-data/official/<data-slug>/` と `raw/frame-data/supercombo/<character>/` の latest mirror 固定パスとして説明する。
  - capture date は path ではなく official manifest の `capture_label` / `created_at_utc`、SuperCombo manifest の `capture_label` / `captured_at_utc` / `source_revision` で追う。
  - historical log / review に残る旧 date-based path は当時の履歴として扱い、現在の読者向け入口は source page、coverage report、synthesis、index に置く。
- 検証:
  - `raw/frame-data/official/*/manifest.json` を確認し、30 official slugs が `storage_policy: latest_frame_data_mirror`、Classic / Modern captures、derived output paths を持つことを確認した。
  - `raw/frame-data/supercombo/jp/manifest.json` と `raw/frame-data/supercombo/ryu/manifest.json` を確認し、`capture_label: 2026-05-30`、`storage_policy: latest_frame_data_mirror`、`source_revision` があることを確認した。
  - `wiki/index.md` の SuperCombo JP / Ryu `Source date` は、取得日ではなく manifest の `capture_label` / source revision に合わせて `2026-05-30` とした。
  - `wiki/sources`、`wiki/outputs/reports`、`wiki/concepts`、`wiki/entities`、`wiki/index.md` の現在参照用ページに旧 `raw/official/frame-data/...` / `raw/supercombo/frame-data/...` path が残っていないことを `rg` で確認した。
  - `wiki/outputs/data/supercombo/frame-data/{jp,ryu}/` の `source_raw_root` / `raw_root` も新 raw path に更新した。
- 未解決事項:
  - official manifest の `raw_review_status` と wiki review page の accepted / pending 状態を同期する運用ルール。
  - `latest_frame_data_mirror` 再取得時に旧 mirror をどこまで外部 artifact として保持するか。

## [2026-06-01] レビュー | Ryu SuperCombo-only 空中竜巻 variant link
- 更新:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/schema.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 決定:
  - `ryu_6hk_214k` は primary official row 41 `空中竜巻旋風脚`、enabled-by row 23 `旋風脚` の conditional variant として扱う。
  - `ryu_6hk_214kk` は primary official row 42 `OD 空中竜巻旋風脚`、enabled-by row 23 `旋風脚` の conditional variant として扱う。
  - row 23 `旋風脚` の damage 800 / startup 16 と、キャンセル後の空中竜巻派生 damage / startup は合算・上書きしない。
- 検証:
  - SuperCombo-only suggested handling は `supplemental_variant_row` 2、`supercombo_only_taunt` 4。
  - `supercombo-only.csv` に `primary_official_row_order`、`enabled_by_official_row_order`、`link_note` などの link fields を追加した。
  - 公式由来列は `wiki/outputs/data/frame-data/ryu/classic.csv` と補助列付き output で全行一致した。
  - `uv run python -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - conditional variant link を他 character にも使う場合、どこまで汎用 schema 化するか。

## [2026-05-31] レビュー | Ryu 公式 + SuperCombo 補助行の人間レビュー反映
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/supercombo-unmatched.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 決定:
  - `[電刃錬気]波動拳`、`[電刃錬気]OD 波動拳`、`[電刃錬気]波掌撃`、`[電刃錬気]SA1 真空波動拳` は Denjin / charged variant の `move_id` に補助リンクする。
  - `SA2 真波掌撃（Lv2/Lv3）` と `[電刃錬気]SA2 真波掌撃（Lv2/Lv3）` は hold-level variant の `move_id` に補助リンクする。
  - `OD 波掌撃` は active duration conflict 付き補助情報として扱い、公式 active `18-22` を正とする。
  - `パリィドライブラッシュ` と `キャンセルドライブラッシュ` は補助リンクとして採用する。
- 検証:
  - enriched status は `enriched` 60 rows、`enriched_reviewed` 13 rows、`official_only` 2 rows。
  - human review decisions は `supplemental_link` 8、`hold_level_supplemental_link` 4、`conflict_supplemental_only` 1。
  - 照合結果は `matched` 61、`matched_manual` 10、`ambiguous` 2、`unmatched` 2。
  - SuperCombo-only rows は 6。`6HK~214K` / `6HK~214KK` と taunt 4件のみ。
  - 公式由来列は `wiki/outputs/data/frame-data/ryu/classic.csv` と補助列付き output で全行一致した。
  - `uv run python -m py_compile tools/extract_supercombo_frame_data.py tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - 公式に存在する damage / startup / active / recovery などの基本数値は公式列を正とし、SuperCombo 値は `supercombo_*` 補助列として保持する。
  - SA2 Lv2 / Lv3 の SuperCombo startup `18~` / `50~` は hold-level 補助情報で、公式 startup 20 / 70 を上書きしない。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - SuperCombo-only の `6HK~214K` / `6HK~214KK` を公式 row の補助情報として扱うか。

## [2026-05-31] 出力 | SuperCombo Ryu 派生データと公式 Ryu 補助データ生成
- 追加:
  - `wiki/outputs/data/supercombo/frame-data/ryu/frames.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/character.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/supercombo-unmatched.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/schema.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - SuperCombo Ryu derived `frames.csv` は 77 rows、`character.csv` は 1 row。
  - 公式 Ryu Classic 75 rows との候補照合は matched 61、ambiguous 10、generic name override matched 2、unmatched 2。
  - enriched rows は 75。内訳は `enriched` 60、`enriched_review_required` 13、`official_only` 2。
  - SuperCombo-only rows は 14。suggested handling は `supercombo_only` 10、`supercombo_only_taunt` 4。
  - `uv run python -m py_compile tools/extract_supercombo_frame_data.py tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - Ryu の `enriched_review_required` 13 rows は accepted 扱いにしない。
  - `パリィドライブラッシュ` / `キャンセルドライブラッシュ` は generic name override で紐づけるが、人間レビューは未完了。
- 未解決事項:
  - Ryu のレビュー対象 13 行を人間レビューする。
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。

## [2026-05-31] 取り込み | SuperCombo Ryu フレームデータ取得
- 追加:
  - `raw/supercombo/frame-data/2026-05-31/ryu/`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/reviews/2026-05-31-supercombo-ryu-frame-data-capture-review.md`
- 更新:
  - `tools/validate_supercombo_frame_data.py`
  - `wiki/index.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/log.md`
- 検証:
  - Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
  - `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 77 件を抽出した。
  - Cargo API は `SF6_FrameData` 77 行、`SF6_CharacterData` 1 行を返し、raw template 件数と一致した。
  - `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state と、4 section x 5 tab = 20 table comparisons を保存した。
  - 5枚の full-page screenshot は目視確認済み。Character Data、各 tab の table、下部 navigation、footer が写っている。
  - 画像参照 173 件、distinct filename 134 件のうち、MediaWiki `imageinfo` で 133 件を解決し、133 件を download した。
  - `uv run python tools/validate_supercombo_frame_data.py --repo-root . --date-label 2026-05-31 --character-slug ryu` は成功。warning は `1 imageinfo titles are missing`。
  - `uv run python -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。
- 注意:
  - Ryu は duplicate input が 10 種類あるため、SuperCombo raw 内では `moveId` を行識別子として扱う。
  - Ryu では `moveType` に `Special` / `Super` の大文字表記があるため、validator で小文字正規化するようにした。
- 未解決事項:
  - missing imageinfo の `File:SF6 Ryu 236p hitbox.png` を、削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
  - Ryu の Denjin / hold level / duplicate input rows の merge policy。

## [2026-05-31] レビュー | JP 公式 + SuperCombo 補助行の人間レビュー反映
- 更新:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/jp/schema.json`
  - `wiki/outputs/data/enriched/frame-data/jp/summary.json`
  - `wiki/outputs/reports/2026-05-31-jp-official-supercombo-enriched-data.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/log.md`
- 決定:
  - `ヴィーハト・アクノ`、`パリィドライブラッシュ`、`キャンセルドライブラッシュ` は `supplemental_link` として採用。
  - `ヴィーハト・チェーニ` は `non_additive_supplemental_damage`。発火した spike damage は補助情報で、元ヴィーハト damage と合算しない。
  - `SA2 ラヴーシュカ` は startup conflict付き補助情報。公式 startup 29 を正とする。
- 検証:
  - enriched status は `enriched` 62 rows、`enriched_reviewed` 5 rows、`official_only` 2 rows。
  - human review decisions は `supplemental_link` 3、`non_additive_supplemental_damage` 1、`conflict_supplemental_only` 1。
  - `python3 -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - 多対一対応 rows と SuperCombo-only rows の正式 merge policy。

## [2026-05-31] 出力 | JP 公式データへの SuperCombo 補助列付与
- 追加:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/jp/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/schema.json`
  - `wiki/outputs/data/enriched/frame-data/jp/summary.json`
  - `wiki/outputs/reports/2026-05-31-jp-official-supercombo-enriched-data.md`
- 更新:
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - 公式 JP Classic 69 rows を保持したまま、SuperCombo 補助列を `supercombo_*` prefix で追加した。
  - enriched rows は 69。内訳は enriched 62、enriched review required 5、official only 2。
  - SuperCombo-only rows は 7。suggested handling は supplemental variant 2、supplemental followup 2、taunt 3。
  - 基本値 conflict は damage 1件、startup 1件。
  - `python3 -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - この output は公式 CSV の置換ではない。公式にある基本フレーム値は公式列を正とし、SuperCombo 値は補助列に分離している。
  - `enriched_review_required` の 5 rows は人間レビューが必要。
- 未解決事項:
  - `ヴィーハト・チェーニ` と `SA2 ラヴーシュカ` の conflict をどう扱うか。
  - official only の前方/後方ステップを、SuperCombo character data の dash fields と別枠で結合するか。

## [2026-05-31] 出力 | SuperCombo JP 派生データと公式 JP 候補照合
- 追加:
  - `tools/extract_supercombo_frame_data.py`
  - `wiki/outputs/data/supercombo/frame-data/jp/frames.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/character.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/supercombo-unmatched.csv`
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
- 更新:
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `tools/extract_supercombo_frame_data.py` は SuperCombo validation passed の raw snapshot だけを入力にする。
  - `frames.csv` は 64 rows、`character.csv` は 1 row。
  - 公式 JP Classic 69 rows との候補照合は、automatic matched 63、JP 固有名 override matched 4、unmatched 2。
  - SuperCombo 側は 64 rows 中 57 distinct rows が候補照合され、7 rows が公式 Classic frame row にはない補助候補として残った。
  - `python3 -m py_compile tools/extract_supercombo_frame_data.py` は成功。
- 注意:
  - 照合結果は最終マージではなくレビュー用候補。公式に存在する基本フレーム値は Capcom 公式 data を正とする。
  - `前方ステップ` と `後方ステップ` は公式側 unmatched。SuperCombo では frame row ではなく character data の dash fields に対応する可能性がある。
- 未解決事項:
  - `matched_manual` 4件と多対一対応 rows を人間レビューして、正式 merge policy に昇格するか。
  - SuperCombo unmatched 7 rows を公式 row の補助情報として扱うか、SuperCombo-only rows として保持するか。

## [2026-05-31] 取り込み | SuperCombo JP フレームデータの生データ取得
- 原本:
  - `raw/supercombo/frame-data/2026-05-31/jp/manifest.json`
  - `raw/supercombo/frame-data/2026-05-31/jp/data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/jp/frame-data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/jp/cargo/`
  - `raw/supercombo/frame-data/2026-05-31/jp/rendered/`
  - `raw/supercombo/frame-data/2026-05-31/jp/screenshots/`
  - `raw/supercombo/frame-data/2026-05-31/jp/images/files/`
- 追加:
  - `tools/capture_supercombo_frame_data.py`
  - `tools/validate_supercombo_frame_data.py`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/reviews/2026-05-31-supercombo-jp-frame-data-capture-review.md`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/jp.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
  - `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 64 件を抽出した。
  - Cargo API は `SF6_FrameData` 64 行、`SF6_CharacterData` 1 行を返し、raw template 件数と一致した。
  - `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state と、4 section x 5 tab = 20 table comparisons を保存した。
  - 5枚の full-page screenshot は目視確認済み。Character Data、各 tab の table、下部 navigation、footer が写っている。
  - 画像参照 143 件、distinct filename 134 件のうち、MediaWiki `imageinfo` で 123 件を解決し、123 件を download した。
  - `tools/validate_supercombo_frame_data.py` は passed。warning は `11 imageinfo titles are missing`。
  - `python3 -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。
- 注意:
  - `6HPHK` と `236236K` は同じ input を持つ複数 row があるため、SuperCombo raw 内では `moveId` を行識別子として扱う。
  - 公式 data と重なる基本フレーム値では Capcom 公式 data を優先し、SuperCombo は公式にない range、juggle、notes、hitbox image などを後で統合する候補 source として扱う。
- 未解決事項:
  - `imageinfo` で missing になった 11 件の画像参照を、削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
  - 公式 JP data と SuperCombo `moveId` rows の crosswalk policy をどう定義するか。
  - SuperCombo の HTML 装飾付き frame advantage を、公式 CSV と比較可能な値へ正規化する schema をいつ作るか。

## [2026-05-30] 質問 | 春麗の立ち中Pからしゃがみ中Pへのリンク可否
- 質問:
  - 春麗の立ち中Pが通常ヒットしたあと、発生6Fのしゃがみ中Pは理論上つながる？理由もフレームで説明して。
- 参照:
  - `wiki/index.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
  - `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
- 作成:
  - `wiki/questions/chun-li-standing-medium-p-into-crouching-medium-p-link.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - 理論上はつながる。`立ち中P（頸穿刀）`は通常ヒット時`+6F`、
    `しゃがみ中P（丹頂拳）`は発生`6F`なので、`+6F - 6F = 0F`。
    最速なら連続ヒットするが、数値上の余裕はない。
- 未解決事項:
  - 実戦での距離、押し戻し、食らい判定は別途確認が必要。

## [2026-05-30] 質問レビュー | 春麗の立ち中P回答の修正
- レビュー指摘:
  - 発生、硬直差、キャンセル、ダメージだけでなく、持続と硬直も含める。
  - `C`は必殺技、ドライブインパクト、ドライブラッシュ、SAでキャンセル可能という意味だと説明する。
  - ガード時`+1`は、ガードされた時に春麗側が有利という意味だと説明する。
- 更新:
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 修正後の回答要約:
  - `立ち中P（頸穿刀）`: 発生5F、持続5-8F、硬直10F、ヒット時+6F、
    ガード時+1F、キャンセル`C`、ダメージ600。
- 未解決事項:
  - なし。

## [2026-05-30] 質問 | 春麗の立ち中Pのフレームデータ
- 質問:
  - 春麗の立ち中Pは、発生・ヒット時・ガード時・キャンセル可否・ダメージを教えて。
- 参照:
  - `wiki/index.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
- 作成:
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - 春麗の`立ち中P（頸穿刀）`はクラシックとモダンで同じ値:
    発生5F、ヒット時+6F、ガード時+1F、キャンセル`C`、ダメージ600。
- 未解決事項:
  - この質問ではなし。

## [2026-05-30] ingest | Official frame-data coverage for remaining roster
- 読み込み:
  - `AGENTS.md`
  - `wiki/index.md`
  - recent entries in `wiki/log.md`
  - existing official frame-data source, entity, review, and concept pages
  - official Capcom frame-data pages via `tools/capture_capcom_frame_data.py`
- raw snapshot 作成:
  - `raw/official/frame-data/2026-05-30/luke/`
  - `raw/official/frame-data/2026-05-30/jamie/`
  - `raw/official/frame-data/2026-05-30/guile/`
  - `raw/official/frame-data/2026-05-30/kimberly/`
  - `raw/official/frame-data/2026-05-30/juri/`
  - `raw/official/frame-data/2026-05-30/ken/`
  - `raw/official/frame-data/2026-05-30/blanka/`
  - `raw/official/frame-data/2026-05-30/dhalsim/`
  - `raw/official/frame-data/2026-05-30/ehonda/`
  - `raw/official/frame-data/2026-05-30/deejay/`
  - `raw/official/frame-data/2026-05-30/manon/`
  - `raw/official/frame-data/2026-05-30/marisa/`
  - `raw/official/frame-data/2026-05-30/lily/`
  - `raw/official/frame-data/2026-05-30/cammy/`
  - `raw/official/frame-data/2026-05-30/rashid/`
  - `raw/official/frame-data/2026-05-30/aki/`
  - `raw/official/frame-data/2026-05-30/ed/`
  - `raw/official/frame-data/2026-05-30/gouki_akuma/`
  - `raw/official/frame-data/2026-05-30/vega_mbison/`
  - `raw/official/frame-data/2026-05-30/terry/`
  - `raw/official/frame-data/2026-05-30/mai/`
  - `raw/official/frame-data/2026-05-30/elena/`
  - `raw/official/frame-data/2026-05-30/sagat/`
  - `raw/official/frame-data/2026-05-30/cviper/`
  - `raw/official/frame-data/2026-05-30/alex/`
  - `raw/official/frame-data/2026-05-30/ingrid/`
- wiki page 作成:
  - `wiki/sources/capcom-official-luke-frame-data.md`
  - `wiki/sources/capcom-official-jamie-frame-data.md`
  - `wiki/sources/capcom-official-guile-frame-data.md`
  - `wiki/sources/capcom-official-kimberly-frame-data.md`
  - `wiki/sources/capcom-official-juri-frame-data.md`
  - `wiki/sources/capcom-official-ken-frame-data.md`
  - `wiki/sources/capcom-official-blanka-frame-data.md`
  - `wiki/sources/capcom-official-dhalsim-frame-data.md`
  - `wiki/sources/capcom-official-e-honda-frame-data.md`
  - `wiki/sources/capcom-official-dee-jay-frame-data.md`
  - `wiki/sources/capcom-official-manon-frame-data.md`
  - `wiki/sources/capcom-official-marisa-frame-data.md`
  - `wiki/sources/capcom-official-lily-frame-data.md`
  - `wiki/sources/capcom-official-cammy-frame-data.md`
  - `wiki/sources/capcom-official-rashid-frame-data.md`
  - `wiki/sources/capcom-official-aki-frame-data.md`
  - `wiki/sources/capcom-official-ed-frame-data.md`
  - `wiki/sources/capcom-official-gouki-akuma-frame-data.md`
  - `wiki/sources/capcom-official-vega-m-bison-frame-data.md`
  - `wiki/sources/capcom-official-terry-frame-data.md`
  - `wiki/sources/capcom-official-mai-frame-data.md`
  - `wiki/sources/capcom-official-elena-frame-data.md`
  - `wiki/sources/capcom-official-sagat-frame-data.md`
  - `wiki/sources/capcom-official-c-viper-frame-data.md`
  - `wiki/sources/capcom-official-alex-frame-data.md`
  - `wiki/sources/capcom-official-ingrid-frame-data.md`
  - `wiki/entities/luke.md`
  - `wiki/entities/jamie.md`
  - `wiki/entities/guile.md`
  - `wiki/entities/kimberly.md`
  - `wiki/entities/juri.md`
  - `wiki/entities/ken.md`
  - `wiki/entities/blanka.md`
  - `wiki/entities/dhalsim.md`
  - `wiki/entities/e-honda.md`
  - `wiki/entities/dee-jay.md`
  - `wiki/entities/manon.md`
  - `wiki/entities/marisa.md`
  - `wiki/entities/lily.md`
  - `wiki/entities/cammy.md`
  - `wiki/entities/rashid.md`
  - `wiki/entities/aki.md`
  - `wiki/entities/ed.md`
  - `wiki/entities/gouki-akuma.md`
  - `wiki/entities/vega-m-bison.md`
  - `wiki/entities/terry.md`
  - `wiki/entities/mai.md`
  - `wiki/entities/elena.md`
  - `wiki/entities/sagat.md`
  - `wiki/entities/c-viper.md`
  - `wiki/entities/alex.md`
  - `wiki/entities/ingrid.md`
  - `wiki/reviews/2026-05-30-official-frame-data-roster-capture-review.md`
  - `wiki/outputs/reports/2026-05-30-official-frame-data-coverage.md`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/capcom.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 派生 output:
  - Added Classic and Modern CSV plus field-meaning JSON outputs under
    `wiki/outputs/data/frame-data/<data-slug>/` for 26 new character data slugs.
- 検証:
  - `tools/validate_capcom_frame_data.py` passed for all 26 new 2026-05-30
    captures.
  - Existing accepted JP, Ryu, Chun-Li, and Zangief captures were also
    revalidated against their raw snapshots.
  - Total coverage is now 30 character data slugs with Classic and Modern
    derived outputs.
- メモ:
  - 公式 frame-data table slug は `gouki_akuma` と `vega_mbison` であり、短い character navigation slug の `gouki` / `vega` ではない。
  - short slug で失敗した試行から生成された空の `raw/official/frame-data/2026-05-30/gouki/manifest.json` は、ingest 記録前に削除した。
- 未解決事項:
  - 26 件の新規取得データを個別に人間レビューするか、代表スクリーンショットの確認後に batch として accepted にするか。
  - roster 全体を単一日付 snapshot にするため、JP、Ryu、Chun-Li、Zangief を `2026-05-30` date label で再取得するか。

## [2026-05-27] concept-update | Frame-data comparison policy
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/reviews/2026-05-27-health-check.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 記録した決定:
  - Classic/Modern frame-data comparisons default to exact official move-name
    matching.
  - Likely corresponding move-name variants are annotated rather than silently
    normalized.
  - Command notation in reader-facing answers remains a display-only transform
    for now; raw input tokens remain source-preserving data.
- 未解決事項:
  - When, if ever, should display-only command notation become a formal wiki
    notation schema?

## [2026-05-27] human-review | Accept post-Zangief wiki health check
- レビュー:
  - `wiki/reviews/2026-05-27-health-check.md`
  - source-page stale open question cleanup
  - accepted character entity cleanup
- 更新:
  - `wiki/reviews/2026-05-27-health-check.md`
  - `wiki/log.md`
- 決定:
  - Accepted the health check while keeping `status: open`.
  - Accepted keeping JP, Ryu, Chun-Li, and Zangief validation results in the
    health check.
  - Accepted deletion of stale source-page questions about whether already-filed
    comparison pages should be created.
  - Accepted cleanup of accepted character entity wording.
- 設計判断:
  - Command notation remains a display-only transform for now.
  - Classic/Modern move comparison defaults to exact official move-name matching.
  - Likely corresponding name variants, such as `しゃがみ強K（ビッグスタンプ）` and
    `ビッグスタンプ`, should be annotated rather than silently normalized.
- メモ:
  - Older open questions in `wiki/log.md` remain unchanged because the log is
    append-only.

## [2026-05-27] lint | post-Zangief wiki health check
- 読み込み:
  - `AGENTS.md`
  - `wiki/index.md`
  - recent `wiki/log.md` entries
  - official frame-data source pages
  - accepted character entity pages
  - filed Classic/Modern comparison question pages
- 作成:
  - `wiki/reviews/2026-05-27-health-check.md`
- 更新:
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/jp.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/chun-li.md`
  - `wiki/entities/zangief.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 確認:
  - Non-template wiki pages have no broken wikilinks.
  - Content pages have frontmatter.
  - Existing non-template wiki pages were registered in `wiki/index.md`.
  - Question pages do not contain operational file-back sections or changed-file
    summaries.
  - Accepted JP, Ryu, Chun-Li, and Zangief frame-data outputs passed validation
    against raw snapshots.
- クリーンアップ:
  - Removed stale source open questions about filing comparison pages that now
    exist.
  - Removed stale wording implying accepted captures were still waiting for
    human review.
- 未解決事項:
  - command-input normalization を正式な wiki concept にするか。
  - 追加の Classic/Modern comparison page を作る前に、move-name identity normalization を導入するか。

## [2026-05-27] query | Zangief Classic vs Modern frame-data comparison
- 質問:
  - Zangiefのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- 作成:
  - `wiki/questions/zangief-modern-vs-classic-frame-data-moves-and-inputs.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - Classic has 72 official frame-data items and Modern has 66.
  - Exact official move-name matching gives 65 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（ビッグスタンプ）` / `ビッグスタンプ` naming difference is
    called out explicitly instead of silently normalizing it.
  - Of 65 shared move names, 62 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 18 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
  - One/two-circle inputs are rendered in the answer as readable command
    notation while the raw source keeps the original input tokens.
- 未解決事項:
  - 今後の comparison page で name variant をまたいだ move identity normalization を行うか、公式技名の完全一致を default のままにするか。

## [2026-05-27] human-review | Accept official Zangief frame-data capture
- 更新:
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/reviews/2026-05-27-official-zangief-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- 決定:
  - Accepted.
- レビュー確認:
  - Full validation passed for Classic 72 rows and Modern 66 rows.
  - `page.html` table hashes match `table.dom.json`.
  - Saved CSV rows match raw-DOM-regenerated rows.
  - Field meanings are regenerated from DOM and match saved JSON.
  - Screenshots show the official Zangief page, selected tabs, full table width,
    table bottom, character select, and footer.
  - Zangief-specific inputs such as `key-circle`, `key-circle key-circle`,
    command grabs, Modern SP/AUTO shortcuts, and parenthesized normal-command
    alternatives are retained.
- クリーンアップ:
  - review index table の review type label を、review page frontmatter に合わせて `capture_validation` に統一した。

## [2026-05-27] ingest | Capcom official Zangief frame data
- 原本:
  - `raw/official/frame-data/2026-05-27/zangief/manifest.json`
  - `raw/official/frame-data/2026-05-27/zangief/classic/`
  - `raw/official/frame-data/2026-05-27/zangief/modern/`
- 派生 output:
  - `wiki/outputs/data/frame-data/zangief/classic.csv`
  - `wiki/outputs/data/frame-data/zangief/modern.csv`
  - `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json`
- 作成:
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/reviews/2026-05-27-official-zangief-frame-data-capture-review.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- 検証:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/zangief/frame`.
  - Extract command reproduced 72 Classic rows and 66 Modern rows from raw DOM.
  - Full validation confirmed `page.html` table hashes, raw DOM, derived CSV,
    field-meanings JSON, overlay metadata, and screenshot coverage for all rows.
  - Metadata reports zero visible Cookiebot and navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width and page
    footer for both Classic and Modern captures.
  - Zangief-specific command-grab and one/two-circle input tokens are retained
    in `input_token_json`.
- 状態:
  - Pending human review before marking the Zangief capture accepted.
- 未解決事項:
  - 人間レビュー後に Zangief Classic/Modern comparison question を file back するか。
  - Which character should be used next to stress-test unusual frame-data table
    formats?

## [2026-05-27] query | Chun-Li Classic vs Modern frame-data comparison
- 質問:
  - Chun-Liのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- 作成:
  - `wiki/questions/chun-li-modern-vs-classic-frame-data-moves-and-inputs.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - Classic has 78 official frame-data items and Modern has 72.
  - Exact official move-name matching gives 71 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（元伝暗殺蹴）` / `元伝暗殺蹴` naming difference is called
    out explicitly instead of silently normalizing it.
  - Of 71 shared move names, 68 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 15 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
- 未解決事項:
  - 今後の comparison page で name variant をまたいだ move identity normalization を行うか、公式技名の完全一致を default のままにするか。

## [2026-05-27] human-review | Accept official Chun-Li frame-data capture
- 更新:
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/entities/chun-li.md`
  - `wiki/reviews/2026-05-27-official-chun-li-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- 決定:
  - Accepted.
- レビュー確認:
  - Raw placement matches the JP and Ryu conventions.
  - Classic and Modern screenshots show the intended Chun-Li official tables
    without visible horizontal cutoff or obstructing overlays.
  - DOM row counts, manifest row counts, and CSV row counts match: Classic 78,
    Modern 72.
  - Field meanings are present: Classic 7 records, Modern 8 records, including
    the Modern SP-button 80% damage note.
  - Chun-Li source, entity, review, and outputs are reachable from the index.
  - Stance-like, branch, charge, and air-action inputs are retained in
    `input_token_json`.
- クリーンアップ:
  - Restored `[[entities/jp]]` to `wiki/concepts/frame-data.md` frontmatter
    `related` to match the page connections and index.
- メモ:
  - Source and review statuses were moved from `pending_human_review` to active
    or accepted as appropriate.

## [2026-05-27] ingest | Capcom official Chun-Li frame data
- 原本:
  - `raw/official/frame-data/2026-05-27/chunli/manifest.json`
  - `raw/official/frame-data/2026-05-27/chunli/classic/`
  - `raw/official/frame-data/2026-05-27/chunli/modern/`
- 派生 output:
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
  - `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`
- 作成:
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/entities/chun-li.md`
  - `wiki/reviews/2026-05-27-official-chun-li-frame-data-capture-review.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- 検証:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/chunli/frame`.
  - Extract command reproduced 78 Classic rows and 72 Modern rows from raw DOM.
  - Metadata reports separate Classic and Modern tab captures with no visible
    Cookiebot or navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width.
- 状態:
  - Pending human review before marking the Chun-Li capture accepted.
- 未解決事項:
  - 人間レビュー後に Chun-Li Classic/Modern comparison question を file back するか。
  - Which character should be used next to stress-test unusual frame-data table
    formats?

## [2026-05-27] query | Ryu Modern vs Classic frame-data counts and inputs
- 質問:
  - Ryuのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
- 作成:
  - `wiki/questions/ryu-modern-vs-classic-frame-data-moves-and-inputs.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - Classic has 75 official frame-data items and Modern has 69.
  - Exact official move-name matching gives 68 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（回転足払い）` / `回転足払い` naming difference is called
    out explicitly instead of silently normalizing it.
  - Of 68 shared move names, 65 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 22 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
- 未解決事項:
  - 今後の comparison page で name variant をまたいだ move identity normalization を行うか、公式技名の完全一致を default のままにするか。

## [2026-05-27] human-review | Accept official Ryu frame-data capture
- 更新:
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/reviews/2026-05-27-official-ryu-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- 決定:
  - Accepted.
- レビュー確認:
  - Raw placement matches the JP convention.
  - Classic and Modern screenshots show the intended Ryu official tables without
    visible horizontal cutoff or obstructing overlays.
  - DOM row counts, manifest row counts, and CSV row counts match: Classic 75,
    Modern 69.
  - Field meanings are present: Classic 7 records, Modern 8 records, including
    the Modern SP-button 80% damage note.
  - Ryu source, entity, review, and outputs are reachable from the index.
- メモ:
  - Source and review statuses were moved from `pending_human_review` to active
    or accepted as appropriate.

## [2026-05-27] schema | Simplify official frame-data CSV rows
- 更新:
  - `tools/capture_capcom_frame_data.py`
  - `tools/extract_capcom_frame_data.py`
  - `README.md`
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
  - `wiki/log.md`
- メモ:
  - Removed repeated source-level metadata from per-move CSV rows.
  - `publisher`、`game`、`locale`、`source_url`、character、control scheme、raw 取得 path、screenshot path は raw manifest、raw metadata、output path、wiki source page に残す。
  - Kept CSVs focused on row-level frame-data fields to make diffs and manual
    inspection easier.

## [2026-05-27] ingest | Capcom official Ryu frame data
- 原本:
  - `raw/official/frame-data/2026-05-27/ryu/manifest.json`
  - `raw/official/frame-data/2026-05-27/ryu/classic/`
  - `raw/official/frame-data/2026-05-27/ryu/modern/`
- 派生 output:
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
  - `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json`
- 作成:
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/reviews/2026-05-27-official-ryu-frame-data-capture-review.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- 検証:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/ryu/frame`.
  - Extract command reproduced 75 Classic rows and 69 Modern rows from raw DOM.
  - Metadata reports separate Classic and Modern tab captures with no visible
    Cookiebot or navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width.
- 状態:
  - Pending human review before marking the Ryu capture accepted.
- 未解決事項:
  - 人間レビュー後に Ryu Classic/Modern comparison question を file back するか。
  - 次に unusual frame-data table format の stress-test 対象にする character はどれか。

## [2026-05-27] review-removal | Remove stale initial health check
- 削除:
  - `wiki/reviews/2026-05-26-health-check.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Removed the initial health check because it described the early wiki state
    around a now-deleted filed-back juggle answer.
  - Kept `wiki/reviews/2026-05-26-official-jp-frame-data-capture-review.md`
    because it records the human acceptance of the official JP frame-data
    capture and remains useful evidence.

## [2026-05-27] query-removal | Remove low-quality juggle answer
- 削除:
  - `wiki/questions/how-juggles-work-internally.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Removed the filed-back juggle question because the current answer quality
    and reader-facing shape no longer match the standard established by later
    question-page tuning.
  - Kept the underlying SuperCombo source and related concept pages intact; this
    is a removal of a weak answer, not a rejection of the source.
- フォローアップ:
  - Re-answer the juggle mechanism question later after the relevant official
    Capcom terminology or a stronger source has been ingested.

## [2026-05-27] query-review | Format JP command examples
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Wrapped command notation examples in inline code for readability.

## [2026-05-27] query-review | Sort JP damage differences by move family
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Reordered the damage-difference table so variants of the same move family,
    such as Stribog and Triglav, stay adjacent.

## [2026-05-27] query-review | Remove bare source footer from JP comparison
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Removed the bare `参照元` wikilink from the answer body because the source
    is already recorded in frontmatter.
  - Kept the evidence section focused on what was checked rather than exposing
    wiki navigation details to the reader.

## [2026-05-27] query-review | Make JP comparison answer less implementation-facing
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Removed implementation-facing wording such as CSV, derived data, and row
    counting from the durable answer prose.
  - Reworded the answer around official frame-data items, move names, input
    displays, and the practical Classic/Modern differences a reader asked for.

## [2026-05-27] schema | Keep question pages reader-facing
- 更新:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `ROADMAP.md`
  - `wiki/templates/question.md`
  - `wiki/questions/how-juggles-work-internally.md`
  - `wiki/log.md`
- メモ:
  - Removed `Filed-back updates` from the question template and the existing
    juggle question page.
  - Clarified that `wiki/questions/` pages are durable reader-facing answers.
  - Operational file-back details, changed files, and task summaries now belong
    in `wiki/log.md` or the final task report, not in question pages.

## [2026-05-26] query-review | Simplify evidence wording
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Replaced internal derived-output file paths in the evidence section with
    user-facing source wording.
  - Kept the wiki source link as the traceability anchor.

## [2026-05-26] query-review | Remove workflow notes from JP answer
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Removed the `File-back` workflow section from the durable answer page.
  - Shortened the caveats so user-facing prose does not expose unnecessary
    storage-field details.

## [2026-05-26] query-review | Prefer official column wording
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Replaced internal comparison field names in user-facing prose with official
    table wording such as 技名 and 入力表示.
  - Kept storage field names only where the page explicitly discusses stored
    evidence fields.

## [2026-05-26] query-review | Display command notation for JP comparison
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Replaced raw DOM tokens such as `key-d` and `icon_punch_l` in user-facing
    examples with readable command notation such as ↓, ↘, →, 弱P, and 強K.
  - Left raw token field names in the limitations section to clarify the stored
    evidence format.

## [2026-05-26] query-review | Japanese wording for JP Modern vs Classic answer
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- メモ:
  - Converted user-facing section headings and explanatory prose to Japanese.
  - Kept technical field names such as `move_name`, `input_raw_display`, and
    token names unchanged where they identify stored data fields.

## [2026-05-26] query-review | Improve JP Modern vs Classic answer
- 更新:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Reworked the answer to start with a user-facing conclusion instead of a CSV
    implementation detail.
  - Added the practical interpretation that shared move-name rows have the same
    captured frame/gauge/cancel fields except for 16 damage differences.
  - Added a damage-difference table and clarified that `input_raw_display`
    remains raw DOM-token output, not normalized command notation.

## [2026-05-26] query | JP Modern vs Classic frame-data counts and inputs
- 質問:
  - JPのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- 読み込み:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/jp.md`
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
- 作成:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - Classic has 69 official derived frame-data rows and Modern has 65.
  - Modern has no unique move-name rows compared with Classic; Classic-only
    rows are standing LK, crouching MP, crouching HK, and Heavy Stribog.
  - Of 65 shared move names, 62 have different raw input displays and 3
    movement/system rows have identical raw input displays.
- 未解決事項:
  - 今後の比較で `input_raw_display` を conventional command notation に正規化するか、raw DOM-token display だけを比較し続けるか。

## [2026-05-26] ingest | Capcom official JP frame data
- 原本:
  - `raw/official/frame-data/2026-05-26/jp/manifest.json`
  - `raw/official/frame-data/2026-05-26/jp/classic/`
  - `raw/official/frame-data/2026-05-26/jp/modern/`
- 派生 output:
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
  - `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/jp/modern.field-meanings.json`
- ツール:
  - Added `pyproject.toml` and `uv.lock` for Scrapling-based capture tooling.
  - Added `tools/capture_capcom_frame_data.py`.
  - Added `tools/extract_capcom_frame_data.py`.
  - Fixed capture URL handling so `--source-url` is derived from
    `--character-slug` unless explicitly provided, and explicit URLs must match
    the slug.
- 作成:
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/jp.md`
  - `wiki/reviews/2026-05-26-official-jp-frame-data-capture-review.md`
- 更新:
  - `README.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/index.md`
  - `wiki/log.md`
- レビュー:
  - 人間レビューで raw snapshot と派生 output を wiki ingest 対象として accepted にした。
  - Classic data row count は 69、Modern data row count は 65。
  - `*.field-meanings.json` stores table-header help text separately from row
    CSVs.
- メモ:
  - 公式 raw 取得データは `raw/official/` 配下の dated snapshot として保持する。
  - `wiki/outputs/data/` 配下の安定した派生 CSV path は、将来の update diff をレビューしやすくするために使う。
- 未解決事項:
  - 次の公式取得で全 character を対象にするか、pipeline 検証のためにまず 1 character を追加するか。
  - raw input token から normalized command notation を後で生成するか。
  - 将来の frame-data change を説明するため、どの公式 update-history source を ingest するか。

## [2026-05-26] lint | Initial wiki health check
- 確認:
  - broken wikilinks
  - pages missing from `wiki/index.md`
  - missing frontmatter
  - duplicate pages
  - contradictions
  - stale claims
  - uncited claims
  - missing concepts
  - data gaps
- 作成:
  - `wiki/reviews/2026-05-26-health-check.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 所見:
  - No broken wikilinks, missing index entries, or missing frontmatter were
    found.
  - Open knowledge gaps remain around official Capcom terminology sources,
    malformed notation-table capture quality, and community-source confidence
    policy.

## [2026-05-26] query-review | Refine juggle explanation
- 更新:
  - `wiki/questions/how-juggles-work-internally.md`
  - `wiki/log.md`
- メモ:
  - Weakened wording from direct hit/whiff language to whether the hit is
    allowed by the juggle rules.
  - Clarified that spacing, timing, hitboxes, and hurtboxes still matter.
  - Clarified that official terminology sources have not yet been independently
    ingested or cited by this wiki page.

## [2026-05-26] query | How juggles work internally
- 質問:
  - `ジャグルって内部的にどういう仕組みで発生するんですか？`
- 読み込み:
  - `wiki/index.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/sources/supercombo-street-fighter-6-glossary.md`
  - `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md`
- 作成:
  - `wiki/questions/how-juggles-work-internally.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Filed the answer back into the wiki because it is likely to be reusable.
  - Answer is limited to the currently ingested SuperCombo Wiki glossary source.
- 未解決事項:
  - Ingest an official source later to compare official Combo Count terminology
    against community juggle terminology.

## [2026-05-26] ingest | Street Fighter 6/Glossary
- 原本:
  - `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md`
- 作成:
  - `wiki/sources/supercombo-street-fighter-6-glossary.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- メモ:
  - Obsidian Web Clipper output を exact raw source copy として保存した。
  - wiki compilation 開始前に、raw source checksum が Downloads の元ファイルと一致することを確認した。
  - source page footer には 2026-01-31 11:22 に last edited とある。source freshness と wiki creation date を混同しないよう記録した。
  - SuperCombo Wiki は medium confidence の community wiki source として扱った。
- 未解決事項:
  - SuperCombo Wiki に標準 source confidence policy を設定するか。
  - malformed numpad-direction table を source から再取得するか。
  - terminology comparison のため、次にどの公式 source を ingest するか。

## [2026-05-26] schema | Initialize LLM Wiki scaffold
- 作成:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `README.md`
  - `raw/`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/templates/`
- メモ:
  - Initialized the domain-independent raw/wiki/schema structure.
  - No raw sources have been ingested yet.
