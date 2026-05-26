# SF6 Knowledge Coach

SF6 Knowledge Coach is a clean-slate local app for building a personal,
character-agnostic Street Fighter 6 coaching system.

JP is the initial active character package, not a global hardcoded assumption.
The repository keeps reviewed public current-fact artifacts in Git and keeps
private user profile data, training logs, answer logs, raw media, and private
overlays out of Git.

## Current State

This branch is intentionally replacing the previous SF6 Knowledge Agent Kit
implementation. Legacy runtime, package, workflow, validator, distribution,
adapter, and generated-code surfaces are removed instead of restored.

The active architecture contract is [docs/PLAN.md](docs/PLAN.md). Multi-file
work after the initial scaffold must be performed through smaller ExecPlans
under [docs/execplans/](docs/execplans/).

## What Exists Now

- `AGENTS.md`: repository rules for agents and maintainers.
- `docs/PLAN.md`: clean-slate architecture contract.
- `docs/execplans/`: scoped execution plans for implementation slices.
- `data/current-facts/`: reviewed current-fact candidate/source-record/export
  artifacts.
- `src/sf6_knowledge_coach/`: minimal deterministic local tools.
- `tests/`: clean-slate tests and validation.

## Local Commands

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
```

Use the CLI without installing:

```bash
PYTHONPATH=src python -m sf6_knowledge_coach.cli context resolve "JPの5LPはガードで何F？"
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer verify "JPの5LPはガードで何F？"
```

`search` and `current lookup` are explicitly unavailable after legacy raw-backed
current-fact retirement. Exact numeric/current-fact answers hold until a later
reviewed scalar-safe or non-scalar disposition contract exists.

After installing the package, the console command is `sf6`.

## Hard Boundaries

- Numeric/current-fact answers must use deterministic tools and tables.
- Prose search or model memory must not be used as authority for frame,
  damage, scaling, punish, combo damage, patch delta, or current move facts.
- Candidate, observed, deprecated, or rejected knowledge must not be used as
  definitive daily-answer evidence.
- Daily answer mode is local and read-only for public repo knowledge/data.
- Web access belongs to update/research modes only.
- Discord, VLM, private vault, private overlay DB, and video pipeline work are
  deferred to later ExecPlans.
