---
title: Package Surface Classification
status: accepted
last_reviewed: 2026-05-18
tracking_issue: "#250"
---

# Package Surface Classification

この文書は、`packages/` 配下の current package directory を
`active_repo_local`、`deferred_distribution`、`legacy`、`shared_infra` の
どれとして扱うかを定義する。

この分類は package directory の運用責務を示す。`surface_role` や
`public_distribution_status` を置き換えるものではなく、
`data/repository-surfaces.json` の package entry と合わせて読む。

## Classification Values

| Classification | 意味 |
|---|---|
| `active_repo_local` | private Hermes-first / maintainer validation で現在使う package。public skill distribution ではない。 |
| `deferred_distribution` | deferred public adapter / legacy distribution lane のためだけに残す package。ADR-0004 の removal sequence で削除対象になり得る。 |
| `legacy` | 現在の executable owner がない historical / placeholder package。新規機能を足さない。 |
| `shared_infra` | active repo-local entrypoint と deferred distribution entrypoint が同居している shared infrastructure。変更時は entrypoint 単位の境界を守る。 |

## Current Package Classification

| Package | Classification | Current responsibility | Boundary |
|---|---|---|---|
| `packages/calculation-executor/` | `active_repo_local` | calculation trace compatibility helper | SF6 formula / rounding / current-fact authority ではない。 |
| `packages/knowledge-generation/` | `active_repo_local` | `knowledge/curated/` から generated knowledge runtime payload を作る | 現在の出力先が deferred adapter path でも、generator 自体は repo-local runtime builder として扱う。 |
| `packages/skill-packaging/` | `shared_infra` | runtime asset builders と release bundle builder が同居 | `build-frame-current-runtime-assets.ps1` と `build-normalization-runtime-assets.ps1` は active repo-local。`build-release-bundle.ps1` は deferred distribution。 |
| `packages/skill-installers/` | `deferred_distribution` | deferred public adapter installer tooling | ADR-0004 により public adapter removal までの interim legacy-lane coverage。 |
| `packages/skill-validator/` | `legacy` | historical placeholder for skill metadata / packaging validation | 現在の validation authority は `tests/validation/`。ここへ新しい public skill validator を足さない。 |

## Maintainer Rules

- `active_repo_local` package は private maintainer workflow / validator / runtime
  generation のために維持してよい。
- `deferred_distribution` package には新しい public distribution features を足さない。
- `legacy` package には新しい executable behavior を足さない。必要な場合は
  `tests/validation/`、`tools/`、または新しい reviewed package surface を使う。
- `shared_infra` package を変更するときは、active repo-local entrypoint と
  deferred distribution entrypoint を PR body と validator notes で分ける。
- package classification を変える PR は、同じ PR で
  `packages/README.md`、package-local `README.md`、
  `data/repository-surfaces.json`、validator を更新する。
- `data/repository-surfaces.json` の package notes には
  `package_classification=<value>` を含める。

## Non-Goals

- This design step does not move package files.
- この design step では package files を移動しない。
- この design step では `.dist`、installer tooling、distribution docs、
  `skills/sf6-agent/` を削除しない。
- この design step では generated runtime assets、current facts、
  `official_raw`、public `sf6-agent` behavior、package executable behavior を変更しない。
- この design step では public skill distribution を再開しない。
- Hermes local state、raw transcripts、memory、sessions、logs、caches、
  credentials、secrets は repo に入れない。
