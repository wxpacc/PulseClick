import pytest

from src.core.hotkey import MOD_ALT, MOD_CONTROL, MOD_NOREPEAT, display_hotkey, parse_hotkey, parse_windows_hotkey


def test_parse_function_key():
    assert parse_hotkey("F6") == "<f6>"


def test_parse_combo():
    assert parse_hotkey("Ctrl+Alt+X") == "<ctrl>+<alt>+x"


def test_parse_windows_hotkey_flags_and_vk():
    hotkey = parse_windows_hotkey("Ctrl+Alt+X")

    assert hotkey.modifiers == MOD_NOREPEAT | MOD_CONTROL | MOD_ALT
    assert hotkey.vk == ord("X")


def test_duplicate_modifier_is_ignored():
    assert parse_hotkey("Ctrl+Ctrl+F6") == "<ctrl>+<f6>"


def test_display_hotkey():
    assert display_hotkey("Ctrl+Alt+X") == "Ctrl+Alt+X"


def test_reject_modifier_only():
    with pytest.raises(ValueError):
        parse_hotkey("Ctrl+Alt")


def test_reject_unknown_key():
    with pytest.raises(ValueError):
        parse_hotkey("Ctrl+Mouse1")
