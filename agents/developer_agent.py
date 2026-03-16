from core.agent_base import AgentBase, AgentResult
from core.provider_router import route_llm


class DeveloperAgent(AgentBase):
    name = "developer_agent"

    def execute(self, task):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        context = self.memory.retrieve_relevant_memories(goal, agent=self.name, limit=6)
        prompt = f"Implementa cambios de código para este objetivo y devuelve pasos concretos:\n{goal}\n\nContexto:\n{context}"
        out = route_llm(self.name, prompt)
        return AgentResult(agent=self.name, status="done", output=str(out), metadata={"goal": goal})
