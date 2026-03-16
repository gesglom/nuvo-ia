import os
import sys

sys.path.append(os.getcwd())

from core.agent_catalog import dedupe_agent_plan
from core.agent_evolution import run_evolution_cycle
from core.agent_registry import AgentRegistry
from core.event_bus import EventBus
from core.task_queue import TaskQueue
from tools.repo_analyzer import analyze_repository
from core.job_queue import create_job, get_job
from core.memory_fabric import retrieve_context, store_episode
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

    # Memoria unificada (local fallback)
    store_episode("architect_agent", "crear arquitectura", "resultado de prueba", status="completed")
    ctx = retrieve_context("arquitectura", agent="architect_agent", limit=3)
    assert isinstance(ctx, str)

    # Evolución de agentes
    evo = run_evolution_cycle(["architect_agent", "backend_engineer"])
    assert "agents" in evo

    # Catálogo de agentes: normalización/deduplicación ES-EN
    deduped = dedupe_agent_plan(["architect_agent", "arquitecto", "backend_engineer", "ingeniero_backend"])
    assert deduped == ["architect_agent", "backend_engineer"]

    # Framework core incremental
    registry = AgentRegistry()
    registry.register("dummy", object(), capabilities=["test"])
    assert "dummy" in registry.find_by_capability("test")

    bus = EventBus()
    state = {"ok": False}
    bus.subscribe("ping", lambda payload: state.update({"ok": payload.get("ok", False)}))
    bus.publish("ping", {"ok": True})
    assert state["ok"] is True

    q = TaskQueue()
    assert q.get(job["job_id"]) is not None

    repo_report = analyze_repository(".")
    assert "modules" in repo_report

    # Seguridad de herramientas
    assert can_write_path("workspace/nuvo_backend/main.py")
    assert not can_write_path("/etc/passwd")
    assert not is_command_allowed("rm -rf /")

    print("OK: runtime fases validado")


if __name__ == "__main__":
    main()
