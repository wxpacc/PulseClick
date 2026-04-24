from __future__ import annotations

import sys

from src.app import PulseClickApp


def main() -> int:
    app = PulseClickApp(sys.argv)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

