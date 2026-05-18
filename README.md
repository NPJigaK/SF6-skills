# SF6 Knowledge Agent Kit

SF6 Knowledge Agent Kit は、Street Fighter 6 の質問にAI agentが証拠境界つきで答えるための、GitHub review可能な知識正本と配布kitです。

このrepoは日本語firstで運用します。本文、source summary、review note、curated proseは日本語で書いてよいです。一方で、metadata key、artifact ID、schema enum、filename/path slug、command名、script名、validator contractは英語互換を維持します。

## これは何か

このrepoは、SF6回答agentのために次のsurfaceを分けて管理します。

- SF6 knowledge source of truth
- exact current fact runtime assets
- evals and validators
- maintainer workflows
- repo-local Hermes orchestration harness

現在の開発優先度は、公開skill配布ではなく、Windows Codex app から
Hermes を操作して知識収集・review・検証・PR化を安定させる
private Hermes-first 運用です。既存のpublic `skills/sf6-agent/` adapter
と deferred distribution surface は、runtime payload relocation 後に削除済みです。
将来public distributionを再開する場合は新しいADRが必要です。

## まずどこを見るか

- このrepoをメンテしてknowledgeを育てたい場合: このREADMEを読み、次に [AGENTS.md](./AGENTS.md) と [workflows/README.md](./workflows/README.md) を見る。
- v2の設計方針を確認したい場合: [docs/architecture/README.md](./docs/architecture/README.md) を見る。

## 主要surface

| Path | 役割 |
|---|---|
| `knowledge/` | SF6 knowledgeのcanonical surface。source、evidence、review、curatedを保持する。 |
| `knowledge/curated/` | review後に受け入れた安定知識。exact current valuesは入れない。 |
| `knowledge/sources/` | 記事、動画などのsource metadataと短いsummary。全文やraw mediaは保存しない。 |
| `knowledge/evidence/claims/` | 記事などから抽出したcandidate claims。review-only境界を守る。 |
| `knowledge/evidence/video-observations/` | 動画からのtimestamped observations。visible observationとspeaker claimを分ける。 |
| `knowledge/review/` | unresolvedな論点、verification needs、promotion待ちのreview note。 |
| `data/exports/` | exact move-specific current factsのauthority。 |
| `data/roster/` | rosterやruntime current-fact生成に必要なauthority。 |
| `contracts/` | schemaとartifact contractのcanonical surface。 |
| `workflows/` | メンテナー手順のcanonical surface。 |
| `evals/` | answer-quality casesとrubricsのcanonical surface。 |
| `packages/` | package classification は `docs/architecture/package-surface-classification.md` に従う。 |
| `packages/knowledge-generation/` | `active_repo_local`。curated knowledgeからgenerated runtime payloadを作るtooling。 |
| `packages/skill-packaging/` | `active_repo_local`。runtime asset builders。 |
| `packs/hermes-sf6/` | repo-local Hermes orchestration support。public answer skillではない。 |
| `tests/validation/` | repo境界を守るvalidation entrypoints。 |

`repo-local` は外部配布境界を表す言葉で、non-canonicalという意味ではありません。たとえば `contracts/` と `workflows/` はrepo-localですが、repo内ではcanonicalです。

Validator-facing boundary markers:

- `knowledge/` is canonical
- `data/exports/` and `data/roster/` are the exact current-fact authority
- `runtime/generated-knowledge/` is derived
- `runtime/frame-current/` is derived
- `runtime/normalization/` is derived

Machine-readable surface classifications live in
[`data/repository-surfaces.json`](./data/repository-surfaces.json). Maintainer
guidance for using the registry with validation lanes is in
[`docs/architecture/repository-surface-registry-policy.md`](./docs/architecture/repository-surface-registry-policy.md).
The Phase 2 plan for separating frame-current runtime assets from the deferred
public adapter is in
[`docs/architecture/frame-current-runtime-separation-plan.md`](./docs/architecture/frame-current-runtime-separation-plan.md).
The Phase 2 plan for separating generated knowledge references from
hand-written public adapter policy references is in
[`docs/architecture/generated-reference-responsibility-plan.md`](./docs/architecture/generated-reference-responsibility-plan.md).
The ADR selecting removal of the public adapter after runtime relocation is in
[`docs/architecture/decisions/0003-retire-public-sf6-agent-adapter.md`](./docs/architecture/decisions/0003-retire-public-sf6-agent-adapter.md).
The ADR selecting interim legacy-lane handling and later deletion for `.dist`,
installers, and distribution docs is in
[`docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md`](./docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md).
The ADR selecting minimal Git retention for raw snapshots and deferring broader
raw cache/hash references to repo-external storage is in
[`docs/architecture/decisions/0005-raw-snapshot-retention.md`](./docs/architecture/decisions/0005-raw-snapshot-retention.md).
Package directory classifications are in
[`docs/architecture/package-surface-classification.md`](./docs/architecture/package-surface-classification.md).
Generic JSON Schema validation runner guidance is in
[`docs/architecture/schema-validation-runner.md`](./docs/architecture/schema-validation-runner.md).

