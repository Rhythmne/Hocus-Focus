# ui_components.py
import tkinter as tk
from datetime import timedelta

def add_hover_effect(button, hover_bg="#BFBFBF", normal_bg=None):
    """Adds hover effect to a tk.Button."""
    if button is None:
        return

    if normal_bg is None:
        try:
            normal_bg = button.cget("background")
        except tk.TclError:
            normal_bg = "#f0f0f0"

    def on_enter(e):
        if button.cget("state") != "disabled":
            button.config(background=hover_bg)

    def on_leave(e):
        if button.cget("state") != "disabled":
            button.config(background=normal_bg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def format_time(seconds):
    td = timedelta(seconds=max(0, int(seconds)))
    mm, ss = divmod(td.seconds, 60)
    return f"{mm:02d}:{ss:02d}"
