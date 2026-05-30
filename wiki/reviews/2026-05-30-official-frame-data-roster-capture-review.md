---
type: review
review_type: capture_validation
created: 2026-05-30
status: open
sources:
  - "[[sources/capcom-official-luke-frame-data]]"
  - "[[sources/capcom-official-jamie-frame-data]]"
  - "[[sources/capcom-official-guile-frame-data]]"
  - "[[sources/capcom-official-kimberly-frame-data]]"
  - "[[sources/capcom-official-juri-frame-data]]"
  - "[[sources/capcom-official-ken-frame-data]]"
  - "[[sources/capcom-official-blanka-frame-data]]"
  - "[[sources/capcom-official-dhalsim-frame-data]]"
  - "[[sources/capcom-official-e-honda-frame-data]]"
  - "[[sources/capcom-official-dee-jay-frame-data]]"
  - "[[sources/capcom-official-manon-frame-data]]"
  - "[[sources/capcom-official-marisa-frame-data]]"
  - "[[sources/capcom-official-lily-frame-data]]"
  - "[[sources/capcom-official-cammy-frame-data]]"
  - "[[sources/capcom-official-rashid-frame-data]]"
  - "[[sources/capcom-official-aki-frame-data]]"
  - "[[sources/capcom-official-ed-frame-data]]"
  - "[[sources/capcom-official-gouki-akuma-frame-data]]"
  - "[[sources/capcom-official-vega-m-bison-frame-data]]"
  - "[[sources/capcom-official-terry-frame-data]]"
  - "[[sources/capcom-official-mai-frame-data]]"
  - "[[sources/capcom-official-elena-frame-data]]"
  - "[[sources/capcom-official-sagat-frame-data]]"
  - "[[sources/capcom-official-c-viper-frame-data]]"
  - "[[sources/capcom-official-alex-frame-data]]"
  - "[[sources/capcom-official-ingrid-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/luke]]"
  - "[[entities/jamie]]"
  - "[[entities/guile]]"
  - "[[entities/kimberly]]"
  - "[[entities/juri]]"
  - "[[entities/ken]]"
  - "[[entities/blanka]]"
  - "[[entities/dhalsim]]"
  - "[[entities/e-honda]]"
  - "[[entities/dee-jay]]"
aliases:
  - "full roster frame data capture review"
tags:
  - review
  - frame-data
  - official
---

# 公式 frame-data roster capture review - 2026-05-30

## 要約

2026-05-30 batch では、既存の JP / Ryu / Chun-Li / Zangief 以外の 26 characters について、Capcom 公式 frame-data raw snapshots と派生 outputs を追加した。26 captures はすべて自動 validation を通過している。既存の 4 accepted captures と合わせて、この wiki には 30 character data slugs 分の Classic / Modern frame-data outputs がある。

## 新規 capture 一覧

| Character | Data slug | Classic rows | Modern rows | Source page |
|---|---|---:|---:|---|
| Luke（ルーク） | `luke` | 76 | 73 | [[sources/capcom-official-luke-frame-data]] |
| Jamie（ジェイミー） | `jamie` | 103 | 98 | [[sources/capcom-official-jamie-frame-data]] |
| Guile（ガイル） | `guile` | 80 | 76 | [[sources/capcom-official-guile-frame-data]] |
| Kimberly（キンバリー） | `kimberly` | 86 | 84 | [[sources/capcom-official-kimberly-frame-data]] |
| Juri（ジュリ） | `juri` | 87 | 82 | [[sources/capcom-official-juri-frame-data]] |
| Ken（ケン） | `ken` | 76 | 71 | [[sources/capcom-official-ken-frame-data]] |
| Blanka（ブランカ） | `blanka` | 91 | 83 | [[sources/capcom-official-blanka-frame-data]] |
| Dhalsim（ダルシム） | `dhalsim` | 89 | 75 | [[sources/capcom-official-dhalsim-frame-data]] |
| E. Honda（エドモンド本田） | `ehonda` | 70 | 65 | [[sources/capcom-official-e-honda-frame-data]] |
| Dee Jay（ディージェイ） | `deejay` | 105 | 101 | [[sources/capcom-official-dee-jay-frame-data]] |
| Manon（マノン） | `manon` | 59 | 53 | [[sources/capcom-official-manon-frame-data]] |
| Marisa（マリーザ） | `marisa` | 91 | 80 | [[sources/capcom-official-marisa-frame-data]] |
| Lily（リリー） | `lily` | 74 | 71 | [[sources/capcom-official-lily-frame-data]] |
| Cammy（キャミィ） | `cammy` | 75 | 73 | [[sources/capcom-official-cammy-frame-data]] |
| Rashid（ラシード） | `rashid` | 85 | 72 | [[sources/capcom-official-rashid-frame-data]] |
| A.K.I. | `aki` | 64 | 57 | [[sources/capcom-official-aki-frame-data]] |
| Ed（エド） | `ed` | 70 | 68 | [[sources/capcom-official-ed-frame-data]] |
| Gouki / Akuma（豪鬼） | `gouki_akuma` | 91 | 83 | [[sources/capcom-official-gouki-akuma-frame-data]] |
| Vega / M. Bison（ベガ） | `vega_mbison` | 72 | 69 | [[sources/capcom-official-vega-m-bison-frame-data]] |
| Terry（テリー） | `terry` | 66 | 60 | [[sources/capcom-official-terry-frame-data]] |
| Mai（不知火舞） | `mai` | 90 | 85 | [[sources/capcom-official-mai-frame-data]] |
| Elena（エレナ） | `elena` | 79 | 74 | [[sources/capcom-official-elena-frame-data]] |
| Sagat（サガット） | `sagat` | 70 | 69 | [[sources/capcom-official-sagat-frame-data]] |
| C. Viper（C.ヴァイパー） | `cviper` | 69 | 67 | [[sources/capcom-official-c-viper-frame-data]] |
| Alex（アレックス） | `alex` | 74 | 73 | [[sources/capcom-official-alex-frame-data]] |
| Ingrid（イングリッド） | `ingrid` | 75 | 74 | [[sources/capcom-official-ingrid-frame-data]] |

## 自動検証

- 新規 manifest はすべて `raw/official/frame-data/2026-05-30/<character>/` 配下にある。
- 各 character は Classic / Modern raw directories を持ち、`page.html`、`table.dom.json`、`screenshot.png`、`metadata.json` が保存されている。
- metadata と manifest は publisher、source URL、capture timestamp、character slug、control scheme を含む。
- `tools/validate_capcom_frame_data.py` は、各 character / control scheme について、raw DOM artifact から saved CSV rows を再現した。
- 同 tool は field-meaning JSON records も raw DOM artifact から再現した。
- screenshot metadata は full table coverage と Cookiebot/navigation overlay removal を示す。
- 既存 accepted の JP、Ryu、Chun-Li、Zangief captures も batch 後に再検証された。

## slug に関する注意

- official character links では `gouki` と `vega` が見えるが、table を持つ frame-data pages は `gouki_akuma` と `vega_mbison`。
- `gouki` の最初の capture attempt は site 404 page の empty manifest になったため、wiki filing 前に削除された。

## 最終判断

自動 validation は passed。26 captures を accepted にするには、代表 screenshot / source review などの人間レビューがまだ必要。
