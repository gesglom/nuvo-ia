import json
import os
from datetime import datetime

FILE = "memory/self_improvement.json"


def _ensure():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump({"suggestions": []}, f, indent=2, ensure_ascii=False)


def _load():
    _ensure()
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def register_feedback(agent: str, task: str, status: str, error: str = ""):
    if status == "done":
        return

    data = _load()
    suggestion = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent,
        "task": task,
        "status": status,
        "suggestion": "Agregar más validaciones de entrada y ejemplos concretos en el prompt.",
        "error_excerpt": (error or "")[:300],
    }
    data["suggestions"].append(suggestion)
    _save(data)


def list_suggestions(limit: int = 20):
    return _load().get("suggestions", [])[-limit:]
