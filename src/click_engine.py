import threading
import time
import random
from PySide6.QtCore import QObject, Signal
from pynput.mouse import Controller, Button


class ClickEngine(QObject):
    state_changed = Signal(bool)
    click_count_updated = Signal(int)
    cps_updated = Signal(float)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._interval_ms = 100
        self._mouse_button = "left"
        self._click_type = "single"
        self._position_mode = "follow"
        self._fixed_x = 0
        self._fixed_y = 0
        self._repeat_mode = "infinite"
        self._repeat_count = 1
        self._random_delay_enabled = False
        self._random_min_ms = 50
        self._random_max_ms = 200
        self._running = False
        self._stop_event = threading.Event()
        self._click_count = 0
        self._click_timestamps = []
        self._controller = Controller()
        self._cps_timer = None

    def interval_ms(self):
        return self._interval_ms

    def set_interval_ms(self, value):
        self._interval_ms = value

    def mouse_button(self):
        return self._mouse_button

    def set_mouse_button(self, value):
        self._mouse_button = value

    def click_type(self):
        return self._click_type

    def set_click_type(self, value):
        self._click_type = value

    def position_mode(self):
        return self._position_mode

    def set_position_mode(self, value):
        self._position_mode = value

    def fixed_x(self):
        return self._fixed_x

    def set_fixed_x(self, value):
        self._fixed_x = value

    def fixed_y(self):
        return self._fixed_y

    def set_fixed_y(self, value):
        self._fixed_y = value

    def repeat_mode(self):
        return self._repeat_mode

    def set_repeat_mode(self, value):
        self._repeat_mode = value

    def repeat_count(self):
        return self._repeat_count

    def set_repeat_count(self, value):
        self._repeat_count = value

    def random_delay_enabled(self):
        return self._random_delay_enabled

    def set_random_delay_enabled(self, value):
        self._random_delay_enabled = value

    def random_min_ms(self):
        return self._random_min_ms

    def set_random_min_ms(self, value):
        self._random_min_ms = value

    def random_max_ms(self):
        return self._random_max_ms

    def set_random_max_ms(self, value):
        self._random_max_ms = value

    def is_running(self):
        return self._running

    def start(self):
        if self._running:
            return
        self._running = True
        self._click_count = 0
        self._click_timestamps = []
        self._stop_event.clear()
        self.state_changed.emit(True)
        self._start_cps_timer()
        thread = threading.Thread(target=self._click_loop, daemon=True)
        thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        self._stop_cps_timer()
        self.state_changed.emit(False)

    def toggle(self):
        if self._running:
            self.stop()
        else:
            self.start()

    def _start_cps_timer(self):
        self._stop_cps_timer()
        self._cps_timer = threading.Timer(0.5, self._emit_cps)
        self._cps_timer.daemon = True
        self._cps_timer.start()

    def _stop_cps_timer(self):
        if self._cps_timer is not None:
            self._cps_timer.cancel()
            self._cps_timer = None

    def _emit_cps(self):
        if self._running:
            cps = self._calculate_cps()
            self.cps_updated.emit(cps)
            self._cps_timer = threading.Timer(0.5, self._emit_cps)
            self._cps_timer.daemon = True
            self._cps_timer.start()

    def _calculate_cps(self):
        now = time.monotonic()
        window = 2.0
        cutoff = now - window
        self._click_timestamps = [t for t in self._click_timestamps if t > cutoff]
        if not self._click_timestamps:
            return 0.0
        span = now - self._click_timestamps[0]
        if span <= 0:
            return 0.0
        return len(self._click_timestamps) / span

    def _get_button(self):
        if self._mouse_button == "right":
            return Button.right
        elif self._mouse_button == "middle":
            return Button.middle
        return Button.left

    def _perform_click(self):
        button = self._get_button()
        if self._position_mode == "fixed":
            original_pos = self._controller.position
            self._controller.position = (self._fixed_x, self._fixed_y)
            self._do_click(button)
            self._controller.position = original_pos
        else:
            self._do_click(button)

    def _do_click(self, button):
        if self._click_type == "double":
            self._controller.click(button)
            time.sleep(0.01)
            self._controller.click(button)
        else:
            self._controller.click(button)

    def _click_loop(self):
        while not self._stop_event.is_set():
            self._perform_click()
            self._click_count += 1
            self._click_timestamps.append(time.monotonic())
            self.click_count_updated.emit(self._click_count)
            if self._repeat_mode == "fixed" and self._click_count >= self._repeat_count:
                self._running = False
                self._stop_event.set()
                self._stop_cps_timer()
                self.state_changed.emit(False)
                self.finished.emit()
                return
            if self._random_delay_enabled:
                delay = random.uniform(self._random_min_ms, self._random_max_ms) / 1000.0
            else:
                delay = self._interval_ms / 1000.0
            self._stop_event.wait(delay)
