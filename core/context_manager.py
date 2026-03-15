import json
import os
from datetime import datetime

CONTEXT_FILE = "memory/shared_context.json"


def _ensure_storage():
    os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
    if not os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
            json.dump({"events": []}, f, indent=2, ensure_ascii=False)


def load_context():
    _ensure_storage()
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_context_event(agent: str, task: str, result: str, status: str = "completed"):
    data = load_context()
    data.setdefault("events", []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "task": task,
            "status": status,
            "result": (result or "")[:2000],
        }
    )
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def summarize_recent(limit: int = 8):
    data = load_context()
    events = data.get("events", [])[-limit:]
    lines = []
    for item in events:
        lines.append(
            f"[{item.get('timestamp')}] {item.get('agent')} | {item.get('status')} | {item.get('task')}"
        )
    return "\n".join(lines)
