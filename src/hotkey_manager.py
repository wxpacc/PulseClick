import threading
from PySide6.QtCore import QObject, Signal
from pynput import keyboard

SPECIAL_KEY_MAP = {
    "f1": "F1",
    "f2": "F2",
    "f3": "F3",
    "f4": "F4",
    "f5": "F5",
    "f6": "F6",
    "f7": "F7",
    "f8": "F8",
    "f9": "F9",
    "f10": "F10",
    "f11": "F11",
    "f12": "F12",
    "space": "Space",
    "enter": "Enter",
    "esc": "Escape",
    "tab": "Tab",
    "shift": "Shift",
    "shift_l": "Shift_L",
    "shift_r": "Shift_R",
    "ctrl": "Ctrl",
    "ctrl_l": "Ctrl_L",
    "ctrl_r": "Ctrl_R",
    "alt": "Alt",
    "alt_l": "Alt_L",
    "alt_r": "Alt_R",
    "backspace": "Backspace",
    "delete": "Delete",
    "insert": "Insert",
    "home": "Home",
    "end": "End",
    "page_up": "PageUp",
    "page_down": "PageDown",
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "caps_lock": "CapsLock",
    "cmd": "Cmd",
    "cmd_l": "Cmd_L",
    "cmd_r": "Cmd_R",
    "num_lock": "NumLock",
    "scroll_lock": "ScrollLock",
    "print_screen": "PrintScreen",
    "pause": "Pause",
}

REVERSE_KEY_MAP = {v: k for k, v in SPECIAL_KEY_MAP.items()}


def _key_to_display(key):
    if isinstance(key, keyboard.Key):
        name = key.name
        return SPECIAL_KEY_MAP.get(name, name.capitalize())
    if isinstance(key, keyboard.KeyCode):
        if key.char:
            return key.char.upper()
        if key.vk is not None:
            return f"VK_{key.vk}"
    return str(key)


class HotkeyManager(QObject):
    hotkey_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hotkey = "F6"
        self._listener = None
        self._recording = False
        self._lock = threading.Lock()

    def set_hotkey(self, key_name):
        with self._lock:
            self._hotkey = key_name
            was_listening = self._listener is not None and self._listener.is_alive()
        if was_listening:
            self.stop_listening()
            self.start_listening()

    def start_listening(self):
        self.stop_listening()
        listener = keyboard.Listener(
            on_press=self._on_key_press,
            daemon=True,
        )
        with self._lock:
            self._listener = listener
        listener.start()

    def stop_listening(self):
        with self._lock:
            listener = self._listener
            self._listener = None
        if listener is not None:
            listener.stop()

    def get_hotkey(self):
        with self._lock:
            return self._hotkey

    def start_recording(self):
        with self._lock:
            self._recording = True

    def is_recording(self):
        with self._lock:
            return self._recording

    def _on_key_press(self, key):
        display_name = _key_to_display(key)
        with self._lock:
            recording = self._recording
        if recording:
            with self._lock:
                self._recording = False
                self._hotkey = display_name
            self.stop_listening()
            self.start_listening()
            return
        with self._lock:
            current_hotkey = self._hotkey
        if display_name == current_hotkey:
            self.hotkey_pressed.emit()
