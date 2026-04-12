from __future__ import annotations

from sf6_ingest.registry import LoadedRegistry, OfficialMatchRule, RegistryMove
from sf6_ingest.binding_policy import load_supercombo_binding_policy
from sf6_ingest.core.common import extract_explicit_total, parse_official_active
from sf6_ingest.core.derive import derive_metrics
from sf6_ingest.core.io import decode_snapshot_bytes
from sf6_ingest.core.official import parse_official_snapshot
from sf6_ingest.core.supercombo import parse_supercombo_snapshot
from sf6_ingest.registry import load_registry

from .conftest import build_snapshot_metadata, fixture_bytes, fixture_html
from .supercombo_fixture import (
    build_supercombo_contract_html,
    build_supercombo_contract_html_with_tables,
    build_supercombo_move_table,
)


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


def test_supercombo_parse_accepts_character_specific_prefixes_without_jp_hardcoding() -> None:
    registry = load_registry("luke")
    binding_policy = load_supercombo_binding_policy("luke", registry)
    html = build_supercombo_contract_html_with_tables(
        [
            (
                "Character Data",
                "Character Vitals",
                "Vitals",
                None,
                '<table><tr><th>Vitals</th><th>Luke</th></tr><tr><td>HP</td><td>10000</td></tr></table>',
            ),
            (
                "Normals",
                "Standing Normals",
                "5LP",
                "Luke_5lp",
                build_supercombo_move_table(
                    raw_source_token="Luke_5lp",
                    notation="5LP",
                    move_name="Standing Light Punch",
                    overrides={"Notes": "Luke prefix should parse"},
                    character_label="Luke",
                ),
            ),
            (
                "Normals",
                "Jumping Normals",
                "j.LP",
                "Luke_jlp",
                build_supercombo_move_table(
                    raw_source_token="Luke_jlp",
                    notation="j.LP",
                    move_name="Jumping Light Punch",
                    overrides={"Notes": "Alias drift row"},
                    character_label="Luke",
                ),
            ),
            (
                "Drive Moves",
                "Drive Moves",
                "6HPHK Recovery",
                "Luke_6hphk_recovery",
                build_supercombo_move_table(
                    raw_source_token="Luke_6hphk_recovery",
                    notation="6HPHK",
                    move_name="Battering Ram (Recovery)",
                    overrides={"Invuln": "1-20 Full", "Notes": "Confirmed Luke recovery row"},
                    character_label="Luke",
                ),
            ),
            (
                "Drive Moves",
                "Drive Moves",
                "MPMK 66 DRC",
                "luke_mpmk_66_drc",
                build_supercombo_move_table(
                    raw_source_token="luke_mpmk_66_drc",
                    notation="66",
                    move_name="Drive Rush Cancel",
                    overrides={"After DR Hit": "+12", "After DR Blk": "+8"},
                    character_label="Luke",
                ),
            ),
            (
                "Drive Moves",
                "Drive Moves",
                "MPMK",
                "Luke_mpmk",
                build_supercombo_move_table(
                    raw_source_token="Luke_mpmk",
                    notation="MPMK",
                    move_name="Drive Parry",
                    overrides={"Notes": "One-to-many withheld"},
                    character_label="Luke",
                ),
            ),
            (
                "Super Arts",
                "Super Arts",
                "236236K (CA)",
                "Luke_236236k(ca)",
                build_supercombo_move_table(
                    raw_source_token="Luke_236236k(ca)",
                    notation="236236K",
                    move_name="Pale Rider (CA)",
                    overrides={"Punish Advantage": "KD +44", "Notes": "CA suffix must be preserved"},
                    character_label="Luke",
                ),
            ),
            (
                "Taunts",
                "Taunts",
                "5PPPKKK",
                "Luke_5pppkkk",
                build_supercombo_move_table(
                    raw_source_token="Luke_5pppkkk",
                    notation="5PPPKKK",
                    move_name="Neutral Taunt",
                    overrides={"Notes": "Excluded taunt row"},
                    character_label="Luke",
                ),
            ),
        ],
        character_label="Luke",
        page_title="Street Fighter 6/Luke/Data - SuperCombo Wiki",
    )
    metadata = build_snapshot_metadata(
        source="supercombo",
        character_slug="luke",
        snapshot_id="20260310T120000Z-luke0001",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-03-10T12:00:00Z",
        success=True,
        page_locale="en",
        page_title="Street Fighter 6/Luke/Data - SuperCombo Wiki",
    )

    records, status = parse_supercombo_snapshot(metadata, html, registry, binding_policy)

    assert status.parse_state == "parsed"
    assert status.blocker_count == 0
    assert status.row_count == 7
    by_token = {record.raw_source_token: record for record in records}
    assert by_token["Luke_5lp"].move_id == "luke_001_5lp"
    assert by_token["Luke_jlp"].binding_class == "B"
    assert by_token["Luke_6hphk_recovery"].binding_class == "F"
    assert by_token["Luke_6hphk_recovery"].confirmation_status == "confirmed"
    assert by_token["luke_mpmk_66_drc"].move_id == "luke_076_cancel_drive_rush"
    assert by_token["Luke_mpmk"].candidate_move_ids == [
        "luke_072_drive_parry",
        "luke_073_just_parry_strike",
        "luke_074_just_parry_projectile",
    ]
    assert by_token["Luke_236236k(ca)"].binding_class == "C"
    assert by_token["Luke_5pppkkk"].binding_class == "G"


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


