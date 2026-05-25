# Current-Fact Row/Move/Cell Candidate Evidence

This is a source-review summary only. It is not a production candidate
artifact, source-record artifact, current-fact export, runtime lookup change,
parser expansion, calculator approval, or authority promotion.

## Boundary

The review used ignored structured v4 row artifacts as reviewer input and
commits only minimal row/move/cell evidence. It does not commit source-page
payloads, complete rows, local payload references, browser session material,
visual reviewer output, generated current-fact artifacts, or private material.

Legacy raw export files are not replacement source input. Official values
remain `authority_candidate`. `annotated_numeric_candidate` and `frame_range`
remain non-scalar and not calculation-safe.

## Counts

| Metric | Count |
| --- | ---: |
| Evidence records | 13 |
| `annotated_candidate_not_calculation_safe` | 9 |
| `parsed_range_not_single_value_calculation_safe` | 4 |
| `startup` | 4 |
| `block_advantage` | 5 |
| `hit_advantage` | 4 |

## Evidence Records

| Character | Move label | Field | Raw value | Row | Cell | Parser rule | Status |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| `alex` | フライングクロスチョップ（ジャンプ中に） 強 | `block_advantage` | `-12～-1` | 41 | 5 | `frame_range.official_signed_wave_dash.v1` | `candidate_identity_evidence_found` |
| `vega_mbison` | ヘッドプレス（シャドウライズ中に） | `block_advantage` | `-39～-33` | 53 | 5 | `frame_range.official_signed_wave_dash.v1` | `candidate_identity_evidence_found` |
| `cammy` | リバースエッジ（フーリガンコンビネーション中に） | `block_advantage` | `-4～-1` | 52 | 5 | `frame_range.official_signed_wave_dash.v1` | `candidate_identity_evidence_found` |
| `ed` | サイコナックル(Lv1)強ホールド | `block_advantage` | `※-2` | 21 | 5 | `annotated_signed_frame.official_prefix_marker.negative.v1` | `candidate_identity_evidence_found` |
| `chunli` | 蘭華（行雲流水中に）弱 | `block_advantage` | `※-4` | 32 | 5 | `annotated_signed_frame.official_prefix_marker.negative.v1` | `candidate_identity_evidence_found` |
| `vega_mbison` | ヘッドプレス（シャドウライズ中に） | `hit_advantage` | `-28～-23` | 53 | 4 | `frame_range.official_signed_wave_dash.v1` | `candidate_identity_evidence_found` |
| `chunli` | 前突（行雲流水中に）弱 | `hit_advantage` | `※-1` | 35 | 4 | `annotated_signed_frame.official_prefix_marker.negative.v1` | `candidate_identity_evidence_found` |
| `chunli` | 蘭華（行雲流水中に）弱 | `hit_advantage` | `※-3` | 32 | 4 | `annotated_signed_frame.official_prefix_marker.negative.v1` | `candidate_identity_evidence_found` |
| `chunli` | 仙風（行雲流水中に）中 | `hit_advantage` | `※-4` | 36 | 4 | `annotated_signed_frame.official_prefix_marker.negative.v1` | `candidate_identity_evidence_found` |
| `kimberly` | 弱 細工手裏剣（細工手裏剣ストックが1以上で） 弱 | `startup` | `122※` | 64 | 1 | `annotated_frame.official_suffix_marker.v1` | `candidate_identity_evidence_found` |
| `kimberly` | 弱 乱れ細工手裏剣（細工手裏剣ストックが2以上で） 弱中 | `startup` | `122※` | 67 | 1 | `annotated_frame.official_suffix_marker.v1` | `candidate_identity_evidence_found` |
| `kimberly` | 中 乱れ細工手裏剣（細工手裏剣ストックが2以上で） 弱強 | `startup` | `122※` | 68 | 1 | `annotated_frame.official_suffix_marker.v1` | `candidate_identity_evidence_found` |
| `kimberly` | 強 細工手裏剣（細工手裏剣ストックが1以上で） 強 | `startup` | `128※` | 66 | 1 | `annotated_frame.official_suffix_marker.v1` | `candidate_identity_evidence_found` |

## Decision

This artifact shows that summary-safe row/move/cell identity evidence exists
for the listed parsed-value groups. It does not generate production candidate
records. A later mandatory-reviewed candidate artifact PR must still reproduce
deterministic parsed payloads, enforce parsed-value-only admission, carry
non-scalar calculation statuses, and exclude blocked values.

Issue #343 remains required for any future value-handling expansion.
