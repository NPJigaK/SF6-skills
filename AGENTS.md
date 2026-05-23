# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Priority / 優先順位

上記の behavioral guidelines は、このファイル内の一般的な作業方針の中で最優先とする。
プロジェクト固有の安全境界、データ境界、ExecPlan、検証ルールとは統合して適用する。

## Architecture Contract / アーキテクチャ契約

`docs/PLAN.md` is the authoritative architecture and implementation contract for this repository.
Implementations and designs must conform to `docs/PLAN.md` and any approved ExecPlan.
Do not introduce designs, runtime behavior, data flows, schemas, dependencies, or public interfaces that diverge from `docs/PLAN.md`.
If a requested change conflicts with or is not covered by `docs/PLAN.md`, state the gap, update the relevant Decision Log or ExecPlan, and stop for confirmation before editing.

## Project Goal / プロジェクト目標

SF6 Knowledge Coach を構築する。これは、キャラクターに依存しない個人向け SF6 コーチングシステムである。
JP は初期の主要アクティブキャラクターであり、グローバルな前提としてハードコードしてはならない。

## Plan Conformance / 計画への準拠

複数ファイルを変更する場合は、編集前に承認済みの ExecPlan を作成するか、それに従う。

実装時:
- 承認済みの ExecPlan に記載された内容のみを実装する。
- 計画外の機能、依存関係、スキーマ、公開 API、ランタイム挙動を追加しない。
- 計画が誤っている、または不完全な場合は、Decision Log を更新し、確認を得るために停止する。
- 各マイルストーンの完了後に Progress を更新する。
- 記載された検証コマンドを実行する。
- 最後に逸脱事項を報告する。

## Hard Rules / 厳守ルール

- 実在する個人データを公開リポジトリに入れない。
- 実在する `user_profile`、`personal_reviewed`、トレーニングログ、回答ログ、プライベート vault パス、プライベート overlay DB をコミットしない。
- 数値を含む回答には、専用ツールの結果が必要である。
- フレーム、ダメージ、スケーリング、確定反撃に関する質問に記憶だけで答えない。
- `candidate`、`observed`、`deprecated` の知識を、daily-answer の確定的な根拠として使わない。
- daily answer mode では、公開リポジトリとナレッジファイルは読み取り専用である。
- daily answer mode では Web アクセスを許可しない。
- Web アクセスは update/research modes でのみ使用する。
- VLM 出力は `observation_candidate` であり、reviewed knowledge ではない。
- Discord は薄いアダプターに限定する。

## Reviewer Tooling Boundary / レビューツールの境界

- 開発エージェントとレビュアーエージェントは、実装、レビュー、検証、成果物確認のために Codex skills、`jq`、browser/Playwright 系ツール、その他の補助ツールを使用してよい。
- これらはエージェント作業を補助するためのツールであり、承認済みの ExecPlan が明示的に追加しない限り、アプリの通常ランタイム、CLI、CI、決定論的バリデーターの依存関係にしない。
- このアプリを使って SF6 の回答を作成する場合、Codex skills、`jq`、browser/Playwright 系ツール、その他の補助ツールを回答根拠として使わない。回答精度は、承認済みの決定論的ツールと reviewed knowledge/data に依存させる。
- `.agents/` は ignore された未コミット状態のままにする。

## Validation / 検証

変更を完了する前に、以下を実行する:
- privacy guard
- schema validation
- 変更ファイルに関連する最小限の eval
- 該当する場合はフォーマット / 型チェック

Validator/test changes must be evidence-first. Do not weaken or rewrite a
validator merely to match current output. Each validator should be grounded in
source data, an approved policy artifact, a synthetic contract fixture, or a
privacy/security boundary; otherwise mark it as a review risk.

## Done / 完了条件

タスクは、以下を満たした場合にのみ完了とする:
- Acceptance Criteria を満たしている。
- Validation Commands が成功している、または失敗内容が明示的に説明されている。
- PLAN からの逸脱事項が列挙されている。
- 残存リスクが列挙されている。
