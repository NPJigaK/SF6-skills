from __future__ import annotations

from tools.web_pages import supercombo_page


def test_page_slug_from_title_uses_last_segment() -> None:
    assert supercombo_page.page_slug_from_title("Street Fighter 6/HUD") == "hud"
    assert supercombo_page.page_slug_from_title("Street Fighter 6/Game Data") == "game-data"


def test_storage_filename_normalizes_mediawiki_file_titles() -> None:
    assert supercombo_page.storage_filename("File:SF6 HUD Full.png") == "SF6_HUD_Full.png"
    assert supercombo_page.storage_filename("File:SF6_HUD_Full.png") == "SF6_HUD_Full.png"


def test_extract_wikitext_file_titles() -> None:
    wikitext = "[[File:SF6 HUD Full.png|thumb|HUD]] and [[Image:SF6_Gauge.webp|x120px]]"

    assert supercombo_page.extract_wikitext_file_titles(wikitext) == [
        "File:SF6 Gauge.webp",
        "File:SF6 HUD Full.png",
    ]


def test_rendered_asset_filename_is_stable_and_safe() -> None:
    url = "https://wiki.supercombo.gg/images/thumb/a/a1/SF6 HUD Full.png/800px-SF6 HUD Full.png"

    filename = supercombo_page.rendered_asset_filename(url)

    assert filename.endswith("-800px-SF6_HUD_Full.png")
    assert "/" not in filename
    assert "\\" not in filename


def test_content_media_file_titles_excludes_navigation_media() -> None:
    wikitext = "[[File:SF6 Battle HUD.jpg|class=sc-img-responsive]]\n{{Navbox-SF6}}"
    media_dom = {
        "images": [
            {
                "file_page_title": "File:SF6 icon counterhit.png",
                "nearest_heading": "HUD Icons",
            },
            {
                "file_page_title": "File:SF6 Ryu Icon.png",
                "nearest_heading": "SF6 Navigation",
            },
        ]
    }

    assert supercombo_page.content_media_file_titles(wikitext, media_dom) == [
        "File:SF6 Battle HUD.jpg",
        "File:SF6 icon counterhit.png",
    ]


def test_excluded_query_file_titles_reports_template_navigation_images() -> None:
    query_titles = [
        "File:SF6 Battle HUD.jpg",
        "File:SF6 Ryu Icon.png",
        "File:SF6 icon counterhit.png",
    ]
    content_titles = [
        "File:SF6 Battle HUD.jpg",
        "File:SF6 icon counterhit.png",
    ]

    assert supercombo_page.excluded_query_file_titles(query_titles, content_titles) == [
        {
            "title": "File:SF6 Ryu Icon.png",
            "reason": "api_prop_images_from_transcluded_or_navigation_content",
        }
    ]
