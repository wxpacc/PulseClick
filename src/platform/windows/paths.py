from __future__ import annotations

import sys
from pathlib import Path


APP_NAME = "PulseClick"


def app_root_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[3]


def app_data_dir() -> Path:
    return app_root_dir() / "data"


def config_dir() -> Path:
    return app_data_dir()


def log_dir() -> Path:
    return app_data_dir() / "logs"
