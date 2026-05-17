---
report_type: full_directory_architecture_refactor_audit
schema_version: directory-architecture-audit/v1
date: 2026-05-17
tracking_issue: "#220"
analysis_mode: hermes_primary_delegated
coverage_source: git_ls_files_directories
covered_directory_count: 188
raw_hermes_transcript_committed: false
hermes_local_state_committed: false
---

# アーキテクチャレビュー

## Executive Summary

- ADR-0002 により active priority は private Hermes-first operation に移ったが、`skills/sf6-agent/`, `.dist`, installer, distribution validator, generated runtime assets はまだ active product のように標準 validation 経路へ残っている。
- 最大の構造負債は、canonical / derived / deferred legacy / repo-local support / historical / non-canonical を一元管理する repository surface registry がないこと。path hardcode と文書分散が refactor を難しくしている。
- `skills/sf6-agent/assets/frame-current/` が deferred public adapter 配下にあるため、exact current-fact runtime payload と public legacy surface が構造的に結合している。
- validators は広く有効だが、PowerShell の手書き列挙・regex・存在確認に寄っており、schema-driven validation、read-only validation lane、legacy distribution lane の分離が不足している。
- knowledge/data/evals の正本境界は概ね良いが、source->evidence->review->curated の lineage、manual-review debt、eval scoring、system-mechanics authority の横断観測性が弱い。

Update: #226 supersedes the recommendation to create a repo-owned
system-mechanics formula / rounding authority surface. v2.6 keeps exact SF6
formulas and rounding rules out of repo authority; needed arithmetic should
route through trusted external CAS / symbolic math backend instructions and
remain non-authoritative.

## 実施方法

Hermes を primary analyst / orchestrator として使い、git 管理下の全ディレクトリを 3 group に分割して read-only delegated analysis を実行した。[Hermes delegation docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) では、child agent は親の会話履歴を持たず、`goal` / `context` に必要情報を明示する必要がある。その前提で repo path、Issue #220、ADR-0002、対象 directory group、分析観点、出力形式を渡した。

Second pass では最大待機時間を伸ばし、初回 top findings の安定性、追加懸念、優先度変化を確認した。追加結果は top findings を大きく入れ替えるものではなく、特に public distribution legacy surface、surface registry 欠如、schema/validator drift、provenance/authority metadata の弱さを補強する内容だった。

Raw Hermes transcript、local profile state、sessions、logs、caches、local skill output は commit していない。この report は Hermes output を要約・統合した repo artifact であり、Hermes output 自体を canonical evidence として扱わない。

参考: [ADR-0002](../decisions/0002-private-hermes-first-operation.md), [Codex-Hermes Bridge Policy](../codex-hermes-bridge-policy.md), [Harness And Distribution Roles](../harness-and-distribution-roles.md)。

## 現在の構造理解

事実:

- Canonical surfaces は `knowledge/`, `data/exports/`, `data/roster/`, `contracts/`, `workflows/`, `evals/`。ADR-0002 ではこれに加えて reviewed architecture docs / ADRs と validators も実質的な governance surface として扱っている。
- `skills/sf6-agent/` は既存 public answer adapter だが、ADR-0002 により active product surface ではなく deferred legacy distribution surface になった。
- `skills/sf6-agent/references/generated-*` は `knowledge/curated/` 由来の derived output。
- `skills/sf6-agent/assets/frame-current/` は `data/exports/` と `data/roster/` 由来の derived current-fact runtime output。
- `.dist/sf6-agent-bundle.zip`, `packages/skill-installers`, `packages/skill-packaging`, `docs/distribution/*` は public distribution 系の deferred/legacy surface。
- `packs/hermes-sf6/` と `packs/codex-hermes-sf6/` は repo-local orchestration support。canonical workflow の代替ではない。
- Hermes memory、sessions、profile state、local skill state、logs、caches、raw transcript は non-canonical。

推測:

