from __future__ import annotations

from collections.abc import Mapping
from typing import Any


SCALAR_CALCULATION_INPUT_STATUSES = frozenset(
    {
        "eligible_only_after_domain_source_and_unit_checks",
    }
)

SCALAR_CALCULATION_KINDS = frozenset(
    {
        "decimal",
        "gauge_amount",
        "integer",
        "percent",
        "signed_frame",
    }
)

NON_SCALAR_OR_BLOCKED_CALCULATION_STATUSES = frozenset(
    {
        "annotated_candidate_not_calculation_safe",
        "enum_only_not_arithmetic",
        "not_numeric_authority",
        "out_of_scope_not_emitted",
        "parsed_range_not_single_value_calculation_safe",
        "raw_preserved_not_calculation",
        "review_required_not_calculation_safe",
    }
)

NON_SCALAR_PARSED_VALUE_KINDS = frozenset(
    {
        "annotated_numeric_candidate",
        "enum_token",
        "frame_range",
        "ordered_pair",
        "raw_note",
    }
)


def is_scalar_calculation_input(
    parsed_value: object | None,
    calculation_input_status: str | None,
) -> bool:
    if not isinstance(parsed_value, Mapping):
        return False
    kind = parsed_value.get("kind")
    if not isinstance(kind, str):
        return False
    if kind in NON_SCALAR_PARSED_VALUE_KINDS:
        return False
    if calculation_input_status in NON_SCALAR_OR_BLOCKED_CALCULATION_STATUSES:
        return False
    if calculation_input_status not in SCALAR_CALCULATION_INPUT_STATUSES:
        return False
    return kind in SCALAR_CALCULATION_KINDS
