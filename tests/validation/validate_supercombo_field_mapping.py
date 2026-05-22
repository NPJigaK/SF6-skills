from __future__ import annotations

import sys

from sf6_knowledge_coach.supercombo_field_mapping import validate_mapping_artifacts


def main() -> int:
    try:
        validate_mapping_artifacts()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("SuperCombo field mapping validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
