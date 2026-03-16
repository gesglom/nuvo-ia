from core.agent_base import AgentBase, AgentResult


class DevOpsAgent(AgentBase):
    name = "devops_agent"

    def execute(self, task):
        plan = {
            "build": "docker build -t nuvo-factory .",
            "deploy": "docker compose up -d",
            "rollback": "docker compose down && docker compose up -d",
            "logs": "docker compose logs --tail=200",
        }
        return AgentResult(agent=self.name, status="planned", output="DevOps runbook generated", metadata=plan)
