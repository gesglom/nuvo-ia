import json
import os
from datetime import datetime

MANIFEST_DIR = "agents/manifests"
REQUIRED_FIELDS = [
    "role",
    "goal",
    "backstory",
    "tools_required",
    "provider_preference",
]


def ensure_manifest_dir():
    os.makedirs(MANIFEST_DIR, exist_ok=True)


def validate_manifest(manifest: dict):
    missing = [field for field in REQUIRED_FIELDS if field not in manifest]
    if missing:
        raise ValueError(f"Manifest incompleto. Faltan: {', '.join(missing)}")
    if not isinstance(manifest.get("tools_required"), list):
        raise ValueError("tools_required debe ser una lista")


def write_manifest(agent_module_name: str, manifest: dict):
    ensure_manifest_dir()
    validate_manifest(manifest)
    manifest = {**manifest, "updated_at": datetime.utcnow().isoformat()}
    path = os.path.join(MANIFEST_DIR, f"{agent_module_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return path


def load_manifest(agent_module_name: str):
    path = os.path.join(MANIFEST_DIR, f"{agent_module_name}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
