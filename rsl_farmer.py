#!/usr/bin/env python3
"""Simple Raid: Shadow Legends farmer.

This script uses :mod:`pyautogui` to click the "Start"/"Replay" button of a
Raid: Shadow Legends dungeon and waits for an image indicating the run has
finished.  It is inspired by the automation features of
`rslhelper <https://github.com/KSPOG/rslhelper>`_.

The game client must be visible on screen and the coordinates of the
"Start"/"Replay" button supplied via ``config.ini``.  Screenshots that appear
when a run completes (e.g. "Victory" or "Defeat" banners) are loaded from the
``images/`` directory so the script knows when to start the next run.

Requires the [PyAutoGUI](https://pyautogui.readthedocs.io/) package, which can
be installed with ``python -m pip install pyautogui``.
"""

from __future__ import annotations

import argparse
import configparser
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

try:
    import pyautogui
except Exception:  # pragma: no cover - environment may not have pyautogui
    pyautogui = None  # type: ignore


@dataclass
class FarmerConfig:
    """Configuration for :class:`RSLFarmer`.

    Attributes
    ----------
    start_button:
        Coordinates of the "Start"/"Replay" button.
    img_dir:
        Directory containing images that indicate a run has completed,
        e.g. screenshots of the "Victory" or "Defeat" banners.
    run_delay:
        Delay between checks in seconds while waiting for a run to finish.
    timeout:
        Maximum time in seconds to wait for a run to finish before aborting.
    """

    start_button: Tuple[int, int]
    img_dir: str
    run_delay: float = 2.0
    timeout: float = 120.0


class RSLFarmer:
    """Automates repeated runs in Raid: Shadow Legends."""

    def __init__(self, config: FarmerConfig):
        if pyautogui is None:
            raise RuntimeError(
                "pyautogui is required but not installed. Install it with 'python -m pip install pyautogui'."
            )
        self.config = config
        self.images = [str(p) for p in Path(config.img_dir).iterdir() if p.is_file()]
        if not self.images:
            raise RuntimeError(f"No completion images found in '{config.img_dir}'.")

    def _wait_for_complete(self) -> None:
        start_time = time.time()
        while True:
            for img in self.images:
                if pyautogui.locateOnScreen(img, confidence=0.8):
                    return
            if time.time() - start_time > self.config.timeout:
                raise RuntimeError("Run timed out waiting for completion image.")
            time.sleep(self.config.run_delay)

    def run(self, runs: int) -> None:
        """Execute a number of runs.

        Parameters
        ----------
        runs:
            Number of runs to perform.
        """

        for i in range(1, runs + 1):
            pyautogui.click(*self.config.start_button)
            self._wait_for_complete()
            # click the "Replay" button, assumed to be at the same coordinates
            pyautogui.click(*self.config.start_button)
            time.sleep(self.config.run_delay)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default="config.ini",
        help="Path to configuration file with start button coords and settings",
    )
    parser.add_argument(
        "--runs", type=int, default=1, help="Number of runs to perform"
    )
    return parser.parse_args()


def load_config(path: str) -> FarmerConfig:
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise RuntimeError(f"Configuration file '{path}' not found")
    cfg = parser["farmer"]
    start_x = cfg.getint("start_x")
    start_y = cfg.getint("start_y")
    img_dir = cfg.get("img_dir", "images")
    run_delay = cfg.getfloat("run_delay", 2.0)
    timeout = cfg.getfloat("timeout", 120.0)
    return FarmerConfig(
        start_button=(start_x, start_y),
        img_dir=img_dir,
        run_delay=run_delay,
        timeout=timeout,
    )


def main() -> None:
    args = _parse_args()
    config = load_config(args.config)
    farmer = RSLFarmer(config)
    farmer.run(args.runs)


if __name__ == "__main__":
    main()
