from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from ..config import repo_root as configured_repo_root
from ..schemas import DatasetName, RunManifest, SnapshotManifest
from ..versioning import EXPORT_CONTRACT_VERSION, SCHEMA_VERSION


DATASET_SOURCE_MAP: dict[DatasetName, Literal["official", "supercombo"]] = {
    "official_raw": "official",
    "derived_metrics": "official",
    "supercombo_enrichment": "supercombo",
}
DATASET_EXPORT_FILENAMES: dict[DatasetName, tuple[str, ...]] = {
    "official_raw": (
        "official_raw.json",
        "official_raw.csv",
        "official_raw_manual_review.json",
        "official_raw_manual_review.csv",
    ),
    "derived_metrics": (
        "derived_metrics.json",
        "derived_metrics.csv",
        "derived_metrics_manual_review.json",
        "derived_metrics_manual_review.csv",
    ),
    "supercombo_enrichment": (
        "supercombo_enrichment.json",
        "supercombo_enrichment.csv",
        "supercombo_enrichment_manual_review.json",
        "supercombo_enrichment_manual_review.csv",
    ),
}


@dataclass(frozen=True)
class PruneItem:
    category: str
    path: Path
    path_type: Literal["file", "dir"]
    size_bytes: int


@dataclass(frozen=True)
class LatestPublishedPruneSummary:
    character_slug: str
    dry_run: bool
    kept_datasets: tuple[str, ...]
    kept_export_files: tuple[Path, ...]
    kept_raw_snapshot_dirs: tuple[Path, ...]
    delete_items: tuple[PruneItem, ...]

    @property
    def delete_file_count(self) -> int:
        return sum(1 for item in self.delete_items if item.path_type == "file")

    @property
    def delete_dir_count(self) -> int:
        return sum(1 for item in self.delete_items if item.path_type == "dir")

    @property
    def reclaimed_bytes(self) -> int:
        return sum(item.size_bytes for item in self.delete_items)

    def render_lines(self, verbose: bool = False) -> list[str]:
        mode = "dry-run" if self.dry_run else "apply"
        lines = [
            f"prune mode={mode} character={self.character_slug}",
            f"kept datasets={', '.join(self.kept_datasets)}",
            f"kept raw snapshots={len(self.kept_raw_snapshot_dirs)}",
            (
                "delete candidates "
                f"files={self.delete_file_count} dirs={self.delete_dir_count} bytes={self.reclaimed_bytes}"
            ),
        ]
        if verbose:
            for path in self.kept_export_files:
                lines.append(f"keep export {path.as_posix()}")
            for path in self.kept_raw_snapshot_dirs:
                lines.append(f"keep raw {path.as_posix()}")
        for item in self.delete_items:
            lines.append(f"delete[{item.category}] {item.path.as_posix()}")
        return lines


