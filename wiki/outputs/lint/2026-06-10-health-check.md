---
type: output
output_type: lint_report
title: "Wiki Health Check - 2026-06-10"
created: 2026-06-10
updated: 2026-06-10
status: active
confidence: medium
sources:
  - "[[index]]"
  - "[[log]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/index]]"
  - "[[syntheses/frame-data-raw-layout]]"
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
tags:
  - lint
  - health-check
  - review-needed
---

# Wiki Health Check - 2026-06-10

## Scope

この health check は `wiki/` 全体の Markdown graph、frontmatter、index coverage、raw/source traceability、derived JSON、raw validation status、既存 review queue を対象にした。`raw/` の再取得や原文・元データの事実修正は行っていない。ユーザー承認後の follow-up として raw manifest status 同期のみ行った。日付は Asia/Tokyo の 2026-06-10 を使う。

確認した主な material:

- `wiki/index.md`、`wiki/log.md` 最近エントリ。
- Markdown 160 files、うち non-template page 149 files。
- `wiki/outputs/**/*.json` 363 files。
- `raw/**/validation.json` 33 files。
- 公式 frame-data 30 character slugs の source page row count と派生 JSON row count。
- 補助確認として、公式 Web の [05.28.2026 Battle Change List](https://www.streetfighter.com/6/buckler/battle_change) と [2026-05-28 update notice](https://www.streetfighter.com/6/buckler/information/detail/update20260528) を quick web search した。

## Executive Summary

- Current source / concept / entity / output の主要な row count と validation には直接の不一致は見つからなかった。
- Ryu / Chun-Li / Zangief の raw manifest `raw_review_status` は、ユーザー確認後に既存 accepted review と同期済み。
- 個別 term page は 36 件になり、`wiki/index.md` の direct rows と [[concepts/terms/index]] の詳細 index の両方から到達できる。
- Question pages の thin backlink は、関連 character entity と主要 term / concept を frontmatter `related:` に追加して軽減した。本文リンクは自然に出る重要語だけに留める運用にした。
- SuperCombo enriched output は 30キャラ分あるが、`enriched_review_required` 1295 行、SuperCombo-only 620 行が残る。これは既存方針どおり未確定扱いで、勝手に直さない。

## 機械チェック結果

| 項目 | 結果 | メモ |
|---|---:|---|
| Markdown files | 160 | templates を含む |
| Non-template pages | 149 | `index.md` / `log.md` を除く |
| Missing frontmatter | 0 | templates を除外 |
| Broken wikilinks | 0 real pages / 5 template placeholders | `templates/*.md` の placeholder 表記など |
| Missing direct index entries | 0 | 個別 term pages も direct row を追加済み |
| Orphan-like pages excluding `index.md` / `log.md` inbound | 1 | この health-check output 自体 |
| JSON parse errors | 0 / 363 | `wiki/outputs/**/*.json` |
| Raw validation failures | 0 / 33 | すべて `passed` |
| Official source row-count mismatches | 0 / 30 | source page と official JSON が一致 |
| Open review pages | 13 | capture review / prereview / old health check |

## 矛盾

### resolved: accepted review と raw manifest status の同期

以下は wiki review/source page の人間レビュー済み accepted と、raw manifest の `raw_review_status` が同期済み。

| Character | Wiki evidence | Raw manifest status |
|---|---|---|
| JP | [[reviews/2026-05-26-official-jp-frame-data-capture-review]], [[sources/capcom-official-jp-frame-data]] | `raw/frame-data/official/jp/manifest.json`: `human_reviewed_accepted` |
| Ryu | [[reviews/2026-05-27-official-ryu-frame-data-capture-review]], [[sources/capcom-official-ryu-frame-data]] | `raw/frame-data/official/ryu/manifest.json`: `human_reviewed_accepted` |
| Chun-Li | [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]], [[sources/capcom-official-chun-li-frame-data]] | `raw/frame-data/official/chunli/manifest.json`: `human_reviewed_accepted` |
| Zangief | [[reviews/2026-05-27-official-zangief-frame-data-capture-review]], [[sources/capcom-official-zangief-frame-data]] | `raw/frame-data/official/zangief/manifest.json`: `human_reviewed_accepted` |