def test_official_parse_uses_full_label_name_key_for_contextual_followups() -> None:
    registry = LoadedRegistry(
        version="2.1.0",
        sha256="0" * 64,
        moves=[
            RegistryMove(
                move_id="ken_054_6_k_after_od_tatsu",
                group="specials",
                sort_key=54,
                official_match=OfficialMatchRule(
                    section="specials",
                    icon_tokens=["6", "K"],
                    name_key="火砕蹴_od風鎌蹴り後に",
                ),
            ),
            RegistryMove(
                move_id="ken_057_6_k_after_od_jinrai",
                group="specials",
                sort_key=57,
                official_match=OfficialMatchRule(
                    section="specials",
                    icon_tokens=["6", "K"],
                    name_key="火砕蹴_od轟雷落とし後に",
                ),
            ),
        ],
    )
    html = """
<!doctype html>
<html lang="ja">
  <body>
    <table>
      <thead>
        <tr>
          <th>技名</th><th>動作フレーム 発生</th><th>持続</th><th>硬直</th><th>ヒット</th><th>ガード</th><th>キャンセル</th><th>ダメージ</th><th>コンボ補正値</th><th>Dゲージ増加 ヒット</th><th>Dゲージ減少 ガード</th><th>Dゲージ減少 パニッシュカウンター</th><th>SAゲージ増加</th><th>属性</th><th>備考</th>
        </tr>
      </thead>
      <tbody>
        <tr><td colspan="15">必殺技</td></tr>
        <tr>
          <td><span class="frame_arts__name">火砕蹴</span>（OD風鎌蹴り後に）<p><img src="/6/assets/images/common/controller/key-r.png"/><img src="/6/assets/images/common/controller/key-plus.png"/><img src="/6/assets/images/common/controller/icon_kick.png"/></p></td>
          <td>15</td><td>15-17</td><td>29</td><td>D</td><td>-12</td><td>SA2</td><td>500</td><td><ul><li>始動補正40%</li></ul></td><td>0</td><td>-5000</td><td>-5000</td><td>600</td><td>上</td><td><ul><li>動作中常に被パニッシュカウンター判定</li></ul></td>
        </tr>
        <tr>
          <td><span class="frame_arts__name">火砕蹴</span>（OD轟雷落とし後に）<p><img src="/6/assets/images/common/controller/key-r.png"/><img src="/6/assets/images/common/controller/key-plus.png"/><img src="/6/assets/images/common/controller/icon_kick.png"/></p></td>
          <td>11</td><td>11-13</td><td>29</td><td>D</td><td>-12</td><td>SA2</td><td>500</td><td><ul><li>始動補正40%</li></ul></td><td>0</td><td>-5000</td><td>-5000</td><td>600</td><td>上</td><td><ul><li>動作中常に被パニッシュカウンター判定</li></ul></td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
"""
    metadata = build_snapshot_metadata(
        source="official",
        character_slug="ken",
        snapshot_id="20260412T000000Z-kendup01",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-04-12T00:00:00Z",
        success=True,
        page_locale="ja-jp",
        page_title="Ken フレームデータ",
    )

    records, status = parse_official_snapshot(metadata, html, registry)

    assert status.parse_state == "parsed"
    assert status.blocker_count == 0
    assert [record.move_id for record in records] == [
        "ken_054_6_k_after_od_tatsu",
        "ken_057_6_k_after_od_jinrai",
    ]


def test_official_parse_matches_contextual_rows_without_input_icons() -> None:
    registry = LoadedRegistry(
        version="2.1.0",
        sha256="1" * 64,
        moves=[
            RegistryMove(
                move_id="cammy_046_razor_edge_slicer",
                group="specials",
                sort_key=46,
                official_match=OfficialMatchRule(
                    section="specials",
                    icon_tokens=[],
                    name_key="レイザーエッジスライサー_フーリガンコンビネーション中に_入力なし",
                ),
            ),
        ],
    )
    html = """
<!doctype html>
<html lang="ja">
  <body>
    <table>
      <thead>
        <tr>
          <th>技名</th><th>動作フレーム 発生</th><th>持続</th><th>硬直</th><th>ヒット</th><th>ガード</th><th>キャンセル</th><th>ダメージ</th><th>コンボ補正値</th><th>Dゲージ増加 ヒット</th><th>Dゲージ減少 ガード</th><th>Dゲージ減少 パニッシュカウンター</th><th>SAゲージ増加</th><th>属性</th><th>備考</th>
        </tr>
      </thead>
      <tbody>
        <tr><td colspan="15">必殺技</td></tr>
        <tr>
          <td><span class="frame_arts__name">レイザーエッジスライサー</span>（フーリガンコンビネーション中に）（入力なし）</td>
          <td>10</td><td>10-18</td><td>13</td><td>D</td><td>2</td><td>SA3</td><td>1000</td><td><ul><li>始動補正20%</li></ul></td><td>2500</td><td>-3000</td><td>-7000</td><td>1000</td><td>下</td><td></td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
"""
    metadata = build_snapshot_metadata(
        source="official",
        character_slug="cammy",
        snapshot_id="20260412T000000Z-cammydup1",
        raw_bytes=html.encode("utf-8"),
        fetched_at="2026-04-12T00:00:00Z",
        success=True,
        page_locale="ja-jp",
        page_title="Cammy フレームデータ",
    )

    records, status = parse_official_snapshot(metadata, html, registry)

    assert status.parse_state == "parsed"
    assert status.blocker_count == 0
    assert [record.move_id for record in records] == ["cammy_046_razor_edge_slicer"]
