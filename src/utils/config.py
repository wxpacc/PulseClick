from __future__ import annotations

import json
import re
from pathlib import Path

from src.core.config import ClickConfig
from src.platform.windows.paths import config_dir as default_config_dir


PROFILE_SAFE_NAME = re.compile(r"^[\w\u4e00-\u9fff .-]{1,40}$")


class ConfigManager:
    CONFIG_DIR = default_config_dir()
    CONFIG_FILE = CONFIG_DIR / "config.json"
    PROFILES_DIR = CONFIG_DIR / "profiles"

    def __init__(self, config_dir: Path | None = None) -> None:
        self.CONFIG_DIR = default_config_dir()
        self.CONFIG_FILE = self.CONFIG_DIR / "config.json"
        self.PROFILES_DIR = self.CONFIG_DIR / "profiles"
        if config_dir is not None:
            self.CONFIG_DIR = config_dir
            self.CONFIG_FILE = config_dir / "config.json"
            self.PROFILES_DIR = config_dir / "profiles"

    def load(self) -> ClickConfig:
        if not self.CONFIG_FILE.exists():
            return ClickConfig()
        try:
            with self.CONFIG_FILE.open("r", encoding="utf-8") as file:
                return ClickConfig.from_dict(json.load(file))
        except (OSError, json.JSONDecodeError, ValueError):
            return ClickConfig()

    def save(self, config: ClickConfig) -> None:
        self._ensure_dirs()
        config.validate()
        with self.CONFIG_FILE.open("w", encoding="utf-8") as file:
            json.dump(config.to_dict(), file, ensure_ascii=False, indent=2)

    def get_default(self) -> ClickConfig:
        return ClickConfig()

    def save_profile(self, name: str, config: ClickConfig) -> None:
        safe_name = self._validate_profile_name(name)
        self._ensure_dirs()
        config.validate()
        path = self.PROFILES_DIR / f"{safe_name}.json"
        with path.open("w", encoding="utf-8") as file:
            json.dump(config.to_dict(), file, ensure_ascii=False, indent=2)

    def load_profile(self, name: str) -> ClickConfig:
        safe_name = self._validate_profile_name(name)
        path = self.PROFILES_DIR / f"{safe_name}.json"
        if not path.exists():
            raise FileNotFoundError(f"profile not found: {safe_name}")
        with path.open("r", encoding="utf-8") as file:
            return ClickConfig.from_dict(json.load(file))

    def list_profiles(self) -> list[str]:
        if not self.PROFILES_DIR.exists():
            return []
        return sorted(path.stem for path in self.PROFILES_DIR.glob("*.json") if path.is_file())

    def delete_profile(self, name: str) -> None:
        safe_name = self._validate_profile_name(name)
        path = self.PROFILES_DIR / f"{safe_name}.json"
        if path.exists():
            path.unlink()

    def _ensure_dirs(self) -> None:
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _validate_profile_name(name: str) -> str:
        safe_name = name.strip()
        if safe_name in {"", ".", ".."} or not PROFILE_SAFE_NAME.match(safe_name):
            raise ValueError("profile name must be 1-40 safe characters")
        return safe_name
