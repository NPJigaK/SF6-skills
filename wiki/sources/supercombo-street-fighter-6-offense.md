---
type: source
source_type: wiki_page
title: "Street Fighter 6/Offense"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/offense/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Offense"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-05-30T00:03:21Z
captured_at_utc: 2026-06-11T11:03:16Z
status: active
confidence: medium
tags:
  - sf6
  - offense
  - throws
  - counter-hit
  - punish-counter
  - safe-jump
  - community-wiki
  - web-page-capture
  - numeric-source
aliases:
  - "SF6 Offense"
  - "Street Fighter 6 Offense"
  - "ストリートファイター6 攻め"
related_concepts:
  - "[[concepts/offense]]"
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Offense

## 1行要約

SuperCombo Wiki の Street Fighter 6 Offense page を MediaWiki wikitext、HTML、rendered DOM、scoped screenshots として保存した raw source。通常技、必殺技、通常投げ、throw range、throw invincibility、throw loop、counter / punish counter、corner dizzy、combo / blockstring、safe jump、empty jump mixup、kara 系 defensive bait の説明を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/offense/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Source freshness は MediaWiki revid `364971`、revision timestamp `2026-05-30T00:03:21Z`。Raw 取得時刻は `2026-06-11T11:03:16Z`。
3. `validation.json` は `passed`。Rendered DOM は heading 17 件、table 2 件、image refs 30 件を記録した。
4. 本文 table は throw range table 1 件のみ。もう 1 件は SF6 Navigation なので本文根拠として扱わない。
5. 本文 content media は 0 件。MediaWiki API の character / navigation icon 30 件は `metadata.json` の excluded provenance として保持し、raw media download 対象にはしていない。
6. この source は community wiki なので、公式 Capcom source と重なる mechanics claim は公式 source を優先する。ただし、throw range、throw invincibility timing、safe jump / empty jump の timing 条件、character-specific throw loop notes など、この wiki に未収録の攻めの補助 source として重要。

## Section summary

| Section | Source fact summary |
|---|---|
| Normal Moves | SF6 は 6ボタン構成。通常技同士が同 frame で衝突すると両者が Counter-hit になり、同 frame の strike と throw では strike が勝つと説明する。 |
| Special Moves | コマンド入力とボタンで special move を出し、2ボタン入力で Drive gauge 2 stocks を使う Overdrive 版にできると説明する。 |
| Throws | 通常投げの startup / active / whiff、forward/back throw、throw punish counter、throw invincibility、throw range、throw loop を説明する。 |
| Counters | Counter-hit は startup / active への攻撃、Punish Counter は recovery への攻撃として説明し、advantage / damage / Drive depletion を述べる。 |
| Corner Dizzy | Burnout 中の cornered opponent へ Drive Impact を当てた後の free stun combo と、character-specific stock / setup examples を説明する。 |
| Combos and Blockstrings | combo、blockstring、true / airtight blockstring、SF6 の 4f input buffer を説明する。 |
| Safe Jumps | standard 45f jump の safe jump knockdown advantage 目安、defender counterplay、empty jump との違いを説明する。 |
| Empty Jump Mixups | +45 以上の knockdown advantage からの empty jump throw / low mixup と、safe jump との見分けづらさを説明する。 |
| Advanced Techniques | 0F 状況の kara-Parry と、+11 into Drive Rush からの kara-DP / Super bait を説明する。 |

## Numeric / timing summary

この section は raw source の数値を wiki query で探しやすくするための compiled view。根拠は `raw/web-pages/wiki.supercombo.gg/offense/page.raw.wikitext` と `raw/web-pages/wiki.supercombo.gg/offense/rendered/main.dom.json`。

### Throws

| Throw property | SuperCombo Offense source fact |
|---|---:|
| Normal throw startup | `5f` |
| Normal throw active | `3f` |
| Normal throw whiff animation | `30f` total |
| Backdash throw invincibility | first `15f` |
| Grounded wakeup throw invincibility | `1f` after grounded wakeup |
| After hitstun / blockstun throw invulnerability | `2f` after exiting hitstun / blockstun |
| Air reset landing recovery throw immunity | `2f` landing recovery frames |
| Punish Counter throw damage boost | `+70%` damage |
| Punish Counter throw Drive drain | `1` Drive bar |

The source states that normal throws work only on grounded opponents, do not connect against pre-jump / airborne frames, cannot throw opponents in hitstun, blockstun, or knockdown, and lose to a strike that connects on the same frame.

### Throw range table

Rendered DOM table 0: `Throw Ranges`.

