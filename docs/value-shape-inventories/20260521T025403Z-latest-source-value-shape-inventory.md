# Latest Source Value-Shape Inventory

This reviewed summary is inventory-only. It is not numeric authority,
does not emit parsed values, and does not promote official or
SuperCombo data to daily-answer authority.

- Run ID: `20260521T025403Z`
- Acquisition report: `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- Artifact boundary: `summarized_inventory_only`
- Authority status: `inventory_only_not_authority`
- Examples per field limit: `5`
- Public raw value character limit: `120`

## Source Family Summary

| Source family | Field summaries | Observations | Review items | Authority role |
| --- | ---: | ---: | ---: | --- |
| `official` | 15 | 34290 | 16 | `authority_candidate_only_not_current_fact_authority` |
| `supercombo` | 403 | 78501 | 231 | `enrichment_cross_reference_candidate_only` |

## Shape Vocabulary

- `scalar`
- `signed_frame`
- `range`
- `plus_expression`
- `note_prefixed`
- `note_suffixed`
- `note_separated_alternate`
- `hidden_detail`
- `multihit`
- `conditional`
- `landing_expression`
- `until_landing`
- `categorical`
- `prose`
- `blank`
- `dash_variant`
- `percent_expression`
- `raw_only`
- `unclassified`

## Review Item Summary

- Grouped count: `247`
- Emitted count: `247`
- Omitted count: `0`
- Truncated: `False`
- Blocks JSON Schema redesign: `False`

## Field Summaries

### official: Dゲージ増加 > ヒット

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 64, "scalar": 2222}`
- Representative examples: `250` (scalar); `1500` (scalar); `2000` (scalar)

### official: Dゲージ減少 > ガード

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 72, "scalar": 448, "signed_frame": 1766}`
- Representative examples: `-500` (signed_frame); `-3000` (signed_frame); `-4000` (signed_frame)

### official: Dゲージ減少 > パニッシュカウンター

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 64, "scalar": 345, "signed_frame": 1877}`
- Representative examples: `-2000` (signed_frame); `-4000` (signed_frame); `-6000` (signed_frame)

### official: SAゲージ増加

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 64, "note_prefixed": 8, "raw_only": 8, "scalar": 2214}`
- Representative examples: `300` (scalar); `500` (scalar); `700` (scalar)

### official: キャンセル

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 1355, "categorical": 339, "multihit": 3, "note_prefixed": 122, "note_suffixed": 106, "raw_only": 140, "unclassified": 452}`
- Representative examples: `C` (categorical); `` (blank); `SA` (categorical)

### official: コンボ補正値

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 1437, "conditional": 170, "note_prefixed": 52, "note_separated_alternate": 3, "note_suffixed": 2, "percent_expression": 847, "raw_only": 849}`
- Representative examples: `始動補正20%` (percent_expression, raw_only); `` (blank); `コンボ補正10%` (percent_expression, raw_only)

### official: ダメージ

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"note_prefixed": 35, "note_separated_alternate": 1, "raw_only": 36, "scalar": 2250}`
- Representative examples: `300` (scalar); `600` (scalar); `700` (scalar)

### official: 備考

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 561, "conditional": 916, "landing_expression": 19, "multihit": 18, "note_prefixed": 92, "note_separated_alternate": 219, "percent_expression": 151, "prose": 437, "range": 657, "raw_only": 1725, "until_landing": 11}`
- Representative examples: `連打キャンセル対応` (raw_only); `` (blank); `ガード、空振り時硬直2F増加` (conditional, raw_only)

### official: 動作フレーム > 持続

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 429, "hidden_detail": 295, "landing_expression": 45, "multihit": 295, "note_prefixed": 2, "note_separated_alternate": 34, "note_suffixed": 10, "prose": 19, "range": 1801, "raw_only": 92, "scalar": 8, "until_landing": 45}`
- Representative examples: `5-6` (range); `4-6` (range); `6-10` (range)

### official: 動作フレーム > 発生

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 230, "note_suffixed": 6, "plus_expression": 3, "raw_only": 6, "scalar": 2047}`
- Representative examples: `5` (scalar); `4` (scalar); `6` (scalar)

### official: 動作フレーム > 硬直

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 30, "landing_expression": 452, "note_prefixed": 24, "note_separated_alternate": 4, "raw_only": 854, "scalar": 1402}`
- Representative examples: `7` (scalar); `12` (scalar); `14` (scalar)

### official: 属性

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 316, "categorical": 1944, "note_prefixed": 9, "raw_only": 1970}`
- Representative examples: `上` (categorical, raw_only); `下` (categorical, raw_only); `中` (categorical, raw_only)

### official: 技名

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"conditional": 68, "note_separated_alternate": 2, "percent_expression": 29, "prose": 8, "raw_only": 2286}`
- Representative examples: `立ち弱P （蛇突）弱` (raw_only); `立ち弱K （蛇咬脚）弱` (raw_only); `立ち中P （蛇咬手）中` (raw_only)

### official: 硬直差 > ガード

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 745, "dash_variant": 4, "note_prefixed": 5, "note_separated_alternate": 1, "range": 18, "raw_only": 6, "scalar": 172, "signed_frame": 1338, "unclassified": 3}`
- Representative examples: `-1` (signed_frame); `-3` (signed_frame); `-2` (signed_frame)

### official: 硬直差 > ヒット

- Source role: `current_fact_authority_candidate`
- Character count: `29`
- Observations: `2286`
- Shape counts: `{"blank": 573, "categorical": 983, "dash_variant": 1, "note_prefixed": 4, "range": 8, "raw_only": 4, "scalar": 619, "signed_frame": 98, "unclassified": 1}`
- Representative examples: `4` (scalar); `3` (scalar); `6` (scalar)

### supercombo: Character Vitals > Back Dash Distance

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `1.079` (scalar); `0.75` (scalar); `1.169` (scalar)

### supercombo: Character Vitals > Back Dash Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `23` (scalar); `25` (scalar); `24` (scalar)

### supercombo: Character Vitals > Back Jump Distance

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `1.60` (scalar); `1.52` (scalar); `1.68` (scalar)

### supercombo: Character Vitals > Back Walk Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `0.032` (scalar); `0.027` (scalar); `0.033` (scalar)

### supercombo: Character Vitals > Drive Rush Max Distance

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `4.049` (scalar); `3.530` (scalar); `2.867` (scalar)

### supercombo: Character Vitals > Drive Rush Min. Distance (Block)

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `2.437` (scalar); `1.722` (scalar); `2.082` (scalar)

### supercombo: Character Vitals > Drive Rush Min. Distance (Throw)

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `0.907` (scalar); `0.393` (scalar); `0.476` (scalar)

### supercombo: Character Vitals > Forward Dash Distance

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `1.300` (scalar); `1.00` (scalar); `1.578` (scalar)

### supercombo: Character Vitals > Forward Dash Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `19` (scalar); `22` (scalar); `18` (scalar)

### supercombo: Character Vitals > Forward Jump Distance

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 27, "unclassified": 2}`
- Representative examples: `2.00` (scalar); `1.90` (scalar); `2.10` (scalar)

### supercombo: Character Vitals > Forward Walk Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `0.0452` (scalar); `0.042` (scalar); `0.047` (scalar)

### supercombo: Character Vitals > HP

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 29}`
- Representative examples: `10000` (scalar); `10500` (scalar); `9000` (scalar)

### supercombo: Character Vitals > Icon

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"blank": 29}`
- Representative examples: `` (blank)

### supercombo: Character Vitals > Jump Apex

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"scalar": 28, "unclassified": 1}`
- Representative examples: `2.176` (scalar); `2.115` (scalar); `2.247` (scalar)

### supercombo: Character Vitals > Jump Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"plus_expression": 29}`
- Representative examples: `4+40+3` (plus_expression); `4+38+3` (plus_expression); `4+42+3` (plus_expression)

### supercombo: Character Vitals > Portrait

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"blank": 29}`
- Representative examples: `` (blank)

### supercombo: Character Vitals > Throw Range / Hurtbox

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `29`
- Shape counts: `{"unclassified": 29}`
- Representative examples: `0.8 / 0.33` (unclassified); `0.85 / 0.38` (unclassified); `0.9 / 0.43` (unclassified)

### supercombo: Command Normals > Active

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 14, "dash_variant": 6, "multihit": 6, "range": 2, "scalar": 106, "unclassified": 13}`
- Representative examples: `3` (scalar); `3(5)3` (unclassified); `5` (scalar)

### supercombo: Command Normals > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"blank": 1, "categorical": 32, "dash_variant": 32, "plus_expression": 69, "scalar": 9, "signed_frame": 88, "unclassified": 11}`
- Representative examples: `+1` (signed_frame, plus_expression); `0` (scalar); `+6` (signed_frame, plus_expression)

### supercombo: Command Normals > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 34, "dash_variant": 32, "plus_expression": 85, "signed_frame": 86, "unclassified": 21}`
- Representative examples: `+7` (signed_frame, plus_expression); `+8` (signed_frame, plus_expression); `-` (dash_variant, categorical)

### supercombo: Command Normals > Airborne

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 135, "dash_variant": 124, "range": 6}`
- Representative examples: `-` (dash_variant, categorical); `Until Land (FKD)` (categorical); `8-28 (FKD)` (range)

### supercombo: Command Normals > Armor

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 141, "dash_variant": 141}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Command Normals > Attack Range

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 14, "dash_variant": 14, "scalar": 76, "unclassified": 51}`
- Representative examples: `1.440` (scalar); `2.162 (2.076)` (unclassified); `1.736 (1.548)` (unclassified)

### supercombo: Command Normals > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "plus_expression": 14, "scalar": 1, "signed_frame": 103, "unclassified": 32}`
- Representative examples: `-3` (signed_frame); `-4` (signed_frame); `+2` (signed_frame, plus_expression)

### supercombo: Command Normals > Blockstun

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 10, "scalar": 116, "unclassified": 8}`
- Representative examples: `18` (scalar); `19` (scalar); `29(21)` (unclassified)

### supercombo: Command Normals > Cancel

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 134, "dash_variant": 69, "multihit": 1, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `SA` (categorical); `Sp SA` (categorical)

### supercombo: Command Normals > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 141, "dash_variant": 141}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Command Normals > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 102, "dash_variant": 102, "plus_expression": 32, "scalar": 1, "signed_frame": 32, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `+10` (signed_frame, plus_expression); `+6` (signed_frame, plus_expression)

### supercombo: Command Normals > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 102, "dash_variant": 102, "plus_expression": 27, "signed_frame": 27, "unclassified": 12}`
- Representative examples: `-` (dash_variant, categorical); `+16` (signed_frame, plus_expression); `+11` (signed_frame, plus_expression)

### supercombo: Command Normals > Damage

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 6, "scalar": 115, "unclassified": 14}`
- Representative examples: `600` (scalar); `900` (scalar); `400x2` (unclassified)

### supercombo: Command Normals > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 108, "dash_variant": 107, "percent_expression": 31, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `20% Starter` (percent_expression); `Both hits apply scaling` (categorical)

### supercombo: Command Normals > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 5, "scalar": 115, "unclassified": 15}`
- Representative examples: `1500` (scalar); `3000` (scalar); `1500x2` (unclassified)

### supercombo: Command Normals > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 4, "scalar": 116, "unclassified": 14}`
- Representative examples: `2500` (scalar); `6000` (scalar); `2000x2` (unclassified)

### supercombo: Command Normals > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 2, "unclassified": 133}`
- Representative examples: `[4000]` (unclassified); `[6000]` (unclassified); `[5000x2]` (unclassified)

### supercombo: Command Normals > Guard

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 141, "dash_variant": 6}`
- Representative examples: `H` (categorical); `LH` (categorical); `H,H` (categorical)

### supercombo: Command Normals > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "plus_expression": 77, "scalar": 5, "signed_frame": 83, "unclassified": 49}`
- Representative examples: `+3` (signed_frame, plus_expression); `+4` (signed_frame, plus_expression); `+5(+15)` (unclassified)

### supercombo: Command Normals > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 75, "dash_variant": 75, "scalar": 40, "unclassified": 26}`
- Representative examples: `-` (dash_variant, categorical); `17` (scalar); `20` (scalar)

### supercombo: Command Normals > Hitstop

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 19, "scalar": 113, "unclassified": 3}`
- Representative examples: `11` (scalar); `13` (scalar); `6,10` (multihit)

### supercombo: Command Normals > Hitstun

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 30, "dash_variant": 30, "multihit": 8, "scalar": 95, "unclassified": 8}`
- Representative examples: `24` (scalar); `26` (scalar); `31(23)` (unclassified)

### supercombo: Command Normals > Invuln

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 125, "dash_variant": 125, "multihit": 1, "range": 16}`
- Representative examples: `-` (dash_variant, categorical); `1-3 (Head), 4-14 Air (Head)` (range, multihit); `4-12 Air (Head)` (range)

### supercombo: Command Normals > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 15, "scalar": 116, "unclassified": 3}`
- Representative examples: `1` (scalar); `0` (scalar); `-` (dash_variant, categorical)

### supercombo: Command Normals > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 16, "scalar": 116, "unclassified": 2}`
- Representative examples: `0` (scalar); `0,1` (multihit); `-` (dash_variant, categorical)

### supercombo: Command Normals > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 9, "scalar": 107, "unclassified": 18}`
- Representative examples: `1` (scalar); `-` (dash_variant, categorical); `0/1` (unclassified)

### supercombo: Command Normals > Notes

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"conditional": 111, "multihit": 58, "percent_expression": 6, "prose": 140, "range": 53, "unclassified": 1}`
- Representative examples: `Relatively slow overhead that leads to combos with meaty timing or Drive Rush` (prose); `1f extra recovery on whiff; great poke that is safe on block due to pushback; hitconfirmable into Super` (conditional, prose); `8f extra recovery on whiff; Low Crush 11-26f (not airborne); 1st hit puts airborne opponents into limited juggle state (...` (range, multihit, conditional, prose)

### supercombo: Command Normals > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "signed_frame": 102, "unclassified": 32}`
- Representative examples: `-19` (signed_frame); `-22` (signed_frame); `-17` (signed_frame)

### supercombo: Command Normals > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 141, "dash_variant": 141}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Command Normals > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "plus_expression": 81, "signed_frame": 81, "unclassified": 56}`
- Representative examples: `+7` (signed_frame, plus_expression); `+8` (signed_frame, plus_expression); `+9(+19)` (unclassified)

### supercombo: Command Normals > Recovery

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "plus_expression": 4, "range": 2, "scalar": 93, "unclassified": 41}`
- Representative examples: `18` (scalar); `20(21)` (unclassified); `16(24)` (unclassified)

### supercombo: Command Normals > Startup

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"plus_expression": 6, "range": 1, "scalar": 122, "unclassified": 12}`
- Representative examples: `24` (scalar); `16` (scalar); `14` (scalar)

