---
type: concept
concept_type: term
title: "Cancel"
created: 2026-06-10
updated: 2026-06-10
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/chain]]"
  - "[[concepts/terms/super-art]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "cancel"
  - "キャンセル"
  - "キャンセル可"
tags:
  - sf6
  - terms
  - notation
  - frame-data
---

# Cancel

## 要約

Cancel は、ある技の animation / recovery を別の行動で中断して次の技へ移ること。SuperCombo notation では `A > B` が A の animation 中に B を入力して cancel する意味で、frame-data の Cancel field には cancel 可能な行動種別が記録される。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-glossary]] | `A > B` は A の animation 中に B を入力して cancel する notation。 | medium |
| [[sources/supercombo-street-fighter-6-glossary]] | Cancel field は、one move into another move へ cancel できる available options を示す。`Chn`、`TC`、`Sp`、`SA`、`Jmp` などがある。 | medium |
| [[sources/capcom-official-fightingground-battle-system]] | Drive Rush は cancel 可能な通常技から出せる。 | high |

## 意味差分

- 公式 frame-data の `C` や SuperCombo の `Chn` / `Sp` / `SA` などは粒度が違う。回答では、どの source の cancel 表記かを明示する。
- Link は前技の recovery 後に次技を出す関係であり、cancel とは区別する。

## 関連

- [[concepts/terms/drive-rush-cancel]]
- [[concepts/terms/chain]]
- [[concepts/terms/super-art]]
- [[concepts/fighting-game-notation]]
