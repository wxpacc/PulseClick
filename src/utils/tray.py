from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayController:
    def __init__(
        self,
        icon_path: Path,
        show_window: Callable[[], None],
        start_clicking: Callable[[], None],
        stop_clicking: Callable[[], None],
        quit_app: Callable[[], None],
    ) -> None:
        self._icon = QSystemTrayIcon(QIcon(str(icon_path)))
        self._icon.setToolTip("PulseClick")

        menu = QMenu()
        menu.addAction("显示主窗口", show_window)
        self._start_action = menu.addAction("开始", start_clicking)
        self._stop_action = menu.addAction("停止", stop_clicking)
        menu.addSeparator()
        menu.addAction("退出", quit_app)

        self._icon.setContextMenu(menu)
        self._icon.activated.connect(lambda reason: show_window() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
        self.set_running(False)

    def show(self) -> None:
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._icon.show()

    def hide(self) -> None:
        self._icon.hide()

    def set_running(self, running: bool) -> None:
        self._start_action.setEnabled(not running)
        self._stop_action.setEnabled(running)
        self._icon.setToolTip("PulseClick - 运行中" if running else "PulseClick - 空闲")