- 現在の repo は「public skill distribution kit」として作り始めた surface と、「private Hermes-first knowledge maintenance system」へ移る surface が同居している。
- 今後の主利用者は公開 skill user ではなく、Windows Codex app から Hermes を操作する maintainer になる。
- そのため、public adapter の互換性維持より、repo artifact の正本境界、Hermes delegation trace、surface retirement map、validator lane 分離の方が重要になる。

## 想定されるユーザー利用シナリオ

- Maintainer が Windows Codex app から調査・設計・実装を依頼する。
- Codex が Hermes に primary analysis / orchestration を委譲する。
- Hermes が source analysis、claim decomposition、architecture review、workflow improvement、validator pattern proposal を draft として返す。
- Codex が boundary audit、artifact conversion、validation、PR 作成を行う。
- 最終成果だけを `knowledge/`, `docs/architecture/`, `workflows/`, `contracts/`, `evals/`, `tests/validation/`, `docs/testing/smoke-runs/` に残す。
- Public `skills/sf6-agent/` は、今後の棚卸しで remove / relocate / reactivate を判断するまで legacy として残る。

誤用されやすい利用:

- Hermes output を canonical source として扱う。
- `knowledge/evidence/claims` や `knowledge/review/current-fact-candidates` を public answer authority として扱う。
- `data/raw/*/page.html` や `*_manual_review.*` を通常回答の直接根拠にする。
- SuperCombo enrichment を official current fact override に使う。
- `packs/*` を canonical workflow より優先する。
- `.dist` や installer が残っていることを public distribution 再開済みと誤読する。

## 探索的に考えられる将来要望

- `skills/sf6-agent/` を削除・移設し、private operation 用 runtime surface を別 root にしたい。
- frame-current runtime lookup を public adapter 配下から切り離したい。
- repository surface registry で canonical / derived / deferred / support / historical / non-canonical を管理したい。
- Hermes delegation の sanitized trace contract を残したい。
- source->claim->review->curated の lineage graph を生成したい。
- evals を静的 YAML ではなく、agent response scoring / regression tracking に使いたい。
- combo scaling、damage formula、system mechanics の計算を、repo-owned authority ではなく外部 CAS / symbolic math backend 向け instruction として扱いたい。
- `run-all.ps1` を read-only validation / build-derived / legacy distribution / toolchain に分割したい。

## 主要な懸念点

### 懸念 1: deferred public distribution が validation により operationally active のまま残っている

- 種別: architecture / operability / maintainability
- 根拠: ADR-0002 は `skills/sf6-agent/`, frame-current assets, `.dist` を deferred distribution surface とする。一方で `tests/validation/run-all.ps1` は generated references、frame-current、normalization、release bundle を preflight 生成し、`validate-distribution.ps1` は `.dist/sf6-agent-bundle.zip` を必須にする。
- 問題: public distribution を deferred にしたのに、標準 validation が public bundle の生成・存在を要求している。
- ユーザー影響: maintainer が private Hermes-first refactor を進めても、legacy public distribution の維持に引き戻される。
- 将来要望との関係: `skills/sf6-agent` 削除・移設、`.dist` 廃止、installer 停止を行うと validation が壊れる。
- 推奨対応: validation lane を `ValidateOnly`, `BuildDerived`, `LegacyDistribution`, `Toolchain` に分ける。`.dist` と installer/bundle validation は legacy distribution lane に移す。
- 優先度: High

### 懸念 2: frame-current runtime が deferred public adapter 配下にある

- 種別: architecture / design
- 根拠: `contracts/frame-current-runtime-assets.md` は runtime assets を `data/exports/` + `data/roster/` 由来とするが、出力先は `skills/sf6-agent/assets/frame-current/`。
- 問題: exact current-fact runtime payload が legacy public adapter path に結合している。
- ユーザー影響: private Hermes-first answer/lookup を作る場合でも deferred public skill path を参照することになる。
- 将来要望との関係: public adapter removal / relocation と current-fact runtime が同時に壊れる。
- 推奨対応: `data/runtime/frame-current/` または `runtime/current-facts/` を新設し、canonical-derived runtime build と legacy adapter copy を分離する。
- 優先度: High

