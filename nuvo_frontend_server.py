import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent_loop import run_job
from core.agent_loader import load_agents
from core.job_queue import create_job, get_job, list_jobs, retry_failed_tasks
from core.llm_client import provider_status
from core.metrics_manager import summary as metrics_summary
from core.self_improvement import list_suggestions
from core.task_contract import TaskContract
from core.tool_policy import policy_snapshot
from nuvo_orchestrator import crear_plan


FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")


class NuvoHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=HTTPStatus.OK):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_file(self, path, content_type):
        with open(path, "rb") as f:
            content = f.read()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            return self._send_file(os.path.join(FRONTEND_DIR, "index.html"), "text/html; charset=utf-8")
        if self.path == "/styles.css":
            return self._send_file(os.path.join(FRONTEND_DIR, "styles.css"), "text/css; charset=utf-8")
        if self.path == "/app.js":
            return self._send_file(os.path.join(FRONTEND_DIR, "app.js"), "application/javascript; charset=utf-8")

        if self.path == "/api/agents":
            return self._send_json({"agents": sorted(list(load_agents().keys()))})
        if self.path == "/api/providers":
            return self._send_json(provider_status())
        if self.path == "/api/jobs":
            return self._send_json({"jobs": list_jobs()})
        if self.path == "/api/metrics":
            return self._send_json(metrics_summary())
        if self.path == "/api/policy":
            return self._send_json(policy_snapshot())
        if self.path == "/api/self-improvement":
            return self._send_json({"suggestions": list_suggestions()})

        if self.path.startswith("/api/jobs/"):
            job_id = self.path.split("/api/jobs/")[-1]
            job = get_job(job_id)
            if not job:
                return self._send_json({"error": "job no encontrado"}, status=HTTPStatus.NOT_FOUND)
            return self._send_json(job)

        return self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self):
        if self.path == "/api/plan":
            body = self._read_json()
            goal = body.get("goal", "").strip()
            if not goal:
                return self._send_json({"error": "goal es requerido"}, status=HTTPStatus.BAD_REQUEST)
            plan = crear_plan(goal, load_agents())
            return self._send_json({"goal": goal, "plan": plan})

        if self.path == "/api/run-agent":
            body = self._read_json()
            name = body.get("agent", "").strip()
            task = body.get("task", "").strip()
            if not name or not task:
                return self._send_json({"error": "agent y task son requeridos"}, status=HTTPStatus.BAD_REQUEST)
            selected = load_agents().get(name)
            if not selected:
                return self._send_json({"error": f"Agente no encontrado: {name}"}, status=HTTPStatus.NOT_FOUND)
            return self._send_json({"agent": name, "task": task, "result": selected.execute(task)})

        if self.path == "/api/agents/smoke":
            body = self._read_json()
            smoke_goal = body.get("goal", "smoke test")
            results = []
            for name, agent in load_agents().items():
                try:
                    out = str(agent.execute(smoke_goal))[:200]
                    status = "ok"
                except Exception as exc:
                    out = str(exc)
                    status = "error"
                results.append({"agent": name, "status": status, "output_excerpt": out})
            return self._send_json({"results": results})

        if self.path == "/api/jobs":
            body = self._read_json()
            goal = body.get("goal", "").strip()
            if not goal:
                return self._send_json({"error": "goal es requerido"}, status=HTTPStatus.BAD_REQUEST)
            plan = create_plan(goal=goal, agents=load_agents())
            tasks = [TaskContract(owner_agent=a, input=goal) for a in plan]
            return self._send_json(create_job(goal, tasks), status=HTTPStatus.CREATED)

        if self.path.startswith("/api/jobs/") and self.path.endswith("/run"):
            job_id = self.path.replace("/api/jobs/", "").replace("/run", "")
            job = run_job(job_id)
            if not job:
                return self._send_json({"error": "job no encontrado"}, status=HTTPStatus.NOT_FOUND)
            return self._send_json(job)

        if self.path.startswith("/api/jobs/") and self.path.endswith("/retry"):
            job_id = self.path.replace("/api/jobs/", "").replace("/retry", "")
            job = retry_failed_tasks(job_id)
            if not job:
                return self._send_json({"error": "job no encontrado"}, status=HTTPStatus.NOT_FOUND)
            return self._send_json(job)

        return self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)


def create_plan(goal, agents):
    from project_leader import create_plan as planner

    return planner(goal, agents)


def main():
    parser = argparse.ArgumentParser(description="Nuvo Frontend Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), NuvoHandler)
    print(f"Nuvo frontend corriendo en http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
