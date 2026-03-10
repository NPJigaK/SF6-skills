from __future__ import annotations

import logging


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("sf6_ingest")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