| Character group | Throw range | Throw hurtbox | Relative throw range |
|---|---:|---:|---:|
| Zangief | `1.02` | `0.49` | `0.53` |
| Marisa | `0.90` | `0.38` | `0.52` |
| Blanka / E. Honda | `0.90` | `0.43` | `0.47` |
| Alex / Sagat | `0.85` | `0.38` | `0.47` |
| Everyone Else | `0.80` | `0.33` | `0.47` |

The source defines relative throw range as throw range minus throw hurtbox width. It notes that Zangief's throw hurtbox was expanded as of Season 3, bringing his relative throw range closer to the rest of the cast.

### Counter / Punish Counter

| State | SuperCombo Offense source fact |
|---|---|
| Counter-hit | Occurs when striking the opponent during startup or active frames; attacks that trade both count as Counter-hit. Adds `+2` frame advantage and `20%` damage. Knockdowns usually do not gain extra knockdown advantage. |
| Punish Counter | Occurs when striking recovery frames. Adds `+4` frame advantage, `20%` damage, and depletes some Drive meter. Certain moves gain extra properties. |
| Punish Counter throw | All normal throws, including air throws, can Punish Counter for `+70%` damage, Hard Knockdown, and `1` Drive bar drain. Throws always Punish Counter Drive Parry. |
| Super Arts | Can technically Counter-hit or Punish Counter, but generally do not gain extra damage, Drive depletion, or knockdown advantage except rare cases. |

### Combo / blockstring / safe jump values

| Topic | SuperCombo Offense source fact |
|---|---|
| Input buffer | SF6 input buffer is generally `4f`; the tightest possible links have `5f` input timing. |
| Safe jump vs 5f anti-air | Standard `45f` jump usually needs `+42` knockdown advantage. |
| Safe jump vs 6f reversal | Standard `45f` jump usually needs `+41` knockdown advantage. |
| Slow jump characters | A.K.I., Chun-Li, Lily, and Zangief require slightly more advantage for safe jumps. |
| Perfect Parry against safe jump | Attacker is left at `-2` on a perfect setup. |
| Empty jump mixup | With `+45` or slightly better knockdown advantage, empty jump into immediate throw or `5f` `2LK` can remain safe from immediate `4f` buttons, but not invincible reversals. |
| Kara-Parry | At `0` on hit/block, buffering a normal can allow reaction to Super freeze by holding Parry before the normal leaves its first startup frame. |
| Kara-DP/Super from +11 into Drive Rush | At knockdown advantage `+11`, immediate Drive Rush button's first normal frame can line up with the defender's first actionable frame, allowing kara-cancel into invincible DP / Super against reversal Super. |

## 関連概念

- [[concepts/offense]]
- [[concepts/terms/throw]]
- [[concepts/terms/throw-loop]]
- [[concepts/terms/safe-jump]]
- [[concepts/terms/empty-jump-mixup]]
- [[concepts/terms/blockstring]]
- [[concepts/terms/counter-hit]]
- [[concepts/terms/punish-counter]]
- [[concepts/terms/stun]]
- [[concepts/terms/oki]]
- [[concepts/frame-data]]
- [[concepts/drive-system]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- Counter / Punish Counter の一般的な advantage / damage 説明は Capcom eSports BASE と重なる。公式 source がある一般値では公式 source を優先し、Offense page は throw-specific / safe-jump / tactical context の補助 source とする。
- Corner Dizzy は [[sources/supercombo-street-fighter-6-gauges]] の Burnout / Drive Impact stun 数値と重なる。stun condition や duration / scaling 値では Gauges source page の数値索引を優先し、Offense page は stock setup や follow-up choice の補助 source とする。
- Throw range table は source page に保持するが、現時点では `wiki/outputs/data/` の derived JSON にはしない。表が 1 件で小さいため、query ではこの source page へ戻る。
- Character-specific throw loop notes は community tactical claim であり、公式 frame-data や実機検証ではない。character query では source authority を明示する。

## 未解決の質問

- Throw range / throw hurtbox / safe jump values を公式 source または実機検証で照合するか。
- Throw loop の character-specific notes を、今後 character pages や matchup / route synthesis へ昇格するか。
- Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric tables を、`wiki/outputs/data/` に JSON 化する基準をどうするか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/offense/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/offense/page.raw.wikitext`
- Rendered DOM: `raw/web-pages/wiki.supercombo.gg/offense/rendered/main.dom.json`
- Media DOM: `raw/web-pages/wiki.supercombo.gg/offense/rendered/media.dom.json`
- Image manifest: `raw/web-pages/wiki.supercombo.gg/offense/images/manifest.json`
- Scoped screenshots: `raw/web-pages/wiki.supercombo.gg/offense/screenshots/`
- Validation: `raw/web-pages/wiki.supercombo.gg/offense/validation.json`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/Offense
