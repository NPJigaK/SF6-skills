from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools.calculations.combo_damage.calculate import (
    ROUNDING_POLICY_FLOOR_EACH_HIT,
    calculate_combo_damage,
    load_ledger,
)


FIXTURE = Path(
    "tests/calculations/combo_damage/fixtures/"
    "jp/classic/2025-10-25-5hp-pc-3178.ledger.json"
)
FIXTURE_DIR = Path("tests/calculations/combo_damage/fixtures")
ALL_LEDGER_FIXTURES = sorted(FIXTURE_DIR.glob("**/*.ledger.json"))
JP_YEAR1_LEGACY_FIXTURE = Path(
    "tests/calculations/combo_damage/fixtures/"
    "jp/classic/2024-02-24-od-amnesia-5790.ledger.json"
)
AGGREGATED_HIT_SPAN_PATTERN = re.compile(r"^\d+\s*-\s*\d+$")
VALID_AUTHORITY = {
    "authority_type": "regression_fixture",
    "confidence": "medium",
    "source_paths": ["wiki/reviews/2026-06-15-mai-combo-damage-ledger-regression.md"],
    "validation_status": "human_training_validation",
    "review_status": "active",
}
JP_FIXTURES = [
    (
        JP_YEAR1_LEGACY_FIXTURE,
        5790,
        [720, 510, 510, 650, 440, 360, 350, 125, 125, 2000],
        "legacy Year1",
    ),
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "jp/classic/2025-10-25-5hp-pc-3178.ledger.json"
        ),
        3178,
        [960, 544, 177, 295, 510, 210, 210, 272],
        "starter plus mid-combo Drive Rush",
    ),
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "jp/classic/2025-10-25-5hk-3660.ledger.json"
        ),
        3660,
        [
            800,
            500,
            480,
            225,
            225,
            280,
            200,
            200,
            200,
            150,
            80,
            60,
            30,
            50,
            100,
            80,
        ],
        "SA2-active immediate scaling",
    ),
]
MAI_FIXTURES = [
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "mai/classic/2026-04-21-5mp-2496.ledger.json"
        ),
        2496,
        [600, 680, 408, 118, 354, 168, 168],
    ),
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "mai/classic/2026-04-21-5lp-ch-1460.ledger.json"
        ),
        1460,
        [360, 400, 350, 350],
    ),
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "mai/classic/2026-04-21-5lp-pc-1960.ledger.json"
        ),
        1960,
        [360, 640, 140, 420, 200, 200],
    ),
    (
        Path(
            "tests/calculations/combo_damage/fixtures/"
            "mai/classic/2026-04-21-raw-dr-6mp-5285.ledger.json"
        ),
        5285,
        [600, 600, 612, 354, 459, 252, 68, 204, 68, 68, 2000],
    ),
]


def minimal_source_backed_ledger() -> dict:
    return {
        "input_type": "combo_damage_ledger",
        "schema_version": 1,
        "title": "minimal source-backed ledger",
        "source_paths": ["wiki/concepts/terms/damage-scaling.md"],
        "authority": VALID_AUTHORITY,
        "rounding_policy": ROUNDING_POLICY_FLOOR_EACH_HIT,
        "expected_total_damage": 50,
        "hits": [
            {
                "hit_index": 1,
                "move": "example",
                "base_damage": 100,
                "condition_multiplier": "1",
                "effective_scaling": "1/2",
                "source_paths": ["wiki/concepts/terms/damage-scaling.md"],
            }
        ],
    }


def assert_common_authority_contract(authority: dict) -> None:
    assert authority["authority_type"] in {
        "source_backed_ledger",
        "regression_fixture",
        "validated_fixture",
    }
    assert authority["confidence"] in {"low", "medium", "high"}
    assert isinstance(authority["source_paths"], list)
    assert authority["source_paths"]
    assert authority["validation_status"]
    assert authority["review_status"]


def assert_no_aggregated_hit_spans(ledger: dict) -> None:
    for hit in ledger["hits"]:
        hit_span = hit.get("hit_span")
        assert not (
            isinstance(hit_span, str) and AGGREGATED_HIT_SPAN_PATTERN.match(hit_span)
        ), hit


