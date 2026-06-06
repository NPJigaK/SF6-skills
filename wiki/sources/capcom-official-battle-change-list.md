---
type: source
source_type: official_battle_change
title: "Capcom 公式 Battle Change List"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/battle-change/official/manifest.json"
original_url: "https://www.streetfighter.com/6/buckler/ja-jp/battle_change"
created: 2026-06-07
updated: 2026-06-07
captured_at_utc: "2026-06-06T15:22:50Z"
status: active
confidence: high
tags:
  - sf6
  - official
  - battle-change
  - patch-notes
aliases:
  - "Battle Change List"
  - "バトル変更リスト"
  - "SF6 battle change"
related_concepts:
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
---

# ソース: Capcom 公式 Battle Change List

## 1行要約

Capcom 公式 Buckler's Boot Camp の Street Fighter 6 Battle Change List を、20 update version 分の raw HTML、Next.js data JSON、metadata、manifest として保存し、wiki 化しやすい flat CSV / JSON に派生抽出した source page。

## 重要ポイント

1. raw capture は `raw/battle-change/official/` 配下の latest mirror 固定パスに保存されている。capture date は path ではなく `manifest.json` の `capture_label` / `created_at_utc` で追う。
2. discovery source は `https://www.streetfighter.com/6/buckler/ja-jp/battle_change`。このページの `adjust.versions` から 20 update version を列挙した。
3. 各 version は `page.html` と `_next/data/.../battle_change/<version>.json` 由来の `data.json` を保存する。validator は HTML 内 `__NEXT_DATA__` の `adjust` と `data.json` の `pageProps.adjust` が一致することを確認する。
4. capture 対象は 2023-07-24 update から 2026-05-28 update までの 20 version。最新 `current_version` は `20260528`。
5. 派生 output は `wiki/outputs/data/battle-change/official/` にあり、20 version / 1820 change rows を持つ。内訳は policy 123 行、common 100 行、fighter 1597 行。
6. version title は、各 version page の title を `version_title`、discovery page の version selector 表記を `version_selector_title` として別列に分ける。両者が異なる場合は `version_title_mismatch: true` で明示する。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| publisher は Capcom で、source URL は公式 Buckler's Boot Camp の Battle Change List。 | `raw/battle-change/official/manifest.json`; `raw/battle-change/official/discovery/metadata.json` | high | metadata が publisher、game、locale、source type、source URL を記録している。 |
| Battle Change List は 20 update version を列挙する。 | `raw/battle-change/official/manifest.json` | high | `versions` は `20260528` から `20230724` まで。 |
| raw capture は各 version の HTML と Next.js data JSON を保持する。 | `raw/battle-change/official/versions/<version>/page.html`; `raw/battle-change/official/versions/<version>/data.json` | high | JSON は `_next/data/<buildId>/ja-jp/battle_change/<version>.json` の response。 |
| 派生 output は 1820 change rows。 | `wiki/outputs/data/battle-change/official/changes.csv`; `wiki/outputs/data/battle-change/official/changes.json`; [[reviews/2026-06-07-official-battle-change-capture-review]] | high | `text_html` は公式 HTML fragment を保持し、翻訳・正規化した置き換えではない。 |
| `20231201` は page title と selector title が異なる。 | `wiki/outputs/data/battle-change/official/versions.csv`; `wiki/outputs/data/battle-change/official/schema.json` | high | `version_title` は `2023.12.1 update`、`version_selector_title` は `2023.12.01 update`。公式由来の表記差なので正規化せず、`version_title_mismatch` で示す。 |

## 関連概念

- [[concepts/frame-data]]

## 関連エンティティ

- [[entities/capcom]]
- [[entities/street-fighter-6]]

## 既存 wiki との矛盾または更新

- 以前の未解決事項だった「frame-data の version change を説明する公式 update-history source」は、この source capture で raw layer まで追加された。ただし個別の調整内容を character / concept page へ昇格する作業は未実施。
- Battle Change List の本文は公式 HTML fragment を含む。`wiki/outputs/data/battle-change/official/changes.csv` の `text_html` は、改行や注意書きの `<span>` を保持するため、読者向け要約では Markdown 化または plain text 化の方針を別途決める必要がある。
- version title は公式 source 内でも page title と selector title が一致しない場合がある。後続の wiki 化では `version_title_mismatch` を確認し、日付の正規化を推測で行わない。

## 未解決の質問

- 20 version 分を、version 別 source page、character 別 synthesis、または時系列 synthesis のどれへ昇格するか。
- `text_html` から plain text / Markdown / structured caution note をどの段階で派生させるか。
- capture review を人間が確認した後、`raw_review_status` を accepted に更新する運用をどうするか。

## ソースメモ

- Raw manifest: `raw/battle-change/official/manifest.json`
- Discovery raw capture: `raw/battle-change/official/discovery/`
- Version raw captures: `raw/battle-change/official/versions/<version>/`
- Derived changes CSV: `wiki/outputs/data/battle-change/official/changes.csv`
- Derived changes JSON: `wiki/outputs/data/battle-change/official/changes.json`
- Derived versions CSV: `wiki/outputs/data/battle-change/official/versions.csv`
- Derived schema: `wiki/outputs/data/battle-change/official/schema.json`
- Capture review: [[reviews/2026-06-07-official-battle-change-capture-review]]
