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

You can grab the coordinates with the helper script:

```
python grab_coords.py
```

On Windows you can instead double‑click `run_grab_coords.bat` which launches the same
helper and keeps the window open after it prints the final coordinates.

If PyAutoGUI isn't installed you'll see a message explaining how to add it. Once the
script is running, move the cursor over the "Start"/"Replay" button and press
`Ctrl+C`. The final `x, y` values printed to the terminal can be copied into
`config.ini`.

Move the cursor over the "Start"/"Replay" button and press `Ctrl+C`. The final
`x, y` values printed to the terminal can be copied into `config.ini`.


Run the farmer from a shell (not the Python `help>` prompt):

```bash
python rsl_farmer.py --runs 10
```

Use `--config` to point to a different configuration file if needed.

You can also configure and launch the script through a small GUI:

```bash
python rsl_farmer.py --gui
```

On Windows, double‑click `run_farmer_gui.bat` to open the same window.

Run the farmer from a shell (not the Python `help>` prompt):

```bash
python rsl_farmer.py --runs 10
```

Use `--config` to point to a different configuration file if needed.


Install dependencies and run the farmer:

Run these commands from a shell (not the Python `help>` prompt):

```bash
python -m pip install -r requirements.txt  # installs PyAutoGUI and other dependencies


PyAutoGUI is available on PyPI and can be installed with `pip install pyautogui`
or via the requirements file below.


Install dependencies and run the farmer:

```bash
pip install -r requirements.txt  # installs PyAutoGUI and other dependencies
pip install -r requirements.txt

python rsl_farmer.py --start-x 1000 --start-y 800 --complete-img victory.png --runs 10
```

`complete-img` should point to an image that appears when the run ends (for example, a
screenshot of the "Victory" banner).

Instead of supplying command line arguments, you can launch a small
configuration window:

```bash
python rsl_farmer.py --gui
# or simply:
python rsl_farmer.py
```

The GUI lets you capture the start button coordinates, choose the completion
image and tweak run settings.