def test_all_combo_damage_fixture_ledgers_are_discovered_and_match_expected() -> None:
    assert ALL_LEDGER_FIXTURES
    for fixture in ALL_LEDGER_FIXTURES:
        ledger = load_ledger(fixture)

        result = calculate_combo_damage(ledger)

        assert result["total_damage"] == ledger["expected_total_damage"], fixture
        assert result["matches_expected"] is True, fixture
        assert_common_authority_contract(ledger["authority"])
        assert_no_aggregated_hit_spans(ledger)


def test_primary_combo_damage_fixture_calculates_expected_damage() -> None:
    ledger = load_ledger(FIXTURE)

    result = calculate_combo_damage(ledger)

    assert result["total_damage"] == 3178
    assert result["expected_total_damage"] == 3178
    assert result["matches_expected"] is True
    assert [row["hit_damage"] for row in result["rows"]] == [
        960,
        544,
        177,
        295,
        510,
        210,
        210,
        272,
    ]
    assert result["rows"][-1]["cumulative_damage"] == 3178


@pytest.mark.parametrize(
    ("fixture", "expected_total", "expected_hit_damage", "expected_trace_marker"),
    JP_FIXTURES,
)
def test_jp_classic_regression_fixtures_match_training_damage(
    fixture: Path,
    expected_total: int,
    expected_hit_damage: list[int],
    expected_trace_marker: str,
) -> None:
    ledger = load_ledger(fixture)

    result = calculate_combo_damage(ledger)

    assert result["total_damage"] == expected_total
    assert result["expected_total_damage"] == expected_total
    assert result["matches_expected"] is True
    assert [row["hit_damage"] for row in result["rows"]] == expected_hit_damage
    assert any(
        expected_trace_marker in row.get("attack_step", "")
        or expected_trace_marker in row.get("scaling_note", "")
        for row in result["rows"]
    )


def test_jp_year1_legacy_fixture_marks_sa3_as_source_backed_move_total() -> None:
    ledger = load_ledger(JP_YEAR1_LEGACY_FIXTURE)

    result = calculate_combo_damage(ledger)

    assert result["total_damage"] == 5790
    assert result["matches_expected"] is True
    notes = ledger["authority"]["notes"]
    assert notes["video_upload_date"] == "2026-04-30"
    assert "before the 2024-02-27 OD Amnesia Battle Change" in notes["fixture_date_basis"]
    sa3_row = result["rows"][-1]
    assert sa3_row["hit_damage"] == 2000
    assert sa3_row["damage_granularity"] == "move_total"
    assert sa3_row["segment_type"] == "super_art_full_move_total"
    assert "internal hit split" in sa3_row["scaling_note"].lower()
    assert "not modeled" in sa3_row["scaling_note"].lower()


@pytest.mark.parametrize(("fixture", "expected_total", "expected_hit_damage"), MAI_FIXTURES)
def test_mai_classic_regression_fixtures_match_training_damage(
    fixture: Path,
    expected_total: int,
    expected_hit_damage: list[int],
) -> None:
    ledger = load_ledger(fixture)

    result = calculate_combo_damage(ledger)

    assert result["total_damage"] == expected_total
    assert result["expected_total_damage"] == expected_total
    assert result["matches_expected"] is True
    assert [row["hit_damage"] for row in result["rows"]] == expected_hit_damage
    if expected_total in {2496, 1960, 5285}:
        assert any("214HP (No Flame)" in row.get("scaling_note", "") for row in result["rows"])


def test_combo_damage_output_preserves_provenance_and_schema_metadata() -> None:
    ledger = load_ledger(FIXTURE)

    result = calculate_combo_damage(ledger)

    assert result["output_type"] == "combo_damage_calculation"
    assert result["schema_version"] == 1
    assert result["calculator"]["name"] == "tools.calculations.combo_damage"
    assert result["calculator"]["version"] == "combo_damage/v1"
    assert result["calculator"]["sympy_version"]
    assert result["source"]["input_sha256"].startswith("sha256:")
    assert result["source"]["source_paths"] == ledger["source_paths"]
    assert result["source"]["authority"] == ledger["authority"]
    assert result["rounding_policy"] == ROUNDING_POLICY_FLOOR_EACH_HIT
    assert result["formula"]["id"] == "sf6_combo_damage_floor_sum_v1"


