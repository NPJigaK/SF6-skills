# SF6 Knowledge Agent Kit メンテナーガイド

このドキュメントは、日本語話者メンテナー向けの入口です。

本文は日本語firstの正本です。`metadata key`、artifact ID、schema enum、filename/path slug、command名、script名、validator contractは英語互換を維持します。

このガイドは詳細手順の置き換えではありません。必須ルールは [AGENTS.md](../../AGENTS.md)、実際の手順は [workflows/](../../workflows/) と [docs/architecture/](../architecture/) を正本として参照してください。

## 1. このrepoは何か

SF6 Knowledge Agent Kit は、Street Fighter 6 の質問にAI agentが証拠境界つきで答えるための、GitHub review可能な知識正本と配布kitです。

このrepoは大きく分けて次の2つを扱います。

- Public answer adapter: ユーザーのSF6質問に答えるための `skills/sf6-agent/`
- Repo-local maintainer surfaces: 知識、検証、workflow、packaging、Hermes harnessを育てるためのrepo内surface

公開利用者向けに配布する主対象は `skills/sf6-agent/` です。メンテナー向けの `AGENTS.md`、`workflows/*`、`tests/validation/*`、`packages/*`、`contracts/*`、`packs/hermes-sf6/*` は、repoをcloneしたメンテナーが使うrepo-local surfaceです。

## 2. まず読むもの

最初はこの順番で読むと迷いにくいです。

1. [AGENTS.md](../../AGENTS.md): agentとメンテナー向けの必須repo guidance
2. [v2-architecture.md](../architecture/v2-architecture.md): v2のsource-of-truth構造
3. [language-policy.md](../architecture/language-policy.md): 日本語first運用と英語互換構造
4. [harness-and-distribution-roles.md](../architecture/harness-and-distribution-roles.md): public adapter、repo-local workflow、Hermes harness、配布境界
5. [japanese-maintainer-docs-policy.md](../architecture/japanese-maintainer-docs-policy.md): 日本語メンテナー向けdoc方針
6. [workflows/README.md](../../workflows/README.md): canonical maintainer proceduresの索引

このガイドは人間向けの入口です。必須挙動を別ファイルへ移動するものではありません。

## 3. Repo全体の地図

| Path | 役割 |
|---|---|
| `AGENTS.md` | repo guidanceのentrypoint。必須ルールを置く場所。 |
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
| `skills/sf6-agent/` | public answer adapter。ユーザー質問に答えるruntime surface。 |
| `skills/sf6-agent/references/generated-*` | `knowledge/curated/` から生成されるderived references。 |
| `skills/sf6-agent/assets/frame-current/` | `data/exports/` と `data/roster/` から生成されるexact current runtime assets。 |
| `packs/hermes-sf6/` | repo-local optional Hermes harness。public answer skillではない。 |
| `packages/knowledge-generation/` | curated knowledgeからgenerated referencesを作るtooling。 |
| `packages/skill-packaging/` | public adapter bundleやframe-current runtime assetsを作るtooling。 |
| `tests/validation/` | repo境界を守るvalidation entrypoints。 |
| `.dist/` | release bundleなどのderived distribution output。正本ではない。 |

`repo-local` は外部配布境界を表す言葉で、non-canonicalという意味ではありません。たとえば `contracts/` と `workflows/` はrepo-localですが、repo内ではcanonicalです。

## 4. Knowledgeを増やす基本フロー

知識追加は、すぐに `knowledge/curated/` へ入れるのではなく、source、evidence、reviewを分けて進めます。

```text
source
  -> evidence / observations / claims
  -> review
  -> curated
  -> generated references
```

基本の考え方は次の通りです。

- Source: URL、accessed_at、短いsummary、scope、copyright boundaryを残す。
- Evidence / observations / claims: 記事、画像、動画から見えたことや主張をreview-onlyで分解する。
- Review: 不確実性、patch sensitivity、setup-specific claim、verification needsを保持する。
- Curated: 安定して受け入れられる知識だけを昇格する。
- Generated references: `knowledge/curated/` から生成されるpublic adapter向けpayload。手で正本化しない。

記事sourceとclaim artifactはvalidatorで守られています。動画sourceとvideo observation artifactはpilot済みですが、専用validatorはfollow-upです。

## 5. Current fact と curated knowledgeを混ぜない

このrepoでは、exact current factsとcurated knowledgeを分けます。

