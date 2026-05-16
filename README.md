# SF6 Knowledge Agent Kit

SF6 Knowledge Agent Kit は、Street Fighter 6 の質問にAI agentが証拠境界つきで答えるための、GitHub review可能な知識正本と配布kitです。

このrepoは日本語firstで運用します。本文、source summary、review note、curated proseは日本語で書いてよいです。一方で、metadata key、artifact ID、schema enum、filename/path slug、command名、script名、validator contractは英語互換を維持します。

## これは何か

このrepoは、SF6回答agentのために次のsurfaceを分けて管理します。

- SF6 knowledge source of truth
- deferred public answer adapter / legacy distribution surface
- exact current fact runtime assets
- evals and validators
- maintainer workflows
- repo-local Hermes orchestration harness

現在の開発優先度は、公開skill配布ではなく、Windows Codex app から
Hermes を操作して知識収集・review・検証・PR化を安定させる
private Hermes-first 運用です。`skills/sf6-agent/` は既存のpublic
adapter surfaceとして残っていますが、既知の外部利用者はいないため、
外部互換性で守るactive product surfaceではありません。

## まずどこを見るか

- 既存public adapter surfaceを確認したい場合: `skills/sf6-agent/` と [docs/distribution/agents/](./docs/distribution/agents/) を見る。ただし現在はdeferred/legacy distribution surfaceです。
- このrepoをメンテしてknowledgeを育てたい場合: このREADMEを読み、次に [AGENTS.md](./AGENTS.md) と [workflows/README.md](./workflows/README.md) を見る。
- v2の設計方針を確認したい場合: [docs/architecture/README.md](./docs/architecture/README.md) を見る。

## 主要surface

| Path | 役割 |
|---|---|
| `skills/sf6-agent/` | 既存public answer adapter。現在はdeferred/legacy distribution surfaceで、private Hermes-first運用の安定化を優先する。 |
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
| `packages/knowledge-generation/` | curated knowledgeからgenerated referencesを作るtooling。 |
| `packages/skill-packaging/` | public adapter bundleやframe-current runtime assetsを作るtooling。 |
| `packs/hermes-sf6/` | repo-local Hermes orchestration support。public answer skillではない。 |
| `tests/validation/` | repo境界を守るvalidation entrypoints。 |
| `.dist/` | release bundleなどのderived distribution output。正本ではない。 |

`repo-local` は外部配布境界を表す言葉で、non-canonicalという意味ではありません。たとえば `contracts/` と `workflows/` はrepo-localですが、repo内ではcanonicalです。

Validator-facing boundary markers:

- `knowledge/` is canonical
- `data/exports/` and `data/roster/` are the exact current-fact authority
- `skills/sf6-agent/references/generated-*` is derived
- `skills/sf6-agent/assets/frame-current/` is derived

## Public answer adapter status

`skills/sf6-agent/` は既存の単一public answer adapter surfaceです。
ただし、現在は公開skill機能拡張の対象ではなく、deferred/legacy
distribution surfaceとして扱います。

主に次を使って回答します。

- hand-written answer, uncertainty, and current-fact policies
- `knowledge/curated/` から生成された `skills/sf6-agent/references/generated-*`
- `data/exports/` と `data/roster/` から生成された `skills/sf6-agent/assets/frame-current/`

`skills/sf6-agent/` は当面、新しい公開機能を足す場所ではありません。
今後のscoped workで残存責務を棚卸ししたうえで、削除・移設・再有効化の
どれにするかを決めます。

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
- Generated references: `knowledge/curated/` から生成されるpublic adapter向けpayload。手で正本化しない。

記事・画像・動画のingestでは、raw article、raw image、screenshot、downloaded video、full transcript、large excerptをrepoへ保存しません。必要なsource metadata、短いsummary、observation、candidate claim、review noteだけを残します。

## Current fact と curated knowledgeを混ぜない

このrepoでは、exact current factsとcurated knowledgeを分けます。

- exact move-specific current facts: `data/exports/`、`data/roster/`、derived `skills/sf6-agent/assets/frame-current/`
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

Public distribution bundle は現在 deferred/legacy output です。

```text
.dist/sf6-agent-bundle.zip
```

Human-readable install docsは [docs/distribution/agents/](./docs/distribution/agents/) にありますが、現在の開発優先度はprivate Hermes-first運用です。

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
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
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
- [docs/architecture/japanese-maintainer-docs-policy.md](./docs/architecture/japanese-maintainer-docs-policy.md): 日本語メンテナー向けdoc方針
- [workflows/README.md](./workflows/README.md): canonical maintainer proceduresの索引
- [docs/testing/README.md](./docs/testing/README.md): smoke runsとvalidation docs

## English note

This repository is Japanese-first in operation. Private Hermes-first operation
is the current priority, and `skills/sf6-agent/` is a deferred legacy
distribution surface. Metadata keys, paths, schema enum values, command names,
validator contracts, and package interfaces remain English-compatible.
