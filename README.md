# Ugoh Notepad

A cross-platform plain-text notepad built entirely in Python with Kivy.
Runs as a Windows desktop app (`.exe`) and an Android app (`.apk`) from
the exact same codebase.

---

## 1. Project Structure

```
UgohNotepad/
├── main.py                        # Entry point - run this to start the app
├── app.py                         # Root Kivy App class, global shortcuts
├── buildozer.spec                 # Android build configuration
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── ui/
│   ├── screens/
│   │   └── editor_screen.py       # Main screen: wires toolbar+editor+status bar
│   ├── widgets/
│   │   ├── menu_bar.py            # Slim File/Edit/Search/Format/View/Tools dropdown menu bar
│   │   ├── status_bar.py          # Bottom status bar
│   │   └── find_replace_dialog.py # Find & Replace popup
│   └── themes/
│       └── theme_manager.py       # Light/Dark color palettes
├── utils/
│   ├── file_manager.py            # Open/Save/Save As, unsaved-change tracking
│   ├── recent_files.py            # Persists last 10 opened files to disk
│   ├── text_utils.py              # Word/char/line count, find/replace logic
│   └── autosave.py                # 30-second autosave timer
├── assets/
│   └── icons/                     # Put your app icon(s) here (see note below)
└── data/
    └── recent_files.json          # Auto-created at runtime, do not edit by hand
```

> **Note on assets/icons/:** no icon files are bundled. Drop a 512x512
> `icon.png` into `assets/icons/` and point `buildozer.spec`'s
> `icon.filename` at it before building the APK, and pass `--icon` to
> PyInstaller for the Windows build (see Section 5).

---

## 2. Dependencies (and why each is needed)

| Package | Why it's needed |
|---|---|
| `kivy` | The GUI framework. It's the only mainstream, stable Python framework that ships a real Android backend (python-for-android) alongside a Windows/Linux/macOS desktop backend, so one codebase runs everywhere. |
| `kivy_deps.sdl2`, `kivy_deps.glew`, `kivy_deps.angle` (Windows only) | Kivy's rendering backend on Windows needs SDL2 (windowing/input) and GLEW/ANGLE (OpenGL). They're installed only on Windows via the `sys_platform` marker in `requirements.txt`. |
| `pyinstaller` | Bundles the app + Python interpreter + Kivy runtime into a single standalone `.exe` so end users don't need Python installed. |
| `buildozer` | Automates the entire Android build pipeline (downloads the NDK/SDK, compiles native Kivy dependencies, and packages the `.apk`). Only runs on Linux. |

---

## 3. Installation Guide (Windows)

Open **Command Prompt** or **PowerShell** in the project folder.

**Step 1 - Create a virtual environment**
```bat
python -m venv venv
```

**Step 2 - Activate it**
```bat
venv\Scripts\activate
```

**Step 3 - Install dependencies**
```bat
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4 - Run the app**
```bat
python main.py
```

You should see the Ugoh Notepad window open with the toolbar, text
editor, and status bar.

---

## 4. Installation Guide (Linux / macOS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 main.py
```

---

## 5. Packaging for Windows (.exe)

With your virtual environment active and `pyinstaller` installed:

```bat
pyinstaller --name "UgohNotepad" --windowed --onefile ^
    --icon assets\icons\icon.ico ^
    --add-data "data;data" ^
    main.py
```

- `--windowed` prevents a console window from appearing behind the GUI.
- `--onefile` produces a single `UgohNotepad.exe` in the `dist/` folder.
- `--icon` is optional - remove it if you haven't added an `.ico` file yet.
- `--add-data "data;data"` bundles the `data/` folder (recent files
  storage) into the executable.

The final executable will be at `dist\UgohNotepad.exe`. Double-click it
to run - no Python installation required on the target machine.

> **PyInstaller + Kivy tip:** if the built `.exe` opens a blank window,
> add `--hidden-import=kivy.core.window.window_sdl2` and
> `--hidden-import=kivy.core.text.text_sdl2` to the command above.
> This is a known quirk of Kivy + PyInstaller and is not specific to
> this project.

---

## 6. Android APK Build Guide (Buildozer)

Buildozer only runs on **Linux** (native Ubuntu, or WSL2 on Windows).

### 6.1 Installation (Ubuntu/Debian/WSL2)

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

pip install --upgrade pip
pip install buildozer cython
```

### 6.2 First-time build

From inside the `UgohNotepad/` folder (where `buildozer.spec` lives):

```bash
buildozer android debug
```

The very first run downloads the Android SDK, NDK, and other build
tools automatically - this can take 20-60 minutes depending on your
internet connection. Subsequent builds are much faster.

### 6.3 Where the APK ends up

```
UgohNotepad/bin/ugohnotepad-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 6.4 Building a release (signed) APK

```bash
buildozer android release
```

You'll need to sign the resulting unsigned APK with `apksigner` and
your own keystore before publishing to the Play Store - see Android's
official app-signing documentation for that step, as it's outside the
scope of Buildozer itself.

### 6.5 Common Errors & Fixes

| Error | Fix |
|---|---|
| `Aidl not found` | Re-run `buildozer android debug` - Buildozer needs to finish downloading the SDK build-tools. |
| `Command failed: ./gradlew ...` | Usually a Java version mismatch. Make sure `openjdk-17-jdk` is installed and `JAVA_HOME` points to it. |
| `Unable to find python3 executable` | Delete the `.buildozer` folder and rebuild - it caches a broken toolchain path. |
| Build hangs on "Installing android sdk" | Check your internet connection; SDK downloads are several GB. |
| `INSTALL_FAILED_INSUFFICIENT_STORAGE` when installing on phone | Free up space on the Android device. |
| App crashes instantly on phone | Run `buildozer android debug deploy run logcat` and check the traceback in the log output. |

