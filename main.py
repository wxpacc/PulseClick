import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.main_window import MainWindow


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("PulseClick")
        self.setOrganizationName("PulseClick")
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "resources", "icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.window = MainWindow()
        if os.path.exists(icon_path):
            self.window.setWindowIcon(QIcon(icon_path))
        self.window.show()


def main():
    app = App(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
