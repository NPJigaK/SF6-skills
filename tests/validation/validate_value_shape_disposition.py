from __future__ import annotations

import sys

from sf6_knowledge_coach.value_shape_disposition import validate_disposition_artifacts


def main() -> int:
    try:
        validate_disposition_artifacts()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Value-shape disposition validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