### 懸念 3: repository surface registry がない

- 種別: architecture / maintainability
- 根拠: ADR-0002 front matter の `canonical_sources` と本文の canonical surfaces が完全一致していない。validators と docs は path hardcode / exact phrase / manual list に依存している。
- 問題: canonical / derived / deferred legacy / support / historical / non-canonical の判定が文書と validator に分散している。
- ユーザー影響: refactor 時にどの surface を残す・移す・消すべきか判断しづらい。
- 将来要望との関係: public skill retirement、runtime root 移設、packages 分割、validators 分割で漏れが出る。
- 推奨対応: `contracts/repository-surface.schema.json` と `data/repository-surfaces.json` を追加し、surface id、path、status、authority_role、source_surfaces、derived_outputs、validators、removal_blockers を管理する。
- 優先度: High

### 懸念 4: Hermes-first boundary が docs/workflows/packs/validators に重複している

- 種別: architecture / maintainability
- 根拠: `docs/architecture/codex-hermes-bridge-policy.md`, `workflows/codex-to-hermes-delegation.md`, `packs/codex-hermes-sf6/skill/SKILL.md`, pack resources/guards に同種ルールが反復している。
- 問題: packs が thin pointer ではなく、実質的な procedure authority になりつつある。
- ユーザー影響: Codex/Hermes role や fallback 条件を変更すると複数箇所を同期する必要がある。
- 将来要望との関係: Hermes delegation trace、provider Codex role、public skill retirement で boundary wording が増えるほど drift する。
- 推奨対応: canonical procedure は `workflows/codex-to-hermes-delegation.md` に寄せ、packs は pointers/templates/checklists に縮小する。policy は machine-readable にして validator は policy id / canonical link を検査する。
- 優先度: High

### 懸念 5: packages の active / legacy / shared 責務が曖昧

- 種別: design / maintainability
- 根拠: `packages/README.md` は second real consumer が出るまで packages を使わない方針だが、実際には public adapter 専用の `knowledge-generation`, `skill-packaging`, `skill-installers` と、repo-local `calculation-executor` が同居している。
- 問題: packages が shared infrastructure なのか legacy public adapter tooling なのか分からない。
- ユーザー影響: 新規 tooling の置き場と削除候補の判断が難しい。
- 将来要望との関係: public distribution retirement と private runtime migration で package boundary が壊れやすい。
- 推奨対応: `packages/README.md` を surface registry と同期し、package ごとに `active_repo_local`, `deferred_distribution`, `legacy`, `shared_infra`, `single_consumer_exception` を明記する。
- 優先度: High

### 懸念 6: schema/validator layer が手書き・regex・存在確認に寄りすぎている

- 種別: testing / maintainability
- 根拠: `validate-v2-contracts.ps1` は schema file の存在や required text の確認中心。`validate-evals.ps1` は固定 file list と regex 検査中心。
- 問題: JSON Schema が canonical contract であるにもかかわらず、実 artifact に対する schema validation が限定的。
- ユーザー影響: schema と実データ/fixtures/Markdown front matter が drift しても検出が遅れる。
- 将来要望との関係: surface registry、eval scoring、system-mechanics schema、source metadata schema を増やすと drift が拡大する。
- 推奨対応: schema validator を導入し、manifest-driven に artifact class ごとの schema validation を実行する。手書き semantic checks は schema validation 後段に限定する。
- 優先度: High

### 懸念 7: data/export manifest と manual-review debt の横断観測性が弱い

