#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright
from scrapling.fetchers import Fetcher


PUBLISHER = "Capcom"
GAME = "Street Fighter 6"
LOCALE = "ja-jp"
SOURCE_TYPE = "official_scoped_web_page_capture"
SOURCE_URL = "https://www.streetfighter.com/6/ja-jp/mode/fightingground"
SOURCE_SCOPE = "fightingground_battle_system_only"
RAW_SCHEMA_VERSION = "capcom_fightingground_battle_system_raw_capture/v1"
MANIFEST_SCHEMA_VERSION = "capcom_fightingground_battle_system_manifest/v1"
METADATA_SCHEMA_VERSION = "capcom_fightingground_battle_system_metadata/v1"
VALIDATION_SCHEMA_VERSION = "capcom_fightingground_battle_system_validation/v1"
RENDER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

GENERATED_DIRS = ["api", "assets", "rendered", "screenshots"]
GENERATED_FILES = ["manifest.json", "metadata.json", "source-provenance.json", "validation.json"]

SECTION_SELECTORS = {
    "battle-system-design": 'section[class*="simpleOperation"]',
    "drive-gauge": 'section[class*="driveGauge"]',
    "common-system": 'section[class*="commonSystem"]',
}

SECTION_EXPECTED_TEXT_KEYS = {
    "battle-system-design": [
        "[t]simpleOperation__title",
        "[t]simpleOperation__text",
        "[t]simpleOperation__link",
    ],
    "drive-gauge": [
        "[t]driveGauge__title",
        "[t]driveGauge__text",
    ],
    "common-system": [
        "[t]commonSystem__title",
        "[t]commonSystem__cost__title",
        "[t]commonSystem__cost__continue",
        "[t]driveimpact__title",
        "[t]driveimpact__text",
        "[t]driveparry__title",
        "[t]driveparry__text",
        "[t]driveparry__attention",
        "[t]overdrive__title",
        "[t]overdrive__text",
        "[t]overdrive__attention",
        "[t]driverush__title",
        "[t]driverush__text",
        "[t]driverush__attention",
        "[t]drivereversal__title",
        "[t]drivereversal__text",
        "[t]drivereversal__attention",
    ],
    "simple-operation-modal": [
        "[t]simpleOperation__list01__title",
        "[t]simpleOperation__list01__text",
        "[t]simpleOperation__list02__title",
        "[t]simpleOperation__list02__text",
        "[t]simpleOperation__list03__title",
        "[t]simpleOperation__list03__text",
        "[t]simpleOperation__list04__title",
        "[t]simpleOperation__list04__text",
        "[t]simpleOperation__list05__title",
        "[t]simpleOperation__list05__text",
        "[t]simpleOperation__list06__title",
        "[t]simpleOperation__list06__text",
    ],
}

KEPT_TEXT_KEYS = sorted({key for keys in SECTION_EXPECTED_TEXT_KEYS.values() for key in keys})

EXCLUDED_KEY_PREFIXES = [
    "[t]accessibility",
    "[t]battlegamage",
    "[t]classic",
    "[t]commentators",
    "[t]conrtol__type",
    "[t]custom",
    "[t]dynamic",
    "[t]extremebattle",
    "[t]image__contents__interface__accessibility",
    "[t]image__contents__interface__battlegamage",
    "[t]image__contents__interface__contents",
    "[t]image__contents__interface__control",
    "[t]image__contents__interface__extreamebattle",
    "[t]image__contents__interface__live",
    "[t]image__contents__interface__onlinebattle",
    "[t]image__contents__interface__trainingmode",
    "[t]image__contents__interface__versus",
    "[t]modern",
    "[t]online",
    "[t]onlinebattle",
    "[t]realtime",
    "[t]training",
    "[t]versus",
]

EXCLUDED_ASSET_TOKENS = [
    "/accessibility",
    "/arcade",
    "/battledamage",
    "/commentator",
    "/custom",
    "/dynamic/",
    "/icon_classic.png",
    "/icon_modern.png",
    "/online",
    "/rtc_",
    "/training",
    "/versus",
    "damage_post",
]

