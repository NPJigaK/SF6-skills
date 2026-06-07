from __future__ import annotations

from tools.frame_data.official.capture import frame_data_payload_from_dom


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
