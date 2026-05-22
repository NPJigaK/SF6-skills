# Current Fact Exports

`data/exports/` は、公開済みの exact current-fact export surface です。

この directory は通常回答で使う move-specific current facts の authority seed
です。clean-slate cleanup 後、runtime が直接読む tracked surface は
`official_raw.json` です。

## Authority Boundary

- `official_raw.json` は現在の runtime current-fact lookup が読む公式 raw
  frame-data export の公開面です。
- `snapshot_manifest.json` は character ごとの legacy published export
  provenance です。
- `data/exports/_index/manual-review-debt.json` は legacy manual-review debt
  observability surface です。

削除済みの CSV、derived metric、manual-review、SuperCombo enrichment
sidecar は normal public answer authority ではありません。通常回答や runtime
current-fact lookup に混ぜるには、後続の reviewed workflow と deterministic
schema/parser/export を通す必要があります。

## Layout

Character ごとの directory は次の形を持ちます。

```text
data/exports/<character_slug>/
  official_raw.json
  snapshot_manifest.json
```

`snapshot_manifest.json` は legacy provenance として残しています。現在の
clean-slate runtime authority は `official_raw.json` です。

## Manual-Review Debt Index

`data/exports/_index/manual-review-debt.json` は、旧 export workflow の横断
index です。

この index は、character / dataset ごとに次を見える化します。

- `publication_state`
- `published_record_count`
- manifest 上の `withheld_review_count`
- actual manual-review sidecar row count
- reason-code counts
- `publish_eligible` / `confirmation_status` counts

この index は observability surface です。normal public answer authority では
ありません。clean-slate cleanup 後は再生成 workflow を持たない legacy
reference であり、削除または移行は別 ExecPlan で判断します。

## Dataset Semantics

Current retained dataset key is:

- `official_raw`

Legacy `snapshot_manifest.json` entries may still mention retired datasets.
Each retained or legacy manifest entry can record:

- `publication_state`
- `published_run_id`
- `published_snapshot_ids`
- `published_record_count`
- `withheld_review_count`
- `registry_version` / `registry_sha256`
- `binding_policy_version` / `binding_policy_sha256`
- `content_hash`

Current runtime must not treat retired sidecar datasets as available authority.

## Non-Authority Surfaces

The following are not normal public answer authority:

- `data/raw/`
- `data/normalized/`
- `*_manual_review.*`
- `derived_metrics.*`
- `supercombo_enrichment.*`
- run-local scraper state
- browser/cache/log output
- Hermes memory, sessions, local skills, Curator output, checkpoints, or raw transcripts

Exact current facts must not be inferred from those surfaces alone.
See `docs/PLAN.md` for the current architecture boundary that keeps these
inputs and observability files out of normal public answer authority.

## Validation

Run current clean-slate validation:

```bash
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
```
