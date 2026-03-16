import json
import os
from datetime import datetime
from typing import Any, Dict, List

from core.agent_manifest import load_manifest, write_manifest
from core.metrics_manager import summary
from core.self_improvement import list_suggestions

EVOLUTION_FILE = "memory/agent_evolution.json"


def _ensure_store():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(EVOLUTION_FILE):
        with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
            json.dump({"cycles": []}, f, indent=2, ensure_ascii=False)


def _load() -> Dict[str, Any]:
    _ensure_store()
    with open(EVOLUTION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: Dict[str, Any]):
    with open(EVOLUTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _agent_stats_from_suggestions(limit: int = 200) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in list_suggestions(limit=limit):
        agent = str(item.get("agent", "")).strip()
        if not agent:
            continue
        counts[agent] = counts.get(agent, 0) + 1
    return counts


def _health_score(total_events: int, failures: int, feedback_hits: int) -> float:
    if total_events <= 0:
        return 0.5
    fail_rate = failures / total_events
    penalty = min(0.4, feedback_hits * 0.02)
    score = max(0.0, min(1.0, 1.0 - fail_rate - penalty))
    return round(score, 3)


def run_evolution_cycle(agents: List[str]) -> Dict[str, Any]:
    metrics = summary()
    feedback_counts = _agent_stats_from_suggestions()

    by_agent = metrics.get("by_agent", {})
    total_events = int(metrics.get("total_events", 0) or 0)
    total_failures = int(metrics.get("failed", 0) or 0)

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "global": {
            "total_events": total_events,
            "failed": total_failures,
            "avg_latency_ms": metrics.get("avg_latency_ms", 0),
        },
        "agents": [],
    }

    for agent_name in sorted(set(agents)):
        events_for_agent = int(by_agent.get(agent_name, 0) or 0)
        estimated_failures = int(total_failures * (events_for_agent / total_events)) if total_events else 0
        feedback_hits = feedback_counts.get(agent_name, 0)

        health = _health_score(events_for_agent, estimated_failures, feedback_hits)
        recommendation = "stable"
        if health < 0.45:
            recommendation = "needs_prompt_hardening"
        if feedback_hits >= 5:
            recommendation = "consider_specialist_or_split_role"

        report["agents"].append(
            {
                "agent": agent_name,
                "events": events_for_agent,
                "feedback_hits": feedback_hits,
                "health_score": health,
                "recommendation": recommendation,
            }
        )

        _write_manifest_evolution(agent_name, health, recommendation, feedback_hits)

    data = _load()
    data.setdefault("cycles", []).append(report)
    _save(data)
    return report


def _write_manifest_evolution(agent_name: str, health: float, recommendation: str, feedback_hits: int):
    manifest = load_manifest(agent_name)
    if not manifest:
        return

    updated = {
        **manifest,
        "evolution": {
            "health_score": health,
            "recommendation": recommendation,
            "feedback_hits": feedback_hits,
            "updated_at": datetime.utcnow().isoformat(),
        },
    }
    try:
        write_manifest(agent_name, updated)
    except Exception:
        # No interrumpir el runtime por manifest legacy o inválido.
        return
