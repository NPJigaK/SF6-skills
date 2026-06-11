---
type: source
source_type: wiki_page
title: "Street Fighter 6/Defense"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/defense/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Defense"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-05-30T00:09:39Z
captured_at_utc: 2026-06-11T11:35:33Z
status: active
confidence: medium
tags:
  - sf6
  - defense
  - blocking
  - throw-escape
  - drive-parry
  - wake-up
  - reversal
  - armor
  - anti-air
  - community-wiki
  - web-page-capture
  - numeric-source
aliases:
  - "SF6 Defense"
  - "Street Fighter 6 Defense"
  - "ストリートファイター6 守り"
related_concepts:
  - "[[concepts/defense]]"
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Defense

## 1行要約

SuperCombo Wiki の Street Fighter 6 Defense page を MediaWiki wikitext、HTML、rendered DOM、button / direction rendered media、scoped screenshots として保存した raw source。blocking、throw escape、Drive Parry、wake-up、reversal buffer、armor、anti-air、punish route の defensive timing と tactical notes を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/defense/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Source freshness は MediaWiki revid `364973`、revision timestamp `2026-05-30T00:09:39Z`。Raw 取得時刻は `2026-06-11T11:35:33Z`。
3. `validation.json` は `passed`。Rendered DOM は heading 9 件、table 1 件、image refs 41 件を記録した。
4. Rendered DOM の table 1 件は SF6 Navigation であり、本文根拠として扱わない。
5. MediaWiki wikitext に直接の semantic file transclusion はない。本文中の button / direction icon は rendered media として 14 件保存し、navigation / character icon 30 件は excluded provenance として保持した。
6. この source は community wiki なので、公式 Capcom source と重なる mechanics claim は公式 source を優先する。ただし、throw escape timing、wake-up forced standing frames、reversal buffer、armor damage、anti-air tactical notes、punish route の補助 source として重要。

## Section summary

| Section | Source fact summary |
|---|---|
| Blocking | Block は相手から離れる方向を入力して行い、空中や自分の recovery 中はできない。Overhead / High は立ち guard、Low は crouch guard、cross-up は前方向 guard を要求すると説明する。 |
| Throw Escape | `LP+LK` で grounded normal throw を tech できるが、command grab / air throw には使えない。成功時は damage を防ぎ、相手を押し離し、defender が Drive Gauge を得ると説明する。 |
| Drive Parry | `MP+MK` hold で high/low と left/right を parry でき、通常 block と同じ frame advantage になり、Perfect Parry なら punish 機会が生まれると説明する。 |
| Wake-up | Normal Rise と Back Rise は knockdown frame advantage に差がなく、2 buttons hold/input で Back Rise になる。Hard Knockdown は Back Rise を防ぐと説明する。 |
| Reversals | Wake-up または hitstun / blockstun / air reset 明けに attack を buffer すると Reversal として出やすくなる。Wake-up とそれ以外で buffer window が異なると説明する。 |
| Armor | Drive Impact や一部 special move の armor は strike / projectile を吸収するが throw に負け、Armor Break property は armor absorption を防ぐと説明する。 |
| Anti-Airs | Anti-Air は jump attack を止める行動で、anti-air special / normal / Super、air-to-air、walk-under、low profile を挙げる。 |
| Punishes | Punish combo route 練習では、最初の攻撃に追加 `+4` hit advantage があることを前提に、通常より強い route が開く場合があると説明する。 |

## Numeric / timing summary

この section は raw source の数値を wiki query で探しやすくするための compiled view。根拠は `raw/web-pages/wiki.supercombo.gg/defense/page.raw.wikitext`。

### Blocking

| Topic | SuperCombo Defense source fact |
|---|---|
| Basic block input | 相手から離れる方向。Standing block は back、crouch block は down-back。 |
| Cannot block | Airborne 中、または自分の attack recovery 中。 |
| Guard direction | Overhead / High は standing block、Low は crouching block、cross-up は相手の下を歩くような forward guard を要求する。 |
| Auto / Absolute Guard | True blockstring 中は mid / overhead を自動 block するが、Low は crouch block が必要。Crouch block 中の overhead は auto-guard されない。 |
| Proximity Guard | 相手攻撃の startup 中に back hold すると、hit 前に blocking animation へ入ることがある。Source は、SF6 では前作群よりかなり弱まり、最大射程外では通常起きにくいと説明する。 |

