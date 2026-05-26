---
title: "Street Fighter 6/Glossary"
source: "https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary"
author:
published:
created: 2026-05-26
description: "Many general Fighting Game terms can be found at Infil's Fighting Game Glossary."
tags:
  - "clippings"
---
Many general Fighting Game terms can be found at [Infil's Fighting Game Glossary](https://glossary.infil.net/).

## Drive System definitions

### Burnout

When the Drive gauge is empty, the fighter will enter Burnout and will not be able to use Drive-related techniques until the gauge is replenished. See [Burnout](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Burnout "Street Fighter 6/Gauges").

### Drive Impact

A powerful strike that can absorb an opponent’s incoming attack. Perform this on an opponent backed into the corner to induce a wall splat, even if they block the attack. See [Drive Impact](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Drive_Impact "Street Fighter 6/Gauges").

### Drive Parry

Automatically repel an opponent’s attack and replenish Drive when performed successfully. Perform a Perfect Parry by parrying just before an opponent’s attack hits you. See [Drive Parry](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Drive_Parry "Street Fighter 6/Gauges").

### Drive Reversal

Perform a counterattack while blocking an opponent’s attack. The damage is low but can help you out of tight situations when you’re being pressured. See [Drive Reversal](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Drive_Reversal "Street Fighter 6/Gauges").

### Drive Rush

Perform a quick rush forward from a Drive Parry or a cancelable normal attack. Drive Rush from a parry costs 1 Drive Stock, while Drive Rush from a normal attack costs 3 Drive Stocks. See [Drive Rush](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Drive_Rush "Street Fighter 6/Gauges").

### Drive System

The Drive System is a meter in Street Fighter 6 that serves as the gateway to universal movement, offense and defense mechanics. See [Drive System](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges "Street Fighter 6/Gauges").

### Overdrive

Press two or more of the same button type instead of one when performing a special move to turn it into an Overdrive Art. These are the same attacks as EX Special Moves in past games. See [Overdrive](https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges#Overdrive "Street Fighter 6/Gauges").

## Frame Data definitions

### Hitbox Images

**Red: Attack hitbox**  
**Pink: Throw hitbox**  
**Green: Hurtbox** (strikes/projectiles)

- Certain move properties, like Projectile Invuln or Air Invuln, may be printed onto the hurtbox and listed in the move description
- A complete lack of hurtboxes represents full invulnerability

**Blue: Throw hurtbox**

- Throw will succeed if the pink throw hitbox overlaps with the blue throwable hurtbox
- Opponent must be on the ground (except for Air Throws which only target airborne opponents)

**Teal: Unique/Interaction box**

- Applies character-specific effects when two of these hitboxes overlap
- Examples: Rashid's air current, Blanka's electric moves + Blanka-chan, Guile's Sonic Blade + Sonic Boom

**Purple: Armor/Counter Hitbox**

- Can appear on top of green hurtboxes or replace them entirely

**Orange: Projectile Clash hitbox**

- Not a projectile itself, but interacts with and destroys projectiles of the same priority
- Light Orange box on Drive Impact: represents the "cinematic DI Slowdown" interaction hitboxes

### Active

How many frames a move remains active (can hurt opponents) for. For projectiles with a maximum active period, a value may be listed in \[brackets\], but this number is not factored into the move's total frame count.

- For multi-hit moves with no gaps between the active hitboxes, active frames are listed as X,Y (or sometimes X\*Y)
- For multi-hit moves with gaps between hits, active frames are listed as X(n)Y where n = the frame gap between hitboxes.

### Cancel

Available options for canceling one move into another move.

- "Chn": Chain cancel (Light normals; specific chain options listed in Description)
- "TC": Target Combo
- "Sp": Special move
- "SA": Super Art (if a number is listed, refers only to that specific Super; SA3 = Lv.3 Super Art)
- "Jmp": Jump cancel (usually on hit only, if applicable)
- "SS": Serenity Stream (Chun-Li's stance)
- "PS": Prowler Stance (Alex's stance)
	- If one hit of a multi-hit attack is cancelable, this can be indicated with (1st), (2nd), etc.
		- Occasionally, a move can be canceled only into a specific follow-up (e.g. Dee Jay \[4\]6P > 22PP); this can be indicated by listing the move input in the Cancel field, or with an asterisk that is explained in the move notes (Sp\*)

### Cancel Hitconfirm Windows

Hitconfirm reaction windows into Special Moves, Target Combos, and Super Arts.

- Refers to the amount of time (in frames) you have to cancel one attack into another attack on reaction
	- e.g. most cancelable 2MKs have a 13 frame window to cancel into a Special/Super on reaction, making them nearly impossible to hitconfirm
- Counts from the first frame the attack connects until the final cancelable frame
	- Visual effects like hitsparks and HP drain do not actually occur until frame 2; the first frame is still counted to keep the numbers consistent with previous games, and because it is technically possible to start reacting to the character's reeling animation on frame 1
- If a Target Combo is cancelable into another attack, the hitconfirm window will include the entire sequence starting from the first hit
	- If there is a frame gap on block between hits of the TC, the hitconfirm window may also be included for just the followup hit
		- Some sequences like Ken's 5MP~HP TC may have a range of values listed (43f~47f). In this example, inputting 5MP~HP at its usual timing gives a 43f hitconfirm into a Special/Super. Delaying the chain into HP gives more total time for the final hitconfirm.

### Damage

Attack damage on hit. Multi-hit moves may have the damage listed for individual hits as X,Y (or sometimes X\*Y). Sometimes a move's damage changes depending on which active frame connects, or on cinematic vs. non-cinematic hits; in this case, multiple values may be listed, and it will be clarified in the move description.  

### Damage Scaling

Some moves cause additional damage scaling in combos. Refer to [Game Data](https://wiki.supercombo.gg/w/Street_Fighter_6/Game_Data#Damage_Scaling "Street Fighter 6/Game Data") page for a more detailed breakdown.

Scaling Types:

- **Starter:** When a move **begins the combo**, the **next attack** is scaled by X percent
	- e.g. Ryu 2MK (20% Starter) > Hadoken: Hadoken is at 80% damage scaling
- **Combo:** When a move **is comboed into**, the **next attack** is scaled by X percent or X number of hits
	- e.g. Ryu 2HP > OD High Blade Kick (2-Hit Combo Scaling) > Shoryuken: Shoryuken is at 70% damage scaling (100% > 100% > \[skip 80%\] > 70%)
		- e.g. Cammy 5HP > OD Spiral Arrow (5% Combo Scaling) > Cannon Spike: Cannon Spike is at 75% damage scaling (100% > 100% > \[80-5 = 75%\])
- **Immediate:** When a move **is comboed into**, **this attack** is scaled by X percent
	- e.g. Drive Impact Crumple (20% Starter) > Throw (20% Immediate): Throw is at 60% damage scaling
- **Multiplier:** A damage scaling multiplier applies after Perfect Parry (50%) and mid-combo Drive Rush (15%). Any hits in the combo continue their usual damage scaling, but reduced by these amounts. These can bring the minimum scaling below the usual 10%, and they stack with each other; as a result, the minimum scaling can reach 4% using a long Drive Rush combo after Perfect Parry.
- **Minimum Scaling:** The lowest damage scaling that can be applied to an attack. Super Art Level 1/2/3 generally has 30%/40%/50% minimum scaling respectively. This ensures the attack will still do reasonable damage even at the end of a heavily scaled combo.

### Drive Rush Cancel Advantage

Refers to the frame advantage when canceling a normal, command normal, or Target Combo into Drive Rush on hit or block (abbreviated as DRC for Drive Rush Cancel). This is calculated at the moment a follow-up attack can be input, not at the moment the character can block or perform movement options. An attack that with DRC +8 on Hit can link into an 8-frame attack, and DRC +4 on Block can create a true blockstring into a 4-frame attack.

Note that any DRC on Block worse than +4 cannot form a true blockstring, allowing the opponent to interrupt with an invincible reversal. Most light normals are slightly negative after a DRC on block, meaning the opponent can mash their fastest normal to guarantee a counter-hit (though this requires fast reactions). The attacking character could punish this with Light > DRC into an immediate invincible attack, but this would be an incredibly expensive and high-risk gambit.  

### Forced Knockdown

Most airborne command normals, special moves, and Super Arts put the user in a **"Forced Knockdown"** state. While in this state, an air knockdown will occur when being hit by any attack, even if it would otherwise cause an air reset.

As an example, Ryu's 2HP causes an air reset when used as an anti-air. Against a move like Cammy's Hooligan Combination, however, the 2HP puts her into an air knockdown state. This allows Ryu to successfully cancel 2HP into Shoryuken for a juggle, similar to how a Drive Impact wall splat works. Taking advantage of Forced Knockdown juggles is important for dealing with moves like Ken's Dragonlash, Dhalsim's Air Teleport, or Kimberly's 6HK~Hop sequence.

Moves that already cause an air knockdown, like most j.MP air-to-airs, will not display the "Forced Knockdown" message.  

### Guard

Refers to the direction an attack must be blocked. L is for **Low** attacks (must be blocked crouching), H is for **High** attacks/overheads (must be blocked standing), LH is for attacks that can be blocked crouching or standing. T is for **Throw** attacks which cannot be blocked.  

### Juggles

When a character is put into an Air Knockdown state, it is often possible to follow up with a Juggle attack before they hit the ground. In the simplest terms, there are 2 main juggle states:

- **Free Juggle:** any attack can juggle, causing an Air Reset or an Air Knockdown
- **Limited Juggle:** only specific attacks with juggle potential may juggle

The following is a more detailed overview of the SF6 juggle system:  
  
**Juggle Count (JC)**: The status of the character being juggled. A high JC limits which attacks can work in juggles.

- **JC0:** free juggle state - any attack that can hit an airborne opponent will work
- **JC1+:** limited juggle state - juggle only works if the attack's Juggle Limit ≥ defender's Juggle Count
	- A juggle count of **\-1** represents a crumple state; this can lead to a grounded or airborne hit depending on timing

**Juggle Start (JS)**: When starting a juggle, the opponent's JC will be set to this value. May be different vs. standing and airborne opponents.

- Attack with Juggle Start value of 3 will put opponent at JC3, so only attacks with Juggle Limit value ≥ 3 can follow up
- Even for attacks that don't normally start a juggle, this is relevant for Forced Knockdown and Crumple situations

**Juggle Increase (JI)**: When opponent is already in a juggle state, attacks will increase the opponent's JC by this amount.

- Airborne opponent at JC1 followed by attack with Juggle Increase value of 3 will set opponent to JC4

**Juggle Limit (JL)**: Property of an attack hitbox that determines whether it connects on a juggled opponent. The JL must be ≥ the opponent's JC to hit successfully.

- An uppercut with a JL value of 5 will connect on an opponent at JC5 or below, but will whiff on JC6 opponent
- Most normals have a JL value of 0, meaning they only work in Free Juggle (JC0) states
- Some multi-hit attacks have different JL values on each hit, so a 3-hit move may only hit twice in juggles

An example to tie everything together:

- An attack (JS3) launches opponent into the air (Opponent now at JC3)
- Followed up with an attack (JI2/JL4); it connects, because JL4 ≥ JC3 (Opponent now at JC5)
- Attempts to juggle again with same attack (JL4), but whiffs because JL4 < JC5 (Opponent hits the ground)

Drive Rush notes:

- DR normals have a Juggle Start/Increase value of 0
- DR normals have +3 added to their usual Juggle Limit

More recently, the official definitions used by Capcom are slightly different than these community-designated terms. When reading official patch notes, the following terms are used instead:

- Combo Count Initial Value
- Combo Count Additional Value
- Combo Count Upper Limit

### On Hit/Block

These are frame advantage values when the attack hits or is blocked. If the number is positive, then the move will recover before the defender can act again. If the number is negative, the defender will be able to act before the attacker and maybe even punish. KD refers to knockdown on hit, and the listed KD Advantage refers to how many frames the attacker can act before the defender finishes their wakeup animation.

- Note that generally, there is an extra +2 hit advantage on Counterhits and +4 hit advantage on Punish Counters (exceptions are noted in the description).

### Recovery

How many frames it takes for a move to finish after the active frames have finished. For projectiles, recovery is considered to begin after the first active frame.

- Moves with different recovery values on hit/block/whiff may have multiple values listed like X(Y), with specific details listed in the description.

### Startup

How many frames it takes before the move becomes 'active' or have a hit box. The last startup frame and the first active frame are the same frame, meaning all values are written as Startup + 1.

- Moves with multiple relevant startup values may be listed as X(Y); for example, a move that hits airborne first before hitting grounded opponents, or a 2-hit move where the first hit whiffs at some ranges.

### IASA / Actionable Recovery

Some moves play out an extended recovery animation when no other button/direction is input (for crouching moves, it applies when holding any down direction). These are often referred to as "actionable recovery" frames; in some games, the term IASA (Interruptible As Soon As) refers to the frame that Actionable Recovery begins.

Letting the Actionable Recovery frames play out can change the character's position, potentially setting up spacing traps by recovering farther away. For example, Manon 5HP will recover much farther away from the opponent if no input is performed immediately after her recovery; holding back or down-back to block will keep her much closer to the opponent.

## Notation Glossary

| Abbreviation | Meaning |
| --- | --- |
| A,B | Link X into Y. This is done by pressing X, then Y after the recovery frames of X. |
| A > B | Cancel A into B. During A's animation, press B to cancel. |
| (N) | Multi-hit move hits only N times. Omitted if all hits are used. |
| xN | Normal that chains into itself pressed N times |
| \[X\] | Hold down X |
| \]X\[ | Release X |
| X~Y | X then Y done in quick succession |
| X/Y | X or Y |
| Fastfall | Cancelling an air normal into another move to change momentum and land early. The 2nd move is land cancelled during startup. |
| Kara | Quickly cancelling a move into another move before it becomes active. This is done for positioning or to access airborne specials from grounded attacks. |
| OTG | Following move hits off the ground |
| CH | Counter hit |
| j. | Prefix an attack command with j. to indicate it must be performed in the air. "nj." means neutral jump only. |
| jc | Jump cancel |
| dl | Delay |
| TK | Tiger knee (doing an air move the moment a jump sends you airborne, typically by inputting a special move motion followed by jump+button.) |
| whiff / (w) | Indicates that the move must not hit the opponent. |
| (move) | Indicates that the move is optional in a sequence. |
| 236 |  |
| 214 |  |
| 623 |  |
| 421 |  |
| \[4\]6 | (hold), |
| \[2\]8 | (hold), |
| 360 |  |

| \|  \|  \|  \| \| --- \| --- \| --- \| \|  \|  \|  \| \|  \| • \|  \| \|  \|  \|  \| | \= | \|  \|  \|  \| \| --- \| --- \| --- \| \| 7 \| 8 \| 9 \| \| 4 \| 5 \| 6 \| \| 1 \| 2 \| 3 \| | \= | \|  \|  \|  \| \| --- \| --- \| --- \| \| up-back \| up \| up-forward \| \| back \| neutral \| forward \| \| down-back \| down \| down-forward \| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |