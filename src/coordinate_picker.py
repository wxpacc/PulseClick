from PySide6.QtCore import QObject, Signal, Qt, QRect
from PySide6.QtGui import QScreen, QCursor, QFont, QColor, QPainter
from PySide6.QtWidgets import QWidget, QApplication


class _OverlayWidget(QWidget):
    def __init__(self, picker):
        super().__init__()
        self._picker = picker

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont()
        font.setPointSize(24)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignCenter, "点击屏幕任意位置拾取坐标 | 按 ESC 取消")
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.globalPosition()
            x = int(pos.x())
            y = int(pos.y())
            self._picker.coordinate_picked.emit(x, y)
            self._picker.stop_picking()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._picker.picking_cancelled.emit()
            self._picker.stop_picking()


class CoordinatePicker(QObject):
    coordinate_picked = Signal(int, int)
    picking_cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._overlay = None
        self._picking = False

    def start_picking(self):
        if self._picking:
            return
        self._picking = True
        self._overlay = _OverlayWidget(self)
        self._overlay.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self._overlay.setAttribute(Qt.WA_TranslucentBackground, False)
        self._overlay.setWindowOpacity(0.3)
        self._overlay.setAutoFillBackground(True)
        palette = self._overlay.palette()
        palette.setColor(self._overlay.backgroundRole(), QColor(0, 0, 0))
        self._overlay.setPalette(palette)
        self._overlay.setCursor(QCursor(Qt.CrossCursor))
        self._overlay.setFocusPolicy(Qt.StrongFocus)
        combined_geometry = self._get_combined_geometry()
        self._overlay.setGeometry(combined_geometry)
        self._overlay.show()
        self._overlay.setFocus()

    def stop_picking(self):
        if not self._picking:
            return
        self._picking = False
        if self._overlay is not None:
            self._overlay.close()
            self._overlay = None

    def _get_combined_geometry(self):
        app = QApplication.instance()
        screens = app.screens()
        if not screens:
            return QRect(0, 0, 1920, 1080)
        min_x = min(s.geometry().x() for s in screens)
        min_y = min(s.geometry().y() for s in screens)
        max_x = max(s.geometry().x() + s.geometry().width() for s in screens)
        max_y = max(s.geometry().y() + s.geometry().height() for s in screens)
        return QRect(min_x, min_y, max_x - min_x, max_y - min_y)
