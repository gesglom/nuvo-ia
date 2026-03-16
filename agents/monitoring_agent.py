from core.agent_base import AgentBase, AgentResult
from core.metrics_manager import summary


class MonitoringAgent(AgentBase):
    name = "monitoring_agent"

    def execute(self, task):
        metrics = summary()
        return AgentResult(agent=self.name, status="done", output="Monitoring snapshot", metadata=metrics)
