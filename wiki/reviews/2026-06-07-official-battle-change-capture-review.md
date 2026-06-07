---
type: review
review_type: capture_validation
created: 2026-06-07
status: open
sources:
  - "[[sources/capcom-official-battle-change-list]]"
related:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Battle Change capture review"
tags:
  - review
  - battle-change
  - official
---

# 公式 Battle Change List capture review - 2026-06-07

## 要約

Capcom 公式 Buckler's Boot Camp の Battle Change List を 20 update version 分 capture した。raw は `raw/battle-change/official/`、派生 output は `wiki/outputs/data/battle-change/official/` にある。自動 validation は通過しているが、人間レビューは未実施なので status は open のままにする。

## Capture 対象

| 項目 | 値 |
|---|---|
| Source URL | `https://www.streetfighter.com/6/buckler/ja-jp/battle_change` |
| Build ID | `JRgr9jaW-XektPBHKodsS` |
| Current version | `20260528` |
| Version count | 20 |
| Raw manifest | `raw/battle-change/official/manifest.json` |
| Derived output | `wiki/outputs/data/battle-change/official/` |

## 自動検証

- `tools/capture_capcom_battle_change.py --dry-run` で discovery page から 20 version を列挙した。
- `tools/capture_capcom_battle_change.py` で discovery と 20 version の `page.html` / `data.json` / `metadata.json` を保存した。
- `tools/validate_capcom_battle_change.py` は各 capture について以下を検証した。
  - metadata の artifact `byte_count` / `sha256` が実ファイルと一致する。
  - HTML 内 `__NEXT_DATA__.props.pageProps.adjust` と `_next/data` JSON の `pageProps.adjust` が一致する。
  - `adjust.current_version` が version URL の ID と一致する。
  - `adjust.versions` は 20 件で、manifest の capture order と一致する。
- `tools/extract_capcom_battle_change.py` は raw JSON から `changes.json`、`changes.json`、`versions.json`、`schema.json` を生成した。
- 派生 output は、各 version page の title を `version_title`、discovery page の selector 表記を `version_selector_title` として別列に保持し、差がある場合は `version_title_mismatch` を `true` にする。

## 集計

| Metric | Count |
|---|---:|
| Versions | 20 |
| Policy rows | 123 |
| Common change rows | 100 |
| Fighter change rows | 1597 |
| Total derived change rows | 1820 |

## Version 別 summary

| Version | Title | Policy | Common changes | Fighters | Fighter details | Fighter changes |
|---|---|---:|---:|---:|---:|---:|
| `20260528` | 2026.05.28 update | 1 | 5 | 14 | 18 | 18 |
| `20260415` | 2026.04.15 update | 0 | 3 | 2 | 3 | 3 |
| `20260317` | 2026.03.17 update | 29 | 4 | 28 | 149 | 149 |
| `20251216` | 2025.12.16 update | 4 | 4 | 9 | 33 | 33 |
| `20251113` | 2025.11.13 update | 0 | 2 | 1 | 2 | 2 |
| `20251022` | 2025.10.22 update | 0 | 1 | 4 | 4 | 4 |
| `20251015` | 2025.10.15 update | 0 | 4 | 13 | 18 | 18 |
| `20250901` | 2025.09.01 update | 0 | 0 | 3 | 5 | 5 |
| `20250805` | 2025.08.05 update | 0 | 0 | 17 | 24 | 24 |
| `202506` | 202506 Ver. | 26 | 15 | 25 | 339 | 339 |
| `20250205` | 2025.02.05 update | 0 | 4 | 12 | 13 | 13 |
| `20241202` | 2024.12.02 update | 25 | 5 | 24 | 166 | 167 |
| `20240924` | 2024.09.24 update | 12 | 6 | 20 | 63 | 63 |
| `20240626` | 2024.06.26 update | 0 | 5 | 15 | 28 | 28 |
| `202405` | 202405 Ver. | 22 | 14 | 21 | 464 | 481 |
| `20240227` | 2024.02.27 update | 4 | 6 | 13 | 43 | 43 |
| `20231201` | 2023.12.1 update | 0 | 4 | 13 | 35 | 35 |
| `20230927` | 2023.09.27 update | 0 | 11 | 19 | 132 | 132 |
| `20230808` | 2023.08.08 update | 0 | 1 | 3 | 5 | 5 |
| `20230724` | 2023.07.24 update | 0 | 6 | 15 | 35 | 35 |

## 注意点

- `changes.json` の `text_html` は公式 HTML fragment を保持する。これは raw 由来の派生列であり、翻訳・要約・正規化した source replacement ではない。
- `20231201` は `version_title` が `2023.12.1 update`、`version_selector_title` が `2023.12.01 update`。公式 source 内の表記差として保持し、`version_title_mismatch: true` で後続の LLM が判別できるようにしている。
- `_next/data` endpoint は Next.js build ID を含むため、将来の再取得では build ID が変わる可能性がある。capture tool は discovery HTML から build ID を再取得する。
- sitemap では過去 version URL が列挙されないため、discovery は公式 page の `adjust.versions` を使う。

## 最終判断

自動 validation は passed。人間レビューでは、代表 version の表示と `text_html` の扱い、20 version の coverage が意図通りかを確認する必要がある。
