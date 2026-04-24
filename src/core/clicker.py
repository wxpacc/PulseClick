from __future__ import annotations

import random
import threading
import time
from collections.abc import Callable
from typing import Protocol

from src.core.config import ClickConfig, RuntimeStats


class MouseController(Protocol):
    @property
    def position(self) -> tuple[int, int]: ...

    @position.setter
    def position(self, value: tuple[int, int]) -> None: ...

    def click(self, button: object) -> None: ...


StatsCallback = Callable[[RuntimeStats], None]


class ClickEngine:
    """Threaded mouse click engine."""

    def __init__(
        self,
        controller: MouseController | None = None,
        button_resolver: Callable[[str], object] | None = None,
    ) -> None:
        self._controller = controller
        self._button_resolver = button_resolver
        self._config = ClickConfig()
        self._running = False
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        self._click_count = 0
        self._start_time: float | None = None
        self._click_timestamps: list[float] = []
        self._stats_callback: StatsCallback | None = None

    def set_stats_callback(self, callback: StatsCallback | None) -> None:
        self._stats_callback = callback

    def configure(self, config: ClickConfig) -> None:
        config.validate()
        with self._lock:
            if self._running:
                raise RuntimeError("cannot reconfigure while running")
            self._config = config

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._config.validate()
            self._running = True
            self._click_count = 0
            self._click_timestamps = []
            self._start_time = time.monotonic()
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._click_loop, name="PulseClickEngine", daemon=True)
            self._thread.start()
        self._emit_stats()

    def stop(self) -> None:
        thread: threading.Thread | None
        with self._lock:
            if not self._running and self._thread is None:
                return
            self._running = False
            self._stop_event.set()
            thread = self._thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=1.0)
        with self._lock:
            if self._thread is thread:
                self._thread = None
        self._emit_stats()

    def toggle(self) -> None:
        if self.is_running:
            self.stop()
        else:
            self.start()

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self._running

    def get_stats(self) -> RuntimeStats:
        with self._lock:
            return RuntimeStats(
                running=self._running,
                click_count=self._click_count,
                cps=self._calculate_cps_locked(),
                elapsed_seconds=self._elapsed_locked(),
            )

    def _click_loop(self) -> None:
        while not self._stop_event.is_set():
            with self._lock:
                config = self._config
            self._perform_click(config)
            now = time.monotonic()
            with self._lock:
                self._click_count += 1
                self._click_timestamps.append(now)
                reached_limit = config.repeat_mode == "count" and self._click_count >= config.repeat_count
            self._emit_stats()
            if reached_limit:
                self._finish_from_worker()
                return
            delay_ms = random.randint(config.random_min, config.random_max) if config.random_enabled else config.interval_ms
            self._stop_event.wait(delay_ms / 1000.0)

    def _finish_from_worker(self) -> None:
        with self._lock:
            self._running = False
            self._thread = None
            self._stop_event.set()
        self._emit_stats()

    def _perform_click(self, config: ClickConfig) -> None:
        controller = self._get_controller()
        button = self._resolve_button(config.button)
        original_pos: tuple[int, int] | None = None
        if config.position_mode == "fixed":
            original_pos = controller.position
            controller.position = (config.fixed_x, config.fixed_y)
        try:
            for _ in range(self._click_multiplier(config.click_type)):
                controller.click(button)
                if config.click_type != "single":
                    time.sleep(0.01)
        finally:
            if original_pos is not None:
                controller.position = original_pos

    def _get_controller(self) -> MouseController:
        if self._controller is None:
            from src.platform.windows.input import WindowsMouseController

            self._controller = WindowsMouseController()
        return self._controller

    def _resolve_button(self, button: str) -> object:
        if self._button_resolver:
            return self._button_resolver(button)
        return button

    @staticmethod
    def _click_multiplier(click_type: str) -> int:
        return {"single": 1, "double": 2, "triple": 3}[click_type]

    def _emit_stats(self) -> None:
        callback = self._stats_callback
        if callback:
            callback(self.get_stats())

    def _elapsed_locked(self) -> float:
        if self._start_time is None:
            return 0.0
        return max(0.0, time.monotonic() - self._start_time)

    def _calculate_cps_locked(self) -> float:
        now = time.monotonic()
        cutoff = now - 2.0
        self._click_timestamps = [timestamp for timestamp in self._click_timestamps if timestamp >= cutoff]
        if len(self._click_timestamps) < 2:
            return float(len(self._click_timestamps))
        span = max(0.001, self._click_timestamps[-1] - self._click_timestamps[0])
        return len(self._click_timestamps) / span
