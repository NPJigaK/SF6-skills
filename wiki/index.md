# Wiki Index

このファイルは LLM-maintained wiki の内容指向カタログです。質問に答える時や、読むべき wiki page を決める時は最初にこのファイルを見ます。

## Raw 保存方針

`raw/` は原則として、原文・元データを保つ原本保存層です。ただし manifest の `storage_policy` で最新ミラーまたは更新可能な取得一式と示されている raw 一式は、path を固定したまま再取得、取得物の差し替え、manifest / metadata / validation / hash 更新を行える。日付や revision は path ではなく manifest の由来を示す項目で確認する。

| Raw 一式 | 現在の `storage_policy` | 入口 |
|---|---|---|
| Frame data | `latest_frame_data_mirror` | `raw/frame-data/official/<data-slug>/manifest.json`, `raw/frame-data/supercombo/<character_slug>/manifest.json` |
| Battle change list | `latest_battle_change_mirror` | `raw/battle-change/official/manifest.json` |
| Web page 取得 | `updateable_web_page_capture` | `raw/web-pages/<domain>/<repo-local-page-slug>/manifest.json` |

翻訳、要約、正規化した置き換え版は更新可能な raw 一式にも置かず、wiki layer か derived output layer に置く。

## Web-page Raw 取得

Web page source は `raw/web-pages/<domain>/<repo-local-page-slug>/manifest.json` を entrypoint とする。この repo は Street Fighter 6 専用なので、raw path の page slug では game prefix を省いてよい。

| Source family | Raw entrypoint | Canonical raw 取得物 | 由来 |
|---|---|---|---|
| SuperCombo glossary | `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json` | `page.raw.wikitext`; 表示証拠は `page.html`、`rendered/tables.dom.json`; notation template は `templates/combo-legend-sf6.raw.wikitext` | `storage_policy: updateable_web_page_capture`; page revid `351898`; `Template:ComboLegend-SF6` revid `283225`; `source_updated_at` 2026-01-31T11:22:26Z; `captured_at_utc` 2026-06-09T13:47:52Z |
| Capcom Fighting Ground Battle System | `raw/web-pages/www.streetfighter.com/fightingground-battle-system/manifest.json` | `api/source-text.scoped.json`; `rendered/battle-system-design.dom.json`, `rendered/drive-gauge.dom.json`, `rendered/common-system.dom.json`, `rendered/simple-operation-modal.dom.json`; 表示証拠は `screenshots/*.png` | `storage_policy: updateable_web_page_capture`; scoped source `fightingground_battle_system_only`; Next.js build ID `8PI3Oj_9ikUinAmp3j_yf`; `captured_at_utc` 2026-06-09T17:13:40Z |
| Capcom eSports BASE terms | `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json` | `source/word-section.raw.html`; `source/modal-open-close.raw.js`; `api/terms.raw.json`; `rendered/word-section.dom.json`; `rendered/modals/`; thumbnail と modal mp4 assets | `storage_policy: updateable_web_page_capture`; scoped source `capcom_esports_base_words_only`; page HTML / JS Last-Modified `2025-11-11T06:17:24Z`; `captured_at_utc` 2026-06-09T17:48:14Z |

## Frame-data Raw 配置

現在の frame-data raw の入口は最新ミラー固定パスです。source freshness、capture date、source revision は path ではなく manifest で確認します。SuperCombo では `source_updated_at` を source freshness、`captured_at_utc` を raw 取得時刻として分けて扱います。派生 output は JSON-only とし、`wiki/outputs/data/frame-data/<variant>/<character>/` に置きます。詳細は [[syntheses/frame-data-raw-layout]]。

