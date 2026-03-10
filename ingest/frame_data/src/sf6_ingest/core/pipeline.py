from __future__ import annotations

import json
from collections import Counter
from typing import Iterable

from ..binding_policy import LoadedSupercomboBindingPolicy, load_supercombo_binding_policy
from ..config import repo_root as configured_repo_root
from ..registry import LoadedRegistry, load_registry
from ..schemas import (
    DatasetRunStatus,
    DerivedExportRecord,
    DerivedNormalizedRecord,
    ManualReviewRecord,
    OfficialExportRecord,
    OfficialNormalizedRecord,
    PublicationOutcome,
    PublishedDatasetManifest,
    RunManifest,
    SnapshotManifest,
    SourceRunStatus,
    SupercomboExportRecord,
    SupercomboNormalizedRecord,
)
from ..versioning import DERIVATION_RULE_VERSION, EXPORT_CONTRACT_VERSION, SCHEMA_VERSION
from .common import sha256_hex, slugify, stable_json_dumps, unique_run_token, utc_now
from .derive import derive_metrics
from .io import (
    exports_dir,
    load_run_manifest,
    load_snapshot,
    load_snapshot_manifest,
    normalized_run_dir,
    read_model_rows,
    remove_export_dataset,
    save_run_manifest,
    save_snapshot_manifest,
    write_export_dataset,
    write_model_rows,
)
from .official import parse_official_snapshot
from .supercombo import parse_supercombo_snapshot


class PublicationSummary:
    def __init__(self, run_id: str, dataset_states: dict[str, str]) -> None:
        self.run_id = run_id
        self.dataset_states = dataset_states


def parse_from_raw(character_slug: str, snapshot_ids: dict[str, str], base_repo_root=None) -> str:
    repo_root = base_repo_root or configured_repo_root()
    registry = load_registry(character_slug)
    binding_policy = load_supercombo_binding_policy(character_slug, registry)
    run_id = _build_run_id(snapshot_ids)
    run_dir = normalized_run_dir(repo_root, character_slug, run_id)

    source_status = {
        "official": SourceRunStatus(source="official", selected="official" in snapshot_ids),
        "supercombo": SourceRunStatus(source="supercombo", selected="supercombo" in snapshot_ids),
    }
    official_records: list[OfficialNormalizedRecord] = []
    supercombo_records: list[SupercomboNormalizedRecord] = []

    if "official" in snapshot_ids:
        snapshot = load_snapshot(repo_root, "official", character_slug, snapshot_ids["official"])
        if snapshot.metadata.success:
            official_records, source_status["official"] = parse_official_snapshot(snapshot.metadata, snapshot.html, registry)
        else:
            source_status["official"] = _skipped_fetch_failure("official", snapshot.metadata.snapshot_id)

    if "supercombo" in snapshot_ids:
        snapshot = load_snapshot(repo_root, "supercombo", character_slug, snapshot_ids["supercombo"])
        if snapshot.metadata.success:
            supercombo_records, source_status["supercombo"] = parse_supercombo_snapshot(
                snapshot.metadata,
                snapshot.html,
                registry,
                binding_policy,
            )
        else:
            source_status["supercombo"] = _skipped_fetch_failure("supercombo", snapshot.metadata.snapshot_id)

    derived_records = derive_metrics(official_records)
    dataset_status = _dataset_status(source_status, official_records, supercombo_records, derived_records)

    if source_status["official"].selected:
        ordered_official = _sort_models(official_records, registry)
        ordered_derived = _sort_models(derived_records, registry)
        write_model_rows(
            run_dir / "official_raw",
            ordered_official,
            OfficialNormalizedRecord,
            _manual_review_only(ordered_official),
        )
        write_model_rows(
            run_dir / "derived_metrics",
            ordered_derived,
            DerivedNormalizedRecord,
            _manual_review_only(ordered_derived),
        )
    if source_status["supercombo"].selected:
        ordered_supercombo = _sort_models(supercombo_records, registry)
        write_model_rows(
            run_dir / "supercombo_enrichment",
            ordered_supercombo,
            SupercomboNormalizedRecord,
            _manual_review_only(ordered_supercombo),
        )

    manifest = RunManifest.model_validate(
        {
            "run_id": run_id,
            "character_slug": character_slug,
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "export_contract_version": EXPORT_CONTRACT_VERSION,
            "derivation_rule_version": DERIVATION_RULE_VERSION,
            "registry_version": registry.version,
            "registry_sha256": registry.sha256,
            "binding_policy_version": binding_policy.version,
            "binding_policy_sha256": binding_policy.sha256,
            "source_status": source_status,
            "dataset_status": dataset_status,
        }
    )
    save_run_manifest(run_dir / "run_manifest.json", manifest)
    return run_id


