from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ConfidenceLevel = Literal["high", "medium", "low"]
SourceName = Literal["official", "supercombo"]
DatasetName = Literal["official_raw", "supercombo_enrichment", "derived_metrics"]
PublicationOutcome = Literal["published", "retained_last_known_good", "unavailable", "not_selected", "skipped"]
SourceParseState = Literal["parsed", "blocked", "skipped_fetch_failure", "not_selected"]
BindingClass = Literal["A", "B", "C", "D", "E", "F", "G"]
ConfirmationStatus = Literal["not_required", "confirmed", "unconfirmed"]


class SnapshotMetadata(BaseModel):
    schema_version: str
    source: SourceName
    character_slug: str
    snapshot_id: str
    source_url: str
    final_url: str | None = None
    fetched_at: str
    page_locale: str
    success: bool
    fetcher_name: str
    status_code: int | None = None
    timeout_ms: int
    retry_count: int
    retry_delay_ms: int
    wait_ms: int
    network_idle: bool
    solve_cloudflare: bool
    response_encoding: str | None = None
    page_title: str | None = None
    challenge_detected: bool = False
    raw_sha256: str
    raw_bytes: int
    raw_payload_filename: str
    metadata_filename: str
    error_message: str | None = None


class OfficialNormalizedRecord(BaseModel):
    source: Literal["official"] = "official"
    snapshot_id: str
    source_row_id: str
    character_slug: str
    source_url: str
    page_locale: str
    fetched_at: str
    move_id: str
    move_name: str | None = None
    input: str | None = None
    move_group: str
    startup: str | None = None
    active: str | None = None
    recovery: str | None = None
    total: str | None = None
    hit_adv: str | None = None
    block_adv: str | None = None
    cancel: str | None = None
    damage: str | None = None
    starter_scaling: str | None = None
    drive_gain_hit: str | None = None
    drive_loss_guard: str | None = None
    drive_loss_punish: str | None = None
    sa_gain: str | None = None
    attribute: str | None = None
    notes_official: str | None = None
    raw_row_json: str
    extraction_confidence: ConfidenceLevel = "high"
    manual_review_needed: bool = False
    review_reasons: list[str] = Field(default_factory=list)


class OfficialExportRecord(BaseModel):
    character_slug: str
    move_id: str
    move_name: str | None = None
    input: str | None = None
    move_group: str
    startup: str | None = None
    active: str | None = None
    recovery: str | None = None
    total: str | None = None
    hit_adv: str | None = None
    block_adv: str | None = None
    cancel: str | None = None
    damage: str | None = None
    starter_scaling: str | None = None
    drive_gain_hit: str | None = None
    drive_loss_guard: str | None = None
    drive_loss_punish: str | None = None
    sa_gain: str | None = None
    attribute: str | None = None
    notes_official: str | None = None


class SupercomboNormalizedRecord(BaseModel):
    source: Literal["supercombo"] = "supercombo"
    snapshot_id: str
    source_row_id: str
    raw_source_token: str
    table_index: int
    character_slug: str
    source_url: str
    page_locale: str
    fetched_at: str
    move_id: str | None = None
    move_name: str | None = None
    input: str | None = None
    move_group: str
    binding_class: BindingClass | None = None
    publish_eligible: bool = False
    confirmation_status: ConfirmationStatus | None = None
    binding_confirmed: bool = False
    candidate_move_ids: list[str] = Field(default_factory=list)
    collision_group: str | None = None
    conflicting_move_ids: list[str] = Field(default_factory=list)
    hitconfirm_window: str | None = None
    hitstun: str | None = None
    blockstun: str | None = None
    hitstop: str | None = None
    punish_adv: str | None = None
    perf_parry_adv: str | None = None
    dr_cancel_hit: str | None = None
    dr_cancel_blk: str | None = None
    after_dr_hit: str | None = None
    after_dr_blk: str | None = None
    invuln: str | None = None
    armor: str | None = None
    airborne: str | None = None
    jug_start: str | None = None
    jug_increase: str | None = None
    jug_limit: str | None = None
    proj_speed: str | None = None
    atk_range: str | None = None
    super_gain_blk: str | None = None
    notes_sc: str | None = None
    raw_row_json: str
    extraction_confidence: ConfidenceLevel = "high"
    manual_review_needed: bool = False
    review_reasons: list[str] = Field(default_factory=list)