## Public answer adapter status

`skills/sf6-agent/` は ADR-0003 の方針に従い、runtime payload relocation 後に削除済みです。
public adapter was removed. Future public answer adapter or distribution work
requires a new scoped architecture decision.

現在の回答用 runtime payload は次の repo-local surface です。

- `knowledge/curated/` から生成された `runtime/generated-knowledge/`
- `data/exports/` と `data/roster/` から生成された `runtime/frame-current/`
- `data/aliases/` から生成された `runtime/normalization/`

`workflows/*`、`tests/validation/*`、`packages/*`、`contracts/*`、
`packs/hermes-sf6/*` はpublic answer skillとして配布しません。

## Knowledgeを増やす基本フロー

知識追加は、すぐに `knowledge/curated/` へ入れるのではなく、source、evidence、reviewを分けて進めます。

```text
source
  -> evidence / observations / claims
  -> review
  -> curated
  -> generated references
```

基本の考え方:

- Source: URL、accessed_at、短いsummary、scope、copyright boundaryを残す。
- Evidence / observations / claims: 記事、画像、動画から見えたことや主張をreview-onlyで分解する。
- Review: 不確実性、patch sensitivity、setup-specific claim、verification needsを保持する。
- Curated: 安定して受け入れられる知識だけを昇格する。
- Generated references: `knowledge/curated/` から生成されるrepo-local runtime payload。手で正本化しない。

記事・画像・動画のingestでは、raw article、raw image、screenshot、downloaded video、full transcript、large excerptをrepoへ保存しません。必要なsource metadata、短いsummary、observation、candidate claim、review noteだけを残します。

## Current fact と curated knowledgeを混ぜない

このrepoでは、exact current factsとcurated knowledgeを分けます。

- exact move-specific current facts: `data/exports/`、`data/roster/`、derived `runtime/frame-current/`
- stable concepts / reviewed explanations: `knowledge/curated/`
- unresolved numeric/system/current claims: `knowledge/review/`

具体的なframe値、move-specific値、現行patch依存の正確な数値は `knowledge/curated/` やgenerated knowledge referencesへ入れません。

コンボ補正のようなsystem mechanicsも、安定概念として説明できる部分と、patch-sensitiveな数値・例外を分けて扱います。

## 記事・画像・動画の扱い

| 対象 | 主なsurface | 手順 |
|---|---|---|
| 記事 | `knowledge/sources/articles/`, `knowledge/evidence/claims/`, `knowledge/review/` | [workflows/ingest-article.md](./workflows/ingest-article.md) |
| 画像込み記事 | article source + image-derived `observation / needs_review` | [workflows/ingest-article.md](./workflows/ingest-article.md), [workflows/media-scratch-cache-policy.md](./workflows/media-scratch-cache-policy.md) |
| 動画 | `knowledge/sources/videos/`, `knowledge/evidence/video-observations/`, `knowledge/review/` | [workflows/ingest-video.md](./workflows/ingest-video.md) |
| Claim review | `knowledge/evidence/claims/`, `knowledge/review/` | [workflows/review-claims.md](./workflows/review-claims.md) |

画像・動画では、repo外scratch/cacheを使います。詳しくは [workflows/media-scratch-cache-policy.md](./workflows/media-scratch-cache-policy.md) を参照してください。

## Hermesの扱い

Hermesは、configured maintainer profile がある環境では primary repo-local orchestration harness です。knowledge ingest、review、image observation、video observation、validation、smoke workflowを束ねるために使います。

ただし、Hermesはpublic answer adapterではなく、必須dependencyでもありません。Hermesが利用できない場合でも、Codex、人間、他agentが同じcanonical workflowに従ってrepo artifactを作ることができます。

重要な境界:

- Hermes memory、sessions、profile state、browser state、cron stateはcanonicalではない。
- 最終成果物は `knowledge/` や `docs/testing/smoke-runs/` などのrepo artifactに残す。
- `packs/hermes-sf6/` はrepo-local orchestration supportで、public answer adapterではない。
- Hermes wrapperを足す場合も、canonical workflowsの薄いwrapperにする。
- Hermesのv2.1 roleは [docs/architecture/decisions/0001-hermes-primary-orchestration.md](./docs/architecture/decisions/0001-hermes-primary-orchestration.md) で定義します。

