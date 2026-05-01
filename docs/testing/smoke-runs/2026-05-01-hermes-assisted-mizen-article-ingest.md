# Hermes-assisted Japanese Article Ingest Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-01 |
| Timezone | Asia/Tokyo |
| OS | WSL2 on Linux |
| Hermes version | Hermes Agent v0.12.0 (2026.4.30) |
| Issue | #38 |
| Source | `≪スト6≫読み合いに勝つコツ「読み合いをシンプルに作る」` |
| Source URL | https://note.com/mizen5/n/n1f61c8308a4d |
| Repo commit before run | `f0b60ec` |
| Final repo artifacts | `knowledge/sources/articles/mizen-2025-simple-yomi.md`, `knowledge/evidence/claims/mizen-2025-simple-yomi.claims.md`, `knowledge/review/unresolved/mizen-2025-simple-yomi.review.md` |

## Setup

- Created a dedicated Hermes profile candidate: `sf6ingest`.
- `sf6ingest` profile path: `/home/devkey/.hermes/profiles/sf6ingest`.
- `sf6ingest` had memory and user profile memory disabled in config.
- `sf6ingest` had curator disabled in config.
- `sf6ingest` could discover `sf6-agent` through `skills.external_dirs`.
- `sf6ingest` could not run the Codex runtime because that profile did not yet have its own stored Codex credentials.
- Actual Hermes-assisted run used the existing isolated `sf6smoke` profile.
- `sf6smoke` profile state lives outside this repository.
- Hermes was not used as canonical memory.

## Method

Hermes was prompted to assist with the article ingest workflow without modifying files or storing memory. The prompt supplied:

- the source title, author, publication date, and URL;
- a short neutral summary of the article;
- the requirement to follow `workflows/ingest-article.md` boundaries;
- the requirement to avoid full article text, exact current values, and curated promotion;
- the requirement to identify claim kinds, volatility, patch sensitivity, review-only boundaries, and workflow friction.

Hermes returned a review-only source/claim/review proposal. The proposal was manually rewritten into the repository's current artifact paths and metadata style.

## Cases

| Check | Expected | Result | Notes |
|---|---|---|---|
| Follows ingest workflow | Uses source -> claims -> review shape. | Pass | Hermes proposed source metadata, candidate claims, and a review note. |
| Source summary shape | Produces a short summary without full article text. | Pass | Final repo artifact stores summary only and no verbatim article excerpt. |
| Claim decomposition | Splits high-level strategy framing from setup-specific hold conditions. | Pass | Final claims separate general strategy framing, okizeme examples, and unresolved setup validity. |
| Numeric/current facts | Avoids exact current values. | Pass | The source did not require exact current values; final artifacts store none. |
| Review-only boundary | Does not promote claims to curated knowledge. | Pass | Final artifacts stay in source, claims, and unresolved review surfaces. |
| Repo state | No Hermes profile, memory, session, cron, credential material, or local state files are created in the repo. | Pass | Hermes state paths remained under `/home/devkey/.hermes/profiles/`. |
| Memory boundary | Hermes memory is not canonical. | Pass | Hermes explicitly identified memory as non-canonical, and final output is repo artifact text. |

## Findings

- Hermes was useful for quickly proposing claim categories and identifying which parts should remain review-only.
- Hermes proposed noncanonical artifact paths, so maintainer review still needed to normalize outputs into the repo's actual `knowledge/sources/`, `knowledge/evidence/claims/`, and `knowledge/review/unresolved/` layout.
- Hermes runtime authentication is profile-scoped. A newly cloned ingest profile may need its own provider authentication before non-interactive runs.
- This run did not validate Hermes browser/vision extraction from article images. Hermes assisted claim decomposition from maintainer-provided source context; image-aware ingest remains a separate follow-up.
- The canonical procedure remains `workflows/ingest-article.md`; Hermes is only a maintainer harness.
- The lack of dedicated validators for source and evidence claim artifacts remains the main workflow gap after this pilot.

## Follow-ups

- Add validators for source and evidence claim artifacts.
- Consider a reusable Hermes prompt template for Japanese article ingest once the source/claim validator shape is stable.
