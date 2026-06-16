---
type: review
review_type: refactor_plan
status: open
created: 2026-06-16
updated: 2026-06-16
severity: P2
confidence: medium
related:
  - "[[syntheses/battle-change-version-timeline]]"
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
sources:
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
tags:
  - sf6
  - review
  - refactor-plan
  - battle-change
  - patch-notes
  - synthesis
---

# Battle Change / SuperCombo Patch Notes version timeline refactor plan

## Summary

この refactor plan は、Capcom 公式 Battle Change List と SuperCombo Patch Notes の version 対応、authority、freshness、derived index の使い分けを、将来の `wiki/syntheses/battle-change-version-timeline.md` として安全に compile するための計画である。

今回の計画では actual synthesis page は作らない。公式 source fact、community source fact、derived fact、synthesis / inference を分け、official-only update、launch row、SuperCombo detail の昇格粒度を人間レビュー項目として残す。

## Current problem

- 公式 Battle Change source と SuperCombo Patch Notes source はそれぞれ source page と derived JSON を持つが、version timeline と authority model はまだ単一 synthesis にまとまっていない。
- patch / version query では、毎回 [[sources/capcom-official-battle-change-list]]、[[sources/supercombo-street-fighter-6-patch-notes]]、`wiki/outputs/data/battle-change/official/`、`wiki/outputs/data/battle-change/supercombo-patch-notes/` を読み直す必要がある。
- official / community authority と freshness の境界は source page に書かれているが、query recipe として再利用しやすい形にはまだ昇格していない。
- SuperCombo detail は community detail / terminology source として有用だが、Capcom 公式 change text と同格に扱うと source authority を誤る。
- official-only 4 update と SuperCombo launch row 1 件の扱いは、timeline synthesis の構造判断に関わる。

## Evidence map

