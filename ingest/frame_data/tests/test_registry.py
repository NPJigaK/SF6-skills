from __future__ import annotations

from sf6_ingest.binding_policy import load_supercombo_binding_policy
from sf6_ingest.core.common import normalize_name_key
from sf6_ingest.registry import load_registry


def test_registry_is_authoritative_and_structured() -> None:
    registry = load_registry("jp")
    assert registry.version == "2.1.0"
    assert len(registry.moves) == 69
    assert len(registry.by_move_id) == 69
    assert len(registry.sha256) == 64
    assert registry.match_official("normals", ["5", "LP"], normalize_name_key("dummy"))[0].move_id == "jp_001_5lp"


def test_binding_policy_is_exact_token_based_and_auditable() -> None:
    registry = load_registry("jp")
    policy = load_supercombo_binding_policy("jp", registry)

    assert policy.version == "1.0.0"
    assert len(policy.entries) == 64
    assert len(policy.sha256) == 64
    assert policy.lookup("jp_jlp").binding_class == "B"
    assert policy.lookup("jp_236236k(ca)").binding_class == "C"
    assert policy.lookup("jp_6hphk_recovery").binding_class == "F"
    assert policy.lookup("jp_22pp").candidate_move_ids == [
        "jp_030_22pp_triglav_od_weak",
        "jp_031_22pp_triglav_od_medium",
        "jp_032_22pp_triglav_od_heavy",
    ]
    assert policy.lookup("jp_214p_214hp").collision_group == "jp_vihat_cheni_followup"
    assert policy.lookup("jp_22k_bomb").binding_class == "G"


def test_luke_registry_and_binding_policy_are_loaded_without_jp_specific_contracts() -> None:
    registry = load_registry("luke")
    policy = load_supercombo_binding_policy("luke", registry)

    assert registry.version == "2.1.0"
    assert len(registry.moves) == 76
    assert len(registry.by_move_id) == 76
    assert len(registry.sha256) == 64
    assert registry.match_official("normals", ["5", "LP"], normalize_name_key("立ち弱P（ファーストスティンガー）"))[0].move_id == "luke_001_5lp"

    assert policy.version == "1.0.0"
    assert len(policy.entries) == 74
    assert len(policy.sha256) == 64
    assert policy.lookup("Luke_jlp").binding_class == "B"
    assert policy.lookup("Luke_236236k(ca)").binding_class == "C"
    assert policy.lookup("Luke_6hphk_recovery").binding_class == "F"
    assert policy.lookup("Luke_mpmk").candidate_move_ids == [
        "luke_072_drive_parry",
        "luke_073_just_parry_strike",
        "luke_074_just_parry_projectile",
    ]
    assert policy.lookup("Luke_5pppkkk").binding_class == "G"
