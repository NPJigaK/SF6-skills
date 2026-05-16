# Repository Directory Architecture Review

## Executive Summary

- `data/raw` に published manifest から参照されない SuperCombo raw snapshot が4件残っており、`ingest/frame_data/README.md` の「published exportsを再現する最小raw snapshots」という設計意図と緊張している。raw snapshot最小性をCIで検査する必要がある。
- `knowledge/` の evidence/review/curated 境界は文書上は堅いが、`source_refs` や current-fact candidate の禁止情報が機械可読な authority role として十分に分離されていない。将来の検索・生成器が review-only 数値や unresolved provenance を authority と誤読するリスクがある。
- `tests/validation/` は境界保護に効いている一方、PowerShell validators がドメイン別の文字列・ファイル存在チェックを多く抱え、schema/contract との重複と validator sprawl が始まっている。
- `docs/testing/video-analysis-calibration/` は raw media を置かず review-only 境界を守っているが、実行済み calibration report の意味論を検査する validator は薄い。個別レポートの知見を workflow/eval/validator に変換する出口管理が次の課題。
- public `skills/sf6-agent/` と repo-local Hermes/Codex tooling の境界は概ね守られている。主な残リスクは現物混入ではなく、将来の generator/installer/pack 運用で provenance と local-state 境界が曖昧になること。
- validation entrypoint `tests/validation/run-all.ps1` は生成系 preflight を含むためCIでは有用だが、docs-only監査やレビュー確認では「非破壊チェック」と「生成ビルド」が分離されていない。

## Scope And Method

- 対象commit: `c028ab5c9b2f82aa8e1678f1a78d784f5208972a`
- 対象branch: #196 merge後の latest `main`
- 作業branch: `v2.6/directory-architecture-audit`
- GitHub precondition: PR #196 は `2026-05-15T23:42:32Z` に merged。監査開始時点で open PR はなし。
- 新規planning issue: #197 `[v2.6 planning] Directory-level architecture audit and refactoring roadmap`
- Directory inventory: `git ls-files` 989件から owning directories 190件、parent/module directories 262件を生成。
- Inventory artifact: `docs/architecture/reviews/repo-directory-inventory-20260516.md`
- Review method: 6つの sub-review cluster とローカル sequential review を統合した。sub-review cluster は root/docs/contracts/validators、data、ingest、knowledge/evals、public adapter、packages/packs を対象にした。
- GitHub issue/PR lookup: `gh issue list` / `gh pr list` を module path ごとに実行。closed issue/PR は historical context としてのみ扱い、現行docsやopen issueが依存していない限り active source とは扱わない。
- Local history lookup: `git log --oneline -- <directory>` を top-level moduleごとに確認。

変更していないもの:

- runtime behavior
- generated references
- public `skills/sf6-agent`
- `official_raw`
- `data/raw`, `data/exports`, `data/roster`
- raw media, frames, screenshots, transcripts, local/Hermes state, credentials
- validators, workflows, packages, CI implementation

Limitations:

- 外部Webの現行CAPCOM/SuperCombo状態は確認していない。この監査は repo architecture と checked-in surfaces の監査である。
- 全GitHub issue本文を網羅読解したわけではなく、path/title検索と関連PR履歴に基づく。
- by-directory findings は 190 owning directories を全て inventory で列挙し、同型の character/snapshot/runtime directories は main report 内で grouped pattern として統合した。

## Directory Inventory Summary

- `git ls-files`: 989 tracked files
- Owning directories: 190
- Parent/module directories: 262
- Root-level files: `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`, `mise.lock`, `mise.toml`
- Top-level tracked modules: `.github`, `contracts`, `data`, `docs`, `evals`, `ingest`, `knowledge`, `packages`, `packs`, `skills`, `tests`, `workflows`

Notable grouped modules:

- `data/exports/<character_slug>`: 29 owning dirs, 13 files each
- `data/raw/official/<character_slug>/<snapshot_id>`: 29 owning dirs
- `data/raw/supercombo/<character_slug>/<snapshot_id>`: 33 owning dirs
- `skills/sf6-agent/assets/frame-current/published/<character_slug>`: 29 owning dirs
- `ingest/frame_data/config/registry` and `ingest/frame_data/config/binding_policy`: character-wise config modules

