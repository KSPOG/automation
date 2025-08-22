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




"""


"Start"/"Replay" button supplied.  An image of the "Victory" (or "Defeat")
screen is required so the script knows when to start the next run.

Requires the [PyAutoGUI](https://pyautogui.readthedocs.io/) package, which can
be installed with ``python -m pip install pyautogui``.



from __future__ import annotations

import argparse
import configparser
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple



import sys
import time
from dataclasses import dataclass
from typing import Tuple

try:  # pragma: no cover - tkinter may be unavailable in some environments
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception:  # pragma: no cover
    tk = None  # type: ignore

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




    complete_img:
        Path to an image on disk that appears when a run is complete,
        e.g. a screenshot of the "Victory" banner.


    run_delay:
        Delay between checks in seconds while waiting for a run to finish.
    timeout:
        Maximum time in seconds to wait for a run to finish before aborting.
    """

    start_button: Tuple[int, int]
    img_dir: str


    complete_img: str

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



                "pyautogui is required but not installed. Install with 'pip install pyautogui'."
            )
        self.config = config



    def _wait_for_complete(self) -> None:
        start_time = time.time()
        while True:
            for img in self.images:
                if pyautogui.locateOnScreen(img, confidence=0.8):
                    return



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
    parser.add_argument(
        "--config",
        default="config.ini",
        help="Path to configuration file with start button coords and settings",
    )
    parser.add_argument(
        "--runs", type=int, help="Number of runs to perform"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open a Tkinter window to configure and start the farmer",

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


def run_gui(config_path: str) -> None:
    """Open a simple Tkinter window to configure and start the farmer."""

    if pyautogui is None:
        raise RuntimeError(
            "pyautogui is required for the GUI. Install it with 'python -m pip install pyautogui'."
        )

    import tkinter as tk
    from tkinter import filedialog, messagebox

    # Load existing configuration if available
    cfg = None
    try:
        cfg = load_config(config_path)
    except Exception:
        cfg = FarmerConfig(start_button=(0, 0), img_dir="images")

    root = tk.Tk()
    root.title("RSL Farmer")

    start_x_var = tk.StringVar(value=str(cfg.start_button[0]))
    start_y_var = tk.StringVar(value=str(cfg.start_button[1]))
    img_dir_var = tk.StringVar(value=cfg.img_dir)
    runs_var = tk.StringVar(value="1")
    run_delay_var = tk.StringVar(value=str(cfg.run_delay))
    timeout_var = tk.StringVar(value=str(cfg.timeout))

    def grab_coords() -> None:
        messagebox.showinfo(
            "Grab Coordinates",
            "Move the mouse over the Start/Replay button and click OK",
        )
        x, y = pyautogui.position()
        start_x_var.set(str(x))
        start_y_var.set(str(y))

    def choose_dir() -> None:
        path = filedialog.askdirectory()
        if path:
            img_dir_var.set(path)

    def start_farming() -> None:
        try:
            config = FarmerConfig(
                start_button=(int(start_x_var.get()), int(start_y_var.get())),
                img_dir=img_dir_var.get(),
                run_delay=float(run_delay_var.get()),
                timeout=float(timeout_var.get()),
            )
            farmer = RSLFarmer(config)
            farmer.run(int(runs_var.get()))
            messagebox.showinfo("RSL Farmer", "Farming complete")
        except Exception as exc:
            messagebox.showerror("RSL Farmer", str(exc))

    tk.Label(root, text="Start X").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=start_x_var, width=6).grid(row=0, column=1)
    tk.Label(root, text="Start Y").grid(row=0, column=2, sticky="e")
    tk.Entry(root, textvariable=start_y_var, width=6).grid(row=0, column=3)
    tk.Button(root, text="Grab", command=grab_coords).grid(row=0, column=4)

    tk.Label(root, text="Images").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=img_dir_var, width=30).grid(row=1, column=1, columnspan=3)
    tk.Button(root, text="Browse", command=choose_dir).grid(row=1, column=4)

    tk.Label(root, text="Runs").grid(row=2, column=0, sticky="e")
    tk.Entry(root, textvariable=runs_var, width=6).grid(row=2, column=1)
    tk.Label(root, text="Delay").grid(row=2, column=2, sticky="e")
    tk.Entry(root, textvariable=run_delay_var, width=6).grid(row=2, column=3)

    tk.Label(root, text="Timeout").grid(row=3, column=0, sticky="e")
    tk.Entry(root, textvariable=timeout_var, width=6).grid(row=3, column=1)
    tk.Button(root, text="Start", command=start_farming).grid(row=3, column=4)