def publish_run(character_slug: str, run_id: str, base_repo_root=None) -> PublicationSummary:
    repo_root = base_repo_root or configured_repo_root()
    registry = load_registry(character_slug)
    binding_policy = load_supercombo_binding_policy(character_slug, registry)
    run_dir = normalized_run_dir(repo_root, character_slug, run_id)
    manifest_path = run_dir / "run_manifest.json"
    manifest = load_run_manifest(manifest_path)
    _assert_parse_inputs_unchanged(manifest, registry, binding_policy)

    export_root = exports_dir(repo_root, character_slug)
    snapshot_manifest_path = export_root / "snapshot_manifest.json"
    snapshot_manifest = load_snapshot_manifest(snapshot_manifest_path, character_slug)
    snapshot_manifest.repo_generation_registry_version = registry.version
    snapshot_manifest.repo_generation_registry_sha256 = registry.sha256
    snapshot_manifest.repo_generation_binding_policy_version = binding_policy.version
    snapshot_manifest.repo_generation_binding_policy_sha256 = binding_policy.sha256

    previous_official_move_ids = _published_move_ids(
        export_root,
        "official_raw",
        OfficialExportRecord,
        snapshot_manifest.datasets["official_raw"],
    )
    previous_supercombo_move_ids = _published_move_ids(
        export_root,
        "supercombo_enrichment",
        SupercomboExportRecord,
        snapshot_manifest.datasets["supercombo_enrichment"],
    )

    official_outcome = _publish_official(manifest, run_dir, export_root, snapshot_manifest, registry)
    authoritative_official_move_ids = _published_move_ids(
        export_root,
        "official_raw",
        OfficialExportRecord,
        snapshot_manifest.datasets["official_raw"],
    )
    official_anchor_changed = previous_official_move_ids != authoritative_official_move_ids

    dataset_states = {
        "official_raw": official_outcome,
        "supercombo_enrichment": _publish_supercombo(
            manifest,
            run_dir,
            export_root,
            snapshot_manifest,
            registry,
            binding_policy,
            authoritative_official_move_ids,
            official_anchor_changed,
            previous_supercombo_move_ids,
        ),
        "derived_metrics": _publish_derived(manifest, run_dir, export_root, snapshot_manifest, registry),
    }
    supercombo_manifest = snapshot_manifest.datasets["supercombo_enrichment"]
    if supercombo_manifest.publication_state == "unavailable":
        _mark_supercombo_unavailable(supercombo_manifest, manifest, binding_policy)
    save_run_manifest(manifest_path, manifest)
    save_snapshot_manifest(snapshot_manifest_path, snapshot_manifest)
    return PublicationSummary(run_id=run_id, dataset_states=dataset_states)


