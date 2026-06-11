#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlencode, urljoin, urlparse

from scrapling.fetchers import StealthySession


BASE_URL = "https://wiki.supercombo.gg"
PUBLISHER = "SuperCombo Wiki"
PLATFORM = "MediaWiki"
GAME = "Street Fighter 6"
MANIFEST_SCHEMA_VERSION = "supercombo_mediawiki_page_capture_manifest/v1"
METADATA_SCHEMA_VERSION = "supercombo_mediawiki_page_capture_metadata/v1"
VALIDATION_SCHEMA_VERSION = "supercombo_mediawiki_page_capture_validation/v1"
IMAGE_MANIFEST_SCHEMA_VERSION = "supercombo_mediawiki_page_image_manifest/v1"

GENERATED_DIRS = ["api", "images", "rendered", "screenshots"]
GENERATED_FILES = [
    "imageinfo.json",
    "manifest.json",
    "metadata.json",
    "page.html",
    "page.raw.wikitext",
    "validation.json",
]

CAPTURE_CSS = """
iframe,
#wiki-top-responsive,
#wiki-anchor-bottom-desktop,
.na-anchor-bottom,
.article-ad-sc,
[id^="article-ad"],
.citizen-sticky-header-container,
.citizen-page-sidebar,
.citizen-toc,
.citizen-drawer,
.mw-editsection,
.oo-ui-windowManager,
.cdx-dialog-backdrop {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
html,
body {
  overflow-x: visible !important;
}
.mw-body,
.citizen-body,
.mw-body-content,
#content,
#bodyContent {
  max-width: none !important;
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


@dataclass(frozen=True)
class CapturePaths:
    root: Path
    api_dir: Path
    images_files_dir: Path
    images_rendered_dir: Path
    rendered_dir: Path
    screenshots_dir: Path


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def response_headers(response: Any) -> dict[str, str]:
    headers = getattr(response, "headers", None)
    if not headers:
        return {}
    if hasattr(headers, "items"):
        return {str(key).lower(): str(value) for key, value in headers.items()}
    return {}


def response_body_bytes(response: Any) -> bytes:
    body = getattr(response, "body", b"")
    if isinstance(body, bytes | bytearray):
        return bytes(body)
    return str(body).encode("utf-8")


def response_text(response: Any) -> str:
    body = getattr(response, "body", b"")
    if isinstance(body, str):
        return body
    encoding = getattr(response, "encoding", None) or "utf-8"
    return bytes(body).decode(encoding, errors="replace")


def response_record(response: Any, requested_url: str) -> dict[str, Any]:
    data = response_body_bytes(response)
    return {
        "url": requested_url,
        "final_url": str(getattr(response, "url", requested_url)),
        "status": getattr(response, "status", None),
        "headers": response_headers(response),
        "byte_count": len(data),
        "sha256": "sha256:" + sha256(data).hexdigest(),
    }


def fetch_text_response(session: StealthySession, url: str, *, timeout_ms: int) -> TextResponse:
    response = session.fetch(url, timeout=timeout_ms, wait=1000, network_idle=False)
    if response.status != 200:
        raise RuntimeError(f"GET {url} returned HTTP {response.status}")
    return TextResponse(text=response_text(response), response=response_record(response, url))


def fetch_binary_response(session: StealthySession, url: str, *, timeout_ms: int) -> BinaryResponse:
    response = session.fetch(url, timeout=timeout_ms, wait=500, network_idle=False)
    if response.status != 200:
        raise RuntimeError(f"GET {url} returned HTTP {response.status}")
    body = response_body_bytes(response)
    return BinaryResponse(body=body, response=response_record(response, url))


def fetch_json_response(session: StealthySession, url: str, *, timeout_ms: int) -> tuple[Any, dict[str, Any]]:
    text_response = fetch_text_response(session, url, timeout_ms=timeout_ms)
    return json.loads(text_response.text), text_response.response


def page_slug_from_title(title: str) -> str:
    last_segment = title.split("/")[-1].strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", last_segment).strip("-")
    return slug or "page"


def page_url_from_title(title: str) -> str:
    path_title = quote(title.replace(" ", "_"), safe="/:_")
    return f"{BASE_URL}/w/{path_title}"


def api_url(params: dict[str, str]) -> str:
    return f"{BASE_URL}/api.php?{urlencode(params)}"


def normalize_file_title(value: str) -> str:
    title = unquote(value).strip()
    if title.lower().startswith(("file:", "image:")):
        title = title.split(":", 1)[1]
    title = title.replace("_", " ")
    title = re.sub(r"\s+", " ", title).strip()
    return f"File:{title}" if title else ""


def extract_wikitext_file_titles(wikitext: str) -> list[str]:
    titles: set[str] = set()
    for match in re.finditer(r"\[\[\s*(?:File|Image)\s*:\s*([^|\]\n]+)", wikitext, flags=re.IGNORECASE):
        title = normalize_file_title(match.group(1))
        if title:
            titles.add(title)
    return sorted(titles)


def safe_filename(value: str) -> str:
    name = unquote(value).replace("\\", "_").replace("/", "_")
    name = re.sub(r"[^A-Za-z0-9._()+\[\]-]+", "_", name).strip("._")
    return name or "asset"


def storage_filename(title: str) -> str:
    name = normalize_file_title(title).removeprefix("File:").replace(" ", "_")
    return safe_filename(name)


def rendered_asset_filename(url: str) -> str:
    parsed = urlparse(url)
    basename = safe_filename(Path(unquote(parsed.path)).name)
    prefix = sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{basename}"


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


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


def png_dimensions(path: Path) -> dict[str, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
    }


def screenshot_record(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "byte_count": path.stat().st_size,
        "sha256": sha256_file(path),
        **png_dimensions(path),
    }


def revision_content(query_payload: dict[str, Any]) -> str:
    pages = query_payload.get("query", {}).get("pages", [])
    page = pages[0] if pages else {}
    revisions = page.get("revisions") or []
    revision = revisions[0] if revisions else {}
    slots = revision.get("slots") or {}
    main_slot = slots.get("main") or {}
    return str(main_slot.get("content") or main_slot.get("*") or revision.get("content") or revision.get("*") or "")


def source_revision_metadata(query_payload: dict[str, Any], *, page_title: str) -> dict[str, Any]:
    pages = query_payload.get("query", {}).get("pages", [])
    page = pages[0] if pages else {}
    revisions = page.get("revisions") or []
    revision = revisions[0] if revisions else {}
    slots = revision.get("slots") or {}
    main_slot = slots.get("main") or {}
    revision_id = revision.get("revid") or page.get("lastrevid")
    return {
        "type": "mediawiki_revision",
        "title": page.get("title") or page_title,
        "pageid": page.get("pageid"),
        "lastrevid": page.get("lastrevid"),
        "revision_id": revision_id,
        "revision_timestamp": revision.get("timestamp"),
        "touched": page.get("touched"),
        "length": revision.get("size") or main_slot.get("size") or len(revision_content(query_payload).encode("utf-8")),
        "contentmodel": main_slot.get("contentmodel") or revision.get("contentmodel"),
        "contentformat": main_slot.get("contentformat") or revision.get("contentformat"),
        "sha1": revision.get("sha1") or main_slot.get("sha1"),
        "fullurl": page.get("fullurl"),
        "canonicalurl": page.get("canonicalurl"),
    }


def template_dependencies(payload: dict[str, Any]) -> list[dict[str, Any]]:
    pages = payload.get("query", {}).get("pages", [])
    page = pages[0] if pages else {}
    templates = page.get("templates") or []
    return sorted(
        ({"ns": item.get("ns"), "title": item.get("title")} for item in templates),
        key=lambda item: str(item.get("title") or ""),
    )


def query_image_titles(payload: dict[str, Any]) -> list[str]:
    pages = payload.get("query", {}).get("pages", [])
    page = pages[0] if pages else {}
    titles = {
        normalize_file_title(image.get("title", ""))
        for image in page.get("images", [])
    }
    return sorted(title for title in titles if title)


def fetch_imageinfo(
    session: StealthySession,
    *,
    titles: list[str],
    paths: CapturePaths,
    timeout_ms: int,
) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    normalized_titles = sorted({normalize_file_title(title) for title in titles if normalize_file_title(title)})
    for index, title_chunk in enumerate(chunks(normalized_titles, 45), start=1):
        url = api_url(
            {
                "action": "query",
                "titles": "|".join(title_chunk),
                "prop": "imageinfo",
                "iiprop": "url|mime|size|sha1|timestamp|user|comment|metadata|commonmetadata|extmetadata",
                "format": "json",
                "formatversion": "2",
            }
        )
        payload, response = fetch_json_response(session, url, timeout_ms=timeout_ms)
        write_json(paths.api_dir / f"imageinfo-{index:03d}.json", payload)
        responses.append(response)
        pages.extend(payload.get("query", {}).get("pages", []))
    resolved = [page for page in pages if not page.get("missing") and page.get("imageinfo")]
    missing = [page for page in pages if page.get("missing") or not page.get("imageinfo")]
    return {
        "requested_titles": normalized_titles,
        "api_response_artifacts": [f"api/imageinfo-{index:03d}.json" for index in range(1, len(responses) + 1)],
        "api_responses": responses,
        "pages": pages,
        "resolved_count": len(resolved),
        "missing_count": len(missing),
        "missing_titles": [page.get("title", "") for page in missing],
    }


def cleanup_capture_page(page: Any) -> None:
    page.add_style_tag(content=CAPTURE_CSS)
    page.evaluate(
        """
        () => {
          const selectors = [
            'iframe',
            '#wiki-top-responsive',
            '#wiki-anchor-bottom-desktop',
            '.na-anchor-bottom',
            '.article-ad-sc',
            '[id^="article-ad"]',
            '.citizen-sticky-header-container',
            '.citizen-page-sidebar',
            '.citizen-toc',
            '.citizen-drawer',
            '.mw-editsection',
            '.oo-ui-windowManager',
            '.cdx-dialog-backdrop'
          ];
          for (const selector of selectors) {
            for (const element of document.querySelectorAll(selector)) {
              element.remove();
            }
          }
        }
        """
    )


def warm_lazy_content(page: Any) -> None:
    page.evaluate(
        """
        async () => {
          const step = Math.max(700, Math.floor(window.innerHeight * 0.85));
          for (let y = 0; y < document.body.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise((resolve) => setTimeout(resolve, 80));
          }
          window.scrollTo(0, 0);
        }
        """
    )


def capture_full_page_png(page: Any, path: Path, root: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.evaluate("() => window.scrollTo(0, 0)")
    tmp_path = Path(tempfile.gettempdir()) / f"sf6-supercombo-page-{path.stem}-{int(time.time() * 1000)}.png"
    page.screenshot(path=str(tmp_path), full_page=True, scale="css", animations="disabled", timeout=180_000)
    path.write_bytes(tmp_path.read_bytes())
    tmp_path.unlink(missing_ok=True)
    return screenshot_record(path, root)


def capture_locator_png(page: Any, selector: str, path: Path, root: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    locator = page.locator(selector).first
    locator.screenshot(path=str(path), animations="disabled", timeout=180_000)
    return screenshot_record(path, root)


def remove_navigation_display_content(page: Any) -> None:
    page.evaluate(
        """
        () => {
          const root = document.querySelector('.mw-parser-output') || document.querySelector('#mw-content-text') || document.body;
          function textOf(element) {
            return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
          }
          const navigationHeadings = Array.from(root.querySelectorAll('h1,h2,h3,h4,h5,h6')).filter((heading) => {
            return textOf(heading) === 'SF6 Navigation' || textOf(heading) === 'Street Fighter 6 Navigation';
          });
          for (const heading of navigationHeadings) {
            const level = Number(heading.tagName.slice(1));
            let current = heading.nextElementSibling;
            while (current) {
              const next = current.nextElementSibling;
              if (/^H[1-6]$/.test(current.tagName) && Number(current.tagName.slice(1)) <= level) break;
              current.remove();
              current = next;
            }
            heading.remove();
          }
          for (const element of root.querySelectorAll('.navbox, table.navbox')) {
            element.remove();
          }
          for (const table of root.querySelectorAll('table.rounded-table.noprint, table')) {
            if (!table.querySelector('.nav-header') && !/Street Fighter 6 \\(SF6\\)/.test(textOf(table))) continue;
            const section = table.closest('section');
            const previous = section && section.previousElementSibling;
            if (section) section.remove();
            if (previous && previous.classList.contains('mw-heading') && !textOf(previous)) previous.remove();
            if (!section) table.remove();
          }
        }
        """
    )


def capture_rendered_state(
    session: StealthySession,
    *,
    page_url: str,
    paths: CapturePaths,
    timeout_ms: int,
) -> dict[str, Any]:
    state: dict[str, Any] = {"screenshots": {}}

    def page_action(page: Any) -> None:
        page.set_viewport_size({"width": 1600, "height": 1100})
        page.wait_for_selector("#mw-content-text, .mw-parser-output", timeout=timeout_ms)
        page.wait_for_timeout(3000)
        cleanup_capture_page(page)
        warm_lazy_content(page)
        cleanup_capture_page(page)

        cleaned_html = page.locator("#mw-content-text").first.evaluate("(element) => element.outerHTML")
        write_text(paths.rendered_dir / "content.cleaned.html", cleaned_html)

        main_dom = page.evaluate(
            """
            () => {
              const root = document.querySelector('.mw-parser-output') || document.querySelector('#mw-content-text') || document.body;
              function textOf(element) {
                return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
              }
              function attrs(element) {
                return Object.fromEntries(Array.from(element.attributes || []).map((attr) => [attr.name, attr.value]));
              }
              function cellPayload(cell, cellIndex) {
                return {
                  cell_index: cellIndex,
                  tag_name: cell.tagName.toLowerCase(),
                  attributes: attrs(cell),
                  text: textOf(cell),
                  html: cell.innerHTML,
                  images: Array.from(cell.querySelectorAll('img')).map((img, imageIndex) => ({
                    image_index: imageIndex,
                    src: img.getAttribute('src'),
                    current_src: img.currentSrc || '',
                    alt: img.getAttribute('alt') || '',
                    title: img.getAttribute('title') || ''
                  }))
                };
              }
              return {
                captured_at_utc: new Date().toISOString().replace(/\\.\\d{3}Z$/, 'Z'),
                title: document.title,
                url: location.href,
                content_text: textOf(root),
                headings: Array.from(root.querySelectorAll('h1,h2,h3,h4,h5,h6')).map((heading, index) => ({
                  index,
                  level: Number(heading.tagName.slice(1)),
                  id: heading.id || '',
                  text: textOf(heading),
                  html: heading.innerHTML
                })),
                paragraphs: Array.from(root.querySelectorAll('p')).map((paragraph, index) => ({
                  index,
                  text: textOf(paragraph),
                  html: paragraph.innerHTML
                })).filter((item) => item.text || item.html),
                lists: Array.from(root.querySelectorAll('ul,ol')).map((list, index) => ({
                  index,
                  tag_name: list.tagName.toLowerCase(),
                  text: textOf(list),
                  items: Array.from(list.children).map((item, itemIndex) => ({
                    index: itemIndex,
                    text: textOf(item),
                    html: item.innerHTML
                  }))
                })),
                tables: Array.from(root.querySelectorAll('table')).map((table, tableIndex) => ({
                  table_index: tableIndex,
                  class_name: table.className,
                  attributes: attrs(table),
                  text: textOf(table),
                  headers: Array.from(table.querySelectorAll('th')).map((cell) => textOf(cell)),
                  rows: Array.from(table.querySelectorAll('tr')).map((row, rowIndex) => ({
                    row_index: rowIndex,
                    cells: Array.from(row.children).map((cell, cellIndex) => cellPayload(cell, cellIndex))
                  })),
                  row_count: table.querySelectorAll('tr').length
                })),
                links: Array.from(root.querySelectorAll('a[href]')).map((link, index) => ({
                  index,
                  text: textOf(link),
                  href: link.href,
                  raw_href: link.getAttribute('href'),
                  title: link.getAttribute('title') || '',
                  class_name: link.className || ''
                })),
                metrics: {
                  heading_count: root.querySelectorAll('h1,h2,h3,h4,h5,h6').length,
                  paragraph_count: root.querySelectorAll('p').length,
                  link_count: root.querySelectorAll('a[href]').length,
                  image_count: root.querySelectorAll('img').length,
                  table_count: root.querySelectorAll('table').length,
                  video_count: root.querySelectorAll('video').length,
                  iframe_count: root.querySelectorAll('iframe').length,
                  body_height: document.body.scrollHeight,
                  viewport_width: innerWidth,
                  viewport_height: innerHeight
                }
              };
            }
            """
        )
        write_json(paths.rendered_dir / "main.dom.json", main_dom)

        media_dom = page.evaluate(
            """
            () => {
              const root = document.querySelector('.mw-parser-output') || document.querySelector('#mw-content-text') || document.body;
              function textOf(element) {
                return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
              }
              function attrs(element) {
                return Object.fromEntries(Array.from(element.attributes || []).map((attr) => [attr.name, attr.value]));
              }
              function rectOf(element) {
                const rect = element.getBoundingClientRect();
                return {
                  left: rect.left,
                  top: rect.top,
                  right: rect.right,
                  bottom: rect.bottom,
                  width: rect.width,
                  height: rect.height
                };
              }
              function nearestHeading(element) {
                let current = element;
                while (current && current !== root) {
                  let previous = current.previousElementSibling;
                  while (previous) {
                    if (/^H[1-6]$/.test(previous.tagName)) return textOf(previous);
                    const heading = previous.querySelector && previous.querySelector('h1,h2,h3,h4,h5,h6');
                    if (heading) return textOf(heading);
                    previous = previous.previousElementSibling;
                  }
                  current = current.parentElement;
                }
                return '';
              }
              function captionFor(element) {
                const figure = element.closest('figure');
                const figureCaption = figure && figure.querySelector('figcaption');
                if (figureCaption) return textOf(figureCaption);
                const thumb = element.closest('.thumb, .thumbinner, .gallerybox, .center, .floatnone');
                const thumbCaption = thumb && thumb.querySelector('.thumbcaption, .gallerytext');
                if (thumbCaption) return textOf(thumbCaption);
                return '';
              }
              function fileTitleFromLink(link) {
                if (!link) return '';
                const title = link.getAttribute('title') || '';
                if (/^(File|Image):/i.test(title)) return title;
                const href = link.getAttribute('href') || '';
                const match = decodeURIComponent(href).match(/\\/(?:File|Image):([^?#]+)/i);
                return match ? `File:${match[1].replace(/_/g, ' ')}` : '';
              }
              function mediaScopeFor(element, heading) {
                if (heading === 'SF6 Navigation' || heading === 'Street Fighter 6 Navigation') {
                  return {
                    scope: 'excluded_navigation',
                    reason: 'sf6_navigation_section'
                  };
                }
                if (element.closest('.navbox, table.navbox')) {
                  return {
                    scope: 'excluded_navigation',
                    reason: 'navbox_template'
                  };
                }
                return {
                  scope: 'content',
                  reason: ''
                };
              }
              const images = Array.from(root.querySelectorAll('img')).map((img, index) => {
                const link = img.closest('a');
                const heading = nearestHeading(img);
                const scope = mediaScopeFor(img, heading);
                return {
                  index,
                  src: img.getAttribute('src') || '',
                  current_src: img.currentSrc || '',
                  resolved_src: img.src || '',
                  srcset: img.getAttribute('srcset') || '',
                  alt: img.getAttribute('alt') || '',
                  title: img.getAttribute('title') || '',
                  class_name: img.className || '',
                  attributes: attrs(img),
                  natural_width: img.naturalWidth || null,
                  natural_height: img.naturalHeight || null,
                  rendered_rect: rectOf(img),
                  link_href: link ? link.href : '',
                  link_title: link ? (link.getAttribute('title') || '') : '',
                  file_page_title: fileTitleFromLink(link),
                  caption: captionFor(img),
                  nearest_heading: heading,
                  media_scope: scope.scope,
                  exclusion_reason: scope.reason,
                  in_navbox: Boolean(img.closest('.navbox')),
                  in_gallery: Boolean(img.closest('.gallery, .gallerybox')),
                  parent_text: textOf(img.parentElement || img).slice(0, 500)
                };
              });
              const videos = Array.from(root.querySelectorAll('video')).map((video, index) => ({
                index,
                src: video.getAttribute('src') || '',
                current_src: video.currentSrc || '',
                resolved_src: video.src || '',
                poster: video.getAttribute('poster') || '',
                controls: video.controls,
                attributes: attrs(video),
                rendered_rect: rectOf(video),
                caption: captionFor(video),
                nearest_heading: nearestHeading(video),
                sources: Array.from(video.querySelectorAll('source')).map((source, sourceIndex) => ({
                  index: sourceIndex,
                  src: source.getAttribute('src') || '',
                  resolved_src: source.src || '',
                  type: source.getAttribute('type') || ''
                }))
              }));
              return {
                captured_at_utc: new Date().toISOString().replace(/\\.\\d{3}Z$/, 'Z'),
                title: document.title,
                url: location.href,
                images,
                videos,
                audios: Array.from(root.querySelectorAll('audio')).map((audio, index) => ({
                  index,
                  src: audio.getAttribute('src') || '',
                  current_src: audio.currentSrc || '',
                  attributes: attrs(audio)
                })),
                media_links: Array.from(root.querySelectorAll('a[href]')).filter((link) => {
                  const href = link.getAttribute('href') || '';
                  return /\\.(?:png|jpe?g|webp|gif|mp4|webm|mov)(?:[?#].*)?$/i.test(href)
                    || /^(?:File|Image):/i.test(link.getAttribute('title') || '');
                }).map((link, index) => ({
                  index,
                  text: textOf(link),
                  href: link.href,
                  raw_href: link.getAttribute('href'),
                  title: link.getAttribute('title') || '',
                  class_name: link.className || ''
                })),
                counts: {
                  images: images.length,
                  content_images: images.filter((image) => image.media_scope === 'content').length,
                  excluded_navigation_images: images.filter((image) => image.media_scope === 'excluded_navigation').length,
                  videos: videos.length
                }
              };
            }
            """
        )
        write_json(paths.rendered_dir / "media.dom.json", media_dom)

        remove_navigation_display_content(page)
        scoped_html = page.locator("#mw-content-text").first.evaluate("(element) => element.outerHTML")
        write_text(paths.rendered_dir / "content.scoped.html", scoped_html)

        state["screenshots"]["page_scoped"] = capture_full_page_png(
            page,
            paths.screenshots_dir / "page-scoped.png",
            paths.root,
        )
        state["screenshots"]["content_scoped"] = capture_locator_png(
            page,
            "#mw-content-text",
            paths.screenshots_dir / "content-scoped.png",
            paths.root,
        )

    response = session.fetch(
        page_url,
        wait_selector="#mw-content-text, .mw-parser-output",
        wait=1000,
        timeout=timeout_ms,
        network_idle=False,
        page_action=page_action,
    )
    state["render_fetch"] = response_record(response, page_url)
    return state


def collect_rendered_file_titles(media_dom: dict[str, Any]) -> list[str]:
    titles = {
        normalize_file_title(image.get("file_page_title", ""))
        for image in media_dom.get("images", [])
    }
    titles.update(
        normalize_file_title(link.get("title", ""))
        for link in media_dom.get("media_links", [])
    )
    return sorted(title for title in titles if title)


def media_record_is_content(record: dict[str, Any]) -> bool:
    scope = record.get("media_scope")
    if scope:
        return scope == "content"
    return record.get("nearest_heading") not in {"SF6 Navigation", "Street Fighter 6 Navigation"}


def optional_file_title(value: str) -> str:
    stripped = value.strip()
    if not stripped.lower().startswith(("file:", "image:")):
        return ""
    return normalize_file_title(stripped)


def content_media_file_titles(wikitext: str, media_dom: dict[str, Any]) -> list[str]:
    titles = set(extract_wikitext_file_titles(wikitext))
    titles.update(
        normalize_file_title(image.get("file_page_title", ""))
        for image in media_dom.get("images", [])
        if media_record_is_content(image)
    )
    titles.update(
        optional_file_title(link.get("title", ""))
        for link in media_dom.get("media_links", [])
        if link.get("nearest_heading") not in {"SF6 Navigation", "Street Fighter 6 Navigation"}
    )
    return sorted(title for title in titles if title)


def excluded_query_file_titles(query_titles: list[str], content_titles: list[str]) -> list[dict[str, str]]:
    content_title_set = {normalize_file_title(title) for title in content_titles}
    return [
        {
            "title": title,
            "reason": "api_prop_images_from_transcluded_or_navigation_content",
        }
        for title in sorted({normalize_file_title(title) for title in query_titles})
        if title and title not in content_title_set
    ]


def collect_rendered_image_urls(media_dom: dict[str, Any]) -> list[str]:
    urls: set[str] = set()
    for image in media_dom.get("images", []):
        if not media_record_is_content(image):
            continue
        for key in ("current_src", "resolved_src", "src"):
            value = image.get(key) or ""
            if not value or value.startswith("data:"):
                continue
            resolved = urljoin(BASE_URL, value)
            parsed = urlparse(resolved)
            if parsed.netloc == "wiki.supercombo.gg" and parsed.path.startswith("/images/"):
                urls.add(resolved)
    return sorted(urls)


def download_to_path(
    session: StealthySession,
    *,
    url: str,
    target_path: Path,
    root: Path,
    timeout_ms: int,
) -> dict[str, Any]:
    response = fetch_binary_response(session, url, timeout_ms=timeout_ms)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(response.body)
    return {
        "path": target_path.relative_to(root).as_posix(),
        "url": url,
        "ok": True,
        "response": response.response,
        "byte_count": target_path.stat().st_size,
        "sha256": sha256_file(target_path),
    }


def download_images(
    session: StealthySession,
    *,
    paths: CapturePaths,
    imageinfo: dict[str, Any],
    media_dom: dict[str, Any],
    timeout_ms: int,
    download_originals: bool,
    download_rendered: bool,
) -> dict[str, Any]:
    original_downloads: list[dict[str, Any]] = []
    rendered_downloads: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    original_urls: set[str] = set()

    if download_originals:
        for page in sorted(imageinfo.get("pages", []), key=lambda item: item.get("title", "")):
            infos = page.get("imageinfo") or []
            if page.get("missing") or not infos:
                continue
            info = infos[0]
            url = info.get("url")
            if not url:
                continue
            title = page.get("title", "")
            original_urls.add(url)
            target_path = paths.images_files_dir / storage_filename(title)
            record: dict[str, Any] = {
                "kind": "mediawiki_original",
                "title": title,
                "url": url,
                "target_path": target_path.relative_to(paths.root).as_posix(),
                "mime": info.get("mime"),
                "source_sha1": info.get("sha1"),
                "width": info.get("width"),
                "height": info.get("height"),
                "size": info.get("size"),
                "timestamp": info.get("timestamp"),
            }
            try:
                record.update(
                    download_to_path(
                        session,
                        url=url,
                        target_path=target_path,
                        root=paths.root,
                        timeout_ms=timeout_ms,
                    )
                )
            except Exception as exc:
                record["ok"] = False
                record["error"] = repr(exc)
                failures.append(record)
            original_downloads.append(record)

    if download_rendered:
        for url in collect_rendered_image_urls(media_dom):
            if url in original_urls:
                continue
            target_path = paths.images_rendered_dir / rendered_asset_filename(url)
            record: dict[str, Any] = {
                "kind": "rendered_image_src",
                "url": url,
                "target_path": target_path.relative_to(paths.root).as_posix(),
            }
            try:
                record.update(
                    download_to_path(
                        session,
                        url=url,
                        target_path=target_path,
                        root=paths.root,
                        timeout_ms=timeout_ms,
                    )
                )
            except Exception as exc:
                record["ok"] = False
                record["error"] = repr(exc)
                failures.append(record)
            rendered_downloads.append(record)

    return {
        "image_manifest_schema_version": IMAGE_MANIFEST_SCHEMA_VERSION,
        "captured_at_utc": utc_now(),
        "source": PUBLISHER,
        "page_media_policy": {
            "mediawiki_originals": "Download original File: artifacts only for semantic page content media, not navigation/template chrome.",
            "rendered_image_src": "Download rendered page img src/currentSrc URLs for semantic content media when they differ from originals.",
            "video_policy": "Record video/audio DOM references but do not download large video artifacts without an explicit scoped request.",
        },
        "requested_titles": imageinfo.get("requested_titles", []),
        "missing_titles": imageinfo.get("missing_titles", []),
        "rendered_images": media_dom.get("images", []),
        "rendered_videos": media_dom.get("videos", []),
        "downloads": {
            "mediawiki_originals": original_downloads,
            "rendered_image_src": rendered_downloads,
        },
        "counts": {
            "requested_titles": len(imageinfo.get("requested_titles", [])),
            "imageinfo_resolved": imageinfo.get("resolved_count", 0),
            "imageinfo_missing": imageinfo.get("missing_count", 0),
            "downloaded_originals": sum(1 for item in original_downloads if item.get("ok")),
            "failed_originals": sum(1 for item in original_downloads if not item.get("ok")),
            "downloaded_rendered_images": sum(1 for item in rendered_downloads if item.get("ok")),
            "failed_rendered_images": sum(1 for item in rendered_downloads if not item.get("ok")),
            "rendered_dom_images": len(media_dom.get("images", [])),
            "rendered_dom_videos": len(media_dom.get("videos", [])),
            "failures": len(failures),
        },
        "failures": failures,
    }


def build_artifact_hashes(raw_root: Path) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    for path in sorted(raw_root.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            artifacts[path.relative_to(raw_root).as_posix()] = {
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
    return artifacts


def is_cloudflare_challenge(value: str) -> bool:
    lowered = value[:20_000].lower()
    return "cf-chl" in lowered or "just a moment..." in lowered or "checking your browser" in lowered


def validate_capture(
    *,
    raw_root: Path,
    page_title: str,
    query_payload: dict[str, Any],
    page_response: dict[str, Any],
    wikitext_response: dict[str, Any],
    api_query_response: dict[str, Any],
    templates_response: dict[str, Any],
    page_html: str,
    wikitext: str,
    imageinfo: dict[str, Any],
    image_manifest: dict[str, Any],
    rendered_state: dict[str, Any],
) -> dict[str, Any]:
    main_dom = json.loads((raw_root / "rendered" / "main.dom.json").read_text(encoding="utf-8"))
    media_dom = json.loads((raw_root / "rendered" / "media.dom.json").read_text(encoding="utf-8"))
    scoped_content_html = (raw_root / "rendered" / "content.scoped.html").read_text(encoding="utf-8")
    api_wikitext = revision_content(query_payload)
    expected_content_titles = content_media_file_titles(wikitext, media_dom)
    requested_titles = imageinfo.get("requested_titles", [])
    excluded_titles = excluded_query_file_titles(query_image_titles(query_payload), expected_content_titles)
    checks = {
        "page_status_200": page_response.get("status") == 200,
        "wikitext_status_200": wikitext_response.get("status") == 200,
        "api_status_200": api_query_response.get("status") == 200,
        "templates_api_status_200": templates_response.get("status") == 200,
        "not_cloudflare_challenge_html": not is_cloudflare_challenge(page_html),
        "wikitext_nonempty": bool(wikitext.strip()),
        "api_wikitext_matches_action_raw": api_wikitext == wikitext,
        "rendered_title_mentions_page": page_title.split("/")[-1] in main_dom.get("title", ""),
        "content_dom_recorded": bool(main_dom.get("content_text")),
        "media_dom_recorded": "images" in media_dom and "videos" in media_dom,
        "imageinfo_requested_for_content_media": requested_titles == expected_content_titles,
        "excluded_api_images_not_downloaded": not any(item["title"] in requested_titles for item in excluded_titles),
        "image_downloads_ok": image_manifest.get("counts", {}).get("failures") == 0,
        "content_scoped_screenshot_exists": (raw_root / "screenshots" / "content-scoped.png").exists(),
        "page_scoped_screenshot_exists": (raw_root / "screenshots" / "page-scoped.png").exists(),
        "scoped_content_excludes_navigation_table": "nav-header" not in scoped_content_html
        and "Street Fighter 6 (SF6)" not in scoped_content_html,
        "render_fetch_status_200": rendered_state.get("render_fetch", {}).get("status") == 200,
    }
    all_passed = all(checks.values())
    source_revision = source_revision_metadata(query_payload, page_title=page_title)
    return {
        "validation_schema_version": VALIDATION_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "status": "passed" if all_passed else "failed",
        "checks": checks,
        "summary": {
            "wikitext_bytes": len(wikitext.encode("utf-8")),
            "page_html_bytes": len(page_html.encode("utf-8")),
            "heading_count": main_dom.get("metrics", {}).get("heading_count"),
            "link_count": main_dom.get("metrics", {}).get("link_count"),
            "table_count": main_dom.get("metrics", {}).get("table_count"),
            "rendered_dom_image_count": media_dom.get("counts", {}).get("images"),
            "content_media_image_count": media_dom.get("counts", {}).get("content_images"),
            "excluded_navigation_image_count": media_dom.get("counts", {}).get("excluded_navigation_images"),
            "rendered_dom_video_count": media_dom.get("counts", {}).get("videos"),
            "api_prop_images_count": len(query_image_titles(query_payload)),
            "imageinfo_requested_count": len(requested_titles),
            "excluded_api_images_count": len(excluded_titles),
            "imageinfo_resolved_count": imageinfo.get("resolved_count"),
            "downloaded_original_image_count": image_manifest.get("counts", {}).get("downloaded_originals"),
            "downloaded_rendered_image_count": image_manifest.get("counts", {}).get("downloaded_rendered_images"),
            "mediawiki_revision_id": source_revision.get("revision_id"),
            "mediawiki_revision_timestamp": source_revision.get("revision_timestamp"),
        },
        "notes": [
            "page.raw.wikitext is the canonical text artifact for this MediaWiki page.",
            "imageinfo.json plus images/files preserve MediaWiki File originals only for semantic content media.",
            "MediaWiki API prop=images may include transcluded navigation/template images; those are recorded as excluded provenance, not downloaded content media.",
            "screenshots preserve scoped rendered page content for future visual questions, but are display evidence rather than source text.",
            "No wiki source page, index entry, or log entry was created by this raw-only capture.",
        ],
    }


def capture(
    repo_root: Path,
    *,
    page_title: str,
    page_slug: str | None,
    timeout_ms: int,
    download_original_images: bool,
    download_rendered_images: bool,
) -> dict[str, Any]:
    slug = page_slug or page_slug_from_title(page_title)
    raw_root = repo_root / "raw" / "web-pages" / "wiki.supercombo.gg" / slug
    reset_raw_root(repo_root, raw_root)
    paths = CapturePaths(
        root=raw_root,
        api_dir=raw_root / "api",
        images_files_dir=raw_root / "images" / "files",
        images_rendered_dir=raw_root / "images" / "rendered",
        rendered_dir=raw_root / "rendered",
        screenshots_dir=raw_root / "screenshots",
    )
    for directory in (
        paths.root,
        paths.api_dir,
        paths.images_files_dir,
        paths.images_rendered_dir,
        paths.rendered_dir,
        paths.screenshots_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    page_url = page_url_from_title(page_title)
    wikitext_url = f"{page_url}?action=raw"
    query_url = api_url(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "titles": page_title,
            "prop": "info|revisions|images",
            "inprop": "url",
            "rvprop": "ids|timestamp|content|size|user|comment|sha1",
            "rvslots": "main",
            "imlimit": "max",
        }
    )
    templates_url = api_url(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "titles": page_title,
            "prop": "templates",
            "tllimit": "max",
        }
    )
    captured_at = utc_now()

    user_data_dir = str(Path(tempfile.gettempdir()) / f"scrapling-supercombo-{slug}")
    with StealthySession(
        headless=True,
        solve_cloudflare=True,
        timeout=timeout_ms,
        wait=1000,
        network_idle=False,
        retries=2,
        user_data_dir=user_data_dir,
        locale="en-US",
        block_ads=True,
    ) as session:
        page = fetch_text_response(session, page_url, timeout_ms=timeout_ms)
        write_text(raw_root / "page.html", page.text)

        wikitext = fetch_text_response(session, wikitext_url, timeout_ms=timeout_ms)
        write_text(raw_root / "page.raw.wikitext", wikitext.text)

        query_payload, query_response = fetch_json_response(session, query_url, timeout_ms=timeout_ms)
        write_json(paths.api_dir / "query.json", query_payload)

        templates_payload, templates_response = fetch_json_response(session, templates_url, timeout_ms=timeout_ms)
        write_json(paths.api_dir / "templates.json", templates_payload)

        rendered_state = capture_rendered_state(
            session,
            page_url=page_url,
            paths=paths,
            timeout_ms=timeout_ms,
        )

        media_dom = json.loads((paths.rendered_dir / "media.dom.json").read_text(encoding="utf-8"))
        api_page_image_titles = query_image_titles(query_payload)
        image_titles = content_media_file_titles(wikitext.text, media_dom)
        excluded_api_image_titles = excluded_query_file_titles(api_page_image_titles, image_titles)
        imageinfo = fetch_imageinfo(
            session,
            titles=image_titles,
            paths=paths,
            timeout_ms=timeout_ms,
        )
        write_json(raw_root / "imageinfo.json", imageinfo)

        image_manifest = download_images(
            session,
            paths=paths,
            imageinfo=imageinfo,
            media_dom=media_dom,
            timeout_ms=timeout_ms,
            download_originals=download_original_images,
            download_rendered=download_rendered_images,
        )
        write_json(raw_root / "images" / "manifest.json", image_manifest)

    source_revision = source_revision_metadata(query_payload, page_title=page_title)
    source_updated_at = source_revision.get("revision_timestamp")
    validation = validate_capture(
        raw_root=raw_root,
        page_title=page_title,
        query_payload=query_payload,
        page_response=page.response,
        wikitext_response=wikitext.response,
        api_query_response=query_response,
        templates_response=templates_response,
        page_html=page.text,
        wikitext=wikitext.text,
        imageinfo=imageinfo,
        image_manifest=image_manifest,
        rendered_state=rendered_state,
    )
    write_json(raw_root / "validation.json", validation)

    metadata = {
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "captured_at_utc": captured_at,
        "publisher": PUBLISHER,
        "platform": PLATFORM,
        "game": GAME,
        "source_family": "web_page",
        "source_type": "community_wiki_page",
        "page_title": page_title,
        "source_url": page_url,
        "wikitext_url": wikitext_url,
        "api_url": query_url,
        "templates_api_url": templates_url,
        "source_revision": source_revision,
        "source_updated_at": source_updated_at,
        "storage_policy": "updateable_web_page_capture",
        "raw_review_status": "pending_human_review",
        "capture_method": {
            "tool": "scrapling",
            "session": "StealthySession",
            "headless": True,
            "solve_cloudflare": True,
            "block_ads": True,
            "network_idle": False,
        },
        "http_status": {
            "page_html": page.response.get("status"),
            "page_raw_wikitext": wikitext.response.get("status"),
            "api_query": query_response.get("status"),
            "api_templates": templates_response.get("status"),
            "render_fetch": rendered_state.get("render_fetch", {}).get("status"),
        },
        "responses": {
            "page_html": page.response,
            "page_raw_wikitext": wikitext.response,
            "api_query": query_response,
            "api_templates": templates_response,
            "render_fetch": rendered_state.get("render_fetch"),
        },
        "template_dependencies": template_dependencies(templates_payload),
        "media_scope_policy": {
            "included": "Page semantic content media: explicit File links in page.raw.wikitext and rendered File links outside navigation sections.",
            "excluded": "Images introduced by transcluded navigation/template chrome, including SF6 Navigation character icons.",
            "api_prop_images_note": "api/query.json preserves MediaWiki prop=images exactly; download scope intentionally uses content_media_titles instead.",
        },
        "api_page_image_titles": api_page_image_titles,
        "content_media_titles": image_titles,
        "excluded_api_image_titles": excluded_api_image_titles,
        "counts": validation.get("summary", {}),
        "artifacts": {
            "page_html": "page.html",
            "page_raw_wikitext": "page.raw.wikitext",
            "api_query": "api/query.json",
            "api_templates": "api/templates.json",
            "imageinfo": "imageinfo.json",
            "image_manifest": "images/manifest.json",
            "rendered_main_dom": "rendered/main.dom.json",
            "rendered_media_dom": "rendered/media.dom.json",
            "rendered_cleaned_content_html": "rendered/content.cleaned.html",
            "rendered_scoped_content_html": "rendered/content.scoped.html",
            "screenshots": rendered_state.get("screenshots", {}),
            "validation": "validation.json",
        },
    }
    write_json(raw_root / "metadata.json", metadata)

    artifact_hashes = build_artifact_hashes(raw_root)
    manifest = {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "raw_root": raw_root.relative_to(repo_root).as_posix(),
        "source_family": "web_page",
        "source_slug": f"wiki.supercombo.gg/{slug}",
        "domain": "wiki.supercombo.gg",
        "page_slug": slug,
        "publisher": PUBLISHER,
        "platform": PLATFORM,
        "page_title": page_title,
        "source_url": page_url,
        "captured_at_utc": captured_at,
        "capture_label": f"{captured_at[:10]}-rev{source_revision.get('revision_id')}",
        "storage_policy": "updateable_web_page_capture",
        "source_revision": source_revision,
        "source_updated_at": source_updated_at,
        "canonical_source_artifacts": [
            "page.raw.wikitext",
            "imageinfo.json",
            "images/manifest.json",
        ],
        "media_source_artifacts": [
            "images/files/",
            "images/rendered/",
        ],
        "display_evidence_artifacts": [
            "page.html",
            "rendered/main.dom.json",
            "rendered/media.dom.json",
            "rendered/content.cleaned.html",
            "rendered/content.scoped.html",
            "screenshots/page-scoped.png",
            "screenshots/content-scoped.png",
        ],
        "metadata": "metadata.json",
        "validation": "validation.json",
        "image_manifest": "images/manifest.json",
        "media_raw_policy": {
            "text": "page.raw.wikitext is canonical for source text.",
            "images": "Only page semantic content media is stored under images/files and images/rendered. Transcluded navigation/template images are excluded from raw media downloads.",
            "api_prop_images": "api/query.json may list all MediaWiki images after template transclusion; excluded_api_image_titles in metadata records titles outside the page media scope.",
            "screenshots": "Screenshots capture scoped rendered page content after navigation removal and are not used as a replacement for source media files.",
            "videos": "Video/audio DOM references are recorded in rendered/media.dom.json; large video downloads require an explicit scoped capture.",
        },
        "template_dependency_policy": {
            "scope": "Direct MediaWiki prop=templates dependencies are recorded by title only.",
            "template_list_artifact": "api/templates.json",
            "captured_template_bodies": [],
            "recursive_capture": False,
        },
        "template_dependencies": template_dependencies(templates_payload),
        "artifact_hashes": artifact_hashes,
        "raw_review_status": "pending_human_review",
        "tool": "tools/web_pages/supercombo_page.py",
    }
    write_json(raw_root / "manifest.json", manifest)

    return {
        "raw_root": raw_root.relative_to(repo_root).as_posix(),
        "manifest": (raw_root / "manifest.json").relative_to(repo_root).as_posix(),
        "validation_status": validation["status"],
        "source_revision_id": source_revision.get("revision_id"),
        "source_updated_at": source_updated_at,
        "imageinfo_resolved": imageinfo.get("resolved_count"),
        "downloaded_original_images": image_manifest.get("counts", {}).get("downloaded_originals"),
        "downloaded_rendered_images": image_manifest.get("counts", {}).get("downloaded_rendered_images"),
        "screenshots": rendered_state.get("screenshots", {}),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--page-title", default="Street Fighter 6/HUD")
    parser.add_argument("--page-slug", default=None)
    parser.add_argument("--timeout-ms", type=int, default=240_000)
    parser.add_argument("--no-download-original-images", action="store_true")
    parser.add_argument("--no-download-rendered-images", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = capture(
        args.repo_root.resolve(),
        page_title=args.page_title,
        page_slug=args.page_slug,
        timeout_ms=args.timeout_ms,
        download_original_images=not args.no_download_original_images,
        download_rendered_images=not args.no_download_rendered_images,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