### supercombo: Command Normals > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 11, "dash_variant": 11, "unclassified": 130}`
- Representative examples: `250 (125)` (unclassified); `500 (250)` (unclassified); `250x2 (125x2)` (unclassified)

### supercombo: Command Normals > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 10, "dash_variant": 10, "unclassified": 131}`
- Representative examples: `500 (350)` (unclassified); `1000 (700)` (unclassified); `500x2 (350x2)` (unclassified)

### supercombo: Command Normals > Total

- Source role: `enrichment_candidate`
- Character count: `28`
- Observations: `141`
- Shape counts: `{"categorical": 18, "dash_variant": 18, "range": 2, "scalar": 99, "unclassified": 22}`
- Representative examples: `44` (scalar); `38(39)` (unclassified); `40(48)` (unclassified)

### supercombo: Drive Moves > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 58, "dash_variant": 58, "scalar": 83, "unclassified": 33}`
- Representative examples: `2` (scalar); `3` (scalar); `12 or until released` (unclassified)

### supercombo: Drive Moves > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 141, "dash_variant": 87, "range": 29, "unclassified": 4}`
- Representative examples: `1-27` (range); `Break` (categorical); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "scalar": 85, "unclassified": 2}`
- Representative examples: `2.50` (scalar); `1.978` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "signed_frame": 58, "unclassified": 29}`
- Representative examples: `-3 / Wall Splat HKD +72` (unclassified); `-6` (signed_frame); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "scalar": 83, "unclassified": 4}`
- Representative examples: `34` (scalar); `23` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 4, "scalar": 29, "unclassified": 54}`
- Representative examples: `200` (scalar); `125 recoverable` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "scalar": 29, "unclassified": 58}`
- Representative examples: `800` (scalar); `500 recoverable` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 58, "dash_variant": 58, "percent_expression": 116}`
- Representative examples: `20% Starter (Hit) 20% Multiplier (Block)` (percent_expression); `-` (dash_variant, categorical); `50% Multiplier (Perfect)` (percent_expression)

### supercombo: Drive Moves > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"multihit": 29, "signed_frame": 145}`
- Representative examples: `-10000` (signed_frame); `-20000` (signed_frame); `-5000,250~` (multihit)

### supercombo: Drive Moves > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 145, "dash_variant": 145, "scalar": 29}`
- Representative examples: `5000` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 145, "dash_variant": 145, "unclassified": 29}`
- Representative examples: `10000 [15000]` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 87}`
- Representative examples: `LH` (categorical); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "unclassified": 87}`
- Representative examples: `KD +35 / Wall Splat KD +65` (unclassified); `KD +23` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 4, "scalar": 79, "unclassified": 4}`
- Representative examples: `25` (scalar); `20` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "range": 58, "unclassified": 29}`
- Representative examples: `-` (dash_variant, categorical); `1-22 Full` (range); `1-20 Full` (range)

### supercombo: Drive Moves > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 2, "scalar": 85}`
- Representative examples: `1` (scalar); `100` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 2, "scalar": 85}`
- Representative examples: `0` (scalar); `1` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 2, "scalar": 85}`
- Representative examples: `0` (scalar); `200` (scalar); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"conditional": 174, "multihit": 62, "percent_expression": 29, "plus_expression": 29, "prose": 174}`
- Representative examples: `See Drive Impact . Airborne connect gives spinning juggle state on Punish Counter or corner Wall Splat with variable hei...` (conditional, prose); `Performed by inputting 6HPHK during blockstun; 5f extra recovery on hit; freezes the screen for 4f during startup; see D...` (conditional, prose); `Performed by holding 6HPHK on wakeup; 5f extra recovery on hit; does not have any screen freeze; see Drive Reversal .` (conditional, prose)

### supercombo: Drive Moves > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "signed_frame": 87}`
- Representative examples: `-35` (signed_frame); `-27` (signed_frame); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 87, "dash_variant": 87, "multihit": 29, "unclassified": 58}`
- Representative examples: `Crumple (Standing +21, Juggle +46, HKD +104)` (multihit); `KD +23` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"scalar": 29, "unclassified": 145}`
- Representative examples: `35` (scalar); `26(31)` (unclassified); `33(1)(11)` (unclassified)

### supercombo: Drive Moves > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"plus_expression": 29, "scalar": 145}`
- Representative examples: `26` (scalar); `20` (scalar); `18` (scalar)

### supercombo: Drive Moves > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 174, "dash_variant": 174}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Drive Moves > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"categorical": 145, "dash_variant": 145, "unclassified": 29}`
- Representative examples: `[3000(2100)]` (unclassified); `-` (dash_variant, categorical)

### supercombo: Drive Moves > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `174`
- Shape counts: `{"scalar": 29, "unclassified": 145}`
- Representative examples: `62` (scalar); `48(53)` (unclassified); `46(51)` (unclassified)

### supercombo: Hidden Arts > Active

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 4}`
- Representative examples: `-` (dash_variant, categorical); `7` (scalar); `30` (scalar)

### supercombo: Hidden Arts > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Airborne

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 5, "dash_variant": 4, "range": 1}`
- Representative examples: `Until Land (FKD)` (categorical); `-` (dash_variant, categorical); `2-69` (range)

### supercombo: Hidden Arts > Armor

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 3}`
- Representative examples: `-` (dash_variant, categorical); `Break` (categorical)

### supercombo: Hidden Arts > Attack Range

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "scalar": 1, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `0.93` (scalar); `2.12 (1st)` (unclassified)

### supercombo: Hidden Arts > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 2, "dash_variant": 1, "signed_frame": 2, "unclassified": 2}`
- Representative examples: `varies` (categorical); `-58(-57)` (unclassified); `-39` (signed_frame)

### supercombo: Hidden Arts > Blockstun

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 2, "unclassified": 3}`
- Representative examples: `26 each` (unclassified); `33(32)` (unclassified); `32 total` (unclassified)

### supercombo: Hidden Arts > Cancel

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 3, "unclassified": 1}`
- Representative examples: `150x2` (unclassified); `750` (scalar); `82x8,90 (746)` (multihit)

### supercombo: Hidden Arts > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Damage

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 3, "unclassified": 1}`
- Representative examples: `600x2` (unclassified); `2900` (scalar); `330x8,360 (3000)` (multihit)

### supercombo: Hidden Arts > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "percent_expression": 4}`
- Representative examples: `20% Starter; Combo (2 hits)` (percent_expression); `40% Minimum` (percent_expression); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "scalar": 1, "unclassified": 1}`
- Representative examples: `2000x2` (unclassified); `-` (dash_variant, categorical); `2000` (scalar)

### supercombo: Hidden Arts > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 3, "unclassified": 1}`
- Representative examples: `2500x2` (unclassified); `5000` (scalar); `500x8,1000 (5000)` (multihit)

### supercombo: Hidden Arts > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 2, "unclassified": 2}`
- Representative examples: `[3000]` (unclassified); `10000` (scalar); `1000x8,2000 (10000)` (multihit)

### supercombo: Hidden Arts > Guard

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 1}`
- Representative examples: `LH` (categorical); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 2, "dash_variant": 1, "unclassified": 4}`
- Representative examples: `varies` (categorical); `KD +25(26)` (unclassified); `KD +38` (unclassified)

### supercombo: Hidden Arts > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 6, "dash_variant": 6}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Hitstop

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 1, "unclassified": 3}`
- Representative examples: `8 each` (unclassified); `5` (scalar); `2x8,12` (multihit)

### supercombo: Hidden Arts > Hitstun

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "unclassified": 1}`
- Representative examples: `28 each` (unclassified); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Invuln

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "range": 5}`
- Representative examples: `-` (dash_variant, categorical); `1-11 Full` (range); `1-16 Full` (range)

### supercombo: Hidden Arts > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 3, "dash_variant": 3, "multihit": 1, "scalar": 2}`
- Representative examples: `0,0` (multihit); `-` (dash_variant, categorical); `0` (scalar)

### supercombo: Hidden Arts > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "multihit": 1, "scalar": 4}`
- Representative examples: `3,3` (multihit); `50` (scalar); `99` (scalar)

### supercombo: Hidden Arts > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 3, "dash_variant": 3, "scalar": 3}`
- Representative examples: `0` (scalar); `-` (dash_variant, categorical); `1` (scalar)

### supercombo: Hidden Arts > Notes

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"conditional": 6, "multihit": 3, "prose": 6, "range": 1}`
- Representative examples: `Shin Akuma only (Back Taunt~Down Taunt); forward Jump only on airborne frame 9-33; throws 2 consecutive 1-hit fireballs ...` (range, multihit, conditional, prose); `Shin Akuma only (Back Taunt~Down Taunt); teleports above opponent from anywhere on screen; 3f less recovery on whiff or ...` (conditional, prose); `Shin Akuma only (Back Taunt~Down Taunt); 9-hit Super projectile with a massive vertical hitbox; cannot be canceled into ...` (conditional, prose)

### supercombo: Hidden Arts > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "signed_frame": 2, "unclassified": 3}`
- Representative examples: `-10~` (unclassified); `-86(-85)` (unclassified); `-62` (signed_frame)

### supercombo: Hidden Arts > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "unclassified": 1}`
- Representative examples: `0.04 (1st) / 0.055 (2nd)` (unclassified); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 2, "dash_variant": 1, "unclassified": 4}`
- Representative examples: `varies` (categorical); `KD +29(30)` (unclassified); `KD +38` (unclassified)

### supercombo: Hidden Arts > Recovery

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"plus_expression": 1, "scalar": 3, "unclassified": 2}`
- Representative examples: `9(2) land` (unclassified); `88(85)` (unclassified); `41` (scalar)

### supercombo: Hidden Arts > Startup

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "range": 1, "scalar": 2, "unclassified": 2}`
- Representative examples: `8(21)` (unclassified); `5(9~10)` (range); `8` (scalar)

### supercombo: Hidden Arts > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "signed_frame": 3, "unclassified": 2}`
- Representative examples: `500x2 (250x2)` (unclassified); `-20000` (signed_frame); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "signed_frame": 3, "unclassified": 2}`
- Representative examples: `1000x2 (700x2)` (unclassified); `-20000` (signed_frame); `-` (dash_variant, categorical)

### supercombo: Hidden Arts > Total

- Source role: `enrichment_candidate`
- Character count: `2`
- Observations: `6`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 4, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `99(96)` (unclassified); `78` (scalar)

### supercombo: Normals > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 5, "scalar": 536, "unclassified": 17}`
- Representative examples: `2` (scalar); `5` (scalar); `3` (scalar)

### supercombo: Normals > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 204, "dash_variant": 204, "plus_expression": 225, "scalar": 29, "signed_frame": 310, "unclassified": 17}`
- Representative examples: `+3` (signed_frame, plus_expression); `+1` (signed_frame, plus_expression); `0` (scalar)

### supercombo: Normals > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 205, "dash_variant": 205, "plus_expression": 308, "signed_frame": 308, "unclassified": 46}`
- Representative examples: `+8` (signed_frame, plus_expression); `+7` (signed_frame, plus_expression); `+5` (signed_frame, plus_expression)

### supercombo: Normals > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 560, "dash_variant": 558}`
- Representative examples: `-` (dash_variant, categorical); `Until Land (FKD)` (categorical)

### supercombo: Normals > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 558, "dash_variant": 558, "range": 1, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `4-release (Upper Body)` (unclassified); `4-34 (Upper Body)` (range)

### supercombo: Normals > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 472, "unclassified": 86}`
- Representative examples: `0.90` (scalar); `1.269` (scalar); `1.782` (scalar)

### supercombo: Normals > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "plus_expression": 34, "scalar": 7, "signed_frame": 349, "unclassified": 197}`
- Representative examples: `-1` (signed_frame); `-3` (signed_frame); `-4` (signed_frame)

### supercombo: Normals > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 11, "scalar": 539, "unclassified": 8}`
- Representative examples: `8` (scalar); `18` (scalar); `20` (scalar)

### supercombo: Normals > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 549, "dash_variant": 253, "unclassified": 11}`
- Representative examples: `Sp SA TC` (categorical); `Sp SA` (categorical); `TC` (categorical)

### supercombo: Normals > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 560, "dash_variant": 560}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Normals > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 347, "dash_variant": 347, "plus_expression": 134, "scalar": 22, "signed_frame": 187, "unclassified": 4}`
- Representative examples: `-2` (signed_frame); `+7` (signed_frame, plus_expression); `-` (dash_variant, categorical)

### supercombo: Normals > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 347, "dash_variant": 347, "plus_expression": 205, "signed_frame": 205, "unclassified": 8}`
- Representative examples: `+3` (signed_frame, plus_expression); `+11` (signed_frame, plus_expression); `-` (dash_variant, categorical)

### supercombo: Normals > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 4, "scalar": 536, "unclassified": 18}`
- Representative examples: `300` (scalar); `600` (scalar); `800` (scalar)

### supercombo: Normals > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 380, "dash_variant": 380, "percent_expression": 179, "unclassified": 1}`
- Representative examples: `20% Starter` (percent_expression); `-` (dash_variant, categorical); `10% Starter` (percent_expression)

### supercombo: Normals > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 1, "scalar": 537, "unclassified": 20}`
- Representative examples: `250` (scalar); `1500` (scalar); `3000` (scalar)

### supercombo: Normals > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 3, "scalar": 536, "unclassified": 15}`
- Representative examples: `500` (scalar); `3000` (scalar); `5000` (scalar)

### supercombo: Normals > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 8, "dash_variant": 8, "multihit": 3, "unclassified": 549}`
- Representative examples: `[2000]` (unclassified); `[4000]` (unclassified); `[8000]` (unclassified)

### supercombo: Normals > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 560, "dash_variant": 2}`
- Representative examples: `LH` (categorical); `L` (categorical); `H` (categorical)

### supercombo: Normals > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 7, "dash_variant": 6, "plus_expression": 280, "scalar": 19, "signed_frame": 302, "unclassified": 232}`
- Representative examples: `+4` (signed_frame, plus_expression); `+3` (signed_frame, plus_expression); `+1` (signed_frame, plus_expression)

### supercombo: Normals > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 299, "dash_variant": 299, "multihit": 2, "scalar": 174, "unclassified": 85}`
- Representative examples: `12 Sp, 14 TC` (multihit); `16` (scalar); `20` (scalar)

### supercombo: Normals > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 19, "scalar": 528, "unclassified": 11}`
- Representative examples: `9` (scalar); `12` (scalar); `13` (scalar)

### supercombo: Normals > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 46, "dash_variant": 46, "multihit": 11, "scalar": 494, "unclassified": 9}`
- Representative examples: `13` (scalar); `22` (scalar); `25` (scalar)

### supercombo: Normals > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 546, "dash_variant": 546, "multihit": 2, "range": 13, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `12-23 Air (Legs/Upper Body)` (range); `11-39 Projectile (Upper Body)` (range)

