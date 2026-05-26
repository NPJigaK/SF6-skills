---
type: concept
title: "Fighting Game Notation"
created: 2026-05-26
updated: 2026-05-26
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/frame-data]]"
tags:
  - notation
  - glossary
---

# Fighting Game Notation

## Summary

Fighting-game notation compactly describes links, cancels, holds, releases,
chains, hit states, air actions, delayed timing, tiger-knee inputs, whiffs, and
directional inputs.

## Definition

The source's notation table defines examples including:

- `A,B` for linking one action into another.
- `A > B` for canceling one action into another.
- `(N)` for using only some hits of a multi-hit move.
- `xN` for repeating a chained normal.
- `[X]` for holding an input.
- `]X[` for releasing an input.
- `X~Y` for doing inputs in quick succession.
- `CH`, `j.`, `jc`, `dl`, `TK`, and whiff notation.

## Why it matters

Notation is required for later wiki pages to preserve source wording while
remaining concise.

## Key claims

| Claim | Sources | Confidence |
|---|---|---|
| `A,B` means linking X into Y after X recovers. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `A > B` means canceling A into B during A's animation. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `[X]` and `]X[` represent hold and release notation. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `TK` means tiger knee input timing for an air move. | [[sources/supercombo-street-fighter-6-glossary]] | medium |

## Connections

- [[concepts/frame-data]]

## Contradictions / caveats

- The clipped source's numpad-direction table appears malformed. Recapture may
  be needed before relying on that part.

## Open questions

- Should the wiki create a separate durable notation reference after additional
  notation sources are ingested?

