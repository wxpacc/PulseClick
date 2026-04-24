from __future__ import annotations

from dataclasses import asdict, dataclass, fields


VALID_BUTTONS = {"left", "right", "middle"}
VALID_CLICK_TYPES = {"single", "double", "triple"}
VALID_REPEAT_MODES = {"infinite", "count"}
VALID_POSITION_MODES = {"follow", "fixed"}


@dataclass(slots=True)
class ClickConfig:
    button: str = "left"
    click_type: str = "single"
    interval_ms: int = 100
    repeat_mode: str = "infinite"
    repeat_count: int = 1000
    position_mode: str = "follow"
    fixed_x: int = 0
    fixed_y: int = 0
    random_enabled: bool = False
    random_min: int = 80
    random_max: int = 120
    hotkey: str = "F6"
    profile_name: str = "默认"

    def validate(self) -> None:
        if self.button not in VALID_BUTTONS:
            raise ValueError("button must be left, right, or middle")
        if self.click_type not in VALID_CLICK_TYPES:
            raise ValueError("click_type must be single, double, or triple")
        if not 1 <= int(self.interval_ms) <= 3_600_000:
            raise ValueError("interval_ms must be between 1 and 3600000")
        if self.repeat_mode not in VALID_REPEAT_MODES:
            raise ValueError("repeat_mode must be infinite or count")
        if not 1 <= int(self.repeat_count) <= 999_999:
            raise ValueError("repeat_count must be between 1 and 999999")
        if self.position_mode not in VALID_POSITION_MODES:
            raise ValueError("position_mode must be follow or fixed")
        if not -100_000 <= int(self.fixed_x) <= 100_000:
            raise ValueError("fixed_x is outside the supported range")
        if not -100_000 <= int(self.fixed_y) <= 100_000:
            raise ValueError("fixed_y is outside the supported range")
        if not 1 <= int(self.random_min) <= 3_600_000:
            raise ValueError("random_min must be between 1 and 3600000")
        if not 1 <= int(self.random_max) <= 3_600_000:
            raise ValueError("random_max must be between 1 and 3600000")
        if int(self.random_min) > int(self.random_max):
            raise ValueError("random_min cannot be greater than random_max")
        if not self.hotkey.strip():
            raise ValueError("hotkey cannot be empty")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, object] | None) -> "ClickConfig":
        values = asdict(cls())
        if data:
            allowed = {field.name for field in fields(cls)}
            values.update({key: value for key, value in data.items() if key in allowed})
        config = cls(**values)
        config.validate()
        return config


@dataclass(slots=True)
class RuntimeStats:
    running: bool = False
    click_count: int = 0
    cps: float = 0.0
    elapsed_seconds: float = 0.0

