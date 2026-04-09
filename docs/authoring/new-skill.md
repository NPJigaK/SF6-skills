# Adding A New Skill

## When to create a new skill

Create a new skill when the workflow, data contract, or trigger conditions are distinct enough that stuffing them into an existing skill would blur its purpose.

## How to scaffold it

1. Copy `shared/templates/skill/` into `skills/<skill-name>/`.
2. Rename `SKILL.md.template` to `SKILL.md`.
3. Add only the references, assets, scripts, and tests that this skill needs.

## When to extract shared pieces

If only one skill needs something, keep it inside that skill.

Move code to `packages/` or non-code artifacts to `shared/` only after a second skill needs the same contract.

## Public vs maintainer-only

Put end-user skills under `skills/`.

Put repository-curation or editorial workflows under `maintainer-skills/`.
