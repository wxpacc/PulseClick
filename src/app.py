from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utils.logger import setup_logging


class PulseClickApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        setup_logging()
        self.setApplicationName("PulseClick")
        self.setOrganizationName("PulseClick")
        self.setQuitOnLastWindowClosed(False)

        icon_path = self._resource_path("resources/icon.svg")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.window = MainWindow(icon_path)
        self.window.show()

    @staticmethod
    def _resource_path(relative: str) -> Path:
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
        return base / relative

