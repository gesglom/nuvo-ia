from core.agent_base import AgentBase, AgentResult
from core.provider_router import route_llm


class PlannerAgent(AgentBase):
    name = "planner_agent"

    def execute(self, task):
        goal = task.get("goal") if isinstance(task, dict) else str(task)
        context = self.memory.retrieve_relevant_memories(goal, agent=self.name, limit=6)
        prompt = f"""
You are a planning agent for an autonomous software factory.
Create an execution plan with phases: planning, implementation, testing, review, commit, deployment, monitoring, improvement.
Return concise actionable bullets in Spanish.

Goal:
{goal}

Memory context:
{context}
"""
        plan = route_llm(self.name, prompt)
        return AgentResult(agent=self.name, status="done", output=str(plan), metadata={"goal": goal})
