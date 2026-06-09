---
type: source
source_type: official_scoped_web_page_capture
title: "Capcom 公式 Fighting Ground Battle System"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/mode/fightingground"
created: 2026-06-10
updated: 2026-06-10
captured_at_utc: "2026-06-09T17:13:40Z"
status: active
confidence: high
tags:
  - sf6
  - official
  - battle-system
  - drive-system
  - web-page-capture
  - scoped-capture
aliases:
  - "Fighting Ground Battle System"
  - "ファイティンググラウンド バトルシステム"
  - "SF6 Battle System Design"
related_concepts:
  - "[[concepts/drive-system]]"
related_entities:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
---

# ソース: Capcom 公式 Fighting Ground Battle System

## 1行要約

Capcom 公式 Street Fighter 6 Fighting Ground ページから、強くなるための質問回答で使う Battle System 範囲だけを scoped raw として保存した source page。

## 重要ポイント

1. Raw entrypoint は `raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json`。
2. 保存対象は `BATTLE SYSTEM DESIGN`、`DRIVE GAUGE`、`COMMON SYSTEM`、クリックで開く `simpleOperationImage` modal。
3. 除外対象は `SOUND ACCESSIBILITY`、`CHARACTER DAMAGE`、`Real Time Commentary`、`CONTROL TYPE`、`BATTLE CONTENTS`。全文 HTML、full Next.js data JSON、page chunk JS は保存せず、hash と response metadata だけを provenance に残した。
4. Canonical raw は `api/source-text.scoped.json` と `rendered/*.dom.json`。表示証拠として section と modal の screenshot、必要な画像 asset を保存している。
5. Next.js build ID は `8PI3Oj_9ikUinAmp3j_yf`。source の公開更新日時は未取得なので、`captured_at_utc` と build ID を由来情報として扱う。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| この raw capture は Fighting Ground 全体ではなく Battle System 範囲だけを保存する。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json` | high | `scope_policy.id` は `fightingground_battle_system_only`。 |
| Drive Gauge はバトル開始時から使用可能で、使いすぎると枯渇状態に陥る。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/api/source-text.scoped.json`; `rendered/drive-gauge.dom.json` | high | 公式ページの `driveGauge__text` に由来する。 |
| Drive Gauge が 0 になるとバーンアウト状態になり、回復するまで Drive System を利用する技は一時的に使用できなくなる。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/api/source-text.scoped.json`; `rendered/simple-operation-modal.dom.json` | high | modal の `ドライブゲージ` 説明。 |
| Drive Rush は Drive Parry の構え、またはキャンセル可能な通常技から出せる。Drive Parry からはコスト 1、通常技からはコスト 3。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/api/source-text.scoped.json`; `rendered/common-system.dom.json` | high | `driverush__text` / `driverush__attention` に由来する。 |
| Drive Impact、Drive Parry、Overdrive、Drive Reversal は Common System として説明されている。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/rendered/common-system.dom.json`; `screenshots/common-system.png` | high | スライダー形式なので `text` だけでなく `outer_html` も確認する。 |
| `simpleOperationImage` modal は `game_screen.jpg` と 6 つの UI 説明を含む。 | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/rendered/simple-operation-modal.dom.json`; `assets/images/mode/fg/game_screen.jpg` | high | screenshot は `screenshots/simple-operation-modal.png`。 |

## 関連概念

- [[concepts/drive-system]]

## 関連エンティティ

- [[entities/capcom]]
- [[entities/street-fighter-6]]

## 既存 wiki との矛盾または更新

- [[concepts/drive-system]] はこれまで SuperCombo glossary を主な根拠としていたが、この source により Drive Gauge、Drive Rush cost、Burnout 周辺の公式説明を参照できるようになった。
- SuperCombo glossary は community terms の補助 source として残す。公式 source と community source の用語差が出た場合は、公式 source を優先して差異を明示する。
- raw は scoped であり、Fighting Ground ページ全体の説明ではない。除外 section の本文や画像を根拠にした質問回答は、この source からは行わない。

## 未解決の質問

- 公式 Fighting Ground ページの他 section を今後も raw 化しない方針でよいか。
- Drive System の詳細な frame / gauge recovery / burnout duration などを、どの公式 source または frame-data-derived source で補うか。

## ソースメモ

- Raw manifest: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json`
- Scoped text: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/api/source-text.scoped.json`
- Rendered DOM: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/rendered/`
- Screenshots: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/screenshots/`
- Asset manifest: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/assets/manifest.json`
- Source provenance: `raw/web-pages/www.streetfighter.com/fightingground-battle-system/source-provenance.json`
- Capture review: [[reviews/2026-06-10-capcom-fightingground-battle-system-capture-review]]