- 種別: data architecture / operability
- 根拠: `ingest/frame_data/README.md` は official_raw canonical、manual_review sidecars、snapshot_manifest provenance を説明するが、`data/exports/` 自体の authority README / schema / 横断 index は薄い。
- 問題: character ごとの dataset state、withheld rows、manual-review reasons、published/unpublished counts が横断的に見えにくい。
- ユーザー影響: patch refresh や manual-review debt 解消時の review 負荷が高い。
- 将来要望との関係: roster 増加、patch history 保持、data/runtime 分離時に provenance が追いにくくなる。
- 推奨対応: `data/exports/README.md`, `contracts/current-fact-export-manifest.schema.json`, `data/exports/_index/current_fact_review_debt.json` を追加する。
- 優先度: Medium

### 懸念 8: raw HTML snapshot retention は長期スケール・権利・セキュリティ負荷が残る

- 種別: security / operability / scalability
- 根拠: `data/raw/official/*/page.html` と `data/raw/supercombo/*/page.html` は reproducibility surface。raw minimality validator はあるが full external HTML を git に保持する。
- 問題: 現状は最小 snapshot だが、patch history や source class が増えると repo size、権利、security review の負担が増える。
- ユーザー影響: raw dump を追加しやすくなり、copyright/security 境界が弱まる。
- 将来要望との関係: historical patch support、multi-source ingestion、image/video raw support が来ると破綻しやすい。
- 推奨対応: raw retention ADR を作り、Git-tracked sanitized reproducibility artifact と repo-external full raw cache/hash reference を分離する。
- 優先度: Medium

### 懸念 9: evals は canonical だが実行可能な answer-quality scoring がない

- 種別: testing / operability
- 根拠: `evals/` は canonical answer-quality surface だが、現在は静的 YAML / rubric / fixture 検証が中心。
- 問題: private Hermes-first loop が回答品質を改善しているか測りにくい。
- ユーザー影響: Hermes/Codex refactor の効果を regression として確認できない。
- 将来要望との関係: answer mode、current-fact hold、web-needed、calculation trace が増えるほど scoring が必要になる。
- 推奨対応: eval artifact validation を YAML parser + schema にし、別 lane で agent response scoring / rubric summary を CI artifact として出す。
- 優先度: Medium

### 懸念 10: knowledge promotion lineage の queryability が弱い

- 種別: architecture / operability
- 根拠: `knowledge/` は source -> evidence -> review -> curated の流れを持つが、横断 graph/index はない。
- 問題: source_refs、review_after、unresolved/contested、generated contamination の棚卸しが手作業になりやすい。
- ユーザー影響: 長期運用で unresolved review が溜まり、何を昇格/保留/破棄すべきか見えにくくなる。
- 将来要望との関係: Hermes の継続学習・source ingest・video observation が増えると lineage が重要になる。
- 推奨対応: read-only `knowledge graph report` を生成し、dangling source refs、duplicate ids、review_after overdue、source->claim->review->curated lineage、generated contamination を検査する。
- 優先度: Medium

### 懸念 11: system-mechanics calculation authority は repo 外へ寄せる

- 種別: architecture / design
- 根拠: combo scaling などは `knowledge/review/current-fact-candidates` に hold され、`packages/calculation-executor` は arithmetic trace executor であり SF6 formula authority ではない。
- 問題: system formula / rounding / minimum guarantee / patch-sensitive exceptions を repo authority として持つと、更新漏れや誤った authority 昇格のリスクが高い。
- ユーザー影響: SF6 の数学的質問で hold が増えるか、review-only material を誤用するリスクがある。
- 将来要望との関係: combo damage calculator、frame advantage calculator、oki timing calculator が欲しくなると、信頼できる外部 CAS / symbolic math backend と operator instruction 管理が必要になる。
- 推奨対応: repo-owned formula / rounding authority は作らず、必要な計算は外部 backend への maintainer instruction と非 authoritative trace に寄せる。
- 優先度: Medium

### 懸念 12: installer / bundle validation の supply-chain boundary が弱い

