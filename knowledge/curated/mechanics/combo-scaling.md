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
summary: "コンボ補正は、コンボ中のダメージを状況に応じて調整する仕組みです。技ごとの現在値はframe-current runtime assetsを参照し、このページでは計算を見るための概念だけを扱います。"
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

## 計算方法を読むための考え方

コンボ補正の計算は、単に技の基礎ダメージを全部足すものではありません。

各ヒットごとに、基礎ダメージに対してコンボ状況や追加条件による補正が関わる、と考えると安全です。

コンボダメージを読む時は、少なくとも次を分けて見ます。

- そのヒットの基礎ダメージ。
- コンボが進んだことによる補正。
- 始動やルート、システム行動による補正。
- 最低保証や技、キャラクター、操作方式に関係する例外。
- 現行patchで確認する具体値。

技ごとの基礎ダメージや、技に紐づく始動補正・コンボ補正の現在値は、このページでは扱いません。必要な場合は `skills/sf6-agent/assets/frame-current/` のruntime assetsを参照します。各キャラクターのpublished runtime dataには、moveごとのraw official fieldsが含まれる場合があります。

このページで扱うのは、補正率そのものではなく、コンボ補正を読むための考え方です。コンボ全体の最終ダメージ計算、システム行動、最低保証、キャラクター固有・技固有の例外、現行patchでの正確な計算式は、frame-current runtime assets、現在の公式情報、ゲーム内検証、または将来のsystem-mechanics fact workflowで確認してください。

## 回答で使ってよいこと

ユーザーに説明する時は、コンボ補正を「コンボ中のダメージを調整する仕組み」として説明してよいです。

また、コンボダメージを見る時には、単純なヒット数だけでなく、始動やルート、途中で使った行動、現在のシステム仕様を分けて確認する必要がある、と案内してよいです。

ただし、特定の補正率、特定キャラクターの例外、特定技の現在仕様、特定ルートの期待ダメージを、このページだけで断定してはいけません。

## Review boundary

このページは安定概念だけをcurated knowledgeとして受け入れています。

次の内容は、このcurated pageには複製しません。必要に応じてframe-current runtime assets、review、またはcurrent-system verificationで扱います。

- 具体的な補正率。
- 技ごとの基礎ダメージ、始動補正、コンボ補正の現在値。
- システム行動、SA最低保証などの現在仕様。
- キャラクター固有、技固有、操作方式固有の例外。
- 現行patchでの正確なコンボダメージや最適ルート。

Hameko 2023記事は、この概念を整理するための有用な日本語sourceですが、現在仕様の最終根拠としては扱いません。数値や例外を回答に使う場合は、このページから推測せず、適切なcurrent-fact surfaceやcurrent-system workflowで確認してください。
