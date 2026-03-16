import os
from typing import Dict, List


EXT_GROUPS = {
    "python": {".py"},
    "web": {".js", ".ts", ".tsx", ".css", ".html"},
    "config": {".yml", ".yaml", ".json", ".toml", ".ini", ".env"},
}


def _group_for_file(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    for group, exts in EXT_GROUPS.items():
        if ext in exts:
            return group
    return "other"


def analyze_repository(root: str = ".") -> Dict:
    modules: Dict[str, int] = {}
    dependencies: List[str] = []
    test_files: List[str] = []
    debt_signals: List[str] = []

    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv", "node_modules"}]
        for file in files:
            path = os.path.join(current_root, file)
            group = _group_for_file(file)
            modules[group] = modules.get(group, 0) + 1

            lower = file.lower()
            if lower in {"requirements.txt", "pyproject.toml", "package.json", "poetry.lock"}:
                dependencies.append(path)
            if lower.startswith("test_") or lower.endswith("_test.py") or "/tests/" in path.replace("\\", "/"):
                test_files.append(path)
            if "todo" in lower or "fixme" in lower:
                debt_signals.append(path)

    missing_tests = modules.get("python", 0) > 0 and len(test_files) == 0

    return {
        "root": os.path.abspath(root),
        "modules": modules,
        "dependency_files": sorted(dependencies),
        "test_files": sorted(test_files),
        "missing_tests": missing_tests,
        "technical_debt_signals": sorted(debt_signals),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(analyze_repository("."), indent=2, ensure_ascii=False))
