from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.core.clicker import ClickEngine
from src.core.config import ClickConfig, RuntimeStats
from src.core.hotkey import HotkeyManager, display_hotkey, parse_hotkey
from src.core.recorder import CoordinatePicker
from src.ui.dialogs import HotkeyDialog, ask_profile_name, show_error
from src.ui.styles import DARK_QSS
from src.utils.config import ConfigManager
from src.utils.tray import TrayController


class MainWindow(QMainWindow):
    stats_received = Signal(object)
    hotkey_pressed = Signal()

    def __init__(self, icon_path: Path) -> None:
        super().__init__()
        self.setWindowTitle("PulseClick")
        self.setFixedSize(380, 600)
        self.setStyleSheet(DARK_QSS)

        self._engine = ClickEngine()
        self._config_manager = ConfigManager()
        self._hotkeys = HotkeyManager()
        self._picker = CoordinatePicker()
        self._tray = TrayController(icon_path, self._show_window, self.start_clicking, self.stop_clicking, self._quit_from_tray)
        self._exiting = False
        self._current_config = self._config_manager.load()

        self._build_ui()
        self._connect_signals()
        self._apply_config(self._current_config)
        self._refresh_profiles()
        self._register_hotkey()
        self._tray.show()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        title = QLabel("PulseClick")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #ffffff;")
        layout.addWidget(title)
        layout.addWidget(self._create_core_group())
        layout.addWidget(self._create_position_group())
        layout.addWidget(self._create_advanced_group())
        layout.addWidget(self._create_hotkey_group())
        layout.addWidget(self._create_status_panel())

        self.start_button = QPushButton("▶ 启动")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setProperty("running", False)
        layout.addWidget(self.start_button)

    def _create_core_group(self) -> QGroupBox:
        group = QGroupBox("核心设置")
        layout = QVBoxLayout(group)

        row = QHBoxLayout()
        row.addWidget(QLabel("鼠标按钮"))
        self.left_radio = QRadioButton("左键")
        self.right_radio = QRadioButton("右键")
        self.middle_radio = QRadioButton("中键")
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.left_radio, 0)
        self.button_group.addButton(self.right_radio, 1)
        self.button_group.addButton(self.middle_radio, 2)
        row.addWidget(self.left_radio)
        row.addWidget(self.right_radio)
        row.addWidget(self.middle_radio)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("点击类型"))
        self.single_radio = QRadioButton("单击")
        self.double_radio = QRadioButton("双击")
        self.triple_radio = QRadioButton("三击")
        self.click_type_group = QButtonGroup(self)
        self.click_type_group.addButton(self.single_radio, 0)
        self.click_type_group.addButton(self.double_radio, 1)
        self.click_type_group.addButton(self.triple_radio, 2)
        row.addWidget(self.single_radio)
        row.addWidget(self.double_radio)
        row.addWidget(self.triple_radio)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("点击间隔"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 3_600_000)
        self.interval_spin.setSuffix(" ms")
        row.addWidget(self.interval_spin)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("重复模式"))
        self.infinite_radio = QRadioButton("无限")
        self.count_radio = QRadioButton("次数")
        self.repeat_group = QButtonGroup(self)
        self.repeat_group.addButton(self.infinite_radio, 0)
        self.repeat_group.addButton(self.count_radio, 1)
        self.repeat_count_spin = QSpinBox()
        self.repeat_count_spin.setRange(1, 999_999)
        row.addWidget(self.infinite_radio)
        row.addWidget(self.count_radio)
        row.addWidget(self.repeat_count_spin)
        layout.addLayout(row)
        return group

    def _create_position_group(self) -> QGroupBox:
        group = QGroupBox("位置设置")
        layout = QVBoxLayout(group)
        row = QHBoxLayout()
        self.follow_radio = QRadioButton("跟随光标")
        self.fixed_radio = QRadioButton("固定坐标")
        self.position_group = QButtonGroup(self)
        self.position_group.addButton(self.follow_radio, 0)
        self.position_group.addButton(self.fixed_radio, 1)
        row.addWidget(self.follow_radio)
        row.addWidget(self.fixed_radio)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("X"))
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-100_000, 100_000)
        row.addWidget(self.x_spin)
        row.addWidget(QLabel("Y"))
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-100_000, 100_000)
        row.addWidget(self.y_spin)
        self.pick_button = QPushButton("拾取坐标")
        row.addWidget(self.pick_button)
        layout.addLayout(row)
        return group

    def _create_advanced_group(self) -> QGroupBox:
        group = QGroupBox("高级设置")
        layout = QVBoxLayout(group)
        self.random_check = QCheckBox("启用随机延迟")
        layout.addWidget(self.random_check)

        row = QHBoxLayout()
        row.addWidget(QLabel("延迟范围"))
        self.random_min_spin = QSpinBox()
        self.random_min_spin.setRange(1, 3_600_000)
        self.random_min_spin.setSuffix(" ms")
        self.random_max_spin = QSpinBox()
        self.random_max_spin.setRange(1, 3_600_000)
        self.random_max_spin.setSuffix(" ms")
        row.addWidget(self.random_min_spin)
        row.addWidget(QLabel("-"))
        row.addWidget(self.random_max_spin)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("配置档案"))
        self.profile_combo = QComboBox()
        row.addWidget(self.profile_combo)
        self.save_profile_button = QPushButton("保存")
        self.load_profile_button = QPushButton("加载")
        self.delete_profile_button = QPushButton("删除")
        row.addWidget(self.save_profile_button)
        row.addWidget(self.load_profile_button)
        row.addWidget(self.delete_profile_button)
        layout.addLayout(row)
        return group

    def _create_hotkey_group(self) -> QGroupBox:
        group = QGroupBox("热键设置")
        layout = QHBoxLayout(group)
        layout.addWidget(QLabel("启停热键"))
        self.hotkey_label = QLabel("F6")
        self.hotkey_label.setStyleSheet("font-weight: 700; color: #e94560;")
        layout.addWidget(self.hotkey_label)
        self.edit_hotkey_button = QPushButton("修改")
        layout.addWidget(self.edit_hotkey_button)
        layout.addStretch()
        return group

    def _create_status_panel(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("statusPanel")
        layout = QHBoxLayout(frame)
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setStyleSheet("color: #8c95aa;")
        self.status_label = QLabel("空闲")
        self.cps_label = QLabel("CPS: 0.0")
        self.count_label = QLabel("点击: 0")
        self.elapsed_label = QLabel("00:00:00")
        layout.addWidget(self.status_dot)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.cps_label)
        layout.addWidget(self.count_label)
        layout.addWidget(self.elapsed_label)
        return frame

    def _connect_signals(self) -> None:
        self.start_button.clicked.connect(self.toggle_clicking)
        self.repeat_group.idToggled.connect(lambda *_: self._update_enabled_states())
        self.position_group.idToggled.connect(lambda *_: self._update_enabled_states())
        self.random_check.toggled.connect(lambda *_: self._update_enabled_states())
        self.pick_button.clicked.connect(self._picker.start)
        self._picker.coordinate_picked.connect(self._set_picked_coordinate)
        self.save_profile_button.clicked.connect(self._save_profile)
        self.load_profile_button.clicked.connect(self._load_profile)
        self.delete_profile_button.clicked.connect(self._delete_profile)
        self.edit_hotkey_button.clicked.connect(self._edit_hotkey)
        self.stats_received.connect(self._update_stats)
        self.hotkey_pressed.connect(self.toggle_clicking)
        self._engine.set_stats_callback(self.stats_received.emit)

        self._stats_timer = QTimer(self)
        self._stats_timer.setInterval(500)
        self._stats_timer.timeout.connect(lambda: self._update_stats(self._engine.get_stats()))
        self._stats_timer.start()

    def toggle_clicking(self) -> None:
        if self._engine.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self) -> None:
        try:
            config = self._read_config()
            self._config_manager.save(config)
            self._engine.configure(config)
            self._engine.start()
        except Exception as exc:
            show_error(self, str(exc))

    def stop_clicking(self) -> None:
        self._engine.stop()

    def _read_config(self) -> ClickConfig:
        config = ClickConfig(
            button={0: "left", 1: "right", 2: "middle"}[self.button_group.checkedId()],
            click_type={0: "single", 1: "double", 2: "triple"}[self.click_type_group.checkedId()],
            interval_ms=self.interval_spin.value(),
            repeat_mode="count" if self.repeat_group.checkedId() == 1 else "infinite",
            repeat_count=self.repeat_count_spin.value(),
            position_mode="fixed" if self.position_group.checkedId() == 1 else "follow",
            fixed_x=self.x_spin.value(),
            fixed_y=self.y_spin.value(),
            random_enabled=self.random_check.isChecked(),
            random_min=self.random_min_spin.value(),
            random_max=self.random_max_spin.value(),
            hotkey=self._current_config.hotkey,
            profile_name=self.profile_combo.currentText() or "默认",
        )
        config.validate()
        self._current_config = config
        return config

    def _apply_config(self, config: ClickConfig) -> None:
        {"left": self.left_radio, "right": self.right_radio, "middle": self.middle_radio}[config.button].setChecked(True)
        {"single": self.single_radio, "double": self.double_radio, "triple": self.triple_radio}[config.click_type].setChecked(True)
        self.interval_spin.setValue(config.interval_ms)
        (self.count_radio if config.repeat_mode == "count" else self.infinite_radio).setChecked(True)
        self.repeat_count_spin.setValue(config.repeat_count)
        (self.fixed_radio if config.position_mode == "fixed" else self.follow_radio).setChecked(True)
        self.x_spin.setValue(config.fixed_x)
        self.y_spin.setValue(config.fixed_y)
        self.random_check.setChecked(config.random_enabled)
        self.random_min_spin.setValue(config.random_min)
        self.random_max_spin.setValue(config.random_max)
        self.hotkey_label.setText(display_hotkey(config.hotkey))
        self._current_config = config
        self._update_enabled_states()

    def _update_enabled_states(self) -> None:
        fixed = self.position_group.checkedId() == 1
        self.x_spin.setEnabled(fixed)
        self.y_spin.setEnabled(fixed)
        self.pick_button.setEnabled(fixed)
        self.repeat_count_spin.setEnabled(self.repeat_group.checkedId() == 1)
        random_enabled = self.random_check.isChecked()
        self.random_min_spin.setEnabled(random_enabled)
        self.random_max_spin.setEnabled(random_enabled)

    def _update_stats(self, stats: RuntimeStats) -> None:
        self.status_dot.setStyleSheet("color: #4ade80;" if stats.running else "color: #8c95aa;")
        self.status_label.setText("运行中" if stats.running else "空闲")
        self.cps_label.setText(f"CPS: {stats.cps:.1f}")
        self.count_label.setText(f"点击: {stats.click_count}")
        self.elapsed_label.setText(self._format_seconds(stats.elapsed_seconds))
        self.start_button.setText("■ 停止" if stats.running else "▶ 启动")
        self.start_button.setProperty("running", stats.running)
        self.start_button.style().unpolish(self.start_button)
        self.start_button.style().polish(self.start_button)
        self._tray.set_running(stats.running)

    def _set_picked_coordinate(self, x: int, y: int) -> None:
        self.x_spin.setValue(x)
        self.y_spin.setValue(y)

    def _save_profile(self) -> None:
        name = ask_profile_name(self)
        if not name:
            return
        try:
            self._config_manager.save_profile(name, self._read_config())
            self._refresh_profiles(name)
        except ValueError as exc:
            show_error(self, str(exc))

    def _load_profile(self) -> None:
        name = self.profile_combo.currentText()
        if not name:
            return
        try:
            config = self._config_manager.load_profile(name)
            config.profile_name = name
            self._apply_config(config)
        except Exception as exc:
            show_error(self, str(exc))

    def _delete_profile(self) -> None:
        name = self.profile_combo.currentText()
        if not name:
            return
        try:
            self._config_manager.delete_profile(name)
            self._refresh_profiles()
        except ValueError as exc:
            show_error(self, str(exc))

    def _refresh_profiles(self, selected: str | None = None) -> None:
        self.profile_combo.clear()
        profiles = self._config_manager.list_profiles()
        self.profile_combo.addItems(profiles)
        if selected and selected in profiles:
            self.profile_combo.setCurrentText(selected)

    def _edit_hotkey(self) -> None:
        dialog = HotkeyDialog(self._current_config.hotkey, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            hotkey = dialog.hotkey()
            parse_hotkey(hotkey)
            self._current_config.hotkey = hotkey
            self.hotkey_label.setText(display_hotkey(hotkey))
            self._config_manager.save(self._read_config())
            self._register_hotkey()
        except ValueError as exc:
            show_error(self, str(exc))

    def _register_hotkey(self) -> None:
        try:
            self._hotkeys.register(self._current_config.hotkey, self.hotkey_pressed.emit)
            self._hotkeys.start()
        except Exception as exc:
            show_error(self, f"热键注册失败：{exc}")

    def _show_window(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _quit_from_tray(self) -> None:
        self._exiting = True
        self.close()

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._exiting or not self._tray:
            self._engine.stop()
            self._hotkeys.stop()
            self._tray.hide()
            event.accept()
            return
        event.ignore()
        self.hide()

    @staticmethod
    def _format_seconds(value: float) -> str:
        total = int(value)
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
