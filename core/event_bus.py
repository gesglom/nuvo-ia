from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List


class EventBus:
    def __init__(self):
        self._handlers: DefaultDict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]):
        self._handlers[topic].append(handler)

    def publish(self, topic: str, payload: Dict[str, Any]):
        for handler in self._handlers.get(topic, []):
            handler(payload)
