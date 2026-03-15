import os

DEFAULT_WRITE_ROOTS = ["workspace", "memory", "agents", "agents/manifests"]
BLOCKED_COMMANDS = ["rm -rf /", "shutdown", "mkfs", "dd if="]


def can_write_path(path: str):
    norm = path.replace("\\", "/").lstrip("./")
    return any(norm.startswith(root) for root in DEFAULT_WRITE_ROOTS)


def is_command_allowed(command: str):
    lowered = command.lower()
    return not any(block in lowered for block in BLOCKED_COMMANDS)


def enforce_write_path(path: str):
    if not can_write_path(path):
        raise PermissionError(f"Path no permitida por policy: {path}")


def enforce_command(command: str):
    if not is_command_allowed(command):
        raise PermissionError(f"Comando bloqueado por policy: {command}")


def policy_snapshot():
    return {
        "allowed_write_roots": DEFAULT_WRITE_ROOTS,
        "blocked_command_patterns": BLOCKED_COMMANDS,
        "cwd": os.getcwd(),
    }
