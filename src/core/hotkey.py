from __future__ import annotations

import ctypes
import threading
from collections.abc import Callable
from ctypes import wintypes


MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312
WM_QUIT = 0x0012

MODIFIER_ALIASES = {
    "CTRL": ("ctrl", MOD_CONTROL),
    "CONTROL": ("ctrl", MOD_CONTROL),
    "ALT": ("alt", MOD_ALT),
    "SHIFT": ("shift", MOD_SHIFT),
    "WIN": ("win", MOD_WIN),
    "WINDOWS": ("win", MOD_WIN),
}

SPECIAL_KEYS = {
    "ESC": ("esc", 0x1B),
    "ESCAPE": ("esc", 0x1B),
    "SPACE": ("space", 0x20),
    "ENTER": ("enter", 0x0D),
    "TAB": ("tab", 0x09),
    "BACKSPACE": ("backspace", 0x08),
    "DELETE": ("delete", 0x2E),
    "INSERT": ("insert", 0x2D),
    "HOME": ("home", 0x24),
    "END": ("end", 0x23),
    "PAGEUP": ("page_up", 0x21),
    "PAGEDOWN": ("page_down", 0x22),
    "UP": ("up", 0x26),
    "DOWN": ("down", 0x28),
    "LEFT": ("left", 0x25),
    "RIGHT": ("right", 0x27),
}


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", wintypes.POINT),
    ]


user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

user32.RegisterHotKey.argtypes = [wintypes.HWND, wintypes.INT, wintypes.UINT, wintypes.UINT]
user32.RegisterHotKey.restype = wintypes.BOOL
user32.UnregisterHotKey.argtypes = [wintypes.HWND, wintypes.INT]
user32.UnregisterHotKey.restype = wintypes.BOOL
user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL
user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.PostThreadMessageW.restype = wintypes.BOOL
kernel32.GetCurrentThreadId.argtypes = []
kernel32.GetCurrentThreadId.restype = wintypes.DWORD


def parse_hotkey(text: str) -> str:
    parsed = parse_windows_hotkey(text)
    return "+".join(parsed.parts)


def parse_windows_hotkey(text: str) -> "WindowsHotkey":
    parts = [part.strip() for part in text.replace("-", "+").split("+") if part.strip()]
    if not parts:
        raise ValueError("hotkey cannot be empty")

    normalized_parts: list[str] = []
    modifiers = MOD_NOREPEAT
    seen_modifiers: set[str] = set()
    vk: int | None = None
    key_label: str | None = None

    for raw_part in parts:
        token = raw_part.upper()
        if token in MODIFIER_ALIASES:
            label, flag = MODIFIER_ALIASES[token]
            if label not in seen_modifiers:
                normalized_parts.append(f"<{label}>")
                modifiers |= flag
                seen_modifiers.add(label)
            continue
        if vk is not None:
            raise ValueError("hotkey can contain only one non-modifier key")
        key_label, vk = _normalize_non_modifier(token)
        normalized_parts.append(key_label)

    if vk is None:
        raise ValueError("hotkey must include a non-modifier key")
    return WindowsHotkey(parts=tuple(normalized_parts), modifiers=modifiers, vk=vk)


def display_hotkey(text: str) -> str:
    parsed = parse_windows_hotkey(text)
    labels: list[str] = []
    for part in parsed.parts:
        if part.startswith("<") and part.endswith(">"):
            labels.append(part[1:-1].capitalize())
        elif len(part) == 1:
            labels.append(part.upper())
        else:
            labels.append(part.replace("_", " ").title().replace(" ", ""))
    return "+".join(labels)


def _normalize_non_modifier(token: str) -> tuple[str, int]:
    if len(token) == 1 and token.isalnum():
        return token.lower(), ord(token)
    if token.startswith("F") and token[1:].isdigit() and 1 <= int(token[1:]) <= 24:
        number = int(token[1:])
        return f"<f{number}>", 0x70 + number - 1
    if token in SPECIAL_KEYS:
        label, vk = SPECIAL_KEYS[token]
        return f"<{label}>", vk
    raise ValueError(f"unsupported hotkey key: {token}")


class WindowsHotkey(tuple):
    __slots__ = ()

    def __new__(cls, parts: tuple[str, ...], modifiers: int, vk: int):
        return super().__new__(cls, (parts, modifiers, vk))

    @property
    def parts(self) -> tuple[str, ...]:
        return self[0]

    @property
    def modifiers(self) -> int:
        return self[1]

    @property
    def vk(self) -> int:
        return self[2]


class HotkeyManager:
    HOTKEY_ID = 1

    def __init__(self) -> None:
        self._hotkey = "F6"
        self._callback: Callable[[], None] | None = None
        self._thread: threading.Thread | None = None
        self._thread_id = 0
        self._ready = threading.Event()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._startup_error: Exception | None = None

    def register(self, hotkey: str, callback: Callable[[], None]) -> None:
        parse_windows_hotkey(hotkey)
        with self._lock:
            self._hotkey = hotkey
            self._callback = callback
            running = self._thread is not None
        if running:
            self.start()

    def start(self) -> None:
        self.stop()
        with self._lock:
            if self._callback is None:
                return
            self._ready.clear()
            self._stop_event.clear()
            self._startup_error = None
            self._thread = threading.Thread(target=self._message_loop, name="PulseClickHotkey", daemon=True)
            self._thread.start()
        if not self._ready.wait(timeout=2.0):
            raise RuntimeError("hotkey listener did not start")
        if self._startup_error is not None:
            self.stop()
            raise self._startup_error

    def stop(self) -> None:
        with self._lock:
            thread = self._thread
            thread_id = self._thread_id
            self._thread = None
            self._thread_id = 0
            self._stop_event.set()
        if thread and thread.is_alive():
            if thread_id:
                user32.PostThreadMessageW(thread_id, WM_QUIT, 0, 0)
            thread.join(timeout=1.0)

    def _message_loop(self) -> None:
        parsed = parse_windows_hotkey(self._hotkey)
        self._thread_id = int(kernel32.GetCurrentThreadId())
        if not user32.RegisterHotKey(None, self.HOTKEY_ID, parsed.modifiers, parsed.vk):
            self._startup_error = ctypes.WinError(ctypes.get_last_error())
            self._ready.set()
            return
        self._ready.set()
        message = MSG()
        try:
            while not self._stop_event.is_set() and user32.GetMessageW(ctypes.byref(message), None, 0, 0) != 0:
                if message.message == WM_HOTKEY and int(message.wParam) == self.HOTKEY_ID:
                    callback = self._callback
                    if callback:
                        callback()
                elif message.message == WM_QUIT:
                    break
        finally:
            user32.UnregisterHotKey(None, self.HOTKEY_ID)
