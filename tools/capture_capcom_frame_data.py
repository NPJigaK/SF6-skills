#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from scrapling.fetchers import DynamicFetcher


MODE_TABS = {
    "classic": 0,
    "modern": 1,
}

COLUMN_KEYS = [
    "move",
    "startup",
    "active",
    "recovery",
    "on_hit",
    "on_block",
    "cancel",
    "damage",
    "combo_scaling",
    "drive_gain_on_hit",
    "drive_loss_on_block",
    "drive_loss_on_punish_counter",
    "sa_gain",
    "attribute",
    "notes",
]

CSV_FIELDS = [
    "publisher",
    "game",
    "locale",
    "source_url",
    "raw_capture_path",
    "screenshot_path",
    "character_slug",
    "control_scheme",
    "category_order",
    "category",
    "row_order",
    "move_name",
    "input_raw_display",
    "input_token_json",
    "startup",
    "active",
    "recovery",
    "on_hit",
    "on_block",
    "cancel",
    "damage",
    "combo_scaling",
    "drive_gain_on_hit",
    "drive_loss_on_block",
    "drive_loss_on_punish_counter",
    "sa_gain",
    "attribute",
    "notes",
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
#framearea,
[class*="frame_framearea"],
[class*="frame_frame_inner"] {
  overflow: visible !important;
  max-width: none !important;
}
"""


@dataclass(frozen=True)
class RawModeCapture:
    mode: str
    raw_dir: Path
    page_html_path: Path
    table_dom_path: Path
    screenshot_path: Path
    metadata_path: Path
    row_count: int
    table_hash: str


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


def remove_obstructions(page: Any) -> None:
    page.add_style_tag(content=CAPTURE_CSS)
    page.evaluate(
        """
        () => {
          const selectors = [
            '#CybotCookiebotDialog',
            '#CybotCookiebotDialogBodyUnderlay',
            '#CookiebotWidget',
            '[id^="CybotCookiebot"]',
            '[class*="CybotCookiebot"]',
            '[class*="CookiebotWidget"]',
            'header[class*="layout_header"]',
            '[class*="layout_header__nav__global"] ul',
            '[class*="layout_header__nav__languages"] dd',
            '[class*="layout_user_nav_list"]'
          ];
          for (const selector of selectors) {
            for (const element of document.querySelectorAll(selector)) {
              element.remove();
            }
          }
        }
        """
    )


def ensure_full_table_width(page: Any, minimum_width: int, viewport_height: int) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for _ in range(4):
        metrics = page.evaluate(
            """
            () => {
              const table = document.querySelector('table');
              const framearea = document.querySelector('#framearea') || document.querySelector('[class*="frame_framearea"]');
              const inner = document.querySelector('[class*="frame_frame_inner"]') || table?.parentElement;
              const tableRect = table.getBoundingClientRect();
              return {
                viewport_width: window.innerWidth,
                document_scroll_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
                table_rect_left: tableRect.left,
                table_rect_right: tableRect.right,
                table_rect_width: tableRect.width,
                table_scroll_width: table.scrollWidth,
                framearea_scroll_width: framearea.scrollWidth,
                inner_scroll_width: inner.scrollWidth
              };
            }
            """
        )
        required_width = max(
            minimum_width,
            int(metrics["document_scroll_width"]),
            int(metrics["table_rect_right"]),
            int(metrics["table_scroll_width"]),
            int(metrics["framearea_scroll_width"]),
            int(metrics["inner_scroll_width"]),
        )
        target_width = required_width + 24
        if target_width <= int(metrics["viewport_width"]):
            return metrics
        page.set_viewport_size({"width": target_width, "height": viewport_height})
        page.wait_for_timeout(500)
        remove_obstructions(page)
    return metrics


def visible_overlay_counts(page: Any) -> dict[str, int]:
    return page.evaluate(
        """
        () => {
          function visibleCount(selectors) {
            const elements = selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)));
            return elements.filter((element) => {
              const style = getComputedStyle(element);
              const rect = element.getBoundingClientRect();
              return style.display !== 'none'
                && style.visibility !== 'hidden'
                && Number(style.opacity || '1') !== 0
                && rect.width > 0
                && rect.height > 0;
            }).length;
          }
          return {
            cookiebot: visibleCount([
              '#CybotCookiebotDialog',
              '#CybotCookiebotDialogBodyUnderlay',
              '#CookiebotWidget',
              '[id^="CybotCookiebot"]',
              '[class*="CybotCookiebot"]',
              '[class*="CookiebotWidget"]'
            ]),
            navigation: visibleCount([
              'header[class*="layout_header"]',
              '[class*="layout_header__nav__global"] ul',
              '[class*="layout_header__nav__languages"] dd',
              '[class*="layout_user_nav_list"]'
            ])
          };
        }
        """
    )


def table_dom_payload(page: Any, *, source_url: str, character_slug: str, mode: str) -> dict[str, Any]:
    payload = page.evaluate(
        """
        () => {
          const table = document.querySelector('table');
          const headers = Array.from(table.querySelectorAll('thead tr')).map((tr, rowIndex) => ({
            row_index: rowIndex,
            cells: Array.from(tr.children).map((cell, cellIndex) => cellPayload(cell, cellIndex))
          }));
          const bodyRows = Array.from(table.querySelectorAll('tbody tr')).map((tr, rowIndex) => ({
            row_index: rowIndex,
            class_name: tr.className,
            cells: Array.from(tr.children).map((cell, cellIndex) => cellPayload(cell, cellIndex))
          }));
          const rect = table.getBoundingClientRect();
          return {
            table_html: table.outerHTML,
            table_text: table.innerText,
            table_rect: {left: rect.left, right: rect.right, width: rect.width, height: rect.height},
            headers,
            rows: bodyRows
          };

          function attrs(element) {
            return Object.fromEntries(Array.from(element.attributes).map((attr) => [attr.name, attr.value]));
          }

          function textOf(element) {
            return (element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim();
          }

          function cellPayload(cell, cellIndex) {
            return {
              cell_index: cellIndex,
              tag_name: cell.tagName.toLowerCase(),
              attributes: attrs(cell),
              class_name: cell.className,
              rowspan: cell.getAttribute('rowspan'),
              colspan: cell.getAttribute('colspan'),
              text: textOf(cell),
              html: cell.innerHTML,
              images: Array.from(cell.querySelectorAll('img')).map((img, imageIndex) => ({
                image_index: imageIndex,
                src: img.getAttribute('src'),
                resolved_src: img.src,
                alt: img.getAttribute('alt') || '',
                class_name: img.className,
                attributes: attrs(img)
              })),
              inputs: Array.from(cell.querySelectorAll('input')).map((input, inputIndex) => ({
                input_index: inputIndex,
                type: input.getAttribute('type'),
                id: input.getAttribute('id'),
                name: input.getAttribute('name'),
                value: input.getAttribute('value'),
                aria_label: input.getAttribute('aria-label'),
                checked: input.checked,
                attributes: attrs(input)
              })),
              labels: Array.from(cell.querySelectorAll('label')).map((label, labelIndex) => ({
                label_index: labelIndex,
                text: textOf(label),
                for_attr: label.getAttribute('for'),
                attributes: attrs(label)
              })),
              token_stream: tokenStream(cell)
            };
          }

          function tokenStream(root) {
            const tokens = [];
            walk(root, tokens);
            return tokens.filter((token) => token.value !== '');
          }

          function walk(node, tokens) {
            if (node.nodeType === Node.TEXT_NODE) {
              const text = node.textContent.replace(/\\s+/g, ' ').trim();
              if (text) tokens.push({type: 'text', value: text});
              return;
            }
            if (node.nodeType !== Node.ELEMENT_NODE) return;
            const element = node;
            const tag = element.tagName.toLowerCase();
            if (tag === 'img') {
              const src = element.getAttribute('src') || '';
              const basename = src.split('/').pop() || '';
              const derivedValue = (element.getAttribute('alt') || basename.replace(/\\.[^.]+$/, '')).trim();
              tokens.push({
                type: 'image',
                value: derivedValue,
                src,
                resolved_src: element.src,
                class_name: element.className
              });
              return;
            }
            if (tag === 'br') {
              tokens.push({type: 'separator', value: '|'});
              return;
            }
            for (const child of Array.from(element.childNodes)) {
              walk(child, tokens);
            }
            if (['p', 'li', 'div'].includes(tag)) {
              tokens.push({type: 'separator', value: '|'});
            }
          }
        }
        """
    )
    rows = payload["rows"]
    return {
        "artifact_schema_version": "capcom_frame_table_dom/v1",
        "captured_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publisher": "Capcom",
        "game": "Street Fighter 6",
        "locale": "ja-jp",
        "source_url": source_url,
        "character_slug": character_slug,
        "control_scheme": mode,
        "column_keys": COLUMN_KEYS,
        "table_sha256": sha256_text(payload["table_html"]),
        "table_text_sha256": sha256_text(payload["table_text"]),
        "table_rect": payload["table_rect"],
        "headers": payload["headers"],
        "rows": rows,
        "data_row_count": sum(1 for row in rows if len(row["cells"]) == len(COLUMN_KEYS)),
        "category_row_count": sum(1 for row in rows if len(row["cells"]) == 1),
    }


def input_raw_display(move_cell: dict[str, Any]) -> str:
    values = []
    for token in move_cell.get("token_stream", []):
        if token["type"] == "separator":
            continue
        value = str(token.get("value", "")).strip()
        if value:
            values.append(value)
    if not values:
        return ""
    move_name = values[0]
    return " ".join(value for value in values[1:] if value != move_name)


def move_name_from_cell(move_cell: dict[str, Any]) -> str:
    for token in move_cell.get("token_stream", []):
        if token.get("type") == "text" and str(token.get("value", "")).strip():
            return str(token["value"]).strip()
    return str(move_cell.get("text", "")).strip()


def csv_rows_from_dom(table_dom: dict[str, Any], raw_capture_path: str, screenshot_path: str) -> list[dict[str, str]]:
    records = []
    category = ""
    category_order = 0
    row_order = 0
    for row in table_dom["rows"]:
        cells = row["cells"]
        if len(cells) == 1:
            category = cells[0]["text"]
            category_order += 1
            continue
        if len(cells) != len(COLUMN_KEYS):
            continue
        row_order += 1
        mapped = dict(zip(COLUMN_KEYS, cells, strict=True))
        records.append(
            {
                "publisher": table_dom.get("publisher", "Capcom"),
                "game": table_dom.get("game", "Street Fighter 6"),
                "locale": table_dom.get("locale", "ja-jp"),
                "source_url": table_dom["source_url"],
                "raw_capture_path": raw_capture_path,
                "screenshot_path": screenshot_path,
                "character_slug": table_dom["character_slug"],
                "control_scheme": table_dom["control_scheme"],
                "category_order": str(category_order),
                "category": category,
                "row_order": str(row_order),
                "move_name": move_name_from_cell(mapped["move"]),
                "input_raw_display": input_raw_display(mapped["move"]),
                "input_token_json": json.dumps(mapped["move"].get("token_stream", []), ensure_ascii=False),
                "startup": mapped["startup"]["text"],
                "active": mapped["active"]["text"],
                "recovery": mapped["recovery"]["text"],
                "on_hit": mapped["on_hit"]["text"],
                "on_block": mapped["on_block"]["text"],
                "cancel": mapped["cancel"]["text"],
                "damage": mapped["damage"]["text"],
                "combo_scaling": mapped["combo_scaling"]["text"],
                "drive_gain_on_hit": mapped["drive_gain_on_hit"]["text"],
                "drive_loss_on_block": mapped["drive_loss_on_block"]["text"],
                "drive_loss_on_punish_counter": mapped["drive_loss_on_punish_counter"]["text"],
                "sa_gain": mapped["sa_gain"]["text"],
                "attribute": mapped["attribute"]["text"],
                "notes": mapped["notes"]["text"],
            }
        )
    return records


def field_meanings_from_dom(table_dom: dict[str, Any]) -> dict[str, Any]:
    records = []
    for header_row in table_dom.get("headers", []):
        for cell in header_row.get("cells", []):
            token_stream = cell.get("token_stream", [])
            explanation_tokens = [
                token
                for token in token_stream
                if token.get("type") == "text" and str(token.get("value", "")).strip()
            ]
            if not cell.get("inputs") and len(explanation_tokens) <= 1:
                continue
            records.append(
                {
                    "header_row_index": header_row.get("row_index"),
                    "header_cell_index": cell.get("cell_index"),
                    "header_text": cell.get("text", ""),
                    "input_ids": [item.get("id") for item in cell.get("inputs", []) if item.get("id")],
                    "labels": [
                        {
                            "text": item.get("text", ""),
                            "for_attr": item.get("for_attr"),
                        }
                        for item in cell.get("labels", [])
                    ],
                    "token_stream": token_stream,
                }
            )
    return {
        "artifact_schema_version": "capcom_frame_field_meanings/v1",
        "source_captured_at_utc": table_dom.get("captured_at_utc"),
        "publisher": table_dom.get("publisher", "Capcom"),
        "game": table_dom.get("game", "Street Fighter 6"),
        "locale": table_dom.get("locale", "ja-jp"),
        "source_url": table_dom["source_url"],
        "character_slug": table_dom["character_slug"],
        "control_scheme": table_dom["control_scheme"],
        "records": records,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def capture_mode(
    *,
    page: Any,
    source_url: str,
    character_slug: str,
    mode: str,
    output_root: Path,
    date_label: str,
    viewport_width: int,
    viewport_height: int,
) -> RawModeCapture:
    tab_index = MODE_TABS[mode]
    tabs = page.locator('ul[class*="frame_movelist_tabs"] li')
    if tab_index > 0:
        tabs.nth(tab_index).click()
    else:
        tabs.nth(0).click()
    page.wait_for_timeout(1000)
    page.wait_for_selector("table", timeout=120_000)
    remove_obstructions(page)
    horizontal_metrics = ensure_full_table_width(page, viewport_width, viewport_height)

    raw_dir = output_root / "raw" / "official" / "frame-data" / date_label / character_slug / mode
    raw_dir.mkdir(parents=True, exist_ok=True)
    page_html_path = raw_dir / "page.html"
    table_dom_path = raw_dir / "table.dom.json"
    screenshot_path = raw_dir / "screenshot.png"
    metadata_path = raw_dir / "metadata.json"

    page_html = page.content()
    page_html_path.write_text(page_html, encoding="utf-8")
    table_dom = table_dom_payload(page, source_url=source_url, character_slug=character_slug, mode=mode)
    write_json(table_dom_path, table_dom)
    page.screenshot(path=str(screenshot_path), full_page=True, scale="css")

    overlay_counts = visible_overlay_counts(page)
    metadata = {
        "metadata_schema_version": "capcom_frame_raw_capture_metadata/v1",
        "captured_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publisher": "Capcom",
        "game": "Street Fighter 6",
        "locale": "ja-jp",
        "source_type": "official_frame_data",
        "source_url": source_url,
        "final_url": page.url,
        "character_slug": character_slug,
        "control_scheme": mode,
        "capture_method": "scrapling_dynamic_fetcher_page_action",
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "capture_adjustments": {
            "selected_frame_data_tab_index": tab_index,
            "cookiebot_removed_from_capture_dom": True,
            "site_header_navigation_removed_from_capture_dom": True,
            "viewport_expanded_to_table_width": True,
        },
        "overlay_visible_counts_after_cleanup": overlay_counts,
        "horizontal_metrics": horizontal_metrics,
        "artifacts": {
            "page_html": {
                "path": "page.html",
                "sha256": sha256_file(page_html_path),
                "byte_count": page_html_path.stat().st_size,
            },
            "table_dom_json": {
                "path": "table.dom.json",
                "sha256": sha256_file(table_dom_path),
                "byte_count": table_dom_path.stat().st_size,
                "data_row_count": table_dom["data_row_count"],
                "category_row_count": table_dom["category_row_count"],
            },
            "screenshot_png": {
                "path": "screenshot.png",
                "sha256": sha256_file(screenshot_path),
                "byte_count": screenshot_path.stat().st_size,
                **png_dimensions(screenshot_path),
                "captured_in_same_browser_state": True,
            },
        },
    }
    write_json(metadata_path, metadata)
    return RawModeCapture(
        mode=mode,
        raw_dir=raw_dir,
        page_html_path=page_html_path,
        table_dom_path=table_dom_path,
        screenshot_path=screenshot_path,
        metadata_path=metadata_path,
        row_count=table_dom["data_row_count"],
        table_hash=table_dom["table_sha256"],
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--character-slug", default="jp")
    parser.add_argument("--date-label", default="2026-05-26")
    parser.add_argument("--source-url")
    parser.add_argument("--output-root", type=Path, default=Path("."))
    parser.add_argument("--viewport-width", type=int, default=1920)
    parser.add_argument("--viewport-height", type=int, default=1080)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.source_url = args.source_url or f"https://www.streetfighter.com/6/ja-jp/character/{args.character_slug}/frame"
    expected_path = f"/character/{args.character_slug}/frame"
    if expected_path not in args.source_url:
        raise ValueError(
            f"--source-url must match --character-slug; expected URL containing {expected_path!r}, got {args.source_url!r}"
        )
    captures: list[RawModeCapture] = []
    csv_rows_by_mode: dict[str, list[dict[str, str]]] = {}

    def action(page: Any) -> None:
        page.set_viewport_size({"width": args.viewport_width, "height": args.viewport_height})
        page.wait_for_selector("table", timeout=120_000)
        page.wait_for_load_state("networkidle", timeout=120_000)
        page.wait_for_timeout(1000)
        remove_obstructions(page)
        for mode in MODE_TABS:
            capture = capture_mode(
                page=page,
                source_url=args.source_url,
                character_slug=args.character_slug,
                mode=mode,
                output_root=args.output_root,
                date_label=args.date_label,
                viewport_width=args.viewport_width,
                viewport_height=args.viewport_height,
            )
            captures.append(capture)
            table_dom = json.loads(capture.table_dom_path.read_text(encoding="utf-8"))
            raw_rel = capture.raw_dir.relative_to(args.output_root).as_posix()
            csv_rows_by_mode[mode] = csv_rows_from_dom(
                table_dom,
                raw_capture_path=raw_rel,
                screenshot_path=f"{raw_rel}/screenshot.png",
            )

    DynamicFetcher.fetch(
        args.source_url,
        headless=True,
        network_idle=True,
        timeout=120_000,
        wait_selector="table",
        wait=500,
        page_action=action,
    )

    output_data_dir = args.output_root / "wiki" / "outputs" / "data"
    for mode, rows in csv_rows_by_mode.items():
        write_csv(output_data_dir / "frame-data" / args.character_slug / f"{mode}.csv", rows)
        table_dom_path = (
            args.output_root
            / "raw"
            / "official"
            / "frame-data"
            / args.date_label
            / args.character_slug
            / mode
            / "table.dom.json"
        )
        table_dom = json.loads(
            table_dom_path.read_text(encoding="utf-8")
        )
        write_json(
            output_data_dir / "frame-data" / args.character_slug / f"{mode}.field-meanings.json",
            field_meanings_from_dom(table_dom),
        )

    manifest = {
        "manifest_schema_version": "capcom_frame_raw_capture_manifest/v1",
        "created_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publisher": "Capcom",
        "game": "Street Fighter 6",
        "locale": "ja-jp",
        "source_type": "official_frame_data",
        "source_url": args.source_url,
        "character_slug": args.character_slug,
        "date_label": args.date_label,
        "raw_review_status": "pending_human_review",
        "repository_scope": "repo_raw_capture",
        "captures": [
            {
                "mode": capture.mode,
                "raw_dir": capture.raw_dir.relative_to(args.output_root).as_posix(),
                "page_html": capture.page_html_path.relative_to(args.output_root).as_posix(),
                "table_dom_json": capture.table_dom_path.relative_to(args.output_root).as_posix(),
                "screenshot_png": capture.screenshot_path.relative_to(args.output_root).as_posix(),
                "metadata_json": capture.metadata_path.relative_to(args.output_root).as_posix(),
                "row_count": capture.row_count,
                "table_sha256": capture.table_hash,
            }
            for capture in captures
        ],
        "derived_outputs": [
            f"wiki/outputs/data/frame-data/{args.character_slug}/{mode}.csv"
            for mode in csv_rows_by_mode
        ] + [
            f"wiki/outputs/data/frame-data/{args.character_slug}/{mode}.field-meanings.json"
            for mode in csv_rows_by_mode
        ],
        "tool": "tools/capture_capcom_frame_data.py",
    }
    manifest_path = (
        args.output_root
        / "raw"
        / "official"
        / "frame-data"
        / args.date_label
        / args.character_slug
        / "manifest.json"
    )
    write_json(manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