### 6.6 Installing the APK on your phone

1. Copy the `.apk` file from `bin/` to your phone (USB cable, or
   `adb push`, or cloud storage).
2. On the phone, enable **Settings → Security → Install unknown apps**
   for the app you used to open the file (e.g. Files, Chrome).
3. Tap the `.apk` file and confirm installation.

Or, with the phone connected via USB and USB debugging enabled:

```bash
buildozer android deploy run
```

This builds, installs, and launches the app on the connected device
in one step.

---

## 7. Testing

### 7.1 Sample test files

Create these two files in the project root to use while manually
testing Open/Save:

**`sample_test_1.txt`**
```
The quick brown fox jumps over the lazy dog.
This is line two of the sample file.
```

**`sample_test_2.txt`**
```
Ugoh Notepad
============
A cross-platform notepad written in Python and Kivy.
Test line for word count, find and replace, and autosave.
```

### 7.2 Manual test checklist

| Feature | How to test |
|---|---|
| New | Click **New** with unsaved text - confirm the discard prompt appears. |
| Open | Click **Open**, select `sample_test_1.txt` - confirm text loads. |
| Save | Edit the text, click **Save** - reopen the file to confirm changes persisted. |
| Save As | Click **Save As**, choose a new name/folder - confirm a new file is created. |
| Undo/Redo | Type text, click **Undo**, then **Redo** - confirm text reverts and reapplies. |
| Cut/Copy/Paste | Select text, **Cut**, click elsewhere, **Paste** - confirm it moves correctly. |
| Select All | Click **Select All** - confirm the entire document is highlighted. |
| Find | Click **Find**, search for a word that exists - confirm it's selected/highlighted. |
| Replace | Click **Replace**, replace one or all occurrences - confirm text updates. |
| Word Count | Click **Word Count** - confirm the popup shows correct words/chars/lines. |
| Dark Mode | Click **Dark Mode** - confirm colors invert; click again to revert. |
| Zoom | Click **Zoom +** / **Zoom -** / **Reset Zoom** - confirm font size changes. |
| Font family/size | Change the spinners - confirm the editor font updates live. |
| Autosave | Save a file once, wait 30+ seconds after editing - confirm the file on disk updates without clicking Save. |
| Unsaved changes warning | Edit text, close the window - confirm a confirmation popup appears before exit. |
| Recent files | Open a few different files, check `data/recent_files.json` - confirm up to 10 paths are stored, most recent first. |
| Keyboard shortcuts | Try Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+Shift+S, Ctrl+Z, Ctrl+Y, Ctrl+X, Ctrl+C, Ctrl+V, Ctrl+A, Ctrl+F, Ctrl+H, Ctrl++, Ctrl+- - confirm each triggers the matching action. |

### 7.3 Automated logic tests

The text-processing logic in `utils/text_utils.py` and
`utils/file_manager.py` has no Kivy dependency and can be tested with
plain `unittest`. Example (save as `tests/test_text_utils.py`):

```python
import unittest
from utils.text_utils import TextStats

class TestTextStats(unittest.TestCase):
    def test_word_count(self):
        self.assertEqual(TextStats.word_count("Hello world"), 2)

    def test_char_count(self):
        self.assertEqual(TextStats.char_count("Hello"), 5)

    def test_replace_all(self):
        text, count = TextStats.replace_all("cat cat cat", "cat", "dog")
        self.assertEqual(text, "dog dog dog")
        self.assertEqual(count, 3)

if __name__ == "__main__":
    unittest.main()
```

Run with:
```bash
python -m unittest discover tests
```

---

## 8. Known Limitation: Rich Text Formatting

Ugoh Notepad saves and loads **plain `.txt` files**, exactly like
Windows Notepad. Plain text has no mechanism to store "this word is
bold" - that requires a rich format such as `.rtf` or `.docx`. The
Bold/Italic/Underline toolbar buttons are included per the spec, but
they only change how the *editor view* looks (a display preference);
that styling is intentionally **not** written to the saved file, since
doing so would silently corrupt the plain-text format users expect
from a notepad app.

---

## 9. Final Checklist

- [x] Runs on Windows as a desktop app via `python main.py`
- [x] Packages into a standalone `.exe` via PyInstaller
- [x] Builds into an `.apk` via Buildozer for Android
- [x] Toolbar: New, Open, Save, Save As, Undo, Redo, Cut, Copy, Paste, Select All, Find, Replace, Word Count, Dark Mode
- [x] Status bar: line, column, word count, character count, filename
- [x] Find & Replace with Find Next and Replace All
- [x] Font family + font size controls, Bold/Italic/Underline (display-only, see Section 8)
- [x] Dark Mode / Light Mode toggle
- [x] Zoom In / Zoom Out / Reset Zoom
- [x] Word/Character/Line counter + reading time estimate
- [x] Autosave every 30 seconds
- [x] Unsaved-changes warning before closing
- [x] Recent files list (last 10, persisted to `data/recent_files.json`)
- [x] Full keyboard shortcut support
- [x] Touch-friendly, responsive layout for Android (portrait + landscape)
- [x] Clean OOP architecture with no duplicated logic