class SupercomboExportRecord(BaseModel):
    character_slug: str
    move_id: str
    move_name: str | None = None
    input: str | None = None
    move_group: str
    hitconfirm_window: str | None = None
    hitstun: str | None = None
    blockstun: str | None = None
    hitstop: str | None = None
    punish_adv: str | None = None
    perf_parry_adv: str | None = None
    dr_cancel_hit: str | None = None
    dr_cancel_blk: str | None = None
    after_dr_hit: str | None = None
    after_dr_blk: str | None = None
    invuln: str | None = None
    armor: str | None = None
    airborne: str | None = None
    jug_start: str | None = None
    jug_increase: str | None = None
    jug_limit: str | None = None
    proj_speed: str | None = None
    atk_range: str | None = None
    super_gain_blk: str | None = None
    notes_sc: str | None = None


class DerivedNormalizedRecord(BaseModel):
    source: Literal["official"] = "official"
    snapshot_id: str
    source_row_id: str
    character_slug: str
    move_id: str
    punishable_threshold: int | None = None
    is_safe_on_block: bool | None = None
    is_plus_on_hit: bool | None = None
    is_plus_on_block: bool | None = None
    meaty_hit_adv_max: int | None = None
    meaty_block_adv_max: int | None = None
    startup_bucket: Literal["4f_or_faster", "5_to_7", "8_to_10", "11_plus"] | None = None
    simple_punish_adv: int | None = None
    derivation_notes: list[str] = Field(default_factory=list)
    extraction_confidence: ConfidenceLevel = "high"
    manual_review_needed: bool = False
    review_reasons: list[str] = Field(default_factory=list)


class DerivedExportRecord(BaseModel):
    character_slug: str
    move_id: str
    punishable_threshold: int | None = None
    is_safe_on_block: bool | None = None
    is_plus_on_hit: bool | None = None
    is_plus_on_block: bool | None = None
    meaty_hit_adv_max: int | None = None
    meaty_block_adv_max: int | None = None
    startup_bucket: Literal["4f_or_faster", "5_to_7", "8_to_10", "11_plus"] | None = None
    simple_punish_adv: int | None = None
    derivation_notes: list[str] = Field(default_factory=list)


class ManualReviewRecord(BaseModel):
    dataset: DatasetName
    source: SourceName
    snapshot_id: str
    source_row_id: str
    raw_source_token: str | None = None
    reason_codes: list[str] = Field(default_factory=list)
    raw_excerpt: str
    move_id: str | None = None
    character_slug: str | None = None
    move_name: str | None = None
    input: str | None = None
    move_group: str | None = None
    table_index: int | None = None
    binding_class: BindingClass | None = None
    publish_eligible: bool | None = None
    confirmation_status: ConfirmationStatus | None = None
    candidate_move_ids: list[str] = Field(default_factory=list)
    collision_group: str | None = None
    conflicting_move_ids: list[str] = Field(default_factory=list)


class SourceRunStatus(BaseModel):
    source: SourceName
    selected: bool
    snapshot_id: str | None = None
    fetch_success: bool | None = None
    parse_state: SourceParseState = "not_selected"
    row_count: int = 0
    matched_row_count: int = 0
    manual_review_count: int = 0
    blocker_count: int = 0
    blockers: list[str] = Field(default_factory=list)


class DatasetRunStatus(BaseModel):
    dataset_name: DatasetName
    selected: bool
    normalized_record_count: int = 0
    published_record_count: int = 0
    withheld_review_count: int = 0
    publishable: bool = False
    publication_outcome: PublicationOutcome = "not_selected"
    published_run_id: str | None = None
    binding_class_counts: dict[str, int] = Field(default_factory=dict)
    confirmation_status_counts: dict[str, int] = Field(default_factory=dict)


class RunManifest(BaseModel):
    run_id: str
    character_slug: str
    created_at: str
    schema_version: str
    export_contract_version: str
    derivation_rule_version: str
    registry_version: str
    registry_sha256: str
    binding_policy_version: str
    binding_policy_sha256: str
    source_status: dict[str, SourceRunStatus]
    dataset_status: dict[str, DatasetRunStatus]


class PublishedDatasetManifest(BaseModel):
    publication_state: Literal["available", "unavailable"] = "unavailable"
    published_run_id: str | None = None
    published_snapshot_ids: list[str] = Field(default_factory=list)
    published_record_count: int = 0
    withheld_review_count: int = 0
    registry_version: str | None = None
    registry_sha256: str | None = None
    binding_policy_version: str | None = None
    binding_policy_sha256: str | None = None
    content_hash: str | None = None


class SnapshotManifest(BaseModel):
    character_slug: str
    schema_version: str
    export_contract_version: str
    derivation_rule_version: str
    repo_generation_registry_version: str | None = None
    repo_generation_registry_sha256: str | None = None
    repo_generation_binding_policy_version: str | None = None
    repo_generation_binding_policy_sha256: str | None = None
    datasets: dict[str, PublishedDatasetManifest]


def field_names(model_cls: type[BaseModel]) -> list[str]:
    return list(model_cls.model_fields.keys())