| Source family | Raw entrypoint | Provenance | Main outputs |
|---|---|---|---|
| Capcom official | `raw/frame-data/official/<data-slug>/manifest.json`、`classic/`、`modern/` | manifest の `capture_label` / `created_at_utc` / `storage_policy` | `wiki/outputs/data/frame-data/official/<data-slug>/`、[[outputs/reports/2026-05-30-official-frame-data-coverage]] |
| SuperCombo JP | `raw/frame-data/supercombo/jp/manifest.json`、`data.raw.wikitext`、`cargo/`、`rendered/tables.dom.json` | manifest の `source_updated_at` / `captured_at_utc` / `source_revision` | [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]]、[[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]] |
| SuperCombo Ryu | `raw/frame-data/supercombo/ryu/manifest.json`、`data.raw.wikitext`、`cargo/`、`rendered/tables.dom.json` | manifest の `source_updated_at` / `captured_at_utc` / `source_revision` | [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]]、[[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] |
| SuperCombo Zangief | `raw/frame-data/supercombo/zangief/manifest.json`、`data.raw.wikitext`、`cargo/`、`rendered/tables.dom.json` | manifest の `source_updated_at` / `captured_at_utc` / `source_revision` | [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]]、[[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] |
| SuperCombo Ingrid | `raw/frame-data/supercombo/ingrid/manifest.json`、`data.raw.wikitext`、`cargo/`、`rendered/tables.dom.json` | manifest の `source_updated_at` / `captured_at_utc` / `source_revision` | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]、[[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] |
| SuperCombo all characters | `raw/frame-data/supercombo/<character_slug>/manifest.json`、`data.raw.wikitext`、`cargo/`、`rendered/tables.dom.json` | 各 manifest の `source_updated_at` / `captured_at_utc` / `source_revision` | [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]、`wiki/outputs/data/frame-data/supercombo/<character_slug>/`、`wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/` |

## Sources

| Page | Summary | Source date | Source type | Status |
|---|---|---:|---|---|
| [[sources/supercombo-street-fighter-6-glossary]] | SuperCombo Wiki の Street Fighter 6 glossary。`raw/web-pages/` capture は MediaWiki wikitext、HTML、rendered DOM、Notation Glossary の template 依存を保持する。旧 Obsidian clipping は削除済み。 | 2026-01-31 | wiki_page | active |
| [[sources/capcom-official-fightingground-battle-system]] | Capcom 公式 Fighting Ground ページの Battle System scoped capture。Drive Gauge、Common System、ゲーム画面説明 modal を保持し、accessibility / damage / commentary / control type / battle contents は保存しない。 | 2026-06-09 | official_scoped_web_page_capture | active |
| [[sources/capcom-esports-base-terms]] | Capcom 公式 CAPCOM eSports BASE の CPT/SFL 観戦向け用語解説 scoped capture。実況ワード解説 23 語、3段階重要度、thumbnail / modal mp4 / modal DOM を保持し、page 全体は保存しない。 | 2025-11-11 | official_scoped_web_page_capture | active |
| [[sources/supercombo-street-fighter-6-frame-data-batch]] | SuperCombo Wiki の Street Fighter 6 frame-data 30キャラ batch capture。raw wikitext、Cargo API、DOM、5タブ screenshot、公式 Classic との派生 output を含む。Source freshness は各 manifest の `source_updated_at` で 2026-05-30 から 2026-06-02 に分布する。 | 2026-05-30..2026-06-02 | community_frame_data | active |
| [[sources/supercombo-jp-frame-data]] | SuperCombo Wiki の JP frame-data raw 取得データ。新 raw path は `raw/frame-data/supercombo/jp/`。Data wikitext、Cargo API、DOM、5タブのスクリーンショット、画像 123 件を含む community source。 | 2026-05-30 | community_frame_data | active |
| [[sources/supercombo-ryu-frame-data]] | SuperCombo Wiki の Ryu frame-data raw 取得データ。新 raw path は `raw/frame-data/supercombo/ryu/`。Data wikitext、Cargo API、DOM、5タブのスクリーンショット、画像 133 件、conditional variant link を含む community source。 | 2026-05-30 | community_frame_data | active |
| [[sources/supercombo-zangief-frame-data]] | SuperCombo Wiki の Zangief frame-data raw 取得データ。新 raw path は `raw/frame-data/supercombo/zangief/`。Data wikitext、Cargo API、DOM、5タブのスクリーンショット、画像 165 件、360/720 と近距離/中距離/遠距離 override を含む community source。 | 2026-06-01 | community_frame_data | active |
| [[sources/supercombo-ingrid-frame-data]] | SuperCombo Wiki の Ingrid frame-data raw 取得データ。新 raw path は `raw/frame-data/supercombo/ingrid/`。Data wikitext、Cargo API、DOM、5タブのスクリーンショット、image refs 164 件、imageinfo resolved title 2 件 / missing title 156 件、公式 Classic との補助列付き output を含む community source。 | 2026-06-02 | community_frame_data | active |
| [[sources/capcom-official-ryu-frame-data]] | Capcom 公式 Ryu（リュウ） frame-data capture。新 raw path は `raw/frame-data/official/ryu/`。Classic 75 rows / Modern 69 rows。 | 2026-05-27 | official_frame_data | active |
| [[sources/capcom-official-luke-frame-data]] | Capcom 公式 Luke（ルーク） frame-data capture。Classic 76 rows / Modern 73 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-jamie-frame-data]] | Capcom 公式 Jamie（ジェイミー） frame-data capture。Classic 103 rows / Modern 98 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-chun-li-frame-data]] | Capcom 公式 Chun-Li（春麗） frame-data capture。Classic 78 rows / Modern 72 rows。 | 2026-05-27 | official_frame_data | active |
| [[sources/capcom-official-guile-frame-data]] | Capcom 公式 Guile（ガイル） frame-data capture。Classic 80 rows / Modern 76 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-kimberly-frame-data]] | Capcom 公式 Kimberly（キンバリー） frame-data capture。Classic 86 rows / Modern 84 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-juri-frame-data]] | Capcom 公式 Juri（ジュリ） frame-data capture。Classic 87 rows / Modern 82 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-ken-frame-data]] | Capcom 公式 Ken（ケン） frame-data capture。Classic 76 rows / Modern 71 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-blanka-frame-data]] | Capcom 公式 Blanka（ブランカ） frame-data capture。Classic 91 rows / Modern 83 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-dhalsim-frame-data]] | Capcom 公式 Dhalsim（ダルシム） frame-data capture。Classic 89 rows / Modern 75 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-e-honda-frame-data]] | Capcom 公式 E. Honda（エドモンド本田） frame-data capture。Classic 70 rows / Modern 65 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-dee-jay-frame-data]] | Capcom 公式 Dee Jay（ディージェイ） frame-data capture。Classic 105 rows / Modern 101 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-manon-frame-data]] | Capcom 公式 Manon（マノン） frame-data capture。Classic 59 rows / Modern 53 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-marisa-frame-data]] | Capcom 公式 Marisa（マリーザ） frame-data capture。Classic 91 rows / Modern 80 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-jp-frame-data]] | Capcom 公式 JP frame-data capture。新 raw path は `raw/frame-data/official/jp/`。Classic 69 rows / Modern 65 rows。 | 2026-05-26 | official_frame_data | active |
| [[sources/capcom-official-zangief-frame-data]] | Capcom 公式 Zangief（ザンギエフ） frame-data capture。Classic 72 rows / Modern 66 rows。 | 2026-05-27 | official_frame_data | active |
| [[sources/capcom-official-lily-frame-data]] | Capcom 公式 Lily（リリー） frame-data capture。Classic 74 rows / Modern 71 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-cammy-frame-data]] | Capcom 公式 Cammy（キャミィ） frame-data capture。Classic 75 rows / Modern 73 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-rashid-frame-data]] | Capcom 公式 Rashid（ラシード） frame-data capture。Classic 85 rows / Modern 72 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-aki-frame-data]] | Capcom 公式 A.K.I. frame-data capture。Classic 64 rows / Modern 57 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-ed-frame-data]] | Capcom 公式 Ed（エド） frame-data capture。Classic 70 rows / Modern 68 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-gouki-akuma-frame-data]] | Capcom 公式 Gouki / Akuma（豪鬼） frame-data capture。Classic 91 rows / Modern 83 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-vega-m-bison-frame-data]] | Capcom 公式 Vega / M. Bison（ベガ） frame-data capture。Classic 72 rows / Modern 69 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-terry-frame-data]] | Capcom 公式 Terry（テリー） frame-data capture。Classic 66 rows / Modern 60 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-mai-frame-data]] | Capcom 公式 Mai（不知火舞） frame-data capture。Classic 90 rows / Modern 85 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-elena-frame-data]] | Capcom 公式 Elena（エレナ） frame-data capture。Classic 79 rows / Modern 74 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-sagat-frame-data]] | Capcom 公式 Sagat（サガット） frame-data capture。Classic 70 rows / Modern 69 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-c-viper-frame-data]] | Capcom 公式 C. Viper（C.ヴァイパー） frame-data capture。Classic 69 rows / Modern 67 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-alex-frame-data]] | Capcom 公式 Alex（アレックス） frame-data capture。Classic 74 rows / Modern 73 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-ingrid-frame-data]] | Capcom 公式 Ingrid（イングリッド） frame-data capture。Classic 75 rows / Modern 74 rows。 | 2026-05-30 | official_frame_data | active |
| [[sources/capcom-official-battle-change-list]] | Capcom 公式 Battle Change List capture。20 update version、policy 123 rows / common 100 rows / fighter 1597 rows の派生 output を含む。 | 2026-06-06 | official_battle_change | active |