- 種別: security / distribution
- 根拠: `packages/skill-installers/install-sf6-agent.ps1` は latest release URL を構成し、download/expand/copy/link を行う。`validate-distribution.ps1` は bundle entries の最低限確認が中心。
- 問題: deferred public distribution surface に remote install path が残っている。checksum/signature/pinned digest/zip entry allowlist/size limit/token-like scan が弱い。
- ユーザー影響: 誤って installer を使うと supply-chain risk が残る。
- 将来要望との関係: public distribution reactivation 時に security hardening が必要になる。
- 推奨対応: ADR-0002 期間中は installer docs を deferred/deprecated と明示する。reactivation するなら checksum/signature verification と strict bundle allowlist を導入する。
- 優先度: Medium

## 改善ロードマップ

### 短期

- この report を Issue #220 の docs-only audit artifact として merge する。
- `skills/sf6-agent`, `.dist`, installers, generated references, frame-current assets の responsibility map を作る。
- `run-all.ps1` を read-only validation と derived generation/preflight に分ける計画を issue 化する。
- `docs/distribution/*`, `skills/README.md`, installer docs に ADR-0002 の deferred warning を追加する。

### 中期

- `contracts/repository-surface.schema.json` と `data/repository-surfaces.json` を導入する。
- current-fact runtime root を `skills/sf6-agent` 配下から切り離す。
- `packages/` を active repo-local / deferred distribution / legacy に分類する。
- schema-driven validation を導入し、PowerShell regex validation を semantic checks に縮小する。
- `data/exports/README.md` と current-fact export manifest schema を追加する。

### 長期

- public skill を削除・移設・再有効化のどれにするかを surface map に基づき決定する。
- private Hermes-first delegation trace contract を作る。
- knowledge graph report と eval scoring harness を追加する。
- SF6 formula / rounding authority は repo に作らず、外部 CAS / symbolic math backend 向け instruction と非 authoritative trace 運用に寄せる。
- raw snapshot retention を Git-tracked sanitized artifact と repo-external raw cache/hash reference に分離する。

## 不確実な点・追加で確認したい点

- public skill external users が none であることは maintainer statement / ADR-0002 に基づく。外部 telemetry は確認していない。
- Hermes child agents の詳細 command output は保存していない。raw transcript は non-canonical であり、この report では summary のみ使っている。
- `data/raw` の long-term retention は source rights / reproducibility / repo size の tradeoff があり、maintainer の許容範囲確認が必要。
- public distribution を完全削除する場合、`validate-distribution.ps1`, `packages/skill-installers`, `docs/distribution`, `.dist`, `skills/sf6-agent` の順序を慎重に決める必要がある。
- `tests/validation/` と architecture docs/ADRs を canonical surface として machine-readable registry に含めるか、governance surface として別分類するかは決める必要がある。

## Coverage Appendix

Coverage source command:

```bash
git ls-files | awk '{ if (index($0,"/") == 0) { print "." } else { sub("/[^/]*$", "", $0); print $0 } }' | sort -u
```

Root files are represented by `.`. This appendix uses the corrected `git ls-files` directory set, not the two typo paths that appeared in the initial Hermes prompt draft.

### Group A: root/docs/contracts/workflows/tests/packs/github/toolchain

```text
.
.github
.github/workflows
contracts
docs/architecture
docs/architecture/decisions
docs/distribution
docs/distribution/agents
docs/testing
docs/testing/smoke-runs
docs/testing/video-analysis-calibration
tests/fixtures/answer-orchestration
tests/fixtures/answer-smoke
tests/fixtures/calculation-executor
tests/fixtures/codex-hermes-delegation
tests/fixtures/external-frame-atlas
tests/fixtures/video-observation-taxonomy
tests/validation
workflows
packs
packs/codex-hermes-sf6
packs/codex-hermes-sf6/guards
packs/codex-hermes-sf6/resources
packs/codex-hermes-sf6/skill
packs/hermes-sf6
packs/hermes-sf6/guards
packs/hermes-sf6/profiles
packs/hermes-sf6/prompts
packs/hermes-sf6/reports
data/toolchain
```