### supercombo: Normals > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 19, "scalar": 538, "unclassified": 1}`
- Representative examples: `1` (scalar); `2` (scalar); `0` (scalar)

### supercombo: Normals > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 20, "scalar": 538}`
- Representative examples: `0` (scalar); `2` (scalar); `1` (scalar)

### supercombo: Normals > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 15, "scalar": 520, "unclassified": 23}`
- Representative examples: `1` (scalar); `2` (scalar); `1 [-1 PC Ground]` (unclassified)

### supercombo: Normals > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"blank": 4, "categorical": 31, "conditional": 359, "multihit": 173, "percent_expression": 1, "prose": 499, "range": 227, "unclassified": 26}`
- Representative examples: `Sinister Slide cancel: +1/-4; short range and not chainable, primarily used for the 5LP~LP Target Combo` (multihit, prose); `2 extra recovery frames on whiff/block; Sinister Slide cancel: +9/+5; moves A.K.I. forward; useful combo tool after 5MK ...` (conditional, prose); `Very good poke that can avoid some low attacks; hitconfirmable into 5HP~HP Target Combo, which is especially strong vs. ...` (multihit, prose)

### supercombo: Normals > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 9, "dash_variant": 9, "signed_frame": 352, "unclassified": 199}`
- Representative examples: `-7` (signed_frame); `-17` (signed_frame); `-22` (signed_frame)

### supercombo: Normals > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 560, "dash_variant": 560}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Normals > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 8, "dash_variant": 8, "plus_expression": 294, "signed_frame": 293, "unclassified": 258}`
- Representative examples: `+8` (signed_frame, plus_expression); `+7` (signed_frame, plus_expression); `+5` (signed_frame, plus_expression)

### supercombo: Normals > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "conditional": 1, "dash_variant": 2, "scalar": 296, "unclassified": 261}`
- Representative examples: `7` (scalar); `14(16)` (unclassified); `21` (scalar)

### supercombo: Normals > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "range": 1, "scalar": 543, "unclassified": 14}`
- Representative examples: `5` (scalar); `6` (scalar); `12` (scalar)

### supercombo: Normals > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 21, "dash_variant": 21, "multihit": 4, "unclassified": 535}`
- Representative examples: `150 (75)` (unclassified); `250 (125)` (unclassified); `500 (250)` (unclassified)

### supercombo: Normals > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 21, "dash_variant": 21, "multihit": 4, "unclassified": 535}`
- Representative examples: `300 (210)` (unclassified); `500 (350)` (unclassified); `1000 (700)` (unclassified)

### supercombo: Normals > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `560`
- Shape counts: `{"categorical": 192, "dash_variant": 192, "scalar": 300, "unclassified": 68}`
- Representative examples: `13` (scalar); `24(26)` (unclassified); `35` (scalar)

### supercombo: Prowler Stance > Active

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "multihit": 1, "scalar": 9}`
- Representative examples: `-` (dash_variant, categorical); `4` (scalar); `3` (scalar)

### supercombo: Prowler Stance > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 15}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Prowler Stance > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 15}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Prowler Stance > Airborne

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 12, "dash_variant": 12, "range": 3}`
- Representative examples: `-` (dash_variant, categorical); `7-36 (FKD)` (range); `9-30 (FKD)` (range)

### supercombo: Prowler Stance > Armor

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 14, "dash_variant": 14, "range": 1}`
- Representative examples: `-` (dash_variant, categorical); `6-16 (2-hit)` (range)

### supercombo: Prowler Stance > Attack Range

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "scalar": 5, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `2.32 / 2.60 / 3.14` (unclassified); `1.36` (scalar)

### supercombo: Prowler Stance > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "plus_expression": 3, "signed_frame": 7, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `-1` (signed_frame); `+1*` (unclassified)

### supercombo: Prowler Stance > Blockstun

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 1, "scalar": 7}`
- Representative examples: `-` (dash_variant, categorical); `21` (scalar); `13` (scalar)

### supercombo: Prowler Stance > Cancel

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 13}`
- Representative examples: `-` (dash_variant, categorical); `Chn Sp SA` (categorical); `TC` (categorical)

### supercombo: Prowler Stance > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 15}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Prowler Stance > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 14, "dash_variant": 14, "plus_expression": 1, "signed_frame": 1}`
- Representative examples: `-` (dash_variant, categorical); `+3` (signed_frame, plus_expression)

### supercombo: Prowler Stance > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 14, "dash_variant": 14, "plus_expression": 1, "signed_frame": 1}`
- Representative examples: `-` (dash_variant, categorical); `+9` (signed_frame, plus_expression)

### supercombo: Prowler Stance > Damage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "scalar": 5, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `1000` (scalar); `300` (scalar)

### supercombo: Prowler Stance > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 10, "dash_variant": 10, "percent_expression": 5}`
- Representative examples: `-` (dash_variant, categorical); `20% Starter` (percent_expression)

### supercombo: Prowler Stance > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "scalar": 7, "unclassified": 3}`
- Representative examples: `-` (dash_variant, categorical); `2000` (scalar); `300` (scalar)

### supercombo: Prowler Stance > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "scalar": 7, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `4000` (scalar); `500` (scalar)

### supercombo: Prowler Stance > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "unclassified": 10}`
- Representative examples: `-` (dash_variant, categorical); `[4000]` (unclassified); `[2000]` (unclassified)

### supercombo: Prowler Stance > Guard

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 5}`
- Representative examples: `-` (dash_variant, categorical); `LH` (categorical); `H` (categorical)

### supercombo: Prowler Stance > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "plus_expression": 3, "signed_frame": 3, "unclassified": 7}`
- Representative examples: `-` (dash_variant, categorical); `+3` (signed_frame, plus_expression); `+7*` (unclassified)

### supercombo: Prowler Stance > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 13, "dash_variant": 13, "scalar": 2}`
- Representative examples: `-` (dash_variant, categorical); `13` (scalar); `22` (scalar)

### supercombo: Prowler Stance > Hitstop

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 1, "scalar": 3, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `13 (15 CH/PC)` (unclassified); `9` (scalar)

### supercombo: Prowler Stance > Hitstun

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 11, "dash_variant": 11, "scalar": 4}`
- Representative examples: `-` (dash_variant, categorical); `25` (scalar); `19` (scalar)

### supercombo: Prowler Stance > Invuln

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 14, "dash_variant": 14, "multihit": 1, "range": 1}`
- Representative examples: `-` (dash_variant, categorical); `1-6 Air (Upper/Mid), 7-13 Air (all)` (range, multihit)

### supercombo: Prowler Stance > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 1, "scalar": 7}`
- Representative examples: `-` (dash_variant, categorical); `1` (scalar); `1,1` (multihit)

### supercombo: Prowler Stance > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 1, "scalar": 7}`
- Representative examples: `-` (dash_variant, categorical); `5` (scalar); `0` (scalar)

### supercombo: Prowler Stance > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "multihit": 1, "scalar": 7}`
- Representative examples: `-` (dash_variant, categorical); `1` (scalar); `1,1` (multihit)

### supercombo: Prowler Stance > Notes

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"conditional": 15, "multihit": 9, "prose": 15, "range": 11}`
- Representative examples: `Cannot block while in stance (counter-hit state for entire duration); Alex is in a crouching state on frame 5 onward (st...` (range, conditional, prose); `Can start exiting stance 1 frame earlier than other follow-ups; fastest total stance + exit time is 42f; Low Profile and...` (range, conditional, prose); `Distance: 1.76; cancelable into Slash Elbow (6P) on frames 1-14 (if done later, Elbow is buffered at the usual follow-up...` (range, multihit, conditional, prose)

### supercombo: Prowler Stance > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "signed_frame": 8}`
- Representative examples: `-` (dash_variant, categorical); `-20` (signed_frame); `-10` (signed_frame)

### supercombo: Prowler Stance > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 15, "dash_variant": 15}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Prowler Stance > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "unclassified": 10}`
- Representative examples: `-` (dash_variant, categorical); `KD +56` (unclassified); `+11*` (unclassified)

### supercombo: Prowler Stance > Recovery

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "plus_expression": 2, "scalar": 12}`
- Representative examples: `-` (dash_variant, categorical); `25` (scalar); `28` (scalar)

### supercombo: Prowler Stance > Startup

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 3, "dash_variant": 3, "plus_expression": 2, "scalar": 7, "unclassified": 3}`
- Representative examples: `18~` (unclassified); `-` (dash_variant, categorical); `12/15/18` (unclassified)

### supercombo: Prowler Stance > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "unclassified": 8}`
- Representative examples: `-` (dash_variant, categorical); `400 (200)` (unclassified); `150 (75)` (unclassified)

### supercombo: Prowler Stance > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "unclassified": 10}`
- Representative examples: `-` (dash_variant, categorical); `800 (560)` (unclassified); `300 (210)` (unclassified)

### supercombo: Prowler Stance > Total

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `15`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 13, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `25` (scalar); `28` (scalar)

### supercombo: SF6 Navigation > column_0

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `203`
- Shape counts: `{"categorical": 87, "conditional": 58, "prose": 87, "unclassified": 29}`
- Representative examples: `Street Fighter 6 (SF6)` (unclassified); `General` (categorical); `FAQ • Controls • HUD • Glossary • Movement • Offense • Defense • Gauges • Game Data • Patch Notes • Links` (prose)

### supercombo: Serenity Stream > Active

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 5, "unclassified": 2}`
- Representative examples: `[57~]` (unclassified); `-` (dash_variant, categorical); `5` (scalar)

### supercombo: Serenity Stream > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Airborne

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Armor

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Attack Range

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 3, "unclassified": 3}`
- Representative examples: `-` (dash_variant, categorical); `0.84` (scalar); `2.30 (1.753)` (unclassified)

### supercombo: Serenity Stream > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "signed_frame": 2, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `-3 (-23)` (unclassified); `-15(-4) [-28(-17)]` (unclassified)

### supercombo: Serenity Stream > Blockstun

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 5, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `18` (scalar); `16` (scalar)

### supercombo: Serenity Stream > Cancel

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 3}`
- Representative examples: `-` (dash_variant, categorical); `Sp SA` (categorical); `Jmp` (categorical)

### supercombo: Serenity Stream > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "plus_expression": 4, "signed_frame": 4}`
- Representative examples: `-` (dash_variant, categorical); `+5` (signed_frame, plus_expression); `+8` (signed_frame, plus_expression)

### supercombo: Serenity Stream > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "plus_expression": 4, "signed_frame": 4}`
- Representative examples: `-` (dash_variant, categorical); `+6` (signed_frame, plus_expression); `+13` (signed_frame, plus_expression)

### supercombo: Serenity Stream > Damage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 1, "scalar": 5}`
- Representative examples: `-` (dash_variant, categorical); `500` (scalar); `750` (scalar)

### supercombo: Serenity Stream > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 5, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `500` (scalar); `2000` (scalar)

### supercombo: Serenity Stream > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 5, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `1500` (scalar); `3000` (scalar)

### supercombo: Serenity Stream > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `[2000]` (unclassified); `[4000]` (unclassified)

### supercombo: Serenity Stream > Guard

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 2}`
- Representative examples: `-` (dash_variant, categorical); `LH` (categorical); `L` (categorical)

### supercombo: Serenity Stream > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "plus_expression": 1, "signed_frame": 1, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `-2 (-22)` (unclassified); `KD +34(+45) [KD +21(+32)]` (unclassified)

### supercombo: Serenity Stream > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 3, "dash_variant": 3, "scalar": 4, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `15` (scalar); `27` (scalar)

### supercombo: Serenity Stream > Hitstop

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 1, "scalar": 5}`
- Representative examples: `-` (dash_variant, categorical); `9` (scalar); `11` (scalar)

### supercombo: Serenity Stream > Hitstun

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "scalar": 3, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `19` (scalar); `31 total` (unclassified)

### supercombo: Serenity Stream > Invuln

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 7, "dash_variant": 7, "range": 1}`
- Representative examples: `23-71 Head Projectile` (range); `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 1, "scalar": 5}`
- Representative examples: `-` (dash_variant, categorical); `1` (scalar); `1,1` (multihit)

### supercombo: Serenity Stream > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 1, "scalar": 5}`
- Representative examples: `-` (dash_variant, categorical); `0` (scalar); `0,0` (multihit)

### supercombo: Serenity Stream > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 6}`
- Representative examples: `-` (dash_variant, categorical); `1` (scalar)

### supercombo: Serenity Stream > Notes

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"conditional": 8, "multihit": 7, "plus_expression": 1, "prose": 8, "range": 4}`
- Representative examples: `Crouching state 14-22f, then low profiles until exiting stance; follow-ups can be input on frame 15 at the earliest; cou...` (range, multihit, conditional, prose); `Input 214P again to manually exit stance (fastest total Serenity Stream time is 37f); cannot block while exiting stance;...` (plus_expression, multihit, conditional, prose); `No charge required to cancel into Kikoken or Spinning Bird Kick; [] refers to recovery when exiting Serenity Stream; sli...` (multihit, conditional, prose)

### supercombo: Serenity Stream > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "signed_frame": 5, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `-37` (signed_frame); `[-42(-31)]` (unclassified)

### supercombo: Serenity Stream > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 8, "dash_variant": 8}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Serenity Stream > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "plus_expression": 1, "signed_frame": 1, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `+2 (-18)` (unclassified); `KD +34(+45) [KD +21(+32)]` (unclassified)

### supercombo: Serenity Stream > Recovery

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 2, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `23(18)` (unclassified); `16[36]` (unclassified)

### supercombo: Serenity Stream > Startup

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "scalar": 6, "unclassified": 1}`
- Representative examples: `14(~)` (unclassified); `-` (dash_variant, categorical); `5` (scalar)

### supercombo: Serenity Stream > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `150 (75)` (unclassified); `150x2 (75x2)` (unclassified)

### supercombo: Serenity Stream > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `300 (210)` (unclassified); `300x2 (210x2)` (unclassified)

### supercombo: Serenity Stream > Total

- Source role: `enrichment_candidate`
- Character count: `1`
- Observations: `8`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "scalar": 1, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `25[45]` (unclassified); `36[49]` (unclassified)

### supercombo: Special Moves > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 169, "conditional": 2, "dash_variant": 145, "multihit": 62, "plus_expression": 2, "prose": 3, "range": 6, "scalar": 380, "unclassified": 215}`
- Representative examples: `-` (dash_variant, categorical); `2` (scalar); `6` (scalar)

### supercombo: Special Moves > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 838, "dash_variant": 838}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Special Moves > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 838, "dash_variant": 838}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Special Moves > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 611, "dash_variant": 524, "multihit": 11, "range": 226, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `9-45 (FKD)` (range); `13-49 (FKD)` (range)

### supercombo: Special Moves > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 813, "dash_variant": 810, "multihit": 3, "range": 21, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `6-13(19)` (range); `3-10(19)` (range)

