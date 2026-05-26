# Wiki Index

This is the content-oriented catalog for the LLM-maintained wiki.

The LLM should read this file first before answering questions or deciding
which wiki pages to inspect.

## Sources

| Page | Summary | Source date | Source type | Status |
|---|---|---:|---|---|
| [[sources/supercombo-street-fighter-6-glossary]] | SuperCombo Wiki glossary for Drive System, frame data, juggle, and notation terms. | 2026-01-31 | wiki_page | active |
| [[sources/capcom-official-jp-frame-data]] | Capcom official JP frame-data capture with Classic/Modern raw snapshots, derived CSVs, and field meanings. | 2026-05-26 | official_frame_data | active |

## Concepts

| Page | Summary | Related |
|---|---|---|
| [[concepts/drive-system]] | Meter system glossary concept for Drive-related movement, offense, defense, and burnout terms. | [[concepts/frame-data]], [[entities/street-fighter-6]] |
| [[concepts/frame-data]] | Timing and property vocabulary plus reviewed official JP structured frame-data capture. | [[concepts/drive-system]], [[concepts/juggle-system]], [[concepts/fighting-game-notation]], [[entities/jp]] |
| [[concepts/juggle-system]] | Glossary concept for free/limited juggle states and Juggle Count/Start/Increase/Limit terminology. | [[concepts/frame-data]], [[entities/street-fighter-6]] |
| [[concepts/fighting-game-notation]] | Compact notation for links, cancels, holds, releases, chains, hit states, air actions, delays, and directional inputs. | [[concepts/frame-data]] |

## Entities

| Page | Summary | Type |
|---|---|---|
| [[entities/street-fighter-6]] | Game context for the ingested community glossary and official JP frame-data source. | other |
| [[entities/supercombo-wiki]] | Source site for the first ingested raw source. | other |
| [[entities/capcom]] | Publisher of the official Street Fighter 6 frame-data source. | company |
| [[entities/jp]] | Street Fighter 6 character covered by the first official frame-data capture. | character |

## Syntheses

| Page | Summary | Updated |
|---|---|---:|

## Questions

| Page | Question | Summary | Updated |
|---|---|---|---:|
| [[questions/how-juggles-work-internally]] | ジャグルって内部的にどういう仕組みで発生するんですか？ | Explains juggle checks using Juggle Count, Start, Increase, and Limit from the ingested glossary. | 2026-05-26 |

## Outputs

| Page | Type | Summary | Updated |
|---|---|---|---:|
| `wiki/outputs/data/frame-data/jp/classic.csv` | csv | Derived JP Classic frame-data rows from the official Capcom capture. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/modern.csv` | csv | Derived JP Modern frame-data rows from the official Capcom capture. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/classic.field-meanings.json` | json | Field explanations extracted from the Classic frame-data table header. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/modern.field-meanings.json` | json | Field explanations extracted from the Modern frame-data table header. | 2026-05-26 |

## Reviews

| Page | Review type | Summary | Status |
|---|---|---|---|
| [[reviews/2026-05-26-health-check]] | lint | Initial health check after first source ingest and first filed-back query. | open |
| [[reviews/2026-05-26-official-jp-frame-data-capture-review]] | human_review | Review accepted the official JP frame-data raw snapshot and derived outputs. | accepted |