Skipped directories: none.

## Cross-Directory Architecture Map

### Major Repo Subsystems

- Public answer adapter: `skills/sf6-agent/`
- Canonical knowledge lifecycle: `knowledge/sources`, `knowledge/evidence`, `knowledge/review`, `knowledge/curated`
- Exact current-fact authority: `data/exports/`, `data/roster/`
- Frame data ingestion and publishing: `ingest/frame_data/`
- Contracts and schemas: `contracts/`
- Answer-quality evaluation: `evals/`
- Validation and CI gates: `tests/validation/`, `.github/workflows/`
- Maintainer workflows: `workflows/`
- Packaging/generation/install tooling: `packages/`
- Repo-local Hermes/Codex support: `packs/hermes-sf6/`, `packs/codex-hermes-sf6/`
- Calibration and smoke evidence: `docs/testing/`

### Boundaries

Fact: `AGENTS.md:11-16` defines `knowledge/`, `data/exports/`, `data/roster/`, `contracts/`, `workflows/`, `evals/`, and selected `skills/sf6-agent` policy files as canonical surfaces. `AGENTS.md:20-24` defines generated references and frame-current assets as derived. `AGENTS.md:28-31` says exact move-specific current facts belong in `data/exports/` and generated frame-current assets, while `data/raw`, `data/normalized`, and `*_manual_review.*` are not final public-answer evidence.

Fact: `skills/sf6-agent/SKILL.md:12-15` keeps generated concept references, frame-current assets, and hand-written adapter behavior separate. `skills/sf6-agent/references/current-fact-policy.md:19-31` requires `official_raw.json` first and prohibits supplemental enrichment override.

Fact: `docs/architecture/harness-and-distribution-roles.md:23-37` separates repo-local maintainer surfaces from public answer distribution. `docs/architecture/codex-hermes-bridge-policy.md:152-167` treats Hermes output as draft input and exact current facts as grounded in current-fact authority surfaces.

### Data/Control Flow

```text
external source metadata / video observation
  -> knowledge/sources
  -> knowledge/evidence
  -> knowledge/review
  -> knowledge/curated
  -> packages/knowledge-generation
  -> skills/sf6-agent/references/generated-*

official / SuperCombo frame pages
  -> ingest/frame_data fetch raw snapshot
  -> ingest/frame_data parse normalized run
  -> ingest/frame_data publish data/exports
  -> packages/skill-packaging build-frame-current-runtime-assets
  -> skills/sf6-agent/assets/frame-current
```

Authority surfaces:

- `data/exports/<character_slug>/official_raw.json`: primary exact current move fact authority.
- `data/exports/<character_slug>/derived_metrics.json`: derived from `official_raw`.
- `data/exports/<character_slug>/supercombo_enrichment.json`: enrichment-only, official-safe subset.
- `data/roster/current-character-roster.json`: roster/current-fact generation authority.
- `knowledge/curated/*`: accepted stable/conceptual knowledge only, not exact current frame values.

Generated surfaces:

- `skills/sf6-agent/references/generated-*`: generated from `knowledge/curated`.
- `skills/sf6-agent/assets/frame-current/*`: generated from `data/exports` and `data/roster`.
- `skills/sf6-agent/assets/normalization/*`: generated from `data/aliases`.
- `.dist/*`: derived distribution output, not checked into this audit.

Validation surfaces:

- `.github/workflows/v2-validation.yml` runs maintainer toolchain lock checks on Linux and `tests/validation/run-all.ps1` on Windows.
- `tests/validation/run-all.ps1:29-64` runs generation preflight and 28 validators.
- `tests/validation/validate-frame-current-assets.ps1:107-113` forbids CSV/manual-review files in runtime frame-current assets and verifies expected inventory.
- `tests/validation/validate-current-fact-boundaries.ps1:31-43` prevents exact current-fact patterns from leaking into curated/generated knowledge.
- `tests/validation/validate-no-video-binary-assets.ps1:11-35` blocks media/cache binaries in repo/public surfaces.

## Per-Directory Findings

The inventory artifact lists every owning directory. This table records the architecture finding for each directory unit; wildcard rows cover every concrete owning directory in that family, with no skipped directories.

