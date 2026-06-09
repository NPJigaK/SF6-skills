---
type: review
review_type: capture_validation
title: "Capcom Fighting Ground Battle System scoped capture review"
created: 2026-06-10
status: open
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
raw_paths:
  - "raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json"
tags:
  - sf6
  - official
  - web-page-capture
  - capture-validation
  - scoped-capture
aliases:
  - "Fighting Ground Battle System capture review"
  - "公式 Fighting Ground Battle System 取得レビュー"
---

# Capcom Fighting Ground Battle System scoped capture review - 2026-06-10

## 要約

Capcom 公式 `Fighting Ground` ページから、Battle System に関係する section だけを `raw/web-pages/` 配下の scoped Web page capture として保存した。全文 HTML、full Next.js data JSON、page chunk JS は保存せず、source provenance には response metadata と hash だけを残した。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json` |
| Source URL | `https://www.streetfighter.com/6/ja-jp/mode/fightingground` |
| Source type | `official_scoped_web_page_capture` |
| Scope policy | `fightingground_battle_system_only` |
| Next.js build ID | `8PI3Oj_9ikUinAmp3j_yf` |
| Captured at | `2026-06-09T17:13:40Z` |
| Canonical raw 取得物 | `api/source-text.scoped.json`, `rendered/*.dom.json` |
| Display evidence | `screenshots/*.png` |
| Downloaded assets | 14 |
| Omitted asset refs | 3 |

## 保存した範囲

- `BATTLE SYSTEM DESIGN`
- `DRIVE GAUGE`
- `COMMON SYSTEM`
- `simpleOperationImage` modal

## 意図的に保存しなかった範囲

- `SOUND ACCESSIBILITY`
- `CHARACTER DAMAGE`
- `Real Time Commentary`
- `CONTROL TYPE`
- `BATTLE CONTENTS`

## Validation

`validation.json` は `passed`。主な確認内容は以下。

- full page HTML、full Next.js data JSON、page chunk JS を保存していない。
- 期待した 34 件の scoped text key がすべて存在する。
- section DOM と modal DOM が存在し、期待 text を含む。
- `simpleOperationImage` modal は 6 item と `game_screen.jpg` を含む。
- 4 枚の screenshot が存在し、asset download はすべて status 200。
- 既知の除外 asset family は downloaded assets に含まれない。

## 判断

自動 validation は passed。人間レビューでは、scoped capture の範囲が質問回答用途として十分か、`COMMON SYSTEM` のスライダー DOM を raw として使う運用でよいかを確認する必要がある。除外 section の本文や画像は raw に保存していないため、この source は Fighting Ground 全体の根拠ではなく Battle System 範囲の根拠として扱う。

## 未解決事項

- Web page capture で scoped raw を作る場合、除外 section 名を manifest policy に残すだけで十分か。
- `COMMON SYSTEM` の command icon refs を binary asset として保存しない運用でよいか。