| Evidence | Path/Page | What it supports | Authority | Notes |
|---|---|---|---|---|
| official Battle Change source page | [[sources/capcom-official-battle-change-list]] | Capcom 公式 Battle Change List の raw entrypoint、20 version、1820 change rows、official source key と `character_slug` の分離 | official source page | `raw_path` は `raw/battle-change/official/manifest.json`。公式本文は raw HTML / Next.js data JSON と derived rows に戻す。 |
| official Battle Change derived versions | `wiki/outputs/data/battle-change/official/versions.json` | official versions = 20 | derived fact | `jq -r '.row_count'` で確認。 |
| official Battle Change derived events | `wiki/outputs/data/battle-change/official/change-events.json` | official change events = 1820 | derived fact | 検索補助 index。結論の根拠は公式本文と source page に戻す。 |
| official Battle Change move index | `wiki/outputs/data/battle-change/official/move-change-index.json` | official move-index rows = 1419 | derived fact | combo / frame-data query の原因候補探索に使う。 |
| SuperCombo Patch Notes source page | [[sources/supercombo-street-fighter-6-patch-notes]] | 17 version detail pages、root/detail freshness 分離、community detail source の扱い | community source page | Capcom 公式 source を上書きしない。 |
| SuperCombo Patch Notes derived versions | `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` | SuperCombo versions = 17、launch row `1.00` | derived fact | `1.00` は official `battle_change` id を持たず、`official_patch_link` は launch site link。 |
| SuperCombo Patch Notes derived events | `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json` | SuperCombo community events = 1374 | derived fact / community index | detail page の top-level bullet と nested explanation を保持する community event index。 |
| SuperCombo Patch Notes move index | `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json` | SuperCombo targets = 1118 | derived fact / community index | combo / juggle / blockstring の community background を探す補助 source。 |
| official crosswalk | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json` | matched versions = 16、launch row = 1、official-only updates = 4 | derived fact | official-only ids は `20230808`, `20250901`, `20251022`, `20251113`。 |
| capture review for official source | [[reviews/2026-06-07-official-battle-change-capture-review]] | official capture validation、version summary、source-side title mismatch caution | review evidence | status は open。人間レビュー未完了。 |
| capture review for SuperCombo Patch Notes | [[reviews/2026-06-11-supercombo-patch-notes-web-page-capture-review]] | SuperCombo 17 detail validations、16 matched / 1 launch / 4 official-only summary | review evidence | status は open。official-only update と launch row の扱いが人間レビュー項目。 |
| frame-data concept | [[concepts/frame-data]] | current value query では frame-data output を優先し、Battle Change / Patch Notes は version/update explanation source として扱う方針 | compiled concept | synthesis では current value と historical change explanation を分ける必要がある。 |
| Street Fighter 6 entity | [[entities/street-fighter-6]] | game-level timeline and source-family overview | compiled entity | 既に年表が長く、version-specific synthesis へ分離する価値がある。 |

## Known counts and scope

| Item | Count / Value | Evidence |
|---|---:|---|
| official versions | 20 | `wiki/outputs/data/battle-change/official/versions.json`; `jq -r '.row_count'` |
| official events | 1820 | `wiki/outputs/data/battle-change/official/change-events.json`; `jq -r '.row_count'` |
| official move-index rows | 1419 | `wiki/outputs/data/battle-change/official/move-change-index.json`; `jq -r '.row_count'` |
| SuperCombo versions | 17 | `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`; `jq -r '.row_count'` |
| SuperCombo events | 1374 | `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json`; `jq -r '.row_count'` |
| SuperCombo targets | 1118 | `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json`; `jq -r '.row_count'` |
| matched versions | 16 | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`; `.summary.matched_count` |
| launch row | 1 | `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`; row `version == "1.00"` |
| official-only updates | 4 | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`; `.official_unmatched_ids` |

## Proposed synthesis page

将来作る候補:

`wiki/syntheses/battle-change-version-timeline.md`

推奨 section:

- `Overview`: official Battle Change と SuperCombo Patch Notes をなぜ同じ timeline synthesis で扱うか。
- `Authority model`: Capcom official、SuperCombo community、derived index、review note の優先順位。
- `Version timeline`: official 20 version と SuperCombo 17 version / launch row の対応。
- `Official vs SuperCombo mapping`: 16 matched、1 launch、4 official-only update の扱い。
- `Freshness rules`: official capture date、SuperCombo root `source_updated_at`、detail `latest_detail_source_updated_at`、raw captured time を混同しない方針。
- `Derived outputs`: `changes.json`、`change-events.json`、`move-change-index.json`、crosswalk の用途と限界。
- `Query recipes`: current value query、historical update explanation、combo / frame-data change cause search の読み順。
- `Open questions`: official-only update、launch row、community detail 昇格粒度、derived output freshness 確認。

## Proposed wiki changes

| Change | Target | Why | Risk | Apply now? |
|---|---|---|---|---|
| refactor plan review note を作る | `wiki/reviews/2026-06-16-battle-change-version-timeline-refactor-plan.md` | synthesis 前に authority / scope / human-review items を固定する | 低い。事実値や source authority は変更しない | yes |
| synthesis draft を作る | `wiki/syntheses/battle-change-version-timeline.md` | repeated patch/version query の入口にする | medium。community detail と official fact の混同リスク | later |
| index に synthesis を追加する | `wiki/index.md` | future query の navigation surface にする | synthesis がない状態で追加すると孤立する | later |
| frame-data concept から synthesis へ related link を追加する | [[concepts/frame-data]] | Battle Change / Patch Notes の version query を概念ページから辿れるようにする | medium。既存 concept がさらに重くなる | later |
| Street Fighter 6 entity の年表を薄くし、version detail を synthesis へ逃がす | [[entities/street-fighter-6]] | game entity の過密化を避ける | medium。大きめ構造変更 | later |
| review dashboard へこの plan を載せる | future `wiki/reviews/...` dashboard | open refactor plan を追跡する | dashboard がまだない | later |

## Human review needed

- official-only 4 update (`20230808`, `20250901`, `20251022`, `20251113`) を timeline でどう扱うか。現時点では SuperCombo Patch Notes table に直接 link がない official update として保持し、SuperCombo 側にない理由は推測しない。
- launch row `1.00` を timeline に含めるか。現時点では SuperCombo launch version として保持し、official Battle Change row との 1:1 対応は持たないと書く。
- SuperCombo detail をどの粒度で synthesis に入れるか。全 detail event を複製せず、timeline / authority / query recipe に必要な範囲だけ要約するのが候補。
- community detail を official source と同格に誤読しないため、表では `authority` column を必ず持たせる。
- derived output の freshness 確認方法。`raw/` 再取得や derived 再生成はこの plan では行わず、source page / validation / manifest へ戻る方針だけ書く。
- official `text_html` を Markdown / plain text に変換するタイミング。現時点では raw-derived field を置き換えず、reader-facing synthesis で必要な要約だけを書く。

## Safe next step

1. この review plan を人間が確認する。
2. `wiki/syntheses/battle-change-version-timeline.md` を draft 作成する。
3. draft では official / community / derived authority を分け、official-only 4 update と launch row を未解決扱いで残す。
4. `wiki/index.md` に synthesis 入口を追加する。
5. patch/version query で使う authority rules を、1 件の scoped query で検証する。

## Not doing in this plan

- source authority 変更なし。
- `raw/` 更新なし。
- derived output 再生成なし。
- actual synthesis 作成なし。
- page merge / split / rename / directory move なし。
- frame 値、patch fact、validation status の変更なし。
- SuperCombo community detail を official fact へ昇格しない。
