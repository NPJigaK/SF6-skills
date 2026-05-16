# System Mechanics Fact Workflow

このworkflowは、frame-current move factだけでは扱い切れないsystem mechanics current factsをreviewで保持し、誤って `knowledge/curated/` やgenerated knowledge referencesへ入れないための手順です。

## 目的

SF6には、moveごとのcurrent factとして扱える値と、system mechanicsとして別に確認が必要な値があります。

`knowledge/curated/` は安定概念を説明できますが、exact current system valuesの正本ではありません。system mechanicsの具体値や計算式を扱う時は、このworkflowでreviewに保持し、accepted useの前にcurrent authority pathを決めます。

## Frame-current fact との違い

Frame-current factsは、packaged frame-current runtime assetsで解決できるmove-specific current valuesです。

例:

- moveごとのdamage。
- moveごとのstartup、active、recovery、advantageなどのcurrent frame fields。
- moveに紐づくpublished raw fieldsに含まれるstarter scalingやcombo scaling。
- roster membershipやpackaged character availability。

これらは `data/exports/` と `data/roster/` をcanonical authorityとし、derived `skills/sf6-agent/assets/frame-current/` をruntime answer surfaceとして使います。

System-mechanics current factsは、単一のmove rowだけでは解決しにくいpatch-sensitiveなsystem valuesや計算規則です。

例:

- コンボ全体の最終ダメージ計算。
- global scaling tableやroute-level scaling rule。
- system actionによる補正。
- minimum guaranteeやSA minimum damage behavior。
- character-specific、move-specific、control-scheme-specific exceptionのうち、packaged move fieldだけで説明できないもの。
- video/article/source observationから出た、現行patchで再検証が必要なsystem behavior。

## 現在の置き場所

Accepted system-mechanics current fact用のdedicated data surfaceは、まだありません。

そのため、system-mechanics exact valuesや計算式は、accepted useの前に次のどちらかに分けます。

1. Packaged frame-current runtime assetsで解決できるmove-specific fieldなら、frame-current factとして扱う。
2. 解決できない場合は `knowledge/review/current-fact-candidates/` にreview-only candidateとして保持する。

`knowledge/review/current-fact-candidates/` は、final public answer evidenceではありません。ここにあるcandidateはgenerated knowledge referencesへ流してはいけません。

## Review flow

1. Claimをstable concept、move-specific current fact、system-mechanics current factに分解する。
2. Move-specific fieldで答えられるか確認する。
3. Packaged frame-current runtime assetsにある値なら、current-fact answer pathへ渡す。
4. Packaged runtime assetsで解決できないsystem valueなら、`knowledge/review/current-fact-candidates/` に保持する。
5. Candidateには、source refs、verification state、confidence、volatility、patch sensitivity、review status、review afterを記録する。
6. Accepted curated knowledgeへは、安定概念だけを入れる。
7. Exact system value、計算式、例外、current patch behaviorは、current authority pathが決まるまでacceptedにしない。

## Candidate artifact guidance

System-mechanics candidateは、普通のcurated pageではなくreview-only current-fact candidateとして書きます。

Minimum fields:

- `id`
- `title`
- `claim_kind`
- `source_kind`
- `source_role`
- `evidence_basis`
- `verification_state`
- `confidence`
- `volatility`
- `patch_sensitivity`
- `review_status`
- `authority_status`
- `authority_role`
- `public_answer_allowed`
- `generated_reference_allowed`
- `accepted_current_fact_authority`
- `source_refs`
- `review_after`

Required authority metadata values:

```yaml
authority_status: review_only
authority_role: review_only_current_fact_candidate
public_answer_allowed: false
generated_reference_allowed: false
accepted_current_fact_authority: false
```

These values are machine-readable guardrails. They do not verify, accept,
promote, or publish current facts. Accepted use requires a separate current-fact
authority path; it is not created by flipping these fields.

Recommended boundary text:

- `not final public answer evidence`
- `must not feed generated knowledge references`
- `not accepted curated knowledge`
- `resolved into the current-fact data surfaces or kept on hold`

Use `review_status: needs_review` until the repo has a clear accepted current-fact authority path for that system value.

## What not to put in curated knowledge

Do not accept these into `knowledge/curated/` as exact current facts by default:

- exact scaling percentages
- minimum guarantee values
- route-level final damage formulas
- current-patch system action modifiers
- character-specific or move-specific exceptions that are not already represented as packaged frame-current fields
- values inferred only from article/video observations

Curated pages may explain the stable concept and point to the relevant current-fact surface. They must not duplicate exact current system values.

## Adapter answer behavior

When `sf6-agent` is asked for a system-mechanics value:

1. If the question asks for a stable concept, answer from generated concept references and state the boundary.
2. If it asks for a move-specific exact value that exists in packaged frame-current runtime assets, answer from the packaged runtime assets.
3. If it asks for a route-level formula, minimum guarantee, system modifier, or exception that is not packaged as an exact current value, use `unresolved / hold`.
4. Do not infer exact system values from `knowledge/curated/`, generated concept references, article claims, video observations, or review candidates.

For combo scaling, this means:

- Explain what combo scaling is from `knowledge/curated/mechanics/combo-scaling.md`.
- Use frame-current runtime assets for packaged move-specific damage and scaling fields when available.
- Hold route-level final damage formulas, minimum guarantee values, and exception rules unless a future accepted system-mechanics authority path exists.

## Calculation executor boundary

Calculation tools, math skills, scripts, and agents may help run arithmetic only
as executors. They do not define SF6 input authority, formula authority,
rounding policy, current facts, or system mechanics.

Before a calculation output can support a public answer, all non-hypothetical
inputs must cite accepted authority refs, formula and rounding policy must be
reviewed, and the output must be captured as an auditable trace. If any input,
formula, rounding rule, route mapping, timing assumption, or authority path is
missing, use `unresolved / hold` instead of letting the executor guess.

See `contracts/calculation-executor-trace.md`.

## Future contract decision

A dedicated system-mechanics current-fact contract or data surface is likely needed before these facts can be accepted as runtime authority.

Possible future surfaces:

- `contracts/system-mechanics-fact.schema.json`
- `data/system-mechanics/`
- a validator for `knowledge/review/current-fact-candidates/` system-mechanics artifacts
- a generated runtime surface distinct from generated concept references

Do not create those surfaces inside an unrelated curation or ingest PR. Add them only after an architecture decision defines authority, validation, and distribution behavior.
