#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from scrapling.fetchers import StealthySession


BASE_URL = "https://wiki.supercombo.gg"
TAB_NAMES = ("General", "Details", "Meter", "Properties", "Notes")

FRAME_FIELDS = [
    "chara",
    "moveId",
    "moveType",
    "input",
    "name",
    "damage",
    "startup",
    "active",
    "recovery",
    "total",
    "hitAdv",
    "blockAdv",
    "guard",
    "cancel",
    "hitconfirm",
    "chip",
    "dmgScaling",
    "punishAdv",
    "perfParryAdv",
    "DRcancelHit",
    "DRcancelBlk",
    "afterDRHit",
    "afterDRBlk",
    "hitstun",
    "blockstun",
    "hitstop",
    "driveDmgBlk",
    "driveDmgHit",
    "driveGain",
    "superGainHit",
    "superGainBlk",
    "invuln",
    "armor",
    "airborne",
    "atkRange",
    "rangeNotes",
    "jugStart",
    "jugIncrease",
    "jugLimit",
    "projSpeed",
    "pushbackHit",
    "pushbackBlk",
    "images",
    "hitboxes",
    "notes",
]

CHARACTER_FIELDS = [
    "chara",
    "name",
    "portrait",
    "icon",
    "hp",
    "throwRange",
    "throwHurtbox",
    "fwdWalkSpd",
    "bwdWalkSpd",
    "fwdDashSpd",
    "bwdDashSpd",
    "fwdDashDist",
    "bwdDashDist",
    "jumpSpd",
    "jumpApex",
    "fwdJumpDist",
    "bwdJumpDist",
    "dRushMin",
    "dRushBlock",
    "dRushMax",
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
table.cargoDynamicTable,
.dataTables_wrapper,
.dataTables_scroll,
.dataTables_scrollBody {
  overflow: visible !important;
  max-width: none !important;
}
"""


@dataclass(frozen=True)
class CapturePaths:
    root: Path
    screenshots_dir: Path
    images_dir: Path
    cargo_dir: Path
    api_dir: Path
    rendered_dir: Path


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def png_dimensions(path: Path) -> dict[str, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return {
        "width": int.from_bytes(header[16:20], "big"),
        "height": int.from_bytes(header[20:24], "big"),
    }


def response_text(response: Any) -> str:
    body = getattr(response, "body", b"")
    if isinstance(body, str):
        return body
    encoding = getattr(response, "encoding", None) or "utf-8"
    return body.decode(encoding, errors="replace")


def fetch_text(session: StealthySession, url: str, *, timeout_ms: int) -> str:
    response = session.fetch(url, timeout=timeout_ms, wait=1000, network_idle=False)
    if response.status != 200:
        raise RuntimeError(f"GET {url} returned HTTP {response.status}")
    return response_text(response)


def api_url(params: dict[str, str]) -> str:
    return f"{BASE_URL}/api.php?{urlencode(params)}"


def fetch_json(session: StealthySession, url: str, *, timeout_ms: int) -> Any:
    text = fetch_text(session, url, timeout_ms=timeout_ms)
    return json.loads(text)


def fetch_page_metadata(session: StealthySession, titles: list[str], *, timeout_ms: int) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    for title in titles:
        payload = fetch_json(
            session,
            api_url(
                {
                    "action": "query",
                    "prop": "info|revisions",
                    "titles": title,
                    "rvprop": "ids|timestamp|user|comment|size",
                    "rvlimit": "1",
                    "format": "json",
                    "formatversion": "2",
                }
            ),
            timeout_ms=timeout_ms,
        )
        if payload.get("error"):
            return payload
        pages.extend(payload.get("query", {}).get("pages", []))
    return {
        "batchcomplete": True,
        "query": {
            "pages": pages,
        },
    }


def source_revision_metadata(page_metadata: dict[str, Any]) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    for page in page_metadata.get("query", {}).get("pages", []):
        revision = (page.get("revisions") or [{}])[0]
        timestamp = revision.get("timestamp") or page.get("touched")
        pages.append(
            {
                "title": page.get("title"),
                "pageid": page.get("pageid"),
                "lastrevid": page.get("lastrevid"),
                "revision_timestamp": timestamp,
                "touched": page.get("touched"),
            }
        )
    timestamps = [page["revision_timestamp"] for page in pages if page.get("revision_timestamp")]
    latest_timestamp = max(timestamps) if timestamps else None
    return {
        "label_basis": "latest_revision_timestamp_across_data_and_frame_pages",
        "label": latest_timestamp[:10] if latest_timestamp else None,
        "latest_revision_timestamp": latest_timestamp,
        "pages": pages,
    }


def split_top_level(value: str, separator: str = "|") -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    template_depth = 0
    link_depth = 0
    i = 0
    while i < len(value):
        two = value[i : i + 2]
        if two == "{{":
            template_depth += 1
            current.append(two)
            i += 2
            continue
        if two == "}}" and template_depth:
            template_depth -= 1
            current.append(two)
            i += 2
            continue
        if two == "[[":
            link_depth += 1
            current.append(two)
            i += 2
            continue
        if two == "]]" and link_depth:
            link_depth -= 1
            current.append(two)
            i += 2
            continue
        char = value[i]
        if char == separator and template_depth == 0 and link_depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
        i += 1
    parts.append("".join(current))
    return parts


def parse_template_blocks(text: str, template_name: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    needle = "{{" + template_name
    index = 0
    while True:
        start = text.find(needle, index)
        if start < 0:
            break
        depth = 0
        cursor = start
        while cursor < len(text) - 1:
            token = text[cursor : cursor + 2]
            if token == "{{":
                depth += 1
                cursor += 2
                continue
            if token == "}}":
                depth -= 1
                cursor += 2
                if depth == 0:
                    break
                continue
            cursor += 1
        block = text[start:cursor]
        body = block[len(needle) :]
        if body.endswith("}}"):
            body = body[:-2]
        record: dict[str, Any] = {
            "_template": template_name,
            "_block_sha256": sha256_text(block),
        }
        for part in split_top_level(body):
            part = part.strip()
            if not part or part == "}}":
                continue
            if part.startswith("|"):
                part = part[1:].strip()
            if "=" not in part:
                continue
            key, raw_value = part.split("=", 1)
            value = raw_value.strip()
            record[key.strip()] = value
        records.append(record)
        index = cursor
    return records


def parse_display_cargo_queries(text: str) -> list[dict[str, Any]]:
    queries: list[dict[str, Any]] = []
    section = ""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        heading = re.fullmatch(r"=+\s*(.*?)\s*=+", line)
        if heading:
            section = heading.group(1)
        if line.startswith("{{#cargo_query:"):
            block_lines = [lines[i]]
            i += 1
            while i < len(lines):
                block_lines.append(lines[i])
                if lines[i].strip() == "}}":
                    break
                i += 1
            block = "\n".join(block_lines)
            query: dict[str, Any] = {
                "section": section,
                "block_sha256": sha256_text(block),
                "raw": block,
            }
            for part in split_top_level(block):
                part = part.strip()
                if not part or part.startswith("{{#cargo_query:") or part == "}}":
                    continue
                if "=" not in part:
                    continue
                key, value = part.split("=", 1)
                value = value.strip()
                if value.endswith("}}"):
                    value = value[:-2].strip()
                query[key.strip()] = value
            queries.append(query)
        i += 1
    return queries


def cargo_records(payload: Any) -> list[dict[str, str]]:
    records = []
    for item in payload.get("cargoquery", []):
        title = item.get("title", {})
        if isinstance(title, dict):
            records.append({str(key): str(value) for key, value in title.items()})
    return records


def extract_image_refs(character_records: list[dict[str, Any]], frame_records: list[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for record in character_records:
        for field in ("portrait", "icon"):
            value = str(record.get(field, "")).strip()
            if value:
                refs.append(
                    {
                        "source": "CharacterData-SF6",
                        "field": field,
                        "moveId": "",
                        "input": "",
                        "name": str(record.get("name", "")),
                        "filename": value,
                    }
                )
    for record in frame_records:
        for field in ("images", "hitboxes"):
            value = str(record.get(field, "")).strip()
            if not value:
                continue
            for filename in re.split(r"\s*,\s*", value):
                filename = filename.strip()
                if filename:
                    refs.append(
                        {
                            "source": "FrameData-SF6",
                            "field": field,
                            "moveId": str(record.get("moveId", "")),
                            "input": str(record.get("input", "")),
                            "name": str(record.get("name", "")),
                            "filename": filename,
                        }
                    )
    seen: set[tuple[str, str, str]] = set()
    unique_refs = []
    for ref in refs:
        key = (ref["field"], ref["moveId"], ref["filename"])
        if key not in seen:
            unique_refs.append(ref)
            seen.add(key)
    return unique_refs


def mediawiki_title(filename: str) -> str:
    return "File:" + filename.replace("_", " ")


def storage_filename(title: str) -> str:
    name = title.removeprefix("File:").replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9._()+\\[\\]-]+", "_", name)
    return name


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def fetch_imageinfo(session: StealthySession, filenames: list[str], *, timeout_ms: int) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    titles = [mediawiki_title(filename) for filename in sorted(set(filenames))]
    for title_chunk in chunks(titles, 45):
        payload = fetch_json(
            session,
            api_url(
                {
                    "action": "query",
                    "titles": "|".join(title_chunk),
                    "prop": "imageinfo",
                    "iiprop": "url|mime|size|sha1|timestamp|user",
                    "format": "json",
                    "formatversion": "2",
                }
            ),
            timeout_ms=timeout_ms,
        )
        pages.extend(payload.get("query", {}).get("pages", []))
    resolved = [page for page in pages if not page.get("missing") and page.get("imageinfo")]
    missing = [page for page in pages if page.get("missing") or not page.get("imageinfo")]
    return {
        "requested_titles": titles,
        "pages": pages,
        "resolved_count": len(resolved),
        "missing_count": len(missing),
        "missing_titles": [page.get("title", "") for page in missing],
    }


def download_image_from_session(
    session: StealthySession,
    url: str,
    output_path: Path,
    *,
    timeout_ms: int,
) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = session.fetch(url, timeout=timeout_ms, wait=500, network_idle=False)
    if response.status != 200:
        raise RuntimeError(f"GET {url} returned HTTP {response.status}")
    data = response.body
    output_path.write_bytes(data)
    return {
        "path": str(output_path),
        "byte_count": output_path.stat().st_size,
        "sha256": sha256_file(output_path),
    }


def page_table_payload(table: Any, table_index: int) -> dict[str, Any]:
    return {
        "table_index": table_index,
        "class_name": table.get("class_name", ""),
        "rect": table.get("rect"),
        "headers": table.get("headers", []),
        "rows": table.get("rows", []),
        "row_count": table.get("row_count", 0),
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


def capture_page_png(page: Any, path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.evaluate("() => window.scrollTo(0, 0)")
    tmp_path = Path(tempfile.gettempdir()) / f"sf6-supercombo-{path.stem}-{int(time.time() * 1000)}.png"
    page.screenshot(path=str(tmp_path), full_page=True, scale="css", animations="disabled", timeout=180_000)
    path.write_bytes(tmp_path.read_bytes())
    tmp_path.unlink(missing_ok=True)
    return {
        "path": str(path),
        "byte_count": path.stat().st_size,
        "sha256": sha256_file(path),
        **png_dimensions(path),
    }


def capture_rendered_page(
    session: StealthySession,
    *,
    url: str,
    paths: CapturePaths,
    character_slug: str,
    timeout_ms: int,
) -> dict[str, Any]:
    rendered: dict[str, Any] = {}

    def warm_lazy_content(page: Any) -> None:
        page.evaluate(
            """
            async () => {
              const step = Math.max(700, Math.floor(window.innerHeight * 0.85));
              for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise((resolve) => setTimeout(resolve, 50));
              }
              window.scrollTo(0, 0);
            }
            """
        )

    def click_tab_everywhere(page: Any, tab_name: str) -> int:
        return int(
            page.evaluate(
                """
                async (tabName) => {
                  function visible(element) {
                    const style = getComputedStyle(element);
                    const rect = element.getBoundingClientRect();
                    return style.display !== 'none'
                      && style.visibility !== 'hidden'
                      && rect.width > 0
                      && rect.height > 0;
                  }
                  const headers = Array.from(document.querySelectorAll('.tabber__header'));
                  let clicked = 0;
                  for (const header of headers) {
                    const target = Array.from(header.querySelectorAll('a,button'))
                      .find((element) => (element.innerText || '').trim() === tabName && visible(element));
                    if (target) {
                      target.scrollIntoView({block: 'center', inline: 'center'});
                      target.click();
                      clicked += 1;
                      await new Promise((resolve) => setTimeout(resolve, 180));
                    }
                  }
                  window.scrollTo(0, 0);
                  await new Promise((resolve) => setTimeout(resolve, 600));
                  return clicked;
                }
                """,
                tab_name,
            )
        )

    def page_action(page: Any) -> None:
        page.set_viewport_size({"width": 1800, "height": 1100})
        page.wait_for_selector("table.cargoDynamicTable", timeout=timeout_ms)
        page.wait_for_timeout(4000)
        cleanup_capture_page(page)
        warm_lazy_content(page)
        cleanup_capture_page(page)

        rendered["captured_at_utc"] = utc_now()
        rendered["source_url"] = url
        rendered["final_url_at_start"] = page.url
        rendered["character_slug"] = character_slug
        rendered["pre_capture_metrics"] = page.evaluate(
            """
            () => ({
              title: document.title,
              url: location.href,
              table_count: document.querySelectorAll('table.cargoDynamicTable').length,
              tabber_count: document.querySelectorAll('.tabber').length,
              iframe_count: document.querySelectorAll('iframe').length,
              ad_visible_count: Array.from(document.querySelectorAll(
                '#wiki-top-responsive,#wiki-anchor-bottom-desktop,.article-ad-sc,[id^="article-ad"]'
              )).filter((element) => {
                const style = getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                return style.display !== 'none'
                  && style.visibility !== 'hidden'
                  && rect.width > 0
                  && rect.height > 0;
              }).length,
              viewport_width: innerWidth,
              document_scroll_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
              body_height: document.body.scrollHeight
            })
            """
        )

        page_html = page.content()
        page_html_path = paths.rendered_dir / "page.html"
        write_text(page_html_path, page_html)
        rendered["page_html"] = {
            "path": str(page_html_path.relative_to(paths.root)),
            "byte_count": page_html_path.stat().st_size,
            "sha256": sha256_file(page_html_path),
        }
        rendered["character_table"] = page.evaluate(
            """
            () => {
              const table = document.querySelector('table.cargoTable:not(.cargoDynamicTable)');
              if (!table) return null;
              const rect = table.getBoundingClientRect();
              return tablePayload(table, 0, rect);

              function tablePayload(table, tableIndex, rect) {
                return {
                  table_index: tableIndex,
                  class_name: table.className,
                  rect: {left: rect.left, top: rect.top, right: rect.right, width: rect.width, height: rect.height},
                  headers: Array.from(table.querySelectorAll('thead th')).map((cell) => textOf(cell)),
                  rows: Array.from(table.querySelectorAll('tbody tr')).map((row, rowIndex) => ({
                    row_index: rowIndex,
                    cells: Array.from(row.children).map((cell, cellIndex) => cellPayload(cell, cellIndex))
                  })),
                  row_count: table.querySelectorAll('tbody tr').length
                };
              }
              function textOf(element) {
                return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
              }
              function attrs(element) {
                return Object.fromEntries(Array.from(element.attributes).map((attr) => [attr.name, attr.value]));
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
                    resolved_src: img.src,
                    alt: img.getAttribute('alt') || '',
                    attributes: attrs(img)
                  }))
                };
              }
            }
            """
        )

        rendered["tab_states"] = []
        for tab_name in TAB_NAMES:
            clicked = click_tab_everywhere(page, tab_name)
            page.wait_for_timeout(800)
            warm_lazy_content(page)
            cleanup_capture_page(page)
            state = page.evaluate(
                """
                (tabName) => {
                  const tabbers = Array.from(document.querySelectorAll('.tabber'));
                  return {
                    tab: tabName,
                    active_sections: tabbers.map((tabber, sectionIndex) => {
                      const heading = headingFor(tabber);
                      const panels = Array.from(tabber.querySelectorAll('.tabber__panel'));
                      const tabIndex = ['General', 'Details', 'Meter', 'Properties', 'Notes'].indexOf(tabName);
                      const activePanel = panels[tabIndex] || panels.find((panel) => {
                        return panel.getAttribute('aria-hidden') === 'false'
                          || panel.className.includes('active')
                          || panel.className.includes('selected');
                      }) || panels[0];
                      const table = activePanel ? activePanel.querySelector('table.cargoDynamicTable') : null;
                      const rect = table ? table.getBoundingClientRect() : null;
                      const selected = Array.from(tabber.querySelectorAll('.tabber__tab')).filter((tab) => {
                        return tab.getAttribute('aria-selected') === 'true'
                          || tab.getAttribute('aria-current') === 'true'
                          || tab.className.includes('active')
                          || tab.className.includes('selected');
                      }).map((tab) => textOf(tab)).filter(Boolean);
                      return {
                        section_index: sectionIndex,
                        heading,
                        tab: tabName,
                        selected_header_texts: selected,
                        panel_count: panels.length,
                        table: table ? tablePayload(table, sectionIndex, rect) : null,
                        horizontal_inside_viewport: rect ? rect.left >= 0 && rect.right <= window.innerWidth : false
                      };
                    }),
                    iframe_count_after_cleanup: document.querySelectorAll('iframe').length,
                    ad_visible_count_after_cleanup: Array.from(document.querySelectorAll(
                      '#wiki-top-responsive,#wiki-anchor-bottom-desktop,.article-ad-sc,[id^="article-ad"]'
                    )).filter((element) => {
                      const style = getComputedStyle(element);
                      const rect = element.getBoundingClientRect();
                      return style.display !== 'none'
                        && style.visibility !== 'hidden'
                        && rect.width > 0
                        && rect.height > 0;
                    }).length,
                    viewport_width: innerWidth,
                    document_scroll_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
                    body_height: document.body.scrollHeight
                  };

                  function headingFor(element) {
                    let previous = element.previousElementSibling;
                    while (previous) {
                      if (/^H[1-6]$/.test(previous.tagName)) return textOf(previous);
                      if (previous.classList && previous.classList.contains('mw-heading')) return textOf(previous);
                      previous = previous.previousElementSibling;
                    }
                    return '';
                  }
                  function tablePayload(table, tableIndex, rect) {
                    return {
                      table_index: tableIndex,
                      class_name: table.className,
                      rect: {left: rect.left, top: rect.top, right: rect.right, width: rect.width, height: rect.height},
                      headers: Array.from(table.querySelectorAll('thead th')).map((cell) => textOf(cell)),
                      rows: Array.from(table.querySelectorAll('tbody tr')).map((row, rowIndex) => ({
                        row_index: rowIndex,
                        class_name: row.className,
                        cells: Array.from(row.children).map((cell, cellIndex) => cellPayload(cell, cellIndex))
                      })),
                      row_count: Array.from(table.querySelectorAll('tbody tr')).filter((row) => row.children.length > 1).length
                    };
                  }
                  function textOf(element) {
                    return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
                  }
                  function attrs(element) {
                    return Object.fromEntries(Array.from(element.attributes).map((attr) => [attr.name, attr.value]));
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
                        resolved_src: img.src,
                        alt: img.getAttribute('alt') || '',
                        attributes: attrs(img)
                      }))
                    };
                  }
                }
                """,
                tab_name,
            )
            state["clicked_tab_controls"] = clicked
            screenshot_path = paths.screenshots_dir / f"{tab_name.lower()}.png"
            screenshot = capture_page_png(page, screenshot_path)
            screenshot["path"] = str(screenshot_path.relative_to(paths.root))
            state["screenshot"] = screenshot
            rendered["tab_states"].append(state)

    response = session.fetch(
        url,
        wait_selector="table.cargoDynamicTable",
        wait=1000,
        timeout=timeout_ms,
        network_idle=False,
        page_action=page_action,
    )
    rendered["fetch_status"] = response.status
    rendered["body_byte_count"] = len(response.body)
    rendered["final_url"] = getattr(response, "url", None)
    return rendered


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--date-label", default=datetime.now(UTC).strftime("%Y-%m-%d"))
    parser.add_argument("--character", default="JP")
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--timeout-ms", type=int, default=240_000)
    parser.add_argument("--no-download-images", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo_root / "raw" / "frame-data" / "supercombo" / args.character_slug
    paths = CapturePaths(
        root=root,
        screenshots_dir=root / "screenshots",
        images_dir=root / "images" / "files",
        cargo_dir=root / "cargo",
        api_dir=root / "api",
        rendered_dir=root / "rendered",
    )
    for directory in (paths.root, paths.screenshots_dir, paths.images_dir, paths.cargo_dir, paths.api_dir, paths.rendered_dir):
        directory.mkdir(parents=True, exist_ok=True)

    character = args.character
    page_title = f"Street_Fighter_6/{character}/Frame_data"
    data_title = f"Street_Fighter_6/{character}/Data"
    frame_page_url = f"{BASE_URL}/w/{page_title}"
    frame_raw_url = f"{frame_page_url}?action=raw"
    data_raw_url = f"{BASE_URL}/w/{data_title}?action=raw"
    captured_at = utc_now()

    with StealthySession(
        headless=True,
        solve_cloudflare=True,
        timeout=args.timeout_ms,
        wait=1000,
        network_idle=False,
        retries=2,
        user_data_dir=f"/tmp/scrapling-supercombo-{args.character_slug}",
        locale="en-US",
        block_ads=True,
    ) as session:
        data_raw = fetch_text(session, data_raw_url, timeout_ms=args.timeout_ms)
        frame_raw = fetch_text(session, frame_raw_url, timeout_ms=args.timeout_ms)
        write_text(root / "data.raw.wikitext", data_raw)
        write_text(root / "frame-data.raw.wikitext", frame_raw)

        character_templates = parse_template_blocks(data_raw, "CharacterData-SF6")
        frame_templates = parse_template_blocks(data_raw, "FrameData-SF6")
        display_queries = parse_display_cargo_queries(frame_raw)
        write_json(root / "data.templates.json", {"character": character_templates, "frames": frame_templates})
        write_json(root / "frame-data.cargo-queries.json", {"queries": display_queries})

        page_metadata = fetch_page_metadata(
            timeout_ms=args.timeout_ms,
            session=session,
            titles=[data_title, page_title],
        )
        write_json(paths.api_dir / "page-metadata.json", page_metadata)
        source_revision = source_revision_metadata(page_metadata)

        frame_cargo = fetch_json(
            session,
            api_url(
                {
                    "action": "cargoquery",
                    "tables": "SF6_FrameData",
                    "fields": "_rowID=rowID," + ",".join(FRAME_FIELDS),
                    "where": f'chara="{character}"',
                    "order_by": "_rowID",
                    "limit": "500",
                    "format": "json",
                    "formatversion": "2",
                }
            ),
            timeout_ms=args.timeout_ms,
        )
        character_cargo = fetch_json(
            session,
            api_url(
                {
                    "action": "cargoquery",
                    "tables": "SF6_CharacterData",
                    "fields": "_rowID=rowID," + ",".join(CHARACTER_FIELDS),
                    "where": f'chara="{character}"',
                    "order_by": "_rowID",
                    "limit": "50",
                    "format": "json",
                    "formatversion": "2",
                }
            ),
            timeout_ms=args.timeout_ms,
        )
        write_json(paths.cargo_dir / "frame-data.json", frame_cargo)
        write_json(paths.cargo_dir / "character-data.json", character_cargo)

        rendered = capture_rendered_page(
            session,
            url=frame_page_url,
            paths=paths,
            character_slug=args.character_slug,
            timeout_ms=args.timeout_ms,
        )
        write_json(paths.rendered_dir / "tables.dom.json", rendered)

        image_refs = extract_image_refs(character_templates, frame_templates)
        imageinfo = fetch_imageinfo(
            session,
            [ref["filename"] for ref in image_refs],
            timeout_ms=args.timeout_ms,
        )
        write_json(root / "imageinfo.json", imageinfo)

        image_pages_by_title = {page.get("title", ""): page for page in imageinfo.get("pages", [])}
        image_manifest: dict[str, Any] = {
            "image_manifest_schema_version": "supercombo_frame_image_manifest/v1",
            "captured_at_utc": utc_now(),
            "source": "SuperCombo Wiki",
            "character": character,
            "refs": image_refs,
            "downloads": [],
            "missing_titles": imageinfo.get("missing_titles", []),
            "download_images": not args.no_download_images,
        }
        if not args.no_download_images:
            for title, page in sorted(image_pages_by_title.items()):
                infos = page.get("imageinfo") or []
                if page.get("missing") or not infos:
                    continue
                info = infos[0]
                url = info.get("url")
                if not url:
                    continue
                output_path = paths.images_dir / storage_filename(title)
                record: dict[str, Any] = {
                    "title": title,
                    "url": url,
                    "target_path": str(output_path.relative_to(paths.root)),
                    "mime": info.get("mime"),
                    "source_sha1": info.get("sha1"),
                }
                try:
                    if output_path.exists() and output_path.stat().st_size > 0:
                        record.update(
                            {
                                "path": str(output_path),
                                "byte_count": output_path.stat().st_size,
                                "sha256": sha256_file(output_path),
                                "cached": True,
                            }
                        )
                    else:
                        record.update(download_image_from_session(session, url, output_path, timeout_ms=args.timeout_ms))
                    record["ok"] = True
                except Exception as exc:
                    record["ok"] = False
                    record["error"] = repr(exc)
                image_manifest["downloads"].append(record)
        write_json(root / "image-manifest.json", image_manifest)

    artifacts: dict[str, Any] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "metadata.json":
            continue
        artifacts[str(path.relative_to(root))] = {
            "byte_count": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    metadata = {
        "metadata_schema_version": "supercombo_frame_raw_capture_metadata/v1",
        "captured_at_utc": captured_at,
        "publisher": "SuperCombo Wiki",
        "game": "Street Fighter 6",
        "source_type": "community_frame_data",
        "character": character,
        "character_slug": args.character_slug,
        "capture_label": source_revision.get("label") or args.date_label,
        "source_revision": source_revision,
        "storage_policy": "latest_frame_data_mirror",
        "source_urls": {
            "frame_data_page": frame_page_url,
            "frame_data_raw": frame_raw_url,
            "data_raw": data_raw_url,
        },
        "capture_method": "scrapling_stealthy_session_cloudflare_page_action",
        "capture_adjustments": {
            "block_ads": True,
            "removed_iframes_ads_and_sticky_ui_from_screenshots": True,
            "captured_tabs": list(TAB_NAMES),
            "downloaded_resolved_images": not args.no_download_images,
        },
        "counts": {
            "character_templates": len(character_templates),
            "frame_templates": len(frame_templates),
            "display_cargo_queries": len(display_queries),
            "cargo_frame_rows": len(cargo_records(frame_cargo)),
            "cargo_character_rows": len(cargo_records(character_cargo)),
            "image_refs": len(image_refs),
            "distinct_image_refs": len(set(ref["filename"] for ref in image_refs)),
            "imageinfo_resolved": imageinfo.get("resolved_count"),
            "imageinfo_missing": imageinfo.get("missing_count"),
            "downloaded_images": sum(1 for item in image_manifest["downloads"] if item.get("ok")),
            "failed_image_downloads": sum(1 for item in image_manifest["downloads"] if not item.get("ok")),
        },
        "artifacts": artifacts,
    }
    write_json(root / "metadata.json", metadata)
    write_json(
        root / "manifest.json",
        {
            "manifest_schema_version": "supercombo_frame_raw_capture_manifest/v1",
            "captured_at_utc": utc_now(),
            "character": character,
            "character_slug": args.character_slug,
            "capture_label": source_revision.get("label") or args.date_label,
            "source_revision": source_revision,
            "storage_policy": "latest_frame_data_mirror",
            "raw_root": str(root),
            "metadata": "metadata.json",
            "validation": "validation.json",
            "artifacts": sorted(artifacts),
        },
    )
    print(
        json.dumps(
            {
                "raw_root": str(root),
                "counts": metadata["counts"],
                "screenshots": [
                    state["screenshot"]
                    for state in rendered.get("tab_states", [])
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
