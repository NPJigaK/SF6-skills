# SF6 URL Source Capture Examples

URL 分類や capture mode が曖昧な時に読む。`raw/` 境界と storage policy の正本は `AGENTS.md`。

## Mode Selection

| ユーザーの意図 | Mode | Action |
|---|---|---|
| 「このURLを入れるべきか見て」 | `read-only plan` | file は書かない。source authority、既存 coverage、wiki value、copyright / media risk を確認し、capture する価値がある場合だけ target path / policy を提案する。 |
| 「raw化して。まだwiki化しないで」 | `capture-only` | source-like artifact を取得し、manifest / metadata / validation と capture review を更新して止める。`$sf6-source-ingest` へ進まない。 |
| 「raw化して、可能ならwiki化まで」 | `capture-then-ingest` | まず capture する。validation と review note が `ready-for-ingest` の場合だけ `$sf6-source-ingest` へ進む。 |
| 「前に取ったURLを取り直して」 | `recapture` | 既存 manifest / review を先に読む。storage policy が更新を許す場合は package path を維持し、source freshness と変更 artifact を記録する。 |

## Source Classification Examples

| URL type | Typical classification | Preferred action |
|---|---|---|
| `streetfighter.com/.../character/<slug>/frame` | Capcom official frame-data | `tools.frame_data.official.capture` を使う。ad hoc な web-page package を作らない。 |
| `streetfighter.com/6/buckler/.../battle_change` | Capcom official Battle Change | `tools.battle_change.official.capture` を使い、validation 後に ingest 可否を判断する。 |
| `wiki.supercombo.gg/w/Street_Fighter_6/...` system page | SuperCombo system page | 対応済みなら `tools.web_pages.supercombo_page` を使う。community authority を見える形で残す。 |
| SuperCombo frame-data page | SuperCombo frame-data | `tools.frame_data.supercombo.capture` を使う。system-page layout と混ぜない。 |
| YouTube or video page | video page | full video は標準では download しない。repo policy で明示許可された場合だけ URL metadata や scoped observation review を扱う。 |
| External article or guide | article / external community page | まず `read-only plan` を優先する。repo policy が明示許可しない限り、copyrighted article の全文保存は避ける。 |

## Storage And Raw Boundary Examples

- `raw/` に置いてよいもの: HTML、wikitext、DOM JSON、API response、screenshot、metadata、manifest、validation、hash。
- `raw/` に置かないもの: LLM summary、translation、normalized replacement、editorial explanation、inferred values。
- scoped capture の場合は、manifest / review に scope 名と excluded section を書く。full-page coverage と誤読させない。
- large media や full transcript が必要に見える場合は、明示 policy と user approval がない限り `needs-human-review` で止める。

## Capture Review Examples

`ready-for-ingest`: validation が passed、scope が clear、残る caveat が wiki compile を妨げない場合。

`needs-human-review`: source は有用だが、authority、copyright / media handling、scope、interpretation を maintainer が見る必要がある場合。

`needs-recapture`: expected artifact が欠けている、hash / validation が合わない、package が stale / incomplete の場合。

`scope-unclear`: URL、source family、target raw path を十分な確度で分類できない場合。

`do-not-ingest`: source trust、copyright、unsupported source type、raw boundary の問題で wiki compile すべきでない場合。
