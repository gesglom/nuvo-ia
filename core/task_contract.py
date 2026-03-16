import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

VALID_STATUS = {"pending", "running", "failed", "done"}


@dataclass
class TaskContract:
    owner_agent: str
    input: str
    expected_output: str = ""
    status: str = "pending"
    retries: int = 0
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    output: str = ""
    error: str = ""
    provider_used: str = ""
    latency_ms: int = 0
    priority: int = 100

    def validate(self):
        if not self.owner_agent:
            raise ValueError("owner_agent es requerido")
        if self.status not in VALID_STATUS:
            raise ValueError(f"status inválido: {self.status}")
        if type(self.priority) is not int:
            raise ValueError("priority debe ser un entero")
        if self.priority < 0:
            raise ValueError("priority debe ser mayor o igual a 0")

    def to_dict(self) -> Dict[str, Any]:
        self.validate()
        return {
            "task_id": self.task_id,
            "owner_agent": self.owner_agent,
            "input": self.input,
            "expected_output": self.expected_output,
            "status": self.status,
            "retries": self.retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "output": self.output,
            "error": self.error,
            "provider_used": self.provider_used,
            "latency_ms": self.latency_ms,
            "priority": self.priority,
        }

    @staticmethod
    def _normalize_priority(value: Any) -> int:
        if type(value) is int:
            return value
        if isinstance(value, str) and value.strip().isdigit():
            return int(value.strip())
        raise ValueError("priority inválido; debe ser entero")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        obj = cls(
            task_id=data.get("task_id", str(uuid.uuid4())),
            owner_agent=data.get("owner_agent", ""),
            input=data.get("input", ""),
            expected_output=data.get("expected_output", ""),
            status=data.get("status", "pending"),
            retries=data.get("retries", 0),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
            output=data.get("output", ""),
            error=data.get("error", ""),
            provider_used=data.get("provider_used", ""),
            latency_ms=data.get("latency_ms", 0),
            priority=cls._normalize_priority(data.get("priority", 100)),
        )
        obj.validate()
        return obj
