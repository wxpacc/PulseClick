from src.platform.windows.paths import app_data_dir, app_root_dir, config_dir, log_dir


def test_storage_paths_stay_under_project_root():
    assert app_data_dir() == app_root_dir() / "data"
    assert config_dir() == app_root_dir() / "data"
    assert log_dir() == app_root_dir() / "data" / "logs"
