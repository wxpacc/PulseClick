DARK_QSS = """
QMainWindow, QWidget {
    background: #1a1a2e;
    color: #f4f6fb;
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 12px;
}
QGroupBox {
    background: #16213e;
    border: 1px solid #243555;
    border-radius: 8px;
    margin-top: 14px;
    padding: 10px 8px 8px 8px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #dce7ff;
}
QLabel#statusDot {
    font-size: 16px;
}
QFrame#statusPanel {
    background: #16213e;
    border: 1px solid #243555;
    border-radius: 8px;
}
QPushButton {
    background: #0f3460;
    border: 0;
    border-radius: 6px;
    min-height: 26px;
    padding: 0 10px;
    color: #f4f6fb;
}
QPushButton:hover {
    background: #15477e;
}
QPushButton:disabled {
    background: #30384d;
    color: #8992a8;
}
QPushButton#primaryButton {
    background: #e94560;
    min-height: 34px;
    font-size: 14px;
    font-weight: 700;
}
QPushButton#primaryButton[running="true"] {
    background: #56637e;
}
QLineEdit, QSpinBox, QComboBox {
    background: #10182b;
    border: 1px solid #31425f;
    border-radius: 4px;
    min-height: 22px;
    padding: 0 6px;
    color: #f4f6fb;
}
QRadioButton, QCheckBox {
    spacing: 6px;
}
QToolTip {
    background: #10182b;
    color: #f4f6fb;
    border: 1px solid #31425f;
}
"""

