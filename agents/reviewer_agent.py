from core.agent_base import AgentBase, AgentResult
from core.provider_router import route_llm


class ReviewerAgent(AgentBase):
    name = "reviewer_agent"

    def execute(self, task):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        prompt = f"Revisa calidad técnica, seguridad y mantenibilidad para: {goal}. Devuelve hallazgos y acciones."
        out = route_llm(self.name, prompt)
        return AgentResult(agent=self.name, status="done", output=str(out))