def _publish_official(
    manifest: RunManifest,
    run_dir,
    export_root,
    snapshot_manifest: SnapshotManifest,
    registry: LoadedRegistry,
) -> str:
    status = manifest.dataset_status["official_raw"]
    published_manifest = snapshot_manifest.datasets["official_raw"]
    if not status.publishable:
        status.publication_outcome = _retain_or_unavailable(status, published_manifest)
        return status.publication_outcome
    records = _sort_models(read_model_rows(run_dir / "official_raw" / "records.json", OfficialNormalizedRecord), registry)
    safe_records = _safe_only(records)
    review_rows = _build_manual_review_records("official_raw", _manual_review_only(records))
    hash_value = write_export_dataset(
        export_root,
        "official_raw",
        [_to_official_export(record) for record in safe_records],
        OfficialExportRecord,
        review_rows,
        ManualReviewRecord,
    )
    _update_snapshot_manifest_dataset(
        dataset_name="official_raw",
        dataset_manifest=published_manifest,
        manifest=manifest,
        hash_value=hash_value,
        published_snapshot_ids=[manifest.source_status["official"].snapshot_id or ""],
        published_record_count=len(safe_records),
        withheld_review_count=len(review_rows),
    )
    status.publication_outcome = "published"
    status.published_run_id = published_manifest.published_run_id
    status.published_record_count = len(safe_records)
    status.withheld_review_count = len(review_rows)
    return "published"


def _publish_supercombo(
    manifest: RunManifest,
    run_dir,
    export_root,
    snapshot_manifest: SnapshotManifest,
    registry: LoadedRegistry,
    binding_policy: LoadedSupercomboBindingPolicy,
    authoritative_official_move_ids: set[str],
    official_anchor_changed: bool,
    previous_supercombo_move_ids: set[str],
) -> str:
    status = manifest.dataset_status["supercombo_enrichment"]
    published_manifest = snapshot_manifest.datasets["supercombo_enrichment"]
    records: list[SupercomboNormalizedRecord] = []
    if status.selected:
        records = _sort_models(
            read_model_rows(run_dir / "supercombo_enrichment" / "records.json", SupercomboNormalizedRecord),
            registry,
        )

    main_records, withheld_records, extra_review_reasons = _split_supercombo_records(
        records,
        authoritative_official_move_ids,
    )
    review_rows = _build_manual_review_records(
        "supercombo_enrichment",
        withheld_records,
        extra_review_reasons_by_source_row_id=extra_review_reasons,
    )
    status.published_record_count = len(main_records)
    status.withheld_review_count = len(withheld_records)
    status.publishable = (
        status.selected
        and manifest.source_status["supercombo"].fetch_success is True
        and manifest.source_status["supercombo"].blocker_count == 0
        and len(main_records) > 0
    )

    if status.publishable:
        hash_value = write_export_dataset(
            export_root,
            "supercombo_enrichment",
            [_to_supercombo_export(record) for record in main_records],
            SupercomboExportRecord,
            review_rows,
            ManualReviewRecord,
        )
        _update_snapshot_manifest_dataset(
            dataset_name="supercombo_enrichment",
            dataset_manifest=published_manifest,
            manifest=manifest,
            hash_value=hash_value,
            published_snapshot_ids=[manifest.source_status["supercombo"].snapshot_id or ""],
            published_record_count=len(main_records),
            withheld_review_count=len(review_rows),
        )
        status.publication_outcome = "published"
        status.published_run_id = published_manifest.published_run_id
        return "published"

    if _can_keep_supercombo_lkg(
        published_manifest,
        authoritative_official_move_ids,
        official_anchor_changed,
        previous_supercombo_move_ids,
    ):
        status.published_run_id = published_manifest.published_run_id
        status.publication_outcome = "retained_last_known_good" if status.selected else "not_selected"
        return status.publication_outcome

    if published_manifest.publication_state == "available" or status.selected:
        remove_export_dataset(export_root, "supercombo_enrichment")
        _mark_supercombo_unavailable(published_manifest, manifest, binding_policy)
        status.published_run_id = None
        status.publication_outcome = "unavailable"
        return "unavailable"

    status.published_run_id = None
    status.publication_outcome = "not_selected"
    return "not_selected"


