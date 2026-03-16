from core.agent_base import AgentBase, AgentResult
from core.provider_router import route_llm


class TesterAgent(AgentBase):
    name = "tester_agent"

    def execute(self, task):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        prompt = f"Diseña estrategia de pruebas para: {goal}. Incluye unitarias, integración y regresión."
        out = route_llm(self.name, prompt)
        return AgentResult(agent=self.name, status="done", output=str(out))
