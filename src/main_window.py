from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

from src.click_engine import ClickEngine
from src.hotkey_manager import HotkeyManager
from src.coordinate_picker import CoordinatePicker
from src.config_manager import ConfigManager


DARK_STYLE = """
QMainWindow { background-color: #0f1115; }
QWidget {
    background-color: #0f1115;
    color: #EAEAEA;
    font-family: "Segoe UI";
    font-size: 12px;
}
QGroupBox {
    border: none;
    margin-top: 6px;
    font-weight: bold;
    color: #00d4ff;
}
QPushButton#startStopBtn {
    background-color: #00d4ff;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    min-height: 38px;
    color: #0f1115;
}
QPushButton#startStopBtn[running="true"] {
    background-color: #ff3b3b;
    color: white;
}
QFrame#statusFrame {
    background-color: #151922;
    border-radius: 6px;
}
QFrame#line {
    background-color: #1f232b;
    max-height: 1px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PulseClick")
        self.setFixedSize(340, 520)
        self.setStyleSheet(DARK_STYLE)

        self.engine = ClickEngine(self)
        self.hotkey_mgr = HotkeyManager(self)
        self.picker = CoordinatePicker(self)
        self.config_mgr = ConfigManager(self)

        self._init_ui()
        self._init_tray()
        self._connect_signals()
        self._load_config()

        self.hotkey_mgr.start_listening()

    # ================= UI =================

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        # 状态 + 主操作
        layout.addWidget(self._create_status_bar())

        self.start_stop_btn = QPushButton("▶ START / F6")
        self.start_stop_btn.setObjectName("startStopBtn")
        self.start_stop_btn.setProperty("running", False)
        layout.addWidget(self.start_stop_btn)

        layout.addWidget(self._divider())

        layout.addWidget(self._create_core())
        layout.addWidget(self._divider())

        layout.addWidget(self._create_position())
        layout.addWidget(self._divider())

        layout.addWidget(self._create_advanced())
        layout.addWidget(self._divider())

        layout.addWidget(self._create_hotkey())

    def _divider(self):
        line = QFrame()
        line.setObjectName("line")
        return line

    def _create_status_bar(self):
        frame = QFrame()
        frame.setObjectName("statusFrame")
        lay = QHBoxLayout(frame)

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color:#666;font-size:14px;")
        lay.addWidget(self.status_dot)

        self.status_text = QLabel("Idle")
        lay.addWidget(self.status_text)

        lay.addStretch()

        self.cps_label = QLabel("CPS: 0.0")
        lay.addWidget(self.cps_label)

        self.click_count_label = QLabel("0")
        lay.addWidget(self.click_count_label)

        return frame

    # ================= 核心 =================

    def _create_core(self):
        box = QGroupBox("Click")
        lay = QVBoxLayout(box)

        # 鼠标
        row = QHBoxLayout()
        row.addWidget(QLabel("Button"))
        self.btn_left = QRadioButton("L")
        self.btn_right = QRadioButton("R")
        self.btn_middle = QRadioButton("M")
        self.btn_left.setChecked(True)

        self.mouse_btn_group = QButtonGroup(self)
        self.mouse_btn_group.addButton(self.btn_left, 0)
        self.mouse_btn_group.addButton(self.btn_right, 1)
        self.mouse_btn_group.addButton(self.btn_middle, 2)

        row.addWidget(self.btn_left)
        row.addWidget(self.btn_right)
        row.addWidget(self.btn_middle)
        row.addStretch()
        lay.addLayout(row)

        # 类型
        row = QHBoxLayout()
        row.addWidget(QLabel("Type"))
        self.click_single = QRadioButton("Single")
        self.click_double = QRadioButton("Double")
        self.click_single.setChecked(True)

        self.click_type_group = QButtonGroup(self)
        self.click_type_group.addButton(self.click_single, 0)
        self.click_type_group.addButton(self.click_double, 1)

        row.addWidget(self.click_single)
        row.addWidget(self.click_double)
        lay.addLayout(row)

        # 间隔
        row = QHBoxLayout()
        row.addWidget(QLabel("Interval"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 999999)
        self.interval_spin.setValue(100)
        self.interval_spin.setSuffix(" ms")
        row.addWidget(self.interval_spin)
        lay.addLayout(row)

        # 重复
        row = QHBoxLayout()
        self.repeat_infinite = QRadioButton("∞")
        self.repeat_fixed = QRadioButton("N")
        self.repeat_infinite.setChecked(True)

        self.repeat_btn_group = QButtonGroup(self)
        self.repeat_btn_group.addButton(self.repeat_infinite, 0)
        self.repeat_btn_group.addButton(self.repeat_fixed, 1)

        self.repeat_count_spin = QSpinBox()
        self.repeat_count_spin.setEnabled(False)

        row.addWidget(self.repeat_infinite)
        row.addWidget(self.repeat_fixed)
        row.addWidget(self.repeat_count_spin)
        lay.addLayout(row)

        return box

    # ================= 位置 =================

    def _create_position(self):
        box = QGroupBox("Position")
        lay = QVBoxLayout(box)

        self.pos_follow = QRadioButton("Follow")
        self.pos_fixed = QRadioButton("Fixed")
        self.pos_follow.setChecked(True)

        self.pos_btn_group = QButtonGroup(self)
        self.pos_btn_group.addButton(self.pos_follow, 0)
        self.pos_btn_group.addButton(self.pos_fixed, 1)

        lay.addWidget(self.pos_follow)
        lay.addWidget(self.pos_fixed)

        row = QHBoxLayout()
        self.x_spin = QSpinBox()
        self.y_spin = QSpinBox()
        self.pick_btn = QPushButton("Pick")

        self.x_spin.setEnabled(False)
        self.y_spin.setEnabled(False)
        self.pick_btn.setEnabled(False)

        row.addWidget(self.x_spin)
        row.addWidget(self.y_spin)
        row.addWidget(self.pick_btn)
        lay.addLayout(row)

        return box

    # ================= 高级 =================

    def _create_advanced(self):
        self.adv = QGroupBox("Advanced ▶")
        self.adv.setCheckable(True)
        self.adv.setChecked(False)

        lay = QVBoxLayout(self.adv)

        self.random_check = QCheckBox("Random Delay")
        lay.addWidget(self.random_check)

        row = QHBoxLayout()
        self.random_min_spin = QSpinBox()
        self.random_max_spin = QSpinBox()
        self.random_min_spin.setEnabled(False)
        self.random_max_spin.setEnabled(False)

        row.addWidget(self.random_min_spin)
        row.addWidget(QLabel("-"))
        row.addWidget(self.random_max_spin)
        lay.addLayout(row)

        row = QHBoxLayout()
        self.profile_combo = QComboBox()
        self.profile_combo.addItem("Default")

        self.profile_save_btn = QPushButton("Save")
        self.profile_load_btn = QPushButton("Load")

        row.addWidget(self.profile_combo)
        row.addWidget(self.profile_save_btn)
        row.addWidget(self.profile_load_btn)
        lay.addLayout(row)

        self.adv.toggled.connect(self._toggle_adv)
        return self.adv

    def _toggle_adv(self, checked):
        for i in range(self.adv.layout().count()):
            w = self.adv.layout().itemAt(i).widget()
            if w:
                w.setVisible(checked)

    # ================= 热键 =================

    def _create_hotkey(self):
        w = QWidget()
        lay = QHBoxLayout(w)

        lay.addWidget(QLabel("Hotkey"))

        self.hotkey_label = QLabel("F6")
        lay.addWidget(self.hotkey_label)

        self.hotkey_record_btn = QPushButton("Edit")
        lay.addWidget(self.hotkey_record_btn)

        lay.addStretch()
        return w

    # ================= 信号 =================

    def _connect_signals(self):
        self.start_stop_btn.clicked.connect(self.engine.toggle)

        self.repeat_btn_group.idToggled.connect(self._on_repeat_changed)
        self.pos_btn_group.idToggled.connect(self._on_pos_changed)
        self.random_check.toggled.connect(self._on_random_changed)

        self.engine.state_changed.connect(self._on_engine_state_changed)

    def _on_repeat_changed(self):
        self.repeat_count_spin.setEnabled(self.repeat_btn_group.checkedId() == 1)

    def _on_pos_changed(self):
        enabled = self.pos_btn_group.checkedId() == 1
        self.x_spin.setEnabled(enabled)
        self.y_spin.setEnabled(enabled)
        self.pick_btn.setEnabled(enabled)

    def _on_random_changed(self):
        enabled = self.random_check.isChecked()
        self.random_min_spin.setEnabled(enabled)
        self.random_max_spin.setEnabled(enabled)

    def _on_engine_state_changed(self, running):
        if running:
            self.start_stop_btn.setText("■ STOP / F6")
            self.start_stop_btn.setProperty("running", True)
            self.status_dot.setStyleSheet("color:#00ff9c;font-size:14px;")
            self.status_text.setText("Running")
        else:
            self.start_stop_btn.setText("▶ START / F6")
            self.start_stop_btn.setProperty("running", False)
            self.status_dot.setStyleSheet("color:#666;font-size:14px;")
            self.status_text.setText("Idle")

        self.start_stop_btn.style().unpolish(self.start_stop_btn)
        self.start_stop_btn.style().polish(self.start_stop_btn)

    # ================= 托盘 =================

    def _init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/icon.svg"))

        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", self.close)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    # ================= 配置 =================

    def _load_config(self):
        pass
