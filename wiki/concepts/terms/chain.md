---
type: concept
concept_type: term
title: "Chain"
created: 2026-06-10
updated: 2026-06-10
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "chain"
  - "chain cancel"
  - "Chn"
  - "連打キャンセル"
tags:
  - sf6
  - terms
  - notation
  - frame-data
---

# Chain

## 要約

Chain は、SuperCombo glossary の frame-data / notation で、light normals などが特定の通常技へ cancel できる関係を表す用語。Cancel field では `Chn` として現れ、notation template では `xN` が self-chain の繰り返しを表す。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-glossary]] | Cancel field の `Chn` は Chain cancel を表し、light normals や特定 chain options が Description に記載される。 | medium |
| [[sources/supercombo-street-fighter-6-glossary]] | `xN` は normal that chains into itself pressed N times を表す notation。 | medium |
| [[sources/supercombo-street-fighter-6-glossary]] | Target Combo が cancelable な時、hitconfirm window は sequence 全体または followup hit に対して記録されることがある。 | medium |

## 意味差分

- 現時点では SuperCombo glossary / notation 由来の用語。公式 frame-data の `C` cancel 表記とは同じではない。
- Query では `chain` と `cancel` を混ぜず、source が `Chn` か `C` かを確認する。

## 関連

- [[concepts/terms/cancel]]
- [[concepts/fighting-game-notation]]
- [[concepts/frame-data]]
