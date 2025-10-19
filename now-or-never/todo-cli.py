"""
Simple To-Do CLI app
Features:
 - add <task title>
 - list
 - done <id>         (mark done)
 - delete <id>
 - clear
 - help
Tasks stored in tasks.json.
"""

import json
import sys
import uuid
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupt. Starting fresh.")
        return []


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def generate_unique_id(tasks):
    """Generate a UUID4 string that doesn't clash with existing IDs."""
    existing_ids = {t["id"] for t in tasks}
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id


def cmd_list(tasks):
    if not tasks:
        print("No tasks. Use: add <task description>")
        return
    print(f"{'ID':36}  {'Done':4}  {'Created':19}  Title")
    print("-" * 80)
    for t in tasks:
        done = "✔" if t.get("done") else " "
        created = t.get("created_at", "")
        print(f"{t['id']}  [{done}]   {created:19}  {t['title']}")


def cmd_add(tasks, title):
    title = title.strip()
    if not title:
        print("Cannot add empty task.")
        return
    t = {
        "id": generate_unique_id(tasks),
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(t)
    save_tasks(tasks)
    print(f"Added task: {t['title']} ({t['id']})")


def find_task(tasks, tid):
    for t in tasks:
        if t["id"] == tid:
            return t
    return None


def cmd_done(tasks, tid):
    t = find_task(tasks, tid)
    if not t:
        print(f"No task with id {tid}")
        return
    t["done"] = True
    save_tasks(tasks)
    print(f"Marked done: {t['title']} ({tid})")


def cmd_delete(tasks, tid):
    t = find_task(tasks, tid)
    if not t:
        print(f"No task with id {tid}")
        return
    tasks.remove(t)
    save_tasks(tasks)
    print(f"Deleted: {t['title']} ({tid})")


def cmd_clear(tasks):
    confirm = input("Delete ALL tasks? Type 'yes' to confirm: ")
    if confirm.lower() == "yes":
        tasks.clear()
        save_tasks(tasks)
        print("All tasks deleted.")
    else:
        print("Aborted.")


def print_help():
    print(__doc__)


def main(argv):
    tasks = load_tasks()

    if len(argv) <= 1:
        print_help()
        return

    cmd = argv[1].lower()

    if cmd == "list":
        cmd_list(tasks)
    elif cmd == "add":
        title = " ".join(argv[2:]) if len(argv) > 2 else input("Task title: ")
        cmd_add(tasks, title)
    elif cmd == "done":
        if len(argv) < 3:
            print("Usage: done <id>")
            return
        cmd_done(tasks, argv[2])
    elif cmd == "delete":
        if len(argv) < 3:
            print("Usage: delete <id>")
            return
        cmd_delete(tasks, argv[2])
    elif cmd == "clear":
        cmd_clear(tasks)
    elif cmd in ("help", "--help", "-h"):
        print_help()
    else:
        print(f"Unknown command: {cmd}")
        print_help()


if __name__ == "__main__":
    main(sys.argv)