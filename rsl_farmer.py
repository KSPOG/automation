#!/usr/bin/env python3
"""Simple Raid: Shadow Legends farmer.

This script uses :mod:`pyautogui` to click the "Start"/"Replay" button of a
Raid: Shadow Legends dungeon and waits for an image indicating the run has
finished.  It is inspired by the automation features of
`rslhelper <https://github.com/KSPOG/rslhelper>`_.

The game client must be visible on screen and the coordinates of the
"Start"/"Replay" button supplied.  An image of the "Victory" (or "Defeat")
screen is required so the script knows when to start the next run.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
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
    complete_img:
        Path to an image on disk that appears when a run is complete,
        e.g. a screenshot of the "Victory" banner.
    run_delay:
        Delay between checks in seconds while waiting for a run to finish.
    timeout:
        Maximum time in seconds to wait for a run to finish before aborting.
    """

    start_button: Tuple[int, int]
    complete_img: str
    run_delay: float = 2.0
    timeout: float = 120.0


class RSLFarmer:
    """Automates repeated runs in Raid: Shadow Legends."""

    def __init__(self, config: FarmerConfig):
        if pyautogui is None:
            raise RuntimeError(
                "pyautogui is required but not installed. Install with 'pip install pyautogui'."
            )
        self.config = config

    def _wait_for_complete(self) -> None:
        start_time = time.time()
        while True:
            if pyautogui.locateOnScreen(self.config.complete_img, confidence=0.8):
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
    parser.add_argument("--start-x", type=int, required=True,
                        help="X coordinate of Start/Replay button")
    parser.add_argument("--start-y", type=int, required=True,
                        help="Y coordinate of Start/Replay button")
    parser.add_argument("--complete-img", required=True,
                        help="Path to an image that signifies a completed run")
    parser.add_argument("--runs", type=int, default=1,
                        help="Number of runs to perform")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Delay between checks in seconds")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="Maximum time to wait for completion image")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config = FarmerConfig(
        start_button=(args.start_x, args.start_y),
        complete_img=args.complete_img,
        run_delay=args.delay,
        timeout=args.timeout,
    )
    farmer = RSLFarmer(config)
    farmer.run(args.runs)


if __name__ == "__main__":
    main()
