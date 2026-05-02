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
- `hermes doctor` result summary during the original #41 run: browser tool available; vision tool unavailable.
- Article page image URLs were discovered through the maintainer environment.
- The images were inspected through a repo-external temporary vision-capable path, not through Hermes vision.
- No screenshots, copied image assets, or temporary image files were stored in the repository.
- Hermes memory, browser state, sessions, and profile state are not canonical SF6 knowledge.

## Method

This run reused the existing Mizen article artifacts from the Hermes-assisted ingest pilot and added an image-aware observation pass.

The goal was not to prove that the images establish accepted strategy knowledge. The goal was to test whether image-derived observations can be inspected, recorded with uncertainty, and captured safely as review-only repo artifacts.

## Visual Observation Summary

The article contains several embedded visual examples around the discussion of simplified mixup structures. The observed image set includes:

| Image | How Observed | Readable Elements | Result | Confidence | Notes |
|---|---|---|---|---|---|
| 1 | Repo-external temporary image inspection | 打撃, コマ投げ, ガード, バクステ(ジャンプ), success/failure markers | Pass | medium | Shows a two-option command grab / strike structure against guard and backdash/jump. |
| 2 | Repo-external temporary image inspection | 打撃, コマ投げ, 様子見, ガード, バクステ(ジャンプ), 無敵技(Dリバ), success/failure markers | Pass | medium | Adds a third offensive option and a reversal/Drive Reversal style defensive row. |
| 3 | Repo-external temporary image inspection | 投げ, シミー, ガード, 遅らせグラ(無敵技), success/failure markers | Pass | medium | Shows throw / shimmy as a simplified structure against guard and delayed throw-tech or invincible response. |
| 4 | Repo-external temporary image inspection | 投げ, シミー, 打撃, ガード, 遅らせグラ(無敵技), バクステ(ジャンプ), success/failure markers | Pass | medium | Adds strike and backdash/jump disruption to the throw / shimmy structure. |
| 5 | Repo-external temporary image inspection | Highlighted ガード and バクステ(ジャンプ), with 投げ and 打撃 emphasized while シミー is faded | Pass | medium | Visually narrows the active simplified pair based on a guard/backdash tendency. |
| 6 | Repo-external temporary image inspection | Highlighted 遅らせグラ(無敵技) and バクステ(ジャンプ), with シミー and 打撃 emphasized while 投げ is faded | Pass | medium | Visually narrows the active simplified pair based on delayed-tech/reversal and backdash/jump tendencies. |

At a high level, the observed visuals support the article's presentation of:

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
| Images observed at image level | Identify source images without copying them into repo. | Pass | Six embedded visual examples were inspected and summarized with image-level notes. |
| Images stored in repo | No screenshots or copied image assets. | Pass | No image files were added. |
| Image-derived claim handling | Route visual statement to observation / needs_review. | Pass | Added one `observation` candidate claim with `review_status` set to `needs_review`. |
| Unclear readings | Keep ambiguity explicit. | Pass | Report states Hermes vision was unavailable and separates repo-external image inspection from Hermes vision extraction. |
| Curated promotion | No image-derived claim enters `knowledge/curated/`. | Pass | No curated pages changed. |
| Generated references | No generated knowledge update from image observations. | Pass | Generated references remain derived from curated knowledge only. |
| State boundary | No Hermes/browser/vision state in repo. | Pass | No profile, session, browser cache, screenshot, or credential artifact was added. |

## Findings

- Image observation adds useful context for the article's structure because the diagrams make the "main two options plus other disruptive option" framing easier to identify.
- The image-aware pass did not justify curated promotion. It only added a review-only observation claim.
- Hermes `sf6ingest` had browser tooling available, but Hermes vision was unavailable during this run. The actual image reading used a repo-external temporary vision-capable path, so this run must not be cited as successful Hermes vision extraction.
- Existing ingest artifact validation accepted the updated source, claim, and review artifacts without requiring copied images or large excerpts.

## Follow-ups

- Keep image-derived article ingest conservative: observation first, review before promotion.
- If full browser/vision extraction is needed later, verify the toolchain separately and record it as a smoke run before using it for broad ingest.