| Directory path | Responsibility | Key files | Architectural concerns | Severity | Recommended action | Confidence |
|---|---|---|---|---|---|---|
| `.` | Repo policy, entrypoint, toolchain pins | `AGENTS.md`, `README.md`, `mise.toml`, `mise.lock` | Canonical/derived boundaries are clear, but `data/exports/` wording can be too broad because manual-review sidecars live under the same subtree. | Medium | Clarify exact authority granularity in future policy docs. | High |
| `.github` | Renovate configuration and helper script | `renovate.json`, `renovate-mise-lock.sh` | Toolchain automation is separated from runtime, but update policy depends on Renovate/post-upgrade task behavior. | Low | Keep Renovate actions pinned and reviewed with lockfile changes. | Medium |
| `.github/workflows` | CI validation entrypoints | `v2-validation.yml`, `renovate.yml` | CI validates important boundaries but `run-all.ps1` is mutating by design. | Medium | Consider a non-mutating validation profile or explicitly document mutation. | High |
| `contracts` | Schemas and artifact contracts | `*.schema.json`, `frame-current-runtime-assets.md`, `evidence-gate.md` | Contracts exist but some validators encode domain rules outside schema. | Medium | Move repeated structural rules into schema/contract where practical. | High |
| `data/aliases` | Query normalization source | `README.md`, `ja-query-fixtures.json` | Boundary is clear; coverage is intentionally minimal. | Low | Expand only with validator-backed alias lifecycle. | High |
| `data/exports/<character_slug>` | Published exact current-fact/export surface for 29 characters | `official_raw.*`, `derived_metrics.*`, `supercombo_enrichment.*`, `*_manual_review.*`, `snapshot_manifest.json` | Main JSON authority, CSV sidecars, and manual-review rows coexist. Directory-level authority wording can cause misuse. | Medium | Add `data/exports/README.md` documenting dataset roles and non-authority sidecars. | High |
| `data/external-frame-atlas/evaluation` | Metadata-only external visual source evaluation | `README.md`, `source-evaluation-matrix.json` | Good non-fetch boundary; future acquisition work could confuse this with `data/raw`. | Low | Add parent `data/external-frame-atlas/README.md` before any cache workflow. | High |
| `data/raw/official/<character_slug>/<snapshot_id>` | Official raw HTML snapshots supporting exports | `page.html`, `metadata.json` | Official raw set matches roster/exports, but raw snapshot hash verification is not enforced on load. | Medium | Add raw metadata hash/byte-count validation in ingest load path. | Medium |
| `data/raw/supercombo/<character_slug>/<snapshot_id>` | SuperCombo raw HTML snapshots supporting enrichment | `page.html`, `metadata.json` | 4 snapshot dirs are not referenced by current published manifests. | High | Add raw snapshot minimality validator or explicit retention policy. | High |
| `data/roster` | Canonical current roster source | `current-character-roster.json`, `README.md` | Good authority surface; roster/source schema enforcement is split between validators and ingest code. | Medium | Narrow ingest config model and keep roster validator as repo guard. | High |
| `data/toolchain` | Toolchain metadata | agent toolchain data | Repo-local only; low architecture risk. | Low | Keep out of public adapter bundle. | Medium |
| `docs/architecture` | Architecture docs and policy surfaces | `v2-architecture.md`, language/harness/video/toolchain policies | Strong boundary documentation; some historical roadmap docs may accumulate stale context. | Medium | Prefer short ADR/policy deltas over expanding roadmap docs indefinitely. | Medium |
| `docs/architecture/decisions` | Architecture decision records | `0001-hermes-primary-orchestration.md` | ADRs are useful but terms like canonical repo artifact vs gameplay authority need care. | Low | Add terminology note when next touching architecture docs. | Medium |
| `docs/distribution` | Distribution docs root | `README`/support docs | Public distribution boundary is small; installer local state details are less visible. | Medium | Improve installer/local-state documentation. | Medium |
| `docs/distribution/agents` | Human-facing install/use docs | agent install docs | Same installer replacement/local-state concern. | Medium | Document private checkout/symlink replacement and non-canonical local state. | Medium |
| `docs/testing` | Testing documentation | `README.md` | Manual validator list lags `run-all.ps1`. | Medium | Make `run-all.ps1` the canonical list and reduce manual duplication. | High |
| `docs/testing/smoke-runs` | Historical smoke reports/templates | smoke reports, video learning template | Smoke reports are execution evidence, not gameplay authority; validator protects template better than historical report semantics. | Medium | Keep historical reports immutable, add clearer execution-evidence terminology. | Medium |
| `docs/testing/video-analysis-calibration` | Executed video calibration reports | 9 calibration reports | Reports preserve review-only boundaries but are accumulating as one-off docs. | Medium | Add exit taxonomy: promote to workflow/eval/validator, hold, or archive as historical. | High |
| `evals` | Answer-quality eval root | `README.md` | Current evals are useful but not a full executable answer grader. | Medium | Extend schema before adding broad new cases. | High |
| `evals/fixtures/combo-damage` | Combo damage oracle fixtures | `jp-ryusei-nyfngnzjv3m.yaml`, `README.md` | Fixtures are review-only and useful, but calculator contract is not yet defined. | Medium | Define damage calculator input/output contract before expanding enabled cases. | High |
| `evals/questions` | Answer mode question fixtures | `*.yaml` | Mostly existence/shape checked; limited scoring semantics. | Medium | Add expected evidence family and disallowed source paths. | High |
| `evals/rubrics` | Human-readable answer rubrics | `answer-modes.md`, `grounding.md` | Good concise boundary, but not machine-linked to eval execution. | Low | Link rubric fields to eval schema in future. | Medium |
| `ingest/frame_data` | Frame data ingestion package and docs | `README.md`, `pyproject.toml`, `uv.lock` | Clear v3 design; fetch/retry and raw minimality gaps remain. | High | Prioritize raw minimality and fetch challenge retry issue. | High |
| `ingest/frame_data/config` | Fetch profile config | `fetch_profiles.yaml` | Retry config exists, but retry applies mainly to exceptions rather than HTTP/challenge states. | High | Treat HTTP >=400/challenge/selector absence as retryable failure. | High |
| `ingest/frame_data/config/binding_policy` | Character SuperCombo binding policies | `*.supercombo.yaml` | Large per-character config surface; generation exists but policy drift needs tests. | Medium | Keep generation deterministic and validate policy/registry hashes. | Medium |
| `ingest/frame_data/config/registry` | Character move registries | `*.moves.yaml` | Critical for parsing and candidate mapping; future character additions touch many surfaces. | Medium | Add checklist tying roster, registry, exports, runtime assets together. | High |
| `ingest/frame_data/src/sf6_ingest` | CLI/config/schema package layer | `cli.py`, `config.py`, `schemas.py` | Config model accepts broad `dict[str, str]`; constraints are mostly external validators. | Medium | Move official/supercombo source constraints into typed model. | High |
| `ingest/frame_data/src/sf6_ingest/core` | Parse/publish/derive/io pipeline | `pipeline.py`, `io.py`, parsers | Publish guardrails are good; raw hash validation on load is missing. | Medium | Verify stored bytes against metadata before parse. | High |
| `ingest/frame_data/src/sf6_ingest/fetch` | Scrapling fetch adapters | `scrapling_client.py`, `official.py`, `supercombo.py` | Challenge/HTTP response handling returns before retry. | High | Add response-quality retry gate and attempt metadata. | High |
| `ingest/frame_data/tests` | Ingest package tests | `test_*.py` | Good coverage for parsing/publish basics; fetch/challenge integration remains limited. | Medium | Add failure-response retry tests and raw orphan tests. | Medium |
| `ingest/frame_data/tests/fixtures` | HTML fixtures | `official_success.html`, `supercombo_success.html`, `supercombo_challenge.html` | Fixtures support parser/challenge tests; use them to test retry semantics. | Medium | Expand challenge fixture test coverage. | Medium |
| `knowledge` | Canonical knowledge lifecycle root | `README.md` | Good flow docs; "knowledge is canonical" can be misread as all subdirs accepted. | Medium | Clarify accepted authority vs review-only canonical tracking. | High |
| `knowledge/curated` | Accepted stable/concept knowledge | `README.md` | Exact current values excluded; source_refs can point to review-only provenance. | Medium | Add per-ref authority role. | High |
| `knowledge/curated/concepts` | Stable concept pages | `frame-timing.md`, `offense-decision-making.md` | Generally healthy; avoid exact current leakage. | Low | Continue generated_allowed contract checks. | High |
| `knowledge/curated/glossary` | Stable glossary pages | term pages | Some accepted terms rely on unresolved/claim provenance. | Medium | Mark provenance roles machine-readably. | High |
| `knowledge/curated/mechanics` | Stable mechanics pages | `combo-scaling.md` | Good current-value exclusion; system-mechanics authority remains unresolved. | Medium | Define system-mechanics promotion contract. | High |
| `knowledge/evidence` | Evidence root | `README.md` | Review-only boundary clear. | Low | Keep evidence outside generated references. | High |
| `knowledge/evidence/claims` | Article/term claim artifacts | `*.claims.md` | Good candidate-claim split; needs robust no-authority metadata. | Medium | Add `authority_status: review_only` in future contract. | Medium |
| `knowledge/evidence/video-observations` | Video observation artifacts | `*.observations.md` | Good observation/review boundary; not a strategy/current-fact authority. | Medium | Keep video observations linked to review decisions and evals. | Medium |
| `knowledge/review` | Review tracking root | `README.md` | Clear hold area. | Low | Keep promotion gates explicit. | High |
| `knowledge/review/contested` | Contested claim holding area | `README.md` | Empty/low-use surface; valid future destination. | Low | Do not expand until conflict cases exist. | Medium |
| `knowledge/review/current-fact-candidates` | Exact current/system candidate hold area | candidate docs | Contains exact numbers; no machine-readable public-answer-deny fields. | High | Add deny fields and validator before adding more candidates. | High |
| `knowledge/review/unresolved` | Unresolved review notes | `*.review.md` | Healthy hold pattern; can be overused if not routed to closeout. | Medium | Add periodic unresolved triage workflow. | Medium |
| `knowledge/sources` | Source metadata root | `README.md` | Good no-raw-source policy. | Low | Keep summaries short and copyright-bound. | High |
| `knowledge/sources/articles` | Article metadata | article source docs | Good review-only source model; not final answer evidence. | Low | Keep `validate-ingest-artifacts` aligned. | High |
| `knowledge/sources/videos` | Video metadata | video source docs | Good metadata-only boundary; video-source follow-up issues remain. | Medium | Tie source E2E rows to #155/#158 closeout. | Medium |
| `packages` | Repo-local build/install/generation tooling root | `README.md` | README says use only after second consumer, but current architecture intentionally uses packages for single public adapter packaging. | Medium | Update README ownership language. | High |
| `packages/knowledge-generation` | Generated knowledge builder | `build-sf6-agent-knowledge.ps1` | Deterministic but Markdown parsing is bespoke. | Medium | Move toward schema-backed front matter parsing if complexity grows. | Medium |
| `packages/skill-installers` | Public adapter installer scripts | install/resolve scripts | Installer replaces local target/symlink; local-state boundary docs are thin. | Medium | Document replacement/integrity/local-state behavior. | Medium |
| `packages/skill-packaging` | Runtime asset and release builders | build scripts | Builders are mutating and run in validation preflight. | Medium | Add check-only mode or document mutation. | High |
| `packages/skill-validator` | Future validator code placeholder | `README.md` | Name conflicts conceptually with canonical `tests/validation`. | Medium | Clarify or remove until a real shared validator package exists. | High |
| `packs` | Repo-local pack root | `README.md` | Boundary is good; operational discovery is manual. | Low | Keep packs outside public adapter. | High |
| `packs/codex-hermes-sf6` | Codex-Hermes maintainer pack | `README.md` | Boundary validator passes; activation/discovery path is not explicit. | Low | Clarify manual vs installable use. | Medium |
| `packs/codex-hermes-sf6/guards` | Boundary guard snippets | guard docs | Good concise safeguards; avoid duplicating canonical policies over time. | Low | Keep as pointers to canonical docs. | Medium |
| `packs/codex-hermes-sf6/resources` | Delegation/checklist resources | resource docs | Good pointer pattern; stale if canonical docs move. | Low | Validate links and avoid command truth duplication. | Medium |
| `packs/codex-hermes-sf6/skill` | Repo-local Codex playbook | `SKILL.md` | Correctly outside `skills/`; not public runtime. | Low | Add usage/discovery guidance if adopted. | Medium |
| `packs/hermes-sf6` | Hermes repo-local support root | guidance docs | Skeleton guidance only; no local state checked in. | Low | Keep non-executable until schema/ops are reviewed. | High |
| `packs/hermes-sf6/guards` | Hermes guard guidance | `README.md` | Good boundary placeholder. | Low | Avoid becoming independent workflow source. | Medium |
| `packs/hermes-sf6/profiles` | Hermes profile guidance | profile guidance docs | Markdown-only, no profile config. | Low | Add schema only after explicit decision. | Medium |
| `packs/hermes-sf6/prompts` | Future prompt wrapper guidance | `README.md` | Empty placeholder; low risk. | Low | Do not store raw prompt/session output. | Medium |
| `packs/hermes-sf6/reports` | Future Hermes report guidance | `README.md` | Correctly routes reports to canonical destinations. | Low | Keep directory as pointer, not report dump. | Medium |
| `skills` | Public skill namespace root | directory root | Single public adapter policy is clear. | Low | Do not add maintainer skills without architecture decision. | High |
| `skills/sf6-agent` | Public answer adapter | `SKILL.md` | Boundary healthy; runtime depends on generated assets. | Low | Keep adapter lean and no repo-local workflows. | High |
| `skills/sf6-agent/assets/frame-current` | Generated frame-current runtime manifest | `runtime_manifest.json` | Manifest lacks generic `generated: true` / `schema_version` / `kind`; provenance still present. | Medium | Strengthen manifest as generated-surface contract. | Medium |
| `skills/sf6-agent/assets/frame-current/published/<character_slug>` | Packaged current-fact runtime JSON for 29 characters | `snapshot_manifest.json`, `official_raw.json`, `derived_metrics.json`, `supercombo_enrichment.json` | Assets are clean; row-level source_role for enrichment is not explicit. | Medium | Add dataset authority metadata in manifest. | Medium |
| `skills/sf6-agent/assets/normalization` | Generated query normalization runtime assets | `aliases.json`, `runtime_manifest.json` | Good non-current-fact markers. | Low | Expand only through alias contract. | High |
| `skills/sf6-agent/references` | Adapter policies and generated concept references | `answer-policy.md`, `current-fact-policy.md`, `generated-*` | Generated concepts include source metadata; `maintainer_note` naming may be confusing in public runtime. | Low | Clarify reviewed maintainer-note role if it causes confusion. | Medium |
| `tests/fixtures/answer-orchestration` | Answer orchestration contract fixtures | JSON fixtures | Good contract support; fixture semantics should track contracts. | Low | Keep fixture validator schema-backed. | Medium |
| `tests/fixtures/answer-smoke` | Answer smoke fixtures | JSON fixtures | Useful for smoke shape; not a grader. | Low | Tie to future answer evaluation runner. | Medium |
| `tests/fixtures/codex-hermes-delegation` | Delegation dry-run fixtures | JSON fixtures | Good boundary examples; avoid stale command truth. | Low | Keep tied to bridge policy. | Medium |
| `tests/fixtures/external-frame-atlas` | External atlas metadata fixtures | JSON fixtures | Good metadata-only guard. | Low | Keep binary assets forbidden. | High |
| `tests/fixtures/video-observation-taxonomy` | Video observation taxonomy fixtures | JSON fixtures | Good taxonomy baseline; needs feedback from executed calibration reports. | Medium | Promote repeated calibration lessons into taxonomy fixtures. | Medium |
| `tests/validation` | Repo validation suite | `run-all.ps1`, `validate-*.ps1` | Strong coverage but growing script sprawl and text-matching duplication. | Medium | Introduce shared validation helpers or schema-driven checks in staged fashion. | High |
| `workflows` | Canonical maintainer procedures | `README.md`, workflow docs | Workflow set is coherent but overlapping video/media/review procedures are growing. | Medium | Add workflow ownership matrix and closeout routing for calibration/E2E. | High |

