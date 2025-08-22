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

Install dependencies and run the farmer:

Run these commands from a shell (not the Python `help>` prompt):

```bash
python -m pip install -r requirements.txt  # installs PyAutoGUI and other dependencies
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
