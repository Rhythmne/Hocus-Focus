# timer_logic.py
import platform
import tkinter as tk
from config import WORK_SESSIONS_PER_LONG_BREAK

class PomodoroTimer:
    """Logic-only component to control time countdown and mode transitions."""
    def __init__(self, app):
        self.app = app  # reference to PomodoroApp for UI updates
        self.timer_job = None

    def start(self):
        self.app.running = True
        self._schedule_tick()

    def pause(self):
        self.app.running = False
        if self.timer_job:
            self.app.after_cancel(self.timer_job)
            self.timer_job = None

    def restart(self):
        self.app.remaining_seconds = self.app.durations[self.app.mode]
        if self.timer_job:
            self.app.after_cancel(self.timer_job)
            self.timer_job = None
        if self.app.running:
            self._schedule_tick()

    def skip(self):
        if self.timer_job:
            self.app.after_cancel(self.timer_job)
            self.timer_job = None
        self._on_mode_complete()

    def _schedule_tick(self):
        self.timer_job = self.app.after(1000, self._tick)

    def _tick(self):
        if not self.app.running:
            return
        self.app.remaining_seconds -= 1
        if self.app.remaining_seconds <= 0:
            self._on_mode_complete()
        else:
            self.app.update_ui()
            self._schedule_tick()

    def _on_mode_complete(self):
        prev_mode = self.app.mode

        if prev_mode == "Work":
            self.app.session_count += 1
            from session_tracker import increment_session
            increment_session()
            if self.app.session_count % WORK_SESSIONS_PER_LONG_BREAK == 0:
                next_mode = "Long Break"
            else:
                next_mode = "Short Break"
        else:
            next_mode = "Work"

        self.app.mode = next_mode
        self.app.remaining_seconds = self.app.durations[self.app.mode]
        self._notify_mode_change(prev_mode, next_mode)
        self.app.update_ui()

        if self.app.running:
            self._schedule_tick()

    def _notify_mode_change(self, prev_mode, next_mode):
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            else:
                self.app.bell()
        except Exception:
            pass
