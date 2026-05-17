---
title: Repository Surface Registry Policy
status: accepted
last_reviewed: 2026-05-17
tracking_issue: "#238"
---

# Repository Surface Registry Policy

この文書は、`data/repository-surfaces.json` を maintainer がどう読むかを定義する。

`data/repository-surfaces.json` は `repository-surfaces/v1` の registry であり、
repo 内の主要 surface を `surface_role`、`path_state`、生成元、配布状態、通常回答
authority などで索引する。これは `AGENTS.md`、ADR、workflow、contract、validator を
置き換える正本ではない。既存の reviewed boundary を参照しやすくするための
machine-readable index である。

## 使い方

maintainer は、path の責務や validation lane を判断するときに次を見る。

1. `AGENTS.md` と関連 ADR / workflow を読む。
2. `data/repository-surfaces.json` で該当 path の surface ID と role を確認する。
3. `validation_expectation` と validation lane を選ぶ。
4. 変更後に該当 validator を実行する。

registry の claim は、それだけで現在の file state の証明にはならない。tracked file
の有無は `git ls-files`、変更状態は `git status`、境界違反は validator で確認する。

## 主要フィールド

| Field | 意味 |
|---|---|
| `id` | surface を参照するための安定 ID。issue、PR、docs では path だけでなく ID も使う。 |
| `path_globs` | surface に属する path pattern。validator は tracked file との整合を確認する。 |
| `path_state` | `tracked_present`、`generated_untracked`、`documented_absent` のどれか。 |
| `surface_role` | `canonical`、`derived`、`deferred_legacy`、`repo_local_support`、`historical`、`non_canonical` のどれか。 |
| `source_of_truth` | surface の根拠になる source。generated surface は `self` を使わない。 |
| `generated` | 生成物かどうか。`true` の surface は `generator` と `source_paths` を持つ。 |
| `allowed_to_edit_directly` | maintainer が手で編集してよい surface かどうか。 |
| `public_distribution_status` | public distribution との関係。deferred public adapter は `deferred` を使う。 |
| `normal_public_answer_authority` | 通常回答の根拠として使えるかどうか。 |
| `validation_expectation` | 期待される validator / boundary check。 |

## Surface Role

| Role | 読み方 | 変更時の基本姿勢 |
|---|---|---|
| `canonical` | repo 内の正本。例: `knowledge/`、`data/exports/`、`contracts/`、`workflows/`。 | 直接編集できるかは `allowed_to_edit_directly` と workflow に従う。 |
| `derived` | generator と source paths から作られる生成物。 | source または generator を直し、必要な lane で再生成する。手で正本化しない。 |
| `deferred_legacy` | 既存 public distribution / adapter 由来だが、現在の active product focus ではない surface。 | 新機能を足さない。残す、移す、消す判断は scoped ADR / issue で行う。 |
| `repo_local_support` | maintainer workflow、validator、package、Hermes pack など repo-local 運用支援。 | public answer skill behavior と混ぜない。procedure authority は canonical workflow へ寄せる。 |
| `historical` | smoke report や過去実行証跡。 | execution evidence として扱い、 gameplay authority や current fact authority にしない。 |
| `non_canonical` | raw snapshot、normalized intermediate、manual-review sidecar など通常回答の正本ではないもの。 | normal public answer authority にしない。必要なら review / retention policy を明示する。 |

## Validation Lane との対応

`tests/validation/run-all.ps1` は次の lane を持つ。

| Lane | 使うとき | 関係する registry role / surface |
|---|---|---|
| `read-only` | docs、contracts、workflows、registry、fixture、境界 marker など、生成物を作らずに確認する通常 lane。 | `canonical`、`repo_local_support`、`historical`、`non_canonical` の boundary check。 |
| `derived-build` | generated references、frame-current assets、normalization assets を再生成して確認するとき。 | `derived` かつ `generated: true` の tracked runtime / reference surface。 |
| `legacy-distribution` | `.dist` や deferred public distribution bundle / installer 境界を確認するとき。 | `deferred_legacy` と deferred distribution output。 |
| `all` | merge 前や CI 相当の full suite。 | read-only、derived-build、legacy-distribution をまとめて確認する。 |

狭い docs / policy PR ではまず `read-only` を使う。generated surface や `.dist` を
触っていないのに `derived-build` や `legacy-distribution` を選ぶ必要はない。

## Generated Surface IDs

次の surface は registry 上で generated / derived として扱う。

