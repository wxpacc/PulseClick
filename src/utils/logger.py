from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from src.platform.windows.paths import log_dir


def setup_logging() -> None:
    logs_path = log_dir()
    logs_path.mkdir(parents=True, exist_ok=True)
    log_file = logs_path / "pulseclick.log"

    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    handler.setFormatter(formatter)
    root.addHandler(handler)