### supercombo: Special Moves > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 352, "dash_variant": 352, "multihit": 3, "range": 6, "scalar": 132, "unclassified": 345}`
- Representative examples: `-` (dash_variant, categorical); `1.77 (1.08)` (unclassified); `1.59` (scalar)

### supercombo: Special Moves > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 161, "dash_variant": 159, "plus_expression": 63, "range": 5, "scalar": 4, "signed_frame": 475, "unclassified": 193}`
- Representative examples: `-10` (signed_frame); `+1` (signed_frame, plus_expression); `-16(-11)` (unclassified)

### supercombo: Special Moves > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 151, "dash_variant": 151, "multihit": 41, "range": 4, "scalar": 408, "unclassified": 235}`
- Representative examples: `26` (scalar); `30 total` (unclassified); `20` (scalar)

### supercombo: Special Moves > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 407, "dash_variant": 377, "multihit": 1, "unclassified": 430}`
- Representative examples: `SA3` (unclassified); `SA2 SA3` (unclassified); `-` (dash_variant, categorical)

### supercombo: Special Moves > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 154, "dash_variant": 154, "multihit": 187, "range": 4, "scalar": 385, "unclassified": 112}`
- Representative examples: `125` (scalar); `75,100` (multihit); `200` (scalar)

### supercombo: Special Moves > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 838, "dash_variant": 838}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Special Moves > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 838, "dash_variant": 838}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Special Moves > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 86, "dash_variant": 86, "multihit": 225, "range": 9, "scalar": 327, "unclassified": 196}`
- Representative examples: `500` (scalar); `300,400` (multihit); `500[800]` (unclassified)

### supercombo: Special Moves > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 531, "dash_variant": 526, "percent_expression": 273, "unclassified": 34}`
- Representative examples: `-` (dash_variant, categorical); `20% Starter` (percent_expression); `Combo (2 hits)` (unclassified)

### supercombo: Special Moves > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 115, "dash_variant": 115, "multihit": 71, "scalar": 314, "signed_frame": 196, "unclassified": 142}`
- Representative examples: `1000` (scalar); `-20000` (signed_frame); `1000 [TB: 5000]` (unclassified)

### supercombo: Special Moves > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 151, "dash_variant": 151, "multihit": 85, "range": 1, "scalar": 404, "unclassified": 197}`
- Representative examples: `2500` (scalar); `1000x2` (unclassified); `1000` (scalar)

### supercombo: Special Moves > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 114, "dash_variant": 114, "multihit": 71, "scalar": 1, "unclassified": 652}`
- Representative examples: `[2000]` (unclassified); `[2500x2]` (unclassified); `[2500]` (unclassified)

### supercombo: Special Moves > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 838, "dash_variant": 96}`
- Representative examples: `LH` (categorical); `-` (dash_variant, categorical); `T` (categorical)

### supercombo: Special Moves > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 90, "dash_variant": 84, "plus_expression": 94, "range": 37, "scalar": 6, "signed_frame": 139, "unclassified": 566}`
- Representative examples: `-5` (signed_frame); `KD +45` (unclassified); `-4 [KD +38]` (unclassified)

### supercombo: Special Moves > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 387, "dash_variant": 387, "multihit": 1, "range": 24, "scalar": 255, "unclassified": 171}`
- Representative examples: `4 SA` (unclassified); `12 SA` (unclassified); `8[13] SA` (unclassified)

### supercombo: Special Moves > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 139, "dash_variant": 139, "multihit": 311, "scalar": 332, "unclassified": 56}`
- Representative examples: `(8)` (unclassified); `(7,6)` (multihit); `3[8(13)]` (unclassified)

### supercombo: Special Moves > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 609, "dash_variant": 609, "multihit": 23, "scalar": 138, "unclassified": 68}`
- Representative examples: `31` (scalar); `-` (dash_variant, categorical); `32` (scalar)

### supercombo: Special Moves > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 619, "dash_variant": 619, "multihit": 36, "prose": 1, "range": 216, "unclassified": 3}`
- Representative examples: `-` (dash_variant, categorical); `6-16 Air` (range); `19-23 Lower Body Projectile` (range)

### supercombo: Special Moves > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 140, "dash_variant": 140, "multihit": 286, "scalar": 364, "unclassified": 48}`
- Representative examples: `1` (scalar); `0,2` (multihit); `3` (scalar)

### supercombo: Special Moves > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 131, "dash_variant": 131, "multihit": 256, "scalar": 383, "unclassified": 68}`
- Representative examples: `1` (scalar); `2,2` (multihit); `6` (scalar)

### supercombo: Special Moves > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 141, "dash_variant": 141, "multihit": 204, "range": 1, "scalar": 388, "unclassified": 104}`
- Representative examples: `1` (scalar); `0,1` (multihit); `[1]` (unclassified)

### supercombo: Special Moves > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 4, "conditional": 759, "multihit": 418, "percent_expression": 50, "plus_expression": 8, "prose": 826, "range": 293, "unclassified": 5}`
- Representative examples: `Slow-moving 1-hit projectile; can be extremely plus on hit/block from longer ranges or when used with meaty timing; pois...` (range, conditional, prose); `Slow-moving 2-hit OD projectile; can be extremely plus on block from longer ranges or when used with meaty timing; poiso...` (range, conditional, prose); `Poisons opponent on hit; refers to the non-burst version (projectile dissipates, causing the whip to strike the opponent...` (multihit, conditional, prose)

### supercombo: Special Moves > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 171, "dash_variant": 171, "multihit": 1, "plus_expression": 5, "range": 4, "scalar": 1, "signed_frame": 439, "unclassified": 222}`
- Representative examples: `-25` (signed_frame); `-7` (signed_frame); `-34(-25)` (unclassified)

### supercombo: Special Moves > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 741, "dash_variant": 741, "multihit": 7, "plus_expression": 3, "range": 16, "scalar": 62, "unclassified": 19}`
- Representative examples: `0.04` (scalar); `0.02 (1-3f), 0.04 (4f~)` (range, multihit); `-` (dash_variant, categorical)

### supercombo: Special Moves > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 92, "dash_variant": 86, "plus_expression": 117, "range": 32, "scalar": 2, "signed_frame": 125, "unclassified": 587}`
- Representative examples: `-1` (signed_frame); `KD +45` (unclassified); `0 [KD +38]` (unclassified)

### supercombo: Special Moves > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 25, "conditional": 2, "dash_variant": 25, "plus_expression": 180, "range": 4, "scalar": 444, "unclassified": 185}`
- Representative examples: `35` (scalar); `28` (scalar); `34` (scalar)

### supercombo: Special Moves > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 9, "dash_variant": 9, "plus_expression": 86, "range": 17, "scalar": 622, "unclassified": 106}`
- Representative examples: `17` (scalar); `16` (scalar); `13` (scalar)

### supercombo: Special Moves > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 151, "dash_variant": 151, "multihit": 116, "range": 1, "unclassified": 570}`
- Representative examples: `300 (150)` (unclassified); `150x2 (75x2)` (unclassified); `150 (75)` (unclassified)

### supercombo: Special Moves > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 82, "dash_variant": 82, "multihit": 149, "plus_expression": 2, "range": 8, "unclassified": 597}`
- Representative examples: `600 (420)` (unclassified); `300x2 (210x2)` (unclassified); `300 (210)` (unclassified)

### supercombo: Special Moves > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `838`
- Shape counts: `{"categorical": 85, "dash_variant": 85, "range": 12, "scalar": 636, "unclassified": 105}`
- Representative examples: `52` (scalar); `44` (scalar); `48` (scalar)

### supercombo: Super Arts > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 17, "dash_variant": 14, "multihit": 12, "plus_expression": 3, "range": 1, "scalar": 115, "unclassified": 32}`
- Representative examples: `3` (scalar); `53(28)12` (unclassified); `5` (scalar)

### supercombo: Super Arts > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 179}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Super Arts > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 179}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Super Arts > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 156, "dash_variant": 147, "multihit": 3, "range": 22, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `2-12` (range); `12-27 (FKD)` (range)

### supercombo: Super Arts > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 177, "dash_variant": 34, "range": 2}`
- Representative examples: `Break` (categorical); `-` (dash_variant, categorical); `Break (all)` (categorical)

### supercombo: Super Arts > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 67, "dash_variant": 67, "scalar": 31, "unclassified": 81}`
- Representative examples: `1.853` (scalar); `-` (dash_variant, categorical); `1.948` (scalar)

### supercombo: Super Arts > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 41, "dash_variant": 41, "plus_expression": 1, "signed_frame": 108, "unclassified": 30}`
- Representative examples: `-46` (signed_frame); `-19~` (unclassified); `-36` (signed_frame)

### supercombo: Super Arts > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 37, "dash_variant": 37, "multihit": 5, "range": 3, "scalar": 79, "unclassified": 55}`
- Representative examples: `25` (scalar); `116~121 total` (range); `22` (scalar)

### supercombo: Super Arts > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 177}`
- Representative examples: `-` (dash_variant, categorical); `Sp*` (categorical); `Jmp` (categorical)

### supercombo: Super Arts > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 41, "dash_variant": 41, "multihit": 35, "range": 6, "scalar": 77, "unclassified": 26}`
- Representative examples: `500` (scalar); `125,80x6,145 (750)` (multihit); `1000` (scalar)

### supercombo: Super Arts > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 179}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Super Arts > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 179}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Super Arts > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "multihit": 31, "range": 10, "scalar": 89, "unclassified": 45}`
- Representative examples: `850,950 (1800)` (multihit); `300,200x6,1000 (2500)` (multihit); `4000` (scalar)

### supercombo: Super Arts > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "percent_expression": 174, "prose": 3}`
- Representative examples: `30% Minimum` (percent_expression); `40% Minimum` (percent_expression); `50% Minimum; 10% Immediate (Sp)` (percent_expression)

### supercombo: Super Arts > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 174, "dash_variant": 174, "signed_frame": 1, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `1000 oH (500 oB)` (unclassified); `[Heal: 10000]` (unclassified)

### supercombo: Super Arts > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 37, "dash_variant": 37, "multihit": 32, "range": 2, "scalar": 81, "unclassified": 27}`
- Representative examples: `2500` (scalar); `625x8 (5000)` (unclassified); `7500` (scalar)

### supercombo: Super Arts > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "multihit": 30, "range": 3, "scalar": 112, "unclassified": 30}`
- Representative examples: `5000` (scalar); `1500,500x6,5500 (10000)` (multihit); `15000` (scalar)

### supercombo: Super Arts > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 179, "dash_variant": 27}`
- Representative examples: `LH` (categorical); `-` (dash_variant, categorical); `T` (categorical)

### supercombo: Super Arts > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 7, "dash_variant": 5, "plus_expression": 16, "range": 6, "signed_frame": 16, "unclassified": 150}`
- Representative examples: `KD +30` (unclassified); `HKD +30` (unclassified); `HKD +21` (unclassified)

### supercombo: Super Arts > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 176, "dash_variant": 176, "range": 1, "scalar": 1, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `41*` (unclassified); `28` (scalar)

### supercombo: Super Arts > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"blank": 1, "categorical": 18, "dash_variant": 18, "multihit": 51, "scalar": 79, "unclassified": 30}`
- Representative examples: `` (blank); `-` (dash_variant, categorical); `13` (scalar)

### supercombo: Super Arts > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 159, "dash_variant": 159, "scalar": 18, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `48` (scalar); `35` (scalar)

### supercombo: Super Arts > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 23, "dash_variant": 23, "multihit": 13, "range": 154, "unclassified": 2}`
- Representative examples: `1-12 Strike/Throw` (range); `-` (dash_variant, categorical); `1-12 Full` (range)

### supercombo: Super Arts > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 75, "dash_variant": 75, "multihit": 36, "scalar": 53, "unclassified": 15}`
- Representative examples: `0,99` (multihit); `-` (dash_variant, categorical); `1` (scalar)

### supercombo: Super Arts > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 16, "dash_variant": 16, "multihit": 10, "scalar": 143, "unclassified": 10}`
- Representative examples: `99` (scalar); `50` (scalar); `-` (dash_variant, categorical)

### supercombo: Super Arts > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 96, "dash_variant": 96, "multihit": 10, "scalar": 61, "unclassified": 12}`
- Representative examples: `1` (scalar); `0,99` (multihit); `-` (dash_variant, categorical)

### supercombo: Super Arts > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"conditional": 151, "multihit": 78, "percent_expression": 46, "plus_expression": 1, "prose": 178, "range": 28, "unclassified": 1}`
- Representative examples: `Poisons opponent on hit; good anti-air hitbox but cannot hit cross-up; transition to a cinematic on hit; very short hori...` (multihit, conditional, prose); `No invincibility; Super-priority projectile hitboxes; button strength determines distance (LP close/mid range, MP mid ra...` (multihit, conditional, prose); `Cannot hit cross-up; cinematic time regenerates ~2.2 Drive bars for A.K.I.` (prose)

### supercombo: Super Arts > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 41, "dash_variant": 41, "plus_expression": 4, "signed_frame": 111, "unclassified": 27}`
- Representative examples: `-69` (signed_frame); `-19(-55)` (unclassified); `-59` (signed_frame)

### supercombo: Super Arts > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 166, "dash_variant": 166, "multihit": 1, "range": 1, "scalar": 5, "unclassified": 7}`
- Representative examples: `-` (dash_variant, categorical); `LK 0.014 / MK 0.021 / HK 0.04` (unclassified); `0.03 / 0.045 / 0.09` (unclassified)

### supercombo: Super Arts > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 32, "dash_variant": 30, "plus_expression": 3, "range": 5, "signed_frame": 3, "unclassified": 139}`
- Representative examples: `KD +30` (unclassified); `HKD +30` (unclassified); `HKD +21` (unclassified)

### supercombo: Super Arts > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 1, "dash_variant": 1, "plus_expression": 16, "scalar": 135, "unclassified": 27}`
- Representative examples: `68` (scalar); `54` (scalar); `58` (scalar)

### supercombo: Super Arts > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"plus_expression": 7, "range": 2, "scalar": 150, "unclassified": 20}`
- Representative examples: `10` (scalar); `7` (scalar); `9` (scalar)

### supercombo: Super Arts > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 34, "dash_variant": 34, "signed_frame": 145}`
- Representative examples: `-10000` (signed_frame); `-20000` (signed_frame); `-30000` (signed_frame)

### supercombo: Super Arts > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"categorical": 24, "dash_variant": 24, "signed_frame": 155}`
- Representative examples: `-10000` (signed_frame); `-20000` (signed_frame); `-30000` (signed_frame)

### supercombo: Super Arts > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `179`
- Shape counts: `{"blank": 20, "categorical": 9, "dash_variant": 9, "range": 2, "scalar": 139, "unclassified": 9}`
- Representative examples: `80` (scalar); `153` (scalar); `70` (scalar)

