from __future__ import annotations

from ..schemas import DerivedNormalizedRecord, OfficialNormalizedRecord
from ..versioning import DERIVATION_RULE_VERSION
from .common import parse_advantage_int, parse_official_active, parse_startup_int


DERIVATION_NOTES = [
    "derived from official_raw only",
    "ignores spacing/pushback",
    "ignores character-specific punish options",
    "ignores invuln/armor/special exceptions",
    "4F baseline",
    f"derivation_rule_version={DERIVATION_RULE_VERSION}",
]


def derive_metrics(records: list[OfficialNormalizedRecord]) -> list[DerivedNormalizedRecord]:
    derived_records: list[DerivedNormalizedRecord] = []
    for record in records:
        block_adv = parse_advantage_int(record.block_adv)
        hit_adv = parse_advantage_int(record.hit_adv)
        startup = parse_startup_int(record.startup)
        active = parse_official_active(record.active)
        punishable_threshold = max(-block_adv, 0) if block_adv is not None else None
        meaty_bonus = max(active.frames - 1, 0) if active.frames is not None else None
        derived_records.append(
            DerivedNormalizedRecord.model_validate(
                {
                    "source": "official",
                    "snapshot_id": record.snapshot_id,
                    "source_row_id": record.source_row_id,
                    "character_slug": record.character_slug,
                    "move_id": record.move_id,
                    "punishable_threshold": punishable_threshold,
                    "is_safe_on_block": None if block_adv is None else block_adv >= -4,
                    "is_plus_on_hit": None if hit_adv is None else hit_adv > 0,
                    "is_plus_on_block": None if block_adv is None else block_adv > 0,
                    "meaty_hit_adv_max": None if hit_adv is None or meaty_bonus is None else hit_adv + meaty_bonus,
                    "meaty_block_adv_max": None if block_adv is None or meaty_bonus is None else block_adv + meaty_bonus,
                    "startup_bucket": _startup_bucket(startup),
                    "simple_punish_adv": punishable_threshold,
                    "derivation_notes": DERIVATION_NOTES,
                    "extraction_confidence": record.extraction_confidence,
                    "manual_review_needed": record.manual_review_needed,
                    "review_reasons": list(record.review_reasons),
                }
            )
        )
    return derived_records


def _startup_bucket(startup: int | None) -> str | None:
    if startup is None:
        return None
    if startup <= 4:
        return "4f_or_faster"
    if startup <= 7:
        return "5_to_7"
    if startup <= 10:
        return "8_to_10"
    return "11_plus"