def _publish_derived(
    manifest: RunManifest,
    run_dir,
    export_root,
    snapshot_manifest: SnapshotManifest,
    registry: LoadedRegistry,
) -> str:
    status = manifest.dataset_status["derived_metrics"]
    published_manifest = snapshot_manifest.datasets["derived_metrics"]
    if not status.publishable:
        status.publication_outcome = _retain_or_unavailable(status, published_manifest)
        return status.publication_outcome
    records = _sort_models(read_model_rows(run_dir / "derived_metrics" / "records.json", DerivedNormalizedRecord), registry)
    safe_records = _safe_only(records)
    review_rows = _build_manual_review_records("derived_metrics", _manual_review_only(records))
    hash_value = write_export_dataset(
        export_root,
        "derived_metrics",
        [_to_derived_export(record) for record in safe_records],
        DerivedExportRecord,
        review_rows,
        ManualReviewRecord,
    )
    _update_snapshot_manifest_dataset(
        dataset_name="derived_metrics",
        dataset_manifest=published_manifest,
        manifest=manifest,
        hash_value=hash_value,
        published_snapshot_ids=[manifest.source_status["official"].snapshot_id or ""],
        published_record_count=len(safe_records),
        withheld_review_count=len(review_rows),
    )
    status.publication_outcome = "published"
    status.published_run_id = published_manifest.published_run_id
    status.published_record_count = len(safe_records)
    status.withheld_review_count = len(review_rows)
    return "published"


def _retain_or_unavailable(status: DatasetRunStatus, dataset_manifest: PublishedDatasetManifest) -> PublicationOutcome:
    if not status.selected:
        status.published_run_id = None
        return "not_selected"
    if dataset_manifest.publication_state == "available":
        status.published_run_id = dataset_manifest.published_run_id
        return "retained_last_known_good"
    status.published_run_id = None
    return "unavailable"


def _dataset_status(
    source_status: dict[str, SourceRunStatus],
    official_records: list[OfficialNormalizedRecord],
    supercombo_records: list[SupercomboNormalizedRecord],
    derived_records: list[DerivedNormalizedRecord],
) -> dict[str, DatasetRunStatus]:
    official_publishable = (
        source_status["official"].selected
        and source_status["official"].fetch_success is True
        and source_status["official"].blocker_count == 0
    )
    supercombo_main_records = _publishable_supercombo_only(supercombo_records)
    supercombo_publishable = (
        source_status["supercombo"].selected
        and source_status["supercombo"].fetch_success is True
        and source_status["supercombo"].blocker_count == 0
        and len(supercombo_main_records) > 0
    )
    return {
        "official_raw": _build_dataset_status("official_raw", source_status["official"].selected, official_publishable, official_records),
        "supercombo_enrichment": _build_dataset_status(
            "supercombo_enrichment",
            source_status["supercombo"].selected,
            supercombo_publishable,
            supercombo_records,
        ),
        "derived_metrics": _build_dataset_status("derived_metrics", source_status["official"].selected, official_publishable, derived_records),
    }


def _build_dataset_status(dataset_name: str, selected: bool, publishable: bool, records: list) -> DatasetRunStatus:
    if dataset_name == "supercombo_enrichment":
        published_rows = _publishable_supercombo_only(records)
        binding_counter = Counter(record.binding_class for record in records if getattr(record, "binding_class", None))
        confirmation_counter = Counter(
            record.confirmation_status for record in records if getattr(record, "confirmation_status", None)
        )
        withheld_review_count = len(records) - len(published_rows)
        published_record_count = len(published_rows)
        return DatasetRunStatus.model_validate(
            {
                "dataset_name": dataset_name,
                "selected": selected,
                "normalized_record_count": len(records),
                "published_record_count": published_record_count,
                "withheld_review_count": withheld_review_count,
                "publishable": publishable,
                "publication_outcome": "skipped" if selected else "not_selected",
                "published_run_id": None,
                "binding_class_counts": dict(sorted(binding_counter.items())),
                "confirmation_status_counts": dict(sorted(confirmation_counter.items())),
            }
        )

    withheld_review_count = sum(1 for record in records if getattr(record, "manual_review_needed", False))
    published_record_count = len(records) - withheld_review_count
    return DatasetRunStatus.model_validate(
        {
            "dataset_name": dataset_name,
            "selected": selected,
            "normalized_record_count": len(records),
            "published_record_count": published_record_count,
            "withheld_review_count": withheld_review_count,
            "publishable": publishable,
            "publication_outcome": "skipped" if selected else "not_selected",
            "published_run_id": None,
        }
    )


