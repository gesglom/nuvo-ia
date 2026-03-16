from core.agent_base import AgentBase, AgentResult
from core.self_improvement import list_suggestions


class SelfImprovementAgent(AgentBase):
    name = "self_improvement_agent"

    def execute(self, task):
        suggestions = list_suggestions(limit=20)
        top = suggestions[-5:]
        proposal = "\n".join([f"- {x.get('agent')}: {x.get('suggestion')}" for x in top]) or "- Sin sugerencias nuevas"
        self.memory.persist_system_improvement(proposal, agent=self.name)
        return AgentResult(agent=self.name, status="done", output=proposal)
