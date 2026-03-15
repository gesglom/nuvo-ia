import json
import os
from datetime import datetime

METRICS_FILE = "memory/metrics.json"


def _ensure():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump({"events": []}, f, indent=2, ensure_ascii=False)


def _load():
    _ensure()
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_metric(agent: str, provider: str, status: str, latency_ms: int, tokens_estimated: int = 0):
    data = _load()
    data["events"].append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "provider": provider or "default",
            "status": status,
            "latency_ms": latency_ms,
            "tokens_estimated": tokens_estimated,
        }
    )
    _save(data)


def summary():
    events = _load().get("events", [])
    total = len(events)
    success = sum(1 for e in events if e.get("status") == "done")
    failed = sum(1 for e in events if e.get("status") == "failed")
    avg_latency = int(sum(e.get("latency_ms", 0) for e in events) / total) if total else 0
    by_agent = {}
    for e in events:
        by_agent.setdefault(e.get("agent"), 0)
        by_agent[e.get("agent")] += 1
    return {
        "total_events": total,
        "success": success,
        "failed": failed,
        "avg_latency_ms": avg_latency,
        "by_agent": by_agent,
    }
