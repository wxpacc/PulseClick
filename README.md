# PulseClick

[简体中文](README.zh-CN.md)

**Latest release:** [PulseClick v1.0.0](https://github.com/wxpacc/PulseClick/releases/tag/v1.0.0)  
**Direct download:** [PulseClick.exe](https://github.com/wxpacc/PulseClick/releases/download/v1.0.0/PulseClick.exe)

PulseClick is a lightweight portable auto clicker for Windows 10/11. It does not require installation: download it, run `PulseClick.exe`, and delete the whole folder when you no longer need it.

## Download

Use the GitHub Release build for normal users:

- Latest release: [PulseClick v1.0.0](https://github.com/wxpacc/PulseClick/releases/tag/v1.0.0)
- Direct download: [PulseClick.exe](https://github.com/wxpacc/PulseClick/releases/download/v1.0.0/PulseClick.exe)

Run `PulseClick.exe` after downloading. On first launch, PulseClick creates its runtime data next to the executable:

```text
data\config.json
data\profiles\
data\logs\pulseclick.log
```

To uninstall, exit PulseClick from the system tray and delete the whole PulseClick folder.

## Features

- Left, right, and middle mouse button clicks
- Single, double, and triple click modes
- Click interval from 1 ms to 1 hour
- Infinite loop or fixed repeat count
- Follow-cursor or fixed-position mode
- Screen overlay coordinate picker
- Global start/stop hotkey, default `F6`, with Ctrl/Alt/Shift/Win modifiers
- System tray actions
- Random delay range
- Config profiles
- Live status, CPS, click count, and elapsed runtime

## Project Status

- Target platform: Windows 10/11
- Release artifact: `PulseClick.exe`
- Input backend: Windows `SendInput`
- Global hotkey backend: Windows `RegisterHotKey`
- Portable data directory: `data\` next to the executable
- Default hotkey: `F6`

## Run From Source

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

When running from source, config and logs are written to the repository root:

```text
data\config.json
data\profiles\
data\logs\pulseclick.log
```

## Tests

```powershell
pytest
```

The test suite covers config persistence, hotkey parsing, clicker state transitions, and portable path behavior. Tests do not trigger real mouse clicks.

## Build

```powershell
python build.py
```

The output file is:

```text
dist\PulseClick.exe
```

`build\` and `PulseClick.spec` are temporary PyInstaller files. `dist\data\` is runtime data and should not be included in release uploads.

## Notes

- Windows 10/11 only.
- If `F6` is already used by another app, change the hotkey in the UI.
- PulseClick uses Windows `SendInput`; some games, anti-cheat systems, or security tools may block simulated input.
- Use auto-clicking only where it is legal, compliant, and allowed by the relevant platform rules.