## Cross-Cutting Concerns

### 1. Authority Boundary Drift

- Fact: `data/exports/` and `data/roster/` are current-fact authority; `knowledge/curated` excludes exact current values.
- Concern: `data/exports/` includes CSV and `*_manual_review.*` next to main JSON authority. The broad phrase "`data/exports/` is authority" is operationally convenient but too coarse for future search/indexing tools.
- Recommendation: Document dataset-level roles in `data/exports/README.md` and eventually expose machine-readable `authority_role`/`answer_allowed` metadata.

### 1b. Raw Snapshot Minimality

- Fact: `ingest/frame_data/README.md:6-12` describes checked-in current artifacts as v3 code, published exports, and minimal raw snapshots needed to reproduce those exports.
- Concern: Local JSON/manifest inspection found 4 `data/raw/supercombo` snapshot directories not referenced by current `data/exports/*/snapshot_manifest.json`: `data/raw/supercombo/jp/20260310T023617Z-3b8fa28a`, `data/raw/supercombo/luke/20260412T151204Z-d96c657b`, `data/raw/supercombo/ryu/20260412T204407Z-384b6831`, and `data/raw/supercombo/sagat/20260412T214225Z-af77c139`.
- Recommendation: Decide whether these are removable residue or intentionally retained review artifacts, then encode that decision in a validator and `data/raw/README.md`.

