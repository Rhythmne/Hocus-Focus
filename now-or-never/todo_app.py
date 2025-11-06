# todo_app.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from task_manager import load_tasks, save_tasks, add_task, delete_tasks
from ui_helpers import add_hover_effect, ask_edit_task, confirm_delete
from config import FONT_MAIN, COLOR_INFO, COLOR_DISABLED

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Now Or Never!")
        self.geometry("520x420")

        self.tasks = load_tasks()
        self.index_map = {}

        self._build_ui()
        self.refresh()

    # ---------------- UI ----------------
    def _build_ui(self):
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=(10, 10))

        self.entry = tk.Entry(input_frame)
        self.entry.pack(fill="x", pady=(0, 4))
        self.entry.bind("<Return>", lambda e: self.add_task())

        add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task)
        add_btn.pack(fill="x")
        add_hover_effect(add_btn)

        info_label = tk.Label(
            self,
            text="Please use Shift+Click and Ctrl+Click for multiple selections",
            font=FONT_MAIN,
            fg=COLOR_INFO,
        )
        info_label.pack(anchor="w", padx=10, pady=(4, 2))

        self.listbox = tk.Listbox(self, activestyle="none", selectmode="extended")
        self.listbox.pack(fill="both", expand=True, padx=10)
        self.listbox.bind("<Double-Button-1>", lambda e: self.toggle_done())
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.update_button_state())

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.edit_btn = tk.Button(
            btn_frame, text="Edit Task", command=self.edit_selected,
            state="disabled", disabledforeground=COLOR_DISABLED
        )
        self.edit_btn.pack(side="left", padx=(0, 6))
        add_hover_effect(self.edit_btn)

        self.delete_btn = tk.Button(
            btn_frame, text="Delete", command=self.delete_selected,
            state="disabled", disabledforeground=COLOR_DISABLED
        )
        self.delete_btn.pack(side="left", padx=(0, 6))
        add_hover_effect(self.delete_btn)

        clear_btn = tk.Button(btn_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side="right")
        add_hover_effect(clear_btn)

    # ---------------- Logic ----------------
    def refresh(self):
        """Refresh listbox and index mapping."""
        self.listbox.delete(0, tk.END)
        self.index_map.clear()
        for i, t in enumerate(sorted(self.tasks, key=lambda x: x["created_at"])):
            prefix = "✔ " if t.get("done") else "  "
            display = f"{prefix}{t['title']}"
            self.listbox.insert(tk.END, display)
            self.index_map[i] = t
        self.update_button_state()

    def update_button_state(self):
        """Enable/disable Edit/Delete based on selection."""
        sel = self.listbox.curselection()
        state = "normal" if sel else "disabled"
        self.edit_btn.config(state=state)
        self.delete_btn.config(state=state)

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            messagebox.showinfo("Empty", "Task title cannot be empty.")
            return
        add_task(self.tasks, title)
        self.entry.delete(0, tk.END)
        self.refresh()

    def toggle_done(self):
        """Toggle done status."""
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.index_map.get(idx)
        if task:
            task["done"] = not task.get("done", False)
            save_tasks(self.tasks)
            self.refresh()

    def edit_selected(self):
        """Edit selected task title."""
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.index_map.get(idx)
        if not task:
            return
        new_title = ask_edit_task(task["title"])
        if new_title and new_title.strip():
            task["title"] = new_title.strip()
            save_tasks(self.tasks)
            self.refresh()

    def delete_selected(self):
        """Delete selected tasks (multi-select supported)."""
        sel = self.listbox.curselection()
        if not sel:
            return
        if not confirm_delete(len(sel)):
            return
        to_delete = [self.index_map[i] for i in sel if i in self.index_map]
        delete_tasks(self.tasks, to_delete)
        self.refresh()

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.refresh()
