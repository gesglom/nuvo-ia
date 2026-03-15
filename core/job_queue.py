import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from core.task_contract import TaskContract

JOBS_FILE = "memory/jobs.json"


def _ensure():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump({"jobs": []}, f, indent=2, ensure_ascii=False)


def _load() -> Dict:
    _ensure()
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: Dict):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_job(goal: str, tasks: List[TaskContract]) -> Dict:
    data = _load()
    job = {
        "job_id": f"job_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
        "goal": goal,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "tasks": [t.to_dict() for t in tasks],
    }
    data["jobs"].append(job)
    _save(data)
    return job


def list_jobs() -> List[Dict]:
    return _load().get("jobs", [])


def get_job(job_id: str) -> Optional[Dict]:
    for job in list_jobs():
        if job.get("job_id") == job_id:
            return job
    return None


def _recompute_status(job):
    statuses = {x.get("status") for x in job.get("tasks", [])}
    if statuses == {"done"}:
        job["status"] = "done"
    elif "failed" in statuses:
        job["status"] = "failed"
    elif "running" in statuses:
        job["status"] = "running"
    else:
        job["status"] = "pending"


def _update_job(job_id: str, updater):
    data = _load()
    for idx, job in enumerate(data.get("jobs", [])):
        if job.get("job_id") == job_id:
            updater(job)
            _recompute_status(job)
            job["updated_at"] = datetime.utcnow().isoformat()
            data["jobs"][idx] = job
            _save(data)
            return job
    return None


def next_pending_task(job_id: str) -> Optional[TaskContract]:
    def updater(job):
        for t in job.get("tasks", []):
            if t.get("status") == "pending":
                t["status"] = "running"
                t["updated_at"] = datetime.utcnow().isoformat()
                job["__picked_task"] = t
                break

    job = _update_job(job_id, updater)
    if not job:
        return None
    picked = job.get("__picked_task")
    if not picked:
        return None
    return TaskContract.from_dict(picked)


def update_task(job_id: str, task: TaskContract):
    def updater(job):
        for i, t in enumerate(job.get("tasks", [])):
            if t.get("task_id") == task.task_id:
                job["tasks"][i] = task.to_dict()
                break

    return _update_job(job_id, updater)


def retry_failed_tasks(job_id: str):
    def updater(job):
        for t in job.get("tasks", []):
            if t.get("status") == "failed":
                t["status"] = "pending"
                t["error"] = ""
                t["updated_at"] = datetime.utcnow().isoformat()

    return _update_job(job_id, updater)