### supercombo: Target Combos > Active

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "scalar": 105, "unclassified": 8}`
- Representative examples: `2` (scalar); `3` (scalar); `4(12)3` (unclassified)

### supercombo: Target Combos > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 118}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Target Combos > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 118}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Target Combos > Airborne

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 115, "dash_variant": 113, "range": 3}`
- Representative examples: `-` (dash_variant, categorical); `Until Land (FKD after bounce)` (categorical); `10-35 (FKD)` (range)

### supercombo: Target Combos > Armor

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 118}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Target Combos > Attack Range

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 97, "dash_variant": 97, "scalar": 11, "unclassified": 10}`
- Representative examples: `-` (dash_variant, categorical); `1.75 (1.65)` (unclassified); `1.96 (1.88)` (unclassified)

### supercombo: Target Combos > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 12, "conditional": 4, "dash_variant": 12, "plus_expression": 3, "signed_frame": 92, "unclassified": 10}`
- Representative examples: `-3` (signed_frame); `-15` (signed_frame); `-12(-19)` (unclassified)

### supercombo: Target Combos > Blockstun

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 12, "dash_variant": 12, "multihit": 1, "scalar": 100, "unclassified": 5}`
- Representative examples: `16` (scalar); `17` (scalar); `21` (scalar)

### supercombo: Target Combos > Cancel

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 116, "dash_variant": 51, "unclassified": 2}`
- Representative examples: `Sp SA` (categorical); `-` (dash_variant, categorical); `PS*` (categorical)

### supercombo: Target Combos > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 118}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Target Combos > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 89, "dash_variant": 89, "plus_expression": 28, "signed_frame": 28, "unclassified": 1}`
- Representative examples: `+4` (signed_frame, plus_expression); `-` (dash_variant, categorical); `+1` (signed_frame, plus_expression)

### supercombo: Target Combos > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 89, "dash_variant": 89, "plus_expression": 13, "signed_frame": 13, "unclassified": 16}`
- Representative examples: `+6` (signed_frame, plus_expression); `-` (dash_variant, categorical); `KD +65` (unclassified)

### supercombo: Target Combos > Damage

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "multihit": 3, "scalar": 67, "unclassified": 43}`
- Representative examples: `300(240)` (unclassified); `400` (scalar); `1200 (840)` (unclassified)

### supercombo: Target Combos > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 98, "dash_variant": 98, "multihit": 2, "percent_expression": 7, "prose": 1, "unclassified": 11}`
- Representative examples: `-` (dash_variant, categorical); `30% Immediate` (percent_expression); `Combo (2 hits, 2nd hit only); each hit scales separately` (multihit, prose)

### supercombo: Target Combos > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 2, "dash_variant": 2, "multihit": 2, "scalar": 103, "unclassified": 11}`
- Representative examples: `500` (scalar); `3000 [TB: 5000]` (unclassified); `1500` (scalar)

### supercombo: Target Combos > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 13, "dash_variant": 13, "multihit": 1, "scalar": 100, "unclassified": 4}`
- Representative examples: `1000` (scalar); `6000` (scalar); `3000` (scalar)

### supercombo: Target Combos > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 31, "dash_variant": 31, "unclassified": 87}`
- Representative examples: `[4000]` (unclassified); `[10000]` (unclassified); `[5000]` (unclassified)

### supercombo: Target Combos > Guard

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 8}`
- Representative examples: `LH` (categorical); `L` (categorical); `H` (categorical)

### supercombo: Target Combos > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 9, "conditional": 3, "dash_variant": 9, "plus_expression": 26, "range": 1, "scalar": 2, "signed_frame": 41, "unclassified": 62}`
- Representative examples: `+1` (signed_frame, plus_expression); `KD +34[+54]` (unclassified); `KD +21` (unclassified)

### supercombo: Target Combos > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 55, "conditional": 1, "dash_variant": 55, "range": 24, "scalar": 21, "unclassified": 17}`
- Representative examples: `32~33 (13)` (range); `-` (dash_variant, categorical); `50(18)` (unclassified)

### supercombo: Target Combos > Hitstop

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 6, "dash_variant": 6, "multihit": 6, "scalar": 106}`
- Representative examples: `10` (scalar); `13` (scalar); `11,13` (multihit)

### supercombo: Target Combos > Hitstun

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 67, "dash_variant": 67, "scalar": 51}`
- Representative examples: `18` (scalar); `-` (dash_variant, categorical); `24` (scalar)

### supercombo: Target Combos > Invuln

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 115, "dash_variant": 115, "range": 3}`
- Representative examples: `-` (dash_variant, categorical); `20-40 Full (hit)` (range); `1-25 Full` (range)

### supercombo: Target Combos > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 22, "dash_variant": 22, "multihit": 5, "scalar": 91}`
- Representative examples: `1` (scalar); `1,1` (multihit); `-` (dash_variant, categorical)

### supercombo: Target Combos > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 19, "dash_variant": 19, "multihit": 7, "scalar": 92}`
- Representative examples: `1` (scalar); `4` (scalar); `3` (scalar)

### supercombo: Target Combos > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 31, "dash_variant": 31, "multihit": 3, "scalar": 84}`
- Representative examples: `1` (scalar); `1,1` (multihit); `-` (dash_variant, categorical)

### supercombo: Target Combos > Notes

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"blank": 1, "categorical": 4, "conditional": 92, "multihit": 40, "percent_expression": 2, "prose": 113, "range": 7}`
- Representative examples: `2f extra recovery on block; 2nd LP can be input with any non-crouching direction; () refers to scaled damage from 5LP co...` (multihit, conditional, prose); `5f extra recovery on block; poisons the opponent on hit; triggers Toxic Blossom, launching opponent into limited juggle ...` (multihit, conditional, prose); `() refers to scaled damage starting from 5MP (full sequence on hit does the same damage as just a counter-hit on the HP ...` (multihit, conditional, prose)

### supercombo: Target Combos > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 64, "dash_variant": 64, "signed_frame": 49, "unclassified": 5}`
- Representative examples: `-17` (signed_frame); `-` (dash_variant, categorical); `-22` (signed_frame)

### supercombo: Target Combos > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 118, "dash_variant": 118}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Target Combos > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 26, "conditional": 1, "dash_variant": 26, "plus_expression": 39, "scalar": 1, "signed_frame": 40, "unclassified": 50}`
- Representative examples: `+5` (signed_frame, plus_expression); `KD +34[+54]` (unclassified); `KD +21` (unclassified)

### supercombo: Target Combos > Recovery

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"plus_expression": 3, "scalar": 92, "unclassified": 23}`
- Representative examples: `15(17)` (unclassified); `24(29)` (unclassified); `21` (scalar)

### supercombo: Target Combos > Startup

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 4, "dash_variant": 4, "range": 3, "scalar": 111}`
- Representative examples: `8` (scalar); `14` (scalar); `15` (scalar)

### supercombo: Target Combos > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 12, "dash_variant": 12, "multihit": 3, "unclassified": 103}`
- Representative examples: `200 (100)` (unclassified); `300 (150)` (unclassified); `500 (250)` (unclassified)

### supercombo: Target Combos > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 5, "dash_variant": 5, "multihit": 3, "unclassified": 110}`
- Representative examples: `400 (280)` (unclassified); `600 (420)` (unclassified); `1000 (700)` (unclassified)

### supercombo: Target Combos > Total

- Source role: `enrichment_candidate`
- Character count: `26`
- Observations: `118`
- Shape counts: `{"categorical": 9, "dash_variant": 9, "scalar": 97, "unclassified": 12}`
- Representative examples: `24(26)` (unclassified); `40(45)` (unclassified); `38` (scalar)

### supercombo: Taunts > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 100, "dash_variant": 100, "scalar": 8, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `32` (scalar); `2` (scalar)

### supercombo: Taunts > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 108, "dash_variant": 108, "range": 2}`
- Representative examples: `-` (dash_variant, categorical); `88-266` (range); `85-139` (range)

### supercombo: Taunts > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 109, "dash_variant": 109, "scalar": 1}`
- Representative examples: `-` (dash_variant, categorical); `0.79` (scalar)

### supercombo: Taunts > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "signed_frame": 6}`
- Representative examples: `-` (dash_variant, categorical); `-239` (signed_frame); `-65` (signed_frame)

### supercombo: Taunts > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 103, "dash_variant": 103, "scalar": 5, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `26` (scalar); `7` (scalar)

### supercombo: Taunts > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 108, "dash_variant": 108, "scalar": 2}`
- Representative examples: `-` (dash_variant, categorical); `150` (scalar); `125` (scalar)

### supercombo: Taunts > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 102, "dash_variant": 102, "multihit": 1, "scalar": 6, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `600` (scalar); `300` (scalar)

### supercombo: Taunts > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "multihit": 2, "scalar": 4}`
- Representative examples: `-` (dash_variant, categorical); `1000` (scalar); `300` (scalar)

### supercombo: Taunts > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "multihit": 1, "scalar": 4, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `2500` (scalar); `600` (scalar)

### supercombo: Taunts > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "multihit": 1, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `[2000]` (unclassified); `[5000]` (unclassified)

### supercombo: Taunts > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 103}`
- Representative examples: `-` (dash_variant, categorical); `LH` (categorical)

### supercombo: Taunts > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 103, "dash_variant": 102, "signed_frame": 2, "unclassified": 5}`
- Representative examples: `-` (dash_variant, categorical); `KD -197` (unclassified); `-58` (signed_frame)

### supercombo: Taunts > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 103, "dash_variant": 103, "scalar": 3, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `8` (scalar); `9(25)` (unclassified)

### supercombo: Taunts > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 108, "dash_variant": 108, "scalar": 2}`
- Representative examples: `-` (dash_variant, categorical); `14` (scalar); `19` (scalar)

### supercombo: Taunts > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 109, "dash_variant": 109, "range": 1}`
- Representative examples: `-` (dash_variant, categorical); `596-693 Full` (range)

### supercombo: Taunts > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 105, "dash_variant": 105, "multihit": 2, "scalar": 3}`
- Representative examples: `-` (dash_variant, categorical); `1` (scalar); `1x7,99` (multihit)

### supercombo: Taunts > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 105, "dash_variant": 105, "scalar": 3, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `2` (scalar); `0` (scalar)

### supercombo: Taunts > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 105, "dash_variant": 105, "scalar": 3, "unclassified": 2}`
- Representative examples: `-` (dash_variant, categorical); `2` (scalar); `1` (scalar)

### supercombo: Taunts > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 1, "conditional": 29, "multihit": 10, "prose": 43, "range": 5, "raw_only": 1, "unclassified": 61}`
- Representative examples: `"The master's prized poison... ahh, a perfect, beautiful, most brilliantly crafted poison! Now you'll get a taste."; bui...` (multihit, conditional, prose); `"Time for some experimentation... I bet poison would work wonders on you."` (conditional, prose); `"Isn't he wonderful? Ahhh~"; "Ugh, you're a trifling little pest." bubbles have a large projectile hitbox behind A.K.I.;...` (conditional, prose)

### supercombo: Taunts > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "signed_frame": 6}`
- Representative examples: `-` (dash_variant, categorical); `-254` (signed_frame); `-70` (signed_frame)

### supercombo: Taunts > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 110, "dash_variant": 110}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Taunts > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 103, "dash_variant": 102, "signed_frame": 1, "unclassified": 6}`
- Representative examples: `-` (dash_variant, categorical); `KD -197` (unclassified); `KD +35 Crumple` (unclassified)

### supercombo: Taunts > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 98, "dash_variant": 98, "scalar": 11, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `258(264)` (unclassified); `45` (scalar)

### supercombo: Taunts > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"plus_expression": 1, "range": 2, "scalar": 10, "unclassified": 97}`
- Representative examples: `611 (total)` (unclassified); `484 (total)` (unclassified); `175` (scalar)

### supercombo: Taunts > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 104, "dash_variant": 104, "multihit": 2, "unclassified": 4}`
- Representative examples: `-` (dash_variant, categorical); `300 (150)` (unclassified); `150 (75)` (unclassified)

### supercombo: Taunts > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"categorical": 102, "dash_variant": 102, "multihit": 4, "unclassified": 4}`
- Representative examples: `1000x5,5000 (10000)` (multihit); `-` (dash_variant, categorical); `600 (420)` (unclassified)

### supercombo: Taunts > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `110`
- Shape counts: `{"range": 2, "scalar": 106, "unclassified": 2}`
- Representative examples: `611` (scalar); `484` (scalar); `464` (scalar)

### supercombo: Throws > Active

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"scalar": 74}`
- Representative examples: `3` (scalar)

### supercombo: Throws > After DR Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > After DR Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Airborne

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Armor

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Attack Range

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"scalar": 74}`
- Representative examples: `0.80` (scalar); `0.85` (scalar); `0.90` (scalar)

### supercombo: Throws > Block Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Blockstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Cancel

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Chip Dmg

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > DR Cancel Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > DR Cancel Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Damage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"multihit": 1, "unclassified": 73}`
- Representative examples: `1200 (2040)` (unclassified); `1300 (2210)` (unclassified); `1082 (1838)` (unclassified)

### supercombo: Throws > Dmg Scaling

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 9, "dash_variant": 9, "percent_expression": 65}`
- Representative examples: `20% Immediate` (percent_expression); `20% Starter (3rd hit); 20% Immediate` (percent_expression); `-` (dash_variant, categorical)

### supercombo: Throws > Drive Gain

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"multihit": 1, "scalar": 70, "unclassified": 3}`
- Representative examples: `2000` (scalar); `7000 / 12000 (DL4)` (unclassified); `1000x2` (unclassified)

### supercombo: Throws > DriveDmg Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > DriveDmg Hit [PC]

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"unclassified": 74}`
- Representative examples: `[10000]` (unclassified); `[5000x2]` (unclassified)

### supercombo: Throws > Guard

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74}`
- Representative examples: `T` (categorical)

### supercombo: Throws > Hit Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"unclassified": 74}`
- Representative examples: `KD +19` (unclassified); `KD +20` (unclassified); `KD +28` (unclassified)

### supercombo: Throws > Hitconfirm Window

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Hitstop

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Hitstun

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Invuln

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Juggle Increase

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Juggle Limit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Juggle Start

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 69, "dash_variant": 69, "multihit": 2, "scalar": 2, "unclassified": 1}`
- Representative examples: `-` (dash_variant, categorical); `5 (DR: 0)` (unclassified); `2` (scalar)

### supercombo: Throws > Notes

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"conditional": 70, "multihit": 51, "percent_expression": 65, "prose": 74, "range": 3}`
- Representative examples: `Can walk 16-17f for a corner throw loop (strict timing to beat 4f normals); 1f more lenient vs. Marisa and 2f more lenie...` (range, conditional, percent_expression, prose); `Side switch; after corner side switch, can Drive Rush for a true strike/throw mixup (auto-timed 5MP becomes +11 oH / +5 ...` (multihit, conditional, percent_expression, prose); `No true throw loop without Drive Rush (can dash + LP Power Bomb, dash up into spaced normals, or use Drive Rush for bett...` (multihit, conditional, percent_expression, prose)