## Concepts

| Page | Summary | Related |
|---|---|---|
| [[concepts/terms/index]] | SF6 用語の統合 index。Capcom eSports BASE、Capcom Fighting Ground、SuperCombo glossary 由来の 36 個別 term pages を集約し、公式 / community source claims を用語ごとに保持する。 | [[concepts/drive-system]], [[concepts/frame-data]], [[concepts/fighting-game-notation]], [[concepts/juggle-system]], [[entities/street-fighter-6]] |
| [[concepts/drive-system]] | Drive gauge に紐づく movement、offense、defense、burnout などの共通 system。Capcom 公式 Fighting Ground source と eSports BASE 用語解説で Battle System / 観戦用語の根拠を追加した。 | [[concepts/terms/index]], [[concepts/terms/burnout]], [[concepts/terms/drive-impact]], [[concepts/terms/drive-parry]], [[concepts/terms/drive-reversal]], [[concepts/terms/drive-rush-cancel]], [[concepts/frame-data]], [[entities/street-fighter-6]] |
| [[concepts/frame-data]] | 技の timing/property vocabulary、Capcom 公式 eSports BASE の frame / counter / hit confirm 観戦用語、30 character data slugs 分の公式 Classic / Modern coverage、SuperCombo 30キャラ community raw 取得データ、公式 + SuperCombo 補助列付き output、最新ミラー raw 配置方針、SuperCombo review queue 優先順。 | [[concepts/terms/index]], [[concepts/drive-system]], [[concepts/juggle-system]], [[concepts/fighting-game-notation]], [[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]], [[entities/street-fighter-6]] |
| [[concepts/juggle-system]] | Free/Limited Juggle、Juggle Count/Start/Increase/Limit、Air Reset / wall bounce などの community terms。 | [[concepts/frame-data]], [[concepts/terms/air-reset]], [[concepts/terms/wall-bounce]], [[entities/street-fighter-6]] |
| [[concepts/fighting-game-notation]] | link、cancel、hold/release、chain、hit state、air action、delay、directional input などの notation。SuperCombo glossary では `ComboLegend-SF6` template に由来する。 | [[concepts/frame-data]], [[concepts/terms/cancel]], [[concepts/terms/chain]] |