Ryu / Chun-Li / Zangief の manifest は、ユーザー確認後に `raw_review_status` だけを更新した。raw source text、DOM、screenshot、derived JSON は変更していない。

### 問題なし: row count / JSON validation

公式 30 character source pages の Classic / Modern row count は、`wiki/outputs/data/frame-data/official/<slug>/{classic,modern}.json` の `row_count` と一致した。`wiki/outputs` の JSON parse error もなかった。

## 古い主張

### resolved-with-note: historical review に旧 raw path が残る

現在の入口は `raw/frame-data/official/<slug>/` と `raw/frame-data/supercombo/<slug>/` の latest mirror fixed path だが、古い review/log には `raw/official/frame-data/<date>/...` と `raw/supercombo/frame-data/<date>/...` が残る。

該当例:

- [[reviews/2026-05-26-official-jp-frame-data-capture-review]]
- [[reviews/2026-05-27-official-ryu-frame-data-capture-review]]
- [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]]
- [[reviews/2026-05-27-official-zangief-frame-data-capture-review]]
- [[reviews/2026-05-30-official-frame-data-roster-capture-review]]
- [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]]
- [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]]
- [[log]]

`[[syntheses/frame-data-raw-layout]]` は「新しい ingest や query では旧 path を使わない」と明記しているので、現在ページの説明としては矛盾しない。follow-up では review page の履歴 path は書き換えず、各 review page に「この raw path は当時の履歴であり、現在入口は latest mirror」と短い注記を足した。`[[log]]` は時系列記録なので履歴文書として残す。

### stale-risk: official / community page freshness

Quick web search では公式 Battle Change List の入口が 2026-05-28 update を示しており、この wiki の `raw/battle-change/official/` と一致する。ただしこれは再取得ではない。今後の公式 patch / SuperCombo revision は変わり得るため、次回 health check では web search ではなく capture script / MediaWiki API / official page fetch で freshness を確認する。

## 出典不足

現行の major concept / entity / question / report pages には source page か raw/output path への根拠がある。heuristic では、重要主張が明らかに無出典の current page は見つからなかった。

注意点:

- `sources/*.md` は source page なので frontmatter `sources:` ではなく `raw_path:` / `original_url:` を使っている。これは出典不足ではない。
- Term pages は 36 件になり、[[sources/capcom-esports-base-terms]]、[[sources/capcom-official-fightingground-battle-system]]、[[sources/supercombo-street-fighter-6-glossary]]、個別 frame-data source の claim を分けて保持する。SuperCombo glossary 由来の補足は community source として medium confidence のまま扱う。
- Individual frame-data row の値は raw / JSON に置き、durable question / synthesis が必要になった時だけ昇格する方針は維持されている。

## 孤立ページ

`wiki/index.md` / `wiki/log.md` からの inbound を除くと、この report 自体以外の orphan-like page は解消済み。follow-up では関連 character entities から question pages へ戻る link を追加し、主要 combo / frame-data question pages の frontmatter `related:` に term pages を追加した。`field_conflict` prereview は [[concepts/frame-data]] から明示リンクした。

## 重複 Concept

Exact duplicate concept title / aliases は見つからなかった。

近接しているが意図的に分離されているもの:

- [[concepts/frame-data]] と [[concepts/terms/frame-advantage]]: 前者は structured data / schema / capture policy、後者は用語。
- [[concepts/drive-system]] と [[concepts/terms/raw-drive-rush]] / [[concepts/terms/drive-impact-counter]] / [[concepts/terms/perfect-parry]]: 前者は system、後者は観戦用語。
- [[concepts/juggle-system]] と [[concepts/terms/scaling-reset]] / [[concepts/terms/setplay]]: overlap はあるが claim source が違う。

現時点では merge しない。今後 SuperCombo glossary を term pages に統合する時、meaning difference を term page 側に追記する。

## Missing Backlinks

主な missing backlink は follow-up で軽減した。

