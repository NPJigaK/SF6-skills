---
title: PowerShell Compatibility Policy
status: accepted
last_reviewed: 2026-05-17
tracking_issue: "#240"
---

# PowerShell Compatibility Policy

この文書は、repo-local maintainer validation で使う PowerShell 実行環境を定義する。

## 結論

`pwsh` を supported maintainer validation command とする。

Windows PowerShell, usually exposed as `powershell.exe`, is treated as a
fallback / legacy-compatible runner. It may be useful for Windows-only legacy
installer checks, but it is not the preferred maintainer validation path for
v2.6 private Hermes-first work.

## 根拠

この repo の maintainer toolchain は `mise.toml` で PowerShell Core を
`powershell-core` として管理し、expected command を `pwsh` としている。
GitHub Actions も v2 validation を `pwsh` shell で実行する。

既存 docs には古い `powershell` / `powershell.exe` examples が残っている。
それらは deferred public distribution installer docs や Windows fallback
確認のためには残してよい。ただし、通常の repo validation、PR validation、
Hermes / Codex maintainer workflow では `pwsh` を使う。

## Supported Command Shape

通常の validation はこの形で実行する。

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1 -Lane read-only
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

focused validator も同じ command shape を使う。

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-doc-links.ps1
```

`-NoProfile` は user profile state の影響を避けるために使う。`-ExecutionPolicy Bypass`
は Windows execution policy で local script validation が止まる環境を避けるために
付ける。これは repo policy や security boundary を緩めるものではなく、repo 内の
reviewed script を明示的に実行するための invocation shape である。

## Known Difference: Git Visibility

Windows PowerShell で `run-all.ps1` や generated-surface validators を実行すると、
`git` が見えない環境がある。この場合、validator は git-based cleanliness check を
skip または warning として扱うことがある。

その warning を validation success と同一視しない。Windows PowerShell が `git` を
見られなかった場合は、WSL、Git Bash、`pwsh`、または別の git-visible shell で
次を確認する。

```bash
git status --porcelain
git diff --check
git diff --check origin/main...HEAD
```

generated surface を触る PR では、少なくとも次の derived / generated paths に
残差分がないことも確認する。

```bash
git status --porcelain -- \
  skills/sf6-agent/references/generated-knowledge-index.md \
  skills/sf6-agent/references/generated-concepts.md \
  skills/sf6-agent/assets/frame-current \
  runtime/normalization \
  skills/sf6-agent/assets/normalization \
  .dist
```

## When Windows PowerShell Is Acceptable

Windows PowerShell は次の用途に限定して扱う。

- deferred public distribution installer docs の legacy example。
- Windows-only user environment での compatibility smoke。
- `powershell.exe` 自体の fallback behavior を検証する scoped issue。

ただし、その結果を CI-equivalent validation として扱うには、`pwsh` または
git-visible shell での確認を併記する。

## Documentation Rule

新しい maintainer docs、workflow docs、PR body examples、smoke report templates では
`pwsh` を使う。`powershell` / `powershell.exe` を書く場合は、Windows fallback、
legacy distribution installer、または explicit compatibility smoke であることを
文脈に書く。

## Non-goals

- Windows PowerShell support を削除しない。
- deferred public distribution installer docs を一括 rewrite しない。
- `run-all.ps1` の runtime behavior をこの policy だけで変更しない。
- local PATH、profile、registry、credential、Hermes profile state を canonical にしない。