- exact move-specific current facts: `data/exports/`、`data/roster/`、derived `skills/sf6-agent/assets/frame-current/`
- stable concepts / reviewed explanations: `knowledge/curated/`
- unresolved numeric/system/current claims: `knowledge/review/`

たとえば、具体的なframe値、move-specific値、現行patch依存の正確な数値は `knowledge/curated/` に入れません。

コンボ補正のようなsystem mechanicsも、安定概念として説明できる部分と、patch-sensitiveな数値・例外を分けて扱います。

## 6. 記事・画像・動画の扱い

記事、画像、動画はsourceとして扱えますが、raw contentをrepoへ保存しないことが基本です。

| 対象 | 主なsurface | 手順 |
|---|---|---|
| 記事 | `knowledge/sources/articles/`, `knowledge/evidence/claims/`, `knowledge/review/` | [ingest-article.md](../../workflows/ingest-article.md) |
| 画像込み記事 | article source + image-derived `observation / needs_review` | [ingest-article.md](../../workflows/ingest-article.md), [media-scratch-cache-policy.md](../../workflows/media-scratch-cache-policy.md) |
| 動画 | `knowledge/sources/videos/`, `knowledge/evidence/video-observations/`, `knowledge/review/` | [ingest-video.md](../../workflows/ingest-video.md) |
| Claim review | `knowledge/evidence/claims/`, `knowledge/review/` | [review-claims.md](../../workflows/review-claims.md) |

画像・動画では、repo外scratch/cacheを使います。raw images、screenshots、downloaded videos、full transcripts、large excerptsはrepoへ保存しません。

詳しくは [media-scratch-cache-policy.md](../../workflows/media-scratch-cache-policy.md) を参照してください。

## 7. Hermesの扱い

Hermesは、knowledge ingest、review、image observation、video observationを反復しやすくするための推奨maintainer harnessです。

ただし、Hermesは必須ではありません。設定済みprofileがある場合は使うのが望ましいですが、Codex、人間、他agentが同じworkflowに従ってrepo artifactを作ることもできます。

重要な境界は次の通りです。

- Hermes memory、sessions、profile state、browser state、cron stateはcanonicalではない。
- 最終成果物は `knowledge/` や `docs/testing/smoke-runs/` などのrepo artifactに残す。
- `packs/hermes-sf6/` はrepo-local optional harnessで、public answer adapterではない。
- Hermes wrapperを足す場合も、canonical workflowsの薄いwrapperにする。

Profile setupは [hermes-ingest-profile-setup.md](../../workflows/hermes-ingest-profile-setup.md) を参照してください。

## 8. GitHub運用

Issue、PR、CI status、label、milestone、merge操作は原則 `gh` CLIで行います。

詳しい正本手順は [github-management.md](../../workflows/github-management.md) です。

通常の流れは次の通りです。

```text
issueでscopeを決める
  -> branchを切る
  -> 小さい変更をcommitする
  -> validationを通す
  -> draft PRを作る
  -> review後にready化/mergeする
```

PR本文やsmoke reportには、認証情報、private local state、profile固有のlocal state、raw mediaを含めません。

## 9. 検証

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

画像・動画を扱ったPRでは、[media-scratch-cache-policy.md](../../workflows/media-scratch-cache-policy.md) のrepo-local media/state scanも実行します。

## 10. 日本語docの方針

このrepoは日本語first運用です。日本語話者メンテナーに必要な説明は、日本語正本、`.ja.*` companion、またはinline Japanese summaryで提供します。

一方で、構造は英語互換を維持します。

- filename/path slug
- metadata key
- artifact ID
- schema enum value
- generated marker
- validator contract
- package/installer interface
- command/script name

`AGENTS.md` や `skills/sf6-agent/SKILL.md` のようなagent entrypointでは、必須ルールを `.ja.*` companionに逃がしません。人間向けの日本語解説は作れても、required behaviorはentrypoint本体に残します。

詳しくは [japanese-maintainer-docs-policy.md](../architecture/japanese-maintainer-docs-policy.md) を参照してください。

## 11. 次にやる作業を選ぶ

迷ったら、次の順で考えると安全です。

1. 既存Issueのscopeを確認する。
2. 該当workflowを読む。
3. canonical output先を決める。
4. raw source、media、private stateをrepoへ入れない。
5. review-onlyとaccepted knowledgeを分ける。
6. validationを通す。
7. PR本文に、何を検証し、何を検証していないかを書く。

特にsource ingestでは、「読めたこと」よりも「どの境界でrepo artifactに落としたか」を重視してください。
