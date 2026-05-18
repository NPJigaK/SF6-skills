---
title: Package Surface Classification
status: accepted
last_reviewed: 2026-05-18
tracking_issue: "#250"
---

# Package Surface Classification

この文書は、`packages/` 配下の current package directory を
`active_repo_local`、`legacy` の
どれとして扱うかを定義する。

この分類は package directory の運用責務を示す。`surface_role` や
`public_distribution_status` を置き換えるものではなく、
`data/repository-surfaces.json` の package entry と合わせて読む。

## Classification Values

| Classification | 意味 |
|---|---|
| `active_repo_local` | private Hermes-first / maintainer validation で現在使う package。public skill distribution ではない。 |
| `legacy` | 現在の executable owner がない historical / placeholder package。新規機能を足さない。 |

## Current Package Classification

| Package | Classification | Current responsibility | Boundary |
|---|---|---|---|
| `packages/calculation-executor/` | `active_repo_local` | calculation trace compatibility helper | SF6 formula / rounding / current-fact authority ではない。 |
| `packages/knowledge-generation/` | `active_repo_local` | `knowledge/curated/` から generated knowledge runtime payload を作る | repo-local runtime builder として扱う。 |
| `packages/skill-packaging/` | `active_repo_local` | runtime asset builders | Deferred public distribution package files were removed with issue #295. |
| `packages/skill-validator/` | `legacy` | historical placeholder for skill metadata / packaging validation | 現在の validation authority は `tests/validation/`。ここへ新しい public skill validator を足さない。 |

## Maintainer Rules

- `active_repo_local` package は private maintainer workflow / validator / runtime
  generation のために維持してよい。
- `legacy` package には新しい executable behavior を足さない。必要な場合は
  `tests/validation/`、`tools/`、または新しい reviewed package surface を使う。
- package classification を変える PR は、同じ PR で
  `packages/README.md`、package-local `README.md`、
  `data/repository-surfaces.json`、validator を更新する。
- `data/repository-surfaces.json` の package notes には
  `package_classification=<value>` を含める。

## Non-Goals

- Deferred public distribution package files were removed with issue #295.
- この design step では generated runtime assets、current facts、
  `official_raw`、public `sf6-agent` behavior、package executable behavior を変更しない。
- この design step では public skill distribution を再開しない。
- Hermes local state、raw transcripts、memory、sessions、logs、caches、
  credentials、secrets は repo に入れない。
