---
name: grilling
description: Interview the user relentlessly about a plan, design, workflow, wiki change, raw/source ingest, tooling change, or SF6 knowledge-base maintenance decision. Use when the user asks to grill, stress-test, challenge, sharpen, or think through a plan before execution.
---

# Grilling

Interview the user relentlessly about the plan until there is a shared, concrete understanding.
Walk down the design tree one decision at a time. For each question, provide your recommended answer and why.

Ask one question at a time and wait for feedback before continuing. Multiple questions at once are hard to answer well.

If a question can be answered by inspecting the repository, inspect the repository instead of asking the user.

## SF6 repo context loading

Do not create or depend on `CONTEXT.md` for this repository. The canonical repo context is:

1. `AGENTS.md` for operating rules, layer boundaries, workflow dispatch, and source-traceability requirements.
2. `wiki/index.md` for the current navigation surface.
3. Relevant `wiki/` pages for compiled knowledge:
   - `wiki/sources/` for source summaries.
   - `wiki/concepts/`, `wiki/entities/`, and `wiki/syntheses/` for reusable knowledge.
   - `wiki/questions/` and `wiki/outputs/` for durable answers and reports.
   - `wiki/reviews/` for review notes, contradictions, stale claims, and refactor plans.
4. Relevant `raw/` package manifests, metadata, validation, and original captures only when source freshness, source authority, validation, or numeric facts matter.
5. Relevant `tools/` code or README files only when the plan changes capture, extraction, validation, lab automation, calculation, or derived-output generation.
6. Existing repo-local skills under `.agents/skills/` when the plan maps to a declared workflow.

Use `rg` or `rg --files` for local discovery. Prefer reading the smallest relevant set of files instead of loading whole directories.

## Boundary rules

- Treat `raw/` as source material. Do not propose editing it unless `AGENTS.md` and the raw package manifest allow the specific update.
- Do not invent SF6 facts, frame values, route ledgers, validation states, or source freshness from memory.
- For exact damage, gauge, juggle, distance, timing proof, fixture, prediction, postmortem, or rule-promotion plans, read `$sf6-calculation-grounding` and `wiki/concepts/combo-damage-ledger-protocol.md`.
- For wiki structure, ingest, durable output, query, health-check, raw capture, or capture-review plans, route through the matching repo-local `sf6-*` skill.
- Keep source facts, derived facts, synthesis, inference, and hypothesis separate.
- When a proposed change would produce durable wiki content, include how `wiki/index.md` and `wiki/log.md` will be updated.

## Question style

Prefer questions that force a decision:

- "Which layer owns this: `raw/`, `wiki/`, `tools/`, or generated output?"
- "What evidence would make this answer source-backed instead of inferred?"
- "What would be unsafe to automate here?"
- "What existing page or tool should this update instead of creating something new?"
- "What exact stop condition prevents us from over-claiming?"

When the likely answer is clear from the repository, state the recommended answer and ask only for confirmation of the remaining trade-off.
