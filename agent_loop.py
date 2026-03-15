import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from core.agent_loader import load_agents
from core.context_manager import add_context_event
from core.job_queue import create_job, get_job, next_pending_task, update_task
from core.metrics_manager import add_metric
from core.self_improvement import register_feedback
from core.task_contract import TaskContract
from project_leader import create_plan

MAX_RETRIES = 2
TASK_TIMEOUT_SECONDS = 120


def _build_tasks(goal, plan):
    tasks = []
    for step in plan:
        tasks.append(
            TaskContract(
                owner_agent=step,
                input=goal,
                expected_output=f"Salida útil del agente {step} para avanzar objetivo",
            )
        )
    return tasks


def _invoke_specialist(agents, failed_task, error_message):
    creator = agents.get("agent_creator")
    if not creator:
        return None

    specialty = f"especialista_{failed_task.input[:40]}"
    created = creator.execute(specialty)

    agents = load_agents()
    new_agent_name = created.get("agent") if isinstance(created, dict) else None
    specialist = agents.get(new_agent_name) if new_agent_name else None

    if specialist:
        start = time.perf_counter()
        result = specialist.execute(
            f"Resolver bloqueo en tarea '{failed_task.input}'. Error previo: {error_message}"
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        add_context_event(new_agent_name, failed_task.input, str(result), status="recovered")
        add_metric(new_agent_name, "dynamic", "done", latency_ms)
        return new_agent_name, result

    return None


def run_job(job_id):
    agents = load_agents()

    while True:
        task = next_pending_task(job_id)
        if not task:
            break

        selected = agents.get(task.owner_agent)
        if not selected:
            task.status = "failed"
            task.error = f"Agente no encontrado: {task.owner_agent}"
            update_task(job_id, task)
            register_feedback(task.owner_agent, task.input, "failed", task.error)
            continue

        start = time.perf_counter()
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(selected.execute, task.input)
                result = future.result(timeout=TASK_TIMEOUT_SECONDS)

            task.output = str(result)
            task.status = "done"
            task.error = ""
            add_context_event(task.owner_agent, task.input, task.output, status="completed")
        except TimeoutError:
            task.retries += 1
            task.error = f"timeout después de {TASK_TIMEOUT_SECONDS}s"
            task.status = "pending" if task.retries <= MAX_RETRIES else "failed"
        except Exception as exc:
            task.retries += 1
            task.error = str(exc)
            task.status = "pending" if task.retries <= MAX_RETRIES else "failed"

        task.updated_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        task.latency_ms = int((time.perf_counter() - start) * 1000)
        add_metric(task.owner_agent, "routed", "done" if task.status == "done" else "failed", task.latency_ms)

        if task.status == "failed":
            register_feedback(task.owner_agent, task.input, "failed", task.error)
            recovery = _invoke_specialist(agents, task, task.error)
            if recovery:
                task.output = f"Recovered by {recovery[0]}"

        update_task(job_id, task)

    return get_job(job_id)


def start_nuvo_flow(goal):
    print(f"🚀 Iniciando misión Nuvo (fábrica autónoma): {goal}")

    agents = load_agents()
    plan = create_plan(goal, agents)

    tasks = _build_tasks(goal, plan)
    job = create_job(goal, tasks)
    final_job = run_job(job["job_id"])

    print(f"🏁 Flujo finalizado. job_id={job['job_id']} status={final_job.get('status')}")
    return final_job


if __name__ == "__main__":
    objetivo = input("¿Qué parte de Nuvo crearemos con auto-mejora activa?: ")
    start_nuvo_flow(objetivo)
