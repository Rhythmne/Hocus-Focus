"""
To-Do GUI (UUID version)
Features:
 - Add task via entry box
 - Double-click to toggle done
 - Delete selected
 - Clear all
 - Saves to tasks.json
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def generate_unique_id(tasks):
    existing_ids = {t["id"] for t in tasks}
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id
        


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Now Or Never!")
        self.geometry("520x420")
        self.tasks = load_tasks()

        # --- Input section ---
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=(10, 10))

        self.entry = tk.Entry(input_frame)
        self.entry.pack(fill="x", pady=(0, 4))
        self.entry.bind("<Return>", lambda e: self.add_task())

        add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task)
        add_btn.pack(fill="x")  # <-- makes button same width as the entry

        # --- Instruction label ---
        info_label = tk.Label(
            self,
            text="Please use Shift+Click and Ctrl+Click for multiple selections",
            font=("Segoe UI", 12),
            fg="#BFBFBF"  # light gray color
        )
        info_label.pack(anchor="w", padx=10, pady=(4, 2))

        # --- Task list ---
        self.listbox = tk.Listbox(self, activestyle="none", selectmode="extended")
        self.listbox.pack(fill="both", expand=True, padx=10)
        self.listbox.bind("<Double-Button-1>", lambda e: self.toggle_done())

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.edit_btn = tk.Button(btn_frame, text="Edit Task", command=self.edit_selected, state="disabled", disabledforeground="#EFEFEF")
        self.edit_btn.pack(side="left", padx=(0, 6))

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_selected, state="disabled", disabledforeground="#EFEFEF")
        self.delete_btn.pack(side="left")

        clear_btn = tk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side="right")

        self.listbox.bind("<<ListboxSelect>>", lambda e: self.update_button_state())

        # NEW: keep index→task mapping
        self.index_map = {}

        self.refresh()

    def refresh(self):
        """Refresh listbox display and rebuild index mapping."""
        self.listbox.delete(0, tk.END)
        self.index_map.clear()
        for i, t in enumerate(sorted(self.tasks, key=lambda x: x["created_at"])):
            prefix = "✔ " if t.get("done") else "  "
            display = f"{prefix}{t['title']}"
            self.listbox.insert(tk.END, display)
            self.index_map[i] = t  # map listbox index to task object
        self.update_button_state()

    def update_button_state(self):
        """Enable or disable Edit/Delete buttons based on selection."""
        sel = self.listbox.curselection()
        if sel:
            self.delete_btn.config(state="normal")
            self.edit_btn.config(state="normal")
        else:
            self.delete_btn.config(state="disabled")
            self.edit_btn.config(state="disabled")

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            messagebox.showinfo("Empty", "Task title cannot be empty.")
            return
        t = {
            "id": generate_unique_id(self.tasks),
            "title": title,
            "done": False,
            "created_at": datetime.now().isoformat(),
        }
        self.tasks.append(t)
        save_tasks(self.tasks)
        self.entry.delete(0, tk.END)
        self.refresh()

    def toggle_done(self):
        """Toggle the 'done' state for the selected task (by object reference)."""
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.index_map.get(idx)
        if not task:
            return
        task["done"] = not task.get("done", False)
        save_tasks(self.tasks)
        self.refresh()

    def edit_selected(self):
        """Edit the title of the selected task without changing its creation time or ID."""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Edit Task", "Please select a task to edit.")
            return

        idx = sel[0]
        task = self.index_map.get(idx)
        if not task:
            return

        # Ask for new title (pre-filled with old one)
        new_title = simpledialog.askstring(
            "Edit Task", "Update task:", initialvalue=task["title"]
        )

        # Only update if user entered something valid
        if new_title and new_title.strip():
            task["title"] = new_title.strip()

            # ✅ DO NOT update created_at or ID
            # They stay the same to preserve task identity

            save_tasks(self.tasks)
            self.refresh()


    def delete_selected(self):
        """Delete all selected tasks (supports multi-select)."""
        sel = self.listbox.curselection()
        if not sel:
            return

        # Confirm deletion (optional)
        confirm = tk.messagebox.askyesno(
            "Confirm Delete", f"Delete {len(sel)} selected task(s)?"
        )
        if not confirm:
            return

        # Collect tasks to remove
        to_delete = [self.index_map[i] for i in sel if i in self.index_map]

        # Remove them from the main list
        self.tasks = [t for t in self.tasks if t not in to_delete]

        save_tasks(self.tasks)
        self.refresh()


    def clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.refresh()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()