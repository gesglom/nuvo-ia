import os

from core.agent_manifest import load_manifest
from core.llm_client import ask_llm


def _fallbacks():
    raw = os.getenv("NUVO_LLM_FALLBACKS", "")
    return [x.strip().lower() for x in raw.split(",") if x.strip()]


def choose_provider(agent_module_name: str):
    manifest = load_manifest(agent_module_name) or {}
    preferred = str(manifest.get("provider_preference", "")).strip().lower()
    if preferred and preferred != "agnostic":
        return preferred
    return None


def route_llm(agent_module_name: str, prompt: str):
    preferred = choose_provider(agent_module_name)

    # Intenta primero preferido/default, luego fallback chain
    providers = [preferred] if preferred else [None]
    providers.extend(_fallbacks())

    last_error = None
    for provider in providers:
        response = ask_llm(prompt, provider=provider)
        if isinstance(response, str) and response.startswith("Error"):
            last_error = response
            continue
        return response

    return last_error or "Error: no se pudo obtener respuesta de ningún proveedor"