### Group B: data/raw/data exports/data current-fact surfaces

```text
data/aliases
data/exports/aki
data/exports/alex
data/exports/blanka
data/exports/cammy
data/exports/chunli
data/exports/cviper
data/exports/deejay
data/exports/dhalsim
data/exports/ed
data/exports/ehonda
data/exports/elena
data/exports/gouki_akuma
data/exports/guile
data/exports/jamie
data/exports/jp
data/exports/juri
data/exports/ken
data/exports/kimberly
data/exports/lily
data/exports/luke
data/exports/mai
data/exports/manon
data/exports/marisa
data/exports/rashid
data/exports/ryu
data/exports/sagat
data/exports/terry
data/exports/vega_mbison
data/exports/zangief
data/external-frame-atlas/evaluation
data/raw/official/aki/20260412T161520Z-7fbd27f7
data/raw/official/alex/20260412T161526Z-9839b882
data/raw/official/blanka/20260412T161514Z-b66cc4c2
data/raw/official/cammy/20260412T161519Z-8289f3ca
data/raw/official/chunli/20260412T161511Z-31b9e71d
data/raw/official/cviper/20260412T161525Z-a7ba6579
data/raw/official/deejay/20260412T161516Z-d5bba474
data/raw/official/dhalsim/20260412T161515Z-bfffb3ab
data/raw/official/ed/20260412T161521Z-719afbc0
data/raw/official/ehonda/20260412T161515Z-f7a529f8
data/raw/official/elena/20260412T161524Z-2649b57a
data/raw/official/gouki_akuma/20260412T161522Z-e5cef7e8
data/raw/official/guile/20260412T161511Z-2fcf0e43
data/raw/official/jamie/20260412T161510Z-786a93e8
data/raw/official/jp/20260412T151014Z-6aeeace2
data/raw/official/juri/20260412T161513Z-f21ab57c
data/raw/official/ken/20260412T161513Z-83e39e41
data/raw/official/kimberly/20260412T161512Z-b0731b91
data/raw/official/lily/20260412T161519Z-400d530c
data/raw/official/luke/20260412T151014Z-a610a92d
data/raw/official/mai/20260412T161523Z-142c38ef
data/raw/official/manon/20260412T161516Z-aedf1008
data/raw/official/marisa/20260412T161517Z-529a56d1
data/raw/official/rashid/20260412T161520Z-c1af6585
data/raw/official/ryu/20260412T161509Z-eee70350
data/raw/official/sagat/20260412T161525Z-6f955abc
data/raw/official/terry/20260412T161523Z-fc92d323
data/raw/official/vega_mbison/20260412T161522Z-d61a7dff
data/raw/official/zangief/20260412T161518Z-44ac8649
data/raw/supercombo/aki/20260412T212323Z-09d0c791
data/raw/supercombo/alex/20260412T214332Z-f7ab00c5
data/raw/supercombo/blanka/20260412T210120Z-b88e35d1
data/raw/supercombo/cammy/20260412T211715Z-583424e1
data/raw/supercombo/chunli/20260412T205125Z-e44b2ca7
data/raw/supercombo/cviper/20260412T214259Z-d1544e78
data/raw/supercombo/deejay/20260412T210554Z-b1ab66c9
data/raw/supercombo/dhalsim/20260412T210424Z-a4a761c1
data/raw/supercombo/ed/20260412T212628Z-f00d5c58
data/raw/supercombo/ehonda/20260412T210510Z-c157f16c
data/raw/supercombo/elena/20260412T214050Z-b474cc50
data/raw/supercombo/gouki_akuma/20260412T212932Z-447e18a5
data/raw/supercombo/guile/20260412T205429Z-168d253c
data/raw/supercombo/jamie/20260412T205050Z-91a98446
data/raw/supercombo/jp/20260412T211216Z-8241f7b0
data/raw/supercombo/juri/20260412T205838Z-3fba7e0e
data/raw/supercombo/ken/20260412T205914Z-7c1dea52
data/raw/supercombo/kimberly/20260412T205632Z-302cf26c
data/raw/supercombo/lily/20260412T211636Z-57501bca
data/raw/supercombo/luke/20260412T204844Z-a2b354b1
data/raw/supercombo/mai/20260412T213746Z-5ee126b8
data/raw/supercombo/manon/20260412T210708Z-de6f395a
data/raw/supercombo/marisa/20260412T211012Z-72a84215
data/raw/supercombo/rashid/20260412T212019Z-7e4c58e2
data/raw/supercombo/ryu/20260412T204539Z-71ff24af
data/raw/supercombo/sagat/20260412T214829Z-28e9df44
data/raw/supercombo/terry/20260412T213442Z-a27a5cb6
data/raw/supercombo/vega_mbison/20260412T213236Z-83650a27
data/raw/supercombo/zangief/20260412T211429Z-385c15f2
data/roster
```

