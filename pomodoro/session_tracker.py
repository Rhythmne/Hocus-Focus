import json
from datetime import datetime
from pathlib import Path

SESSIONS_FILE = Path("sessions.json")


def load_sessions():
    """Load session data from JSON, or initialize a new one if not found or outdated."""
    if not SESSIONS_FILE.exists():
        data = _init_new_day()
        save_sessions(data)
        return data

    try:
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = _init_new_day()

    today = datetime.now().strftime("%d/%m/%Y")
    if data.get("created") != today:
        data = _init_new_day()
        save_sessions(data)

    return data


def save_sessions(data):
    """Save session data safely to the JSON file."""
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def increment_session():
    """Increment session count and update hours after a work session completes."""
    data = load_sessions()
    data["sessions_count"] += 1
    data["hours"] = round(data["sessions_count"] / 3, 2)
    save_sessions(data)
    return data


def _init_new_day():
    """Initialize a fresh session record for the current date."""
    today = datetime.now().strftime("%d/%m/%Y")
    return {"created": today, "sessions_count": 0, "hours": 0}
