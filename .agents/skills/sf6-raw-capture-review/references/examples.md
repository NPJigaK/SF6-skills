# SF6 Raw Capture Review Examples

raw package を ingest してよいか判断する時に読む。この reference を source fact の変更に使わない。

## Ingest Readiness Examples

| Situation | Classification | Action |
|---|---|---|
| manifest が存在し、validation が passed、scope と artifact が一致し、source freshness が記録されている | `ready-for-ingest` | `$sf6-source-ingest` を推奨する。caveat は review note に残す。 |
| validation は passed だが、source authority や scoped exclusion が claim の使い方に影響する | `needs-human-review` | ユーザーが caveat を受け入れるまで automatic ingest しない。 |
| manifest が missing artifact や stale validation output を指している | `needs-recapture` | この skill では raw artifact を編集しない。`$sf6-url-source-capture` または既存 capture tool を推奨する。 |
| validation result が failed、または必須 validation artifact がない | `validation-failed` | failure を記録し、ingest 前に止める。 |
| raw path、URL family、storage policy が repo convention に合うか判断できない | `scope-unclear` | source-family decision を依頼するか、review note を作る。 |
| raw boundary や copyright / media constraint のため source を安全に保存・利用できない | `do-not-ingest` | blocking reason を説明し、unsupported source fact を保持しない。 |

## Review-Status Correction Examples

- manifest `raw_review_status` は、既存 policy が更新を許可し、evidence が直接支える場合だけ変更する。
- automatic validation だけで `human_reviewed_accepted` にしない。
- 既存の human-accepted review を、明示指示なしに downgrade / erase しない。conflict がある場合は review note に残す。
- review note status と manifest review status は、schema が異なる場合は分けて扱う。

## Scope Checks

- scoped official page では、どの section を取得し、どの section を除外したか review note に書かれているか確認する。
- SuperCombo page では、validation が passed でも community authority を見える形で残す。
- screenshot-heavy package では、screenshot が表示証拠であり、claim 用の source text / structured data が別にあるか確認する。
- raw-derived artifact では、生成 tool と validation artifact が明記されているか確認する。

## Final Report Examples

passed package の例:

```text
Status: ready-for-ingest
Raw package: raw/web-pages/example/manifest.json
Validation: passed via validation.json
Review note: wiki/reviews/YYYY-MM-DD-example-capture-review.md
Next: use $sf6-source-ingest
```

incomplete package の例:

```text
Status: needs-recapture
Raw package: raw/web-pages/example/manifest.json
Missing evidence: validation.json references an artifact that is absent
Next: use $sf6-url-source-capture or the existing capture tool
```
