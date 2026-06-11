from __future__ import annotations

from pathlib import Path

import pytest

from tools.battle_change.paths import repo_relative_path


def test_repo_relative_path_reads_serialized_posix_paths_on_native_platform() -> None:
    repo_root = Path("repo")

    path = repo_relative_path(repo_root, "raw/web-pages/wiki.supercombo.gg/patch-notes/page.raw.wikitext")

    assert path == repo_root / "raw" / "web-pages" / "wiki.supercombo.gg" / "patch-notes" / "page.raw.wikitext"


def test_repo_relative_path_rejects_paths_outside_repo() -> None:
    with pytest.raises(ValueError):
        repo_relative_path(Path("repo"), "../outside.json")
