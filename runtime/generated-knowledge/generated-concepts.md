---
generated: true
generator: packages/knowledge-generation/build-sf6-agent-knowledge.ps1
source_paths:
  - knowledge/curated/concepts/frame-timing.md
  - knowledge/curated/concepts/offense-decision-making.md
  - knowledge/curated/glossary/cancel.md
  - knowledge/curated/glossary/cross-up.md
  - knowledge/curated/glossary/lethal.md
  - knowledge/curated/glossary/meaty.md
  - knowledge/curated/glossary/shimmy.md
  - knowledge/curated/mechanics/combo-scaling.md
target_path: runtime/generated-knowledge/generated-concepts.md
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

## Cancel

- source: knowledge/curated/glossary/cancel.md
- claim_kind: stable_concept
- source_kind: community
- source_role: community terminology boundary
- verification_state: partially_verified
- confidence: 0.62
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: 2026-10-14
- summary: Cancel, or キャンセル, is community terminology for ending the later recovery of one action into another action, such as a normal into a special, without asserting current move-specific cancel routes.

Cancel, often called `キャンセル` in Japanese SF6 discussion, is community
terminology for ending the later recovery of one action into another action.
For example, players often discuss a normal attack being canceled into a special
move as a general concept.

Use this page for the stable term only. Whether a specific move can cancel, when
it can cancel, and what routes are valid are current move or route facts that
need separate evidence.

## Cross-Up

- source: knowledge/curated/glossary/cross-up.md
- claim_kind: stable_concept
- source_kind: community
- source_role: community terminology boundary
- verification_state: partially_verified
- confidence: 0.64
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: 2026-10-14
- summary: Cross-up, or めくり, is community terminology for an attack that crosses or threatens from the opposite side and changes or obscures the defender's guard direction.

Cross-up, often called `めくり` in Japanese SF6 discussion, is community
terminology for an attack that crosses or threatens from the opposite side and
therefore changes or obscures the defender's guard direction.

Use this as a terminology boundary. Do not treat it as evidence that a specific
current jump attack, setup, spacing, or character route crosses up without
separate verification.

## Lethal

- source: knowledge/curated/glossary/lethal.md
- claim_kind: stable_concept
- source_kind: community
- source_role: community terminology boundary
- verification_state: partially_verified
- confidence: 0.62
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: 2026-10-14
- summary: Lethal, or リーサル, is community terminology for an option or combo that can finish the opponent from the current life total.

Lethal, often called `リーサル` in Japanese SF6 discussion, is community
terminology for an option, sequence, or combo that can finish the opponent from
the current life total.

Use this as a stable term only. Whether something is actually lethal depends on
current health, character, resources, scaling, route damage, positioning, and
patch-specific behavior.

## Meaty

- source: knowledge/curated/glossary/meaty.md
- claim_kind: stable_concept
- source_kind: community
- source_role: community terminology boundary
- verification_state: partially_verified
- confidence: 0.62
- volatility: stable
- patch_sensitivity: low
- review_status: accepted
- review_after: 2026-10-14
- summary: Meaty, or 重ね, is community terminology for timing an attack to overlap a defender's wake-up or recovery timing without asserting a specific guaranteed setup.

Meaty, often called `重ね` in Japanese SF6 discussion, is community terminology
for timing an attack so it overlaps the defender's wake-up or recovery timing.
The basic idea is that the attacker places an active threat where the defender
is about to become able to act.

Use this as a stable terminology explanation only. Whether a particular meaty
setup works depends on knockdown type, spacing, recovery timing, active
duration, invincible options, defensive system choices, and current move
behavior.

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

## Combo Scaling

- source: knowledge/curated/mechanics/combo-scaling.md
- claim_kind: stable_concept
- source_kind: community
- source_role: reviewed japanese article stable mechanics concept
- verification_state: partially_verified
- confidence: 0.7
- volatility: stable
- patch_sensitivity: medium
- review_status: accepted
- review_after: 2026-11-03
- summary: コンボ補正は、コンボ中のダメージを状況に応じて調整する仕組みです。技ごとの現在値はframe-current runtime assetsを参照し、このページでは計算を見るための概念だけを扱います。

コンボ補正は、コンボ中のダメージを状況に応じて調整する仕組みです。

コンボで複数の攻撃がつながる時、各ヒットを常に独立した最大ダメージとして扱うのではなく、始動、ルート、途中で使う行動、ヒットの位置づけなどによって最終的なダメージが変わります。

### 何を説明する概念か

コンボ補正は、同じように見えるコンボでもダメージが変わる理由を説明するための安定概念です。

たとえば、次のような観点を分けて考える時に使います。

- どの行動からコンボが始まったか。
- コンボ中にどのようなルートを選んだか。
- システム行動や特殊な条件が関係しているか。
- 途中のヒットが、後続ダメージにどのような影響を持つ可能性があるか。

このページは、そうした考え方の入口だけを扱います。具体的な数値、技ごとの例外、キャラクター固有の扱いは扱いません。

### 計算方法を読むための考え方

コンボ補正の計算は、単に技の基礎ダメージを全部足すものではありません。

各ヒットごとに、基礎ダメージに対してコンボ状況や追加条件による補正が関わる、と考えると安全です。

コンボダメージを読む時は、少なくとも次を分けて見ます。

- そのヒットの基礎ダメージ。
- コンボが進んだことによる補正。
- 始動やルート、システム行動による補正。
- 最低保証や技、キャラクター、操作方式に関係する例外。
- 現行patchで確認する具体値。

技ごとの基礎ダメージや、技に紐づく始動補正・コンボ補正の現在値は、このページでは扱いません。必要な場合は `runtime/frame-current/` のruntime assetsを参照します。各キャラクターのpublished runtime dataには、moveごとのraw official fieldsが含まれる場合があります。

このページで扱うのは、補正率そのものではなく、コンボ補正を読むための考え方です。コンボ全体の最終ダメージ計算、システム行動、最低保証、キャラクター固有・技固有の例外、現行patchでの正確な計算式は、frame-current runtime assets、現在の公式情報、ゲーム内検証、または将来のsystem-mechanics fact workflowで確認してください。

### 回答で使ってよいこと

ユーザーに説明する時は、コンボ補正を「コンボ中のダメージを調整する仕組み」として説明してよいです。

また、コンボダメージを見る時には、単純なヒット数だけでなく、始動やルート、途中で使った行動、現在のシステム仕様を分けて確認する必要がある、と案内してよいです。

ただし、特定の補正率、特定キャラクターの例外、特定技の現在仕様、特定ルートの期待ダメージを、このページだけで断定してはいけません。

### Review boundary

このページは安定概念だけをcurated knowledgeとして受け入れています。

次の内容は、このcurated pageには複製しません。必要に応じてframe-current runtime assets、review、またはcurrent-system verificationで扱います。

- 具体的な補正率。
- 技ごとの基礎ダメージ、始動補正、コンボ補正の現在値。
- システム行動、SA最低保証などの現在仕様。
- キャラクター固有、技固有、操作方式固有の例外。
- 現行patchでの正確なコンボダメージや最適ルート。

Hameko 2023記事は、この概念を整理するための有用な日本語sourceですが、現在仕様の最終根拠としては扱いません。数値や例外を回答に使う場合は、このページから推測せず、適切なcurrent-fact surfaceやcurrent-system workflowで確認してください。
