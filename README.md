# raidslegends
raid shadow

## Native Raid window helper

A Win32 helper library is provided in `src/main/native` for clicking and
capturing the "Raid: Shadow Legends" game window without moving the mouse.
Build the DLL on Windows with MinGW:

```
cd src\main\native
build.bat
```

This produces `build\RaidClient.dll` exporting:

- `BOOL clickRaid(int x, int y)` — post a left click to the game window
- `BOOL captureRaid(const char* path)` — save the client area as a BMP file

## Python farmer

A minimal farmer script inspired by [rslhelper](https://github.com/KSPOG/rslhelper)
resides in `rsl_farmer.py`. It uses [PyAutoGUI](https://pyautogui.readthedocs.io/)
to click the "Start"/"Replay" button and detect when a run has finished.
PyAutoGUI is available on PyPI and can be installed from your terminal with
`python -m pip install pyautogui`, or via the requirements file below.

Install dependencies and prepare configuration:

```bash
python -m pip install -r requirements.txt  # installs PyAutoGUI and other dependencies
```

Edit `config.ini` to set the screen coordinates of the "Start"/"Replay" button.
Create an `images/` directory in the project root and place one or more screenshots
that signify a completed run (e.g. "Victory" or "Defeat" banners) inside it. The
farmer will consider the run finished when any image in that directory appears on screen.

You can grab the coordinates with the helper script (run from a terminal, not the
Python `help>` prompt):

```
python grab_coords.py
```

On Windows you can instead double‑click `run_grab_coords.bat` which launches the same
helper and keeps the window open after it prints the final coordinates.

If PyAutoGUI isn't installed you'll see a message explaining how to add it. Once the
script is running, move the cursor over the "Start"/"Replay" button and press
`Ctrl+C`. The final `x, y` values printed to the terminal can be copied into
`config.ini`.

Run the farmer from a shell (not the Python `help>` prompt):

```bash
python rsl_farmer.py --runs 10
```

Use `--config` to point to a different configuration file if needed.
