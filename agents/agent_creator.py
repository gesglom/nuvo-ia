import os
from datetime import datetime

from core.agent_manifest import write_manifest
from core.base_agent import BaseAgent

EVOLUTION_LOG = "memory/factory_evolution.log"


class AgentCreatorAgent(BaseAgent):
    """Crea agentes especialistas on-demand y los registra en el ecosistema."""

    def execute(self, goal):
        return self.create_specialist_agent(goal)

    def create_specialist_agent(self, specialty: str):
        module_name = self._build_module_name(specialty)
        class_name = self._build_class_name(module_name)
        file_path = os.path.join("agents", f"{module_name}.py")

        if not os.path.exists(file_path):
            code = self._render_agent_code(class_name, specialty, module_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

        manifest = {
            "role": f"Especialista en {specialty}",
            "goal": f"Resolver bloqueos técnicos relacionados con {specialty}",
            "backstory": "Agente generado de forma autónoma por la fábrica Nuvo para eliminar cuellos de botella.",
            "tools_required": ["route_llm", "shared_context"],
            "provider_preference": "agnostic",
        }
        manifest_path = write_manifest(module_name, manifest)
        self._log_evolution(module_name, specialty, manifest_path)

        return {
            "status": "created",
            "agent": module_name,
            "class": class_name,
            "file": file_path,
            "manifest": manifest_path,
        }

    def _render_agent_code(self, class_name: str, specialty: str, module_name: str):
        return f'''from core.base_agent import BaseAgent
from core.context_manager import summarize_recent
from core.provider_router import route_llm


class {class_name}(BaseAgent):

    def execute(self, goal):
        context = summarize_recent()
        prompt = f"""
Eres un especialista en {specialty} dentro de una fábrica de software multi-agente.

Debes resolver la tarea de forma concreta, segura y accionable.

Contexto reciente del proyecto:
{{context}}

Tarea:
{{goal}}
"""
        return route_llm("{module_name}", prompt)
'''

    def _build_module_name(self, specialty: str):
        base = specialty.lower().strip().replace(" ", "_")
        safe = "".join(c for c in base if c.isalnum() or c == "_")
        safe = safe.strip("_") or "specialist"
        if not safe.endswith("_agent"):
            safe = f"{safe}_agent"
        return safe

    def _build_class_name(self, module_name: str):
        return "".join(part.capitalize() for part in module_name.split("_"))

    def _log_evolution(self, module_name: str, specialty: str, manifest_path: str):
        os.makedirs("memory", exist_ok=True)
        with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.utcnow().isoformat()} | created_agent={module_name} | specialty={specialty} | manifest={manifest_path}\n"
            )
