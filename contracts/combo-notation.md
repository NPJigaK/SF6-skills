# Combo Notation Contract

This contract defines how combo notation is recorded for `evals/fixtures/combo-damage/*.yaml`.

It is intentionally smaller than a damage calculator input contract. The goal is to make fixture notation reviewable, stable enough for damage-hidden eval gating, and explicit about unresolved route context.

## Fields

Combo damage fixture cases use two notation fields:

- `combo_notation_jp`: human-facing Japanese notation copied from visible overlays, source-local wording, or maintainer review notes.
- `combo_notation_normalized`: provisional machine-facing notation written with English-compatible tokens.

`combo_notation_normalized` is a review aid and future-facing bridge. It is not yet a complete damage calculator input format unless a later contract says so.

## Enabled Case Precision

`enabled_for_damage_hidden_eval: true` requires a precise route-to-damage mapping.

An enabled case must have:

- a non-empty `combo_notation_normalized`;
- exact starter and route steps, not only a generic category;
- clear cancel or Drive Rush placement;
- clear OD, target-combo, branch, and timing modifiers when present;
- a visible and unambiguous observed damage label;
- no unresolved inherited route context;
- `notation_confidence: high`;
- `damage_confidence: high`;
- `damage_visible: true`;
- `review_status: needs_review` until a fixture-specific accepted state is designed.

If any of these are missing, keep the case disabled.

## Move Tokens

Use numpad-style directional notation for exact normal moves:

- `5LP`
- `2LP`
- `5MP`
- `2MP`
- `5HP`
- `2HP`
- `6HK`

Use English-compatible move names for specials and supers:

- `weak Stribog`
- `medium Stribog`
- `heavy Stribog`
- `medium Torbalan`
- `Triglav`
- `OD Triglav`

The token set is provisional. Prefer consistency and reviewability over inventing aliases.

## Generic Starters

Visible overlays may use generic starters such as:

- `中攻撃`
- `小P`
- `大P`

Represent these as generic normalized tokens only when the exact move is not known:

- `medium_normal`
- `light_punch`
- `heavy_punch`

Generic starters are not precise enough for `enabled_for_damage_hidden_eval: true` unless a later review maps the generic starter to an exact move such as `2MP` or `5MP`.

## Separators And Cancel Notation

Use `>` between sequential hits or actions.

Use `xx` when a move is canceled into another action:

- `2LP > 5LP > weak Stribog`
- `2MP xx Drive Rush > 2HP > heavy Stribog`

If the source only says "cancel rush" without a confirmed source move, keep the generic starter:

- `medium_normal xx Drive Rush > 2HP > heavy Stribog`

Such cases should remain disabled until the starter and cancel point are reviewed.

## Drive Rush

Use `Drive Rush` for rush steps.

Examples:

- `2MP xx Drive Rush > 2HP`
- `Drive Rush 6HK(delayed)`

If Drive Rush is inferred from commentary or inherited context rather than visible route text, record that uncertainty in `notes` and keep the case disabled.

## OD Moves And Follow-ups

Use `OD <move>` for overdrive moves:

- `OD Triglav`

If the source describes an OD follow-up without showing the full route in the same visible overlay, keep the inherited route context explicit:

- `medium_normal xx Drive Rush > 2HP > heavy Stribog > medium Torbalan > OD Triglav follow-up`

Inherited OD follow-up routes should remain disabled unless the full route-to-damage mapping is reviewed.

## Target Combos And Branches

Use `target combo` when a source names a target combo but the exact move chain is not normalized yet:

- `back MP target combo`

Use branch notation only for disabled candidates:

- `2MP or back MP target combo`

Cases with unresolved branches must remain `enabled_for_damage_hidden_eval: false`.

## Timing Modifiers

Put timing modifiers in parentheses after the affected token:

- `Drive Rush 6HK(delayed)`
- `6HK(slightly delayed)`

Timing-sensitive cases should stay disabled unless the timing modifier is accepted by review and the future damage calculator contract can represent it.

## Position And Carry Context

Route notes may mention position or carry context:

- `corner carry`
- `near corner`
- `spacing-dependent`

Do not encode position context as an exact calculator input unless a later contract defines the field. If position or spacing affects the route-to-damage mapping, keep the case disabled and explain the uncertainty in `notes`.

## Inherited Route Context

Sometimes a video explains a route once and then shows a later variant by saying "replace the last move" or "from this position."

Inherited context is insufficient for enabled damage-hidden eval unless the resulting full route is explicitly reconstructed and reviewed.

Disabled cases should explain which part is inherited:

- starter inherited from previous overlay;
- final move replaced by OD variant;
- route inferred from commentary rather than visible text;
- position-specific setup inferred from prior segment.

## Boundary

This notation contract does not:

- make observed damage current-system authority;
- define a damage calculation engine;
- define exact current system mechanics;
- promote fixture cases to `knowledge/curated/`;
- allow generated references to consume fixture observed damage;
- replace `workflows/system-mechanics-fact-workflow.md`.

Observed damage remains an eval oracle label only.