### supercombo: Throws > Perfect Parry Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Projectile Speed

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Punish Advantage

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"unclassified": 74}`
- Representative examples: `HKD +19` (unclassified); `HKD +20` (unclassified); `HKD +28` (unclassified)

### supercombo: Throws > Recovery

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"scalar": 65, "unclassified": 9}`
- Representative examples: `23` (scalar); `3 land` (unclassified)

### supercombo: Throws > Startup

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"scalar": 74}`
- Representative examples: `5` (scalar)

### supercombo: Throws > Super Gain Blk

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 74, "dash_variant": 74}`
- Representative examples: `-` (dash_variant, categorical)

### supercombo: Throws > Super Gain Hit

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"multihit": 1, "unclassified": 73}`
- Representative examples: `2000(1400) [4000(2800)]` (unclassified); `1000x2(700x2) [2000x2(1400x2)]` (unclassified); `1800,200(1260,140) [3800,200(2660,140)]` (multihit)

### supercombo: Throws > Total

- Source role: `enrichment_candidate`
- Character count: `29`
- Observations: `74`
- Shape counts: `{"categorical": 9, "dash_variant": 9, "scalar": 65}`
- Representative examples: `30` (scalar); `-` (dash_variant, categorical)

## Review Items

- `unclassified_expression` / `supercombo` / `Special Moves > DriveDmg Hit [PC]`: 652 observations; examples: `[2000]`, `[2500x2]`, `[2500]`, `[2000x2]`, `[5000]`
- `unclassified_expression` / `supercombo` / `Special Moves > Super Gain Hit`: 597 observations; examples: `600 (420)`, `300x2 (210x2)`, `300 (210)`, `900 (630)`, `200x4 (140x4)`
- `unclassified_expression` / `supercombo` / `Special Moves > Punish Advantage`: 587 observations; examples: `KD +45`, `0 [KD +38]`, `KD +42`, `KD +43(+57)`, `KD +40`
- `unclassified_expression` / `supercombo` / `Special Moves > Super Gain Blk`: 570 observations; examples: `300 (150)`, `150x2 (75x2)`, `150 (75)`, `450 (225)`, `250 (125)`
- `unclassified_expression` / `supercombo` / `Special Moves > Hit Advantage`: 566 observations; examples: `KD +45`, `-4 [KD +38]`, `KD +42`, `KD +40`, `+1(+3) [KD +44(46)]`
- `unclassified_expression` / `supercombo` / `Normals > DriveDmg Hit [PC]`: 549 observations; examples: `[2000]`, `[4000]`, `[8000]`, `[6000]`, `[10000]`
- `unclassified_expression` / `supercombo` / `Normals > Super Gain Blk`: 535 observations; examples: `150 (75)`, `250 (125)`, `500 (250)`, `350 (175)`, `300 (150)`
- `unclassified_expression` / `supercombo` / `Normals > Super Gain Hit`: 535 observations; examples: `300 (210)`, `500 (350)`, `1000 (700)`, `700 (490)`, `600 (420)`
- `unclassified_expression` / `official` / `キャンセル`: 452 observations; examples: `SA3`, `SA2`
- `unclassified_expression` / `supercombo` / `Special Moves > Cancel`: 430 observations; examples: `SA3`, `SA2 SA3`, `[TB: SA2 SA3]`, `SA2* SA3*`, `SA3 (2nd)`
- `unclassified_expression` / `supercombo` / `Special Moves > Attack Range`: 345 observations; examples: `1.77 (1.08)`, `1.70 (1.65)`, `2.11 (1.97)`, `2.10 (1.79)`, `1.75 (1.48)`
- `source_specific_expression` / `official` / `備考`: 311 observations; examples: `ヒット時毒状態30-36F専用技でキャンセル可※35-52F OD版蛇軽功でキャンセル可`, `ヒット時毒状態毒状態中にヒット時毒破裂※毒破裂時ダメージ800/吹き飛びダウン飛び道具相殺判定あり（1回）`, `ヒット時毒状態34-35F専用技でキャンセル可※32-33F OD版蛇軽功でキャンセル可`, `ヒット時毒状態毒状態中にヒット時毒破裂※毒破裂時ダメージ800/吹き飛びダウン飛び道具相殺判定あり（1回）パニッシュカウンター時に膝崩れダウンに ＋16※毒破裂時＋22`, `ヒット時毒状態毒状態中にヒット時毒破裂※毒破裂時ダメージ700/膝崩れ飛び道具相殺判定あり（1回）`
- `unclassified_expression` / `supercombo` / `Normals > Recovery`: 261 observations; examples: `14(16)`, `15(17)`, `3 land`, `16(20)`, `17(22)`
- `unclassified_expression` / `supercombo` / `Normals > Punish Advantage`: 258 observations; examples: `+12 Stagger`, `HKD +49`, `KD +48 Spin`, `+6(+13)`, `+13(+15)`
- `unclassified_expression` / `supercombo` / `Special Moves > Blockstun`: 235 observations; examples: `30 total`, `30(31)`, `37(24)`, `42 total`, `32 total`
- `unclassified_expression` / `supercombo` / `Normals > Hit Advantage`: 232 observations; examples: `KD +27`, `+2 (+9)`, `+9(+11)`, `+5(+15)`, `+4(+10)`
- `unclassified_expression` / `supercombo` / `Special Moves > Perfect Parry Advantage`: 222 observations; examples: `-34(-25)`, `-31(-22)`, `-27(-25)`, `-28(-25)`, `-43(-29)`
- `unclassified_expression` / `supercombo` / `Special Moves > Active`: 215 observations; examples: `[160]`, `3(14)9`, `2(5)2(4)2(5)2`, `3(4)2(4)2(5)2`, `[185]`
- `unclassified_expression` / `supercombo` / `Normals > Perfect Parry Advantage`: 199 observations; examples: `-9 (-2)`, `-4 (-2)`, `-12 (-2)`, `-8 (-2)`, `-11 (-2)`
- `unclassified_expression` / `supercombo` / `Normals > Block Advantage`: 197 observations; examples: `-2 (+5)`, `+5(+7)`, `+1 (+11)`, `0 (+6)`, `0 (+9)`
- `unclassified_expression` / `supercombo` / `Special Moves > DriveDmg Blk`: 197 observations; examples: `1000x2`, `1500x2`, `1000x4`, `2000x2`, `2500x2`
- `unclassified_expression` / `supercombo` / `Special Moves > Damage`: 196 observations; examples: `500[800]`, `600[800]`, `800x2`, `600[700]`, `700[800]`
- `unclassified_expression` / `supercombo` / `Special Moves > Block Advantage`: 193 observations; examples: `-16(-11)`, `-13(-10)`, `-2 (+4)`, `-8(-6)`, `-14(-11)`
- `unclassified_expression` / `supercombo` / `Special Moves > Recovery`: 185 observations; examples: `20(26)`, `18 land`, `17(20)`, `12(3) land`, `15(17)`
- `unclassified_expression` / `supercombo` / `Special Moves > Hitconfirm Window`: 171 observations; examples: `4 SA`, `12 SA`, `8[13] SA`, `10[15] SA`, `14[15] SA`
- `unclassified_expression` / `supercombo` / `Super Arts > Hit Advantage`: 150 observations; examples: `KD +30`, `HKD +30`, `HKD +21`, `HKD +19 (Air: Wall Splat)`, `HKD +29`
- `unclassified_expression` / `supercombo` / `Drive Moves > Recovery`: 145 observations; examples: `26(31)`, `33(1)(11)`, `15(37)`, `26(33)`, `26(32)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Total`: 145 observations; examples: `48(53)`, `46(51)`, `45(3)`, `26(48)`, `24(46)`
- `unclassified_expression` / `supercombo` / `Special Moves > Drive Gain`: 142 observations; examples: `1000 [TB: 5000]`, `0 [TB: 2000]`, `1000x2`, `2000 [TB: 4000]`, `2500 [TB: 4500]`
- `source_specific_expression` / `official` / `キャンセル`: 140 observations; examples: `※SA3`, `※SA2`, `※`, `※1`, `C※`
- `unclassified_expression` / `supercombo` / `Super Arts > Punish Advantage`: 139 observations; examples: `KD +30`, `HKD +30`, `HKD +21`, `HKD +19 (Air: Wall Splat)`, `HKD +18`
- `unclassified_expression` / `supercombo` / `Command Normals > DriveDmg Hit [PC]`: 133 observations; examples: `[4000]`, `[6000]`, `[5000x2]`, `[5000]`, `[8000]`
- `unclassified_expression` / `supercombo` / `Command Normals > Super Gain Hit`: 131 observations; examples: `500 (350)`, `1000 (700)`, `500x2 (350x2)`, `2500 (1750)`, `250x2 (175x2)`
- `unclassified_expression` / `supercombo` / `Command Normals > Super Gain Blk`: 130 observations; examples: `250 (125)`, `500 (250)`, `250x2 (125x2)`, `125x2 (62x2)`, `150 (75)`
- `unclassified_expression` / `supercombo` / `Special Moves > Chip Dmg`: 112 observations; examples: `50x4 (200)`, `75x2`, `200 [225]`, `100 [125]`, `100 each`
- `unclassified_expression` / `supercombo` / `Target Combos > Super Gain Hit`: 110 observations; examples: `400 (280)`, `600 (420)`, `1000 (700)`, `700 (490)`, `500 (350)`
- `unclassified_expression` / `supercombo` / `Special Moves > Startup`: 106 observations; examples: `37 total`, `39 total`, `11(28)`, `18~`, `27(30) total`
- `unclassified_expression` / `supercombo` / `Special Moves > Total`: 105 observations; examples: `36(42)`, `42(45)`, `47(148)`, `27(30)`, `32(35)`
- `unclassified_expression` / `supercombo` / `Special Moves > Juggle Start`: 104 observations; examples: `[1]`, `1 / [1] [-1 PC]`, `1 / [-1 ground]`, `1 / [1]`, `2 / [-1]`
- `unclassified_expression` / `supercombo` / `Target Combos > Super Gain Blk`: 103 observations; examples: `200 (100)`, `300 (150)`, `500 (250)`, `350 (175)`, `250 (125)`
- `unclassified_expression` / `supercombo` / `Taunts > Startup`: 97 observations; examples: `611 (total)`, `484 (total)`, `370 (total)`, `256 (total)`, `405 (total)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Hit Advantage`: 87 observations; examples: `KD +35 / Wall Splat KD +65`, `KD +23`, `KD +24`
- `unclassified_expression` / `supercombo` / `Target Combos > DriveDmg Hit [PC]`: 87 observations; examples: `[4000]`, `[10000]`, `[5000]`, `[7000]`, `[2000]`
- `unclassified_expression` / `supercombo` / `Normals > Attack Range`: 86 observations; examples: `1.23 (1.13)`, `2.05 (2.00)`, `2.30 (2.20)`, `0.94 (0.84)`, `1.33 (0.93)`
- `unclassified_expression` / `supercombo` / `Normals > Hitconfirm Window`: 85 observations; examples: `13 (DR: 14)`, `14 SA`, `20 SA`, `16 / 19 TC`, `19 SA`
- `unclassified_expression` / `supercombo` / `Super Arts > Attack Range`: 81 observations; examples: `2.61 (2.26)`, `2.50 (2.31)`, `2.70 (2.60)`, `2.66 (2.56)`, `4.278 (1.299)`
- `unclassified_expression` / `supercombo` / `Throws > DriveDmg Hit [PC]`: 74 observations; examples: `[10000]`, `[5000x2]`
- `unclassified_expression` / `supercombo` / `Throws > Hit Advantage`: 74 observations; examples: `KD +19`, `KD +20`, `KD +28`, `KD +16`, `KD +22`
- `unclassified_expression` / `supercombo` / `Throws > Punish Advantage`: 74 observations; examples: `HKD +19`, `HKD +20`, `HKD +28`, `HKD +16`, `HKD +22`
- `unclassified_expression` / `supercombo` / `Throws > Damage`: 73 observations; examples: `1200 (2040)`, `1300 (2210)`, `1082 (1838)`, `1082 (1839)`, `1400 (2380)`
- `unclassified_expression` / `supercombo` / `Throws > Super Gain Hit`: 73 observations; examples: `2000(1400) [4000(2800)]`, `1000x2(700x2) [2000x2(1400x2)]`, `3000(2100) [6000(4200)]`
- `unclassified_expression` / `supercombo` / `Normals > Total`: 68 observations; examples: `24(26)`, `25(27)`, `25(29)`, `33(38)`, `27(30)`
- `unclassified_expression` / `supercombo` / `Special Moves > Hitstun`: 68 observations; examples: `41(28)`, `43(30)`, `44(31)`, `(29)`, `36 total`
- `unclassified_expression` / `supercombo` / `Special Moves > Juggle Limit`: 68 observations; examples: `5x4`, `1/10`, `6/7`, `6/8`, `3/5/7`
- `unclassified_expression` / `supercombo` / `Target Combos > Hit Advantage`: 62 observations; examples: `KD +34[+54]`, `KD +21`, `HKD +20`, `KD +49`, `KD +26`
- `unclassified_expression` / `supercombo` / `Taunts > Notes`: 61 observations; examples: `"... BOOM!"`, `"Bring it."`, `"Let's do this!"`, `"Aaalex. Aaaalex! AAAALEX!!! AAHHHH!!"`, `"Peekaboo!"`
- `unclassified_expression` / `supercombo` / `Drive Moves > Damage`: 58 observations; examples: `500 recoverable`, `250x2 recoverable`
- `unclassified_expression` / `supercombo` / `Drive Moves > Punish Advantage`: 58 observations; examples: `KD +23`, `KD +24`
- `unclassified_expression` / `supercombo` / `Command Normals > Punish Advantage`: 56 observations; examples: `+9(+19)`, `HKD +33`, `+4(+17)`, `HKD +76(+79) Crumple`, `HKD +29(+38)`
- `unclassified_expression` / `supercombo` / `Special Moves > Hitstop`: 56 observations; examples: `(8)`, `3[8(13)]`, `3(13)`, `12[13]`, `18 / 15(14)`
- `source_specific_expression` / `official` / `コンボ補正値`: 55 observations; examples: `※即時補正10%`, `※即時補正10％`, `※始動補正30%コンボ補正20%`, `※即時補正20%`, `※即時補正10％コンボ補正20%`
- `unclassified_expression` / `supercombo` / `Super Arts > Blockstun`: 55 observations; examples: `17 (3P: 18)`, `30 total`, `66 total`, `72 total`, `76(7)20`
- `unclassified_expression` / `supercombo` / `Drive Moves > Chip Dmg`: 54 observations; examples: `125 recoverable`
- `unclassified_expression` / `supercombo` / `Command Normals > Attack Range`: 51 observations; examples: `2.162 (2.076)`, `1.736 (1.548)`, `1.783 (1.163)`, `1.73 (1.32)`, `1.519 (Stand)`
- `unclassified_expression` / `supercombo` / `Target Combos > Punish Advantage`: 50 observations; examples: `KD +34[+54]`, `KD +21`, `HKD +20`, `KD +26`, `KD +34`
- `unclassified_expression` / `supercombo` / `Command Normals > Hit Advantage`: 49 observations; examples: `+5(+15)`, `HKD +33`, `0 (+13)`, `KD +27(+30)`, `KD +29(+38)`
- `unclassified_expression` / `supercombo` / `Special Moves > Juggle Increase`: 48 observations; examples: `5 / [2]`, `0x4`, `3/0`, `1/0`, `1/10`
- `unclassified_expression` / `supercombo` / `Normals > After DR Hit`: 46 observations; examples: `KD +27`, `KD +29`, `KD +25`, `KD +38`, `KD +40`
- `unclassified_expression` / `supercombo` / `Super Arts > Damage`: 45 observations; examples: `3000 (2000 Air)`, `2800 (1680)`, `2000 [2200]`, `3000 (220x6)`, `3000 (220x8)`
- `source_specific_expression` / `official` / `動作フレーム > 持続`: 44 observations; examples: `※`, `[※2] 1-12`, `6-366-11, 13-18※,20-25, 34-36`, `7-377-12,14-19※, 21-26, 35-37`, `8-388-13, 15-20※, 22-27, 36-38`
- `unclassified_expression` / `supercombo` / `Target Combos > Damage`: 43 observations; examples: `300(240)`, `1200 (840)`, `1000 (800)`, `400(320)`, `625(438)`
- `unclassified_expression` / `supercombo` / `Command Normals > Recovery`: 41 observations; examples: `20(21)`, `16(24)`, `3 land`, `20(35) land`, `28(31)`
- `source_specific_expression` / `official` / `ダメージ`: 36 observations; examples: `※500`, `※600`, `※700`, `※900`, `※1000`
- `unclassified_expression` / `supercombo` / `Special Moves > Dmg Scaling`: 34 observations; examples: `Combo (2 hits)`, `[Combo (2 hits)]`, `Combo (3 hits)`, `Combo (2-hit)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Active`: 33 observations; examples: `12 or until released`, `3(10)3`, `3(6)3`
- `unclassified_expression` / `supercombo` / `Command Normals > Block Advantage`: 32 observations; examples: `+1 (+11)`, `-14 (-1)`, `-15(-12)`, `-18(-9)`, `+1(+2)`
- `unclassified_expression` / `supercombo` / `Command Normals > Perfect Parry Advantage`: 32 observations; examples: `-12 (-2)`, `-47(-34)`, `-33(-30)`, `-30(-21)`, `-26(-35)`
- `unclassified_expression` / `supercombo` / `Super Arts > Active`: 32 observations; examples: `53(28)12`, `[1500 total]`, `2(24)1(7)1`, `4(3)6`, `3(5)3`
- `unclassified_expression` / `supercombo` / `Super Arts > Block Advantage`: 30 observations; examples: `-19~`, `-24(-22)`, `-24(-18)`, `-23(-18)`, `-33(-23)`
- `unclassified_expression` / `supercombo` / `Super Arts > DriveDmg Hit [PC]`: 30 observations; examples: `2000 each`, `1000x5`, `625x16 (10000)`, `2500x2`, `1000 (10000 total)`
- `unclassified_expression` / `supercombo` / `Super Arts > Hitstop`: 30 observations; examples: `25(20)`, `10 (15 air)`, `(20)`, `9x4.10`, `9x5`
- `unclassified_expression` / `supercombo` / `Character Vitals > Throw Range / Hurtbox`: 29 observations; examples: `0.8 / 0.33`, `0.85 / 0.38`, `0.9 / 0.43`, `0.9 / 0.38`, `1.02 / 0.49`
- `unclassified_expression` / `supercombo` / `Drive Moves > Block Advantage`: 29 observations; examples: `-3 / Wall Splat HKD +72`
- `unclassified_expression` / `supercombo` / `Drive Moves > DriveDmg Hit [PC]`: 29 observations; examples: `10000 [15000]`
- `unclassified_expression` / `supercombo` / `Drive Moves > Invuln`: 29 observations; examples: `6 Full (after Perfect Parry)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Super Gain Hit`: 29 observations; examples: `[3000(2100)]`
- `unclassified_expression` / `supercombo` / `SF6 Navigation > column_0`: 29 observations; examples: `Street Fighter 6 (SF6)`
- `source_specific_expression` / `official` / `動作フレーム > 硬直`: 28 observations; examples: `全体 ※43`, `全体 ※42`, `※16`, `※17`, `※20`
- `unclassified_expression` / `supercombo` / `Super Arts > DriveDmg Blk`: 27 observations; examples: `625x8 (5000)`, `1000 each`, `500x5`, `1250x2`, `420x12 (5040)`
- `unclassified_expression` / `supercombo` / `Super Arts > Perfect Parry Advantage`: 27 observations; examples: `-19(-55)`, `-37(-43)`, `-42(-36)`, `-41(-36)`, `-51(-41)`
- `unclassified_expression` / `supercombo` / `Super Arts > Recovery`: 27 observations; examples: `7(9) land`, `37 land`, `16 land`, `79(64)`, `181 total`
- `unclassified_expression` / `supercombo` / `Command Normals > Hitconfirm Window`: 26 observations; examples: `31 (2PP)`, `19 (20 stance)`, `18 (stance)`, `20 (stance)`, `19(18)`
- `unclassified_expression` / `supercombo` / `Normals > Notes`: 26 observations; examples: `Long range sweep; has juggle potential`, `Solid neutral poke; SA2 cancel: +10/+3`, `Chains into 5LP/2LP/2LK; Stance Cancel: -1/-6`, `Chains into 5LP/2LP/2LK`, `Chains into 5LP/2LP/1LK`
- `unclassified_expression` / `supercombo` / `Super Arts > Chip Dmg`: 26 observations; examples: `100x5`, `100x5 (500)`, `250x2 (500)`, `492 (+300 rec)`, `150x5 (750)`
- `unclassified_expression` / `supercombo` / `Normals > Juggle Start`: 23 observations; examples: `1 [-1 PC Ground]`, `1 [0 PC]`, `1 air [0 PC Air]`, `1 air`, `-1 PC ground / 0 PC air`
- `unclassified_expression` / `supercombo` / `Target Combos > Recovery`: 23 observations; examples: `15(17)`, `24(29)`, `3 land`, `17(19)`, `22 total`
- `unclassified_expression` / `supercombo` / `Command Normals > Total`: 22 observations; examples: `38(39)`, `40(48)`, `49(52)`, `40(45)`, `34(36)`
- `unclassified_expression` / `supercombo` / `Command Normals > After DR Hit`: 21 observations; examples: `KD +27(+30)`, `KD +29(+38)`, `KD +31`, `+9(+10)`, `KD +33`
- `unclassified_expression` / `supercombo` / `Normals > Drive Gain`: 20 observations; examples: `1000x2`, `500x2 (500)`, `250(150)`, `1500x2`, `2000x2`
- `unclassified_expression` / `supercombo` / `Super Arts > Startup`: 20 observations; examples: `8(2)`, `8(11)`, `13(2)`, `10(27)`, `10(3)`
- `unclassified_expression` / `supercombo` / `Special Moves > Projectile Speed`: 19 observations; examples: `0.012 (bounce) / 0.05 (walk)`, `0.15 (22f~)`, `LP 0.033 / MP 0.044 / HP 0.06`, `LPMP 0.033 / LPHP 0.044 / MPHP 0.06`, `LK 0.0195 / MK 0.0385 / HK 0.07`
- `unclassified_expression` / `supercombo` / `Command Normals > Juggle Start`: 18 observations; examples: `0/1`, `0 air [-1 PC Ground]`, `1 CH/PC Air`, `1 air`, `1 [-1 PC Ground]`
- `unclassified_expression` / `supercombo` / `Normals > Damage`: 18 observations; examples: `450x2`, `300x2`, `800(500)`, `800(700)`, `400x2`
- `unclassified_expression` / `supercombo` / `Normals > Active`: 17 observations; examples: `3(5)5`, `4(6)5`, `2(1)4`, `3(6)5`, `3(4)3`
- `unclassified_expression` / `supercombo` / `Normals > After DR Blk`: 17 observations; examples: `0 (+5)`, `-7 (+2)`, `-6 (0)`, `-6 (+6)`, `-12 (+3)`
- `unclassified_expression` / `supercombo` / `Target Combos > Hitconfirm Window`: 17 observations; examples: `50(18)`, `59(33)`, `41(15)`, `57 (60 PC)`, `18 (56 total)`
- `unclassified_expression` / `supercombo` / `Target Combos > DR Cancel Hit`: 16 observations; examples: `KD +65`, `KD +39`, `KD +52`, `KD +48`, `KD +47`
- `unclassified_expression` / `supercombo` / `Command Normals > Drive Gain`: 15 observations; examples: `1500x2`, `750x2`, `1000x2`, `1250x2`, `1000x2 (1000)`
- `unclassified_expression` / `supercombo` / `Normals > DriveDmg Blk`: 15 observations; examples: `2500x2`, `2000x2`, `3000x2`, `500x2`, `1500x2`
- `unclassified_expression` / `supercombo` / `Super Arts > Juggle Increase`: 15 observations; examples: `2 each`, `1x12`, `1x4`, `[0]`, `1xN`
- `unclassified_expression` / `supercombo` / `Command Normals > Damage`: 14 observations; examples: `400x2`, `300x2`, `450x2`, `500x2`, `600x2`
- `unclassified_expression` / `supercombo` / `Command Normals > DriveDmg Blk`: 14 observations; examples: `2000x2`, `1250x2`, `2500x2`, `625x2`, `1500x2`
- `unclassified_expression` / `supercombo` / `Normals > Startup`: 14 observations; examples: `8(9)`, `13(24)`, `5(8)`, `23(5)`, `24(10)`
- `unclassified_expression` / `supercombo` / `Command Normals > Active`: 13 observations; examples: `3(5)3`, `3(7)2`, `3(15)3`, `1(1)3`, `3(6)3`
- `unclassified_expression` / `supercombo` / `Command Normals > DR Cancel Hit`: 12 observations; examples: `KD +65`, `KD +42`, `+17/+12`, `KD +69`, `KD +55`
- `unclassified_expression` / `supercombo` / `Command Normals > Startup`: 12 observations; examples: `19(21)`, `15(23)`, `10(19)`, `20(3)`, `28(14)`
- `unclassified_expression` / `supercombo` / `Super Arts > Juggle Start`: 12 observations; examples: `1 air`, `0 / 1 air`, `1 air [-1 CH/PC Ground] [0 PC Air]`, `1 (Forced)`, `0 (Forced)`
- `unclassified_expression` / `supercombo` / `Target Combos > Total`: 12 observations; examples: `24(26)`, `40(45)`, `30(32)`, `35(39)`, `33(36)`
- `unclassified_expression` / `supercombo` / `Command Normals > After DR Blk`: 11 observations; examples: `-14(-5)`, `+5(+6)`, `+2 (+6)`, `-6 (+2)`, `0 (+4)`
- `unclassified_expression` / `supercombo` / `Normals > Cancel`: 11 observations; examples: `Sp SA2`, `SS Sp SA (2nd)`, `Sp SA1`, `Sp SA (2nd)`, `Sp SA (1st)`
- `unclassified_expression` / `supercombo` / `Normals > Hitstop`: 11 observations; examples: `15 (25 PC)`, `13 (25 PC)`, `13 (16 PC)`, `13(20)`, `13 (PC: 25)`
- `unclassified_expression` / `supercombo` / `Target Combos > Dmg Scaling`: 11 observations; examples: `Combo (2 hits)`, `Combo (3 hits)`
- `unclassified_expression` / `supercombo` / `Target Combos > Drive Gain`: 11 observations; examples: `3000 [TB: 5000]`, `1000x2`, `2500 / 10000 (DL4)`, `500x2`, `5000 / 10000 (DL4)`
- `unclassified_expression` / `supercombo` / `Prowler Stance > DriveDmg Hit [PC]`: 10 observations; examples: `[4000]`, `[2000]`, `[5000]`, `[8000]`, `[10000]`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Punish Advantage`: 10 observations; examples: `KD +56`, `+11*`, `HKD +22`, `+10 (Backturn)`, `+10 Backturn`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Super Gain Hit`: 10 observations; examples: `800 (560)`, `300 (210)`, `400x2 (280x2) [2400(1680)]`, `1000 (700)`, `1100 (770)`
- `unclassified_expression` / `supercombo` / `Super Arts > Juggle Limit`: 10 observations; examples: `99x5`, `11x3`, `100x4`, `99 [99]`, `99x8`
- `unclassified_expression` / `supercombo` / `Target Combos > Attack Range`: 10 observations; examples: `1.75 (1.65)`, `1.96 (1.88)`, `1.94 (1.76)`, `2.35 (1.79)`, `1.90 (1.88)`
- `unclassified_expression` / `supercombo` / `Target Combos > Block Advantage`: 10 observations; examples: `-12(-19)`, `-11(-7)`, `-8(-23)`, `-6(-20)`, `-3 / (-10/-23)`
- `source_specific_expression` / `official` / `属性`: 9 observations; examples: `※中上`, `※下`, `※中`
- `unclassified_expression` / `supercombo` / `Normals > Hitstun`: 9 observations; examples: `32 total`, `28(25)`, `36(29)`, `37(26)`, `28(27)`
- `unclassified_expression` / `supercombo` / `Super Arts > Total`: 9 observations; examples: `61(81)`, `201(180)`, `68(79)`, `73(79)`, `62~`
- `unclassified_expression` / `supercombo` / `Throws > Recovery`: 9 observations; examples: `3 land`
- `source_specific_expression` / `official` / `SAゲージ増加`: 8 observations; examples: `※3000`, `※2150`
- `unclassified_expression` / `supercombo` / `Command Normals > Blockstun`: 8 observations; examples: `29(21)`, `20(18)`, `28(18)`, `25(22)`, `26 total`
- `unclassified_expression` / `supercombo` / `Command Normals > Hitstun`: 8 observations; examples: `31(23)`, `26(24)`, `36(26)`, `25(26)`, `48 total`
- `unclassified_expression` / `supercombo` / `Normals > Blockstun`: 8 observations; examples: `28 total`, `23(16)`, `33(22)`, `27(20)`, `25(20)`
- `unclassified_expression` / `supercombo` / `Normals > DR Cancel Hit`: 8 observations; examples: `+17(+15)`, `KD +46`, `+13 / +13`, `+7 (KD +39)`, `KD +51`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Super Gain Blk`: 8 observations; examples: `400 (200)`, `150 (75)`, `200x2 (100x2)`, `500 (250)`, `550 (275)`
- `unclassified_expression` / `supercombo` / `Target Combos > Active`: 8 observations; examples: `4(12)3`, `4(3)4`, `3(5)3`, `3(5)2`, `2(8)2(11)2`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Hit Advantage`: 7 observations; examples: `+7*`, `KD +51`, `KD +28`, `KD +29`, `KD +25`
- `unclassified_expression` / `supercombo` / `Super Arts > Projectile Speed`: 7 observations; examples: `LK 0.014 / MK 0.021 / HK 0.04`, `0.03 / 0.045 / 0.09`, `0.3 (2nd hit)`, `0.12 / 0.22 final`
- `source_specific_expression` / `official` / `動作フレーム > 発生`: 6 observations; examples: `122※`, `124※`, `128※`
- `source_specific_expression` / `official` / `硬直差 > ガード`: 6 observations; examples: `※-4`, `※-15`, `※-5`, `※-10`, `※-2`
- `unclassified_expression` / `supercombo` / `Command Normals > Cancel`: 6 observations; examples: `2PP*`, `6KK*`, `Sp SA (2nd)`, `Sp SA (1st)`, `SA (2nd)`
- `unclassified_expression` / `supercombo` / `Command Normals > DR Cancel Blk`: 6 observations; examples: `+7/+6`, `+6 / +9`, `+4 / +6`, `+4(+10)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > DriveDmg Hit [PC]`: 6 observations; examples: `[2000]`, `[4000]`, `[3000x2]`, `[10000]`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Super Gain Blk`: 6 observations; examples: `150 (75)`, `150x2 (75x2)`, `500 (250)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Super Gain Hit`: 6 observations; examples: `300 (210)`, `300x2 (210x2)`, `1000 (700)`
- `unclassified_expression` / `supercombo` / `Taunts > Punish Advantage`: 6 observations; examples: `KD -197`, `KD +35 Crumple`, `KD -46`, `KD -171`, `KD -148`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Attack Range`: 5 observations; examples: `2.32 / 2.60 / 3.14`, `1.10 (0.81)`, `1.48 (1.41)`, `3.05 / 2.43 / 1.34`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Damage`: 5 observations; examples: `400x2 (2680)`, `600 (2420)`, `1200 (2040)`, `2000 (2300)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Hit Advantage`: 5 observations; examples: `-2 (-22)`, `KD +34(+45) [KD +21(+32)]`, `0 (-23)`, `-3 (-27)`, `KD +41`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Punish Advantage`: 5 observations; examples: `+2 (-18)`, `KD +34(+45) [KD +21(+32)]`, `+4 (-19)`, `+1 (-23)`, `KD +41`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Recovery`: 5 observations; examples: `23(18)`, `16[36]`, `19[32]`, `13[36]`, `22[46]`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Total`: 5 observations; examples: `25[45]`, `36[49]`, `25[48]`, `36[60]`, `[36]`
- `unclassified_expression` / `supercombo` / `Special Moves > Notes`: 5 observations; examples: `Slow hopping command grab; Range: 2.49 (shortest)`, `Slow hopping command grab; Range: 3.41 (mid-range)`, `Slow hopping command grab; Range: 4.24 (longest)`, `Damage DL2-DL4: 1600/1677/1760 (Chip: 397/416/435)`, `Good anti-air; cannot hit cross-up`
- `unclassified_expression` / `supercombo` / `Target Combos > Blockstun`: 5 observations; examples: `25(18)`, `16*`, `22 total`, `24 total`, `42(33)(20)`
- `unclassified_expression` / `supercombo` / `Target Combos > Perfect Parry Advantage`: 5 observations; examples: `≤ -2`, `≤ -26`, `-19 *`, `-23 *`
- `unclassified_expression` / `supercombo` / `Taunts > DriveDmg Hit [PC]`: 5 observations; examples: `[2000]`, `[5000]`, `[60]`
- `unclassified_expression` / `supercombo` / `Taunts > Hit Advantage`: 5 observations; examples: `KD -197`, `KD -50`, `KD -171`, `KD -148`, `KD -96`
- `source_specific_expression` / `official` / `硬直差 > ヒット`: 4 observations; examples: `※-3`, `※-1`, `※-4`, `※1`
- `unclassified_expression` / `supercombo` / `Drive Moves > Armor`: 4 observations; examples: `Break (1st hit)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Blockstun`: 4 observations; examples: `36 total`, `32 total`
- `unclassified_expression` / `supercombo` / `Drive Moves > Hitstop`: 4 observations; examples: `20(16)`, `20 (16 block)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Hit Advantage`: 4 observations; examples: `KD +25(26)`, `KD +38`, `KD +17`, `KD 0(+6)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Punish Advantage`: 4 observations; examples: `KD +29(30)`, `KD +38`, `KD +17`, `KD 0(+6)`
- `unclassified_expression` / `supercombo` / `Normals > DR Cancel Blk`: 4 observations; examples: `+8(+11)`, `+5 / +6`, `+10/+10`, `+11 / +10`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Hitstop`: 4 observations; examples: `13 (15 CH/PC)`, `13 (20 CH/PC)`, `6 (15 PC)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Block Advantage`: 4 observations; examples: `-3 (-23)`, `-15(-4) [-28(-17)]`, `-4(-27)`, `-9(-33)`
- `unclassified_expression` / `supercombo` / `Special Moves > Armor`: 4 observations; examples: `6~release`, `3~release`, `11~`, `3~ (2-hit)`
- `unclassified_expression` / `supercombo` / `Super Arts > Drive Gain`: 4 observations; examples: `1000 oH (500 oB)`, `[Heal: 10000]`, `5000 / 10000 (DL4)`, `10000 / 30000 (DL4)`
- `unclassified_expression` / `supercombo` / `Target Combos > DriveDmg Blk`: 4 observations; examples: `3000x2`, `2000x2`, `1000x2`, `1500x2`
- `unclassified_expression` / `supercombo` / `Taunts > Hitstop`: 4 observations; examples: `9(25)`, `11(20)`, `7x8`
- `unclassified_expression` / `supercombo` / `Taunts > Super Gain Blk`: 4 observations; examples: `300 (150)`, `150 (75)`, `250 (125)`
- `unclassified_expression` / `supercombo` / `Taunts > Super Gain Hit`: 4 observations; examples: `600 (420)`, `300 (210)`, `500 (350)`
- `malformed_looking_source_value` / `official` / `動作フレーム > 持続`: 3 observations; examples: `30-34.35`, `20-24.25`, `23--33`
- `unclassified_expression` / `official` / `硬直差 > ガード`: 3 observations; examples: `-12～-1`, `-4～-1`, `-39～-33`
- `unclassified_expression` / `supercombo` / `Command Normals > Hitstop`: 3 observations; examples: `11 (PC: 13)`, `13(20)`, `13 (25 PC)`
- `unclassified_expression` / `supercombo` / `Command Normals > Juggle Increase`: 3 observations; examples: `0/1`, `1(2)`, `1(0)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Blockstun`: 3 observations; examples: `26 each`, `33(32)`, `32 total`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Hitstop`: 3 observations; examples: `8 each`, `0(8)`, `12(15)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Perfect Parry Advantage`: 3 observations; examples: `-10~`, `-86(-85)`, `-107(-101)`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Drive Gain`: 3 observations; examples: `1000x2 [2500]`, `2000 [3000]`, `1000 [2000]`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Startup`: 3 observations; examples: `18~`, `12/15/18`, `22~`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Attack Range`: 3 observations; examples: `2.30 (1.753)`, `1.677 (1.40)`, `1.519 (1.493)`
- `unclassified_expression` / `supercombo` / `Special Moves > Invuln`: 3 observations; examples: `17~ Projectile (Legs)`, `1~ Projectile (Legs)`, `3-(15/16/17) Projectile`
- `unclassified_expression` / `supercombo` / `Throws > Drive Gain`: 3 observations; examples: `7000 / 12000 (DL4)`, `1000x2`
- `source_specific_expression` / `official` / `技名`: 2 observations; examples: `スクトゥム(当身派生版)※スクトゥム中に打撃を受ける`, `OD スクトゥム(当身派生版)※ODスクトゥム中に打撃を受ける`
- `unclassified_expression` / `supercombo` / `Character Vitals > Forward Jump Distance`: 2 observations; examples: `1.90 (3.00)`, `1.90 (5.07)`
- `unclassified_expression` / `supercombo` / `Command Normals > Dmg Scaling`: 2 observations; examples: `Combo (2 hits)`
- `unclassified_expression` / `supercombo` / `Command Normals > Juggle Limit`: 2 observations; examples: `0(1)`, `12(16)`
- `unclassified_expression` / `supercombo` / `Drive Moves > Attack Range`: 2 observations; examples: `2.066 (1.69)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Block Advantage`: 2 observations; examples: `-58(-57)`, `-94(-88)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > DriveDmg Hit [PC]`: 2 observations; examples: `[3000]`, `[5000]`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Recovery`: 2 observations; examples: `9(2) land`, `88(85)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Startup`: 2 observations; examples: `8(21)`, `9(15)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Super Gain Blk`: 2 observations; examples: `500x2 (250x2)`, `600 (300)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Super Gain Hit`: 2 observations; examples: `1000x2 (700x2)`, `1200 (840)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Active`: 2 observations; examples: `[57~]`, `2(6)2`
- `unclassified_expression` / `supercombo` / `Super Arts > Hitstun`: 2 observations; examples: `56(55)`, `41 each`
- `unclassified_expression` / `supercombo` / `Super Arts > Invuln`: 2 observations; examples: `1 Strike/Throw`
- `unclassified_expression` / `supercombo` / `Target Combos > Cancel`: 2 observations; examples: `SA2`, `Sp* SA2*`
- `unclassified_expression` / `supercombo` / `Taunts > Active`: 2 observations; examples: `[178]`, `[55]`
- `unclassified_expression` / `supercombo` / `Taunts > Blockstun`: 2 observations; examples: `100 total`
- `unclassified_expression` / `supercombo` / `Taunts > Juggle Limit`: 2 observations; examples: `99x8`
- `unclassified_expression` / `supercombo` / `Taunts > Juggle Start`: 2 observations; examples: `1x8`
- `unclassified_expression` / `supercombo` / `Taunts > Total`: 2 observations; examples: `570(514)`, `442(792)`
- `unclassified_expression` / `official` / `硬直差 > ヒット`: 1 observations; examples: `-28～-23`
- `unclassified_expression` / `supercombo` / `Character Vitals > Back Dash Distance`: 1 observations; examples: `1.10 (1.91)`
- `unclassified_expression` / `supercombo` / `Character Vitals > Back Jump Distance`: 1 observations; examples: `1.52 (3.63)`
- `unclassified_expression` / `supercombo` / `Character Vitals > Back Walk Speed`: 1 observations; examples: `0.033 (0.0366)`
- `unclassified_expression` / `supercombo` / `Character Vitals > Forward Dash Distance`: 1 observations; examples: `1.20 (1.86)`
- `unclassified_expression` / `supercombo` / `Character Vitals > Forward Walk Speed`: 1 observations; examples: `0.0505 (0.0561)`
- `unclassified_expression` / `supercombo` / `Character Vitals > Jump Apex`: 1 observations; examples: `2.11 (2.195)`
- `unclassified_expression` / `supercombo` / `Command Normals > Notes`: 1 observations; examples: `Chains into 5LP/2LP/1LK`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Attack Range`: 1 observations; examples: `2.12 (1st)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Chip Dmg`: 1 observations; examples: `150x2`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Damage`: 1 observations; examples: `600x2`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Drive Gain`: 1 observations; examples: `2000x2`
- `unclassified_expression` / `supercombo` / `Hidden Arts > DriveDmg Blk`: 1 observations; examples: `2500x2`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Hitstun`: 1 observations; examples: `28 each`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Projectile Speed`: 1 observations; examples: `0.04 (1st) / 0.055 (2nd)`
- `unclassified_expression` / `supercombo` / `Hidden Arts > Total`: 1 observations; examples: `99(96)`
- `unclassified_expression` / `supercombo` / `Normals > Armor`: 1 observations; examples: `4-release (Upper Body)`
- `unclassified_expression` / `supercombo` / `Normals > Dmg Scaling`: 1 observations; examples: `Combo (2 hits)`
- `unclassified_expression` / `supercombo` / `Normals > Invuln`: 1 observations; examples: `32~ Projectile (Body)`
- `unclassified_expression` / `supercombo` / `Normals > Juggle Increase`: 1 observations; examples: `1(2)`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Block Advantage`: 1 observations; examples: `+1*`
- `unclassified_expression` / `supercombo` / `Prowler Stance > DriveDmg Blk`: 1 observations; examples: `1500x2`
- `unclassified_expression` / `supercombo` / `Prowler Stance > Total`: 1 observations; examples: `33/36/39`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Blockstun`: 1 observations; examples: `26 total`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Drive Gain`: 1 observations; examples: `1000x2`
- `unclassified_expression` / `supercombo` / `Serenity Stream > DriveDmg Blk`: 1 observations; examples: `2500x2`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Hitconfirm Window`: 1 observations; examples: `30 (jump)`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Hitstun`: 1 observations; examples: `31 total`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Perfect Parry Advantage`: 1 observations; examples: `[-42(-31)]`
- `unclassified_expression` / `supercombo` / `Serenity Stream > Startup`: 1 observations; examples: `14(~)`
- `unclassified_expression` / `supercombo` / `Special Moves > Airborne`: 1 observations; examples: `13~Land (FKD)`
- `unclassified_expression` / `supercombo` / `Super Arts > Airborne`: 1 observations; examples: `14~land (FKD)`
- `unclassified_expression` / `supercombo` / `Super Arts > Hitconfirm Window`: 1 observations; examples: `41*`
- `unclassified_expression` / `supercombo` / `Super Arts > Notes`: 1 observations; examples: `Cinematic time regenerates ~2 Drive bars for Juri`
- `unclassified_expression` / `supercombo` / `Target Combos > DR Cancel Blk`: 1 observations; examples: `+5 *`
- `unclassified_expression` / `supercombo` / `Taunts > Damage`: 1 observations; examples: `100x8`
- `unclassified_expression` / `supercombo` / `Taunts > DriveDmg Blk`: 1 observations; examples: `60x8`
- `unclassified_expression` / `supercombo` / `Taunts > Recovery`: 1 observations; examples: `258(264)`
- `unclassified_expression` / `supercombo` / `Throws > Juggle Start`: 1 observations; examples: `5 (DR: 0)`

## Boundary Notes

- Official values remain authority candidates only.
- SuperCombo remains enrichment, cross-reference, or candidate evidence only.
- English canonical keys are deferred to a later normalized schema ExecPlan.
- This artifact intentionally excludes raw HTML, full raw rows, and full source table dumps.
