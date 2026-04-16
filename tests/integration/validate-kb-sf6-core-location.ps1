Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$required = @(
  'skills/kb-sf6-core/SKILL.md',
  'skills/kb-sf6-core/references/CORE_QUESTIONS.md',
  'skills/kb-sf6-core/references/KNOWLEDGE.md',
  'skills/kb-sf6-core/references/REVIEW_QUEUE.md',
  'skills/kb-sf6-core/references/SOURCE_POLICY.md'
)

$missing = $required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $repoRoot $_)) }
if (@($missing).Count -gt 0) {
  throw "Missing kb-sf6-core public files: $($missing -join ', ')"
}

$expectedSkill = [string]::Join("`n", @(
  '---'
  'name: kb-sf6-core'
  'description: SF6の不変の概念を説明するときに使う。フレーム、発生/持続/硬直、有利不利、確反、ヒット確認、起き攻め、シミーなどの概念質問に答える。'
  '---'
  ''
  'あなたは SF6 の **不変の概念を優先して説明する** skill です。'
  ''
  '## 目的'
  '- SF6 の概念質問に、短く・ぶれず・再利用しやすい形で答える。'
  '- current fact / exact 数値 / パッチ差分に踏み込まない。'
  '- mixed question では概念を先に答え、exact current values は別確認に切り分ける。'
  ''
  '## 参照順'
  '1. `references/KNOWLEDGE.md`'
  '2. `references/CORE_QUESTIONS.md`'
  '3. `references/SOURCE_POLICY.md`'
  '4. `references/REVIEW_QUEUE.md`（未確定や pending の確認用）'
  ''
  '## 回答方針'
  '- 基本ラベルは `[概念のみ]`。'
  '- まず一言定義を書く。'
  '- 次に実戦で何に効く概念かを 1〜2 文で書く。'
  '- 似た概念との違いが必要なら 1 点だけ補足する。'
  '- コミュニティ用語は「コミュニティで一般的な言い方」と明記する。'
  '- 質問が current fact を含むなら、概念を答えたあとで exact current values は `kb-sf6-frame-current` 側の別確認が必要だと述べる。'
  ''
  '## 禁止事項'
  '- 根拠なしで exact 数値を作らない。'
  '- current fact や patch-specific behavior をこの skill 単体で断定しない。'
  '- コミュニティ用語を公式定義のように扱わない。'
  '- `T1` / `T2` の current verification を、この skill 単体で主張しない。'
  '- mixed / current fact を concept-only knowledge に混ぜ込まない。'
  ''
  '## 出力テンプレ'
  '[概念のみ]'
  '一言定義。'
  '実戦で何に効く概念か。'
  '必要なら似た概念との違いを 1 つだけ補足。'
  'current fact や exact 数値が必要なら、その部分は別確認だと明記。'
)) + "`n"

$expectedSourcePolicy = [string]::Join("`n", @(
  '# Source Policy'
  ''
  '## 目的'
  'この knowledge は「不変の概念」を安定して答えるためのもの。'
  'current fact / exact 数値 / パッチ差分はここに混ぜない。'
  ''
  '## 採用基準'
  '- Core 概念として安定している'
  '- キャラ依存・パッチ依存・特定状況依存が薄い'
  '- 定義や実戦的意味が長く保てる'
  ''
  '## 送付先'
  '- Core 概念: `KNOWLEDGE.md`'
  '- mixed / current fact / ソース不足: `REVIEW_QUEUE.md`'
  ''
  '## 階層'
  '- T1: 公式一次情報'
  '- T2: 公式相当のゲーム内観測'
  '- T3: 継続メンテ第三者（補助）'
  '- T4: コミュニティ知見'
  ''
  '## Runtime Answer Boundary'
  '- この knowledge の outward label は `[概念のみ]` を基本とする。'
  '- この knowledge 単体では current verification や exact current values を断定しない。'
  '- packaged move-specific current facts / exact current values が必要なときは `kb-sf6-frame-current` 側の published current-fact surface に切り替える。'
  '- packaged frame-data exports だけでは結論できない current behavior / patch-specific question は `REVIEW_QUEUE.md` に残すか maintainer workflow に回す。'
  ''
  '## ルール'
  '- exact 数値や current 仕様は T1/T2 が無ければ knowledge に昇格しない。'
  '- コミュニティ語は採用してよいが、「コミュニティで一般的な言い方」とラベル付けする。'
  '- コミュニティ語を公式定義のように扱わない。'
)) + "`n"

$skillPath = Join-Path $repoRoot 'skills/kb-sf6-core/SKILL.md'
$skillContent = [System.IO.File]::ReadAllText($skillPath)
if ($skillContent -ne $expectedSkill) {
  throw 'skills/kb-sf6-core/SKILL.md does not match the expected public shell contract'
}

$sourcePolicyPath = Join-Path $repoRoot 'skills/kb-sf6-core/references/SOURCE_POLICY.md'
$sourcePolicyContent = [System.IO.File]::ReadAllText($sourcePolicyPath)
if ($sourcePolicyContent -ne $expectedSourcePolicy) {
  throw 'skills/kb-sf6-core/references/SOURCE_POLICY.md does not match the expected public shell contract'
}

$legacyRoot = Join-Path $repoRoot '.agents'
if (Test-Path -LiteralPath $legacyRoot -PathType Container) {
  throw 'Repo-root .agents must not exist'
}

Write-Host 'kb-sf6-core public shell OK'