def launch_gui() -> None:
    """Open a simple Tkinter window to configure and start the farmer."""
    if tk is None:
        raise RuntimeError("tkinter is required for the GUI but is not available.")
    if pyautogui is None:
        raise RuntimeError(
            "pyautogui is required but not installed. Install it with 'python -m pip install pyautogui'."
        )

    root = tk.Tk()
    root.title("RSL Farmer")

    start_x_var = tk.StringVar()
    start_y_var = tk.StringVar()
    img_var = tk.StringVar()
    runs_var = tk.StringVar(value="1")
    delay_var = tk.StringVar(value="2.0")
    timeout_var = tk.StringVar(value="120.0")

    def capture_start() -> None:
        root.withdraw()
        time.sleep(3)
        x, y = pyautogui.position()
        start_x_var.set(str(x))
        start_y_var.set(str(y))
        root.deiconify()

    def browse_img() -> None:
        path = filedialog.askopenfilename()
        if path:
            img_var.set(path)

    def start_runs() -> None:
        try:
            config = FarmerConfig(
                start_button=(int(start_x_var.get()), int(start_y_var.get())),
                complete_img=img_var.get(),
                run_delay=float(delay_var.get()),
                timeout=float(timeout_var.get()),
            )
            runs = int(runs_var.get())
        except Exception as exc:  # pragma: no cover - user input errors
            messagebox.showerror("Invalid input", str(exc))
            return

        root.withdraw()
        try:
            RSLFarmer(config).run(runs)
        except Exception as exc:  # pragma: no cover - runtime errors
            messagebox.showerror("Error", str(exc))
        finally:
            root.deiconify()

    # Layout
    frm = tk.Frame(root)
    frm.pack(padx=10, pady=10)

    tk.Label(frm, text="Start X").grid(row=0, column=0, sticky="e")
    tk.Entry(frm, textvariable=start_x_var, width=6).grid(row=0, column=1)
    tk.Label(frm, text="Start Y").grid(row=0, column=2, sticky="e")
    tk.Entry(frm, textvariable=start_y_var, width=6).grid(row=0, column=3)
    tk.Button(frm, text="Capture", command=capture_start).grid(row=0, column=4, padx=(5, 0))

    tk.Label(frm, text="Completion image").grid(row=1, column=0, sticky="e")
    tk.Entry(frm, textvariable=img_var, width=25).grid(row=1, column=1, columnspan=3)
    tk.Button(frm, text="Browse", command=browse_img).grid(row=1, column=4, padx=(5, 0))

    tk.Label(frm, text="Runs").grid(row=2, column=0, sticky="e")
    tk.Entry(frm, textvariable=runs_var, width=6).grid(row=2, column=1)

    tk.Label(frm, text="Delay").grid(row=2, column=2, sticky="e")
    tk.Entry(frm, textvariable=delay_var, width=6).grid(row=2, column=3)

    tk.Label(frm, text="Timeout").grid(row=3, column=0, sticky="e")
    tk.Entry(frm, textvariable=timeout_var, width=6).grid(row=3, column=1)

    tk.Button(frm, text="Start", command=start_runs).grid(row=4, column=0, columnspan=5, pady=(10, 0))


    root.mainloop()


def main() -> None:
    args = _parse_args()
    if args.gui or args.runs is None:
        run_gui(args.config)
        return
    config = load_config(args.config)
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gui", action="store_true", help="Launch configuration window")
    parser.add_argument("--start-x", type=int, help="X coordinate of Start/Replay button")
    parser.add_argument("--start-y", type=int, help="Y coordinate of Start/Replay button")
    parser.add_argument("--complete-img", help="Path to an image that signifies a completed run")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs to perform")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between checks in seconds")
    parser.add_argument("--timeout", type=float, default=120.0, help="Maximum time to wait for completion image")

    argv = sys.argv[1:]
    if not argv:
        return argparse.Namespace(gui=True, start_x=None, start_y=None,
                                  complete_img=None, runs=1, delay=2.0, timeout=120.0)
    args = parser.parse_args(argv)
    if not args.gui and (
        args.start_x is None or args.start_y is None or args.complete_img is None
    ):
        parser.error("--start-x, --start-y and --complete-img are required unless --gui is used")
    return args

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
    config = load_config(args.config)


    if args.gui:
        launch_gui()
        return
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
