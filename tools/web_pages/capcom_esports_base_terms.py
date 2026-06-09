#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

from lxml import html as lxml_html
from scrapling.fetchers import DynamicFetcher, Fetcher


PUBLISHER = "Capcom"
GAME = "Street Fighter 6"
LOCALE = "ja-jp"
SOURCE_TYPE = "official_scoped_web_page_capture"
SOURCE_URL = "https://sf.esports.capcom.com/base/"
PAGE_JS_URL = urljoin(SOURCE_URL, "./assets/js/page.js")
SOURCE_SCOPE = "capcom_esports_base_words_only"
RAW_SCHEMA_VERSION = "capcom_esports_base_terms_raw_capture/v1"
MANIFEST_SCHEMA_VERSION = "capcom_esports_base_terms_manifest/v1"
METADATA_SCHEMA_VERSION = "capcom_esports_base_terms_metadata/v1"
PROVENANCE_SCHEMA_VERSION = "capcom_esports_base_terms_provenance/v1"
VALIDATION_SCHEMA_VERSION = "capcom_esports_base_terms_validation/v1"
EXPECTED_TERM_COUNT = 23
RENDER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

GENERATED_DIRS = ["api", "assets", "rendered", "screenshots", "source"]
GENERATED_FILES = ["manifest.json", "metadata.json", "source-provenance.json", "validation.json"]
UNWANTED_ASSET_TOKENS = [
    "assets/movie/",
    "assets/consult/",
    "logo_",
    "thumb_top",
    "icon_new",
    "icon_consult",
]
SOURCE_ASSET_HOST = urlparse(SOURCE_URL).netloc
SOURCE_ASSET_PATH_PREFIX = "/base/"
ALLOWED_SOURCE_ASSET_RE = re.compile(
    r"^assets/(?:img/(?:thumb_word\d+\.jpg|icon_mic\.png)|mp4/word\d+\.mp4)$"
)

CAPTURE_CSS = """
#onetrust-consent-sdk,
#onetrust-banner-sdk,
#onetrust-pc-sdk,
.ot-sdk-container,
.ot-sdk-row,
#CybotCookiebotDialog,
#CybotCookiebotDialogBodyUnderlay,
#CookiebotWidget,
[id^="CybotCookiebot"],
[class*="CybotCookiebot"],
[class*="CookiebotWidget"],
#navigation,
#pageTop,
#loadFooter,
.page__top,
.cta__body,
header,
.header,
.footer,
.content__mv,
.fixed_bnr {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
html,
body {
  overflow: auto !important;
}
"""


@dataclass(frozen=True)
class TextResponse:
    text: str
    response: dict[str, Any]


@dataclass(frozen=True)
class BinaryResponse:
    body: bytes
    response: dict[str, Any]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def reset_raw_root(repo_root: Path, raw_root: Path) -> None:
    raw_web_pages_root = (repo_root / "raw" / "web-pages").resolve()
    resolved_raw_root = raw_root.resolve()
    resolved_raw_root.relative_to(raw_web_pages_root)
    for directory in GENERATED_DIRS:
        target = resolved_raw_root / directory
        if target.exists():
            shutil.rmtree(target)
    for filename in GENERATED_FILES:
        target = resolved_raw_root / filename
        if target.exists():
            target.unlink()


def response_headers(page: Any) -> dict[str, str]:
    headers = getattr(page, "headers", None)
    if not headers:
        return {}
    if hasattr(headers, "items"):
        return {str(key).lower(): str(value) for key, value in headers.items()}
    return {}


def fetch_text_response(url: str, *, timeout: int) -> TextResponse:
    page = Fetcher.get(url, stealthy_headers=True, impersonate="chrome", timeout=timeout)
    body = page.body.decode("utf-8", "replace") if isinstance(page.body, (bytes, bytearray)) else str(page.body)
    return TextResponse(
        text=body,
        response={
            "url": url,
            "final_url": str(getattr(page, "url", url)),
            "status": getattr(page, "status", None),
            "headers": response_headers(page),
            "byte_count": len(body.encode("utf-8")),
            "sha256": sha256_text(body),
        },
    )


