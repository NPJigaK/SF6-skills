# SuperCombo System Mechanics Parser Inputs

Status: Reviewed source summary for parser/schema planning.

This document records source-confirmed mechanics from SuperCombo's Street
Fighter 6 system pages. It is not a normalized data schema, parser
implementation, calculator, or numeric authority table.

## Source Set

Captured on 2026-05-23 JST with Scrapling reviewer tooling. Local evidence is
ignored under `.local/reviewer-evidence/supercombo-system-20260523/`.

| Page | Permanent revision | Last modified in capture | Parser relevance |
| --- | --- | --- | --- |
| Controls | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Controls&oldid=323750 | 2025-03-20 19:58 | notation, inputs, Classic/Modern distinction |
| HUD | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/HUD&oldid=345794 | 2026-01-03 12:40 | HUD icons, health/drive/super UI labels |
| Gauges | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Gauges&oldid=358728 | 2026-03-20 14:26 | Drive/Super units, costs, gains, burnout, parry, Drive Rush, scaling modifiers |
| Offense | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Offense&oldid=358708 | 2026-03-20 10:38 | throws, counter/punish, combo/blockstring, safe-jump timing |
| Defense | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Defense&oldid=358706 | 2026-03-20 10:20 | guard, throw escape, wakeup, reversal buffers, armor |
| Movement | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Movement&oldid=358703 | 2026-03-20 09:58 | walk/dash/jump timing, landing recovery, distance units |
| Game Data | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Game_Data&oldid=360454 | 2026-04-02 09:56 | frame definitions, input buffers, scaling, system data tables |
| Glossary | https://wiki.supercombo.gg/index.php?title=Street_Fighter_6/Glossary&oldid=351898 | 2026-01-31 11:22 | frame-data field definitions and notation legend |

## Image Observations

Images were reviewed only as local ignored reviewer evidence. They are not
committed.

- `FAF_Move_Stages.png` visually shows startup and active overlapping at the
  first active frame. This supports the Game Data rule that total frames are
  `startup + active + recovery - 1`, not a simple sum.
- `SF6_Health_Bars_SA3_Scaling.png` visually presents minimum-scaling health
  bar examples such as standard SA3, CA, Lily SA3/CA, and Zangief SA3/CA. Use
  this as illustrative source evidence; exact calculator constants must come
  from the accompanying text or reviewed data, not pixel measurement.
- `SF6_Battle_HUD.jpg` labels vitality, Drive gauge, timer, round count,
  attribute icon, character/control icon, and Super Art gauge. This supports UI
  label mapping but not numeric calculation.
- `SF6_Drive_Gauge.jpg` shows the segmented Drive gauge. The numeric unit is
  the page text: one Drive bar is 10,000 Drive meter.
- `SF6_DI_Armor_Example.png` labels armor during startup, armor during the
  second active frame, and no armor during recovery. This supports armor window
  semantics for Drive Impact review.

## Parser-Relevant Facts

### Time And Frame Units

- One frame is one sixtieth of a second.
- Frame advantage uses signs: positive means the attacker can act earlier;
  negative means the defender can act earlier.
- SF6 uses first-active-frame startup. Total frames for a simple move are
  `startup + active + recovery - 1`.
- Input buffer is generally four early frames plus the true timing frame.
  Dashes and wakeup reversals have their own larger buffer rules.

Parser decision: timing values need units and formula context. A `startup`
integer is not interchangeable with true startup, total frames, recovery, or
advantage.

### Active / Startup / Recovery Shapes

Glossary defines the important expression classes:

- `X,Y` or `X*Y`: multi-hit values with no gap between active hitboxes or
  per-hit damage values.
- `X(n)Y`: multi-hit active frames with a gap of `n` frames.
- `[bracketed]` projectile maximum active period: not included in total frame
  count.
- `X(Y)`: context-dependent startup or recovery values that require the move
  description to identify the condition.
- Range values such as `43f~47f`: timing interval, not a single scalar.
- Landing expressions such as `4+38+3`: structured prejump/airborne/landing
  components, not arithmetic to collapse by default.

Parser decision: these must become structured timing variants with condition
labels, not plain numbers.

### Advantage And State

- Counter-hit generally adds 2 frames of hit advantage.
- Punish Counter generally adds 4 frames of hit advantage and can add move-
  specific effects.
- `KD` means knockdown; listed knockdown advantage is wakeup-relative
  advantage.
- Drive Rush Cancel advantage is measured at the moment a follow-up attack can
  be input, not at the moment the character can block or move.
- Burnout adds four additional frames of blockstun to blocked attacks, but does
  not change hitstun.

Parser decision: advantage fields need state and modifier context:
`base`, `counter_hit`, `punish_counter`, `burnout_block`, `knockdown`, and
`drive_rush_cancel` must not be collapsed.

### Damage And Scaling

System pages define several different scaling families:

- Starter scaling affects the next attack when the move begins a combo.
- Combo scaling affects the next attack when the move is comboed into.
- Immediate scaling affects the current attack when comboed into.
- Multiplier scaling applies after Perfect Parry and mid-combo Drive Rush.
- Minimum scaling is a lower bound, with Super Art level-specific minimums.
- General combo progression depends on attack count, where an attack is a move
  input by the player, not necessarily each hit.
- Drive Rush mid-combo adds a 15 percent penalty to remaining hits and rounds
  down to a whole percentage.
