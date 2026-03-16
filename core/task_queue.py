from typing import Dict, List, Optional

from core.job_queue import create_job, get_job, next_pending_task, update_task
from core.task_contract import TaskContract


class TaskQueue:
    """Compatibility layer over current persistent job_queue backend."""

    def create(self, goal: str, tasks: List[TaskContract]) -> Dict:
        return create_job(goal, tasks)

    def get(self, job_id: str) -> Optional[Dict]:
        return get_job(job_id)

    def next_task(self, job_id: str) -> Optional[TaskContract]:
        return next_pending_task(job_id)

    def update(self, job_id: str, task: TaskContract):
        return update_task(job_id, task)
