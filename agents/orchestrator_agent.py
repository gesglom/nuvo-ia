from typing import Dict, List

from core.agent_base import AgentBase, AgentResult
from core.agent_registry import AgentRegistry
from core.event_bus import EventBus
from core.task_contract import TaskContract
from core.task_queue import TaskQueue


class OrchestratorAgent(AgentBase):
    name = "orchestrator_agent"

    def __init__(self, registry: AgentRegistry = None, queue: TaskQueue = None, bus: EventBus = None):
        super().__init__()
        self.registry = registry or AgentRegistry()
        self.queue = queue or TaskQueue()
        self.bus = bus or EventBus()

    def execute(self, task: Dict):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        phases = task.get("phases") if isinstance(task, dict) else None
        phases = phases or [
            "planner_agent",
            "developer_agent",
            "tester_agent",
            "reviewer_agent",
            "git_agent",
            "devops_agent",
            "monitoring_agent",
            "self_improvement_agent",
        ]

        contracts: List[TaskContract] = [
            TaskContract(owner_agent=phase, input=goal, expected_output=f"Output from {phase}", priority=idx)
            for idx, phase in enumerate(phases)
        ]
        job = self.queue.create(goal, contracts)
        self.bus.publish("goal.received", {"goal": goal, "job_id": job["job_id"]})

        self.memory.store_agent_knowledge(self.name, "autonomous_loop", f"Created job {job['job_id']} for goal: {goal}")
        return AgentResult(agent=self.name, status="planned", output=f"job_id={job['job_id']}", metadata={"phases": phases})
