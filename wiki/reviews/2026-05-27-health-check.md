---
type: review
review_type: health_check
created: 2026-05-27
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/capcom-official-chun-li-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
  - "[[entities/ryu]]"
  - "[[entities/chun-li]]"
  - "[[entities/zangief]]"
aliases:
  - "2026-05-27 wiki health check"
tags:
  - review
  - health-check
---

# Wiki ヘルスチェック - 2026-05-27

## 要約

JP、Ryu、Chun-Li、Zangief の公式 frame-data captures と Classic / Modern 比較 question pages の後に実施した health check。blocking structural issue は見つからなかった。

## 人間レビュー判断

2026-05-27 に accepted。

- follow-up design work が残るため `status: open` は維持する。
- JP、Ryu、Chun-Li、Zangief の validation results をこの health check に保持する。
- command notation は当面 display-only transform とする。raw input tokens が source-preserving data。
- Classic / Modern 比較は、公式技名の完全一致を default rule とする。
- `しゃがみ強K（ビッグスタンプ）` と `ビッグスタンプ` のような pair は、勝手に normalize せず、対応しそうな name variants として注記する。

## 構造上の問題

### 壊れたリンク

non-template wiki pages では見つからなかった。`wiki/templates/` の placeholder links は意図的に除外した。

### index 未掲載ページ

この review page 追加前の既存 non-template wiki page には、`wiki/index.md` 未掲載のものはなかった。

### frontmatter 不足

content pages には frontmatter missing はなかった。`wiki/index.md` と `wiki/log.md` は special navigation/log files として frontmatter を持たない。

## データ検証

| Character | Classic rows | Modern rows | Result |
|---|---:|---:|---|
| JP | 69 | 65 | passed |
| Ryu | 75 | 69 | passed |
| Chun-Li | 78 | 72 | passed |
| Zangief | 72 | 66 | passed |

validation は raw HTML / raw DOM snapshot から再生成した data と saved derived JSON rows / field meanings を比較する。screenshots は page state、table width、overlay の visual coverage evidence として使い、cell-value source にはしない。

## 知識上の問題

### 古い open questions

すでに filed-back された Classic / Modern comparison pages の作成有無を問う stale questions を整理した。

### 矛盾

accepted source pages、character entities、index entries、question pages の間に直接の contradiction は見つからなかった。

## 次に調べる質問の候補

- reader-facing command notation を normalized schema として定義するべきか。
- SuperCombo Wiki の community terms と Capcom official terms の対応を、公式 source で確認するべきか。