- Perfect Parry applies a 50 percent damage-scaling multiplier to the punish.
- Drive Impact has separate hit/crumple/stun starter behavior and blocked wall
  splat multiplier behavior.
- Comboing into throw after stun, Drive Impact crumple, or specific wall splats
  can add immediate throw scaling; the source explicitly says this is not
  universal for every command throw.

Parser decision: `combo_scaling` cannot be a single percent field. It needs
`scaling_type`, `trigger`, `target`, `amount`, `unit`, `stacking_rule`, and
`exception_note` or `review_required` when source text says exceptions exist.

### Gauge Values

- One Drive bar is 10,000 Drive meter; page prose may use decimals such as
  `1.7 Drive`.
- Drive actions can spend stocks, raw Drive units, or continuous per-frame
  drain.
- Drive Parry has activation cost, per-frame drain, drive gain on successful
  parry, and special Perfect Parry gain behavior.
- Drive regeneration uses per-frame Drive units and percent-of-bar per second.
  Forward walking adds Drive and later doubles base regeneration under specific
  conditions.
- Drive regeneration cooldown timers differ by action and can freeze or reset.
- Super Gauge gain ratios differ for attacker/defender and hit/block/armor
  absorb; Perfect Parry can scale Super and Drive gain/damage.

Parser decision: gauge parsers need explicit unit conversion and event context:
`drive_units`, `drive_bars`, `super_percent`, `per_frame`, `per_second`,
`cooldown_frames`, `hit`, `block`, `armor_absorb`, `parry`, and `burnout`.

### Cancel / Guard / Attribute Enums

- Cancel tokens include chain, target combo, special, Super Art, jump cancel,
  stance-specific tokens, per-hit modifiers such as first/second hit, and
  specific follow-up input notes.
- Guard tokens include low, high/overhead, high-or-low blockable, and throw.
- Hitbox color legend distinguishes attack, throw, hurtbox, throwable hurtbox,
  unique/interaction box, armor/counter hitbox, and projectile clash hitbox.
- HUD/system icons such as Counter-hit, Punish Counter, Forced Knockdown,
  Cross-up, Reversal, Throw Escape, Stun/Dizzy, Armor Break, Crush, and Lock
  are discrete states.

Parser decision: enum design must preserve source-native labels and map them to
canonical enum values. Unknown tokens must be review-required, not guessed.

### Juggle Semantics

- Juggle Count, Juggle Start, Juggle Increase, and Juggle Limit are separate
  fields.
- A juggle connects only when the attack's limit is at least the defender's
  current juggle count.
- `JC0` is a free juggle state; `JC1+` is limited juggle; `-1` represents a
  crumple state.
- Drive Rush normals have zero start/increase and add 3 to usual Juggle Limit.
- Official Capcom terminology maps these community terms to combo-count
  initial value, additional value, and upper limit.

Parser decision: juggle values are not ordinary signed integers. They need a
domain-specific object and terminology mapping.

### Movement / Spatial Values

- Walk speed can have a first-frame quarter-speed exception.
- Dash input has timing windows for held direction and neutral time.
- Backdash throw invincibility is frame-bounded.
- Throw range, throw hurtbox, and relative throw range are related; relative
  throw range is the difference between throw range and hurtbox width.
- Jump timing uses prejump, airborne duration, and landing recovery components.

Parser decision: mobility/spatial values require domain-specific units and
component labels. Expressions such as `4+38+3` must not be parsed as one
undifferentiated total unless the target calculator explicitly asks for total
duration and preserves components.

## Disposition Implications

The current disposition counts are:

- `247` total review item groups.
- `208` `parse_rule_required_before_schema` groups.
- `16` `source_specific_enum_required` groups.
- `6` `schema_supports_raw_only` groups.
- `17` `out_of_scope_first_normalized_export` groups.
- `0` `blocked_pending_source_review` groups.

These counts mean:

- `parse_rule_required_before_schema`: calculation is blocked until a
  deterministic parser produces structured output for the relevant expression
  class.
- `source_specific_enum_required`: calculation and filtering are blocked until
  the enum vocabulary is reviewed and unknown values hard fail.
- `schema_supports_raw_only`: the value may be preserved and displayed, but it
  is explicitly excluded from calculation unless a later policy changes it.
- `out_of_scope_first_normalized_export`: excluded from first normalized output
  by reviewed rationale; not silently skipped.
- `blocked_pending_source_review`: currently zero after prior source-review
  work, but future drift can reintroduce this status.

## Required Follow-Up Work

The next deterministic parser/classifier implementation must consume this
source review and produce explicit statuses:

```text
parsed
enum_classified
raw_preserved_non_calculation
review_required
out_of_scope_first_normalized_export
```

Calculation tools may later consume only `parsed` records whose source role,
authority status, unit, and parsed kind match the calculation domain. Everything
else remains unavailable for arithmetic.

## Answer To Calculation Safety Question

At the current stage, the raw and partially reviewed values are not sufficient
for general SF6 calculations such as frame math, punish lookup, damage scaling,
combo damage, or resource calculations. Exact raw lookup can still show source
values, but arithmetic must wait until deterministic parser/classifier output
exists and is reviewed.

This is not acceptable to ignore. It is acceptable only as a gated roadmap:
source acquisition, value-shape inventory, mapping, disposition, system
mechanics review, deterministic parser/classifier, normalized schema, then
domain calculators.
