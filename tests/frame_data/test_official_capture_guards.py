from __future__ import annotations

from tools.frame_data.official.capture import COLUMN_KEYS, frame_rows_from_dom, validate_mode_tab_state


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


def main() -> int:
    test_unknown_body_row_shape_is_rejected()
    test_tab_state_must_match_requested_mode()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