CAPTURE_CSS = """
#CybotCookiebotDialog,
#CybotCookiebotDialogBodyUnderlay,
#CookiebotWidget,
[id^="CybotCookiebot"],
[class*="CybotCookiebot"],
[class*="CookiebotWidget"],
header[class*="layout_header"],
[class*="layout_header__nav__global"] ul,
[class*="layout_header__nav__languages"] dd,
[class*="layout_user_nav_list"] {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
html,
body {
  overflow-x: visible !important;
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


def extract_next_data(page_html: str) -> dict[str, Any]:
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        page_html,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("page HTML does not contain __NEXT_DATA__")
    return json.loads(html.unescape(match.group(1)))


def build_data_url(build_id: str) -> str:
    return f"https://www.streetfighter.com/6/_next/data/{build_id}/{LOCALE}/mode/fightingground.json"


def build_page_chunk_url(page_html: str) -> str:
    match = re.search(r'src="([^"]*chunks/pages/mode/fightingground[^"]*\.js)"', page_html)
    if not match:
        raise ValueError("page HTML does not contain fightingground page chunk")
    return urljoin(SOURCE_URL, match.group(1))


def nextjs_source_revision(build_id: str) -> dict[str, str]:
    return {"type": "nextjs_build_id", "build_id": build_id}


def png_dimensions(path: Path) -> dict[str, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
    }


def artifact_record(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_file(path),
        "byte_count": path.stat().st_size,
    }


def cleanup_page(page: Any) -> None:
    page.add_style_tag(content=CAPTURE_CSS)


def dom_payload(page: Any, *, scope_id: str, selector: str, source_revision: dict[str, str]) -> dict[str, Any]:
    payload = page.evaluate(
        """
        ({scopeId, selector, sourceUrl, sourceRevision}) => {
          const root = document.querySelector(selector);
          if (!root) {
            return {found: false, scope_id: scopeId, selector};
          }
          return elementPayload(root, scopeId, selector, sourceUrl, sourceRevision);

          function elementPayload(root, scopeId, selector, sourceUrl, sourceRevision) {
            const rect = root.getBoundingClientRect();
            const text = textOf(root);
            return {
              artifact_schema_version: "capcom_fightingground_scoped_dom/v1",
              scope_id: scopeId,
              selector,
              source_url: sourceUrl,
              source_revision: sourceRevision,
              found: true,
              tag_name: root.tagName.toLowerCase(),
              id: root.id || "",
              class_name: String(root.className || ""),
              text,
              text_sha256: sha256Lite(text),
              outer_html: root.outerHTML,
              outer_html_sha256: sha256Lite(root.outerHTML),
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
              background_images: backgroundImages(root),
              links: Array.from(root.querySelectorAll("a")).map((link, index) => ({
                index,
                href: link.getAttribute("href") || "",
                resolved_href: link.href || "",
                text: textOf(link),
                class_name: String(link.className || "")
              }))
            };
          }

          function textOf(element) {
            return (element.innerText || element.textContent || "").replace(/\\s+/g, " ").trim();
          }

          function backgroundImages(root) {
            const records = [];
            for (const [index, element] of Array.from(root.querySelectorAll("*")).entries()) {
              const bg = getComputedStyle(element).backgroundImage || "";
              if (!bg || bg === "none" || !bg.includes("url(")) continue;
              records.push({
                index,
                tag_name: element.tagName.toLowerCase(),
                class_name: String(element.className || ""),
                background_image: bg,
                urls: Array.from(bg.matchAll(/url\\(["']?([^"')]+)["']?\\)/g)).map((match) => new URL(match[1], location.href).href)
              });
            }
            return records;
          }

          function sha256Lite(value) {
            let h1 = 0xdeadbeef ^ value.length;
            let h2 = 0x41c6ce57 ^ value.length;
            for (let i = 0, ch; i < value.length; i++) {
              ch = value.charCodeAt(i);
              h1 = Math.imul(h1 ^ ch, 2654435761);
              h2 = Math.imul(h2 ^ ch, 1597334677);
            }
            h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
            h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
            return "js-hash:" + (h2 >>> 0).toString(16).padStart(8, "0") + (h1 >>> 0).toString(16).padStart(8, "0");
          }
        }
        """,
        {
            "scopeId": scope_id,
            "selector": selector,
            "sourceUrl": SOURCE_URL,
            "sourceRevision": source_revision,
        },
    )
    if not payload.get("found"):
        raise ValueError(f"missing DOM section {scope_id}: {selector}")
    payload["captured_at_utc"] = utc_now()
    payload["text_sha256"] = sha256_text(payload.get("text", ""))
    payload["outer_html_sha256"] = sha256_text(payload.get("outer_html", ""))
    return payload


def modal_payload(page: Any, *, source_revision: dict[str, str]) -> dict[str, Any]:
    payload = page.evaluate(
        """
        ({sourceUrl, sourceRevision}) => {
          const panel = document.querySelector('ul[class*="modal__drive"]');
          const root = document.querySelector('article[class*="image__modal"]');
          if (!panel || !root) {
            return {found: false};
          }
          const rect = panel.getBoundingClientRect();
          const rootRect = root.getBoundingClientRect();
          const outerHtml = root.outerHTML;
          const panelOuterHtml = panel.outerHTML;
          const listItems = Array.from(panel.querySelectorAll("li")).map((item, index) => ({
            index,
            text: textOf(item),
            class_name: String(item.className || ""),
            html: item.innerHTML
          }));
          const text = textOf(panel);
          return {
            artifact_schema_version: "capcom_fightingground_scoped_modal_dom/v1",
            scope_id: "simple-operation-modal",
            source_url: sourceUrl,
            source_revision: sourceRevision,
            found: true,
            modal_state: "simpleOperationImage",
            root_class_name: String(root.className || ""),
            panel_class_name: String(panel.className || ""),
            text,
            text_sha256: sha256Lite(text),
            outer_html_scope: "modal_root_article",
            outer_html: outerHtml,
            outer_html_sha256: sha256Lite(outerHtml),
            panel_outer_html: panelOuterHtml,
            panel_outer_html_sha256: sha256Lite(panelOuterHtml),
            rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
            root_rect: {x: rootRect.x, y: rootRect.y, width: rootRect.width, height: rootRect.height},
            list_items: listItems,
            images: Array.from(root.querySelectorAll("img")).map((img, index) => ({
              index,
              src: img.getAttribute("src") || "",
              resolved_src: img.currentSrc || img.src || "",
              alt: img.getAttribute("alt") || "",
              width: img.naturalWidth || null,
              height: img.naturalHeight || null,
              class_name: String(img.className || "")
            })),
            background_images: backgroundImages(root)
          };

          function textOf(element) {
            return (element.innerText || element.textContent || "").replace(/\\s+/g, " ").trim();
          }

          function backgroundImages(root) {
            const records = [];
            for (const [index, element] of Array.from(root.querySelectorAll("*")).entries()) {
              const bg = getComputedStyle(element).backgroundImage || "";
              if (!bg || bg === "none" || !bg.includes("url(")) continue;
              records.push({
                index,
                tag_name: element.tagName.toLowerCase(),
                class_name: String(element.className || ""),
                background_image: bg,
                urls: Array.from(bg.matchAll(/url\\(["']?([^"')]+)["']?\\)/g)).map((match) => new URL(match[1], location.href).href)
              });
            }
            return records;
          }

          function sha256Lite(value) {
            let h1 = 0xdeadbeef ^ value.length;
            let h2 = 0x41c6ce57 ^ value.length;
            for (let i = 0, ch; i < value.length; i++) {
              ch = value.charCodeAt(i);
              h1 = Math.imul(h1 ^ ch, 2654435761);
              h2 = Math.imul(h2 ^ ch, 1597334677);
            }
            h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
            h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
            return "js-hash:" + (h2 >>> 0).toString(16).padStart(8, "0") + (h1 >>> 0).toString(16).padStart(8, "0");
          }
        }
        """,
        {"sourceUrl": SOURCE_URL, "sourceRevision": source_revision},
    )
    if not payload.get("found"):
        raise ValueError("missing simpleOperationImage modal")
    payload["captured_at_utc"] = utc_now()
    payload["text_sha256"] = sha256_text(payload.get("text", ""))
    payload["outer_html_sha256"] = sha256_text(payload.get("outer_html", ""))
    return payload


def screenshot_locator(page: Any, selector: str, output_path: Path, raw_root: Path) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    locator = page.locator(selector)
    count = locator.count()
    if count != 1:
        raise ValueError(f"expected 1 screenshot target for {selector}, got {count}")
    locator.screenshot(path=str(output_path), animations="disabled", timeout=180_000)
    return {
        **artifact_record(output_path, raw_root),
        **png_dimensions(output_path),
    }


def capture_rendered_state(raw_root: Path, *, timeout: int, source_revision: dict[str, str]) -> dict[str, Any]:
    rendered_dir = raw_root / "rendered"
    screenshots_dir = raw_root / "screenshots"
    rendered_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {"sections": {}, "screenshots": {}}
    render_started_at = utc_now()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1440, "height": 1000},
            locale="ja-JP",
            user_agent=RENDER_USER_AGENT,
        )
        response = page.goto(SOURCE_URL, wait_until="networkidle", timeout=timeout)
        page.wait_for_selector(SECTION_SELECTORS["battle-system-design"], timeout=120_000)
        page.wait_for_timeout(1000)
        cleanup_page(page)

        for scope_id, selector in SECTION_SELECTORS.items():
            payload = dom_payload(page, scope_id=scope_id, selector=selector, source_revision=source_revision)
            path = rendered_dir / f"{scope_id}.dom.json"
            write_json(path, payload)
            result["sections"][scope_id] = path.relative_to(raw_root).as_posix()
            screenshot_path = screenshots_dir / f"{scope_id}.png"
            result["screenshots"][scope_id] = screenshot_locator(page, selector, screenshot_path, raw_root)

        modal_button = page.locator('p[class*="simpleOperation__contents__link"]')
        if modal_button.count() != 1:
            raise ValueError("expected 1 simple operation modal button")
        modal_button.scroll_into_view_if_needed(timeout=30_000)
        modal_button.click(timeout=30_000, force=True)
        page.wait_for_selector('article[class*="image__modal"]', timeout=60_000)
        page.wait_for_timeout(1000)
        cleanup_page(page)
        modal = modal_payload(page, source_revision=source_revision)
        modal_path = rendered_dir / "simple-operation-modal.dom.json"
        write_json(modal_path, modal)
        result["sections"]["simple-operation-modal"] = modal_path.relative_to(raw_root).as_posix()
        modal_screenshot_path = screenshots_dir / "simple-operation-modal.png"
        page.screenshot(path=str(modal_screenshot_path), full_page=False, scale="css", animations="disabled", timeout=180_000)
        result["screenshots"]["simple-operation-modal"] = {
            **artifact_record(modal_screenshot_path, raw_root),
            **png_dimensions(modal_screenshot_path),
        }

        render_final_url = page.url
        render_status = response.status if response else None
        browser.close()

    result["render_fetch"] = {
        "method": "playwright_chromium",
        "url": SOURCE_URL,
        "final_url": render_final_url,
        "status": render_status,
        "captured_at_utc": render_started_at,
    }
    return result


def collect_asset_urls(raw_root: Path) -> tuple[list[str], list[str]]:
    urls: set[str] = set()
    omitted: set[str] = set()
    for path in (raw_root / "rendered").glob("*.dom.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for image in payload.get("images", []):
            url = image.get("resolved_src") or image.get("src") or ""
            add_asset_url(url, urls, omitted)
        for record in payload.get("background_images", []):
            for url in record.get("urls", []):
                add_asset_url(url, urls, omitted)
    return sorted(urls), sorted(omitted)


def add_asset_url(url: str, urls: set[str], omitted: set[str]) -> None:
    if not url or url.startswith("data:"):
        return
    resolved = urljoin(SOURCE_URL, url)
    path = urlparse(resolved).path
    if any(token in path for token in EXCLUDED_ASSET_TOKENS):
        omitted.add(resolved)
        return
    if "/6/assets/images/mode/fg/" in path or "/6/assets/images/common/controller/" in path:
        urls.add(resolved)
        return
    if path.endswith("/6/assets/images/common/arrow_interface_wh.png"):
        urls.add(resolved)
        return
    omitted.add(resolved)


def local_asset_path(raw_root: Path, url: str) -> Path:
    path = urlparse(url).path
    if path.startswith("/6/assets/"):
        relative = path.removeprefix("/6/assets/")
    else:
        relative = "external/" + re.sub(r"[^A-Za-z0-9._-]+", "_", url)
    return raw_root / "assets" / relative


def download_assets(raw_root: Path, urls: list[str], omitted: list[str], *, timeout: int) -> dict[str, Any]:
    downloads: list[dict[str, Any]] = []
    for url in urls:
        target = local_asset_path(raw_root, url)
        response = fetch_binary_response(url, timeout=timeout)
        write_bytes(target, response.body)
        downloads.append(
            {
                "url": url,
                "path": target.relative_to(raw_root).as_posix(),
                "ok": response.response["status"] == 200,
                "response": response.response,
                "artifact": artifact_record(target, raw_root),
            }
        )
    manifest = {
        "asset_manifest_schema_version": "capcom_fightingground_scoped_assets/v1",
        "captured_at_utc": utc_now(),
        "scope_policy": SOURCE_SCOPE,
        "downloaded_assets": downloads,
        "omitted_asset_refs": omitted,
        "counts": {
            "downloaded": len(downloads),
            "failed": sum(1 for item in downloads if not item.get("ok")),
            "omitted": len(omitted),
        },
    }
    write_json(raw_root / "assets" / "manifest.json", manifest)
    return manifest


def scoped_text_payload(
    full_next_payload: dict[str, Any],
    *,
    data_url: str,
    data_response: dict[str, Any],
    source_revision: dict[str, str],
) -> dict[str, Any]:
    namespaces = full_next_payload.get("pageProps", {}).get("__namespaces")
    if namespaces is None:
        namespaces = full_next_payload.get("props", {}).get("pageProps", {}).get("__namespaces", {})
    fg = namespaces.get("mode/fightingground", {})
    kept = {key: fg[key] for key in KEPT_TEXT_KEYS if key in fg}
    missing = [key for key in KEPT_TEXT_KEYS if key not in fg]
    return {
        "artifact_schema_version": "capcom_fightingground_scoped_next_text/v1",
        "captured_at_utc": utc_now(),
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_url": SOURCE_URL,
        "data_url": data_url,
        "source_revision": source_revision,
        "scope_policy": SOURCE_SCOPE,
        "kept_namespace": "mode/fightingground",
        "kept_keys": kept,
        "kept_key_count": len(kept),
        "missing_expected_keys": missing,
        "excluded_key_prefixes": EXCLUDED_KEY_PREFIXES,
        "source_data_response": data_response,
        "notes": [
            "This artifact stores only human-curated exact text keys needed for the Battle System scope.",
            "Full Next.js data JSON is intentionally not stored to avoid preserving unrelated page sections in raw.",
        ],
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


def validate_capture(raw_root: Path) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    notes: list[str] = []
    text_payload = json.loads((raw_root / "api" / "source-text.scoped.json").read_text(encoding="utf-8"))
    assets_manifest = json.loads((raw_root / "assets" / "manifest.json").read_text(encoding="utf-8"))

    checks["no_full_page_html_saved"] = not (raw_root / "page.html").exists()
    checks["no_full_next_data_json_saved"] = not (raw_root / "data.json").exists()
    checks["no_full_page_chunk_saved"] = not (raw_root / "next" / "page-chunk.js").exists()
    checks["all_expected_text_keys_present"] = not text_payload.get("missing_expected_keys")
    checks["excluded_prefixes_not_in_scoped_text"] = not any(
        key.startswith(tuple(EXCLUDED_KEY_PREFIXES))
        for key in text_payload.get("kept_keys", {})
    )

    scoped_text = text_payload.get("kept_keys", {})
    for scope_id, keys in SECTION_EXPECTED_TEXT_KEYS.items():
        path = raw_root / "rendered" / f"{scope_id}.dom.json"
        checks[f"{scope_id}_dom_exists"] = path.exists()
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = normalize_text_for_compare(
            payload.get("text", "") + " " + html_text(payload.get("outer_html", ""))
        )
        section_keys = [key for key in keys if key in scoped_text]
        text_keys = [
            key
            for key in section_keys
            if scoped_text[key] and normalize_text_for_compare(scoped_text[key]) in text
        ]
        checks[f"{scope_id}_contains_expected_text"] = len(text_keys) >= max(1, len(section_keys) // 2)
        checks[f"{scope_id}_has_outer_html"] = bool(payload.get("outer_html"))

    modal_payload_path = raw_root / "rendered" / "simple-operation-modal.dom.json"
    if modal_payload_path.exists():
        modal = json.loads(modal_payload_path.read_text(encoding="utf-8"))
        checks["simple_operation_modal_state"] = modal.get("modal_state") == "simpleOperationImage"
        checks["simple_operation_modal_has_six_items"] = len(modal.get("list_items", [])) == 6
        checks["simple_operation_modal_has_game_screen_image"] = any(
            "game_screen.jpg" in image.get("resolved_src", "")
            for image in modal.get("images", [])
        )

    screenshot_paths = [
        raw_root / "screenshots" / "battle-system-design.png",
        raw_root / "screenshots" / "drive-gauge.png",
        raw_root / "screenshots" / "common-system.png",
        raw_root / "screenshots" / "simple-operation-modal.png",
    ]
    checks["screenshots_exist"] = all(path.exists() and path.stat().st_size > 0 for path in screenshot_paths)
    checks["asset_downloads_ok"] = assets_manifest.get("counts", {}).get("failed") == 0
    checks["assets_exclude_known_unwanted_families"] = not any(
        any(token in item.get("path", "") for token in EXCLUDED_ASSET_TOKENS)
        for item in assets_manifest.get("downloaded_assets", [])
    )

    all_passed = all(checks.values())
    if not all_passed:
        notes.append("One or more scoped raw capture checks failed; inspect checks before ingesting this source.")
    else:
        notes.append("Scoped raw capture passed. Full page HTML and full Next.js data JSON were intentionally not stored.")

    return {
        "validation_schema_version": VALIDATION_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "status": "passed" if all_passed else "failed",
        "checks": checks,
        "summary": {
            "kept_text_key_count": text_payload.get("kept_key_count"),
            "downloaded_asset_count": assets_manifest.get("counts", {}).get("downloaded"),
            "omitted_asset_ref_count": assets_manifest.get("counts", {}).get("omitted"),
            "scope_policy": SOURCE_SCOPE,
        },
        "notes": notes,
    }


def normalize_text_for_compare(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def html_text(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", value))


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def capture(repo_root: Path, *, timeout: int) -> dict[str, Any]:
    raw_root = repo_root / "raw" / "web-pages" / "www.streetfighter.com" / "fightingground-battle-system"
    reset_raw_root(repo_root, raw_root)
    api_dir = raw_root / "api"
    raw_root.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)

    captured_at = utc_now()
    page = fetch_text_response(SOURCE_URL, timeout=timeout)
    next_payload = extract_next_data(page.text)
    build_id = next_payload["buildId"]
    source_revision = nextjs_source_revision(build_id)
    data_url = build_data_url(build_id)
    data = fetch_text_response(data_url, timeout=timeout)
    data_payload = json.loads(data.text)
    chunk_url = build_page_chunk_url(page.text)
    chunk = fetch_text_response(chunk_url, timeout=timeout)

    scoped_text = scoped_text_payload(
        data_payload,
        data_url=data_url,
        data_response=data.response,
        source_revision=source_revision,
    )
    write_json(api_dir / "source-text.scoped.json", scoped_text)

    source_provenance = {
        "provenance_schema_version": "capcom_fightingground_battle_system_source_provenance/v1",
        "captured_at_utc": captured_at,
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_type": SOURCE_TYPE,
        "source_url": SOURCE_URL,
        "data_url": data_url,
        "page_chunk_url": chunk_url,
        "source_revision": source_revision,
        "scope_policy": SOURCE_SCOPE,
        "full_source_not_stored": {
            "page_html": True,
            "next_data_json": True,
            "page_chunk_js": True,
            "reason": "The user-selected raw scope excludes unrelated Fighting Ground sections.",
        },
        "responses": {
            "page_html": page.response,
            "next_data_json": data.response,
            "page_chunk_js": chunk.response,
        },
    }
    write_json(raw_root / "source-provenance.json", source_provenance)

    rendered = capture_rendered_state(raw_root, timeout=timeout, source_revision=source_revision)
    asset_urls, omitted_asset_refs = collect_asset_urls(raw_root)
    assets_manifest = download_assets(raw_root, asset_urls, omitted_asset_refs, timeout=timeout)

    metadata = {
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "captured_at_utc": captured_at,
        "publisher": PUBLISHER,
        "game": GAME,
        "locale": LOCALE,
        "source_type": SOURCE_TYPE,
        "source_url": SOURCE_URL,
        "data_url": data_url,
        "page_chunk_url": chunk_url,
        "source_revision": source_revision,
        "storage_policy": "updateable_web_page_capture",
        "scope_policy": SOURCE_SCOPE,
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "capture_method": "scrapling_fetcher_for_provenance_and_assets_and_playwright_chromium_for_scoped_dom",
        "included_sections": [
            "BATTLE SYSTEM DESIGN",
            "DRIVE GAUGE",
            "COMMON SYSTEM",
            "simpleOperationImage modal",
        ],
        "excluded_sections": [
            "SOUND ACCESSIBILITY",
            "CHARACTER DAMAGE",
            "Real Time Commentary",
            "CONTROL TYPE",
            "BATTLE CONTENTS",
        ],
        "artifacts": {
            "source_provenance": "source-provenance.json",
            "scoped_text": "api/source-text.scoped.json",
            "asset_manifest": "assets/manifest.json",
            "rendered_sections": rendered["sections"],
            "screenshots": {
                key: value["path"]
                for key, value in rendered["screenshots"].items()
            },
        },
        "counts": {
            "kept_text_keys": scoped_text["kept_key_count"],
            "downloaded_assets": assets_manifest["counts"]["downloaded"],
            "omitted_asset_refs": assets_manifest["counts"]["omitted"],
        },
        "render_fetch": rendered.get("render_fetch"),
    }
    write_json(raw_root / "metadata.json", metadata)

    validation = validate_capture(raw_root)
    write_json(raw_root / "validation.json", validation)

    artifact_hashes = build_artifact_hashes(raw_root)
    manifest = {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "raw_root": relative(raw_root, repo_root),
        "source_family": "web_page",
        "source_slug": "www.streetfighter.com/fightingground-battle-system",
        "domain": "www.streetfighter.com",
        "page_slug": "fightingground-battle-system",
        "publisher": PUBLISHER,
        "platform": "Next.js",
        "page_title": "Fighting Ground Battle System scope",
        "source_type": SOURCE_TYPE,
        "source_url": SOURCE_URL,
        "data_url": data_url,
        "page_chunk_url": chunk_url,
        "captured_at_utc": captured_at,
        "capture_label": f"{captured_at[:10]}-{build_id}",
        "storage_policy": "updateable_web_page_capture",
        "source_revision": source_revision,
        "canonical_source_artifacts": [
            "api/source-text.scoped.json",
            "rendered/battle-system-design.dom.json",
            "rendered/drive-gauge.dom.json",
            "rendered/common-system.dom.json",
            "rendered/simple-operation-modal.dom.json",
        ],
        "display_evidence_artifacts": [
            "screenshots/battle-system-design.png",
            "screenshots/drive-gauge.png",
            "screenshots/common-system.png",
            "screenshots/simple-operation-modal.png",
        ],
        "metadata": "metadata.json",
        "validation": "validation.json",
        "asset_manifest": "assets/manifest.json",
        "scope_policy": {
            "id": SOURCE_SCOPE,
            "included_sections": metadata["included_sections"],
            "excluded_sections": metadata["excluded_sections"],
            "full_source_artifacts_intentionally_not_stored": [
                "page.html",
                "data.json",
                "page-chunk.js",
            ],
        },
        "artifact_hashes": artifact_hashes,
        "raw_review_status": "pending_human_review",
        "tool": "tools/web_pages/capcom_fightingground_battle_system.py",
    }
    write_json(raw_root / "manifest.json", manifest)
    return {
        "raw_root": relative(raw_root, repo_root),
        "manifest": relative(raw_root / "manifest.json", repo_root),
        "validation_status": validation["status"],
        "downloaded_assets": assets_manifest["counts"]["downloaded"],
        "kept_text_keys": scoped_text["kept_key_count"],
        "build_id": build_id,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--timeout", type=int, default=120_000)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = capture(args.repo_root.resolve(), timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
