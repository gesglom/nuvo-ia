import json
import os
from typing import Optional
from urllib import error, request


DEFAULT_TIMEOUT = int(os.getenv("NUVO_LLM_TIMEOUT", "120"))


class LLMError(Exception):
    pass


def _post_json(url: str, payload: dict, headers: Optional[dict] = None) -> dict:
    raw = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=raw,
        headers={"content-type": "application/json", **(headers or {})},
        method="POST",
    )
    with request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _provider_from_env() -> str:
    return os.getenv("NUVO_LLM_PROVIDER", "ollama").strip().lower()


def _call_ollama(prompt: str) -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    data = _post_json(url, {"model": model, "prompt": prompt, "stream": False})
    return data.get("response", "")


def _call_openai_compatible(prompt: str, base_url: str, api_key: str, model: str) -> str:
    data = _post_json(
        f"{base_url.rstrip('/')}/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return data["choices"][0]["message"]["content"]


def _call_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMError("OPENAI_API_KEY no configurado")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return _call_openai_compatible(prompt, base_url, api_key, model)


def _call_openai_compatible_custom(prompt: str) -> str:
    api_key = os.getenv("OPENAI_COMPAT_API_KEY")
    if not api_key:
        raise LLMError("OPENAI_COMPAT_API_KEY no configurado")

    base_url = os.getenv("OPENAI_COMPAT_BASE_URL")
    model = os.getenv("OPENAI_COMPAT_MODEL")

    if not base_url or not model:
        raise LLMError("OPENAI_COMPAT_BASE_URL y OPENAI_COMPAT_MODEL son requeridos")

    return _call_openai_compatible(prompt, base_url, api_key, model)


def _call_anthropic(prompt: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMError("ANTHROPIC_API_KEY no configurado")

    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
    data = _post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "model": model,
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": prompt}],
        },
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    content = data.get("content", [])
    if content and isinstance(content, list):
        return "".join(block.get("text", "") for block in content if block.get("type") == "text")
    return ""


def _call_localdev(prompt: str) -> str:
    lower = prompt.lower()

    if "responde solo con una lista separada por comas" in lower:
        return "architect_agent, backend_engineer, frontend_engineer, security_auditor"

    if "file:" in lower and "codigo" in lower:
        return (
            "FILE: app/main.py\n"
            "CODE:\n"
            "from fastapi import FastAPI\n\n"
            "app = FastAPI(title='Nuvo API')\n\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return {'status': 'ok'}\n"
        )

    if "arquitecto senior de software" in lower:
        return (
            "Arquitectura propuesta:\n"
            "- backend FastAPI en /app\n"
            "- frontend Next.js en /frontend\n"
            "- capa de agentes en /agents\n"
            "- memoria y métricas en /memory\n"
        )

    if "ingeniero frontend" in lower:
        return (
            "1) Estructura: frontend/app, frontend/components, frontend/lib\n"
            "2) Componentes: TaskBoard, AgentStatus, LogStream\n"
            "3) Páginas: /, /jobs/[id], /settings\n"
            "4) Integración: fetch a /api/jobs y /api/metrics\n"
        )

    return (
        "Modo localdev activo.\n"
        "Entrega incremental recomendada: crear endpoint /health, cola de jobs y runner básico."
    )


def ask_llm(prompt: str, provider: Optional[str] = None) -> str:
    selected = (provider or _provider_from_env()).lower()

    try:
        if selected == "ollama":
            return _call_ollama(prompt)
        if selected == "openai":
            return _call_openai(prompt)
        if selected in {"openai_compatible", "openai-compat", "compat"}:
            return _call_openai_compatible_custom(prompt)
        if selected == "anthropic":
            return _call_anthropic(prompt)
        if selected in {"localdev", "mock", "local"}:
            return _call_localdev(prompt)
    except error.URLError as exc:
        return f"Error conectando con proveedor '{selected}': {exc}"
    except LLMError as exc:
        return f"Configuración inválida para proveedor '{selected}': {exc}"
    except Exception as exc:
        return f"Error inesperado en proveedor '{selected}': {exc}"

    return (
        f"Proveedor '{selected}' no soportado. "
        "Usa NUVO_LLM_PROVIDER=ollama|openai|openai_compatible|anthropic|localdev"
    )


def provider_status():
    return {
        "default_provider": _provider_from_env(),
        "fallbacks": [x.strip() for x in os.getenv("NUVO_LLM_FALLBACKS", "").split(",") if x.strip()],
        "providers": {
            "ollama": {
                "configured": bool(os.getenv("OLLAMA_URL")),
                "model": os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b"),
            },
            "openai": {
                "configured": bool(os.getenv("OPENAI_API_KEY")),
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            },
            "openai_compatible": {
                "configured": bool(os.getenv("OPENAI_COMPAT_API_KEY") and os.getenv("OPENAI_COMPAT_BASE_URL") and os.getenv("OPENAI_COMPAT_MODEL")),
                "model": os.getenv("OPENAI_COMPAT_MODEL", ""),
            },
            "anthropic": {
                "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
                "model": os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"),
            },
            "localdev": {
                "configured": True,
                "model": "rule-based",
            },
        },
    }
