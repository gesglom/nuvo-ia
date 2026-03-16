from typing import Any, Dict, List, Optional

from core.memory_fabric import retrieve_context, store_episode


class MemoryAdapter:
    """Engram-oriented memory interface wrapper.

    Backed by memory_fabric, which can route to Engram when configured.
    """

    def store_agent_knowledge(self, agent: str, topic: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        store_episode(
            agent=agent,
            task=f"knowledge:{topic}",
            result=content,
            status="knowledge",
            metadata=metadata or {},
        )

    def retrieve_relevant_memories(self, query: str, agent: Optional[str] = None, limit: int = 8) -> str:
        return retrieve_context(query=query, agent=agent, limit=limit)

    def save_architectural_decision(self, title: str, decision: str, rationale: str, agent: str = "architect_agent"):
        payload = f"ADR: {title}\nDecision: {decision}\nRationale: {rationale}"
        store_episode(agent=agent, task=f"adr:{title}", result=payload, status="architectural_decision")

    def persist_system_improvement(self, improvement: str, agent: str = "self_improvement_agent"):
        store_episode(agent=agent, task="system_improvement", result=improvement, status="improvement")

    def store_repository_insight(self, repository: str, insight: str, metadata: Optional[Dict[str, Any]] = None):
        store_episode(
            agent="repository_engineer_agent",
            task=f"repo_insight:{repository}",
            result=insight,
            status="repository_insight",
            metadata=metadata or {},
        )