def _skipped_fetch_failure(source: str, snapshot_id: str) -> SourceRunStatus:
    return SourceRunStatus.model_validate(
        {
            "source": source,
            "selected": True,
            "snapshot_id": snapshot_id,
            "fetch_success": False,
            "parse_state": "skipped_fetch_failure",
            "blockers": [f"{source} fetch failed"],
            "blocker_count": 1,
        }
    )


def _build_run_id(snapshot_ids: dict[str, str]) -> str:
    digest = sha256_hex(json.dumps(snapshot_ids, sort_keys=True))[:8]
    return f"{unique_run_token()}-{digest}"


def _sort_models(records: Iterable, registry: LoadedRegistry) -> list:
    def sort_tuple(record):
        move_id = getattr(record, "move_id", None)
        return (
            registry.sort_key_by_move_id.get(move_id, 10_000),
            move_id or "",
            getattr(record, "raw_source_token", "") or "",
            getattr(record, "source_row_id", ""),
        )

    return sorted(records, key=sort_tuple)


def _manual_review_only(records: Iterable) -> list:
    return [record for record in records if getattr(record, "manual_review_needed", False)]


def _safe_only(records: Iterable) -> list:
    return [record for record in records if not getattr(record, "manual_review_needed", False)]


def _publishable_supercombo_only(records: Iterable[SupercomboNormalizedRecord]) -> list[SupercomboNormalizedRecord]:
    return [record for record in records if _is_supercombo_binding_publishable(record)]


def _is_supercombo_binding_publishable(record: SupercomboNormalizedRecord) -> bool:
    return (
        not record.manual_review_needed
        and record.move_id is not None
        and record.binding_class in {"A", "B", "C", "F"}
        and record.publish_eligible
        and (record.binding_class != "F" or record.confirmation_status == "confirmed")
    )


def _split_supercombo_records(
    records: Iterable[SupercomboNormalizedRecord],
    authoritative_official_move_ids: set[str],
) -> tuple[list[SupercomboNormalizedRecord], list[SupercomboNormalizedRecord], dict[str, list[str]]]:
    main_records: list[SupercomboNormalizedRecord] = []
    withheld_records: list[SupercomboNormalizedRecord] = []
    extra_review_reasons: dict[str, list[str]] = {}

    for record in records:
        binding_publishable = _is_supercombo_binding_publishable(record)
        has_official_anchor = binding_publishable and record.move_id in authoritative_official_move_ids
        if has_official_anchor:
            main_records.append(record)
            continue
        withheld_records.append(record)
        if binding_publishable and record.move_id not in authoritative_official_move_ids:
            extra_review_reasons[record.source_row_id] = ["supercombo missing official safe row"]

    return main_records, withheld_records, extra_review_reasons


def _can_keep_supercombo_lkg(
    published_manifest: PublishedDatasetManifest,
    authoritative_official_move_ids: set[str],
    official_anchor_changed: bool,
    previous_supercombo_move_ids: set[str],
) -> bool:
    if published_manifest.publication_state != "available":
        return False
    if not authoritative_official_move_ids:
        return False
    if not official_anchor_changed:
        return True
    return previous_supercombo_move_ids.issubset(authoritative_official_move_ids)


def _published_move_ids(
    export_root,
    stem: str,
    model_cls: type[OfficialExportRecord] | type[SupercomboExportRecord],
    dataset_manifest: PublishedDatasetManifest,
) -> set[str]:
    if dataset_manifest.publication_state != "available":
        return set()
    path = export_root / f"{stem}.json"
    if not path.exists():
        return set()
    return {row.move_id for row in read_model_rows(path, model_cls)}


def _to_official_export(record: OfficialNormalizedRecord) -> OfficialExportRecord:
    return OfficialExportRecord.model_validate(
        record.model_dump(
            exclude={
                "source",
                "snapshot_id",
                "source_row_id",
                "source_url",
                "page_locale",
                "fetched_at",
                "raw_row_json",
                "extraction_confidence",
                "manual_review_needed",
                "review_reasons",
            }
        )
    )


