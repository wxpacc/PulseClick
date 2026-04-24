from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    if sys.platform != "win32":
        print("PulseClick is Windows-only. Build on Windows 10/11.")
        return 1

    root = Path(__file__).resolve().parent
    icon = root / "resources" / "icon.ico"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        "PulseClick",
        "--add-data",
        f"{root / 'resources'};resources",
    ]
    if icon.exists():
        command.extend(["--icon", str(icon)])
    command.append(str(root / "main.py"))
    return subprocess.call(command, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
