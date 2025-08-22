#!/usr/bin/env python3
"""Print the current mouse coordinates.

Move the cursor to the desired location and press Ctrl+C to exit. The
last printed coordinates can be copied into ``config.ini``.
"""

import time

try:
    import pyautogui
except Exception:  # pragma: no cover - environment may not have pyautogui
    pyautogui = None  # type: ignore

if pyautogui is None:
    raise RuntimeError(
        "pyautogui is required but not installed. Install it with 'python -m pip install pyautogui'."
    )

print("Move the mouse to the target and press Ctrl+C to capture the coordinates.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"\r{x}, {y}", end="", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    x, y = pyautogui.position()
    print(f"\nFinal coordinates: {x}, {y}")