## Term Pages

個別 term page は `wiki/index.md` に direct row を持たせ、詳細な source claim の統合は [[concepts/terms/index]] に集約する。

| Page | Term / 表記 | Primary source family | Main concepts |
|---|---|---|---|
| [[concepts/terms/abare]] | 暴れ / abare | Capcom eSports BASE | [[concepts/terms/invincible-move]], [[concepts/terms/meaty]] |
| [[concepts/terms/air-reset]] | Air Reset / 空中リセット | SuperCombo glossary | [[concepts/juggle-system]], [[concepts/terms/wall-bounce]] |
| [[concepts/terms/anti-air]] | 対空 / anti-air | Capcom eSports BASE | [[concepts/drive-system]] |
| [[concepts/terms/burnout]] | バーンアウト / Burnout | Capcom Fighting Ground, Capcom eSports BASE, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/chip-damage]], [[concepts/terms/stun]] |
| [[concepts/terms/cancel]] | キャンセル / Cancel | Capcom Fighting Ground, SuperCombo glossary | [[concepts/fighting-game-notation]], [[concepts/terms/drive-rush-cancel]], [[concepts/terms/chain]] |
| [[concepts/terms/chain]] | Chain / Chn | SuperCombo glossary | [[concepts/fighting-game-notation]], [[concepts/terms/cancel]] |
| [[concepts/terms/chip-damage]] | 削り / chip damage | Capcom eSports BASE | [[concepts/drive-system]], [[concepts/terms/burnout]] |
| [[concepts/terms/command-throw]] | コマ投げ / command throw | Capcom eSports BASE | [[concepts/terms/shimmy]] |
| [[concepts/terms/corner]] | 画面端 / corner | Capcom eSports BASE | [[concepts/terms/stun]], [[concepts/terms/oki]] |
| [[concepts/terms/critical-art]] | Critical Art / CA | Official Zangief frame data, SuperCombo Zangief frame data | [[concepts/terms/super-art]], [[concepts/frame-data]] |
| [[concepts/terms/cross-up]] | めくり / cross-up | Capcom eSports BASE | [[concepts/terms/anti-air]] |
| [[concepts/terms/damage-scaling]] | ダメージ補正 / damage scaling | Capcom eSports BASE, SuperCombo glossary | [[concepts/frame-data]], [[concepts/terms/scaling-reset]] |
| [[concepts/terms/drive-impact]] | Drive Impact / ドライブインパクト | Capcom Fighting Ground, Capcom eSports BASE, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/drive-impact-counter]], [[concepts/terms/wall-bounce]] |
| [[concepts/terms/drive-impact-counter]] | インパクト返し / Drive Impact counter | Capcom eSports BASE | [[concepts/drive-system]], [[concepts/terms/drive-impact]], [[concepts/terms/corner]] |
| [[concepts/terms/drive-parry]] | Drive Parry / ドライブパリィ | Capcom Fighting Ground, Capcom eSports BASE, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/perfect-parry]], [[concepts/terms/raw-drive-rush]] |
| [[concepts/terms/drive-reversal]] | Drive Reversal / ドライブリバーサル | Capcom Fighting Ground, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/invincible-move]] |
| [[concepts/terms/drive-rush-cancel]] | Drive Rush Cancel / DRC / キャンセルラッシュ | Capcom Fighting Ground, Capcom eSports BASE, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/cancel]], [[concepts/terms/frame-advantage]] |
| [[concepts/terms/frame-advantage]] | 有利 frame / frame advantage | Capcom eSports BASE | [[concepts/frame-data]] |
| [[concepts/terms/guaranteed-punish]] | 確定反撃 / guaranteed punish | Capcom eSports BASE | [[concepts/terms/frame-advantage]], [[concepts/terms/punish-counter]] |
| [[concepts/terms/hit-confirm]] | ヒット確認 / hit confirm | Capcom eSports BASE | [[concepts/frame-data]], [[concepts/terms/frame-advantage]] |
| [[concepts/terms/invincible-move]] | 無敵技 / invincible move | Capcom eSports BASE | [[concepts/terms/abare]], [[concepts/terms/drive-reversal]] |
| [[concepts/terms/lethal]] | リーサル / lethal | Capcom eSports BASE | [[concepts/terms/hit-confirm]] |
| [[concepts/terms/meaty]] | 重ね / meaty | Capcom eSports BASE | [[concepts/terms/oki]], [[concepts/terms/setplay]] |
| [[concepts/terms/oki]] | 起き攻め / oki | Capcom eSports BASE | [[concepts/terms/meaty]], [[concepts/terms/setplay]] |
| [[concepts/terms/overdrive]] | Overdrive / OD | Capcom Fighting Ground, SuperCombo glossary | [[concepts/drive-system]], [[concepts/terms/burnout]] |
| [[concepts/terms/perfect-parry]] | ジャストパリィ / Perfect Parry | Capcom eSports BASE | [[concepts/drive-system]], [[concepts/terms/drive-parry]], [[concepts/terms/damage-scaling]] |
| [[concepts/terms/punish-counter]] | パニッシュカウンター / Punish Counter | Capcom eSports BASE | [[concepts/frame-data]], [[concepts/terms/guaranteed-punish]] |
| [[concepts/terms/raw-drive-rush]] | 生ラッシュ / raw Drive Rush | Capcom eSports BASE | [[concepts/drive-system]], [[concepts/terms/drive-parry]], [[concepts/terms/frame-advantage]] |
| [[concepts/terms/scaling-reset]] | 補正切り / scaling reset | Capcom eSports BASE | [[concepts/terms/damage-scaling]], [[concepts/terms/hit-confirm]] |
| [[concepts/terms/setplay]] | セットプレイ / setplay | Capcom eSports BASE | [[concepts/terms/oki]], [[concepts/terms/meaty]] |
| [[concepts/terms/shikomi]] | 仕込み / option-select-like input | Capcom eSports BASE | [[concepts/terms/hit-confirm]], [[concepts/terms/whiff-punish]] |
| [[concepts/terms/shimmy]] | シミー / shimmy | Capcom eSports BASE | [[concepts/terms/command-throw]], [[concepts/terms/whiff-punish]] |
| [[concepts/terms/stun]] | スタン / stun | Capcom eSports BASE | [[concepts/drive-system]], [[concepts/terms/burnout]], [[concepts/terms/corner]] |
| [[concepts/terms/super-art]] | Super Art / SA | Capcom Fighting Ground, SuperCombo glossary | [[concepts/frame-data]], [[concepts/terms/critical-art]], [[concepts/terms/cancel]] |
| [[concepts/terms/wall-bounce]] | wall bounce / 壁バウンド | Capcom Fighting Ground, SuperCombo glossary, official frame data | [[concepts/juggle-system]], [[concepts/terms/drive-impact]], [[concepts/terms/air-reset]] |
| [[concepts/terms/whiff-punish]] | 差し返し / whiff punish | Capcom eSports BASE | [[concepts/terms/shikomi]], [[concepts/terms/punish-counter]] |