def prune_latest_published_state(
    character_slug: str,
    *,
    apply: bool = False,
    verbose: bool = False,
    base_repo_root: Path | None = None,
) -> LatestPublishedPruneSummary:
    repo_root = (base_repo_root or configured_repo_root()).resolve()
    data_root = _resolve_under(repo_root / "data", repo_root / "data")
    exports_root = _resolve_under(data_root, data_root / "exports" / character_slug)
    manifest_path = _resolve_under(data_root, exports_root / "snapshot_manifest.json")

    manifest = _load_prune_manifest(manifest_path)
    if manifest.character_slug != character_slug:
        raise ValueError(f"snapshot manifest character mismatch: {manifest.character_slug} != {character_slug}")

    available_datasets = {
        dataset_name: dataset_manifest
        for dataset_name, dataset_manifest in manifest.datasets.items()
        if dataset_manifest.publication_state == "available"
    }
    if not available_datasets:
        raise ValueError("snapshot manifest has no available datasets; refusing to prune")

    keep_exports: set[Path] = {manifest_path}
    keep_raw_dirs: set[Path] = set()
    kept_datasets = sorted(available_datasets.keys())

    for dataset_name, dataset_manifest in available_datasets.items():
        if dataset_name not in DATASET_EXPORT_FILENAMES:
            raise ValueError(f"unknown dataset in snapshot manifest: {dataset_name}")
        if not dataset_manifest.published_run_id:
            raise ValueError(f"available dataset {dataset_name} missing published_run_id")
        if not dataset_manifest.published_snapshot_ids:
            raise ValueError(f"available dataset {dataset_name} missing published_snapshot_ids")
        if dataset_manifest.registry_version is None or dataset_manifest.registry_sha256 is None:
            raise ValueError(f"available dataset {dataset_name} missing registry provenance")
        if dataset_name == "supercombo_enrichment" and (
            dataset_manifest.binding_policy_version is None or dataset_manifest.binding_policy_sha256 is None
        ):
            raise ValueError(f"available dataset {dataset_name} missing binding policy provenance")

        for filename in DATASET_EXPORT_FILENAMES[dataset_name]:
            export_path = _resolve_under(data_root, exports_root / filename)
            if not export_path.exists():
                raise ValueError(f"required export file missing for {dataset_name}: {export_path}")
            keep_exports.add(export_path)

        raw_source = DATASET_SOURCE_MAP[dataset_name]
        for snapshot_id in dataset_manifest.published_snapshot_ids:
            raw_dir = _resolve_under(data_root, data_root / "raw" / raw_source / character_slug / snapshot_id)
            if not raw_dir.exists():
                raise ValueError(f"required raw snapshot missing for {dataset_name}: {raw_dir}")
            keep_raw_dirs.add(raw_dir)

        _validate_optional_run_manifest(
            data_root=data_root,
            character_slug=character_slug,
            dataset_name=dataset_name,
            published_run_id=dataset_manifest.published_run_id,
            published_snapshot_ids=tuple(dataset_manifest.published_snapshot_ids),
        )

    delete_items: list[PruneItem] = []
    delete_items.extend(_collect_export_delete_items(data_root, exports_root, keep_exports))
    delete_items.extend(_collect_normalized_delete_items(data_root, character_slug))
    delete_items.extend(_collect_raw_delete_items(data_root, character_slug, keep_raw_dirs))
    delete_items.extend(_collect_archive_delete_items(data_root))
    delete_items.extend(_collect_empty_dir_delete_items(data_root, delete_items))
    delete_items = _dedupe_delete_items(delete_items)

    summary = LatestPublishedPruneSummary(
        character_slug=character_slug,
        dry_run=not apply,
        kept_datasets=tuple(kept_datasets),
        kept_export_files=tuple(sorted(keep_exports)),
        kept_raw_snapshot_dirs=tuple(sorted(keep_raw_dirs)),
        delete_items=tuple(delete_items),
    )

    if apply:
        _apply_delete_items(delete_items)
    return summary


def _load_prune_manifest(path: Path) -> SnapshotManifest:
    payload = SnapshotManifest.model_validate_json(path.read_text(encoding="utf-8"))
    if payload.schema_version != SCHEMA_VERSION:
        raise ValueError(f"unsupported snapshot manifest schema_version={payload.schema_version}")
    if payload.export_contract_version != EXPORT_CONTRACT_VERSION:
        raise ValueError(f"unsupported snapshot manifest export_contract_version={payload.export_contract_version}")
    return payload


def _validate_optional_run_manifest(
    *,
    data_root: Path,
    character_slug: str,
    dataset_name: str,
    published_run_id: str,
    published_snapshot_ids: tuple[str, ...],
) -> None:
    run_dir = _resolve_under(data_root, data_root / "normalized" / character_slug / published_run_id)
    if not run_dir.exists():
        return
    manifest_path = _resolve_under(data_root, run_dir / "run_manifest.json")
    if not manifest_path.exists():
        raise ValueError(f"published run directory exists without run_manifest.json: {run_dir}")
    run_manifest = RunManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    if run_manifest.character_slug != character_slug:
        raise ValueError(f"run manifest character mismatch: {run_manifest.character_slug} != {character_slug}")
    dataset_status = run_manifest.dataset_status.get(dataset_name)
    if dataset_status is None:
        raise ValueError(f"run manifest missing dataset {dataset_name}: {manifest_path}")
    if dataset_status.published_run_id != published_run_id or dataset_status.publication_outcome != "published":
        raise ValueError(f"run manifest dataset state mismatch for {dataset_name}: {manifest_path}")
    source_name = DATASET_SOURCE_MAP[dataset_name]
    source_status = run_manifest.source_status.get(source_name)
    if source_status is None:
        raise ValueError(f"run manifest missing source {source_name}: {manifest_path}")
    if source_status.snapshot_id and source_status.snapshot_id not in published_snapshot_ids:
        raise ValueError(f"run manifest snapshot mismatch for {dataset_name}: {manifest_path}")
    if not run_manifest.binding_policy_version or not run_manifest.binding_policy_sha256:
        raise ValueError(f"run manifest missing binding policy provenance: {manifest_path}")


