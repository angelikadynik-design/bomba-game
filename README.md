# Python GUI Homework Project

A collection of three small, beginner-friendly desktop applications made with Python 3 and `tkinter`. The code uses only Python's standard library and includes short English comments where helpful.

## Project contents

### `bomb_clicker/main.py` — Bomb Clicker

A timed click game. Click the bomb 30 times before the 10-second countdown ends to defuse it. The window shows the remaining time and clicks, displays **Bomb defused!** or **BOOM!**, and includes a Restart button.

### `mage_diary/main.py` — Mage's Diary

A spellbook-themed notes app with a list of note titles and an editor. Create, edit, save, and delete notes; add comma-separated tags and filter the list by tag. Notes are stored in `mage_diary/notes.json`, created next to the script when needed. Missing, empty, or invalid JSON files are handled without crashing.

### `my_game/main.py` — Catch the Star

A complete 30-second game with start, play, and game-over screens. Click the star as it moves around the canvas to score points. The target moves more quickly as your score increases. Your best score is stored in `my_game/best_score.json`; if the file is missing or unreadable, the game starts with a best score of zero.

### Other files

- `.gitignore` excludes Python cache files and generated game data files.
- `README.md` explains the project, requirements, and how to launch each app.

## Requirements

- Python 3.10 or later
- `tkinter` (included with many Python installations; no third-party packages are used)

On some Linux distributions, tkinter is packaged separately from Python. If importing `tkinter` fails, install your distribution's standard `python3-tk` package.

## Run an app

Run a command from the repository's root directory:

```bash
python bomb_clicker/main.py
python mage_diary/main.py
python my_game/main.py
```

On systems where Python 3 is invoked as `python3`, replace `python` with `python3`.