### Throw Escape

| Throw escape property | SuperCombo Defense source fact |
|---|---:|
| Input | `LP+LK` |
| Defender Drive gain on success | `5000` Drive Gauge / `1/2` bar |
| Tech input window | Thrown state の `9th` frame まで。Throw が接続した frame を含む。 |
| Non-techable throws | Command grabs、air throws、相手が throw できない状態で接続した throws。 |
| Drive Rush movement throw | DR movement frames 中に接続した throw は Counter-hit 扱いになり、throw escape できない。 |
| Option-select restriction | 9 frame window 中に grounded throw を neutral で出せなくする input があると throw escape にならない。Forward Dash `66` は既知の例外。 |

### Wake-up / reversal timing

| Topic | SuperCombo Defense source fact |
|---|---:|
| Rise types | Normal Rise / Back Rise |
| Back Rise input | Landing 時に 2 buttons hold / input |
| Knockdown frame advantage | Normal Rise と Back Rise で差はない。距離が変わらなければ meaty setup は影響を受けない。 |
| Hard Knockdown | Back Rise を完全に防ぐ。Source example は Punish Counter throw。 |
| Wake-up forced standing | Crouch animation は最初 `4f` が forced standing、hurtbox shrink は frame `5`。 |
| Air reset forced standing | Landing frame 自体を除いて `2` forced standing frames。 |
| Reversal buffer on wake-up | `10f` buffer。True reversal frame を含めると total `11f` window。 |
| Reversal buffer after hitstun / blockstun / air reset | `4f` buffer。True reversal frame を含めると total `5f` window。 |
| Dash buffer | 全 scenario で `7f` が intended と説明されるが、一部 bugged case があるとする。 |

### Armor / punish

| Topic | SuperCombo Defense source fact |
|---|---:|
| Armor damage | Absorbed attack の normal damage `50%` を recoverable damage として受ける。 |
| Armor loses to | Any Throw. |
| Armor Break examples | Super Arts、Drive Reversals。 |
| Punish route bonus | Punish combo の first attack は `4` extra frames of hit advantage を持つ。 |

## 関連概念

- [[concepts/defense]]
- [[concepts/terms/blocking]]
- [[concepts/terms/throw-escape]]
- [[concepts/terms/drive-parry]]
- [[concepts/terms/wake-up]]
- [[concepts/terms/reversal]]
- [[concepts/terms/armor]]
- [[concepts/terms/anti-air]]
- [[concepts/terms/guaranteed-punish]]
- [[concepts/frame-data]]
- [[concepts/drive-system]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- Drive Parry、Perfect Parry、Drive Reversal、Drive Impact、Overdrive、Super Art など公式 source と重なる system mechanics は公式 source または既存 source page を優先し、Defense page は defensive use case と timing notes の補助 source とする。
- Throw escape / Reversal / Cross-up / Armor Break は SuperCombo HUD page の display cue と重なる。HUD page は表示 cue、Defense page は defensive input / timing / counterplay の補助 source として分ける。
- Defense page の rendered table は navigation table のみ。本文数値は prose 由来なので、今回は `wiki/outputs/data/` の derived JSON を作らず、source page と term pages に索引として保持する。

## 未解決の質問

- Throw escape window、reversal buffer、wake-up forced standing frames、armor damage を公式 source または実機検証で照合するか。
- Blocking / proximity guard / wake-up crouch block の lab notes を、将来の defensive mechanics synthesis に昇格するか。
- Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric facts を derived JSON にする基準をどうするか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/defense/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/defense/page.raw.wikitext`
- Rendered DOM: `raw/web-pages/wiki.supercombo.gg/defense/rendered/main.dom.json`
- Media DOM: `raw/web-pages/wiki.supercombo.gg/defense/rendered/media.dom.json`
- Image manifest: `raw/web-pages/wiki.supercombo.gg/defense/images/manifest.json`
- Scoped screenshots: `raw/web-pages/wiki.supercombo.gg/defense/screenshots/`
- Validation: `raw/web-pages/wiki.supercombo.gg/defense/validation.json`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/Defense
