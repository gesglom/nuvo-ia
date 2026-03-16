from typing import Any, Callable, Dict, List


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, fn: Callable[..., Any], capabilities: List[str] = None):
        self._tools[name] = fn
        self._metadata[name] = {"capabilities": capabilities or []}

    def get(self, name: str):
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def describe(self, name: str) -> Dict[str, Any]:
        return self._metadata.get(name, {})
