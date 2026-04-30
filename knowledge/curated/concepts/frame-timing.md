---
id: sf6-concept-frame-timing
title: Frame Timing And Advantage
claim_kind: stable_concept
source_kind: maintainer_note
source_role: migrated stable concept material
evidence_basis:
  - "Fighting-game actions can be compared by frame timing, action phases, recovery, and post-contact advantage."
  - "The migrated material describes conceptual relationships only and excludes exact current move values."
verification_state: verified
confidence: 0.9
volatility: stable
patch_sensitivity: low
review_status: accepted
source_refs:
  - label: "Legacy stable concept notes reviewed during v2 migration"
    path: "skills/kb-sf6-core/references/KNOWLEDGE.md"
    source_revision: "efd7a8ae251bd2600e58a675d9066673711351e3"
review_after: null
summary: "Frames are the shared timing unit for comparing move speed, recovery, advantage, and punishability without asserting exact current values."
generated_allowed: true
must_not_include:
  - "exact current startup, active, recovery, total, hit advantage, or block advantage values"
  - "move-specific punish recommendations"
---

# Frame Timing And Advantage

Frames are the common timing unit for discussing how long actions take and who can move first after interaction. They are useful for reasoning about speed, recovery, pressure, and punishment, but this page does not provide exact current move values.

## Action Phases

Startup is the time before a move can hit. Active frames are the period when the attack can connect. Recovery is the time after the active portion before the character can act again.

These phases answer different questions:

- Startup helps compare how quickly an option can interrupt, punish, or contest.
- Active duration matters for space control, meaty timing, and catching movement.
- Recovery shapes whiff risk and post-block vulnerability.

## Total Duration And Advantage

Total duration describes the complete length of an action. Advantage compares when each player can act after hit or block interaction. A longer total duration does not automatically mean a move is always worse, and a shorter total duration does not automatically mean it is always safer; contact timing, spacing, cancel options, and opponent state can change the practical result.

Hit stun and block stun are the periods where the defender cannot act after being hit or after blocking. These periods are part of why the same move can produce different practical outcomes on hit and on block.

## Plus, Minus, And Punishment

When a situation is plus, the attacker can act first. When it is minus, the defender can act first. Whether that becomes a guaranteed punish depends on the size of the disadvantage, the defender's available option, range, pushback, stance, cancel state, and other context.

Use this concept to explain how punishability is determined. Do not use it as evidence for a specific punish route or exact current frame claim.
