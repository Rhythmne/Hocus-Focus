# task_manager.py
import json
import uuid
from datetime import datetime
from config import DATA_FILE

def load_tasks():
    """Load tasks from JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save task list to JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def generate_unique_id(tasks):
    """Generate a new UUID that doesn’t clash with existing IDs."""
    existing_ids = {t["id"] for t in tasks}
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            return new_id

def add_task(tasks, title):
    """Create and append a new task."""
    t = {
        "id": generate_unique_id(tasks),
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(t)
    save_tasks(tasks)

def delete_tasks(tasks, to_delete):
    """Remove selected tasks from the list."""
    tasks[:] = [t for t in tasks if t not in to_delete]
    save_tasks(tasks)
