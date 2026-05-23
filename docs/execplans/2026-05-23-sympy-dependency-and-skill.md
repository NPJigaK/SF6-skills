# SymPy Dependency And Skill

Status: Implemented locally; validation and mandatory review complete.

## Purpose

Add SymPy as a project dependency and install the referenced SymPy Codex skill
into the ignored local agent skill area so future SF6 numeric-calculation work
can use exact deterministic arithmetic when an approved tool or workflow calls
for it.

## Scope

Included:

- Add `sympy` to project dependencies and refresh `uv.lock`.
- Install the referenced `scientific-skills/sympy` skill under
  `.agents/skills/Sympy-Skill/`, including its reference files and upstream MIT
  license notice.
- Validate that locked dependency resolution works.
- Validate a minimal SymPy import and exact arithmetic smoke.
- Run privacy guard, schema validation, related validators, and tests.

Excluded:

- Do not add new SF6 answer behavior, schemas, public APIs, CLIs, retrieval
  behavior, or data pipelines.
- Do not promote any numeric SF6 fact source or change current-fact authority.
- Do not make Codex skills part of the app runtime.
- Do not commit `.agents/`; it remains an ignored reviewer/developer tool
  area.

## Acceptance Criteria

- `pyproject.toml` declares `sympy`.
- `uv.lock` is consistent with `pyproject.toml`.
- `PYTHONPATH=src uv run --locked python -c "import sympy"` succeeds.
- A minimal exact arithmetic smoke confirms SymPy is usable from the locked
  project environment.
- The SymPy skill files exist under `.agents/skills/Sympy-Skill/` and remain
  ignored by git.
- Existing validation commands succeed, or failures are explained.

## Files / Interfaces

Tracked files:

- `pyproject.toml`
- `uv.lock`
- `docs/execplans/2026-05-23-sympy-dependency-and-skill.md`

Ignored local files:

- `.agents/skills/Sympy-Skill/SKILL.md`
- `.agents/skills/Sympy-Skill/LICENSE.md`
- `.agents/skills/Sympy-Skill/references/*.md`

No runtime command, schema, parser, retrieval, data artifact, answer mode, CI
workflow, or public interface is added.

## Validation Commands

Run from the repository root:

```bash
uv lock --check
PYTHONPATH=src uv run --locked python -c "from sympy import Rational, symbols, expand; x = symbols('x'); assert Rational(1, 3) + Rational(1, 6) == Rational(1, 2); assert expand((x + 1)**2) == x**2 + 2*x + 1"
test -f .agents/skills/Sympy-Skill/SKILL.md
test -f .agents/skills/Sympy-Skill/LICENSE.md
test -f .agents/skills/Sympy-Skill/references/core-capabilities.md
git check-ignore -v .agents/skills/Sympy-Skill/SKILL.md
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_current_fact_schemas.py
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
git diff --check
git diff --cached --check
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Reviewed `AGENTS.md`, `docs/PLAN.md`, current
  dependency files, and existing ignored `.agents/skills` layout.
- [x] (2026-05-23 JST) Confirmed the upstream SymPy skill consists of
  `SKILL.md` plus five `references/*.md` files, and the upstream repository is
  MIT licensed.
- [x] (2026-05-23 JST) Drafted this ExecPlan.
- [x] (2026-05-23 JST) Installed ignored local SymPy skill files under
  `.agents/skills/Sympy-Skill/`.
- [x] (2026-05-23 JST) Added `sympy>=1.14,<2` with `uv add`, resolving
  `sympy==1.14.0` and `mpmath==1.3.0` in `uv.lock`.
- [x] (2026-05-23 JST) Ran validation: `uv lock --check`, SymPy exact
  arithmetic smoke, skill file checks, git ignore check, clean-slate
  validator, current-fact schema validator, validator/test audit validator,
  unit tests, and diff checks.
- [x] (2026-05-23 JST) Completed review table.
- [x] (2026-05-23 JST) Ran mandatory review with
  `codex review --uncommitted`; no actionable defects were found.

## Decision Log

- Decision: Add SymPy as a normal project dependency, not only as an agent
  convenience package.
  Rationale: The user asked to add `sympy` to this repository for future SF6
  numeric-calculation work. Keeping it in `pyproject.toml` and `uv.lock` makes
  availability deterministic for approved tools.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep the SymPy skill under ignored `.agents/skills/`.
  Rationale: Existing project rules state `.agents/` remains ignored and that
  Codex skills are reviewer/developer tooling unless an approved ExecPlan makes
  them runtime dependencies. Installing the skill locally there supports agent
  use without changing application runtime behavior.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not add SF6 calculation APIs or answer behavior in this slice.
  Rationale: Adding dependency availability is separate from designing
  deterministic SF6 numeric tools and authority boundaries.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- SymPy availability does not by itself make any SF6 numeric answer valid.
  Numeric answers still require approved deterministic tools and reviewed data.
- Future calculation tools must still be planned separately before they change
  runtime behavior, schemas, CLI, or answer mode.
- The ignored local skill is not part of git-tracked project state.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Deterministic numeric tool availability | Added SymPy dependency and locked transitive `mpmath` | `pyproject.toml`, `uv.lock` | `uv lock --check`; SymPy exact arithmetic smoke | Pass | None | None | Dependency only; no SF6 authority or answer behavior added |
| Reviewer/developer skill boundary | Installed SymPy skill under ignored `.agents/skills/Sympy-Skill/` with references and MIT license | ignored `.agents/skills/Sympy-Skill/` | file existence checks; `git check-ignore -v .agents/skills/Sympy-Skill/SKILL.md` | Pass | None | None | Ignored skill is local tool state, not tracked project state |
| Privacy and schema boundaries | Preserved current public/private and schema surfaces | no schema/data changes | `validate_clean_slate.py`; `validate_current_fact_schemas.py`; `validate_validator_test_audit.py`; unit tests | Pass | None | None | Future calculation tools still need separate ExecPlan |
| Whitespace and worktree hygiene | Checked diff formatting and final status | tracked changed files only | `git diff --check`; `git diff --cached --check`; `git status --short --branch` | Pass | None | None | `.agents/`, `.local/`, `.venv/`, caches remain ignored |
