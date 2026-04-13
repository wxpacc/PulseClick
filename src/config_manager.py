import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal


class ConfigManager(QObject):
    config_saved = Signal()
    config_loaded = Signal()

    _DEFAULTS = {
        "interval_ms": 100,
        "mouse_button": "left",
        "click_type": "single",
        "position_mode": "follow",
        "fixed_x": 0,
        "fixed_y": 0,
        "repeat_mode": "infinite",
        "repeat_count": 1,
        "random_delay_enabled": False,
        "random_min_ms": 50,
        "random_max_ms": 200,
        "hotkey": "f6",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config_dir = Path.home() / "Documents" / "PulseClick"
        self._profiles_dir = self._config_dir / "profiles"
        self._config_path = self._config_dir / "config.json"

    def _ensure_dirs(self):
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._profiles_dir.mkdir(parents=True, exist_ok=True)

    def get_defaults(self) -> dict:
        return dict(self._DEFAULTS)

    def save_config(self, settings: dict):
        self._ensure_dirs()
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        self.config_saved.emit()

    def load_config(self) -> dict:
        defaults = self.get_defaults()
        if not self._config_path.exists():
            return defaults
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = defaults
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            return defaults

    def save_profile(self, name: str, settings: dict):
        self._ensure_dirs()
        profile_path = self._profiles_dir / f"{name}.json"
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def load_profile(self, name: str) -> dict:
        profile_path = self._profiles_dir / f"{name}.json"
        if not profile_path.exists():
            raise KeyError(f"Profile '{name}' not found")
        defaults = self.get_defaults()
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = defaults
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            return defaults

    def delete_profile(self, name: str):
        profile_path = self._profiles_dir / f"{name}.json"
        if profile_path.exists():
            profile_path.unlink()

    def list_profiles(self) -> list[str]:
        if not self._profiles_dir.exists():
            return []
        return [p.stem for p in self._profiles_dir.glob("*.json")]
