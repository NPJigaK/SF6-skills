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
tags:
  - review
  - frame-data
  - official
---

# Official Frame Data Roster Capture Review - 2026-05-30

## Summary

The 2026-05-30 batch added official Capcom frame-data raw snapshots and derived
outputs for 26 characters that were not previously represented as character
frame-data sources in the wiki. All 26 new captures passed automated validation.
Together with the four earlier human-accepted captures for JP, Ryu, Chun-Li,
and Zangief, the wiki now has derived Classic and Modern frame-data outputs for
30 character slugs.

## New captures reviewed

| Character | Data slug | Classic rows | Modern rows | Source page |
|---|---|---:|---:|---|
| Luke | `luke` | 76 | 73 | [[sources/capcom-official-luke-frame-data]] |
| Jamie | `jamie` | 103 | 98 | [[sources/capcom-official-jamie-frame-data]] |
| Guile | `guile` | 80 | 76 | [[sources/capcom-official-guile-frame-data]] |
| Kimberly | `kimberly` | 86 | 84 | [[sources/capcom-official-kimberly-frame-data]] |
| Juri | `juri` | 87 | 82 | [[sources/capcom-official-juri-frame-data]] |
| Ken | `ken` | 76 | 71 | [[sources/capcom-official-ken-frame-data]] |
| Blanka | `blanka` | 91 | 83 | [[sources/capcom-official-blanka-frame-data]] |
| Dhalsim | `dhalsim` | 89 | 75 | [[sources/capcom-official-dhalsim-frame-data]] |
| E. Honda | `ehonda` | 70 | 65 | [[sources/capcom-official-e-honda-frame-data]] |
| Dee Jay | `deejay` | 105 | 101 | [[sources/capcom-official-dee-jay-frame-data]] |
| Manon | `manon` | 59 | 53 | [[sources/capcom-official-manon-frame-data]] |
| Marisa | `marisa` | 91 | 80 | [[sources/capcom-official-marisa-frame-data]] |
| Lily | `lily` | 74 | 71 | [[sources/capcom-official-lily-frame-data]] |
| Cammy | `cammy` | 75 | 73 | [[sources/capcom-official-cammy-frame-data]] |
| Rashid | `rashid` | 85 | 72 | [[sources/capcom-official-rashid-frame-data]] |
| A.K.I. | `aki` | 64 | 57 | [[sources/capcom-official-aki-frame-data]] |
| Ed | `ed` | 70 | 68 | [[sources/capcom-official-ed-frame-data]] |
| Gouki / Akuma | `gouki_akuma` | 91 | 83 | [[sources/capcom-official-gouki-akuma-frame-data]] |
| Vega / M. Bison | `vega_mbison` | 72 | 69 | [[sources/capcom-official-vega-m-bison-frame-data]] |
| Terry | `terry` | 66 | 60 | [[sources/capcom-official-terry-frame-data]] |
| Mai | `mai` | 90 | 85 | [[sources/capcom-official-mai-frame-data]] |
| Elena | `elena` | 79 | 74 | [[sources/capcom-official-elena-frame-data]] |
| Sagat | `sagat` | 70 | 69 | [[sources/capcom-official-sagat-frame-data]] |
| C. Viper | `cviper` | 69 | 67 | [[sources/capcom-official-c-viper-frame-data]] |
| Alex | `alex` | 74 | 73 | [[sources/capcom-official-alex-frame-data]] |
| Ingrid | `ingrid` | 75 | 74 | [[sources/capcom-official-ingrid-frame-data]] |

## Automated checks

- Every new manifest is under `raw/official/frame-data/2026-05-30/<character>/`.
- Every new character has separate Classic and Modern raw directories with
  `page.html`, `table.dom.json`, `screenshot.png`, and `metadata.json`.
- Metadata and manifests include publisher, source URL, capture timestamps,
  character slug, and control scheme.
- `tools/validate_capcom_frame_data.py` reproduced all saved CSV rows from raw
  DOM artifacts for each new character and control scheme.
- `tools/validate_capcom_frame_data.py` reproduced all saved field-meaning JSON
  records from raw DOM artifacts for each new character and control scheme.
- Screenshot metadata reports full table coverage checks and no visible
  Cookiebot/navigation overlays after cleanup.
- Existing accepted JP, Ryu, Chun-Li, and Zangief captures were also revalidated
  after the batch.

## Special slug findings

- The official character links expose `gouki` and `vega`, but the frame-data
  pages that contain tables are `gouki_akuma` and `vega_mbison`.
- A first attempt to capture `gouki` produced an empty manifest pointing at the
  site's 404 page; that invalid generated artifact was removed before filing
  wiki pages.

## Final decision

Automated validation passed. Human review is still required before marking the
26 new captures as accepted.

## Requires human review

- Spot-check representative screenshots, especially wide tables and special
  input-token cases.
- Decide whether the 26 new captures should receive individual accepted review
  pages or whether this batch review is enough.
- Decide whether to recapture JP, Ryu, Chun-Li, and Zangief under the same
  2026-05-30 date label for a single-date full-roster snapshot.
