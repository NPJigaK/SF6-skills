# Ingest Article Workflow

Use this workflow to turn an article, guide, note, interview, changelog summary, or maintainer research note into reviewable v2 claim candidates.

Article ingest does not automatically create accepted knowledge. It creates source metadata, extracted claims, and review notes that can be accepted or rejected by `workflows/review-claims.md`.

## Boundaries

- Do not store full copyrighted articles by default.
- Do not copy long verbatim passages into the repo.
- Do not put exact current move values into `knowledge/curated/`.
- Do not use legacy source tiers, bracket labels, or old canonical taxonomies.
- Do not treat a community article as final authority for current frame values when `data/exports/` covers the fact.

## Inputs

Record these before extracting claims:

- Source title.
- Source URL or local path.
- Author or publisher when available.
- Accessed or captured timestamp.
- Source kind using `contracts/source-metadata.schema.json`: `official`, `reproducible_observation`, `maintained_third_party`, `community`, `maintainer_note`, or `unknown`.
- Source role, such as `primary_rule_source`, `strategy_explanation`, `matchup_note`, `patch_context`, `community_term_source`, or `background_context`.
- Known patch, roster, character, mode, or matchup scope.

## Extraction Flow

1. Read the input material and write a short neutral source summary.
2. Search existing `knowledge/curated/` and `knowledge/review/` for the same topic or claim.
3. Extract atomic claims. Split mixed claims so each candidate has one statement and one evidence boundary.
4. Assign `claim_kind` from `contracts/claim.schema.json`: `stable_concept`, `strategy_or_matchup`, `observation`, `current_fact`, or `unresolved`.
5. Create v2 evidence metadata for each claim.
6. Mark exact current facts as `current_fact` and route them to the frame-data workflow unless the claim is only contextual evidence.
7. Mark claims as `unresolved` when the source is vague, patch-sensitive, contradicted, or missing reproducible evidence.
8. Keep the article summary and extracted candidates in `knowledge/review/` until claim review accepts them.

## Evidence Metadata

Every candidate claim must carry these fields from `contracts/source-metadata.schema.json`:

- `source_kind`
- `source_role`
- `evidence_basis`
- `verification_state`
- `confidence`
- `volatility`
- `patch_sensitivity`
- `review_status`
- `source_refs`
- `review_after`

Use `review_status = needs_review` for newly ingested claims unless a maintainer is only recording a rejected duplicate.

## Candidate Claim Shape

Use `contracts/claim.schema.json` as the machine-readable contract. A Markdown review note may mirror the same fields when JSON is not practical.

```json
{
  "id": "candidate-short-id",
  "claim_kind": "strategy_or_matchup",
  "statement": "One atomic statement from the source.",
  "scope": "Character, matchup, patch, mode, or general scope.",
  "evidence": {
    "source_kind": "maintained_third_party",
    "source_role": "strategy_explanation",
    "evidence_basis": [
      "source_summary",
      "specific_section_or_timestamp"
    ],
    "verification_state": "unverified",
    "confidence": 0.5,
    "volatility": "patch_sensitive",
    "patch_sensitivity": "medium",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Source title",
        "url": "https://example.invalid/article",
        "accessed_at": "2026-04-30"
      }
    ],
    "review_after": null
  },
  "notes": "Short paraphrase, conflicts, and follow-up checks."
}
```

## Japanese Sources

For Japanese SF6 sources:

- Preserve the original Japanese title and source URL.
- Summarize in Japanese by default.
- Optionally include an English maintainer summary when useful.
- Extract claims into repo artifacts, not private agent memory.
- Do not store full article text.
- Use short excerpts only when necessary for review.
- Normalize Japanese terminology cautiously.
- Do not turn Japanese community shorthand into official terminology unless supported.
- Do not promote patch-sensitive setup claims to curated knowledge without current evidence.

Common Japanese terms and shorthand such as `しゃがみ中P`, `屈中P`, `2MP`, `ガード硬直差`, `確反`, `起き攻め`, and `シミー` may require normalization before exact current fact lookup. If the source or claim cannot be confidently mapped to a packaged character, move, and field, keep it in review or route it to the appropriate current-fact workflow.

## Routing Rules

- Accepted stable concepts go through claim review before entering `knowledge/curated/`.
- Strategy or matchup claims stay in review until checked against scope, patch sensitivity, and conflicting evidence.
- Exact current frame values, costs, roster facts, and patch labels are not accepted into curated knowledge; route them to `data/exports/`, `data/roster/`, or the relevant workflow.
- Community terms may be kept as terminology only when the source role and evidence boundary make that status clear.
- Conflicting claims remain in `knowledge/review/` with `verification_state = conflicting`.

## Ingest Report

End the ingest with:

- Source metadata summary.
- Candidate claim count by `claim_kind`.
- Duplicate claims found.
- Claims routed to current-fact workflows.
- Claims that need reproduction, official confirmation, or matchup review.
