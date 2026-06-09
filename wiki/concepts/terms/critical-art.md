---
type: concept
concept_type: term
title: "クリティカルアーツ"
created: 2026-06-10
updated: 2026-06-10
status: active
confidence: medium
sources:
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/terms/super-art]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Critical Art"
  - "CA"
  - "クリティカルアーツ"
  - "CA variant"
tags:
  - sf6
  - terms
  - frame-data
---

# クリティカルアーツ

## 要約

クリティカルアーツは、公式 frame-data 上で `CA` として Super Art とは別 row / variant になることがある強化版の arts。現時点のこの wiki では、Zangief の `SA3 ボリショイストームバスター` と `CA ボリショイストームバスター` の分離が明示的な根拠になっている。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-zangief-frame-data]] | Zangief 公式 frame-data は `SA3 ボリショイストームバスター` と、体力25%以下条件の `CA ボリショイストームバスター` を別 row として保持している。 | high |
| [[sources/supercombo-zangief-frame-data]] | Zangief の 720 input には SA3 / CA variant があり、公式 Classic との照合では `move_id` で分けて扱う。 | medium |
| [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] | `SA3 ボリショイストームバスター` と `CA ボリショイストームバスター` は separate variant として human review accepted。 | high |

## 意味差分

- この page は、現時点では `CA` の一般公式定義ではなく、frame-data / crosswalk 上の variant handling を主に説明する。
- 全 character の Critical Art 条件と Super Art との差分を一般化するには、公式 manual / frame-data の横断確認が必要。

## 関連

- [[concepts/terms/super-art]]
- [[concepts/frame-data]]
