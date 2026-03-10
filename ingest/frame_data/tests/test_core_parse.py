from __future__ import annotations

from sf6_ingest.binding_policy import load_supercombo_binding_policy
from sf6_ingest.core.common import extract_explicit_total, parse_official_active
from sf6_ingest.core.derive import derive_metrics
from sf6_ingest.core.io import decode_snapshot_bytes
from sf6_ingest.core.official import parse_official_snapshot
from sf6_ingest.core.supercombo import parse_supercombo_snapshot
from sf6_ingest.registry import load_registry

from .conftest import build_snapshot_metadata, fixture_bytes, fixture_html
from .supercombo_fixture import build_supercombo_contract_html


def test_official_parse_handles_total_active_and_structured_columns() -> None:
    registry = load_registry("jp")
    html = fixture_html("official_success.html")
    metadata = build_snapshot_metadata(
        source="official",
        snapshot_id="20260308T000000Z-11111111",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-03-08T00:00:00Z",
        success=True,
        page_locale="ja-jp",
        page_title="JP 繝輔Ξ繝ｼ繝繝・・繧ｿ",
    )

    records, status = parse_official_snapshot(metadata, html, registry)

    assert status.parse_state == "parsed"
    assert status.blocker_count == 0
    assert [record.move_id for record in records] == [
        "jp_001_5lp",
        "jp_065_drive_parry",
        "jp_068_parry_drive_rush",
    ]

    five_lp = records[0]
    assert five_lp.total is None
    assert five_lp.drive_gain_hit == "250"
    assert five_lp.drive_loss_guard == "-500"
    assert five_lp.drive_loss_punish == "-2000"
    assert five_lp.sa_gain == "300"
    assert five_lp.attribute is not None

    drive_parry = records[1]
    assert drive_parry.manual_review_needed is True
    assert any(reason.startswith("official active parse ambiguous:") for reason in drive_parry.review_reasons)

    parry_drive_rush = records[2]
    assert parry_drive_rush.input == "66"
    assert parry_drive_rush.total == "45"
    assert parry_drive_rush.manual_review_needed is False

    derived = derive_metrics(records)
    five_lp_derived = derived[0]
    assert five_lp_derived.source == "official"
    assert five_lp_derived.source_row_id == five_lp.source_row_id
    assert five_lp_derived.punishable_threshold == 2
    assert five_lp_derived.is_safe_on_block is True
    assert five_lp_derived.is_plus_on_hit is True
    assert five_lp_derived.startup_bucket == "5_to_7"
    assert five_lp_derived.meaty_block_adv_max == 0


def test_supercombo_parse_uses_live_contract_and_binding_policy() -> None:
    registry = load_registry("jp")
    binding_policy = load_supercombo_binding_policy("jp", registry)
    html = build_supercombo_contract_html()
    metadata = build_snapshot_metadata(
        source="supercombo",
        snapshot_id="20260308T000100Z-22222222",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-03-08T00:01:00Z",
        success=True,
        page_locale="en",
        page_title="Street Fighter 6/JP/Data - SuperCombo Wiki",
    )

    records, status = parse_supercombo_snapshot(metadata, html, registry, binding_policy)

    assert status.parse_state == "parsed"
    assert status.blocker_count == 0
    assert status.row_count == 8
    assert len(records) == 8

    by_token = {record.raw_source_token: record for record in records}
    assert by_token["jp_5lp"].source_row_id == "20260308T000100Z-22222222:t001:jp_5lp"
    assert by_token["jp_5lp"].binding_class == "A"
    assert by_token["jp_jlp"].binding_class == "B"
    assert by_token["jp_236236k(ca)"].binding_class == "C"
    assert by_token["jp_236236k(ca)"].move_id == "jp_056_ca_236236k"
    assert by_token["jp_6hphk_recovery"].binding_class == "F"
    assert by_token["jp_6hphk_recovery"].confirmation_status == "confirmed"
    assert by_token["jp_6hphk_recovery"].publish_eligible is True
    assert by_token["jp_mpmk_66_drc"].move_id == "jp_069_cancel_drive_rush"
    assert by_token["jp_22pp"].binding_class == "D"
    assert by_token["jp_22pp"].candidate_move_ids == [
        "jp_030_22pp_triglav_od_weak",
        "jp_031_22pp_triglav_od_medium",
        "jp_032_22pp_triglav_od_heavy",
    ]
    assert by_token["jp_214p_214hp"].binding_class == "E"
    assert by_token["jp_214p_214hp"].collision_group == "jp_vihat_cheni_followup"
    assert by_token["jp_22k_bomb"].binding_class == "G"
    assert by_token["jp_22k_bomb"].move_id is None


def test_supercombo_label_mismatch_withholds_row_without_snapshot_block() -> None:
    registry = load_registry("jp")
    binding_policy = load_supercombo_binding_policy("jp", registry)
    html = build_supercombo_contract_html().replace("Hitconfirm Window", "Hitconfirm Surprise", 1)
    metadata = build_snapshot_metadata(
        source="supercombo",
        snapshot_id="20260308T000100Z-22222222",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-03-08T00:01:00Z",
        success=True,
        page_locale="en",
        page_title="Street Fighter 6/JP/Data - SuperCombo Wiki",
    )

    records, status = parse_supercombo_snapshot(metadata, html, registry, binding_policy)

    assert status.parse_state == "parsed"
    row = next(record for record in records if record.raw_source_token == "jp_5lp")
    assert row.manual_review_needed is True
    assert row.hitconfirm_window is None
    assert any(reason.startswith("supercombo label mismatch") for reason in row.review_reasons)


def test_decode_snapshot_bytes_is_deterministic() -> None:
    raw_bytes = fixture_bytes("official_success.html")
    assert decode_snapshot_bytes(raw_bytes, "utf-8") == fixture_html("official_success.html")


def test_total_and_active_helpers_are_strict() -> None:
    assert extract_explicit_total("全体 45") == "45"
    assert extract_explicit_total("10") is None
    active = parse_official_active("[※2] 1-12")
    assert active.kind == "range"
    assert active.frames == 12
    assert active.ambiguous is True
