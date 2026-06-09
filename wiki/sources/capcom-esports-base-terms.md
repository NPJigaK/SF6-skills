---
type: source
source_type: official_scoped_web_page_capture
title: "CAPCOM eSports BASE 用語解説"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json"
original_url: "https://sf.esports.capcom.com/base/"
created: 2026-06-10
updated: 2026-06-10
source_last_modified_at: "2025-11-11T06:17:24Z"
captured_at_utc: "2026-06-09T17:48:14Z"
status: active
confidence: high
tags:
  - sf6
  - official
  - glossary
  - capcom-esports
  - cpt
  - sfl
  - web-page-capture
  - scoped-capture
aliases:
  - "CAPCOM eSports BASE"
  - "CPT/SFLがもっと楽しくなる！ CAPCOM eSports BASE"
  - "Capcom esports base terms"
  - "スト6 観戦用語"
related_concepts:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
---

# ソース: CAPCOM eSports BASE 用語解説

## 1行要約

Capcom 公式 `CAPCOM eSports BASE` から、CPT / SFL 観戦で使われる Street Fighter 6 用語 23 語の解説セクションだけを scoped raw として保存した source page。

## 重要ポイント

1. Raw entrypoint は `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json`。
2. 保存対象は `実況ワード解説` の word card HTML、用語 JSON、クリック modal DOM、各用語の thumbnail と modal mp4。
3. 除外対象は top page hero、news、word section 外の movie list、consult / coaching content、logos、page chrome、unrelated images。full page HTML と full page JavaScript は保存せず、response metadata と hash を `source-provenance.json` に残している。
4. Canonical raw は `source/word-section.raw.html`、`source/modal-open-close.raw.js`、`api/terms.raw.json`、`rendered/word-section.dom.json`、`rendered/modals/`。
5. `metadata.json` は 23 語を重要度 3 段階に分ける。各用語は [[concepts/terms/index]] 配下の term page に昇格し、将来の source claims を同じ用語へ集約する。
6. `validation.json` は `passed` で、23 modal DOM、47 downloaded assets、2 screenshot を確認している。
7. HTTP `Last-Modified` は page HTML と page JavaScript のどちらも `2025-11-11T06:17:24Z`。raw 取得時刻は `2026-06-09T17:48:14Z`。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| この raw capture は `CAPCOM eSports BASE` 全体ではなく、`実況ワード解説` セクションだけを保存する。 | `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json` | high | `scope_policy.id` は `capcom_esports_base_words_only`。 |
| 23 語は重要度 3 段階に分けられる。重要度 3 は [[concepts/terms/chip-damage|削り]]、[[concepts/terms/stun|スタン]]、[[concepts/terms/anti-air|対空]]、[[concepts/terms/corner|画面端]]、[[concepts/terms/cross-up|めくり]]、[[concepts/terms/command-throw|コマ投げ]]、[[concepts/terms/raw-drive-rush|生ラッシュ]]、[[concepts/terms/drive-impact-counter|インパクト返し]]、[[concepts/terms/perfect-parry|ジャストパリィ]]。 | `raw/web-pages/sf.esports.capcom.com/base-terms/metadata.json`; `api/terms.raw.json` | high | `groups[]` と `terms[]` の対応で確認できる。 |
| [[concepts/terms/chip-damage|削り]] は通常ガード時の Drive Gauge 減少と、Burnout 中の必殺技ガードによる体力削り / 削り K.O. を説明する。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-00`。 |
| [[concepts/terms/stun|スタン]] は Burnout 中の相手に Drive Impact をガードさせ、画面端に到達した場合に起きる状態として説明される。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-01`。 |
| [[concepts/terms/raw-drive-rush|生ラッシュ]] は Drive Parry から出す Drive Rush、`キャンセルラッシュ` は通常技キャンセルから出す Drive Rush と説明され、D gauge cost はそれぞれ 1 / 3 とされる。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-06`。 |
| [[concepts/terms/perfect-parry|ジャストパリィ]] は 2 frame の猶予、成功時の slow 演出、反撃に向けた有利時間、後続 combo への 50% damage scaling を伴うと説明される。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-08`。 |
| [[concepts/terms/frame-advantage|有利フレーム]] は 1 frame = 1/60 秒、攻撃を hit / guard させた後に自分が先に動ける時間として説明される。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-13`。 |
| [[concepts/terms/punish-counter|パニッシュカウンター]] は戻り際への hit、通常 hit より damage 1.2 倍、counter +2 / punish counter +4 の advantage 増加、Drive Gauge 減少を含む説明として保存されている。 | `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json` | high | `word-10`。 |

## 用語一覧

| 重要度 | 用語 | 読み | 要約 |
|---:|---|---|---|
| 3 | [[concepts/terms/chip-damage|削り]] | けずり | Guard による Drive Gauge 減少と Burnout 中の体力削り / 削り K.O.。 |
| 3 | [[concepts/terms/stun|スタン]] | すたん | Burnout 中に Drive Impact をガードして画面端へ到達した時の無防備状態。 |
| 3 | [[concepts/terms/anti-air|対空]] | たいくう | Jump など空中の相手を迎撃する攻撃。 |
| 3 | [[concepts/terms/corner|画面端]] | がめんはし | 逃げ場がなく、Drive Impact、壁やられ、stun、line control が絡む危険な位置。 |
| 3 | [[concepts/terms/cross-up|めくり]] | めくり | 相手の背中側を狙い、guard direction を惑わせる jump attack 系の崩し。 |
| 3 | [[concepts/terms/command-throw|コマ投げ]] | こまなげ | 投げ抜けできない command throw / special throw。 |
| 3 | [[concepts/terms/raw-drive-rush|生ラッシュ]] | なまらっしゅ | Drive Parry から出す Drive Rush。通常技 cancel 版との cost 差も説明される。 |
| 3 | [[concepts/terms/drive-impact-counter|インパクト返し]] | いんぱくとがえし | Drive Impact に Drive Impact を打ち返す対策。 |
| 3 | [[concepts/terms/perfect-parry|ジャストパリィ]] | じゃすとぱりぃ | 2 frame window の parry timing。成功後の反撃機会と damage scaling を伴う。 |
| 2 | [[concepts/terms/oki|起き攻め]] | おきぜめ | 相手の起き上がりに攻めを重ね、選択肢を迫る状況。 |
| 2 | [[concepts/terms/punish-counter|パニッシュカウンター]] | ぱにっしゅかうんたー | 技の戻り際への counter。damage、advantage、Drive Gauge への影響を説明する。 |
| 2 | [[concepts/terms/whiff-punish|差し返し]] | さしかえし | 空振りした相手の技の隙に攻撃を当てる地上戦の対抗策。 |
| 2 | [[concepts/terms/invincible-move|無敵技]] | むてきわざ | 無敵時間を持つ切り返し技。属性別無敵にも触れる。 |
| 2 | [[concepts/terms/frame-advantage|有利フレーム]] | ゆうりふれーむ | 自分が相手より先に動ける frame advantage。 |
| 2 | [[concepts/terms/meaty|重ね]] | かさね | 起き上がりに合わせて投げや打撃を置く攻め。 |
| 2 | [[concepts/terms/lethal|リーサル]] | りーさる | 一度の機会で相手を倒し切れる状況判断。 |
| 1 | [[concepts/terms/shikomi|仕込み]] | しこみ | 通常技の motion 中に次行動を入力し、hit 時だけ出す technique。 |
| 1 | [[concepts/terms/guaranteed-punish|確定反撃]] | かくていはんげき | Guard 後の不利 frame に確実に入る反撃。 |
| 1 | [[concepts/terms/hit-confirm|ヒット確認]] | ひっとかくにん | Hit を確認して、hit 時だけ cancel special などへ繋ぐ technique。 |
| 1 | [[concepts/terms/shimmy|シミー]] | しみー | Throw tech を誘い、その whiff に punish counter を狙う崩し。 |
| 1 | [[concepts/terms/setplay|セットプレイ]] | せっとぷれい | 行動不能時間を利用した pattern 化された起き攻め。frame kill にも触れる。 |
| 1 | [[concepts/terms/abare|暴れ]] | あばれ | 連携の隙間に速い技や無敵技で割り込む防御側の行動。 |
| 1 | [[concepts/terms/scaling-reset|補正切り]] | ほせいぎり | Combo scaling を一度切って reset する狙い。double up とも呼ばれる。 |

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/terms/index]]

## 関連エンティティ

- [[entities/capcom]]
- [[entities/street-fighter-6]]

## 既存 wiki との矛盾または更新

- [[sources/supercombo-street-fighter-6-glossary]] は community source だが、この source は Capcom 公式の観戦者向け日本語用語 source として扱える。
- [[sources/capcom-official-fightingground-battle-system]] は Battle System の公式説明、こちらは CPT / SFL 観戦で頻出する用語の公式説明として補完関係にある。
- この raw は scoped capture であり、`CAPCOM eSports BASE` ページ全体、news、movie list、consult content の根拠には使わない。

## 未解決の質問

- 今後追加する source claim を term page と source page のどちらにどの粒度で二重記録するか。
- `source_last_modified_at` を source freshness として扱うか、HTTP artifact metadata としてのみ扱うか。
- 用語の公式説明と SuperCombo community glossary の対応表を作るべきか。

## ソースメモ

- Raw manifest: `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json`
- Terms JSON: `raw/web-pages/sf.esports.capcom.com/base-terms/api/terms.raw.json`
- Raw word section HTML: `raw/web-pages/sf.esports.capcom.com/base-terms/source/word-section.raw.html`
- Rendered word section DOM: `raw/web-pages/sf.esports.capcom.com/base-terms/rendered/word-section.dom.json`
- Modal DOM: `raw/web-pages/sf.esports.capcom.com/base-terms/rendered/modals/`
- Asset manifest: `raw/web-pages/sf.esports.capcom.com/base-terms/assets/manifest.json`
- Source provenance: `raw/web-pages/sf.esports.capcom.com/base-terms/source-provenance.json`
- Capture review: [[reviews/2026-06-10-capcom-esports-base-terms-capture-review]]
