import json
from pathlib import Path
import random
import time
import tkinter as tk


DATA_FILE = Path(__file__).resolve().with_name("best_score.json")
GAME_LENGTH = 30


def load_best_score():
    """Return previous best score or 0 if file is missing or invalid."""
    if not DATA_FILE.exists():
        return 0

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return 0
            data = json.loads(content)
            if isinstance(data, dict):
                return int(data.get("best_score", 0))
            return 0
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return 0


def save_best_score(value):
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump({"best_score": value}, file)
    except OSError:
        pass


class CatchTheStar:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Star")
        self.root.geometry("560x560")
        self.root.resizable(False, False)

        self.best_score = load_best_score()
        self.score = 0
        self.time_left = GAME_LENGTH
        self.game_running = False
        self.target_speed = 900
        self.after_id = None

        self.container = tk.Frame(root, bg="#f5f7ff")
        self.container.pack(fill="both", expand=True)

        self.start_frame = tk.Frame(self.container, bg="#f5f7ff")
        self.start_frame.pack(fill="both", expand=True)

        tk.Label(
            self.start_frame,
            text="Catch the Star",
            font=("Arial", 28, "bold"),
            bg="#f5f7ff",
        ).pack(pady=(90, 10))
        tk.Label(
            self.start_frame,
            text="Click the star as many times as you can in 30 seconds.",
            font=("Arial", 12),
            bg="#f5f7ff",
            wraplength=420,
        ).pack(pady=10)
        tk.Button(
            self.start_frame,
            text="Play",
            font=("Arial", 14, "bold"),
            command=self.start_game,
            width=14,
            height=2,
            bg="#4caf50",
            fg="white",
        ).pack(pady=20)

        self.game_frame = tk.Frame(self.container, bg="#f5f7ff")
        self.game_frame.pack(fill="both", expand=True)
        self.game_frame.pack_forget()

        top_bar = tk.Frame(self.game_frame, bg="#f5f7ff")
        top_bar.pack(fill="x", padx=20, pady=(20, 10))

        self.score_label = tk.Label(top_bar, text="Score: 0", font=("Arial", 16, "bold"), bg="#f5f7ff")
        self.score_label.pack(side="left")

        self.time_label = tk.Label(top_bar, text="Time: 30", font=("Arial", 16, "bold"), bg="#f5f7ff")
        self.time_label.pack(side="right")

        self.best_label = tk.Label(top_bar, text=f"Best: {self.best_score}", font=("Arial", 12), bg="#f5f7ff")
        self.best_label.pack(side="right", padx=(0, 20))

        self.canvas = tk.Canvas(self.game_frame, width=500, height=420, bg="#ffffff", highlightthickness=2, highlightbackground="#dfe7ff")
        self.canvas.pack(padx=20, pady=10)

        self.end_frame = tk.Frame(self.container, bg="#f5f7ff")
        self.end_frame.pack(fill="both", expand=True)
        self.end_frame.pack_forget()

        self.result_label = tk.Label(self.end_frame, text="", font=("Arial", 22, "bold"), bg="#f5f7ff")
        self.result_label.pack(pady=(80, 10))

        self.final_score_label = tk.Label(self.end_frame, text="", font=("Arial", 14), bg="#f5f7ff")
        self.final_score_label.pack(pady=10)

        self.play_again_button = tk.Button(
            self.end_frame,
            text="Play again",
            font=("Arial", 14, "bold"),
            command=self.start_game,
            width=14,
            height=2,
            bg="#3b82f6",
            fg="white",
        )
        self.play_again_button.pack(pady=20)

    def show_frame(self, frame_name):
        for frame in (self.start_frame, self.game_frame, self.end_frame):
            frame.pack_forget()
        if frame_name == "start":
            self.start_frame.pack(fill="both", expand=True)
        elif frame_name == "game":
            self.game_frame.pack(fill="both", expand=True)
        else:
            self.end_frame.pack(fill="both", expand=True)

    def random_target_position(self):
        margin = 30
        x = random.randint(margin, 500 - margin)
        y = random.randint(margin, 420 - margin)
        return x, y

    def spawn_target(self):
        x, y = self.random_target_position()
        self.target = self.canvas.create_text(x, y, text="★", font=("Arial", 28, "bold"), fill="#f5c542")
        self.canvas.tag_bind(self.target, "<Button-1>", self.hit_target)

    def hit_target(self, event):
        if not self.game_running:
            return

        self.score += 1
        self.best_score = max(self.best_score, self.score)
        save_best_score(self.best_score)
        self.canvas.delete(self.target)
        self.score_label.config(text=f"Score: {self.score}")
        self.best_label.config(text=f"Best: {self.best_score}")
        self.target_speed = max(250, 900 - self.score * 20)
        self.spawn_target()

    def update_clock(self):
        if not self.game_running:
            return

        self.time_left -= 1
        self.time_label.config(text=f"Time: {self.time_left}")

        if self.time_left <= 0:
            self.end_game()
            return

        self.after_id = self.root.after(1000, self.update_clock)

    def start_game(self):
        self.score = 0
        self.time_left = GAME_LENGTH
        self.game_running = True
        self.target_speed = 900
        self.score_label.config(text="Score: 0")
        self.time_label.config(text=f"Time: {self.time_left}")
        self.best_label.config(text=f"Best: {self.best_score}")

        self.canvas.delete("all")
        self.show_frame("game")
        self.spawn_target()

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(1000, self.update_clock)

    def end_game(self):
        self.game_running = False
        self.canvas.delete("all")
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.result_label.config(text="Game over")
        self.final_score_label.config(text=f"Your score: {self.score}\nBest score: {self.best_score}")
        self.show_frame("end")


if __name__ == "__main__":
    root = tk.Tk()
    app = CatchTheStar(root)
    app.show_frame("start")
    root.mainloop()

