from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from core.base_agent import BaseAgent
from core.memory_adapter import MemoryAdapter


@dataclass
class AgentResult:
    agent: str
    status: str
    output: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentBase(BaseAgent):
    """Forward-compatible base class for advanced agents.

    Keeps compatibility with legacy loader by inheriting from BaseAgent.
    """

    name = "agent_base"

    def __init__(self, memory: Optional[MemoryAdapter] = None):
        self.memory = memory or MemoryAdapter()

    def run(self, task: Dict[str, Any]) -> AgentResult:
        payload = self.execute(task)
        if isinstance(payload, AgentResult):
            return payload
        return AgentResult(agent=self.name, status="done", output=str(payload), metadata={"task": task})