def _collect_export_delete_items(data_root: Path, exports_root: Path, keep_exports: set[Path]) -> list[PruneItem]:
    items: list[PruneItem] = []
    if not exports_root.exists():
        return items
    for path in exports_root.rglob("*"):
        resolved = _resolve_under(data_root, path)
        if resolved in keep_exports:
            continue
        if resolved.is_file():
            items.append(_delete_item("exports", resolved))
    return items


def _collect_normalized_delete_items(data_root: Path, character_slug: str) -> list[PruneItem]:
    root = _resolve_under(data_root, data_root / "normalized" / character_slug)
    if not root.exists():
        return []
    return [_delete_item("normalized_runs", _resolve_under(data_root, child)) for child in root.iterdir()]


def _collect_raw_delete_items(data_root: Path, character_slug: str, keep_raw_dirs: set[Path]) -> list[PruneItem]:
    items: list[PruneItem] = []
    for source_name in ("official", "supercombo"):
        root = _resolve_under(data_root, data_root / "raw" / source_name / character_slug)
        if not root.exists():
            continue
        for child in root.iterdir():
            resolved = _resolve_under(data_root, child)
            if resolved in keep_raw_dirs:
                continue
            items.append(_delete_item("raw_snapshots", resolved))
    return items


def _collect_archive_delete_items(data_root: Path) -> list[PruneItem]:
    archive_root = _resolve_under(data_root, data_root / "archive")
    if not archive_root.exists():
        return []
    return [_delete_item("archive", archive_root)]


def _collect_empty_dir_delete_items(data_root: Path, explicit_delete_items: list[PruneItem]) -> list[PruneItem]:
    explicit_delete_paths = {_resolve_under(data_root, item.path) for item in explicit_delete_items}
    explicit_delete_dirs = {path for path in explicit_delete_paths if path.is_dir()}

    remaining_paths: list[Path] = []
    for path in data_root.rglob("*"):
        resolved = _resolve_under(data_root, path)
        if any(_is_relative_to(resolved, deleted_dir) for deleted_dir in explicit_delete_dirs):
            continue
        if resolved in explicit_delete_paths and resolved.is_file():
            continue
        remaining_paths.append(resolved)

    remaining_set = set(remaining_paths)
    empty_dir_paths: list[Path] = []
    for path in sorted((path for path in remaining_paths if path.is_dir()), key=lambda current: len(current.parts), reverse=True):
        if path == data_root:
            continue
        if path in explicit_delete_paths:
            continue
        if any(_is_relative_to(path, deleted_dir) for deleted_dir in explicit_delete_dirs):
            continue
        if not any(candidate != path and _is_relative_to(candidate, path) for candidate in remaining_set):
            empty_dir_paths.append(path)
            remaining_set.discard(path)
    return [_delete_item("empty_dirs", path) for path in empty_dir_paths]


def _dedupe_delete_items(items: list[PruneItem]) -> list[PruneItem]:
    by_path: dict[Path, PruneItem] = {}
    for item in items:
        by_path[item.path] = item
    return sorted(by_path.values(), key=lambda item: (item.category, item.path.as_posix()))


def _apply_delete_items(items: Iterable[PruneItem]) -> None:
    files = [item for item in items if item.path_type == "file"]
    dirs = [item for item in items if item.path_type == "dir"]
    for item in sorted(files, key=lambda current: len(current.path.parts), reverse=True):
        if item.path.exists():
            item.path.unlink()
    for item in sorted(dirs, key=lambda current: len(current.path.parts), reverse=True):
        if item.path.exists():
            shutil.rmtree(item.path)


def _delete_item(category: str, path: Path) -> PruneItem:
    return PruneItem(
        category=category,
        path=path,
        path_type="dir" if path.is_dir() else "file",
        size_bytes=_path_size(path),
    )


def _path_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    total = 0
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                total += child.stat().st_size
    return total


def _resolve_under(data_root: Path, path: Path) -> Path:
    resolved_root = data_root.resolve()
    resolved_path = path.resolve(strict=False)
    if not _is_relative_to(resolved_path, resolved_root):
        raise ValueError(f"path escapes data root: {resolved_path}")
    return resolved_path


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
