import json
import os

MEMORY_FILE = "memory/project_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_completed_task(task):

    memory = load_memory()

    memory.setdefault("tasks_completed", []).append(task)

    save_memory(memory)
