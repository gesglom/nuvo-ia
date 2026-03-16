import os
import subprocess
import tempfile
from typing import Dict

from core.memory_adapter import MemoryAdapter
from tools.repo_analyzer import analyze_repository


def ingest_repository(repo_url: str, branch: str = "main") -> Dict:
    memory = MemoryAdapter()

    with tempfile.TemporaryDirectory(prefix="nuvo_repo_ingest_") as tmp:
        target = os.path.join(tmp, "repo")
        clone = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", branch, repo_url, target],
            capture_output=True,
            text=True,
            check=False,
        )
        if clone.returncode != 0:
            return {
                "status": "error",
                "error": clone.stderr.strip() or clone.stdout.strip(),
                "repo_url": repo_url,
            }

        report = analyze_repository(target)
        summary = (
            f"Repository: {repo_url}\n"
            f"Modules: {report['modules']}\n"
            f"Dependency files: {len(report['dependency_files'])}\n"
            f"Missing tests: {report['missing_tests']}\n"
            f"Debt signals: {len(report['technical_debt_signals'])}"
        )
        memory.store_repository_insight(repository=repo_url, insight=summary, metadata={"branch": branch})

        return {"status": "ok", "repo_url": repo_url, "report": report}