def _to_supercombo_export(record: SupercomboNormalizedRecord) -> SupercomboExportRecord:
    return SupercomboExportRecord.model_validate(
        record.model_dump(
            exclude={
                "source",
                "snapshot_id",
                "source_row_id",
                "raw_source_token",
                "table_index",
                "source_url",
                "page_locale",
                "fetched_at",
                "binding_class",
                "publish_eligible",
                "confirmation_status",
                "binding_confirmed",
                "candidate_move_ids",
                "collision_group",
                "conflicting_move_ids",
                "raw_row_json",
                "extraction_confidence",
                "manual_review_needed",
                "review_reasons",
            }
        )
    )


def _to_derived_export(record: DerivedNormalizedRecord) -> DerivedExportRecord:
    return DerivedExportRecord.model_validate(
        record.model_dump(
            exclude={
                "source",
                "snapshot_id",
                "source_row_id",
                "extraction_confidence",
                "manual_review_needed",
                "review_reasons",
            }
        )
    )


def _build_manual_review_records(
    dataset_name: str,
    records: Iterable,
    *,
    extra_review_reasons_by_source_row_id: dict[str, list[str]] | None = None,
) -> list[ManualReviewRecord]:
    extra_review_reasons_by_source_row_id = extra_review_reasons_by_source_row_id or {}
    return [
        ManualReviewRecord.model_validate(
            _manual_review_payload(
                dataset_name,
                record,
                extra_review_reasons=extra_review_reasons_by_source_row_id.get(getattr(record, "source_row_id"), []),
            )
        )
        for record in records
    ]


def _manual_review_payload(
    dataset_name: str,
    record,
    *,
    extra_review_reasons: list[str] | None = None,
) -> dict[str, object]:
    review_reasons = list(getattr(record, "review_reasons", []))
    for reason in extra_review_reasons or []:
        if reason not in review_reasons:
            review_reasons.append(reason)
    payload = {
        "dataset": dataset_name,
        "source": getattr(record, "source", "official"),
        "snapshot_id": getattr(record, "snapshot_id"),
        "source_row_id": getattr(record, "source_row_id"),
        "raw_source_token": getattr(record, "raw_source_token", None),
        "reason_codes": [_reason_code(reason) for reason in review_reasons],
        "raw_excerpt": _raw_excerpt(record),
        "move_id": getattr(record, "move_id", None),
        "character_slug": getattr(record, "character_slug", None),
        "move_name": getattr(record, "move_name", None),
        "input": getattr(record, "input", None),
        "move_group": getattr(record, "move_group", None),
        "table_index": getattr(record, "table_index", None),
        "binding_class": getattr(record, "binding_class", None),
        "publish_eligible": getattr(record, "publish_eligible", None),
        "confirmation_status": getattr(record, "confirmation_status", None),
        "candidate_move_ids": list(getattr(record, "candidate_move_ids", [])),
        "collision_group": getattr(record, "collision_group", None),
        "conflicting_move_ids": list(getattr(record, "conflicting_move_ids", [])),
    }
    return payload


def _reason_code(reason: str) -> str:
    exact_map = {
        "official registry mismatch": "official_registry_mismatch",
        "official total parse failed": "official_total_parse_failed",
        "binding policy missing": "binding_policy_missing",
        "supercombo one-to-many binding withheld": "supercombo_binding_one_to_many",
        "supercombo many-to-one binding collision": "supercombo_binding_collision",
        "supercombo excluded binding": "supercombo_binding_excluded",
        "supercombo unconfirmed class F binding": "supercombo_binding_unconfirmed_f",
        "supercombo missing official safe row": "supercombo_missing_official_safe_row",
    }
    if reason in exact_map:
        return exact_map[reason]
    if reason.startswith("official active parse ambiguous"):
        return "official_active_ambiguous"
    if reason.startswith("supercombo label mismatch"):
        return "supercombo_label_mismatch"
    if reason.startswith("supercombo value row short"):
        return "supercombo_value_row_short"
    return slugify(reason)