## Entities

| Page | Summary | Type |
|---|---|---|
| [[entities/street-fighter-6]] | glossary、公式 CAPCOM eSports BASE 用語解説、36 term pages、公式 Fighting Ground Battle System、公式 frame-data sources、公式 Battle Change List、SuperCombo 30キャラ community frame-data 取得データ、公式 + SuperCombo 補助 output、raw layout の game context。 | other |
| [[entities/supercombo-wiki]] | glossary と 30キャラ分の SuperCombo frame-data raw 取得データ、公式補助 output の source である community wiki。 | other |
| [[entities/capcom]] | 公式 Street Fighter 6 eSports BASE 用語解説、Fighting Ground Battle System、frame-data sources、Battle Change List の publisher。 | company |
| [[entities/ryu]] | Ryu（リュウ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/luke]] | Luke（ルーク）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/jamie]] | Jamie（ジェイミー）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/chun-li]] | Chun-Li（春麗）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/guile]] | Guile（ガイル）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/kimberly]] | Kimberly（キンバリー）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/juri]] | Juri（ジュリ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/ken]] | Ken（ケン）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/blanka]] | Blanka（ブランカ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/dhalsim]] | Dhalsim（ダルシム）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/e-honda]] | E. Honda（エドモンド本田）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/dee-jay]] | Dee Jay（ディージェイ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/manon]] | Manon（マノン）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/marisa]] | Marisa（マリーザ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/jp]] | JP。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/zangief]] | Zangief（ザンギエフ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/lily]] | Lily（リリー）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/cammy]] | Cammy（キャミィ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/rashid]] | Rashid（ラシード）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/aki]] | A.K.I.。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/ed]] | Ed（エド）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/gouki-akuma]] | Gouki / Akuma（豪鬼）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/vega-m-bison]] | Vega / M. Bison（ベガ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/terry]] | Terry（テリー）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/mai]] | Mai（不知火舞）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/elena]] | Elena（エレナ）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/sagat]] | Sagat（サガット）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/c-viper]] | C. Viper（C.ヴァイパー）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/alex]] | Alex（アレックス）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |
| [[entities/ingrid]] | Ingrid（イングリッド）。公式 Classic / Modern frame-data outputs と SuperCombo community frame-data output がある character。 | character |

