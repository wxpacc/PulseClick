from __future__ import annotations

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QInputDialog, QKeySequenceEdit, QMessageBox

from src.core.hotkey import display_hotkey


def ask_profile_name(parent, title: str = "保存配置档案") -> str | None:
    name, ok = QInputDialog.getText(parent, title, "档案名称：")
    if not ok:
        return None
    return name.strip() or None


def show_error(parent, message: str) -> None:
    QMessageBox.warning(parent, "PulseClick", message)


class HotkeyDialog(QDialog):
    def __init__(self, current_hotkey: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("修改启停热键")
        self._editor = QKeySequenceEdit(QKeySequence(display_hotkey(current_hotkey)))

        layout = QFormLayout(self)
        layout.addRow("按下组合键：", self._editor)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def hotkey(self) -> str:
        return self._editor.keySequence().toString(QKeySequence.SequenceFormat.PortableText)

