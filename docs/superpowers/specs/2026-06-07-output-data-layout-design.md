# Output Data Layout Migration Design

## Goal

Reorganize `wiki/outputs/data/` before more generated datasets are added, so the first directory level consistently represents the data family rather than a mixture of source, processing stage, and data family.

## Target Layout

```text
wiki/outputs/data/
  frame-data/
    official/<character>/
    supercombo/<character>/
    official-supercombo-enriched/<character>/
  battle-change/
    official/
```

## Rationale

Readers and tools most often start from the question "which kind of data is this?" For Street Fighter 6 frame data, the official Capcom rows, SuperCombo-derived rows, and official-plus-SuperCombo enriched rows are variants of the same data family. Keeping them under `frame-data/` makes comparisons and future additions easier to discover.

The previous layout mixed axes:

- `frame-data/<character>/` used data family but implicitly meant Capcom official.
- `supercombo/frame-data/<character>/` used source first.
- `enriched/frame-data/<character>/` used processing stage first.
- `battle-change/official/` used data family first.

The migration makes `battle-change/official/` the pattern rather than the exception.

## Compatibility Policy

This repository is still early enough that old output paths should not be preserved as compatibility aliases. The migration updates generators, validators, audit scripts, README, wiki index, synthesis pages, source pages, reports, and question citations to the new contract. Git history remains the rollback mechanism.

## Affected Contracts

- Official frame-data outputs move from `wiki/outputs/data/frame-data/<character>/` to `wiki/outputs/data/frame-data/official/<character>/`.
- SuperCombo frame-data outputs move from `wiki/outputs/data/supercombo/frame-data/<character>/` to `wiki/outputs/data/frame-data/supercombo/<character>/`.
- Official + SuperCombo enriched outputs move from `wiki/outputs/data/enriched/frame-data/<character>/` to `wiki/outputs/data/frame-data/official-supercombo-enriched/<character>/`.
- Battle Change outputs remain at `wiki/outputs/data/battle-change/official/`.

## Implementation Notes

- Move directories with Git-aware filesystem operations so history is reviewable.
- Update path constants at script call sites rather than introducing a broad path abstraction prematurely.
- Update markdown citations in reader-facing wiki pages.
- Verify by running existing focused tests and by searching for stale old path prefixes.

## Verification

- `python -m pytest tools/test_supercombo_frame_comparison.py tools/test_supercombo_enrichment_review.py tools/test_supercombo_validation_integrity.py tools/test_capcom_capture_guards.py tools/test_battle_change_validation.py`
- `python tools/validate_capcom_frame_data.py --character-slug ryu`
- `python tools/extract_capcom_frame_data.py --character-slug ryu`
- `python tools/extract_supercombo_frame_data.py --character-slug ryu`
- `python tools/build_official_supercombo_enriched_data.py --character-slug ryu`
- `rg "wiki/outputs/data/(supercombo/frame-data|enriched/frame-data|frame-data/[a-z0-9_]+/)" README.md tools wiki`
