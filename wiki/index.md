# Wiki Index

This is the content-oriented catalog for the LLM-maintained wiki.

The LLM should read this file first before answering questions or deciding
which wiki pages to inspect.

## Sources

| Page | Summary | Source date | Source type | Status |
|---|---|---:|---|---|
| [[sources/supercombo-street-fighter-6-glossary]] | SuperCombo Wiki glossary for Drive System, frame data, juggle, and notation terms. | 2026-01-31 | wiki_page | active |
| [[sources/capcom-official-jp-frame-data]] | Capcom official JP frame-data capture with Classic/Modern raw snapshots, derived CSVs, and field meanings. | 2026-05-26 | official_frame_data | active |
| [[sources/capcom-official-ryu-frame-data]] | Capcom official Ryu frame-data capture with Classic/Modern raw snapshots, derived CSVs, and field meanings. | 2026-05-27 | official_frame_data | active |
| [[sources/capcom-official-chun-li-frame-data]] | Capcom official Chun-Li frame-data capture with Classic/Modern raw snapshots, derived CSVs, and field meanings. | 2026-05-27 | official_frame_data | active |
| [[sources/capcom-official-zangief-frame-data]] | Capcom official Zangief frame-data capture with Classic/Modern raw snapshots, derived CSVs, and field meanings. | 2026-05-27 | official_frame_data | active |

## Concepts

| Page | Summary | Related |
|---|---|---|
| [[concepts/drive-system]] | Meter system glossary concept for Drive-related movement, offense, defense, and burnout terms. | [[concepts/frame-data]], [[entities/street-fighter-6]] |
| [[concepts/frame-data]] | Timing/property vocabulary, official JP/Ryu/Chun-Li/Zangief frame-data captures, and accepted Classic/Modern comparison policy. | [[concepts/drive-system]], [[concepts/juggle-system]], [[concepts/fighting-game-notation]], [[entities/jp]], [[entities/ryu]], [[entities/chun-li]], [[entities/zangief]] |
| [[concepts/juggle-system]] | Glossary concept for free/limited juggle states and Juggle Count/Start/Increase/Limit terminology. | [[concepts/frame-data]], [[entities/street-fighter-6]] |
| [[concepts/fighting-game-notation]] | Compact notation for links, cancels, holds, releases, chains, hit states, air actions, delays, and directional inputs. | [[concepts/frame-data]] |

## Entities

| Page | Summary | Type |
|---|---|---|
| [[entities/street-fighter-6]] | Game context for the ingested community glossary and official JP/Ryu/Chun-Li/Zangief frame-data sources. | other |
| [[entities/supercombo-wiki]] | Source site for the first ingested raw source. | other |
| [[entities/capcom]] | Publisher of the official Street Fighter 6 frame-data sources. | company |
| [[entities/jp]] | Street Fighter 6 character covered by the first official frame-data capture. | character |
| [[entities/ryu]] | Street Fighter 6 character covered by the second official frame-data capture. | character |
| [[entities/chun-li]] | Street Fighter 6 character covered by the third official frame-data capture. | character |
| [[entities/zangief]] | Street Fighter 6 character covered by the fourth official frame-data capture. | character |

## Syntheses

| Page | Summary | Updated |
|---|---|---:|

## Questions

| Page | Question | Summary | Updated |
|---|---|---|---:|
| [[questions/jp-modern-vs-classic-frame-data-moves-and-inputs]] | JPのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | JP Classic/Modernの項目数、Classic専用項目、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/ryu-modern-vs-classic-frame-data-moves-and-inputs]] | Ryuのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Ryu Classic/Modernの項目数、技名差分、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/chun-li-modern-vs-classic-frame-data-moves-and-inputs]] | Chun-Liのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Chun-Li Classic/Modernの項目数、技名差分、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/zangief-modern-vs-classic-frame-data-moves-and-inputs]] | Zangiefのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Zangief Classic/Modernの項目数、技名差分、一回転/二回転入力、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |

## Outputs

| Page | Type | Summary | Updated |
|---|---|---|---:|
| `wiki/outputs/data/frame-data/jp/classic.csv` | csv | Derived JP Classic frame-data rows from the official Capcom capture. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/modern.csv` | csv | Derived JP Modern frame-data rows from the official Capcom capture. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/classic.field-meanings.json` | json | Field explanations extracted from the Classic frame-data table header. | 2026-05-26 |
| `wiki/outputs/data/frame-data/jp/modern.field-meanings.json` | json | Field explanations extracted from the Modern frame-data table header. | 2026-05-26 |
| `wiki/outputs/data/frame-data/ryu/classic.csv` | csv | Derived Ryu Classic frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/ryu/modern.csv` | csv | Derived Ryu Modern frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json` | json | Field explanations extracted from the Ryu Classic frame-data table header. | 2026-05-27 |
| `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json` | json | Field explanations extracted from the Ryu Modern frame-data table header. | 2026-05-27 |
| `wiki/outputs/data/frame-data/chunli/classic.csv` | csv | Derived Chun-Li Classic frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/chunli/modern.csv` | csv | Derived Chun-Li Modern frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json` | json | Field explanations extracted from the Chun-Li Classic frame-data table header. | 2026-05-27 |
| `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json` | json | Field explanations extracted from the Chun-Li Modern frame-data table header. | 2026-05-27 |
| `wiki/outputs/data/frame-data/zangief/classic.csv` | csv | Derived Zangief Classic frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/zangief/modern.csv` | csv | Derived Zangief Modern frame-data rows from the official Capcom capture. | 2026-05-27 |
| `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json` | json | Field explanations extracted from the Zangief Classic frame-data table header. | 2026-05-27 |
| `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json` | json | Field explanations extracted from the Zangief Modern frame-data table header. | 2026-05-27 |

## Reviews

| Page | Review type | Summary | Status |
|---|---|---|---|
| [[reviews/2026-05-26-official-jp-frame-data-capture-review]] | capture_validation | Review accepted the official JP frame-data raw snapshot and derived outputs. | accepted |
| [[reviews/2026-05-27-official-ryu-frame-data-capture-review]] | capture_validation | Review accepted the official Ryu frame-data raw snapshot and derived outputs. | accepted |
| [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]] | capture_validation | Review accepted the official Chun-Li frame-data raw snapshot and derived outputs. | accepted |
| [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | capture_validation | Review accepted the official Zangief frame-data raw snapshot and derived outputs. | accepted |
| [[reviews/2026-05-27-health-check]] | health_check | Checked wiki structure, stale open questions, question-page cleanliness, and accepted frame-data outputs after four character captures. | open |
