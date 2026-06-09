from __future__ import annotations

from pathlib import Path

import pytest

from tools.web_pages import capcom_esports_base_terms as terms_capture


def test_source_asset_path_accepts_capcom_base_assets() -> None:
    assert (
        terms_capture.source_asset_path("https://sf.esports.capcom.com/base/assets/img/thumb_word0.jpg")
        == "assets/img/thumb_word0.jpg"
    )
    assert (
        terms_capture.source_asset_path("https://sf.esports.capcom.com/base/assets/mp4/word22.mp4")
        == "assets/mp4/word22.mp4"
    )
    assert (
        terms_capture.source_asset_path("https://sf.esports.capcom.com/base/assets/img/icon_mic.png")
        == "assets/img/icon_mic.png"
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://sf.esports.capcom.com/base/assets/img/thumb_word0.jpg",
        "https://evil.example/base/assets/img/thumb_word0.jpg",
        "//evil.example/base/assets/img/thumb_word0.jpg",
        "https://sf.esports.capcom.com/base/assets/%2e%2e/%2e%2e/AGENTS.md",
        "https://sf.esports.capcom.com/base/assets/img/../thumb_word0.jpg",
        "https://sf.esports.capcom.com/base/assets/img/thumb_top.jpg",
    ],
)
def test_source_asset_path_rejects_assets_outside_scoped_allowlist(url: str) -> None:
    with pytest.raises(ValueError):
        terms_capture.source_asset_path(url)


def test_safe_asset_output_path_stays_under_assets_directory(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw" / "web-pages" / "sf.esports.capcom.com" / "base-terms"

    assert terms_capture.safe_asset_output_path(raw_root, "assets/img/thumb_word0.jpg") == (
        raw_root / "assets" / "img" / "thumb_word0.jpg"
    ).resolve()

    with pytest.raises(ValueError):
        terms_capture.safe_asset_output_path(raw_root, "assets/../../../../../AGENTS.md")

    with pytest.raises(ValueError):
        terms_capture.safe_asset_output_path(raw_root, r"assets\img\thumb_word0.jpg")
