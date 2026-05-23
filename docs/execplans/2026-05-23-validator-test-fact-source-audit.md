# Validator Test Fact Source Audit

Status: Implementation complete; review pending.

## Purpose

Audit every current test and validator for evidence basis before JSON Schema
redesign.

The rule is evidence-first: do not change validators merely to fit generated
artifacts. If a validator cannot be tied to source data, policy, or a privacy
boundary, it must be marked as a review risk rather than treated as proof.

## Scope

Included:

- inventory every current `tests/test_*.py` and `tests/validation/*.py` file,
  including this audit validator itself;
- classify each file by evidence class;
- record which checks are source-derived, policy-derived, synthetic-contract,
  privacy-boundary, or artifact-consistency only;
- add a small audit validator that fails when new test/validator files are not
  represented in the audit artifact;
- change CI to run every `tests/validation/validate_*.py` script so new
  validators are not silently skipped;
- add a concise AGENTS.md rule for evidence-first validators.

Excluded:

- do not implement schema/parser/retrieval/answer behavior;
- do not run live source acquisition in this audit;
- do not claim artifact-consistency validators prove source truth;
- do not promote official or SuperCombo data to numeric authority.

## Findings

- Current acquisition artifact validators are useful for integrity/privacy and
  local raw artifact consistency, but they are not themselves source truth.
- Current mapping/disposition/policy validators mostly prove internal
  consistency against reviewed artifacts. They must not be described as live
  source verification.
- Current CLI numeric smoke for `JP 5LP block_adv = -2` is supported by
  retained `data/exports/jp/official_raw.json` and the ignored local official
  acquisition artifact for JP, but it is still a smoke, not broad current-fact
  validation.
- JSON Schema redesign can start only if it treats these artifacts as reviewed
  inputs with known limits, not as parser/schema truth.

## Files

- `AGENTS.md`
- `.github/workflows/ci.yml`
- `docs/validator-audits/20260523-validator-test-fact-source-audit.md`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- `tests/validation/validate_validator_test_audit.py`
- `docs/execplans/2026-05-23-validator-test-fact-source-audit.md`

## Validation

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python tests/validation/validate_validator_test_audit.py
for script in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$script"; done
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
```

PLAN deviations: none.

## Remaining Risks

- Full live-source re-acquisition is still a separate update-mode task.
- This audit does not prove every SF6 value is semantically parsed correctly;
  it classifies validator evidence and blocks overclaiming.
