from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QAction, QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QRadioButton,
    QButtonGroup, QCheckBox, QPushButton, QLineEdit,
    QComboBox, QSystemTrayIcon, QMenu, QMessageBox,
    QGroupBox, QSizePolicy, QFrame,
)
from src.click_engine import ClickEngine
from src.hotkey_manager import HotkeyManager
from src.coordinate_picker import CoordinatePicker
from src.config_manager import ConfigManager


DARK_STYLE = """
QMainWindow {
    background-color: #1A1A2E;
}
QWidget {
    background-color: #1A1A2E;
    color: #E0E0E0;
    font-family: "Segoe UI", "Noto Sans CJK SC", sans-serif;
    font-size: 12px;
}
QGroupBox {
    border: 1px solid #2A2A4A;
    border-radius: 6px;
    margin-top: 8px;
    padding: 12px 8px 8px 8px;
    font-weight: bold;
    font-size: 11px;
    color: #4FC3F7;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}
QLabel {
    background: transparent;
    font-size: 11px;
}
QRadioButton {
    background: transparent;
    spacing: 4px;
    font-size: 11px;
}
QRadioButton::indicator {
    width: 14px;
    height: 14px;
    border: 2px solid #4FC3F7;
    border-radius: 8px;
    background: #1A1A2E;
}
QRadioButton::indicator:checked {
    background: #4FC3F7;
}
QCheckBox {
    background: transparent;
    spacing: 4px;
    font-size: 11px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 2px solid #4FC3F7;
    border-radius: 3px;
    background: #1A1A2E;
}
QCheckBox::indicator:checked {
    background: #4FC3F7;
}
QSpinBox, QDoubleSpinBox, QLineEdit {
    background-color: #16213E;
    border: 1px solid #2A2A4A;
    border-radius: 4px;
    padding: 3px 6px;
    color: #E0E0E0;
    font-size: 11px;
    min-height: 22px;
}
QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
    border-color: #4FC3F7;
}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #16213E;
    border: none;
    width: 16px;
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #2A2A4A;
}
QComboBox {
    background-color: #16213E;
    border: 1px solid #2A2A4A;
    border-radius: 4px;
    padding: 3px 8px;
    color: #E0E0E0;
    font-size: 11px;
    min-height: 22px;
}
QComboBox:hover {
    border-color: #4FC3F7;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #16213E;
    border: 1px solid #2A2A4A;
    color: #E0E0E0;
    selection-background-color: #4FC3F7;
    selection-color: #1A1A2E;
}
QPushButton {
    background-color: #16213E;
    border: 1px solid #2A2A4A;
    border-radius: 4px;
    padding: 5px 12px;
    color: #E0E0E0;
    font-size: 11px;
    min-height: 24px;
}
QPushButton:hover {
    background-color: #2A2A4A;
    border-color: #4FC3F7;
}
QPushButton:pressed {
    background-color: #4FC3F7;
    color: #1A1A2E;
}
QPushButton#startStopBtn {
    background-color: #0D7377;
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: bold;
    min-height: 44px;
    max-height: 44px;
}
QPushButton#startStopBtn:hover {
    background-color: #14A3A8;
}
QPushButton#startStopBtn[running="true"] {
    background-color: #C62828;
}
QPushButton#startStopBtn[running="true"]:hover {
    background-color: #E53935;
}
QFrame#statusFrame {
    background-color: #16213E;
    border: 1px solid #2A2A4A;
    border-radius: 6px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PulseClick")
        self.setFixedSize(360, 540)
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

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        layout.addWidget(self._create_interval_group())
        layout.addWidget(self._create_button_type_group())
        layout.addWidget(self._create_position_group())
        layout.addWidget(self._create_repeat_group())
        layout.addWidget(self._create_random_delay_group())
        layout.addWidget(self._create_hotkey_group())
        layout.addWidget(self._create_profile_group())

        self.start_stop_btn = QPushButton("▶  启动  (F6)")
        self.start_stop_btn.setObjectName("startStopBtn")
        self.start_stop_btn.setProperty("running", False)
        layout.addWidget(self.start_stop_btn)

        layout.addWidget(self._create_status_bar())

    def _create_interval_group(self):
        group = QGroupBox("点击间隔")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 999999)
        self.interval_spin.setValue(100)
        self.interval_spin.setSuffix(" ms")
        self.interval_spin.setFixedWidth(120)
        lay.addWidget(QLabel("间隔:"))
        lay.addWidget(self.interval_spin)
        lay.addStretch()
        return group

    def _create_button_type_group(self):
        group = QGroupBox("按键与类型")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        lay.addWidget(QLabel("按键:"))
        self.btn_left = QRadioButton("左键")
        self.btn_right = QRadioButton("右键")
        self.btn_middle = QRadioButton("中键")
        self.btn_left.setChecked(True)
        self.mouse_btn_group = QButtonGroup(self)
        self.mouse_btn_group.addButton(self.btn_left, 0)
        self.mouse_btn_group.addButton(self.btn_right, 1)
        self.mouse_btn_group.addButton(self.btn_middle, 2)
        lay.addWidget(self.btn_left)
        lay.addWidget(self.btn_right)
        lay.addWidget(self.btn_middle)

        lay.addWidget(self._vsep())

        lay.addWidget(QLabel("类型:"))
        self.click_single = QRadioButton("单击")
        self.click_double = QRadioButton("双击")
        self.click_single.setChecked(True)
        self.click_type_group = QButtonGroup(self)
        self.click_type_group.addButton(self.click_single, 0)
        self.click_type_group.addButton(self.click_double, 1)
        lay.addWidget(self.click_single)
        lay.addWidget(self.click_double)
        return group

    def _create_position_group(self):
        group = QGroupBox("点击位置")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        self.pos_follow = QRadioButton("跟随光标")
        self.pos_fixed = QRadioButton("固定位置")
        self.pos_follow.setChecked(True)
        self.pos_btn_group = QButtonGroup(self)
        self.pos_btn_group.addButton(self.pos_follow, 0)
        self.pos_btn_group.addButton(self.pos_fixed, 1)
        lay.addWidget(self.pos_follow)
        lay.addWidget(self.pos_fixed)

        self.x_spin = QSpinBox()
        self.x_spin.setRange(0, 99999)
        self.x_spin.setPrefix("X: ")
        self.x_spin.setFixedWidth(80)
        self.x_spin.setEnabled(False)
        self.y_spin = QSpinBox()
        self.y_spin.setRange(0, 99999)
        self.y_spin.setPrefix("Y: ")
        self.y_spin.setFixedWidth(80)
        self.y_spin.setEnabled(False)
        lay.addWidget(self.x_spin)
        lay.addWidget(self.y_spin)

        self.pick_btn = QPushButton("拾取")
        self.pick_btn.setFixedWidth(44)
        self.pick_btn.setEnabled(False)
        lay.addWidget(self.pick_btn)
        return group

    def _create_repeat_group(self):
        group = QGroupBox("重复次数")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        self.repeat_infinite = QRadioButton("无限")
        self.repeat_fixed = QRadioButton("固定")
        self.repeat_infinite.setChecked(True)
        self.repeat_btn_group = QButtonGroup(self)
        self.repeat_btn_group.addButton(self.repeat_infinite, 0)
        self.repeat_btn_group.addButton(self.repeat_fixed, 1)
        lay.addWidget(self.repeat_infinite)
        lay.addWidget(self.repeat_fixed)

        self.repeat_count_spin = QSpinBox()
        self.repeat_count_spin.setRange(1, 999999)
        self.repeat_count_spin.setValue(1)
        self.repeat_count_spin.setEnabled(False)
        self.repeat_count_spin.setFixedWidth(100)
        lay.addWidget(QLabel("次数:"))
        lay.addWidget(self.repeat_count_spin)
        lay.addStretch()
        return group

    def _create_random_delay_group(self):
        group = QGroupBox("随机延迟")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        self.random_check = QCheckBox("启用")
        lay.addWidget(self.random_check)

        lay.addWidget(QLabel("最小:"))
        self.random_min_spin = QSpinBox()
        self.random_min_spin.setRange(1, 999999)
        self.random_min_spin.setValue(50)
        self.random_min_spin.setSuffix(" ms")
        self.random_min_spin.setFixedWidth(100)
        self.random_min_spin.setEnabled(False)
        lay.addWidget(self.random_min_spin)

        lay.addWidget(QLabel("最大:"))
        self.random_max_spin = QSpinBox()
        self.random_max_spin.setRange(1, 999999)
        self.random_max_spin.setValue(200)
        self.random_max_spin.setSuffix(" ms")
        self.random_max_spin.setFixedWidth(100)
        self.random_max_spin.setEnabled(False)
        lay.addWidget(self.random_max_spin)
        return group

    def _create_hotkey_group(self):
        group = QGroupBox("热键")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        self.hotkey_label = QLabel("F6")
        self.hotkey_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #4FC3F7;")
        lay.addWidget(QLabel("当前热键:"))
        lay.addWidget(self.hotkey_label)
        lay.addStretch()

        self.hotkey_record_btn = QPushButton("修改热键")
        self.hotkey_record_btn.setFixedWidth(72)
        lay.addWidget(self.hotkey_record_btn)
        return group

    def _create_profile_group(self):
        group = QGroupBox("配置档案")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(8, 16, 8, 6)

        self.profile_combo = QComboBox()
        self.profile_combo.setFixedWidth(120)
        self.profile_combo.addItem("（默认）")
        lay.addWidget(self.profile_combo)

        self.profile_save_btn = QPushButton("保存")
        self.profile_save_btn.setFixedWidth(44)
        lay.addWidget(self.profile_save_btn)

        self.profile_load_btn = QPushButton("加载")
        self.profile_load_btn.setFixedWidth(44)
        lay.addWidget(self.profile_load_btn)

        self.profile_del_btn = QPushButton("删除")
        self.profile_del_btn.setFixedWidth(44)
        lay.addWidget(self.profile_del_btn)
        return group

    def _create_status_bar(self):
        frame = QFrame()
        frame.setObjectName("statusFrame")
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(10, 4, 10, 4)

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #666; font-size: 14px;")
        self.status_dot.setFixedWidth(16)
        lay.addWidget(self.status_dot)

        self.status_text = QLabel("已停止")
        self.status_text.setStyleSheet("font-size: 11px;")
        lay.addWidget(self.status_text)

        lay.addStretch()

        self.click_count_label = QLabel("点击: 0")
        self.click_count_label.setStyleSheet("font-size: 11px; color: #888;")
        lay.addWidget(self.click_count_label)

        self.cps_label = QLabel("CPS: 0.0")
        self.cps_label.setStyleSheet("font-size: 11px; color: #888;")
        lay.addWidget(self.cps_label)
        return frame

    def _vsep(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #2A2A4A;")
        sep.setFixedWidth(12)
        return sep

    def _init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip("PulseClick")

        menu = QMenu()
        menu.setStyleSheet(DARK_STYLE)

        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self._show_window)
        menu.addAction(show_action)

        self.tray_toggle_action = QAction("启动", self)
        self.tray_toggle_action.triggered.connect(self._toggle_from_tray)
        menu.addAction(self.tray_toggle_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self._quit_app)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._tray_activated)
        self.tray_icon.show()

    def _connect_signals(self):
        self.start_stop_btn.clicked.connect(self._on_start_stop)

        self.interval_spin.valueChanged.connect(self._sync_engine)
        self.mouse_btn_group.idToggled.connect(lambda: self._sync_engine())
        self.click_type_group.idToggled.connect(lambda: self._sync_engine())
        self.pos_btn_group.idToggled.connect(self._on_position_mode_changed)
        self.x_spin.valueChanged.connect(self._sync_engine)
        self.y_spin.valueChanged.connect(self._sync_engine)
        self.repeat_btn_group.idToggled.connect(self._on_repeat_mode_changed)
        self.repeat_count_spin.valueChanged.connect(self._sync_engine)
        self.random_check.toggled.connect(self._on_random_check_changed)
        self.random_min_spin.valueChanged.connect(self._sync_engine)
        self.random_max_spin.valueChanged.connect(self._sync_engine)

        self.pick_btn.clicked.connect(self._on_pick_coordinate)
        self.hotkey_record_btn.clicked.connect(self._on_record_hotkey)

        self.profile_save_btn.clicked.connect(self._on_save_profile)
        self.profile_load_btn.clicked.connect(self._on_load_profile)
        self.profile_del_btn.clicked.connect(self._on_delete_profile)

        self.engine.state_changed.connect(self._on_engine_state_changed)
        self.engine.click_count_updated.connect(self._on_click_count_updated)
        self.engine.cps_updated.connect(self._on_cps_updated)
        self.engine.finished.connect(self._on_engine_finished)

        self.hotkey_mgr.hotkey_pressed.connect(self._on_hotkey_pressed)

        self.picker.coordinate_picked.connect(self._on_coordinate_picked)
        self.picker.picking_cancelled.connect(self._on_picking_cancelled)

        self._auto_save_timer = QTimer(self)
        self._auto_save_timer.setInterval(1000)
        self._auto_save_timer.setSingleShot(True)
        self._auto_save_timer.timeout.connect(self._save_config)

    def _sync_engine(self):
        self.engine.set_interval_ms(self.interval_spin.value())
        btn_map = {0: "left", 1: "right", 2: "middle"}
        self.engine.set_mouse_button(btn_map.get(self.mouse_btn_group.checkedId(), "left"))
        self.engine.set_click_type("single" if self.click_type_group.checkedId() == 0 else "double")
        self.engine.set_position_mode("follow" if self.pos_btn_group.checkedId() == 0 else "fixed")
        self.engine.set_fixed_x(self.x_spin.value())
        self.engine.set_fixed_y(self.y_spin.value())
        self.engine.set_repeat_mode("infinite" if self.repeat_btn_group.checkedId() == 0 else "fixed")
        self.engine.set_repeat_count(self.repeat_count_spin.value())
        self.engine.set_random_delay_enabled(self.random_check.isChecked())
        self.engine.set_random_min_ms(self.random_min_spin.value())
        self.engine.set_random_max_ms(self.random_max_spin.value())
        self._schedule_auto_save()

    def _schedule_auto_save(self):
        if self._auto_save_timer.isActive():
            self._auto_save_timer.stop()
        self._auto_save_timer.start()

    def _on_position_mode_changed(self):
        is_fixed = self.pos_btn_group.checkedId() == 1
        self.x_spin.setEnabled(is_fixed)
        self.y_spin.setEnabled(is_fixed)
        self.pick_btn.setEnabled(is_fixed)
        self._sync_engine()

    def _on_repeat_mode_changed(self):
        is_fixed = self.repeat_btn_group.checkedId() == 1
        self.repeat_count_spin.setEnabled(is_fixed)
        self._sync_engine()

    def _on_random_check_changed(self):
        enabled = self.random_check.isChecked()
        self.random_min_spin.setEnabled(enabled)
        self.random_max_spin.setEnabled(enabled)
        self._sync_engine()

    def _on_start_stop(self):
        self.engine.toggle()

    def _on_hotkey_pressed(self):
        self.engine.toggle()

    def _toggle_from_tray(self):
        self.engine.toggle()

    def _on_engine_state_changed(self, running):
        if running:
            self.start_stop_btn.setText("■  停止  (" + self.hotkey_mgr.get_hotkey() + ")")
            self.start_stop_btn.setProperty("running", True)
            self.status_dot.setStyleSheet("color: #4CAF50; font-size: 14px;")
            self.status_text.setText("运行中")
            self.tray_toggle_action.setText("停止")
        else:
            self.start_stop_btn.setText("▶  启动  (" + self.hotkey_mgr.get_hotkey() + ")")
            self.start_stop_btn.setProperty("running", False)
            self.status_dot.setStyleSheet("color: #666; font-size: 14px;")
            self.status_text.setText("已停止")
            self.tray_toggle_action.setText("启动")
        self.start_stop_btn.style().unpolish(self.start_stop_btn)
        self.start_stop_btn.style().polish(self.start_stop_btn)

    def _on_click_count_updated(self, count):
        self.click_count_label.setText(f"点击: {count}")

    def _on_cps_updated(self, cps):
        self.cps_label.setText(f"CPS: {cps:.1f}")

    def _on_engine_finished(self):
        pass

    def _on_pick_coordinate(self):
        self.picker.start_picking()

    def _on_coordinate_picked(self, x, y):
        self.x_spin.setValue(x)
        self.y_spin.setValue(y)

    def _on_picking_cancelled(self):
        pass

    def _on_record_hotkey(self):
        self.hotkey_record_btn.setText("按下按键...")
        self.hotkey_record_btn.setEnabled(False)
        self.hotkey_mgr.start_recording()
        self._recording_check_timer = QTimer(self)
        self._recording_check_timer.timeout.connect(self._check_recording_done)
        self._recording_check_timer.start(100)

    def _check_recording_done(self):
        if not self.hotkey_mgr.is_recording():
            new_key = self.hotkey_mgr.get_hotkey()
            self.hotkey_label.setText(new_key)
            self.hotkey_record_btn.setText("修改热键")
            self.hotkey_record_btn.setEnabled(True)
            self._recording_check_timer.stop()
            self._update_start_stop_text()
            self._schedule_auto_save()

    def _update_start_stop_text(self):
        running = self.engine.is_running()
        key = self.hotkey_mgr.get_hotkey()
        if running:
            self.start_stop_btn.setText(f"■  停止  ({key})")
        else:
            self.start_stop_btn.setText(f"▶  启动  ({key})")

    def _on_save_profile(self):
        name = self.profile_combo.currentText()
        if name == "（默认）" or not name:
            from PySide6.QtWidgets import QInputDialog
            name, ok = QInputDialog.getText(self, "保存档案", "档案名称:")
            if not ok or not name.strip():
                return
            name = name.strip()
        settings = self._gather_settings()
        self.config_mgr.save_profile(name, settings)
        self._refresh_profiles()
        idx = self.profile_combo.findText(name)
        if idx >= 0:
            self.profile_combo.setCurrentIndex(idx)

    def _on_load_profile(self):
        name = self.profile_combo.currentText()
        if name == "（默认）" or not name:
            return
        try:
            settings = self.config_mgr.load_profile(name)
            self._apply_settings(settings)
        except KeyError:
            pass

    def _on_delete_profile(self):
        name = self.profile_combo.currentText()
        if name == "（默认）" or not name:
            return
        self.config_mgr.delete_profile(name)
        self._refresh_profiles()

    def _refresh_profiles(self):
        current = self.profile_combo.currentText()
        self.profile_combo.clear()
        self.profile_combo.addItem("（默认）")
        for name in self.config_mgr.list_profiles():
            self.profile_combo.addItem(name)
        idx = self.profile_combo.findText(current)
        if idx >= 0:
            self.profile_combo.setCurrentIndex(idx)

    def _gather_settings(self):
        btn_map = {0: "left", 1: "right", 2: "middle"}
        return {
            "interval_ms": self.interval_spin.value(),
            "mouse_button": btn_map.get(self.mouse_btn_group.checkedId(), "left"),
            "click_type": "single" if self.click_type_group.checkedId() == 0 else "double",
            "position_mode": "follow" if self.pos_btn_group.checkedId() == 0 else "fixed",
            "fixed_x": self.x_spin.value(),
            "fixed_y": self.y_spin.value(),
            "repeat_mode": "infinite" if self.repeat_btn_group.checkedId() == 0 else "fixed",
            "repeat_count": self.repeat_count_spin.value(),
            "random_delay_enabled": self.random_check.isChecked(),
            "random_min_ms": self.random_min_spin.value(),
            "random_max_ms": self.random_max_spin.value(),
            "hotkey": self.hotkey_mgr.get_hotkey(),
        }

    def _apply_settings(self, settings):
        self.interval_spin.setValue(settings.get("interval_ms", 100))
        btn_rmap = {"left": 0, "right": 1, "middle": 2}
        btn_id = btn_rmap.get(settings.get("mouse_button", "left"), 0)
        btn = self.mouse_btn_group.button(btn_id)
        if btn:
            btn.setChecked(True)
        ct = settings.get("click_type", "single")
        self.click_single.setChecked(ct == "single")
        self.click_double.setChecked(ct == "double")
        pm = settings.get("position_mode", "follow")
        self.pos_follow.setChecked(pm == "follow")
        self.pos_fixed.setChecked(pm == "fixed")
        self.x_spin.setValue(settings.get("fixed_x", 0))
        self.y_spin.setValue(settings.get("fixed_y", 0))
        rm = settings.get("repeat_mode", "infinite")
        self.repeat_infinite.setChecked(rm == "infinite")
        self.repeat_fixed.setChecked(rm == "fixed")
        self.repeat_count_spin.setValue(settings.get("repeat_count", 1))
        self.random_check.setChecked(settings.get("random_delay_enabled", False))
        self.random_min_spin.setValue(settings.get("random_min_ms", 50))
        self.random_max_spin.setValue(settings.get("random_max_ms", 200))
        hk = settings.get("hotkey", "F6")
        self.hotkey_mgr.set_hotkey(hk)
        self.hotkey_label.setText(hk)
        self._on_position_mode_changed()
        self._on_repeat_mode_changed()
        self._on_random_check_changed()
        self._sync_engine()
        self._update_start_stop_text()

    def _save_config(self):
        settings = self._gather_settings()
        self.config_mgr.save_config(settings)

    def _load_config(self):
        settings = self.config_mgr.load_config()
        self._apply_settings(settings)
        self._refresh_profiles()

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self._show_window()

    def _show_window(self):
        self.showNormal()
        self.activateWindow()

    def _quit_app(self):
        self.engine.stop()
        self.hotkey_mgr.stop_listening()
        self.tray_icon.hide()
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
