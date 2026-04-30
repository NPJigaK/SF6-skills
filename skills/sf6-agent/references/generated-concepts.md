---
generated: true
generator: packages/knowledge-generation/build-sf6-agent-knowledge.ps1
source_paths:
  - knowledge/curated/concepts/frame-timing.md
  - knowledge/curated/concepts/offense-decision-making.md
  - knowledge/curated/glossary/shimmy.md
target_path: skills/sf6-agent/references/generated-concepts.md
---

# Generated Concepts

GENERATED FILE - DO NOT EDIT
generator: packages/knowledge-generation/build-sf6-agent-knowledge.ps1
source_root: knowledge/curated

This file is derived from `knowledge/curated` and must be regenerated from curated source files.
It must not contain exact current frame values; exact current move values belong outside curated generated knowledge.

## Boundary

The entries below are derived summaries and concept text from curated v2 knowledge. They are suitable for stable concept grounding only and must not be used as exact current frame data.

## Frame Timing And Advantage

- source: knowledge/curated/concepts/frame-timing.md
- claim_kind: stable_concept
- source_kind: maintainer_note
- source_role: migrated stable concept material
- verification_state: verified
- confidence: 0.9
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: null
- summary: Frames are the shared timing unit for comparing move speed, recovery, advantage, and punishability without asserting exact current values.

Frames are the common timing unit for discussing how long actions take and who can move first after interaction. They are useful for reasoning about speed, recovery, pressure, and punishment, but this page does not provide exact current move values.

### Action Phases

Startup is the time before a move can hit. Active frames are the period when the attack can connect. Recovery is the time after the active portion before the character can act again.

These phases answer different questions:

- Startup helps compare how quickly an option can interrupt, punish, or contest.
- Active duration matters for space control, meaty timing, and catching movement.
- Recovery shapes whiff risk and post-block vulnerability.

### Total Duration And Advantage

Total duration describes the complete length of an action. Advantage compares when each player can act after hit or block interaction. A longer total duration does not automatically mean a move is always worse, and a shorter total duration does not automatically mean it is always safer; contact timing, spacing, cancel options, and opponent state can change the practical result.

Hit stun and block stun are the periods where the defender cannot act after being hit or after blocking. These periods are part of why the same move can produce different practical outcomes on hit and on block.

### Plus, Minus, And Punishment

When a situation is plus, the attacker can act first. When it is minus, the defender can act first. Whether that becomes a guaranteed punish depends on the size of the disadvantage, the defender's available option, range, pushback, stance, cancel state, and other context.

Use this concept to explain how punishability is determined. Do not use it as evidence for a specific punish route or exact current frame claim.

## Offensive Decision Concepts

- source: knowledge/curated/concepts/offense-decision-making.md
- claim_kind: stable_concept
- source_kind: maintainer_note
- source_role: migrated stable concept material
- verification_state: verified
- confidence: 0.86
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: null
- summary: Hit confirming and wake-up pressure describe how players choose followups, pressure, throws, delays, and checks without asserting character-specific current routes.

Offensive decisions often depend on observing whether the previous action connected, whether the opponent is waking up, and which defensive options the opponent is likely to choose. This page gives stable concept boundaries only.

### Hit Confirming

Hit confirming means choosing a followup after recognizing that an earlier action hit. The practical purpose is to extend offense or damage when the attack connects while avoiding unnecessary risk when it is blocked or misses.

Confirm difficulty depends on the situation, visual cue, buffer window, cancel rules, input timing, and the player's preparation. Exact confirm windows and optimal routes are character-specific current facts or strategy claims and need separate evidence.

### Wake-Up Pressure

Wake-up pressure means applying offense as the opponent rises from knockdown. Common pressure choices include strikes, throws, delayed actions, movement baits, and waiting to react.

The concept is stable, but the actual setup depends on knockdown type, spacing, recovery timing, available reversals, defensive system choices, and current move behavior. Treat exact meaty setups and guaranteed followups as separate claims that need current verification.

## Shimmy

- source: knowledge/curated/glossary/shimmy.md
- claim_kind: stable_concept
- source_kind: community
- source_role: community terminology boundary
- verification_state: partially_verified
- confidence: 0.74
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: 2026-10-30
- summary: A shimmy is a community term for baiting a throw-tech or delayed defensive response by threatening throw, moving just out of range, and punishing the whiff or response.

Shimmy is a community term for a pressure bait. The attacker threatens throw, briefly moves out of throw range, and then punishes the defender's throw-tech attempt, delayed throw tech, or other delayed defensive response.

Use the term as community terminology, not as official game wording. Whether a shimmy works in a specific situation depends on spacing, timing, throw range, walk speed, available buttons, defensive choices, and the current move environment.
