from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def data_dir() -> Path:
    return repo_root() / "data"


def aliases_file() -> Path:
    return data_dir() / "aliases" / "ja-query-fixtures.json"


def exports_dir() -> Path:
    return data_dir() / "exports"
