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