### 2. Review-Only Evidence And Current-Fact Candidates

- Fact: `knowledge/review/current-fact-candidates` explicitly says candidates are not final public-answer evidence.
- Concern: The files can still contain exact numbers and formulas. If a whole-repo RAG/indexer ignores prose warnings, review-only values can leak into answers.
- Recommendation: Add machine-readable deny fields such as `authority_status: review_only`, `public_answer_allowed: false`, `generated_reference_allowed: false`, and validate them.

### 3. Validator Sprawl

- Fact: `run-all.ps1` runs 28 validators and generation preflight.
- Concern: validators are effective, but many rules are bespoke PowerShell text searches. This makes behavior harder to reason about and duplicates contract intent.
- Recommendation: Keep existing validators; do not rewrite. Add shared helpers/schema-backed checks only where repeated rules create maintenance cost.

### 4. Generated Surface Fragility

- Fact: generated concept references have YAML generated markers. frame-current runtime assets rely on `runtime_manifest.json` with generator/source/hash.
- Concern: frame-current manifest does not use the same generic generated-surface shape. This is not a current bug, but increases special-case validator logic.
- Recommendation: Add `generated`, `schema_version`, and `kind` to future frame-current/normalization manifests as a staged contract update.

### 5. Media Scratch/Cache Boundary