def test_combo_damage_output_preserves_optional_scaling_trace_fields() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["hits"][0]["attack_step"] = "6th attack"
    ledger["hits"][0]["scaling_note"] = (
        "Character-specific extra scaling advances this hit."
    )

    result = calculate_combo_damage(ledger)

    assert result["rows"][0]["attack_step"] == "6th attack"
    assert (
        result["rows"][0]["scaling_note"]
        == "Character-specific extra scaling advances this hit."
    )


def test_combo_damage_rejects_unsupported_rounding_policy() -> None:
    ledger = load_ledger(FIXTURE)
    ledger["rounding_policy"] = "round_at_end"

    with pytest.raises(ValueError, match="unsupported rounding_policy"):
        calculate_combo_damage(ledger)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_paths", []),
        ("authority", {}),
    ],
)
def test_combo_damage_rejects_ledgers_without_source_backed_top_level_contract(
    field: str,
    value: object,
) -> None:
    ledger = minimal_source_backed_ledger()
    ledger[field] = value

    with pytest.raises(ValueError, match=field):
        calculate_combo_damage(ledger)


@pytest.mark.parametrize("field", ["condition_multiplier", "effective_scaling"])
def test_combo_damage_rejects_hits_without_explicit_scaling_factors(field: str) -> None:
    ledger = minimal_source_backed_ledger()
    del ledger["hits"][0][field]

    with pytest.raises(ValueError, match=field):
        calculate_combo_damage(ledger)


def test_combo_damage_rejects_candidate_authority_for_deterministic_output() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["authority"] = {
        **ledger["authority"],
        "authority_type": "candidate_fixture",
    }

    with pytest.raises(ValueError, match="authority_type"):
        calculate_combo_damage(ledger)


def test_combo_damage_rejects_aggregated_hit_span_ranges() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["hits"][0]["hit_span"] = "1-2"
    ledger["hits"][0]["move"] = "aggregated multi-hit subtotal"

    with pytest.raises(ValueError, match="hit_span"):
        calculate_combo_damage(ledger)


def test_combo_damage_rejects_move_total_segment_without_segment_type() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["hits"][0]["damage_granularity"] = "move_total"

    with pytest.raises(ValueError, match="segment_type"):
        calculate_combo_damage(ledger)


def test_combo_damage_rejects_unknown_damage_granularity() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["hits"][0]["damage_granularity"] = "subtotal"

    with pytest.raises(ValueError, match="damage_granularity"):
        calculate_combo_damage(ledger)


def test_combo_damage_rejects_empty_segment_type() -> None:
    ledger = minimal_source_backed_ledger()
    ledger["hits"][0]["segment_type"] = ""

    with pytest.raises(ValueError, match="segment_type"):
        calculate_combo_damage(ledger)


def test_combo_damage_schema_file_documents_required_output_fields() -> None:
    schema = json.loads(
        Path("wiki/outputs/data/calculations/combo-damage/schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert schema["output_type"] == "combo_damage_calculation_schema"
    assert schema["schema_format"] == "repo_local_contract_descriptor"
    assert "total_damage" in schema["required_output_fields"]
    assert "calculator.sympy_version" in schema["required_output_fields"]
    assert "source.input_sha256" in schema["required_output_fields"]
    assert "source.authority" in schema["required_output_fields"]
    assert "authority_type" in schema["required_authority_fields"]
    assert "regression_fixture" in schema["deterministic_authority_types"]
    assert "candidate_fixture" in schema["non_deterministic_authority_types"]
    assert "attack_step" in schema["optional_hit_trace_fields"]
    assert "scaling_note" in schema["optional_hit_trace_fields"]
    assert "damage_granularity" in schema["optional_hit_trace_fields"]
    assert "segment_type" in schema["optional_hit_trace_fields"]
    assert "move_total" in schema["damage_granularity_values"]
