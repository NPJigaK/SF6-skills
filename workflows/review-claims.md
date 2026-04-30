# Review Claims Workflow

Use this workflow to decide whether review candidates become accepted v2 knowledge, remain under review, or are rejected.

Review is a separate step from article or video ingest. Ingest records evidence; review makes the repository decision.

## Review Inputs

- Candidate claims from `knowledge/review/`.
- Source metadata that follows `contracts/source-metadata.schema.json`.
- Claim records that follow `contracts/claim.schema.json` or equivalent Markdown fields.
- Existing accepted pages under `knowledge/curated/`.
- Exact current-fact exports under `data/exports/` when the claim touches move-specific current facts.
- Current roster source under `data/roster/current-character-roster.json` when the claim depends on roster membership.

## Decision Values

Use v2 metadata fields:

- `review_status = accepted`
- `review_status = needs_review`
- `review_status = rejected`
- `review_status = deprecated`

Use `verification_state` to explain evidence quality:

- `verified`
- `partially_verified`
- `unverified`
- `conflicting`
- `not_applicable`

Do not encode decisions with legacy source tiers, bracket labels, or old taxonomy terms.

## Review Flow

1. Read the candidate claim and source metadata.
2. Check whether the claim duplicates or conflicts with existing `knowledge/curated/` or `knowledge/review/` content.
3. Split mixed claims before deciding. One claim should not combine stable concept, matchup advice, current fact, and observation evidence.
4. Verify the evidence basis against the cited source refs.
5. Check volatility and patch sensitivity.
6. For exact current move values, compare against `data/exports/` and do not accept the value into curated knowledge.
7. For roster-dependent claims, compare against `data/roster/current-character-roster.json`.
8. Decide `accepted`, `needs_review`, `rejected`, or `deprecated`.
9. Update or create the smallest appropriate curated page only for accepted knowledge.
10. Preserve unresolved, rejected, or conflicting candidates in `knowledge/review/` with the decision reason.

## Acceptance Criteria

A claim may be accepted when all of these are true:

- The statement is atomic and scoped.
- The claim kind is one of the v2 values.
- The evidence metadata is complete.
- The source refs are reviewable.
- The confidence value is justified by the evidence basis.
- Patch-sensitive content has a clear boundary or review timing.
- The claim does not duplicate an existing accepted page without improving it.
- The claim does not put exact current frame values, costs, roster facts, or patch labels into curated knowledge.

## Curated Knowledge Rules

Accepted curated pages should:

- Prefer concise definitions, practical meaning, and boundaries.
- Include v2 evidence metadata.
- Avoid long examples that only restate the source.
- Avoid exact current move values.
- Link or refer to claim IDs when a page aggregates several reviewed claims.
- Keep generated adapter text out of `knowledge/curated/`; generation belongs to the knowledge-generation workflow or package.

## Rejection And Hold Rules

Keep `review_status = needs_review` when:

- The source is ambiguous.
- Evidence is only anecdotal.
- The claim needs reproduction.
- The claim depends on a patch, matchup, distance, input method, or roster state that is not pinned.
- Sources conflict and the conflict has not been resolved.

Use `review_status = rejected` when:

- The claim is false against accepted evidence.
- The claim is too vague to make reviewable.
- The source cannot be located.
- The claim duplicates accepted knowledge without adding useful scope or evidence.

Use `review_status = deprecated` when accepted knowledge was once valid but has been superseded.

## Review Report

End the review with:

- Accepted claim IDs and target curated paths.
- Claims left in review and the next check required.
- Rejected or deprecated claim IDs and reasons.
- Any exact current facts routed to frame-data or roster workflows.
- Any observations that remain separate source artifacts rather than accepted knowledge.
