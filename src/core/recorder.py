from __future__ import annotations

from PySide6.QtCore import QObject, QRect, Qt, Signal
from PySide6.QtGui import QColor, QCursor, QFont, QPainter
from PySide6.QtWidgets import QApplication, QWidget


class CoordinateOverlay(QWidget):
    def __init__(self, picker: "CoordinatePicker") -> None:
        super().__init__()
        self._picker = picker

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
        painter.setPen(QColor(255, 255, 255))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "点击屏幕任意位置拾取坐标，按 ESC 取消")

    def mousePressEvent(self, event) -> None:  # noqa: N802
        pos = event.globalPosition()
        self._picker.coordinate_picked.emit(int(pos.x()), int(pos.y()))
        self._picker.stop()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() == Qt.Key.Key_Escape:
            self._picker.cancelled.emit()
            self._picker.stop()


class CoordinatePicker(QObject):
    coordinate_picked = Signal(int, int)
    cancelled = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._overlay: CoordinateOverlay | None = None

    def start(self) -> None:
        if self._overlay is not None:
            return
        overlay = CoordinateOverlay(self)
        overlay.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        overlay.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        overlay.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        overlay.setGeometry(self._combined_screen_geometry())
        overlay.show()
        overlay.activateWindow()
        overlay.setFocus()
        self._overlay = overlay

    def stop(self) -> None:
        if self._overlay is not None:
            self._overlay.close()
            self._overlay = None

    def _combined_screen_geometry(self) -> QRect:
        app = QApplication.instance()
        screens = app.screens() if app else []
        if not screens:
            return QRect(0, 0, 1920, 1080)
        min_x = min(screen.geometry().x() for screen in screens)
        min_y = min(screen.geometry().y() for screen in screens)
        max_x = max(screen.geometry().x() + screen.geometry().width() for screen in screens)
        max_y = max(screen.geometry().y() + screen.geometry().height() for screen in screens)
        return QRect(min_x, min_y, max_x - min_x, max_y - min_y)