- Character entities から関連 question pages へ戻る link を追加した。
- JP combo theory pages は [[concepts/terms/drive-rush-cancel]]、[[concepts/terms/cancel]]、[[concepts/terms/frame-advantage]]、[[concepts/terms/wall-bounce]]、[[concepts/terms/damage-scaling]] などを frontmatter `related:` に持つ。
- Chun-Li frame-data question pages は [[concepts/terms/cancel]]、[[concepts/terms/drive-impact]]、[[concepts/terms/drive-rush-cancel]]、[[concepts/terms/super-art]]、[[concepts/terms/frame-advantage]]、[[concepts/terms/punish-counter]] などを frontmatter `related:` に持つ。
- 本文リンクは、回答本文に自然に出る重要語だけにする。発見性のためだけの link は frontmatter `related:` に集約する。

## Concept 化すべき頻出語

頻出しているが、まだ独立 concept / synthesis として切っていない候補。

Domain mechanics:

- 作成済み: [[concepts/terms/burnout]]、[[concepts/terms/drive-parry]]、[[concepts/terms/drive-reversal]]、[[concepts/terms/drive-impact]]、[[concepts/terms/drive-rush-cancel]]、[[concepts/terms/overdrive]]、[[concepts/terms/super-art]]、[[concepts/terms/critical-art]]、[[concepts/terms/damage-scaling]]、[[concepts/terms/wall-bounce]]、[[concepts/terms/air-reset]]、[[concepts/terms/chain]]、[[concepts/terms/cancel]]。
- `hitbox` / `hurtbox`: SuperCombo image refs と raw evidence の扱いが絡むため、source confidence policy を含む concept / term page 候補として残す。

Wiki / data workflow:

- `manifest` / `validation` / `storage_policy` / `source freshness`: [[syntheses/frame-data-raw-layout]] に近い。frame-data 以外の web-page raw にも広がるため、`raw-provenance` synthesis 候補。
- `crosswalk` / `enriched output` / `review queue` / `field_conflict`: SuperCombo official enrichment workflow の説明が増えているため、data workflow synthesis 候補。
- `imageinfo`: SuperCombo image evidence の欠損・再解決 policy として独立 review/synthesis 候補。

## Web Search で埋めるべき Data Gaps

この health check では raw 更新をしていない。次に web / official API / MediaWiki API で埋めるべき gap は以下。

1. Official Battle Change List freshness: 2026-05-28 以降の update が出ていないか、[official Battle Change List](https://www.streetfighter.com/6/buckler/battle_change) と update notice を定期確認する。
2. Official frame-data freshness: 30 character frame pages の `capture_label` / actual source update を再取得し、Battle Change List と row values が一致するか確認する。
3. SuperCombo frame-data freshness: 30 character pages の `source_updated_at` / `lastrevid` を MediaWiki API で再確認する。特に 2026-06-02 以降の Ingrid / all-character edits。
4. SuperCombo glossary freshness: page revid `351898` / 2026-01-31 以降の glossary update と `Template:ComboLegend-SF6` update を確認する。
5. Official terminology coverage: CAPCOM eSports BASE / Fighting Ground 以外の公式 manual / in-game help で `Critical Art`、`hitbox`、`hurtbox`、damage scaling 周辺の説明を補う。
6. `hitbox` / `hurtbox` evidence: SuperCombo image refs の欠損が source 側か取得側か、MediaWiki imageinfo / page assets で再解決する。
7. Scoped web capture freshness: Fighting Ground の Next.js build ID と HTTP metadata だけで source freshness を扱ってよいか、公式ページの更新日取得方法を追加確認する。

## 次に聞くべき質問

1. `hitbox` / `hurtbox` を term page 化する時、SuperCombo image refs の confidence policy と imageinfo 欠損 policy を同じ page に含めるか、別 synthesis に分けるか。
2. SuperCombo enriched review queue は、方針どおり `field_conflict` から始める場合、199 件すべてを batch review するか、既存 prereview の 11 件から拡張するか。
3. `manual_or_ambiguous_match` 161 件は、character batch ではなく ambiguity type ごとに分けるべきか。
4. Official frame-data freshness を web search ではなく再capture / validation で確認する周期をどう置くか。
5. `raw-provenance` / `review-queue` workflow synthesis を frame-data 以外の raw families に広げるか。

## Not Fixed

- 不確実な事実問題は確定扱いにしていない。
- `hitbox` / `hurtbox`、SuperCombo-only 620 行、imageinfo 欠損、official frame-data freshness は review-needed / data gap として残す。
- Web search は gap identification に使っただけで、raw capture freshness の証明としては扱わない。
