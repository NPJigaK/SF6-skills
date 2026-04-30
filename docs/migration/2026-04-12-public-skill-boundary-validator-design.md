# Public Skill Boundary Validator Design

## Goal

Add one small validator that protects the most important public-skill boundary:
`skills/<skill-name>/` must stay independent from other skill directories.

## Background

This repository now treats `skills/<skill-name>/` as the canonical public unit.
The next useful guard is not a stricter folder-shape rule, but a dependency-boundary rule.

That choice is intentional.

- GitHub describes agent skills as folders of instructions, scripts, and resources.
- Anthropic's public skills repository also treats each skill as a self-contained folder centered on `SKILL.md`.
- Repositories with broad skill ecosystems do not generally freeze one rigid top-level optional shape for every skill.

This repo should follow that direction.
We should avoid introducing a repo-local rule that is stricter than the ecosystem unless it protects a clearly higher-value boundary.

## Design Decision

Add a lightweight validator that checks only two things:

1. each public skill directory contains `SKILL.md`
2. each public `SKILL.md` avoids explicit path dependencies on another skill directory

The validator will not enforce a fixed optional folder layout.

## Why This Approach

### Recommended Approach

Validate boundary independence, not folder shape.

- keeps the rule close to the public-distribution goal
- matches the style of well-known skill repositories
- avoids overfitting the repo too early
- catches the most dangerous coupling with minimal policy surface

### Rejected Approach: Fixed Top-Level Shape

Do not require every public skill to expose only `SKILL.md`, `references/`, `assets/`, and `agents/`.

Reason:

- that is stricter than common ecosystem practice
- it would turn a local preference into a hard contract too early
- it would make future skills harder to prototype without strong evidence that the restriction is worth it

### Rejected Approach: Broad Recursive Banned-Content Scan

Do not recursively ban many directory names or file patterns inside public skills in this step.

Reason:

- it increases false positives
- it is harder to explain
- it goes beyond the minimum boundary we actually need right now

## Scope

### In Scope

- new validator: `tests/integration/validate-public-skill-boundaries.ps1`
- verification that every direct child of `skills/` has `SKILL.md`
- verification that `SKILL.md` does not contain explicit path dependencies on another skill directory
- add this validator to the repo's normal verification set

### Out of Scope

- banning `scripts/`, `docs/`, or other optional directories inside a public skill
- banning bare mentions of another skill by name
- scanning `references/`, `assets/`, or other files for all possible cross-skill references
- adding a new generic validation framework

## What Counts As A Forbidden Dependency

The validator should reject explicit path references that make one public skill depend on another skill directory.

Examples to reject:

- `skills/other-skill/...`
- `.agents/skills/other-skill/...`
- `../other-skill/...` when used as a sibling-skill directory reference

Examples to allow:

- `Use together with kb-sf6-core`
- plain mentions of another skill name
- references to `packages/` or `shared/` when shared demand is proven elsewhere in the repo contract

## Detection Rules

For each `skills/<skill-name>/SKILL.md`:

- reject `skills/<name>/` when `<name>` is not the current skill name
- reject any `.agents/skills/<name>/` path reference
- reject obvious sibling traversal patterns that point at another skill directory

Keep the matching rules simple and explainable.
The validator should prefer a few readable checks over a broad heuristic scanner.

## Expected Output

On success:

- `Public skill boundaries OK`

On failure:

- throw a message that identifies the offending skill and the offending reference pattern

## Verification Plan

Run:

- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-authoring-assets.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-core-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1`
- `powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1`

## Success Criteria

- the validator is easy to explain in one paragraph
- the validator does not impose a new rigid public-skill folder shape
- the validator catches explicit cross-skill directory dependencies
- existing public skills pass unchanged