- Fact: media binary validator blocks common raw media/frame/cache leaks. Calibration reports state raw media not committed.
- Concern: executed calibration reports are growing as rich review-only artifacts; their lessons may remain one-off prose unless routed.
- Recommendation: Add a closeout section or workflow step mapping each calibration lesson to `workflow update`, `fixture/eval`, `validator`, `hold`, or `no action`.

### 6. Public Adapter Vs Maintainer-Local Tooling

- Fact: public runtime is `skills/sf6-agent`; `packs/*`, `packages/*`, `workflows/*`, and `tests/validation/*` are repo-local.
- Concern: package/installer docs and Codex-Hermes pack discovery are thinner than the boundary docs.
- Recommendation: Improve maintainer-local tooling docs without moving them into public adapter.

## Refactoring Roadmap

### Short Term

- Add a raw snapshot minimality follow-up: detect `data/raw/*` snapshot directories not referenced by `data/exports/*/snapshot_manifest.json`, or explicitly document retention exceptions.
- Update `docs/testing/README.md` so `run-all.ps1` is the canonical validator list and manual lists do not drift.
- Add `data/exports/README.md`, `data/raw/README.md`, and `data/external-frame-atlas/README.md` to place boundary guidance next to the data surfaces.
- Document that `run-all.ps1` and release preflight are mutating generation checks, not pure read-only validators.
- Add a lightweight calibration report closeout checklist for `docs/testing/video-analysis-calibration`.

