import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib import error, request

from core.context_manager import add_context_event, summarize_recent

MEMORY_TRACE_FILE = "memory/memory_fabric.json"


def _ensure_trace_store():
    os.makedirs("memory", exist_ok=True)
    if not os.path.exists(MEMORY_TRACE_FILE):
        with open(MEMORY_TRACE_FILE, "w", encoding="utf-8") as f:
            json.dump({"queries": [], "writes": []}, f, indent=2, ensure_ascii=False)


def _load_trace() -> Dict[str, Any]:
    _ensure_trace_store()
    with open(MEMORY_TRACE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_trace(data: Dict[str, Any]):
    with open(MEMORY_TRACE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _engram_enabled() -> bool:
    return os.getenv("NUVO_MEMORY_PROVIDER", "local").strip().lower() == "engram"


def _engram_base_url() -> str:
    return os.getenv("ENGRAM_API_URL", "").strip().rstrip("/")


def _engram_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    base_url = _engram_base_url()
    if not base_url:
        raise RuntimeError("ENGRAM_API_URL no configurado")

    api_key = os.getenv("ENGRAM_API_KEY", "").strip()
    headers = {"content-type": "application/json"}
    if api_key:
        headers["authorization"] = f"Bearer {api_key}"

    raw = json.dumps(payload).encode("utf-8")
    req = request.Request(f"{base_url}{path}", data=raw, headers=headers, method="POST")
    with request.urlopen(req, timeout=int(os.getenv("ENGRAM_TIMEOUT", "20"))) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _trace_query(query: str, agent: Optional[str], provider: str, hit_count: int):
    data = _load_trace()
    data.setdefault("queries", []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "agent": agent,
            "provider": provider,
            "hits": hit_count,
        }
    )
    _save_trace(data)


def _trace_write(agent: str, task: str, status: str, provider: str):
    data = _load_trace()
    data.setdefault("writes", []).append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "task": task,
            "status": status,
            "provider": provider,
        }
    )
    _save_trace(data)


def retrieve_context(query: str, agent: Optional[str] = None, limit: int = 6) -> str:
    if _engram_enabled():
        try:
            response = _engram_post(
                "/retrieve",
                {
                    "query": query,
                    "agent": agent,
                    "limit": limit,
                },
            )
            chunks = response.get("items", [])
            lines = []
            for item in chunks[:limit]:
                text = str(item.get("text", "")).strip()
                if text:
                    lines.append(text)
            _trace_query(query, agent, "engram", len(lines))
            if lines:
                return "\n".join(lines)
        except (error.URLError, RuntimeError, Exception):
            # fallback local sin romper ejecución
            pass

    local = summarize_recent(limit=limit)
    _trace_query(query, agent, "local", len(local.splitlines()) if local else 0)
    return local


def store_episode(
    agent: str,
    task: str,
    result: str,
    status: str = "completed",
    metadata: Optional[Dict[str, Any]] = None,
):
    if _engram_enabled():
        try:
            _engram_post(
                "/store",
                {
                    "agent": agent,
                    "task": task,
                    "result": (result or "")[:5000],
                    "status": status,
                    "metadata": metadata or {},
                },
            )
            _trace_write(agent, task, status, "engram")
            return
        except (error.URLError, RuntimeError, Exception):
            pass

    add_context_event(agent, task, result, status=status)
    _trace_write(agent, task, status, "local")