## Syntheses

| Page | Summary | Updated |
|---|---|---:|
| [[syntheses/frame-data-raw-layout]] | frame-data raw を最新ミラー固定パスに置き、manifest の `source_updated_at` / `captured_at_utc` / `source_revision` を分けて由来を追う方針。official 30キャラと SuperCombo 30キャラの raw entrypoint と data-family first output layout を整理する。 | 2026-06-09 |

## Questions

| Page | Question | Summary | Updated |
|---|---|---|---:|
| [[questions/jp-modern-vs-classic-frame-data-moves-and-inputs]] | JPのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | JP Classic / Modern の項目数、Classic専用項目、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/jp-crouching-light-p-standing-light-p-light-stribog-combo-theory]] | JPのしゃがみ弱P＞立ち弱P＞弱ストリボーグは、なぜ理論上つながる？ | `しゃがみ弱P`→`立ち弱P` は弱攻撃 chain、`立ち弱P`→`弱 ストリボーグ` は `C` 必殺技キャンセルとして説明する。 | 2026-06-08 |
| [[questions/jp-crouching-medium-p-drc-crouching-heavy-p-heavy-stribog-medium-torbalan-triglav-combo-theory]] | JPのしゃがみ中P＞キャンセルラッシュ＞しゃがみ強P＞強ストリボーグ＞中トルバラン＞トリグラフは、なぜ理論上つながる？ | キャンセルDRの最速攻撃可能9F、DR通常技+4F、強ストリボーグの limited juggle / wall bounce、Torbalan / Triglav の juggle limit から説明する。 | 2026-06-08 |
| [[questions/ryu-modern-vs-classic-frame-data-moves-and-inputs]] | Ryuのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Ryu Classic / Modern の項目数、技名差分、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/chun-li-modern-vs-classic-frame-data-moves-and-inputs]] | Chun-Liのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Chun-Li Classic / Modern の項目数、技名差分、入力表示、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/zangief-modern-vs-classic-frame-data-moves-and-inputs]] | Zangiefのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？ | Zangief Classic / Modern の項目数、技名差分、一回転/二回転入力、ダメージ差分を公式フレームデータから比較する。 | 2026-05-27 |
| [[questions/chun-li-standing-medium-p-frame-data]] | 春麗の立ち中Pは、発生・ヒット時・ガード時・キャンセル可否・ダメージはいくつですか？ | 春麗の立ち中P（頸穿刀）の発生、持続、硬直、有利、不利、Cキャンセル、ダメージを公式JSONから答える。 | 2026-06-08 |
| [[questions/chun-li-standing-medium-p-into-crouching-medium-p-link]] | 春麗の立ち中Pが通常ヒットしたあと、発生6Fのしゃがみ中Pは理論上つながりますか？ | 立ち中Pの通常ヒット+6Fとしゃがみ中Pの発生6Fから、最速リンクが理論上成立する理由を説明する。 | 2026-06-08 |

## Outputs

