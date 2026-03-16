from core.agent_base import AgentBase, AgentResult
from core.provider_router import route_llm


class RefactorAgent(AgentBase):
    name = "refactor_agent"

    def execute(self, task):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        prompt = f"Propón y prioriza refactors incrementales para: {goal}."
        out = route_llm(self.name, prompt)
        return AgentResult(agent=self.name, status="done", output=str(out))
