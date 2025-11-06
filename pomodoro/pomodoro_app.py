# pomodoro_app.py
import tkinter as tk
from config import DEFAULTS, COLORS
from ui_components import add_hover_effect, format_time
from timer_logic import PomodoroTimer
from session_tracker import load_sessions

class PomodoroApp(tk.Tk):
    def __init__(self, durations=None):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("420x520")
        self.resizable(False, False)

        self.durations = durations or DEFAULTS.copy()
        self.mode = "Work"
        self.remaining_seconds = self.durations[self.mode]
        self.running = False
        self.session_count = load_sessions()["sessions_count"]

        self.timer = PomodoroTimer(self)
        self._build_ui()
        self.update_ui()

        self.bind("<space>", lambda e: self.toggle())
        self.bind("r", lambda e: self.restart())
        self.bind("s", lambda e: self.skip())

    # UI setup
    def _build_ui(self):
        self.mode_label = tk.Label(self, text=self.mode, font=("Segoe UI", 18, "bold"))
        self.mode_label.pack(pady=(18, 6))

        size = 320
        self.canvas = tk.Canvas(self, width=size, height=size, highlightthickness=0)
        self.canvas.pack(pady=(4, 6))
        self.center = size // 2
        r = int(size * 0.38)

        self.bg_circle = self.canvas.create_oval(
            self.center - r, self.center - r, self.center + r, self.center + r,
            fill="#ffffff", outline="#ddd", width=4
        )

        self.arc = self.canvas.create_arc(
            self.center - r, self.center - r, self.center + r, self.center + r,
            start=-90, extent=0, style="arc", outline="#FFFFFF", width=25
        )

        self.time_text = self.canvas.create_text(
            self.center, self.center - 10,
            text=format_time(self.remaining_seconds),
            font=("Segoe UI", 46, "bold"), fill="black", anchor="center"
        )

        self.sub_text = self.canvas.create_text(
            self.center, self.center + 34, text="", font=("Segoe UI", 10)
        )

        self.session_label = tk.Label(
            self, text=f"Work sessions completed: {self.session_count}",
            font=("Segoe UI", 10)
        )
        self.session_label.pack(pady=(6, 2))

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=18, pady=(6, 14))

        self.play_btn = tk.Button(btn_frame, text="► Play", width=10, command=self.toggle)
        self.restart_btn = tk.Button(btn_frame, text="↺ Restart", width=10, command=self.restart)
        self.skip_btn = tk.Button(btn_frame, text="⏭ Skip", width=10, command=self.skip)

        for b in (self.play_btn, self.restart_btn, self.skip_btn):
            b.pack(side="left", padx=(0, 8))
            add_hover_effect(b)

        tk.Label(self, text="Space: Play/Pause    r: Restart    s: Skip", font=("Segoe UI", 9), fg="#666").pack()

    # UI updates
    def update_ui(self):
        self.mode_label.config(text=self.mode)
        total = self.durations[self.mode]
        elapsed = total - self.remaining_seconds
        frac = elapsed / total if total > 0 else 0
        extent = 360 * frac
        color = COLORS.get(self.mode, "#FF6B6B")

        self.canvas.itemconfigure(self.arc, extent=extent, outline=color)
        self.canvas.itemconfigure(self.time_text, text=format_time(self.remaining_seconds))
        self.canvas.itemconfigure(self.sub_text, text="Running" if self.running else "Paused")
        self.session_label.config(text=f"Work sessions completed: {self.session_count}")
        self.play_btn.config(text="❚❚ Pause" if self.running else "► Play")

    # Event handlers
    def toggle(self):
        if self.running:
            self.timer.pause()
        else:
            self.timer.start()
        self.update_ui()

    def restart(self):
        self.timer.restart()
        self.update_ui()

    def skip(self):
        self.timer.skip()
        self.update_ui()
