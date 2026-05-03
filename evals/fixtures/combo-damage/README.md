# Combo Damage Oracle Fixtures

このdirectoryは、コンボ表記と動画・検証runで観測したdamage labelを保持するeval fixture surfaceです。

ここにあるartifactは、damage-hidden calculation evalや将来のcombo damage calculator検証に使うためのoracle候補です。`knowledge/curated/` ではなく、public answer用のcurrent-system authorityでもありません。

## Boundary

- `observed_damage` はeval oracle labelです。
- `observed_damage` はaccepted current-system factではありません。
- Fixtureはgenerated referencesへ流してはいけません。
- Fixtureはpublic answer sourceとして直接使ってはいけません。
- Raw video、frames、screenshots、contact sheets、browser cache、full transcriptはrepoに保存しません。
- Source metadata、video observations、review notesを参照し、観測条件と不確実性を追えるようにします。

## Enabled And Disabled Cases

`enabled_for_damage_hidden_eval: true` のcaseだけが、damage-hidden calculation evalの入力候補です。

Enabled caseは少なくとも次を満たす必要があります。

- combo notationが明確。
- observed damageが明確。
- route-to-damage対応が明確。
- `notation_confidence: high`。
- `damage_confidence: high`。
- `review_status: needs_review` または、将来定義されるfixture-specific accepted state。

`enabled_for_damage_hidden_eval: false` のcaseは、観測済みでもまだ計算evalには使いません。

Disabled caseの例:

- overlayが複数route候補を示している。
- route-to-damage対応が曖昧。
- notation normalizationが未確定。
- damage labelは見えるが、該当routeの条件が不明。

## Notation

Fixture may include both human-facing Japanese notation and a provisional normalized notation.

Examples:

- `combo_notation_jp`
- `combo_notation_normalized`

The normalized notation is provisional until a combo notation contract is defined. Do not treat the current strings as a stable machine-readable contract.

## Relationship To Current Facts

Combo damage fixtures are useful for testing whether a future calculator can reproduce observed results. They do not make the observed values authoritative.

Exact current system mechanics still require the workflow in `workflows/system-mechanics-fact-workflow.md`.

Move-specific current values still come from `data/exports/`, `data/roster/`, and generated frame-current runtime assets when packaged.

## Expected Follow-ups

- Add a validator for `evals/fixtures/combo-damage/*.yaml`.
- Expand fixture coverage with high-confidence cases across different route types.
- Define a combo notation contract.
- Define combo damage calculation input/output contracts.
- Add damage-hidden calculation evals only after fixture and notation boundaries are reviewed.