### Medium Term

- Introduce machine-readable authority roles for curated `source_refs`, review-only evidence, and current-fact candidates.
- Extend eval schema with `expected_evidence_family`, `allowed_authority_surfaces`, `disallowed_source_paths`, and required boundary statements.
- Add fetch retry semantics for HTTP failure, challenge marker detection, and selector absence in `ingest/frame_data`.
- Add raw snapshot load integrity checks against `metadata.json` hash/byte count.
- Strengthen frame-current runtime manifest with generated-surface metadata and dataset authority roles.

### Long Term

- Define a system-mechanics current-fact authority/promotion contract for combo scaling, calculator-style fixtures, and patch-sensitive system rules.
- Split validation into contract/schema-backed checks plus domain policy checks while keeping the current PowerShell entrypoint stable.
- Build a controlled promotion lifecycle for video calibration lessons into taxonomy fixtures, answer evals, and maintainer workflows.
- Clarify Codex-Hermes pack installation/discovery only after a real maintainer workflow needs it.

## Proposed Follow-Up Issues

### 1. Validate and document raw snapshot minimality

- Why: `data/raw/supercombo` has 4 current unreferenced snapshot directories while docs describe checked-in raw as minimal reproduction state.
- Scope: validator or report that compares raw snapshot dirs with `snapshot_manifest.published_snapshot_ids`; document explicit retention exceptions if needed.
- Non-goals: deleting snapshots in the planning PR; changing current exports; fetching new raw data.
- Priority: High
- Dependencies: none

