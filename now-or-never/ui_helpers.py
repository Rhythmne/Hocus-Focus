# ui_helpers.py
import tkinter as tk
from tkinter import messagebox, simpledialog

def add_hover_effect(widget, hover_bg="#BFBFBF", normal_bg=None):
    """Add simple hover color effect to buttons."""
    if normal_bg is None:
        try:
            normal_bg = widget.cget("background")
        except tk.TclError:
            normal_bg = "#f0f0f0"

    def on_enter(e):
        if widget.cget("state") != "disabled":
            widget.config(background=hover_bg)

    def on_leave(e):
        if widget.cget("state") != "disabled":
            widget.config(background=normal_bg)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def ask_edit_task(old_title):
    """Prompt user to edit task title."""
    return simpledialog.askstring("Edit Task", "Update task:", initialvalue=old_title)

def confirm_delete(count):
    """Confirm multiple task deletion."""
    return messagebox.askyesno("Confirm Delete", f"Delete {count} selected task(s)?")
