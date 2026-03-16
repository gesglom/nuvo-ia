import os
import sys

sys.path.append(os.getcwd())

from core.agent_evolution import run_evolution_cycle
from core.job_queue import create_job, get_job
from core.memory_fabric import retrieve_context, store_episode
from core.metrics_manager import add_metric, summary
from core.self_improvement import register_feedback, list_suggestions
from core.task_contract import TaskContract
from core.tool_policy import can_write_path, is_command_allowed
from core.llm_client import ask_llm


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

    # Memoria unificada (local fallback)
    store_episode("architect_agent", "crear arquitectura", "resultado de prueba", status="completed")
    ctx = retrieve_context("arquitectura", agent="architect_agent", limit=3)
    assert isinstance(ctx, str)

    # Evolución de agentes
    evo = run_evolution_cycle(["architect_agent", "backend_engineer"])
    assert "agents" in evo

    # LLM localdev para arranque sin infraestructura externa
    response = ask_llm("responde algo", provider="localdev")
    assert isinstance(response, str) and len(response) > 0

    # Seguridad de herramientas
    assert can_write_path("workspace/nuvo_backend/main.py")
    assert not can_write_path("/etc/passwd")
    assert not is_command_allowed("rm -rf /")

    print("OK: runtime fases validado")


if __name__ == "__main__":
    main()
