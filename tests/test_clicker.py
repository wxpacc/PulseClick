import time

from src.core.clicker import ClickEngine
from src.core.config import ClickConfig


class FakeMouse:
    def __init__(self):
        self.position = (10, 20)
        self.clicks = []

    def click(self, button):
        self.clicks.append((button, self.position))


def resolve_button(name):
    return name


def wait_until(predicate, timeout=1.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def test_engine_stops_after_repeat_count():
    mouse = FakeMouse()
    engine = ClickEngine(mouse, resolve_button)
    engine.configure(ClickConfig(interval_ms=1, repeat_mode="count", repeat_count=3))

    engine.start()

    assert wait_until(lambda: not engine.is_running)
    assert len(mouse.clicks) == 3


def test_fixed_position_restores_original_position():
    mouse = FakeMouse()
    engine = ClickEngine(mouse, resolve_button)
    engine.configure(
        ClickConfig(
            interval_ms=1,
            repeat_mode="count",
            repeat_count=1,
            position_mode="fixed",
            fixed_x=100,
            fixed_y=200,
        )
    )

    engine.start()

    assert wait_until(lambda: not engine.is_running)
    assert mouse.clicks == [("left", (100, 200))]
    assert mouse.position == (10, 20)


def test_double_click_counts_as_one_repeat_with_two_mouse_clicks():
    mouse = FakeMouse()
    engine = ClickEngine(mouse, resolve_button)
    engine.configure(ClickConfig(interval_ms=1, repeat_mode="count", repeat_count=1, click_type="double"))

    engine.start()

    assert wait_until(lambda: not engine.is_running)
    assert len(mouse.clicks) == 2
    assert engine.get_stats().click_count == 1


def test_stop_is_idempotent():
    mouse = FakeMouse()
    engine = ClickEngine(mouse, resolve_button)
    engine.configure(ClickConfig(interval_ms=1000))

    engine.start()
    engine.stop()
    engine.stop()

    assert not engine.is_running