### Group C: knowledge/ingest/evals/packages/skills distribution surfaces

```text
knowledge
knowledge/curated
knowledge/curated/concepts
knowledge/curated/glossary
knowledge/curated/mechanics
knowledge/evidence
knowledge/evidence/claims
knowledge/evidence/video-observations
knowledge/review
knowledge/review/contested
knowledge/review/current-fact-candidates
knowledge/review/unresolved
knowledge/sources
knowledge/sources/articles
knowledge/sources/videos
evals
evals/fixtures/combo-damage
evals/questions
evals/rubrics
ingest/frame_data
ingest/frame_data/config
ingest/frame_data/config/binding_policy
ingest/frame_data/config/registry
ingest/frame_data/src/sf6_ingest
ingest/frame_data/src/sf6_ingest/core
ingest/frame_data/src/sf6_ingest/fetch
ingest/frame_data/tests
ingest/frame_data/tests/fixtures
packages
packages/calculation-executor
packages/knowledge-generation
packages/skill-installers
packages/skill-packaging
packages/skill-validator
skills
skills/sf6-agent
skills/sf6-agent/assets/frame-current
skills/sf6-agent/assets/frame-current/published/aki
skills/sf6-agent/assets/frame-current/published/alex
skills/sf6-agent/assets/frame-current/published/blanka
skills/sf6-agent/assets/frame-current/published/cammy
skills/sf6-agent/assets/frame-current/published/chunli
skills/sf6-agent/assets/frame-current/published/cviper
skills/sf6-agent/assets/frame-current/published/deejay
skills/sf6-agent/assets/frame-current/published/dhalsim
skills/sf6-agent/assets/frame-current/published/ed
skills/sf6-agent/assets/frame-current/published/ehonda
skills/sf6-agent/assets/frame-current/published/elena
skills/sf6-agent/assets/frame-current/published/gouki_akuma
skills/sf6-agent/assets/frame-current/published/guile
skills/sf6-agent/assets/frame-current/published/jamie
skills/sf6-agent/assets/frame-current/published/jp
skills/sf6-agent/assets/frame-current/published/juri
skills/sf6-agent/assets/frame-current/published/ken
skills/sf6-agent/assets/frame-current/published/kimberly
skills/sf6-agent/assets/frame-current/published/lily
skills/sf6-agent/assets/frame-current/published/luke
skills/sf6-agent/assets/frame-current/published/mai
skills/sf6-agent/assets/frame-current/published/manon
skills/sf6-agent/assets/frame-current/published/marisa
skills/sf6-agent/assets/frame-current/published/rashid
skills/sf6-agent/assets/frame-current/published/ryu
skills/sf6-agent/assets/frame-current/published/sagat
skills/sf6-agent/assets/frame-current/published/terry
skills/sf6-agent/assets/frame-current/published/vega_mbison
skills/sf6-agent/assets/frame-current/published/zangief
skills/sf6-agent/assets/normalization
skills/sf6-agent/references
```
