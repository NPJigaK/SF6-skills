# Image-aware Japanese Article Ingest Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-02 |
| Timezone | Asia/Tokyo |
| Issue | #41 |
| Source | `≪スト6≫読み合いに勝つコツ「読み合いをシンプルに作る」` |
| Source URL | https://note.com/mizen5/n/n1f61c8308a4d |
| Source artifact | `knowledge/sources/articles/mizen-2025-simple-yomi.md` |
| Claims artifact | `knowledge/evidence/claims/mizen-2025-simple-yomi.claims.md` |
| Review artifact | `knowledge/review/unresolved/mizen-2025-simple-yomi.review.md` |

## Tooling

- Hermes profile checked: `sf6ingest`.
- Hermes version: Hermes Agent v0.12.0 (2026.4.30).
- `hermes doctor` result summary: browser tool available; vision tool unavailable; OpenAI Codex provider auth not logged in for this profile.
- Article page and image URLs were observed through the maintainer environment, but no screenshots or copied image assets were stored in the repository.
- Hermes memory, browser state, sessions, and profile state are not canonical SF6 knowledge.

## Method

This run reused the existing Mizen article artifacts from the Hermes-assisted ingest pilot and added an image-aware observation pass.

The goal was not to prove that the images establish accepted strategy knowledge. The goal was to test whether image-derived observations can be captured safely as review-only repo artifacts.

## Visual Observation Summary

The article contains several embedded visual examples around the discussion of simplified mixup structures. At a high level, the observed visuals support the article's presentation of:

- a non-SF6 analogy image near the initial discussion of multi-option decision structures;
- a command-grab okizeme payoff table;
- an invincible reversal disruption table for that command-grab / strike structure;
- a throw / shimmy payoff table for non-command-grab okizeme;
- a backdash or jump disruption table for the throw / shimmy structure;
- alternate simplified-pair tables based on observed opponent defensive tendencies.

The observed SF6-focused visuals support the article's presentation of:

- command-grab okizeme as a simplified command grab / strike structure;
- invincible reversal or Drive Reversal style options as additional defensive options that can disrupt that simplified structure;
- throw / shimmy structures for non-command-grab okizeme;
- backdash or jump as escape options that can change whether throw / shimmy is a sufficient structure;
- switching the simplified pair based on observed opponent defensive habits.

These observations are source-local and visual-contextual. They are not accepted curated knowledge, final public answer evidence, exact current facts, or proof of current setup validity.

## Cases

| Check | Expected | Result | Notes |
|---|---|---|---|
| Images observed at high level | Identify source images without copying them into repo. | Pass | Embedded visual examples were observed and summarized at a high level. |
| Images stored in repo | No screenshots or copied image assets. | Pass | No image files were added. |
| Image-derived claim handling | Route visual statement to observation / needs_review. | Pass | Added one `observation` candidate claim with `review_status` set to `needs_review`. |
| Unclear readings | Keep ambiguity explicit. | Pass | Report states Hermes vision was unavailable and does not claim full visual extraction. |
| Curated promotion | No image-derived claim enters `knowledge/curated/`. | Pass | No curated pages changed. |
| Generated references | No generated knowledge update from image observations. | Pass | Generated references remain derived from curated knowledge only. |
| State boundary | No Hermes/browser/vision state in repo. | Pass | No profile, session, browser cache, screenshot, or credential artifact was added. |

## Findings

- Image observation adds useful context for the article's structure because the diagrams make the "main two options plus other disruptive option" framing easier to identify.
- The image-aware pass did not justify curated promotion. It only added a review-only observation claim.
- Hermes `sf6ingest` still needs provider/runtime readiness for full non-interactive ingest. `hermes doctor` also reported vision unavailable, so this run records tool limits instead of claiming complete vision extraction.
- Existing ingest artifact validation accepted the updated source, claim, and review artifacts without requiring copied images or large excerpts.

## Follow-ups

- Keep image-derived article ingest conservative: observation first, review before promotion.
- If full browser/vision extraction is needed later, verify the toolchain separately and record it as a smoke run before using it for broad ingest.