def fetch_binary_response(url: str, *, timeout: int) -> BinaryResponse:
    page = Fetcher.get(url, stealthy_headers=True, impersonate="chrome", timeout=timeout)
    body = bytes(page.body) if isinstance(page.body, (bytes, bytearray)) else str(page.body).encode("utf-8")
    return BinaryResponse(
        body=body,
        response={
            "url": url,
            "final_url": str(getattr(page, "url", url)),
            "status": getattr(page, "status", None),
            "headers": response_headers(page),
            "byte_count": len(body),
            "sha256": sha256_bytes(body),
        },
    )


def page_title(page_html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", page_html, flags=re.IGNORECASE | re.DOTALL)
    return normalize_text(match.group(1)) if match else ""


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def class_contains(class_name: str) -> str:
    return f"contains(concat(' ', normalize-space(@class), ' '), ' {class_name} ')"


def first(elements: list[Any]) -> Any | None:
    return elements[0] if elements else None


def element_text(element: Any | None) -> str:
    if element is None:
        return ""
    return normalize_text(element.text_content())


def inner_html(element: Any | None) -> str:
    if element is None:
        return ""
    text = element.text or ""
    children = "".join(lxml_html.tostring(child, encoding="unicode", method="html") for child in element)
    return text + children


def outer_html(element: Any | None) -> str:
    if element is None:
        return ""
    return lxml_html.tostring(element, encoding="unicode", method="html")


def section_raw_html(page_html: str) -> str:
    match = re.search(r"<section\b[^>]*\bid=[\"']word[\"'][^>]*>", page_html, flags=re.IGNORECASE)
    if not match:
        raise ValueError("page HTML does not contain section#word")
    start = match.start()
    depth = 0
    token_re = re.compile(r"</?section\b[^>]*>", flags=re.IGNORECASE)
    for token in token_re.finditer(page_html, start):
        token_text = token.group(0)
        if token_text.startswith("</") or token_text.startswith("</".upper()):
            depth -= 1
            if depth == 0:
                return page_html[start : token.end()]
        else:
            depth += 1
    raise ValueError("could not find closing tag for section#word")


def source_asset_path(url: str) -> str:
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if parsed.scheme != "https" or parsed.netloc != SOURCE_ASSET_HOST:
        raise ValueError(f"unexpected source asset path: {url}")
    if "\\" in path or not path.startswith(f"{SOURCE_ASSET_PATH_PREFIX}assets/"):
        raise ValueError(f"unexpected source asset path: {url}")
    path = path[len(SOURCE_ASSET_PATH_PREFIX) :]
    if any(part in {"", ".", ".."} for part in path.split("/")):
        raise ValueError(f"unexpected source asset path: {url}")
    if not ALLOWED_SOURCE_ASSET_RE.fullmatch(path):
        raise ValueError(f"unexpected source asset path: {url}")
    return path


def safe_asset_output_path(raw_root: Path, asset_path: str) -> Path:
    if "\\" in asset_path:
        raise ValueError(f"unexpected local asset path: {asset_path}")
    output_path = (raw_root / asset_path).resolve()
    output_path.relative_to((raw_root / "assets").resolve())
    return output_path


def relative_artifact(path: Path, raw_root: Path) -> str:
    return path.relative_to(raw_root).as_posix()


def artifact_record(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": relative_artifact(path, root),
        "sha256": sha256_file(path),
        "byte_count": path.stat().st_size,
    }


def png_dimensions(path: Path) -> dict[str, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
    }


def extract_modal_js(page_js: str) -> str:
    start = page_js.find("modalOpenClose(){")
    if start < 0:
        raise ValueError("page.js does not contain modalOpenClose()")
    end = page_js.find("}setSlider(){", start)
    if end < 0:
        raise ValueError("page.js does not contain modalOpenClose() end marker")
    snippet = page_js[start : end + 1]
    if "word${n}.mp4" not in snippet:
        raise ValueError("modalOpenClose() snippet does not contain generated word video rule")
    return snippet


def extract_terms(section_html: str) -> dict[str, Any]:
    root = lxml_html.fromstring(section_html)
    groups: list[dict[str, Any]] = []
    terms: list[dict[str, Any]] = []
    term_index = 0

    for group_index, group in enumerate(root.xpath(f".//*[ {class_contains('word__list')} ]")):
        priority_el = first(group.xpath(f".//*[ {class_contains('priority')} ]//p"))
        title_el = first(group.xpath(f".//*[ {class_contains('title')} ]//h3"))
        priority_label = element_text(priority_el)
        group_record = {
            "group_index": group_index,
            "priority_label": priority_label,
            "priority_stars": priority_label.count("★"),
            "title_html": inner_html(title_el),
            "title_text": element_text(title_el),
            "term_indices": [],
        }
        groups.append(group_record)

        for item in group.xpath(".//ul/li"):
            word_el = first(item.xpath(f".//*[ {class_contains('word__main')} ]"))
            if word_el is None or not element_text(word_el):
                continue

            kana_el = first(item.xpath(f".//*[ {class_contains('word__kana')} ]"))
            use_text_el = first(item.xpath(f".//*[ {class_contains('use')} ]//p"))
            description_el = first(item.xpath(f".//*[ {class_contains('description')} ]"))
            thumbnail_el = first(item.xpath(f".//*[ {class_contains('img')} ]//img"))
            usage_icon_el = first(item.xpath(f".//*[ {class_contains('use')} ]//img"))
            thumbnail_src = thumbnail_el.get("src", "") if thumbnail_el is not None else ""
            usage_icon_src = usage_icon_el.get("src", "") if usage_icon_el is not None else ""
            thumbnail_url = urljoin(SOURCE_URL, thumbnail_src) if thumbnail_src else ""
            usage_icon_url = urljoin(SOURCE_URL, usage_icon_src) if usage_icon_src else ""
            video_url = urljoin(SOURCE_URL, f"./assets/mp4/word{term_index}.mp4")

            term = {
                "index": term_index,
                "id": f"word-{term_index:02d}",
                "source_modal_video_index": term_index,
                "group_index": group_index,
                "priority_label": priority_label,
                "priority_stars": group_record["priority_stars"],
                "group_title_text": group_record["title_text"],
                "word_html": inner_html(word_el),
                "word_text": element_text(word_el),
                "kana_html": inner_html(kana_el),
                "kana_text": element_text(kana_el),
                "usage_html": inner_html(use_text_el),
                "usage_text": element_text(use_text_el),
                "description_html": inner_html(description_el),
                "description_text": element_text(description_el),
                "description_highlight_texts": [
                    element_text(span) for span in description_el.xpath(".//span")
                ]
                if description_el is not None
                else [],
                "thumbnail": {
                    "url": thumbnail_url,
                    "source_src": thumbnail_src,
                    "asset_path": source_asset_path(thumbnail_url) if thumbnail_url else "",
                    "alt": thumbnail_el.get("alt", "") if thumbnail_el is not None else "",
                },
                "usage_icon": {
                    "url": usage_icon_url,
                    "source_src": usage_icon_src,
                    "asset_path": source_asset_path(usage_icon_url) if usage_icon_url else "",
                    "alt": usage_icon_el.get("alt", "") if usage_icon_el is not None else "",
                },
                "modal_video": {
                    "url": video_url,
                    "source_rule": "./assets/mp4/word${n}.mp4 from modalOpenClose()",
                    "asset_path": source_asset_path(video_url),
                },
                "card_outer_html": outer_html(item),
                "card_outer_html_sha256": sha256_text(outer_html(item)),
            }
            terms.append(term)
            group_record["term_indices"].append(term_index)
            term_index += 1

    return {
        "artifact_schema_version": RAW_SCHEMA_VERSION,
        "captured_at_utc": utc_now(),
        "source_type": SOURCE_TYPE,
        "source_url": SOURCE_URL,
        "source_scope": SOURCE_SCOPE,
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "groups": groups,
        "terms": terms,
    }


def element_payload_js() -> str:
    return """
    ({selector, scopeId, sourceUrl, sourceScope}) => {
      const root = document.querySelector(selector);
      if (!root) {
        return {found: false, scope_id: scopeId, selector};
      }
      const rect = root.getBoundingClientRect();
      const text = textOf(root);
      return {
        artifact_schema_version: "capcom_esports_base_terms_dom/v1",
        scope_id: scopeId,
        selector,
        source_url: sourceUrl,
        source_scope: sourceScope,
        found: true,
        tag_name: root.tagName.toLowerCase(),
        id: root.id || "",
        class_name: String(root.className || ""),
        text,
        outer_html: root.outerHTML,
        rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
        headings: Array.from(root.querySelectorAll("h1,h2,h3,h4,h5,h6")).map((el, index) => ({
          index,
          tag_name: el.tagName.toLowerCase(),
          text: textOf(el),
          class_name: String(el.className || "")
        })),
        images: Array.from(root.querySelectorAll("img")).map((img, index) => ({
          index,
          src: img.getAttribute("src") || "",
          resolved_src: img.currentSrc || img.src || "",
          alt: img.getAttribute("alt") || "",
          width: img.naturalWidth || null,
          height: img.naturalHeight || null,
          class_name: String(img.className || "")
        })),
        videos: Array.from(root.querySelectorAll("video")).map((video, index) => ({
          index,
          src: video.getAttribute("src") || "",
          resolved_src: video.currentSrc || video.src || "",
          autoplay: video.autoplay,
          loop: video.loop,
          muted: video.muted,
          plays_inline: video.playsInline,
          class_name: String(video.className || "")
        })),
        buttons: Array.from(root.querySelectorAll("button,.close,label")).map((button, index) => ({
          index,
          tag_name: button.tagName.toLowerCase(),
          text: textOf(button),
          class_name: String(button.className || ""),
          for_attr: button.getAttribute("for") || ""
        }))
      };

      function textOf(element) {
        return (element.innerText || element.textContent || "").replace(/\\s+/g, " ").trim();
      }
    }
    """


def modal_payload_js() -> str:
    return """
    ({sourceUrl, sourceScope}) => {
      const root = document.querySelector("#wordModal");
      const toggle = document.querySelector("#modal-toggle");
      if (!root) {
        return {found: false, selector: "#wordModal"};
      }
      const rect = root.getBoundingClientRect();
      const word = root.querySelector(".word__main");
      const kana = root.querySelector(".word__kana");
      const usage = root.querySelector(".use p");
      const description = root.querySelector(".description");
      const video = root.querySelector("video");
      const text = textOf(root);
      return {
        artifact_schema_version: "capcom_esports_base_term_modal_dom/v1",
        source_url: sourceUrl,
        source_scope: sourceScope,
        found: true,
        selector: "#wordModal",
        body_class: document.body.className || "",
        modal_toggle_checked: !!(toggle && toggle.checked),
        tag_name: root.tagName.toLowerCase(),
        id: root.id || "",
        class_name: String(root.className || ""),
        text,
        outer_html: root.outerHTML,
        rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
        word_text: textOf(word),
        kana_text: textOf(kana),
        usage_text: textOf(usage),
        description_text: textOf(description),
        description_highlight_texts: Array.from(root.querySelectorAll(".description span")).map(textOf),
        video: video ? {
          src: video.getAttribute("src") || "",
          resolved_src: video.currentSrc || video.src || "",
          autoplay: video.autoplay,
          loop: video.loop,
          muted: video.muted,
          plays_inline: video.playsInline,
          width: video.videoWidth || null,
          height: video.videoHeight || null
        } : null,
        images: Array.from(root.querySelectorAll("img")).map((img, index) => ({
          index,
          src: img.getAttribute("src") || "",
          resolved_src: img.currentSrc || img.src || "",
          alt: img.getAttribute("alt") || "",
          width: img.naturalWidth || null,
          height: img.naturalHeight || null,
          class_name: String(img.className || "")
        }))
      };

      function textOf(element) {
        return element ? (element.innerText || element.textContent || "").replace(/\\s+/g, " ").trim() : "";
      }
    }
    """


def add_python_hashes(payload: dict[str, Any]) -> dict[str, Any]:
    payload["captured_at_utc"] = utc_now()
    payload["text_sha256"] = sha256_text(payload.get("text", ""))
    payload["outer_html_sha256"] = sha256_text(payload.get("outer_html", ""))
    return payload


def screenshot_record(path: Path, raw_root: Path) -> dict[str, Any]:
    return {**artifact_record(path, raw_root), **png_dimensions(path)}


def close_modal(page: Any) -> None:
    page.evaluate(
        """
        () => {
          const toggle = document.querySelector("#modal-toggle");
          if (toggle) toggle.checked = false;
          document.body.classList.remove("noScroll");
        }
        """
    )


def capture_rendered_state(
    raw_root: Path,
    terms: list[dict[str, Any]],
    *,
    timeout: int,
) -> dict[str, Any]:
    rendered_dir = raw_root / "rendered"
    modal_dir = rendered_dir / "modals"
    screenshots_dir = raw_root / "screenshots"
    rendered_dir.mkdir(parents=True, exist_ok=True)
    modal_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    capture_state: dict[str, Any] = {
        "started_at_utc": utc_now(),
        "finished_at_utc": None,
        "errors": [],
        "sections": {},
        "modals": [],
        "screenshots": {},
        "fetch_response": None,
    }

    def action(page: Any) -> None:
        try:
            page.set_default_timeout(timeout)
            page.wait_for_selector("section#word", state="attached", timeout=timeout)
            page.add_style_tag(content=CAPTURE_CSS)
            page.evaluate("() => window.scrollTo(0, 0)")
            page.wait_for_timeout(400)

            section_payload = page.evaluate(
                element_payload_js(),
                {
                    "selector": "section#word",
                    "scopeId": "word-section",
                    "sourceUrl": SOURCE_URL,
                    "sourceScope": SOURCE_SCOPE,
                },
            )
            if not section_payload.get("found"):
                raise ValueError("rendered section#word was not found")
            section_payload = add_python_hashes(section_payload)
            section_path = rendered_dir / "word-section.dom.json"
            write_json(section_path, section_payload)
            capture_state["sections"]["word-section"] = relative_artifact(section_path, raw_root)

            section_screenshot = screenshots_dir / "word-section.png"
            page.locator("section#word").screenshot(
                path=str(section_screenshot), animations="disabled", timeout=timeout
            )
            capture_state["screenshots"]["word-section"] = screenshot_record(section_screenshot, raw_root)

            cards = page.locator("section#word .word__list ul > li")
            card_count = cards.count()
            if card_count != len(terms):
                raise ValueError(f"expected {len(terms)} word cards, found {card_count}")

            for term in terms:
                index = term["index"]
                card = cards.nth(index)
                close_modal(page)
                card.scroll_into_view_if_needed(timeout=timeout)
                page.wait_for_timeout(150)
                card.click(timeout=timeout)
                page.wait_for_function(
                    """
                    ({word, videoName}) => {
                      const toggle = document.querySelector("#modal-toggle");
                      const modal = document.querySelector("#wordModal");
                      const wordEl = modal && modal.querySelector(".word__main");
                      const video = modal && modal.querySelector("video");
                      return !!(
                        toggle && toggle.checked &&
                        wordEl && wordEl.textContent.trim() === word &&
                        video && (video.getAttribute("src") || "").includes(videoName)
                      );
                    }
                    """,
                    arg={"word": term["word_text"], "videoName": f"word{index}.mp4"},
                    timeout=timeout,
                )
                page.wait_for_timeout(250)
                payload = page.evaluate(modal_payload_js(), {"sourceUrl": SOURCE_URL, "sourceScope": SOURCE_SCOPE})
                if not payload.get("found"):
                    raise ValueError(f"modal payload missing for {term['id']}")
                payload["term_id"] = term["id"]
                payload["term_index"] = index
                payload["expected_word_text"] = term["word_text"]
                payload["expected_modal_video"] = f"word{index}.mp4"
                payload = add_python_hashes(payload)
                modal_path = modal_dir / f"{term['id']}.dom.json"
                write_json(modal_path, payload)
                modal_record = {
                    "term_id": term["id"],
                    "term_index": index,
                    "path": relative_artifact(modal_path, raw_root),
                    "word_text": payload.get("word_text", ""),
                    "video_src": (payload.get("video") or {}).get("src", ""),
                }
                capture_state["modals"].append(modal_record)

                if index == 0:
                    modal_screenshot = screenshots_dir / "modal-word-00.png"
                    page.locator("#wordModal").screenshot(
                        path=str(modal_screenshot), animations="disabled", timeout=timeout
                    )
                    capture_state["screenshots"]["modal-word-00"] = screenshot_record(modal_screenshot, raw_root)
                close_modal(page)

            capture_state["finished_at_utc"] = utc_now()
        except Exception as exc:  # Scrapling logs and swallows page_action exceptions.
            capture_state["errors"].append(repr(exc))

    response = DynamicFetcher.fetch(
        SOURCE_URL,
        headless=True,
        network_idle=True,
        load_dom=True,
        wait=500,
        page_action=action,
        timeout=timeout,
        locale="ja-JP",
        useragent=RENDER_USER_AGENT,
    )
    capture_state["fetch_response"] = {
        "url": SOURCE_URL,
        "final_url": str(getattr(response, "url", SOURCE_URL)),
        "status": getattr(response, "status", None),
        "headers": response_headers(response),
        "byte_count": len(response.body) if isinstance(response.body, (bytes, bytearray)) else len(str(response.body)),
    }
    if capture_state["errors"]:
        raise RuntimeError("; ".join(capture_state["errors"]))
    if len(capture_state["modals"]) != len(terms):
        raise RuntimeError(f"captured {len(capture_state['modals'])} modals for {len(terms)} terms")
    return capture_state


def download_assets(raw_root: Path, terms: list[dict[str, Any]], *, timeout: int) -> dict[str, Any]:
    assets_dir = raw_root
    asset_inputs: dict[str, str] = {}
    for term in terms:
        asset_inputs[term["thumbnail"]["asset_path"]] = term["thumbnail"]["url"]
        asset_inputs[term["usage_icon"]["asset_path"]] = term["usage_icon"]["url"]
        asset_inputs[term["modal_video"]["asset_path"]] = term["modal_video"]["url"]

    downloaded: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for asset_path, url in sorted(asset_inputs.items()):
        try:
            if source_asset_path(url) != asset_path:
                raise ValueError(f"asset URL and output path mismatch: {url} -> {asset_path}")
            response = fetch_binary_response(url, timeout=timeout)
            if response.response.get("status") != 200:
                raise ValueError(f"status {response.response.get('status')}")
            output_path = safe_asset_output_path(assets_dir, asset_path)
            write_bytes(output_path, response.body)
            downloaded.append(
                {
                    **artifact_record(output_path, raw_root),
                    "source_url": url,
                    "response": response.response,
                }
            )
        except Exception as exc:
            failures.append({"path": asset_path, "source_url": url, "error": repr(exc)})

    manifest = {
        "artifact_schema_version": "capcom_esports_base_terms_asset_manifest/v1",
        "created_at_utc": utc_now(),
        "source_url": SOURCE_URL,
        "source_scope": SOURCE_SCOPE,
        "downloaded": downloaded,
        "failures": failures,
        "expected_asset_count": EXPECTED_TERM_COUNT * 2 + 1,
        "notes": [
            "Only word thumbnails, modal mp4 files, and the repeated microphone icon were downloaded.",
            "Other page assets are intentionally outside this scoped raw capture.",
        ],
    }
    write_json(raw_root / "assets" / "manifest.json", manifest)
    return manifest


def collect_artifact_hashes(raw_root: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(raw_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(raw_root).as_posix()
        if relative == "manifest.json":
            continue
        records[relative] = {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    return records


def validate_capture(raw_root: Path, *, asset_manifest: dict[str, Any]) -> dict[str, Any]:
    terms_payload = json.loads((raw_root / "api" / "terms.raw.json").read_text(encoding="utf-8"))
    terms = terms_payload.get("terms", [])
    checks: dict[str, bool] = {}

    checks["no_full_page_html_saved"] = not (raw_root / "page.html").exists()
    checks["no_full_page_js_saved"] = not (raw_root / "source" / "page.raw.js").exists()
    checks["word_section_raw_html_exists"] = (raw_root / "source" / "word-section.raw.html").exists()
    checks["modal_js_snippet_exists"] = (raw_root / "source" / "modal-open-close.raw.js").exists()
    checks["modal_js_contains_generated_video_rule"] = "word${n}.mp4" in (
        raw_root / "source" / "modal-open-close.raw.js"
    ).read_text(encoding="utf-8")
    checks["term_count_23"] = len(terms) == EXPECTED_TERM_COUNT
    checks["term_indices_contiguous"] = [term.get("index") for term in terms] == list(range(EXPECTED_TERM_COUNT))
    checks["all_terms_have_core_text"] = all(
        term.get("word_text")
        and term.get("kana_text")
        and term.get("usage_text")
        and term.get("description_text")
        for term in terms
    )
    checks["all_terms_have_thumbnail_and_video_paths"] = all(
        term.get("thumbnail", {}).get("asset_path") and term.get("modal_video", {}).get("asset_path") for term in terms
    )
    checks["groups_cover_all_terms"] = sorted(
        index for group in terms_payload.get("groups", []) for index in group.get("term_indices", [])
    ) == list(range(EXPECTED_TERM_COUNT))
    checks["downloaded_assets_expected_count"] = len(asset_manifest.get("downloaded", [])) == EXPECTED_TERM_COUNT * 2 + 1
    checks["asset_downloads_ok"] = not asset_manifest.get("failures")
    checks["assets_exist"] = all((raw_root / item["path"]).exists() for item in asset_manifest.get("downloaded", []))
    downloaded_paths = [item["path"] for item in asset_manifest.get("downloaded", [])]
    checks["assets_exclude_unwanted_page_families"] = all(
        not any(token in path for token in UNWANTED_ASSET_TOKENS) for path in downloaded_paths
    )

    modal_files = sorted((raw_root / "rendered" / "modals").glob("word-*.dom.json"))
    checks["modal_dom_count_23"] = len(modal_files) == EXPECTED_TERM_COUNT
    modal_word_matches: list[bool] = []
    modal_video_matches: list[bool] = []
    for term in terms:
        modal_path = raw_root / "rendered" / "modals" / f"{term['id']}.dom.json"
        if not modal_path.exists():
            modal_word_matches.append(False)
            modal_video_matches.append(False)
            continue
        modal = json.loads(modal_path.read_text(encoding="utf-8"))
        modal_word_matches.append(modal.get("word_text") == term.get("word_text"))
        modal_video_matches.append(f"word{term['index']}.mp4" in ((modal.get("video") or {}).get("src", "")))
    checks["modal_words_match_terms"] = all(modal_word_matches)
    checks["modal_video_srcs_match_indices"] = all(modal_video_matches)
    checks["rendered_section_dom_exists"] = (raw_root / "rendered" / "word-section.dom.json").exists()
    checks["word_section_screenshot_exists"] = (raw_root / "screenshots" / "word-section.png").exists()
    checks["first_modal_screenshot_exists"] = (raw_root / "screenshots" / "modal-word-00.png").exists()

    status = "passed" if all(checks.values()) else "failed"
    validation = {
        "validation_schema_version": VALIDATION_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "status": status,
        "checks": checks,
        "summary": {
            "term_count": len(terms),
            "group_count": len(terms_payload.get("groups", [])),
            "downloaded_asset_count": len(asset_manifest.get("downloaded", [])),
            "asset_failure_count": len(asset_manifest.get("failures", [])),
            "modal_dom_count": len(modal_files),
            "scope_policy": SOURCE_SCOPE,
        },
        "notes": [
            "Scoped raw capture covers only the CAPCOM eSports BASE word explanation section.",
            "Full page HTML, full page JavaScript, movie list assets, consult assets, logos, and unrelated page chrome were intentionally not stored.",
        ],
    }
    write_json(raw_root / "validation.json", validation)
    return validation


def build_manifest(
    repo_root: Path,
    raw_root: Path,
    *,
    captured_at_utc: str,
    page: TextResponse,
    page_js: TextResponse,
    title: str,
    validation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "raw_root": raw_root.relative_to(repo_root).as_posix(),
        "source_family": "web_page",
        "source_slug": "sf.esports.capcom.com/base-terms",
        "domain": "sf.esports.capcom.com",
        "page_slug": "base-terms",
        "publisher": PUBLISHER,
        "platform": "static_html_javascript",
        "page_title": title,
        "source_type": SOURCE_TYPE,
        "source_url": SOURCE_URL,
        "page_js_url": PAGE_JS_URL,
        "captured_at_utc": captured_at_utc,
        "capture_label": captured_at_utc[:10],
        "storage_policy": "updateable_web_page_capture",
        "source_revision": {
            "type": "http_capture_hashes",
            "page_html_sha256": page.response["sha256"],
            "page_js_sha256": page_js.response["sha256"],
            "page_html_last_modified": page.response.get("headers", {}).get("last-modified", ""),
            "page_js_last_modified": page_js.response.get("headers", {}).get("last-modified", ""),
        },
        "canonical_source_artifacts": [
            "source/word-section.raw.html",
            "source/modal-open-close.raw.js",
            "api/terms.raw.json",
            "rendered/word-section.dom.json",
            "rendered/modals/",
        ],
        "display_evidence_artifacts": [
            "screenshots/word-section.png",
            "screenshots/modal-word-00.png",
        ],
        "metadata": "metadata.json",
        "validation": "validation.json",
        "asset_manifest": "assets/manifest.json",
        "scope_policy": {
            "id": SOURCE_SCOPE,
            "included_sections": [
                "実況ワード解説 / word explanation section",
                "word card source HTML",
                "clicked word modal DOM for each term",
                "word thumbnails",
                "word modal mp4 files",
                "microphone icon used by term usage text",
            ],
            "excluded_sections": [
                "top page hero",
                "news and external links",
                "movie list outside the word section",
                "consult / coaching content",
                "logos, page chrome, and unrelated images",
            ],
            "full_source_artifacts_intentionally_not_stored": [
                "page.html",
                "source/page.raw.js",
                "full CSS",
            ],
        },
        "artifact_hashes": collect_artifact_hashes(raw_root),
        "raw_review_status": "pending_human_review",
        "validation_status": validation["status"],
        "tool": "tools/web_pages/capcom_esports_base_terms.py",
    }


def run(repo_root: Path, *, timeout: int) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    raw_root = repo_root / "raw" / "web-pages" / "sf.esports.capcom.com" / "base-terms"
    captured_at_utc = utc_now()
    reset_raw_root(repo_root, raw_root)
    raw_root.mkdir(parents=True, exist_ok=True)

    page = fetch_text_response(SOURCE_URL, timeout=timeout)
    if page.response.get("status") != 200:
        raise ValueError(f"source page returned status {page.response.get('status')}")
    page_js = fetch_text_response(PAGE_JS_URL, timeout=timeout)
    if page_js.response.get("status") != 200:
        raise ValueError(f"page.js returned status {page_js.response.get('status')}")

    title = page_title(page.text)
    word_section = section_raw_html(page.text)
    modal_js = extract_modal_js(page_js.text)
    write_text(raw_root / "source" / "word-section.raw.html", word_section)
    write_text(raw_root / "source" / "modal-open-close.raw.js", modal_js)

    terms_payload = extract_terms(word_section)
    write_json(raw_root / "api" / "terms.raw.json", terms_payload)
    terms = terms_payload["terms"]
    if len(terms) != EXPECTED_TERM_COUNT:
        raise ValueError(f"expected {EXPECTED_TERM_COUNT} terms, extracted {len(terms)}")

    rendered_state = capture_rendered_state(raw_root, terms, timeout=timeout)
    asset_manifest = download_assets(raw_root, terms, timeout=timeout)

    metadata = {
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "source_url": SOURCE_URL,
        "source_scope": SOURCE_SCOPE,
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "page_title": title,
        "term_count": len(terms),
        "groups": terms_payload["groups"],
        "asset_policy": {
            "included": [
                "assets/img/thumb_word*.jpg",
                "assets/img/icon_mic.png",
                "assets/mp4/word*.mp4",
            ],
            "excluded": [
                "movie list assets",
                "consult assets",
                "logos",
                "page chrome",
                "full page CSS and JS",
            ],
        },
    }
    write_json(raw_root / "metadata.json", metadata)

    provenance = {
        "provenance_schema_version": PROVENANCE_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "source_url": SOURCE_URL,
        "page_js_url": PAGE_JS_URL,
        "source_scope": SOURCE_SCOPE,
        "fetcher": {
            "static": "scrapling.fetchers.Fetcher",
            "rendered": "scrapling.fetchers.DynamicFetcher",
            "asset": "scrapling.fetchers.Fetcher",
        },
        "responses": {
            "page": page.response,
            "page_js": page_js.response,
            "rendered_fetch": rendered_state["fetch_response"],
        },
        "source_artifacts": {
            "word_section_raw_html": "source/word-section.raw.html",
            "modal_open_close_raw_js": "source/modal-open-close.raw.js",
            "terms_raw_json": "api/terms.raw.json",
        },
        "rendered_artifacts": {
            "word_section": rendered_state["sections"],
            "modals": rendered_state["modals"],
            "screenshots": rendered_state["screenshots"],
        },
        "scope_notes": [
            "The page HTML and page.js were fetched only to extract the scoped word section and modal video rule.",
            "The fetched full page and full JavaScript source were not stored as raw artifacts to avoid unrelated page data.",
        ],
    }
    write_json(raw_root / "source-provenance.json", provenance)

    validation = validate_capture(raw_root, asset_manifest=asset_manifest)
    manifest = build_manifest(
        repo_root,
        raw_root,
        captured_at_utc=captured_at_utc,
        page=page,
        page_js=page_js,
        title=title,
        validation=validation,
    )
    write_json(raw_root / "manifest.json", manifest)
    return {"raw_root": raw_root, "validation": validation, "manifest": manifest}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture scoped raw data for CAPCOM eSports BASE SF6 terms.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=180_000, help="Timeout in milliseconds for fetch and browser actions.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run(args.repo_root, timeout=args.timeout)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "raw_root": str(result["raw_root"]),
                "validation_status": result["validation"]["status"],
                "term_count": result["validation"]["summary"]["term_count"],
                "downloaded_asset_count": result["validation"]["summary"]["downloaded_asset_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