| Page | Type | Summary | Updated |
|---|---|---|---:|
| [[outputs/lint/2026-06-10-health-check]] | lint_report | wiki 全体の health check と follow-up。review status 同期、旧 raw path 履歴注記、term index/direct rows、question backlink 方針、web search で埋めるべき data gaps を記録。 | 2026-06-10 |
| [[outputs/reports/2026-05-30-official-frame-data-coverage]] | report | 30 character data slugs の公式 frame-data coverage table。row counts と review status を含む。 | 2026-05-30 |
| [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]] | report | SuperCombo JP の派生 output と Capcom 公式 JP Classic JSON の候補照合。 | 2026-05-31 |
| [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]] | report | Capcom 公式 JP Classic JSON を正として保持し、SuperCombo 補助列を付与した output。 | 2026-05-31 |
| [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]] | report | SuperCombo Ryu の派生 output と Capcom 公式 Ryu Classic JSON の照合。Denjin / hold-level review override と 6HK conditional variant link 反映済み。 | 2026-06-01 |
| [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] | report | Capcom 公式 Ryu Classic JSON を正として保持し、SuperCombo 補助列を付与した output。レビュー済み13行と conditional variant link を含む。 | 2026-06-01 |
| [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]] | report | SuperCombo Zangief の派生 output と Capcom 公式 Zangief Classic JSON の照合。360/720、hold、近距離/中距離/遠距離、CA variant override を含む。 | 2026-06-02 |
| [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] | report | Capcom 公式 Zangief Classic JSON を正として保持し、SuperCombo 補助列を付与した output。人間レビュー済み25行と SuperCombo-only taunt 4行を含む。 | 2026-06-02 |
| [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]] | report | SuperCombo Ingrid の派生 output と Capcom 公式 Ingrid Classic JSON の照合。Sun Crest stock level、OD Sun Shot 共有 row、SA1/SA2、Drive Rush override を含む。 | 2026-06-02 |
| [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] | report | Capcom 公式 Ingrid Classic JSON を正として保持し、SuperCombo 補助列を付与した output。人間レビュー済み26行、official-only 2行、SuperCombo-only 13行を含む。特殊隠しコマンド / Monoid 操作の 9 行は通常回答から分離する。 | 2026-06-02 |
| [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | report | SuperCombo frame-data 30キャラ分の raw capture / validation / official crosswalk / enriched output coverage。未レビュー補助行 1295 行、レビュー済み 69 行、SuperCombo-only 620 行、review queue 集計を含む。 | 2026-06-06 |
| `wiki/outputs/data/frame-data/supercombo/<character_slug>/` | json | SuperCombo 30キャラ分の派生 frames/character JSON、公式 Classic との候補照合。 | 2026-06-05 |
| `wiki/outputs/data/frame-data/official-supercombo-enriched/<character_slug>/` | json | 公式 Classic rows に SuperCombo `supercombo_*` 補助列を付与した data。既存レビュー済み 69 行を保持し、複数候補・再利用・基本 field conflict・比較不能 field・条件付き field は `enrichment_review_queues` で分離する。 | 2026-06-06 |
| `wiki/outputs/data/battle-change/official/` | json | Capcom 公式 Battle Change List 20 version 分の派生 output。`changes.json` は policy / common / fighter change rows 1820 行を保持し、`text_html` は公式 HTML fragment を保持する。 | 2026-06-07 |
| `wiki/outputs/data/frame-data/supercombo/jp/` | json | SuperCombo JP の派生 frames/character JSON、公式 Classic との候補照合。 | 2026-05-31 |
| `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/` | json | 公式 JP Classic rows に SuperCombo `supercombo_*` 補助列を付与した data と SuperCombo-only row。 | 2026-05-31 |
| `wiki/outputs/data/frame-data/supercombo/ryu/` | json | SuperCombo Ryu の派生 frames/character JSON、公式 Classic との候補照合。 | 2026-05-31 |
| `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/` | json | 公式 Ryu Classic rows に SuperCombo `supercombo_*` 補助列を付与した data、レビュー済み行、conditional variant link。 | 2026-06-01 |
| `wiki/outputs/data/frame-data/supercombo/zangief/` | json | SuperCombo Zangief の派生 frames/character JSON、公式 Classic との候補照合。 | 2026-06-02 |
| `wiki/outputs/data/frame-data/official-supercombo-enriched/zangief/` | json | 公式 Zangief Classic rows に SuperCombo `supercombo_*` 補助列を付与した data、`enriched_reviewed` 行、SuperCombo-only taunt row。 | 2026-06-02 |
| `wiki/outputs/data/frame-data/supercombo/ingrid/` | json | SuperCombo Ingrid の派生 frames/character JSON、公式 Classic との候補照合。 | 2026-06-02 |
| `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/` | json | 公式 Ingrid Classic rows に SuperCombo `supercombo_*` 補助列を付与した data、`enriched_reviewed` 26行、SuperCombo-only 13行。特殊隠しコマンド / Monoid 操作の 9 行は通常回答から分離する。 | 2026-06-02 |
| `wiki/outputs/data/frame-data/official/ryu/` | json | Ryu（リュウ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-27 |
| `wiki/outputs/data/frame-data/official/luke/` | json | Luke（ルーク） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/jamie/` | json | Jamie（ジェイミー） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/chunli/` | json | Chun-Li（春麗） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-27 |
| `wiki/outputs/data/frame-data/official/guile/` | json | Guile（ガイル） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/kimberly/` | json | Kimberly（キンバリー） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/juri/` | json | Juri（ジュリ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/ken/` | json | Ken（ケン） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/blanka/` | json | Blanka（ブランカ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/dhalsim/` | json | Dhalsim（ダルシム） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/ehonda/` | json | E. Honda（エドモンド本田） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/deejay/` | json | Dee Jay（ディージェイ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/manon/` | json | Manon（マノン） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/marisa/` | json | Marisa（マリーザ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/jp/` | json | JP の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-26 |
| `wiki/outputs/data/frame-data/official/zangief/` | json | Zangief（ザンギエフ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-27 |
| `wiki/outputs/data/frame-data/official/lily/` | json | Lily（リリー） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/cammy/` | json | Cammy（キャミィ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/rashid/` | json | Rashid（ラシード） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/aki/` | json | A.K.I. の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/ed/` | json | Ed（エド） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/gouki_akuma/` | json | Gouki / Akuma（豪鬼） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/vega_mbison/` | json | Vega / M. Bison（ベガ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/terry/` | json | Terry（テリー） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/mai/` | json | Mai（不知火舞） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/elena/` | json | Elena（エレナ） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/sagat/` | json | Sagat（サガット） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/cviper/` | json | C. Viper（C.ヴァイパー） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/alex/` | json | Alex（アレックス） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |
| `wiki/outputs/data/frame-data/official/ingrid/` | json | Ingrid（イングリッド） の Classic / Modern JSON（field_meanings 埋め込み）。 | 2026-05-30 |

## Reviews

| Page | Review type | Summary | Status |
|---|---|---|---|
| [[reviews/2026-05-26-official-jp-frame-data-capture-review]] | capture_validation | JP 公式 frame-data 取得データの人間レビュー。 | accepted |
| [[reviews/2026-05-27-official-ryu-frame-data-capture-review]] | capture_validation | Ryu 公式 frame-data 取得データの人間レビュー。 | accepted |
| [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]] | capture_validation | Chun-Li 公式 frame-data 取得データの人間レビュー。 | accepted |
| [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | capture_validation | Zangief 公式 frame-data 取得データの人間レビュー。 | accepted |
| [[reviews/2026-05-27-health-check]] | health_check | 初期 official captures と Classic / Modern comparison pages 後の health check。 | open |
| [[reviews/2026-05-30-official-frame-data-roster-capture-review]] | capture_validation | 2026-05-30 batch の 26 character 取得データの自動検証レビュー。 | open |
| [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]] | capture_validation | SuperCombo JP frame-data raw 取得データの自動検証レビュー。 | open |
| [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]] | capture_validation | SuperCombo Ryu frame-data raw 取得データの自動検証レビュー。 | open |
| [[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]] | capture_validation | SuperCombo Zangief frame-data raw 取得データの自動検証レビュー。 | open |
| [[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]] | capture_validation | SuperCombo Ingrid frame-data raw 取得データの自動検証レビュー。補助データ26行 accepted、imageinfo missing 156 件と SuperCombo-only 9行の扱いが残る。 | open |
| [[reviews/2026-06-02-supercombo-ingrid-supercombo-only-prereview]] | prereview | SuperCombo Ingrid の公式 row に直接照合しない 9 行を外部 web evidence も使って事前レビュー。特殊隠しコマンド / Monoid 操作として通常回答から分離し、accept ではなく pending。 | open |
| [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | capture_validation | SuperCombo frame-data 30キャラ分の batch capture review。raw capture は 30/30 passed、未レビュー補助行 1295 行と SuperCombo-only 620 行が残り、review queue で理由を分離している。 | open |
| [[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]] | prereview | SuperCombo `field_conflict` 単独 11 行の事前レビュー。Jamie 酔いLv damage、Terry jMP/jMK 入れ替わり疑い、通常 source conflict を分離し、追加 accept はしていない。 | open |
| [[reviews/2026-06-07-official-battle-change-capture-review]] | capture_validation | Capcom 公式 Battle Change List 20 update version capture の自動検証レビュー。raw HTML / Next.js data JSON は artifact hash と payload 一致を通過し、派生 change rows は 1820 行。 | open |
| [[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]] | capture_validation | SuperCombo glossary を `raw/web-pages/` 試験 layout で取得。MediaWiki wikitext を canonical raw 取得物、HTML / rendered DOM を表示構造の証拠として保存した。 | open |
| [[reviews/2026-06-10-capcom-fightingground-battle-system-capture-review]] | capture_validation | Capcom 公式 Fighting Ground ページから Battle System 範囲だけを scoped raw capture。validation は passed、full HTML / full Next.js data / page chunk は保存しない。 | open |
| [[reviews/2026-06-10-capcom-esports-base-terms-capture-review]] | capture_validation | Capcom 公式 CAPCOM eSports BASE から実況ワード解説 23 語だけを scoped raw capture。validation は passed、full page HTML / JS は保存しない。 | open |
