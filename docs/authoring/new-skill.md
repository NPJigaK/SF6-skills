# Adding A New Skill

## When to create a new skill

Create a new skill when the workflow, data contract, or trigger conditions are distinct enough that stuffing them into an existing skill would blur its purpose.

## How to scaffold it

1. Copy `shared/templates/skill/` into `skills/<skill-name>/`.
2. Rename `SKILL.md.template` to `SKILL.md`.
3. Add only the references, assets, and agent metadata that this skill needs.
4. Keep skill-specific artifacts local to the skill directory.
5. If a repo-level contract really needs protection, add the minimum validator under `tests/`.

## When to extract shared pieces

If only one skill needs something, keep it inside that skill.

Move executable or code-like infrastructure to `packages/` only after a second skill needs the same contract.

Move non-code artifacts to `shared/` only after a second skill needs the same contract.

## Public vs maintainer-only

Put end-user skills under `skills/`.

Put repository-curation or editorial workflows under `maintainer-skills/`.

`.agents/skills/` is a dogfooding mirror, not a source surface.

## What not to add to a public skill

Do not add dependencies on another skill, ingestion code, installer or bundle machinery, or raw/review artifacts to a public skill.
