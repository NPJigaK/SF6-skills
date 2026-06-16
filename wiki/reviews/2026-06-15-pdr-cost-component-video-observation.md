---
type: review
review_type: mechanics_evidence_review
title: "PDR cost component video observation"
created: 2026-06-15
updated: 2026-06-15
status: active
confidence: medium
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/raw-drive-rush]]"
tags:
  - sf6
  - review
  - drive-system
  - raw-drive-rush
---

# PDR cost component video observation

## Summary

Drive Rush from Parry の cost は、Capcom 公式の `1` と SuperCombo の cost table `1/2` を矛盾として扱わず、Drive Parry activation `0.5` + Drive Rush from Parry transition `0.5` = 最小総消費 `1.0` として扱う。

## Evidence

| 種別 | 内容 | 根拠 |
|---|---|---|
| source fact | Capcom 公式 source は Drive Parry から出す Drive Rush を cost `1`、通常技 cancel 版を cost `3` と説明する。 | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]] |
| source fact | SuperCombo Gauges は Drive Parry activation を `5000` Drive on frame `2`、hold drain を frame `4` から `50` Drive/frame と説明する。 | [[sources/supercombo-street-fighter-6-gauges]] |
| source fact | SuperCombo Gauges の cost table は Drive Rush from Parry を `1/2` Drive Stock 相当として示し、Drive Rush section / caption は Parry からの Drive Rush を `1 Drive Stock` と説明する。 | `raw/web-pages/wiki.supercombo.gg/gauges/page.raw.wikitext`; `wiki/outputs/data/gauges/supercombo/numeric-tables.json` |
| user lab observation | ユーザー提供の実機動画確認では、`0.5` 本以上で Drive Rush が出てから Burnout する例と、`0.5` 本未満では Drive Rush へ進まず Burnout する例が確認された。 | 会話内のユーザー検証報告。raw 動画は repo 永続 source としては保持しない方針。 |

## Interpretation

SuperCombo の cost table `1/2` は、Drive Parry activation とは別に Drive Rush from Parry transition で払う component と読む。Capcom 公式の `1` は、Drive Parry activation `0.5` と transition `0.5` を足した最小総消費として読む。この解釈は、`0.5` 本未満では initial Parry cost を払った時点で Burnout して Drive Rush へ進めないという SuperCombo の説明、およびユーザー実機検証の観察と整合する。

## 未解決事項

- frame `4` 到達時に Drive Rush cancel と hold drain が同一 frame でどう解決されるか。
- 特定の入力履歴から transition 前 hold drain が何 frame 分乗ったかを、動画だけでどこまで確定できるか。
- 入力履歴だけで Burnout / no-Burnout を完全分類できるとは扱わない。
