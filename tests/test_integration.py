from src.core.config import ClickConfig
from src.utils.config import ConfigManager


def test_config_round_trip_integration(tmp_path):
    manager = ConfigManager(tmp_path)
    config = ClickConfig(button="middle", click_type="single", interval_ms=33, hotkey="Ctrl+Alt+P")

    manager.save(config)
    loaded = manager.load()

    assert loaded == config

