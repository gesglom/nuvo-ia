import importlib
import os

from core.base_agent import BaseAgent

AGENTS_FOLDER = "agents"


def load_agents():
    """Carga agentes de forma dinámica (hot-loading) en cada invocación."""
    importlib.invalidate_caches()
    agents = {}

    for file in os.listdir(AGENTS_FOLDER):
        if not file.endswith(".py") or file.startswith("_"):
            continue

        module_name = file[:-3]
        fqmn = f"agents.{module_name}"

        try:
            module = importlib.import_module(fqmn)
            module = importlib.reload(module)
        except Exception as exc:
            print(f"No se pudo cargar módulo {fqmn}: {exc}")
            continue

        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, BaseAgent) and obj is not BaseAgent:
                agents[module_name] = obj()
                break

    return agents
