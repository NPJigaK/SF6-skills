---
id: sf6-mechanics-combo-scaling
title: Combo Scaling
claim_kind: stable_concept
source_kind: community
source_role: reviewed japanese article stable mechanics concept
evidence_basis:
  - "Hameko 2023 combo scaling article source metadata and summary were recorded for review."
  - "Candidate claims separated stable combo-scaling concepts from numeric, character-specific, move-specific, and current-system claims."
  - "Review notes held concrete scaling values and exception claims for future current-system verification."
verification_state: partially_verified
confidence: 0.7
volatility: stable
patch_sensitivity: medium
review_status: accepted
source_refs:
  - label: "Source metadata: Hameko 2023 combo scaling"
    path: "knowledge/sources/articles/hameko-2023-combo-scaling.md"
    accessed_at: "2026-05-01"
  - label: "Candidate claims: Hameko 2023 combo scaling"
    path: "knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md"
    accessed_at: "2026-05-01"
  - label: "Review holding note: Hameko 2023 combo scaling"
    path: "knowledge/review/unresolved/hameko-2023-combo-scaling.review.md"
    accessed_at: "2026-05-01"
review_after: "2026-11-03"
summary: "コンボ補正は、コンボ中のダメージを状況に応じて調整する仕組みです。具体的な補正率や例外は現在仕様として別途確認が必要です。"
generated_allowed: true
must_not_include:
  - "exact scaling percentages"
  - "character-specific or move-specific current exceptions"
  - "current-system numeric claims"
---

# Combo Scaling

コンボ補正は、コンボ中のダメージを状況に応じて調整する仕組みです。

コンボで複数の攻撃がつながる時、各ヒットを常に独立した最大ダメージとして扱うのではなく、始動、ルート、途中で使う行動、ヒットの位置づけなどによって最終的なダメージが変わります。

## 何を説明する概念か

コンボ補正は、同じように見えるコンボでもダメージが変わる理由を説明するための安定概念です。

たとえば、次のような観点を分けて考える時に使います。

- どの行動からコンボが始まったか。
- コンボ中にどのようなルートを選んだか。
- システム行動や特殊な条件が関係しているか。
- 途中のヒットが、後続ダメージにどのような影響を持つ可能性があるか。

このページは、そうした考え方の入口だけを扱います。具体的な数値、技ごとの例外、キャラクター固有の扱いは扱いません。

## 回答で使ってよいこと

ユーザーに説明する時は、コンボ補正を「コンボ中のダメージを調整する仕組み」として説明してよいです。

また、コンボダメージを見る時には、単純なヒット数だけでなく、始動やルート、途中で使った行動、現在のシステム仕様を分けて確認する必要がある、と案内してよいです。

ただし、特定の補正率、特定キャラクターの例外、特定技の現在仕様、特定ルートの期待ダメージを、このページだけで断定してはいけません。

## Review boundary

このページは安定概念だけをcurated knowledgeとして受け入れています。

次の内容は、引き続きreviewまたはcurrent-system verificationの対象です。

- 具体的な補正率。
- 弱攻撃始動、システム行動、SA最低保証などの現在仕様。
- キャラクター固有、技固有、操作方式固有の例外。
- 現行patchでの正確なコンボダメージや最適ルート。

Hameko 2023記事は、この概念を整理するための有用な日本語sourceですが、現在仕様の最終根拠としては扱いません。数値や例外を回答に使う場合は、別のcurrent-system workflowで確認してください。
