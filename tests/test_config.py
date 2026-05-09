import json
from src.core.config import ClickConfig
from src.utils.config import ConfigManager


def test_default_config_is_valid():
    config = ClickConfig()
    config.validate()
    assert config.interval_ms == 100
    assert config.hotkey == "F6"


def test_load_broken_json_returns_default(tmp_path):
    manager = ConfigManager(tmp_path / "data")
    manager.CONFIG_DIR.mkdir()
    manager.CONFIG_FILE.write_text("{broken", encoding="utf-8")

    config = manager.load()

    assert config == ClickConfig()


def test_save_and_load_config(tmp_path):
    manager = ConfigManager(tmp_path)
    config = ClickConfig(button="right", interval_ms=250, repeat_mode="count", repeat_count=12)

    manager.save(config)

    assert manager.load() == config


def test_profile_lifecycle(tmp_path):
    manager = ConfigManager(tmp_path)
    config = ClickConfig(click_type="triple")

    manager.save_profile("测试", config)

    assert manager.list_profiles() == ["测试"]
    assert manager.load_profile("测试").click_type == "triple"
    manager.delete_profile("测试")
    assert manager.list_profiles() == []


def test_config_from_dict_ignores_unknown_keys():
    config = ClickConfig.from_dict({"interval_ms": 20, "unknown": True})

    assert config.interval_ms == 20
    assert not hasattr(config, "unknown")


def test_invalid_random_range_fails():
    config = ClickConfig(random_enabled=True, random_min=200, random_max=100)

    try:
        config.validate()
    except ValueError as exc:
        assert "random_min" in str(exc)
    else:
        raise AssertionError("expected invalid random range")


def test_default_config_paths_use_project_data_dir():
    manager = ConfigManager()

    assert manager.CONFIG_DIR.name == "data"
    assert manager.CONFIG_FILE == manager.CONFIG_DIR / "config.json"
    assert manager.PROFILES_DIR == manager.CONFIG_DIR / "profiles"
