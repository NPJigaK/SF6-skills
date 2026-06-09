from __future__ import annotations

import json
from pathlib import Path

from tools.frame_data.official.capture import COLUMN_KEYS, frame_data_payload_from_dom, sha256_text
from tools.frame_data.official.validate import validate_mode


def cell(text: str) -> dict[str, object]:
    return {
        "text": text,
        "token_stream": [{"type": "text", "value": text}],
    }


def test_frame_data_payload_contains_rows_and_field_meanings() -> None:
    data_cells = [cell("立ち弱P")]
    data_cells.extend(cell(str(index)) for index in range(1, 15))
    table_dom = {
        "artifact_schema_version": "capcom_frame_table_dom/v1",
        "captured_at_utc": "2026-01-01T00:00:00Z",
        "publisher": "Capcom",
        "game": "Street Fighter 6",
        "locale": "ja-jp",
        "source_url": "https://example.test/frame",
        "character_slug": "ryu",
        "control_scheme": "classic",
        "headers": [
            {
                "row_index": 0,
                "cells": [
                    {
                        "cell_index": 1,
                        "text": "動作フレーム 発生 持続 硬直",
                        "inputs": [{"id": "active_frame"}],
                        "labels": [{"text": "持続", "for_attr": "active_frame"}],
                        "token_stream": [{"type": "text", "value": "持続"}],
                    }
                ],
            }
        ],
        "rows": [
            {"row_index": 0, "cells": [cell("通常技")]},
            {"row_index": 1, "cells": data_cells},
        ],
    }

    payload = frame_data_payload_from_dom(table_dom)

    assert payload["schema_version"] == "capcom_official_frame_data/v2"
    assert payload["source"]["character_slug"] == "ryu"
    assert payload["source"]["control_scheme"] == "classic"
    assert payload["row_count"] == 1
    assert payload["rows"][0]["move_name"] == "立ち弱P"
    assert payload["rows"][0]["input_tokens"] == [{"type": "text", "value": "立ち弱P"}]
    assert payload["field_meanings"]["records"][0]["input_ids"] == ["active_frame"]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def test_validate_mode_allows_output_without_optional_source_revision(tmp_path) -> None:
    raw_dir = tmp_path / "raw" / "frame-data" / "official" / "ryu" / "classic"
    output_dir = tmp_path / "wiki" / "outputs" / "data" / "frame-data" / "official" / "ryu"
    table_html = "<table><tbody></tbody></table>"
    data_cells = [cell("立ち弱P")]
    data_cells.extend(cell(str(index)) for index in range(1, len(COLUMN_KEYS)))
    table_dom = {
        "artifact_schema_version": "capcom_frame_table_dom/v1",
        "captured_at_utc": "2026-01-01T00:00:00Z",
        "publisher": "Capcom",
        "game": "Street Fighter 6",
        "locale": "ja-jp",
        "source_url": "https://example.test/frame",
        "character_slug": "ryu",
        "control_scheme": "classic",
        "source_revision": {"type": "nextjs_build_id", "build_id": "build-from-source"},
        "column_keys": COLUMN_KEYS,
        "table_sha256": sha256_text(table_html),
        "table_text_sha256": sha256_text(""),
        "table_rect": {"left": 0, "right": 10, "width": 10, "height": 10},
        "headers": [],
        "rows": [
            {"row_index": 0, "cells": [cell("通常技")]},
            {"row_index": 1, "cells": data_cells},
        ],
        "data_row_count": 1,
        "category_row_count": 1,
        "unexpected_row_count": 0,
        "unexpected_rows": [],
    }
    output_payload = frame_data_payload_from_dom(table_dom)
    del output_payload["source"]["source_revision"]

    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "page.html").write_text(table_html, encoding="utf-8")
    write_json(raw_dir / "table.dom.json", table_dom)
    write_json(
        raw_dir / "metadata.json",
        {
            "capture_adjustments": {},
            "artifacts": {
                "table_dom_json": {
                    "data_row_count": 1,
                },
                "screenshot_png": {
                    "width": 100,
                    "height": 100,
                },
            },
            "horizontal_metrics": {
                "table_rect_right": 10,
            },
            "overlay_visible_counts_after_cleanup": {
                "cookiebot": 0,
                "navigation": 0,
            },
        },
    )
    write_json(output_dir / "classic.json", output_payload)

    result = validate_mode(tmp_path, "ryu", "classic")

    assert result["row_count"] == 1
