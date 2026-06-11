from __future__ import annotations

from pathlib import Path, PurePosixPath


def repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve a stored repo-relative POSIX path on the current platform."""
    path_text = str(relative_path).replace("\\", "/")
    posix_path = PurePosixPath(path_text)
    if not path_text or posix_path.is_absolute() or ".." in posix_path.parts or any(":" in part for part in posix_path.parts):
        raise ValueError(f"path is not a safe repo-relative path: {relative_path!r}")
    return repo_root.joinpath(*posix_path.parts)
