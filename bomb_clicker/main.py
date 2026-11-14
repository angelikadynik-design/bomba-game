import tkinter as tk
from tkinter import messagebox


class BombClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bomb Clicker")
        self.root.geometry("420x500")
        self.root.resizable(False, False)

        self.target_clicks = 30
        self.time_limit = 10
        self.clicks_made = 0
        self.time_left = self.time_limit
        self.game_running = False
        self.timer_id = None

        self.main_frame = tk.Frame(root, padx=20, pady=20, bg="#f3f3f3")
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.main_frame,
            text="Defuse the Bomb",
            font=("Arial", 20, "bold"),
            bg="#f3f3f3",
        )
        self.title_label.pack(pady=(10, 5))

        self.timer_label = tk.Label(
            self.main_frame,
            text="Time: 10",
            font=("Arial", 18),
            fg="#1c1c1c",
            bg="#f3f3f3",
        )
        self.timer_label.pack()

        self.clicks_label = tk.Label(
            self.main_frame,
            text="Remaining clicks: 30",
            font=("Arial", 18),
            fg="#1c1c1c",
            bg="#f3f3f3",
        )
        self.clicks_label.pack(pady=(5, 15))

        self.bomb_button = tk.Button(
            self.main_frame,
            text="💣",
            font=("Arial", 60),
            width=4,
            height=2,
            command=self.handle_click,
            bg="#d9534f",
            fg="white",
            relief="raised",
            bd=3,
        )
        self.bomb_button.pack(pady=10)

        self.result_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 20, "bold"),
            fg="#2d2d2d",
            bg="#f3f3f3",
        )
        self.result_label.pack(pady=10)

        self.restart_button = tk.Button(
            self.main_frame,
            text="Restart",
            command=self.restart_game,
            font=("Arial", 12, "bold"),
            bg="#5cb85c",
            fg="white",
            padx=12,
            pady=6,
        )
        self.restart_button.pack(pady=10)

        self.restart_game()

    def update_labels(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        remaining_clicks = max(0, self.target_clicks - self.clicks_made)
        self.clicks_label.config(text=f"Remaining clicks: {remaining_clicks}")

    def start_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(1000, self.tick)

    def tick(self):
        if not self.game_running:
            return

        self.time_left -= 1
        self.update_labels()

        if self.time_left <= 0:
            self.end_game(False)
            return

        self.timer_id = self.root.after(1000, self.tick)

    def handle_click(self):
        if not self.game_running:
            return

        self.clicks_made += 1
        self.update_labels()

        if self.clicks_made >= self.target_clicks:
            self.end_game(True)

    def end_game(self, won):
        self.game_running = False
        self.bomb_button.config(state="disabled")

        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if won:
            self.result_label.config(text="Bomb defused!", fg="#2ca02c")
        else:
            self.result_label.config(text="BOOM!", fg="#d62728")

    def restart_game(self):
        self.clicks_made = 0
        self.time_left = self.time_limit
        self.game_running = True
        self.result_label.config(text="")
        self.bomb_button.config(state="normal")
        self.update_labels()
        self.start_timer()


if __name__ == "__main__":
    root = tk.Tk()
    app = BombClickerApp(root)
    root.mainloop()

