# Value-Shape Source Review Resolution

Status: Implementation complete; review pending.

## Purpose

Resolve the 3 `blocked_pending_source_review` value-shape items from the
20260521T025403Z disposition artifact by recording source-review decisions.

## Scope

Create public Markdown/JSON source-review summaries and a validator. Do not
change schema, parser, normalized export, retrieval, answer behavior, source
acquisition, or authority status.

## Decisions

- Official active-frame malformed-looking values are source-confirmed raw
  values and need parse-rule policy before schema work.
- Official note-bearing move names are source-confirmed raw move labels and can
  be represented raw-only until a later move-identity split is designed.
- SuperCombo `Throw Range / Hurtbox` is a source-native paired value. It can be
  mapped as SuperCombo-specific enrichment with later pair parsing, not as
  official numeric authority.

## Files

- `docs/source-reviews/20260521T025403Z-value-shape-blocked-source-review.md`
- `data/source-reviews/20260521T025403Z-value-shape-blocked-source-review-summary.json`
- `tests/validation/validate_value_shape_source_review.py`
- `docs/execplans/2026-05-23-value-shape-source-review-resolution.md`

## Validation

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_source_review.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_disposition.py
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

PLAN deviations: none.

## Remaining Risks

- The disposition and SuperCombo mapping artifacts still need a follow-up
  update to consume these source-review resolutions.
- Parser/classifier and enum policies remain unimplemented.