### 2. Add data-surface README boundary docs

- Why: `data/exports`, `data/raw`, and `data/external-frame-atlas` boundaries are currently spread across AGENTS, ingest README, and external atlas evaluation docs.
- Scope: docs-only READMEs explaining authority, sidecars, manual-review rows, raw snapshots, and external visual cache prohibition.
- Non-goals: data mutation or schema changes.
- Priority: Medium
- Dependencies: raw snapshot minimality decision may inform `data/raw/README.md`.

### 3. Add machine-readable review-only authority metadata

- Why: prose warnings are not enough for future RAG/index/generator use.
- Scope: contract fields and validators for review-only evidence/current-fact candidates and possibly per-ref authority role in curated source refs.
- Non-goals: promoting or rejecting existing claims.
- Priority: High
- Dependencies: contract design review.

### 4. Define video calibration report closeout lifecycle

- Why: calibration reports are accumulating detailed lessons that need routing into workflows, fixtures, evals, validators, or holds.
- Scope: workflow/template update and optional validator for required closeout fields.
- Non-goals: rewriting historical reports; adding raw media.
- Priority: Medium
- Dependencies: #155/#158 E2E validation closeout context.

### 5. Separate mutating generation preflight from check-only validation

- Why: `run-all.ps1` is correct for CI but less ergonomic for docs-only review and architecture audit verification.
- Scope: document mutation clearly or add `-CheckOnly`/non-mutating helper where feasible.
- Non-goals: removing existing CI behavior.
- Priority: Medium
- Dependencies: packaging/generation maintainers.

### 6. Improve ingest fetch failure and integrity handling

- Why: HTTP/challenge failures are not retried as first-class failures, and raw bytes are not revalidated against metadata on load.
- Scope: retry gate for status/challenge/selector, raw hash validation, focused tests.
- Non-goals: changing official data, adding external visual scraping.
- Priority: High
- Dependencies: raw snapshot retention policy.

## Findings Not Worth Acting On Yet

- Creating a separate `sf6-agent-ja` adapter: current language policy and public adapter boundary intentionally keep one adapter.
- Rewriting all validators into a new framework: current validators protect real boundaries; staged extraction is safer.
- Moving Hermes/Codex packs into `skills/`: current architecture explicitly keeps maintainer-local tooling outside public answer distribution.
- Turning external frame-atlas evaluation into a cache workflow: current metadata-only policy is correct until permission, storage, validator, and bundle boundaries are decided.
- Expanding eval fixtures broadly before schema improvements: more cases without stronger evidence fields would increase maintenance load without improving confidence enough.

## Uncertainties

- Whether the 4 unreferenced SuperCombo raw snapshots are accidental residue or intentionally retained audit artifacts is not confirmed from code alone.
- Whether maintainers prefer warning-only or failure behavior for raw snapshot minimality needs product/process decision.
- GitHub issue search was path/title oriented; some design rationale may exist in issue comments not inspected here.
- Actual public release bundle artifact was not rebuilt or inspected in this docs-only audit before final validation.
- This report does not assert current external frame-data freshness.
