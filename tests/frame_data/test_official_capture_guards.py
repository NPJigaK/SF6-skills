from __future__ import annotations

from tools.frame_data.official.capture import (
    COLUMN_KEYS,
    frame_data_payload_from_dom,
    frame_rows_from_dom,
    next_build_id_from_html,
    table_dom_payload,
    validate_mode_tab_state,
)


def cell(text: str) -> dict[str, object]:
    return {
        "text": text,
        "token_stream": [{"type": "text", "value": text}],
    }


def test_unknown_body_row_shape_is_rejected() -> None:
    data_cells = [cell("Move")]
    data_cells.extend(cell(str(index)) for index in range(1, len(COLUMN_KEYS)))
    unknown_cells = [cell(str(index)) for index in range(len(COLUMN_KEYS) - 1)]
    table_dom = {
        "rows": [
            {"row_index": 0, "cells": [cell("通常技")]},
            {"row_index": 1, "cells": data_cells},
            {"row_index": 2, "cells": unknown_cells},
        ]
    }

    try:
        frame_rows_from_dom(table_dom)
    except ValueError as exc:
        assert "unexpected Capcom frame-data row shape" in str(exc)
        assert "row_index=2" in str(exc)
    else:
        raise AssertionError("unknown body row shape should fail closed")


def test_tab_state_must_match_requested_mode() -> None:
    tab_state = {
        "requested_mode": "classic",
        "selected_tab_index": 0,
        "tabs": [
            {
                "tab_index": 0,
                "text": "",
                "class_name": "frame_movelist_active__swapped",
                "image_sources": ["/6/assets/images/mode/fg/logo-modern.png"],
                "is_active": True,
            },
            {
                "tab_index": 1,
                "text": "",
                "class_name": "",
                "image_sources": ["/6/assets/images/mode/fg/logo-classic.png"],
                "is_active": False,
            },
        ],
    }

    try:
        validate_mode_tab_state("classic", tab_state)
    except ValueError as exc:
        assert "expected classic tab" in str(exc)
    else:
        raise AssertionError("classic capture should reject a selected Modern tab")


def test_next_build_id_is_extracted_from_captured_page_html() -> None:
    html = (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        '{"buildId":"build-from-source","props":{"pageProps":{}}}'
        "</script></html>"
    )

    assert next_build_id_from_html(html) == "build-from-source"


def test_official_payload_carries_source_revision_when_raw_dom_has_it() -> None:
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
        "headers": [],
        "rows": [
            {"row_index": 0, "cells": [cell("通常技")]},
            {"row_index": 1, "cells": data_cells},
        ],
    }

    payload = frame_data_payload_from_dom(table_dom)

    assert payload["source"]["source_revision"] == {
        "type": "nextjs_build_id",
        "build_id": "build-from-source",
    }


def test_table_dom_payload_carries_source_revision_when_supplied() -> None:
    class Page:
        def evaluate(self, _script: str) -> dict[str, object]:
            return {
                "table_html": "<table></table>",
                "table_text": "",
                "table_rect": {"left": 0, "right": 0, "width": 0, "height": 0},
                "headers": [],
                "rows": [],
            }

    payload = table_dom_payload(
        Page(),
        source_url="https://example.test/frame",
        character_slug="ryu",
        mode="classic",
        source_revision={"type": "nextjs_build_id", "build_id": "build-from-source"},
    )

    assert payload["source_revision"] == {
        "type": "nextjs_build_id",
        "build_id": "build-from-source",
    }


def main() -> int:
    test_unknown_body_row_shape_is_rejected()
    test_tab_state_must_match_requested_mode()
    test_next_build_id_is_extracted_from_captured_page_html()
    test_official_payload_carries_source_revision_when_raw_dom_has_it()
    test_table_dom_payload_carries_source_revision_when_supplied()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
