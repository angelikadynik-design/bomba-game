# My Python Games and Apps

This project has three small apps. They are made with Python and tkinter. You do not need to install extra Python packages.

## 1. Bomb Clicker

Open the game and click the bomb 30 times before the 10-second timer ends. Click fast to win! The game shows how much time and how many clicks are left. Press **Restart** to play again.

Run it with:

```bash
python bomb_clicker/main.py
```

## 2. Mage's Diary

This is a little wizard notebook. You can make notes, write their titles and text, and add tags such as `spell` or `potion`. Use the search box to find notes by tag. You can also save or delete notes.

Your notes are saved in `mage_diary/notes.json`. The app can start even if this file is missing or empty.

Run it with:

```bash
python mage_diary/main.py
```

## 3. Catch the Star

Try to click the star as many times as you can before 30 seconds are over. The star moves to a new place after each click and gets faster as you score more points. The game shows your score and your best score.

Your best score is saved in `my_game/best_score.json`. The app can start if this file is missing or empty.

Run it with:

```bash
python my_game/main.py
```

## What you need

- Python 3.10 or newer
- tkinter, which comes with many Python installations

On some Linux computers, tkinter may need to be installed separately as `python3-tk`.

If your computer uses `python3` instead of `python`, use `python3` in the commands above.
