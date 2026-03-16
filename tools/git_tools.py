import subprocess
from typing import Dict


def _run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return {"cmd": " ".join(cmd), "code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}


def detect_changes() -> Dict:
    return _run(["git", "status", "--short"])


def stage_changes() -> Dict:
    return _run(["git", "add", "."])


def create_commit(message: str) -> Dict:
    return _run(["git", "commit", "-m", message])


def push_changes() -> Dict:
    return _run(["git", "push"])
