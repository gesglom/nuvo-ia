import os
import sys

sys.path.append(os.getcwd())

from core.job_queue import create_job, get_job
from core.metrics_manager import add_metric, summary
from core.self_improvement import register_feedback, list_suggestions
from core.task_contract import TaskContract
from core.tool_policy import can_write_path, is_command_allowed


def main():
    # Task contract + queue
    t1 = TaskContract(owner_agent="architect_agent", input="crear arquitectura")
    t2 = TaskContract(owner_agent="backend_engineer", input="crear api")
    job = create_job("crear app", [t1, t2])
    loaded = get_job(job["job_id"])
    assert loaded is not None and len(loaded["tasks"]) == 2

    # Observabilidad
    add_metric("architect_agent", "ollama", "done", 123)
    s = summary()
    assert s["total_events"] >= 1

    # Automejora supervisada
    register_feedback("backend_engineer", "crear api", "failed", "error de timeout")
    suggestions = list_suggestions()
    assert len(suggestions) >= 1

    # Seguridad de herramientas
    assert can_write_path("workspace/nuvo_backend/main.py")
    assert not can_write_path("/etc/passwd")
    assert not is_command_allowed("rm -rf /")

    print("OK: runtime fases validado")


if __name__ == "__main__":
    main()
