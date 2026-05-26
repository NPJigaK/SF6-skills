---
type: question
created: 2026-05-26
updated: 2026-05-26
status: active
question: "ジャグルって内部的にどういう仕組みで発生するんですか？"
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/juggle-system]]"
  - "[[concepts/frame-data]]"
---

# Question: ジャグルって内部的にどういう仕組みで発生するんですか？

## Short answer

この wiki に取り込まれている SuperCombo Wiki glossary によると、
SF6 のジャグル可否は、ざっくり言うと「浮いた相手の現在の
ジャグル状態」と「追撃する技側のジャグル性能」を比べて、
空中追撃できるかを判定する仕組みとして説明できる。

中心になるのは、相手側の現在状態を表す `Juggle Count` と、攻撃側の
`Juggle Start`、`Juggle Increase`、`Juggle Limit` の関係。
限定ジャグルでは、ジャグル制限上、攻撃の `Juggle Limit` が相手の
`Juggle Count` 以上なら接続可能で、足りなければ接続不可になる。
ただし、これはあくまでジャグル制限の判定であり、実際にヒットするには
攻撃判定、喰らい判定、距離、タイミングも噛み合う必要がある。

## Evidence

- [[concepts/juggle-system]] summarizes the source terminology.
- [[sources/supercombo-street-fighter-6-glossary]] records the glossary source
  and points to the raw source section `Frame Data definitions > Juggles`.

## Reasoning

The source describes two broad juggle states:

- `Free Juggle`: any applicable attack can juggle the airborne opponent.
- `Limited Juggle`: only attacks with enough juggle potential are allowed by
  the juggle rules.

For limited juggles, the source uses these terms:

| Term | Role |
|---|---|
| `Juggle Count` / `JC` | The defender's current juggle state. A higher value makes follow-ups more restricted. |
| `Juggle Start` / `JS` | The value that starts or sets the defender's juggle state when a juggle begins. |
| `Juggle Increase` / `JI` | The amount added to the defender's juggle state after a follow-up hit connects. |
| `Juggle Limit` / `JL` | The attack hitbox's limit for being allowed against the defender's current juggle state. |

For limited juggles, the practical rule described by the source is:

```text
if attack.JuggleLimit >= defender.JuggleCount:
    the hit is allowed by the juggle rules
else:
    the hit is not allowed by the juggle rules
```

This does not mean the attack is guaranteed to hit. It only means the juggle
system allows the hit to connect; spacing, timing, hitboxes, and hurtboxes
still matter.

Conceptually, the flow is:

1. A hit puts the opponent into an air knockdown or juggle-capable state.
2. That state has a current `Juggle Count`.
3. A follow-up attack checks its `Juggle Limit` against that count.
4. If the attack connects, its `Juggle Increase` can raise the opponent's count.
5. As the count rises, fewer later attacks can connect.

The source also says `Forced Knockdown` matters because it can cause an air
knockdown in situations that might otherwise produce an air reset. That creates
or preserves a state where a follow-up juggle can happen.

## Limits / uncertainty

- This answer is based on one community wiki glossary source.
- This page is based on the SuperCombo community glossary. The SuperCombo
  source says official Capcom terminology differs and lists related official
  patch-note terms such as Combo Count Initial Value, Combo Count Additional
  Value, and Combo Count Upper Limit, but this wiki page has not yet
  independently ingested or cited official Capcom source pages for those terms.
- This answer explains the mechanism conceptually. It does not provide
  character-specific routes or reviewed move-specific juggle values.

## Filed-back updates

- Added this reusable question page.
- No concept page changes were required; [[concepts/juggle-system]] already
  contained the relevant core model.
