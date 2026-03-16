from typing import Any, Dict, List, Optional


class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.capabilities: Dict[str, List[str]] = {}

    def register(self, name: str, agent: Any, capabilities: Optional[List[str]] = None):
        self.agents[name] = agent
        self.capabilities[name] = list(capabilities or [])

    def unregister(self, name: str):
        self.agents.pop(name, None)
        self.capabilities.pop(name, None)

    def get(self, name: str):
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        return list(self.agents.keys())

    def find_by_capability(self, capability: str) -> List[str]:
        return [name for name, caps in self.capabilities.items() if capability in caps]