def _raw_excerpt(record) -> str:
    if isinstance(record, OfficialNormalizedRecord):
        excerpt = {
            "input": record.input,
            "move_name": record.move_name,
            "move_group": record.move_group,
            "startup": record.startup,
            "active": record.active,
            "recovery": record.recovery,
            "block_adv": record.block_adv,
        }
    elif isinstance(record, SupercomboNormalizedRecord):
        excerpt = {
            "raw_source_token": record.raw_source_token,
            "input": record.input,
            "move_name": record.move_name,
            "move_group": record.move_group,
            "binding_class": record.binding_class,
            "punish_adv": record.punish_adv,
            "notes_sc": record.notes_sc,
        }
    else:
        excerpt = {
            "move_id": record.move_id,
            "punishable_threshold": record.punishable_threshold,
            "startup_bucket": record.startup_bucket,
            "meaty_block_adv_max": record.meaty_block_adv_max,
            "simple_punish_adv": record.simple_punish_adv,
        }
    compact = {key: value for key, value in excerpt.items() if value is not None}
    return json.dumps(compact, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _update_snapshot_manifest_dataset(
    dataset_name: str,
    dataset_manifest: PublishedDatasetManifest,
    manifest: RunManifest,
    hash_value: str,
    published_snapshot_ids: list[str],
    published_record_count: int,
    withheld_review_count: int,
) -> None:
    if dataset_manifest.publication_state == "available" and dataset_manifest.content_hash == hash_value:
        return
    dataset_manifest.publication_state = "available"
    dataset_manifest.published_run_id = manifest.run_id
    dataset_manifest.published_snapshot_ids = published_snapshot_ids
    dataset_manifest.published_record_count = published_record_count
    dataset_manifest.withheld_review_count = withheld_review_count
    dataset_manifest.registry_version = manifest.registry_version
    dataset_manifest.registry_sha256 = manifest.registry_sha256
    if dataset_name == "supercombo_enrichment":
        dataset_manifest.binding_policy_version = manifest.binding_policy_version
        dataset_manifest.binding_policy_sha256 = manifest.binding_policy_sha256
    else:
        dataset_manifest.binding_policy_version = None
        dataset_manifest.binding_policy_sha256 = None
    dataset_manifest.content_hash = hash_value


def _mark_supercombo_unavailable(
    dataset_manifest: PublishedDatasetManifest,
    manifest: RunManifest,
    binding_policy: LoadedSupercomboBindingPolicy,
) -> None:
    dataset_manifest.publication_state = "unavailable"
    dataset_manifest.published_run_id = None
    dataset_manifest.published_snapshot_ids = []
    dataset_manifest.published_record_count = 0
    dataset_manifest.withheld_review_count = 0
    dataset_manifest.registry_version = manifest.registry_version
    dataset_manifest.registry_sha256 = manifest.registry_sha256
    dataset_manifest.binding_policy_version = binding_policy.version
    dataset_manifest.binding_policy_sha256 = binding_policy.sha256
    dataset_manifest.content_hash = None


def _assert_parse_inputs_unchanged(
    manifest: RunManifest,
    registry: LoadedRegistry,
    binding_policy: LoadedSupercomboBindingPolicy,
) -> None:
    if manifest.registry_version != registry.version or manifest.registry_sha256 != registry.sha256:
        raise ValueError(
            "registry changed since parse-from-raw; rerun parse-from-raw before publish "
            f"(manifest={manifest.registry_version}/{manifest.registry_sha256[:8]}, current={registry.version}/{registry.sha256[:8]})"
        )
    if manifest.binding_policy_version != binding_policy.version or manifest.binding_policy_sha256 != binding_policy.sha256:
        raise ValueError(
            "binding policy changed since parse-from-raw; rerun parse-from-raw before publish "
            f"(manifest={manifest.binding_policy_version}/{manifest.binding_policy_sha256[:8]}, "
            f"current={binding_policy.version}/{binding_policy.sha256[:8]})"
        )