| ID | Path | Generator | Source |
|---|---|---|---|
| `generated_knowledge_references` | `skills/sf6-agent/references/generated-*` | `packages/knowledge-generation/build-sf6-agent-knowledge.ps1` | `knowledge/curated` |
| `knowledge_lineage_report` | `data/knowledge-lineage.json` | `tests/validation/validate-knowledge-lineage-report.ps1 -Update` | `knowledge/` |
| `frame_current_runtime_assets` | `skills/sf6-agent/assets/frame-current/*` | `packages/skill-packaging/build-frame-current-runtime-assets.ps1` | `data/exports`, `data/roster` |
| `normalization_runtime_assets` | `skills/sf6-agent/assets/normalization/*` | `packages/skill-packaging/build-normalization-runtime-assets.ps1` | `data/aliases` |
| `release_bundle_dist` | `.dist/sf6-agent-bundle.zip` | `packages/skill-packaging/build-release-bundle.ps1` | `skills/sf6-agent`, `packages/skill-packaging` |

`generated_knowledge_references`、`frame_current_runtime_assets`、`normalization_runtime_assets`
は tracked generated outputs である。変更する場合は source / generator / generated
output の差分を review する。

`generated_knowledge_references` は現在 `skills/sf6-agent/references/generated-*` に
あるが、hand-written public adapter policy references とは別責務で扱う。
Phase 2 の責務分離 plan は
`docs/architecture/generated-reference-responsibility-plan.md` を参照する。

`frame_current_runtime_assets` は現在 `skills/sf6-agent/assets/frame-current/` にあるが、
Phase 2 では deferred public adapter から切り離す。移行 plan は
`docs/architecture/frame-current-runtime-separation-plan.md` を参照する。

`release_bundle_dist` は `generated_untracked` であり、local validation で作られても
tracked artifact にしない。

## Deferred Legacy Surface IDs

次の surface は private Hermes-first operation の active product focus ではない。

| ID | 意味 |
|---|---|
| `sf6_agent_public_adapter` | 既存 public answer adapter。現在は deferred legacy distribution surface。 |
| `sf6_agent_adapter_policy_references` | hand-written `skills/sf6-agent/references/*-policy.md`。deferred public adapter behavior only。 |
| `distribution_docs` | `docs/distribution/*`。interim install / release docs for deferred public distribution。 |
| `skill_installers_package` | deferred public skill installer tooling。 |
| `release_bundle_dist` | deferred public distribution bundle output。 |

これらを変更する PR は、通常の private workflow 改善と混ぜない。public adapter を
remove / relocate / reactivate するかは、後続の scoped ADR / issue で決める。
ADR-0004 により、`.dist`、installer tooling、distribution docs は public adapter
removal までの interim legacy-lane surface であり、長期 retained surface ではない。
Policy reference:
`docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md`。

## Non-canonical Boundary IDs

次の surface は通常回答の根拠ではない。

| ID | 境界 |
|---|---|
| `raw_snapshots` | current published exports を再現するための最小 Git-tracked input。ADR-0005 により、それ以上の raw cache / history は repo-external が既定。normal public answer evidence ではない。 |
| `normalized_intermediate_state` | intermediate state。現在は `documented_absent`。 |
| `manual_review_sidecars` | withheld rows や review holds。runtime current fact payload に入れない。 |
| `manual_review_debt_index` | manual-review debt の generated observability index。normal public answer authority ではない。 |

これらを accepted answer authority に昇格しない。必要な情報は review / curated /
exported current-fact surface へ、明示的な workflow と validator を通して移す。

Raw snapshot retention boundary:
`docs/architecture/decisions/0005-raw-snapshot-retention.md`。

Cross-surface non-canonical data authority boundary:
`docs/architecture/noncanonical-data-authority-boundaries.md`。

## Maintainer Rule

新しい directory、生成物、distribution output、local support package を追加するときは、
次を同じ PR で確認する。

- `data/repository-surfaces.json` に既存 role で表せるか。
- 表せない場合は `contracts/repository-surface.schema.json` の変更が必要か。
- `tests/validation/validate-repository-surfaces.ps1` に required ID や boundary check が必要か。
- README / architecture / workflow のどこから maintainer がその surface を発見できるか。

registry は refactor の許可証ではない。破壊的変更は歓迎だが、surface の role、source、
distribution status、validator expectation を先に見える化してから実施する。

## Package Surface Classification

`packages/` 配下の directory-level package classification は
`docs/architecture/package-surface-classification.md` を参照する。

現在の classification values:

- `active_repo_local`
- `deferred_distribution`
- `legacy`
- `shared_infra`

package entry は `data/repository-surfaces.json` の notes に
`package_classification=<value>` を含め、package-local README と一致させる。