Profile setupは [workflows/hermes-ingest-profile-setup.md](./workflows/hermes-ingest-profile-setup.md) を参照してください。

## 配布

Public distribution bundle、installer tooling、distribution docs は ADR-0004
と issue #295 により削除済みです。deferred distribution surfaces were removed.

APM / Agent Skills配布は、private運用とknowledge workflowが安定するまで
再開しません。repo maintainer workflowをpublic skill packageとして配布しません。

## GitHub運用

Issue、PR、CI status、label、milestone、merge操作は原則 `gh` CLIで行います。

詳しい正本手順は [workflows/github-management.md](./workflows/github-management.md) です。

PR本文やsmoke reportには、認証情報、private local state、profile固有のlocal state、raw mediaを含めません。

## Maintainer toolchain

WSL/Linux向けのrepo-local maintainer toolchainは `mise.toml` と `mise.lock` で管理します。Python依存は `ingest/frame_data/uv.lock` で固定し、通常の更新PRは Renovate で扱います。

Hermes CLIは `mise.toml` のtoolには含めません。Hermesはconfigured
maintainer profileがある環境のrepo-local growth engineであり、root
`flake.nix` / `flake.lock` と Renovate Nix flake PRs で管理します。

詳しい手順と境界は [workflows/manage-maintainer-toolchain.md](./workflows/manage-maintainer-toolchain.md) を参照してください。

## 検証

変更後は、少なくとも次を確認します。

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane read-only
```

`run-all.ps1` は validation lane を持ちます。引数なしは従来互換の
`all` lane です。

| Lane | 用途 |
|---|---|
| `read-only` | 通常の docs / contracts / workflows / registry / artifact 境界検証。generated output を作らない。 |
| `derived-build` | generated references、frame-current assets、normalization assets を再生成して残差分を確認する。 |
| `all` | CI相当。derived build を含むfull suite。 |

Validation lane と repository surface role の対応は
[`docs/architecture/repository-surface-registry-policy.md`](./docs/architecture/repository-surface-registry-policy.md)
を参照してください。

Maintainer validation は `pwsh` を supported command とします。
Windows PowerShell / `powershell.exe` fallback と git visibility warning の扱いは
[`docs/architecture/powershell-compatibility-policy.md`](./docs/architecture/powershell-compatibility-policy.md)
を参照してください。

広いPRやmerge前確認では、従来どおりfull suiteを実行します。

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

追加でよく使う確認:

```bash
git diff --check
git status --porcelain
```

Generated referencesやframe-current assetsを変更するPRでは、derived outputが意図せず汚れていないかも確認します。

画像・動画を扱ったPRでは、[workflows/media-scratch-cache-policy.md](./workflows/media-scratch-cache-policy.md) のrepo-local media/state scanも実行します。

## 次に読むもの

- [AGENTS.md](./AGENTS.md): agentとメンテナー向けの必須repo guidance
- [docs/architecture/v2-architecture.md](./docs/architecture/v2-architecture.md): v2のsource-of-truth構造
- [docs/architecture/language-policy.md](./docs/architecture/language-policy.md): 日本語first運用と英語互換構造
- [docs/architecture/harness-and-distribution-roles.md](./docs/architecture/harness-and-distribution-roles.md): public adapter、repo-local workflow、Hermes harness、配布境界
- [docs/architecture/repository-surface-registry-policy.md](./docs/architecture/repository-surface-registry-policy.md): repository surface registry と validation lane の使い方
- [docs/architecture/frame-current-runtime-separation-plan.md](./docs/architecture/frame-current-runtime-separation-plan.md): frame-current runtime assets を deferred public adapter から分離する Phase 2 plan
- [docs/architecture/powershell-compatibility-policy.md](./docs/architecture/powershell-compatibility-policy.md): `pwsh` と Windows PowerShell fallback の互換 policy
- [docs/architecture/japanese-maintainer-docs-policy.md](./docs/architecture/japanese-maintainer-docs-policy.md): 日本語メンテナー向けdoc方針
- [workflows/README.md](./workflows/README.md): canonical maintainer proceduresの索引
- [docs/testing/README.md](./docs/testing/README.md): smoke runsとvalidation docs

## English note

This repository is Japanese-first in operation. Private Hermes-first operation
is the current priority. The former `skills/sf6-agent/` adapter and deferred
distribution surface were removed after runtime relocation. Metadata keys, paths, schema enum values, command names,
validator contracts, and package interfaces remain English-compatible.
