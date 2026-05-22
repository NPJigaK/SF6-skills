## Project Goal

Build SF6 Knowledge Coach: a character-agnostic personal SF6 coaching system.
JP is the initial primary active character, not a hardcoded global assumption.

## Plan Conformance

For multi-file changes, create or follow an approved ExecPlan before editing.

When implementing:
- Implement only what the approved ExecPlan says.
- Do not add features, dependencies, schemas, public APIs, or runtime behavior outside the plan.
- If the plan is wrong or incomplete, update Decision Log and stop for confirmation.
- Keep Progress updated after each milestone.
- Run listed validation commands.
- Report deviations at the end.

## Hard Rules

- Do not put real personal data in the public repo.
- Do not commit real user_profile, personal_reviewed, training logs, answer logs, private vault path, or private overlay DB.
- Numeric answers require dedicated tool results.
- Do not answer frame/damage/scaling/punish questions from memory.
- Do not use candidate/observed/deprecated knowledge as definitive daily-answer evidence.
- Daily answer mode is read-only for public repo and knowledge files.
- Web access is not allowed in daily answer mode.
- Web access belongs to update/research modes only.
- VLM output is observation_candidate, never reviewed knowledge.
- Discord is a thin adapter only.

## Reviewer Tooling Boundary

- Repo-local Codex skills may be installed under `.agents/skills/` for reviewer-only external observation.
- Playwright/browser skills, if installed, are reviewer observation tools only.
- Do not add Playwright/browser automation to committed runtime code, CLI commands, CI validation, or normal deterministic validators unless an approved ExecPlan explicitly authorizes it.
- Do not install project skills into global Codex locations or Windows global Codex paths.
- Keep `.agents/` ignored and uncommitted.

## Validation

Before finalizing changes, run:
- privacy guard
- schema validation
- minimal eval relevant to changed files
- formatting/type checks if applicable

## Done

A task is done only when:
- Acceptance Criteria are satisfied.
- Validation Commands pass or failures are explicitly explained.
- PLAN deviations are listed.
- Remaining risks are listed.
